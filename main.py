import argparse
import os
import markdown
from markdown.extensions import Extension
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from bs4 import BeautifulSoup

LOGO = r"""
   __  ______    ___    __ __________  _____ 
  /  |/  / _ \  |_  |  / // /_  __/  |/  / / 
 / /|_/ / // / / __/  / _  / / / / /|_/ / /__
/_/  /_/____/ /____/ /_//_/ /_/ /_/  /_/____/
"""

FOOTER = """
<footer>
    <p>Powered by <a href="https://github.com/ZigaoWang/md2html/">MD2HTML</a></p>
</footer>
"""

COPY_BUTTON_SCRIPT = """
<script>
function copyCode(button) {
    const code = button.closest('.code-header').nextElementSibling.innerText;
    navigator.clipboard.writeText(code).then(() => {
        button.innerHTML = 'Copied!';
        setTimeout(() => { button.innerHTML = 'Copy'; }, 2000);
    });
}
</script>
"""

MATHJAX_SCRIPT = """
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
"""


def print_logo():
    print(LOGO)
    print("MD2HTML - Markdown to HTML converter")
    print("Made with 💜 by Zigao Wang.")
    print("GitHub Repo: https://github.com/ZigaoWang/md2html/")


def convert_md_to_html(md_text, css_mode):
    extensions = [
        'fenced_code', 'tables', 'footnotes', 'attr_list', 'extra', 'sane_lists', 'smarty', 'codehilite'
    ]
    html = markdown.markdown(md_text, extensions=extensions)
    soup = BeautifulSoup(html, 'html.parser')

    for code in soup.find_all('code'):
        parent = code.parent
        if parent.name == 'pre' and code.string:
            language = code.get('class', [''])[0].replace('language-', '') or 'text'
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(style='default')
            highlighted_code = highlight(code.string, lexer, formatter)
            code.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))

            copy_button_html = f'''
            <div class="code-header">
                <span class="language-label">{language}</span>
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
            </div>
            '''
            parent.insert_before(BeautifulSoup(copy_button_html, 'html.parser'))

    css_file = "css/github-markdown.css"
    if css_mode == "only dark":
        css_file = "css/github-markdown-dark.css"
    elif css_mode == "only light":
        css_file = "css/github-markdown-light.css"

    css_content = read_file(css_file)

    return soup.prettify(), css_content


def add_custom_style(html_content, css_content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Markdown to HTML</title>
        <style>{css_content}</style>
        {HtmlFormatter().get_style_defs('.highlight')}
    </head>
    <body>
        {html_content}
        {FOOTER}
        {COPY_BUTTON_SCRIPT}
        {MATHJAX_SCRIPT}
    </body>
    </html>
    """


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def choose_css_mode():
    mode = input("Choose CSS mode (auto/only dark/only light, default is auto): ").strip().lower()
    if mode not in ["auto", "only dark", "only light"]:
        mode = "auto"
    return mode


def prompt_based_conversion():
    while True:
        md_file_path = input("Enter the path to your Markdown file (or 'q' to quit): ").strip()
        if md_file_path.lower() == 'q':
            print("Goodbye!")
            break
        if not os.path.isfile(md_file_path):
            print("File not found. Please check the path and try again.")
            continue

        css_mode = choose_css_mode()
        md_text = read_file(md_file_path)

        html, css_content = convert_md_to_html(md_text, css_mode)
        styled_html = add_custom_style(html, css_content)

        output_file = input("Enter the name of the output HTML file (default: output.html): ").strip() or 'output.html'
        write_file(output_file, styled_html)
        print(f"Markdown converted to HTML successfully! Output saved to {output_file}")
        break


def arg_based_conversion(args):
    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return

    css_mode = args.mode.lower()
    md_text = read_file(args.input_file)

    html, css_content = convert_md_to_html(md_text, css_mode)
    styled_html = add_custom_style(html, css_content)

    output_path = os.path.join(args.output_dir, args.output_file)
    write_file(output_path, styled_html)

    print(f"Markdown converted to HTML successfully! Output saved to {output_path}")


def main():
    print_logo()

    parser = argparse.ArgumentParser(description="Convert Markdown files to HTML.")
    parser.add_argument("-i", "--input_file", help="Path to the input Markdown file.")
    parser.add_argument("-o", "--output_file", default="output.html", help="Name of the output HTML file.")
    parser.add_argument("-d", "--output_dir", default=".", help="Directory where the output HTML file will be saved.")
    parser.add_argument("-m", "--mode", default="auto",
                        help="Choose CSS mode (auto/only dark/only light). Default is auto.")

    args = parser.parse_args()

    if args.input_file:
        arg_based_conversion(args)
    else:
        prompt_based_conversion()


if __name__ == "__main__":
    main()
