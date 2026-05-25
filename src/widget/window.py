from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.reactive import reactive
from textual.containers import Grid
from rich.text import Text

BORDER = {
    "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
    "h": "─", "v": "│",
    "tee_l": "├", "tee_r": "┤",
}

def clamp(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[:max_len - 1] + "…"

class WindowWidget(Widget):
    top_left = reactive("")
    top_right = reactive("")
    bottom_left = reactive("")
    bottom_right = reactive("")
    color = reactive("")
