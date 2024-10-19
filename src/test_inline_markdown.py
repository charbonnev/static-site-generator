import unittest
from htmlnode import *
from inline_markdown import *


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(repr(new_nodes),
                         "[TextNode('This is text with a ', 'TEXT', None), "
                         "TextNode('code block', 'CODE', None), "
                         "TextNode(' word', 'TEXT', None)]")


class TestLinksAndImages(unittest.TestCase):
    def test_extract_md_images(self):
        text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
                "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual(extract_markdown_images(text),
                             [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_md_links(self):
        text = ("This is text with a link [to boot dev](https://www.boot.dev) "
                "and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(extract_markdown_links(text),
                             [("to boot dev", "https://www.boot.dev"), 
                              ("to youtube", "https://www.youtube.com/@bootdotdev")])
