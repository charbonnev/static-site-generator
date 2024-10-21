import re
from textnode import TextType, TextNode
from htmlnode import *

def split_nodes_delimiter(old_nodes : list[TextNode], delimiter, text_type):
    # takes a list of TextNodes and returns a list of TextNodes,
    # but splits them if they are TEXT type and contains the a pair number of delimiter
    # , they will be split in TEXT types and text_type types.
    # Returns a list of nodes in correct order or an Exception in some cases
    new_nodes = []
    if text_type.value not in [item.value for item in TextType]:
        raise Exception(f"Invalid text_type passed: {text_type}")
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT.value:
                quantity_of_delimiters = len(list(filter(lambda x: x == delimiter,node.text)))
                if quantity_of_delimiters == 0:
                    new_nodes.append(node)
                    continue
                if quantity_of_delimiters % 2 != 0:
                    raise Exception(f"Invalid quantity of delimiters: _{delimiter}_, {node.text}")
                split_text = node.text.split(delimiter)
                between_delimiters = False
                for text in split_text:
                    if not between_delimiters:
                        between_delimiters = True
                        new_nodes.append(TextNode(text, TextType.TEXT))
                        continue
                    # is between delimiters
                    between_delimiters = False
                    new_nodes.append(TextNode(text, text_type))
            case _:
                new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes : list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        md_images = extract_markdown_images(node.text)
        if not md_images:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        remaining_text = node.text
        for image in md_images:
            split_text = remaining_text.split(f"![{image[0]}]({image[1]})")
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = split_text[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes : list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        md_links = extract_markdown_links(node.text)
        if not md_links:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        remaining_text = node.text
        for link in md_links:
            split_text = remaining_text.split(f"[{link[0]}]({link[1]})")
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = split_text[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes