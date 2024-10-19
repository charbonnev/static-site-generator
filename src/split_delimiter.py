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
                print("case texttype.TEXT")
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
            