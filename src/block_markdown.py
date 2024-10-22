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

def block_to_block_type(md_block: str):
    if md_block[0] == "#":
        i = 1
        while md_block[i] == "#":
            i += 1
        if md_block[i] == " ":
            return "heading"
    if md_block[:3] == "```":
        if md_block[-3:] == "```":
            return "code"
    if md_block[0] == ">":
        md_text_split = md_block.split("\n")
        for line in md_text_split[1:]:
            if line[0] == ">":
                continue
            return "paragraph"
        return "quote"
    if md_block[:2] == "* " or md_block[:2] == "- ":
        md_text_split = md_block.split("\n")
        for line in md_text_split[1:]:
            if line[:2] == "* " or line[:2] == "- ":
                continue
            return "paragraph"
        return "unordered_list"
    if md_block[:3] == "1. ":
        md_text_split = md_block.split("\n")
        number = 2
        len_number = 1
        for line in md_text_split[1:]:
            len_number = len(str(number))
            if line[:len_number + 2] == f"{number}. ":
                number += 1
                continue
            return "paragraph"
        return "ordered_list"
    return "paragraph"
            