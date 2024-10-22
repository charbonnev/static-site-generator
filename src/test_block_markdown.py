import unittest
from block_markdown import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        input_text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected_blocks = [
            """# This is a heading""",
            """This is a paragraph of text. It has some **bold** and *italic* words inside of it.""",
            ("* This is the first list item in a list block" "\n"
             "* This is a list item" "\n"
             "* This is another list item")
        ]
        blocks = markdown_to_blocks(input_text)
        self.assertEqual(blocks, expected_blocks)
        block_types = list(map(block_to_block_type, blocks))
        expected_block_types = ["heading", "paragraph", "unordered_list"]
        self.assertEqual(block_types, expected_block_types)

    def test_text_to_children(self):
        input_text = "This is a **text** node"
        expected_children = [LeafNode(None, 'This is a ', None),
                             LeafNode('b', 'text', None),
                             LeafNode(None, ' node', None)]
        children = text_to_children(input_text)
        self.assertListEqual(children, expected_children)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
