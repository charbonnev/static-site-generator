from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url
    
    def __eq__(self, other) -> bool:
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
        
    def __repr__(self) -> str:
        # !r = repr
        # !s = str
        return f'TextNode({self.text!r}, {self.text_type!r}, {self.url!r})'
    
def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', None, {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid TextType")