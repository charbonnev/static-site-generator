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
        
