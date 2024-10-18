import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_repr1(self):
        node = HTMLNode("h1", "This is an H1")
        node2 = HTMLNode("a", "This is an anchor", props={
            "href": "https://www.google.com"})
        self.assertEqual(
            repr(node), "HTMLNode('h1', 'This is an H1', None, None)")
        self.assertEqual(repr(
            node2), "HTMLNode('a', 'This is an anchor', None, {'href': 'https://www.google.com'})")

    def test_repr2(self):
        node = HTMLNode("img", "This is an image", props={
                        "src": "https://www.google.com", "alt": "This is an image"})
        self.assertEqual(repr(
            node), "HTMLNode('img', 'This is an image', None, {'src': 'https://www.google.com', 'alt': 'This is an image'})")

    def test_props_to_html1(self):
        node = HTMLNode("h1", "This is an H1")
        node2 = HTMLNode("a", "This is an anchor", props={
                         "href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(),
                         ' href="https://www.google.com"')

    def test_props_to_html2(self):
        node = HTMLNode("img", "This is an image", props={
                        "src": "https://www.google.com", "alt": "This is an image"})

        self.assertEqual(node.props_to_html(),
                         ' src="https://www.google.com" alt="This is an image"')


class TestLeafNode(unittest.TestCase):
    def test_repr1(self):
        node = LeafNode("h1", "This is an H1")
        self.assertEqual(
            repr(node), "LeafNode('h1', 'This is an H1', None)")

    def test_to_html(self):
        node = LeafNode("h1", "This is an H1")
        self.assertEqual(
            node.to_html(), "<h1>This is an H1</h1>")


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(
        ), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_to_html_2_levels(self):
        level2_node = LeafNode("b", "level2")
        level1_node = ParentNode("p", [level2_node])
        level0_node = ParentNode("div", [level1_node])
        self.assertEqual(
            level0_node.to_html(),
            "<div><p><b>level2</b></p></div>",
        )


if __name__ == "__main__":
    unittest.main()
