from textual.widget import Widget
from rich.text import Text
from rich.console import RenderableType

class EditRichLog(Widget):
    def __init__(self):
        super().__init__()
        self.lines: list[Text] = []

    def write(self, text: Text) -> None:
        self.lines.append(text)
        self.refresh()

    def rewrite(self, line: int, text: Text) -> None:
        self.lines[line] = text
        self.refresh()

    def delete(self, line: int) -> None:
        self.lines.pop(line)
        self.refresh()

    def clear(self) -> None:
        self.lines.clear()
        self.refresh()

    def render(self):
        result = Text()
        for i, line in enumerate(self.lines):
            result.append_text(line)
            if i < len(self.lines) - 1:
                result.append("\n")
        return result