import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a link node", TextType.LINK,
                        "https://www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK,
                         "https://www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a link node", TextType.LINK,
                        "https://www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK,
                         "https://www.youtube.com")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTML(unittest.TestCase):

    def text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(leaf_node), repr(
            LeafNode(None, "This is a text node")))

    def bold(self):
        text_node = TextNode("This is a bold node", TextType.BOLD)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(leaf_node), repr(
            LeafNode('b', "This is a bold node")))

    def italic(self):
        text_node = TextNode("This is an italic node", TextType.ITALIC)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(leaf_node), repr(
            LeafNode('i', "This is an italic node")))

    def code(self):
        text_node = TextNode("This is a code node", TextType.CODE)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(leaf_node), repr(
            LeafNode('code', "This is a code node")))

    def link(self):
        text_node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(leaf_node), repr(
            LeafNode('a', "This is a link node", {"href":"https://www.google.com"})))

    def image(self):
        text_node = TextNode("This is an image node", TextType.LINK, "https://www.google.com/img.png")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(leaf_node), repr(
            LeafNode('img', "This is an image node", {"href":"https://www.google.com/img.png"})))

    def other_invalid_type(self):
        with self.assertRaises(Exception):
            text_node = TextNode("This is an invalid node", "INVALID", "https://www.google.com/img.png")
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
