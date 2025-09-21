# gui_app.py
import customtkinter as ctk
from login import create_login_frame
from browser import open_product_urls
from capture import take_screenshot
from compare import compare_prices
import time, os

BASE_COLOR = "#06a13f"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class GroceryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_mode = "Dark"
        self.geometry("360x500")
        self.resizable(False, False)
        self.title("Gropaa")

        # Title bar icon
        try:
            self.iconbitmap("logotitlebar.ico")
        except Exception as e:
            print("⚠️ Could not load title bar icon:", e)

        # Chat frame (hidden initially)
        self.chat_frame_main = ctk.CTkFrame(self, fg_color=self.get_bg_color())
        self.chat_widgets = []

        self.chat_frame = ctk.CTkScrollableFrame(self.chat_frame_main, width=320, height=280, fg_color=self.get_bg_color())
        self.chat_frame.pack(padx=8, pady=8, fill="both", expand=True)

        self.input_frame = ctk.CTkFrame(self.chat_frame_main, fg_color=self.get_bg_color())
        self.input_frame.pack(fill="x", padx=10, pady=(4,8))

        self.input_box = ctk.CTkEntry(self.input_frame, placeholder_text="Type product...", width=220,
                                      fg_color=self.get_entry_bg())
        self.input_box.pack(side="left", padx=(0,6), ipady=3)

        self.send_button = ctk.CTkButton(self.input_frame, text="Go", width=70, height=32,
                                         fg_color=BASE_COLOR, hover_color="#059133", command=self.handle_query)
        self.send_button.pack(side="right")

        # Theme switch
        self.theme_switch = ctk.CTkSwitch(self, text="🌗", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.place(relx=0.5, rely=0.95, anchor="s")

        # Show login frame first
        create_login_frame(self, on_success=self.show_chat_frame)

    def get_bg_color(self):
        return "#FFFFFF" if self.current_mode=="Light" else "#1E1E1E"

    def get_entry_bg(self):
        return "#F0F0F0" if self.current_mode=="Light" else "#2E2E2E"

    def toggle_theme(self):
        self.current_mode = "Dark" if self.theme_switch.get()==1 else "Light"
        ctk.set_appearance_mode(self.current_mode)
        self.chat_frame_main.configure(fg_color=self.get_bg_color())
        self.chat_frame.configure(fg_color=self.get_bg_color())
        self.input_frame.configure(fg_color=self.get_bg_color())
        self.input_box.configure(fg_color=self.get_entry_bg())
        for label in self.chat_widgets:
            label.configure(fg_color=self.get_bg_color() if label.cget("fg_color")!=BASE_COLOR else BASE_COLOR,
                            text_color="black" if self.current_mode=="Light" else "white")

    # -------------------------
    # Chat functionality
    # -------------------------
    def show_chat_frame(self, name):
        # Welcome message
        self.welcome_label = ctk.CTkLabel(self, text=f'Welcome to Gropaa "{name}"', anchor="e")
        self.welcome_label.place(relx=0.95, rely=0.05, anchor="ne")
        self.chat_frame_main.pack(fill="both", expand=True, padx=8, pady=8)

    def add_message(self, sender, message, is_user=False):
        bubble_color = BASE_COLOR if is_user else (self.get_bg_color() if self.current_mode=="Light" else "#2E2E2E")
        anchor_side = "e" if is_user else "w"

        label = ctk.CTkLabel(
            self.chat_frame,
            text=message,
            wraplength=240,
            justify="left",
            anchor="w",
            fg_color=bubble_color,
            corner_radius=10,
            text_color="black" if self.current_mode=="Light" else "white",
            padx=6,
            pady=3
        )
        label.pack(anchor=anchor_side, pady=3, padx=6)
        self.chat_widgets.append(label)
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def handle_query(self):
        query = self.input_box.get().strip()
        if not query:
            self.add_message("Assistant", "❌ Please enter a product name.")
            return

        # Show user's query
        self.add_message("You", query, is_user=True)
        self.input_box.delete(0, "end")

        # Assistant responses
        self.add_message("Assistant", f"🌐 Checking Blinkit & Amazon for '{query}'...")
        open_product_urls(query)
        self.add_message("Assistant", "✅ Tabs opened. Waiting...")

        # Delay for screenshot capture
        self.after(2000, self.capture_screenshots)

    def capture_screenshots(self):
        self.add_message("Assistant", "📸 Capturing Blinkit...")
        blinkit_path = take_screenshot("blinkit.png")
        self.add_message("Assistant", "📸 Capturing Amazon...")
        amazon_path = take_screenshot("amazon.png")
        time.sleep(1)
        self.add_message("Assistant", "🔍 Comparing prices...")
        result = compare_prices(blinkit_path, amazon_path)
        self.add_message("Assistant", f"📊 {result}")

        # Clean up temporary screenshots
        if os.path.exists(blinkit_path): os.remove(blinkit_path)
        if os.path.exists(amazon_path): os.remove(amazon_path)
        self.add_message("Assistant", "✨ Done!")

if __name__ == "__main__":
    app = GroceryApp()
    app.mainloop()
