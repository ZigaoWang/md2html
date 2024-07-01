import os
import argparse
import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from emoji_extension import EmojiExtension  # Import the custom emoji extension


def print_logo():
    logo = r"""
   __  ______    ___    __ __________  _____ 
  /  |/  / _ \  |_  |  / // /_  __/  |/  / / 
 / /|_/ / // / / __/  / _  / / / / /|_/ / /__
/_/  /_/____/ /____/ /_//_/ /_/ /_/  /_/____/
    """
    print("--------------------------------------------------")
    print(logo)
    print("MD2HTML - Markdown to HTML converter")
    print("Made with 💜 by Zigao Wang.")
    print("This project is licensed under MIT License.")
    print("GitHub Repo: https://github.com/ZigaoWang/md2html/")
    print("--------------------------------------------------")


def convert_md_to_html(md_text, light_mode=True):
    html = markdown.markdown(md_text,
                             extensions=['fenced_code', 'tables', 'toc', 'footnotes', 'attr_list', 'md_in_html', 'extra', 'sane_lists', 'smarty', 'codehilite', EmojiExtension()])
    soup = BeautifulSoup(html, 'lxml')

    # Add syntax highlighting and copy button to code blocks
    for code in soup.find_all('code'):
        parent = code.parent
        if parent.name == 'pre' and code.string:
            language = code.get('class', [''])[0].replace('language-', '') or 'text'
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(style='default' if light_mode else 'monokai')
            highlighted_code = highlight(code.string, lexer, formatter)
            code.replace_with(BeautifulSoup(highlighted_code, 'lxml'))

            copy_button_html = '''
            <div class="code-header">
                <span class="language-label">{}</span>
                <button class="copy-button" onclick="copyCode(this)">
                    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon">
                        <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path>
                        <path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
                    </svg>
                </button>
            </div>
            '''.format(language)
            parent.insert_before(BeautifulSoup(copy_button_html, 'lxml'))

    return soup.prettify()


def add_custom_style(html_content, css_content=None):
    if css_content:
        styled_html = f"<style>{css_content}</style>\n{html_content}"
    else:
        styled_html = html_content

    footer = """
    <footer>
        <p>Powered by <a href="https://github.com/ZigaoWang/md2html/">MD2HTML</a> by <a href="https://zigao.wang">Zigao Wang</a></p>
    </footer>
    """

    copy_button_script = """
    <script>
    function copyCode(button) {
        const code = button.closest('.code-header').nextElementSibling.innerText;
        navigator.clipboard.writeText(code).then(() => {
            button.innerHTML = '<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-check"><path fill-rule="evenodd" d="M13.78 3.22a.75.75 0 0 1 0 1.06l-7.5 7.5a.75.75 0 0 1-1.06 0l-3.5-3.5a.75.75 0 0 1 1.06-1.06L6 10.44l7.22-7.22a.75.75 0 0 1 1.06 0z"></path></svg>';
            setTimeout(() => { 
                button.innerHTML = '<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg>';
            }, 2000);
        });
    }
    </script>
    """

    mathjax_script = """
    <script>
    (function () {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
        document.head.appendChild(script);
    })();
    </script>
    """

    return styled_html + footer + copy_button_script + mathjax_script


def prompt_based_conversion():
    while True:
        md_file_path = input("Enter the path to your Markdown file (or 'q' to quit): ").strip()
        if md_file_path.lower() == 'q':
            print("Goodbye!")
            break
        if not os.path.isfile(md_file_path):
            print("File not found. Please check the path and try again.")
            continue

        light_mode = input("Choose mode (light/dark, default is light): ").strip().lower() != 'dark'
        css_path = 'style_light.css' if light_mode else 'style_dark.css'
        css_content = ""
        if os.path.isfile(css_path):
            with open(css_path, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()

        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            md_text = md_file.read()

        html = convert_md_to_html(md_text, light_mode=light_mode)
        styled_html = add_custom_style(html, css_content)

        output_file = input("Enter the name of the output HTML file (default: output.html): ").strip() or 'output.html'
        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(styled_html)
        print(f"Markdown converted to HTML successfully! Output saved to {output_file}")
        break


def arg_based_conversion(args):
    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return

    light_mode = args.mode.lower() != 'dark'
    css_path = 'style_light.css' if light_mode else 'style_dark.css'
    css_content = ""
    if os.path.isfile(css_path):
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css_content = css_file.read()

    with open(args.input_file, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()

    html = convert_md_to_html(md_text, light_mode=light_mode)
    styled_html = add_custom_style(html, css_content)

    output_path = os.path.join(args.output_dir, args.output_file)
    with open(output_path, 'w', encoding='utf-8') as html_file:
        html_file.write(styled_html)

    print(f"Markdown converted to HTML successfully! Output saved to {output_path}")


def main():
    print_logo()

    parser = argparse.ArgumentParser(description="Convert Markdown files to HTML.")
    parser.add_argument("-i", "--input_file", help="Path to the input Markdown file.")
    parser.add_argument("-o", "--output_file", default="output.html", help="Name of the output HTML file.")
    parser.add_argument("-d", "--output_dir", default=".", help="Directory where the output HTML file will be saved.")
    parser.add_argument("-c", "--css_file", help="Path to a custom CSS file.")
    parser.add_argument("-m", "--mode", default="light", help="Choose mode (light/dark). Default is light.")

    args = parser.parse_args()

    if args.input_file:
        arg_based_conversion(args)
    else:
        prompt_based_conversion()


if __name__ == "__main__":
    main()