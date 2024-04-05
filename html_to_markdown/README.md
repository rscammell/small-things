# html_to_markdown

A fast, simple HTML to [Markdown](https://daringfireball.net/projects/markdown/) converter utility.

html_to_markdown is easy to use:

```python html_to_markdown.py --infile <HTML file to process> --outfile <Markdown file to output>```

Additional flags for debugging (```--debug```) and link removal (```--omitlinks```) are also provided.

The tool requires [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), which can be installed via pip.

Planned enhancements include expanding the set of tags that are converted into Markdown, however the current version produces clean, usable output even with very complex HTML documents.

html_to_markdown is offered under the 3-clause BSD license included in [LICENSE.md](LICENSE.md)
Contributions from the community welcomed!