from textual.app import App, ComposeResult
from textual.widgets import *
from textual.containers import *
from textual.binding import Binding

class DataAutomatic(App):
    # Tiêu đề hiển thị trên thanh Header
    TITLE = "Data Automatic"
    SUB_TITLE = "v0.0"

    CSS_PATH = "app_screen.tcss"

    def on_load(self):
        pass

    def compose(self) -> ComposeResult:
        """Khai báo UI — chạy MỘT lần khi app khởi động."""
        yield Header()

    def on_mount(self) -> None:
        """Chạy sau khi UI đã được render xong."""
        pass