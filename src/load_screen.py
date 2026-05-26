import asyncio
import httpx
import json

from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.binding import Binding

from widget.EditableRichLog import EditRichLog

REPO = "Masonnica/DataAutomatic"

class LoadScreen(App):
    _log = None
    _bar = None

    check_list = [
        "check_network",
        "check_version",
        "check_color",
    ]

    ask_update = False

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

        asyncio.create_task(self.run_all_checks())

    async def run_all_checks(self) -> None:
        tasks = []
        for i in range(len(self.check_list)):
            fn = getattr(self, self.check_list[i])
            tasks.append(fn(i))

        await asyncio.gather(*tasks)

    def update_bar_width(self) -> None:
        if self._bar is None:
            return
        self._bar.styles.width = self.size.width - 2

    def ask_update_version(self):
        pass

    def update_version(self):
        pass

    def done(self) -> None:
        if self._bar is None:
            return
        if self._bar.progress == len(self.check_list) and not self.ask_update:
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

        with open("info.json", "r", encoding="utf-8") as f:
            data_f = json.load(f)
            f.close()

        url = f"https://api.github.com/repos/{REPO}/releases/latest"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=1)
            data_g = response.json()

        try:
            latest = data_g["tag_name"]

            if latest == data_f["version"]:
                text = Text.from_markup("Version\t\tOk")
                text.stylize("green", 0, len(text))
                self._log.rewrite(index, text)
            else:
                text = Text.from_markup(f"[rgb(255,255,0)]Version\t\tA new version is available: {latest}[/]")
                self._log.rewrite(index, text)
                self.ask_update = True
        except:
            text = Text.from_markup(f"[rgb(255,255,0)]Version\t\tNot found![/]")
            self._log.rewrite(index, text)

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
