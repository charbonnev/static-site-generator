import unittest
from htmlnode import *
from split_delimiter import *

class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(repr(new_nodes), 
                         "[TextNode('This is text with a ', 'TEXT', None), "
                         "TextNode('code block', 'CODE', None), "
                         "TextNode(' word', 'TEXT', None)]")
