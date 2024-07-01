import argparse
import os
import xml.etree.ElementTree as etree
import markdown
from bs4 import BeautifulSoup
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from emoji_extension import EmojiExtension

LOGO = r"""
   __  ______    ___    __ __________  _____ 
  /  |/  / _ \  |_  |  / // /_  __/  |/  / / 
 / /|_/ / // / / __/  / _  / / / / /|_/ / /__
/_/  /_/____/ /____/ /_//_/ /_/ /_/  /_/____/
"""

FOOTER = """
<footer>
    <p>Powered by <a href="https://github.com/ZigaoWang/md2html/">MD2HTML</a> by <a href="https://zigao.wang">Zigao Wang</a></p>
</footer>
"""

COPY_BUTTON_SCRIPT = """
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
    print("--------------------------------------------------")
    print(LOGO)
    print("MD2HTML - Markdown to HTML converter")
    print("Made with 💜 by Zigao Wang.")
    print("This project is licensed under MIT License.")
    print("GitHub Repo: https://github.com/ZigaoWang/md2html/")
    print("--------------------------------------------------")

class TaskListExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(TaskListTreeprocessor(md), 'tasklist', 25)

class TaskListTreeprocessor(Treeprocessor):
    def run(self, root):
        for ul in root.iter('ul'):
            for li in list(ul):
                if li.text and (li.text.startswith('[ ] ') or li.text.startswith('[x] ')):
                    new_li = etree.Element('li')
                    checkbox = etree.Element('input')
                    checkbox.set('type', 'checkbox')
                    checkbox.set('disabled', 'disabled')

                    if li.text.startswith('[x] '):
                        checkbox.set('checked', 'checked')

                    new_li.append(checkbox)
                    new_li.text = li.text[3:]

                    ul.remove(li)
                    ul.append(new_li)

class TocExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(TocTreeprocessor(md), 'toc', 30)

class TocTreeprocessor(Treeprocessor):
    def run(self, root):
        toc_html = etree.Element('div', {'class': 'toc'})
        toc_title = etree.SubElement(toc_html, 'h2')
        toc_title.text = 'Table of Contents'
        toc_list = etree.SubElement(toc_html, 'ul')

        for header in root.iter():
            if header.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(header.tag[1])
                if 'id' not in header.attrib:
                    header.set('id', header.text.replace(' ', '-').lower())
                toc_item = etree.SubElement(toc_list, 'li', {'class': f'toc-level-{level}'})
                toc_link = etree.SubElement(toc_item, 'a', {'href': f'#{header.get("id")}'})
                toc_link.text = header.text

        for el in root.iter():
            if el.tag == 'p' and el.text and '[toc]' in el.text.lower():
                el.clear()
                el.append(toc_html)

        return root

def convert_md_to_html(md_text, light_mode=True):
    extensions = [
        'fenced_code', 'tables', 'footnotes', 'attr_list', 'md_in_html', 'extra', 'sane_lists', 'smarty', 'codehilite',
        EmojiExtension(), TaskListExtension(), TocExtension()
    ]
    html = markdown.markdown(md_text, extensions=extensions)
    soup = BeautifulSoup(html, 'html.parser')

    for code in soup.find_all('code'):
        parent = code.parent
        if parent.name == 'pre' and code.string:
            language = code.get('class', [''])[0].replace('language-', '') or 'text'
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(style='default' if light_mode else 'monokai')
            highlighted_code = highlight(code.string, lexer, formatter)
            code.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))

            copy_button_html = f'''
            <div class="code-header">
                <span class="language-label">{language}</span>
                <button class="copy-button" onclick="copyCode(this)">
                    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon">
                        <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path>
                        <path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
                    </svg>
                </button>
            </div>
            '''
            parent.insert_before(BeautifulSoup(copy_button_html, 'html.parser'))

    return soup.prettify()

def add_custom_style(html_content, css_content=None):
    styled_html = f"<style>{css_content}</style>\n{html_content}" if css_content else html_content
    return styled_html + FOOTER + COPY_BUTTON_SCRIPT + MATHJAX_SCRIPT

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def choose_mode():
    return input("Choose mode (light/dark, default is light): ").strip().lower() != 'dark'

def get_css_content(light_mode):
    css_path = 'style_light.css' if light_mode else 'style_dark.css'
    return read_file(css_path) if os.path.isfile(css_path) else ""

def prompt_based_conversion():
    while True:
        md_file_path = input("Enter the path to your Markdown file (or 'q' to quit): ").strip()
        if md_file_path.lower() == 'q':
            print("Goodbye!")
            break
        if not os.path.isfile(md_file_path):
            print("File not found. Please check the path and try again.")
            continue

        light_mode = choose_mode()
        css_content = get_css_content(light_mode)
        md_text = read_file(md_file_path)

        html = convert_md_to_html(md_text, light_mode)
        styled_html = add_custom_style(html, css_content)

        output_file = input("Enter the name of the output HTML file (default: output.html): ").strip() or 'output.html'
        write_file(output_file, styled_html)
        print(f"Markdown converted to HTML successfully! Output saved to {output_file}")
        break

def arg_based_conversion(args):
    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return

    light_mode = args.mode.lower() != 'dark'
    css_content = read_file(args.css_file) if args.css_file and os.path.isfile(args.css_file) else get_css_content(light_mode)
    md_text = read_file(args.input_file)

    html = convert_md_to_html(md_text, light_mode)
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
    parser.add_argument("-c", "--css_file", help="Path to a custom CSS file.")
    parser.add_argument("-m", "--mode", default="light", help="Choose mode (light/dark). Default is light.")

    args = parser.parse_args()

    if args.input_file:
        arg_based_conversion(args)
    else:
        prompt_based_conversion()

if __name__ == "__main__":
    main()