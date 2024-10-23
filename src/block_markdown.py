from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes

BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_ULIST = "unordered_list"
BLOCK_TYPE_OLIST = "ordered_list"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_CODE = "code"


def markdown_to_blocks(markdown: str) -> list[str]:
    # we are looking for two newlines in a row
    # if we find one, we are at the end of a block
    # if we find two, we are at the beginning of a new block
    blocks = []
    split_markdown = markdown.split("\n\n")
    for block_string in split_markdown:
        if not block_string:
            continue
        blocks.append(block_string.strip())
    return blocks


def block_to_block_type(md_block: str, heading_level = False):
    if md_block[0] == "#":
        i = 1
        while md_block[i] == "#":
            i += 1
        if md_block[i] == " ":
            if heading_level:
                return BLOCK_TYPE_HEADING + f"|{i}"
            return BLOCK_TYPE_HEADING
    if md_block[:3] == "```":
        if md_block[-3:] == "```":
            return BLOCK_TYPE_CODE
    if md_block[0] == ">":
        md_text_split = md_block.split("\n")
        for line in md_text_split[1:]:
            if line[0] == ">":
                continue
            return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_QUOTE
    if md_block[:2] == "* " or md_block[:2] == "- ":
        md_text_split = md_block.split("\n")
        for line in md_text_split[1:]:
            if line[:2] == "* " or line[:2] == "- ":
                continue
            return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_ULIST
    if md_block[:3] == "1. ":
        md_text_split = md_block.split("\n")
        number = 2
        len_number = 1
        for line in md_text_split[1:]:
            len_number = len(str(number))
            if line[:len_number + 2] == f"{number}. ":
                number += 1
                continue
            return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_OLIST
    return BLOCK_TYPE_PARAGRAPH


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BLOCK_TYPE_HEADING:
        return block_to_heading(block)
    if block_type == BLOCK_TYPE_PARAGRAPH:
        return block_to_paragraph(block)
    if block_type == BLOCK_TYPE_ULIST:
        return block_to_ulist(block)
    if block_type == BLOCK_TYPE_OLIST:
        return block_to_olist(block)
    if block_type == BLOCK_TYPE_QUOTE:
        return block_to_quote(block)
    if block_type == BLOCK_TYPE_CODE:
        return block_to_code(block)
    raise Exception(f"Invalid block type: {block_type}")

def block_to_code(block: str):
    # a code block looks like this:
    # ```
    # code
    # ```
    # and has inline children
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError(f"Invalid code block: {block}")
    text = block[4:-3]
    inline_children = text_to_children(text)
    code = ParentNode("code", inline_children)
    return ParentNode("pre", [code])

def block_to_quote(block: str):
    # a quote block looks like this:
    # > Quote
    # and has inline children
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        # if not line.startswith("> "):
        #     raise Exception(f"Invalid quote block: {block}")
        new_lines.append(line.removeprefix("> ").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_olist(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def block_to_ulist(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_to_paragraph(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    inline_children = text_to_children(paragraph)
    return ParentNode("p", inline_children)

def block_to_heading(block: str):
    # a heading block looks like this:
    # ## Heading
    # and has inline children
    heading_level = block_to_block_type(block, heading_level=True).split("|")[1]
    text = block[int(heading_level) + 1:]
    inline_children = text_to_children(text)
    return ParentNode(f"h{heading_level}", inline_children)

def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        if node.text:
            children.append(text_node_to_html_node(node))
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
