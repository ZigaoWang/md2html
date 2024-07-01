import os
import markdown
from bs4 import BeautifulSoup


def convert_md_to_html(md_text):
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, 'lxml')
    return soup.prettify()


def add_custom_style(html_content, css_content=None):
    if css_content:
        styled_html = f"<style>{css_content}</style>\n{html_content}"
        return styled_html
    return html_content


def main():
    print("Markdown to HTML Converter\n")

    while True:
        md_file_path = input("Enter the path to your Markdown file (default: README.md): ").strip()
        if not md_file_path:
            md_file_path = 'README.md'
        if os.path.isfile(md_file_path):
            break
        else:
            print("File not found. Please check the path and try again.")

    css_path = 'style.css'
    css_content = ""
    if os.path.isfile(css_path):
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css_content = css_file.read()

    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()
    html = convert_md_to_html(md_text)
    styled_html = add_custom_style(html, css_content)

    while True:
        output_file = input("Enter the name of the output HTML file (default: index.html): ").strip()
        if not output_file:
            output_file = 'index.html'
        if not output_file.endswith('.html'):
            print("Please enter a valid HTML file name.")
        else:
            break

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(styled_html)
    print(f"\nMarkdown converted to HTML successfully! Output saved to {output_file}")


if __name__ == "__main__":
    main()
