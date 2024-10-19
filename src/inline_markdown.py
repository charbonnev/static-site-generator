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

def useless():
    text = "I have a (cat) and a (dog)"
    matches = re.findall(r"\((.*?)\)", text)
    print(matches) # ['cat', 'dog']

def extract_markdown_images(text):
    # takes a string and returns a list of tuples. 
    # Each tuple should contain the alt text and the URL of any markdown images.
    # findall actually returns a list of strings, 
    # but if there are more than one group in a pattern a list of tuples of strings
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    #same as above but for links
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches