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
        if value == None:
            raise ValueError("value cannot be empty for LeafNode")
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.tag!r}, {self.value!r}, {self.props!r})'

    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )


class ParentNode(HTMLNode):
    def __init__(self, tag: str = None, children: list = None, props: dict = None):
        if not children:
            raise ValueError("children cannot be empty for ParentNode")
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("tag cannot be empty for ParentNode")

        return (f"<{self.tag}{self.props_to_html()}>"
                f"{''.join([child.to_html() for child in self.children])}"
                f"</{self.tag}>")
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.tag!r}, {self.children!r}, {self.props!r})'
