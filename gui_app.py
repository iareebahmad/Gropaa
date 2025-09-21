# gui_app.py
import customtkinter as ctk
from login import create_login_frame
from chat_ui import ChatUI

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class GroceryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("360x500")
        self.resizable(False, False)
        self.title("Gropaa")

        # Title bar icon
        try:
            self.iconbitmap("logotitlebar.ico")
        except Exception as e:
            print("⚠️ Could not load title bar icon:", e)

        # Show login frame first
        create_login_frame(self, on_success=self.show_chat_ui)

    def show_chat_ui(self, name):
        # Initialize ChatUI module
        self.chat_ui = ChatUI(self, name)


if __name__ == "__main__":
    app = GroceryApp()
    app.mainloop()
