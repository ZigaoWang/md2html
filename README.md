# MD2HTML - Markdown to HTML Converter

```txt
   __  ______    ___    __ __________  _____ 
  /  |/  / _ \  |_  |  / // /_  __/  |/  / / 
 / /|_/ / // / / __/  / _  / / / / /|_/ / /__
/_/  /_/____/ /____/ /_//_/ /_/ /_/  /_/____/
```

MD2HTML is a powerful and easy-to-use command-line tool for converting Markdown files into beautifully styled HTML documents. It supports syntax highlighting, custom CSS, and includes handy features like copy-to-clipboard buttons for code blocks.

## Features

- **Syntax Highlighting:** Converts code blocks into beautifully highlighted code using Pygments.
- **Custom CSS:** Apply your custom CSS styles to the output HTML.
- **Light/Dark Mode:** Easily switch between light and dark themes.
- **Copy-to-Clipboard Buttons:** Adds copy buttons to code blocks for easy copying.
- **MathJax Support:** Automatically includes MathJax for rendering mathematical expressions.

## Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/ZigaoWang/md2html.git
    cd md2html
    ```

2. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command-Line Arguments

MD2HTML can be used directly from the command line with various options.

```sh
python md2html.py -i <input_file> -o <output_file> -d <output_dir> -c <css_file> -m <mode>
```

#### Arguments

- `-i`, `--input_file`: Path to the input Markdown file. (Required)
- `-o`, `--output_file`: Name of the output HTML file. Default is `output.html`.
- `-d`, `--output_dir`: Directory where the output HTML file will be saved. Default is the current directory.
- `-c`, `--css_file`: Path to a custom CSS file. (Optional)
- `-m`, `--mode`: Choose mode (`light`/`dark`). Default is `light`.

### Interactive Prompt

If no arguments are provided, MD2HTML will prompt you for the necessary inputs interactively.

```sh
python md2html.py
```

### Example

```sh
python md2html.py -i example.md -o example.html -d ./output -m dark
```

## Custom CSS

You can provide your CSS file using the `-c` or `--css_file` argument. If not provided, the tool will use default styles (`style_light.css` or `style_dark.css`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## Acknowledgements

- **Markdown:** [Python-Markdown](https://github.com/Python-Markdown/markdown)
- **Syntax Highlighting:** [Pygments](https://pygments.org/)
- **HTML Parsing:** [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## Author

Made with 💜 by [Zigao Wang](https://zigao.wang)
