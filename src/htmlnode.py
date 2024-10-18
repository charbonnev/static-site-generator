class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})'


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        if not value:
            raise ValueError("Value cannot be empty for LeafNode")
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
