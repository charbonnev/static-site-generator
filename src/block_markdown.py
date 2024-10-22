def markdown_to_blocks(markdown: str) -> list[str]:
    # we are looking for two newlines in a row
    # if we find one, we are at the end of a block
    # if we find two, we are at the beginning of a new block
    blocks = []
    split_markdown = markdown.split("\n\n")
    for block_string in split_markdown:
        if not block_string:
            continue
        blocks.append(block_string.strip())
    return blocks