#!/usr/bin/env python3
# Convert HTMl to plaintext in markdown format
# (C) 2024 Rupert Scammell <rupert.scammell@gmail.com>
# This software is licensed under the 3-clause BSD license specified at https://opensource.org/license/BSD-3-clause
# Originally written January, 2024
# Current version: https://github.com/rscammell/small-things/tree/main/html_to_markdown

# Dependencies: pip install beautifulsoup4
# TODO - Does not yet convert all tags to appropriate Markdown, but still produces clean and usable output.

from bs4 import BeautifulSoup, Comment, NavigableString
import sys
import argparse
import re

def process_html(html_content, omit_links, debug):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove all comments
    for comments in soup.findAll(string=lambda string:isinstance(string, Comment)):
        comments.extract()
        
    # Remove all script tags, including those with attributes
    for script in soup.find_all("script"):
        script.decompose()
    
    # Remove all noscript tags, including those with attributes
    for script in soup.find_all("noscript"):
        script.decompose()
        
    # Remove all style tags, including those with attributes
    for script in soup.find_all("style"):
        script.decompose()
    
    # Remove all button tags, including those with attributes
    for script in soup.find_all("button"):
        script.decompose()
    
    # Remove all input tags, including those with attributes
    for script in soup.find_all("input"):
        script.decompose()
        
    # Function to handle different tags for markdown conversion
    def handle_tag(tag):
        if tag.name == "b" or tag.name == "strong":
            tag_text = process_tag_children(tag)
            if tag_text is not None and tag_text != "":
                return "**" + "".join(tag_text) + "**"
            else:
                if debug:
                    return "(b-strong)-none-"
                else:
                    return ""
                    
        elif tag.name == "i" or tag.name == "em":
            tag_text = process_tag_children(tag)
            if tag_text is not None and tag_text != "":
                return "*" + "".join(tag_text) + "*"
            else:
                if debug:
                    return "(em)-none-"
                else:
                    return ""
                    
        elif tag.name == "p":
            tag_text = process_tag_children(tag)
            if tag_text is not None and tag_text != "":
                if debug:
                    return "\n(p)" + "".join(tag_text) + "\n(p)"
                else:
                    return "\n" + "".join(tag_text) + "\n"
            else:
                if debug:
                    return "(p)-none-"
                else:
                    return ""
                    
        elif tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(tag.name[1])
            tag_text = process_tag_children(tag)
            if tag_text is not None and tag_text != "":
                if debug:
                    return "#" * level + " " + "".join(tag_text) + "\n(h)"
                else:
                    return "#" * level + " " + "".join(tag_text) + "\n"
            else:
                if debug:
                    return "(h)-none-"
                else:
                    return ""
                    
        elif tag.name == "ul":
            tag_text = process_list_items(tag)
            if tag_text is not None and tag_text != "":
                if debug:
                    return "\n(ul)" + tag_text + "\n(ul)"
                else:
                    return "\n" + tag_text + "\n"
            else:
                if debug:
                    return "(ul)-none-"
                else:
                    return ""
                    
        elif tag.name == "ol":
            if debug:
                return "\n(ol)" + "\n(ol)".join(f"{i+1}. {handle_child(li)}" for i, li in enumerate(tag.find_all("li", recursive=False))) + "\n(li)"
            else:
                return "\n" + "\n".join(f"{i+1}. {handle_child(li)}" for i, li in enumerate(tag.find_all("li", recursive=False))) + "\n"
                
        elif tag.name == "blockquote":
            tag_text = process_list_items(tag)
            if tag_text is not None and tag_text != "":
                if debug:
                    return "> " + "".join(tag_text) + "\n(blockquote)"
                else:
                    return "> " + "".join(tag_text) + "\n"
            else:
                if debug:
                    return "(blockquote)-none-"
                else:
                    return ""
        
        # Use fenced code style (triple back-ticks) rather than indents for clarity
        elif tag.name == "code":
            tag_text = "".join(str(child) for child in tag.children)
            if tag_text.strip():  # Check if the tag_text is not just whitespace
                if debug:
                    return "```" + tag_text + "```(code)"
                else:
                    return "```" + tag_text + "```"
            else:
                if debug:
                    return "(code)-none-"
                else:
                    return ""
                   
        elif tag.name == "a":
            if omit_links:
                if debug:
                    return f"{tag.get_text()}(a)"
                else:
                    return f"{tag.get_text()}"

            else:
                if debug:
                    return f"[{tag.get_text()}]({tag.get('href')})(a)"
                else:
                    return f"[{tag.get_text()}]({tag.get('href')})"
                    
        elif tag.name == "br":
            if debug:
                return "\n(br)"
            else:
                return "\n"
        
        elif tag.name == "hr":
            if debug:
                return "\n(hr)"
            else:
                return "---\n"
        
        elif tag.name == 'table':
            return convert_table_to_markdown(tag)
        
        else:
            # For tags that are not specifically handled, return their string representation
            tag_text = process_tag_children(tag)
            if tag_text is not None and tag_text != "":
                return "".join(tag_text)
            else:
                # TODO - Return actual tag name in debug output
                if debug:
                    return "(other tag)-none-"
                else:
                    return ""
            
    def handle_child(child):
            if isinstance(child, NavigableString):
                return str(child)
            else:
                return handle_tag(child)
    
    def process_tag_children(tag):
        processed_children = []
        for child in tag.children:
            processed_child = handle_child(child)
            processed_children.append(processed_child)
        if processed_children == "":
            return None
        else:
            return "".join(processed_children)

    def process_list_items(tag):
        processed_items = []
        for li in tag.find_all("li", recursive=False):
            processed_item = handle_child(li)
            processed_items.append(processed_item)
        if processed_items == "":
            return None
        else:
            if debug:
                return "\n(process_list_items)".join(processed_items)
            else:
                return "\n".join(processed_items)

    # Process only the direct children of the body tag (avoids duplicating data in output file)
    body = soup.body
    if body:
        return "".join(handle_child(child) for child in body.children)
    else:
        print("Warning: process_html is returning blank string!")
        return ""

    # Recursively process each tag
    def process_tags(element):
        text = ""
        for content in element.descendants:
            if isinstance(content, str):
                text += content
            elif content.name:
                text += handle_tag(content)
        return text

    return process_tags(soup)

# First pass at table conversion. Needs refinement.
def convert_table_to_markdown(table_tag):
    markdown_table = ""

    for row in table_tag.find_all("tr"):
        row_data = []

        for cell in row.find_all(["th", "td"]):
            cell_text = cell.get_text().strip().replace("\n", " ")
            row_data.append(cell_text)

        markdown_table += "| " + " | ".join(row_data) + " |\n"

    # Add the header separator after the first row
    header_separator = "| " + " | ".join(["-" * len(cell) for cell in row_data]) + " |\n"
    markdown_table = markdown_table.split("\n", 1)
    markdown_table.insert(1, header_separator)
    markdown_table = "\n".join(markdown_table)

    return markdown_table

def convert_html_to_markdown(input_file, output_file, omit_links, debug):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            html_content = file.read()
        markdown_text = process_html(html_content, omit_links, debug)
        
        # Condense blocks of more than one empty line to a single empty line
        condensed_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
        
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(condensed_text)

    except Exception as e:
        return str(e)

def main():
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown formatted text.")
    parser.add_argument("--infile", required=True, help="Input HTML file path")
    parser.add_argument("--outfile", required=True, help="Output file path for Markdown text")
    parser.add_argument("--omitlinks", action="store_true", required=False, help="URL references in <a> tags will be omitted if set.")
    parser.add_argument("--debug", action="store_true", required=False, help="Return debug markup in output text if set")
    
    args = parser.parse_args()

    convert_html_to_markdown(args.infile, args.outfile, args.omitlinks, args.debug)

if __name__ == "__main__":
    main()