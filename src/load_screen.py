import asyncio
import httpx

from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.binding import Binding

from widget.EditableRichLog import EditRichLog

class LoadScreen(App):
    _log = None
    _bar = None

    check_list = [
        "check_network",
        "check_version",
        "check_color",
    ]

    CSS_PATH = "load_screen.tcss"
    BINDINGS = [
        Binding("ctrl+q", "noop", show=False),
    ]
    ENABLE_COMMAND_PALETTE = False

    def compose(self) -> ComposeResult:
        yield EditRichLog()
        yield ProgressBar(len(self.check_list), show_eta=False)

    def on_mount(self) -> None:
        self._log = self.query_one(EditRichLog)
        self._bar = self.query_one(ProgressBar)

        self.set_interval(0.3, self.update_bar_width)
        self.set_interval(1, self.done)

        for i in range(len(self.check_list)):
            fn = getattr(self, self.check_list[i])
            asyncio.create_task(fn(i))

    def update_bar_width(self) -> None:
        if self._bar is None:
            return
        self._bar.styles.width = self.size.width - 2

    def done(self):
        if self._bar is None:
            return
        if self._bar.progress == len(self.check_list):
            self.exit()

    async def check_network(self, index: int) -> None:
        self._log.write(Text.from_markup("Network\t\tChecking..."))

        async with httpx.AsyncClient() as client:
            response = await client.get("https://github.com/Masonnica/DataAutomatic", timeout=5)
        if response.status_code == 200:
            text = Text.from_markup(f"Network\t\tOk:{response.status_code}")
            text.stylize("green", 0, len(text))
            self._log.rewrite(index, text)
        else:
            text = Text.from_markup(f"Network\t\tFalse:{response.status_code}")
            text.stylize("red", 0, len(text))
            self._log.rewrite(index, text)

        self._bar.advance(1)

    async def check_version(self, index: int) -> None:
        self._log.write(Text.from_markup("Version\t\tChecking..."))

        # TODO: Write function

        self._bar.advance(1)

    async def check_color(self, index: int) -> None:
        text = Text.from_markup("Color\t\tChecking...\n\t")
        text_test = Text.from_markup("")
        self._log.write(text + text_test)

        for r in range(5):
            for g in range(5):
                for b in range(5):
                    t = Text.from_markup(f"[rgb({r*51},{g*51},{b*51})]■[/]")
                    text_test += t
                    self._log.rewrite(index, text + text_test)
                    await asyncio.sleep(0.01)

        text = Text.from_markup("Color\t\tDone\n\t")
        text.stylize("green", 0, len(text))
        self._log.rewrite(index, text + text_test)

        self._bar.advance(1)
