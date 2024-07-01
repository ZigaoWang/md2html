import argparse
import markdown
from bs4 import BeautifulSoup

def convert_md_to_html(md_text):
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, 'lxml')
    return soup.prettify()

def add_custom_style(html_content, css_path=None):
    if css_path:
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css = css_file.read()
        styled_html = f"<style>{css}</style>\n{html_content}"
        return styled_html
    return html_content

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML.')
    parser.add_argument('markdown_file', type=str, help='Path to the Markdown file.')
    parser.add_argument('--css', type=str, help='Path to the CSS file (optional).')
    parser.add_argument('--output', type=str, default='output.html', help='Output HTML file (default: output.html).')
    args = parser.parse_args()

    with open(args.markdown_file, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()
    html = convert_md_to_html(md_text)
    styled_html = add_custom_style(html, args.css)
    with open(args.output, 'w', encoding='utf-8') as html_file:
        html_file.write(styled_html)
    print(f"Markdown converted to HTML successfully! Output saved to {args.output}")

if __name__ == "__main__":
    main()
