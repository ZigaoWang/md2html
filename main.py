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
    md_file_path = input("Enter the path to your Markdown file: ")
    if not os.path.isfile(md_file_path):
        print("File not found. Please check the path and try again.")
        return

    css_path = 'style.css'  # Default CSS file
    css_content = ""
    if os.path.isfile(css_path):
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css_content = css_file.read()

    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()
    html = convert_md_to_html(md_text)
    styled_html = add_custom_style(html, css_content)

    output_file = input("Enter the name of the output HTML file (e.g., index.html): ")
    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(styled_html)
    print(f"Markdown converted to HTML successfully! Output saved to {output_file}")

if __name__ == "__main__":
    main()
