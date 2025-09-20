# gui_app.py
import customtkinter as ctk
from browser import open_product_urls
from capture import take_screenshot
from compare import compare_prices
from PIL import Image, ImageTk
import time, os

BASE_COLOR = "#06a13f"  # brand green

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class GroceryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_mode = "Dark"

        # Compact window
        self.title("Gropaa")
        self.geometry("320x420")
        self.resizable(False, False)

        # 🔹 Title bar icon
        try:
            self.iconbitmap("logotitlebar.ico")
        except Exception as e:
            print("⚠️ Could not load title bar icon:", e)

        # 🔹 Logo inside app
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("logo.png"),
                dark_image=Image.open("logo.png"),
                size=(48, 48)
            )
            self.logo_label = ctk.CTkLabel(self, image=logo_image, text="")
            self.logo_label.pack(pady=(8, 4))
        except Exception as e:
            print("⚠️ Could not load in-app logo:", e)

        # Chat area
        self.chat_frame = ctk.CTkScrollableFrame(self, width=300, height=260, fg_color=self.get_bg_color())
        self.chat_frame.pack(padx=8, pady=8, fill="both", expand=True)

        self.chat_widgets = []

        # Input frame
        self.input_frame = ctk.CTkFrame(self, fg_color=self.get_bg_color())
        self.input_frame.pack(fill="x", padx=10, pady=(4, 8))

        self.input_box = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type product...",
            width=200,
            font=ctk.CTkFont(size=12),
            fg_color=self.get_entry_bg()
        )
        self.input_box.pack(side="left", padx=(0, 6), ipady=3)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Go",
            corner_radius=12,
            width=70,
            height=32,
            fg_color=BASE_COLOR,
            hover_color="#059133",
            command=self.handle_query
        )
        self.send_button.pack(side="right")

        # Theme switch
        self.theme_switch = ctk.CTkSwitch(self, text="🌗", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.pack(pady=(0, 4))

    def get_bg_color(self):
        return "#FFFFFF" if self.current_mode == "Light" else "#1E1E1E"

    def get_entry_bg(self):
        return "#F0F0F0" if self.current_mode == "Light" else "#2E2E2E"

    def toggle_theme(self):
        self.current_mode = "Dark" if self.theme_switch.get() == 1 else "Light"
        ctk.set_appearance_mode(self.current_mode)

        # Update chat frame and input frame backgrounds
        self.chat_frame.configure(fg_color=self.get_bg_color())
        self.input_frame.configure(fg_color=self.get_bg_color())
        self.input_box.configure(fg_color=self.get_entry_bg())

        # Update existing chat bubbles
        for label in self.chat_widgets:
            # Keep user bubbles green, assistant bubbles adapt
            if label.cget("fg_color") != BASE_COLOR:
                label.configure(fg_color=self.get_bg_color())

    def add_message(self, sender, message, is_user=False):
        bubble_color = BASE_COLOR if is_user else (self.get_bg_color() if self.current_mode == "Light" else "#2E2E2E")
        anchor_side = "e" if is_user else "w"

        label = ctk.CTkLabel(
            self.chat_frame,
            text=message,
            wraplength=240,
            justify="left",
            anchor="w",
            fg_color=bubble_color,
            corner_radius=10,
            text_color="black" if self.current_mode == "Light" else "white",
            font=ctk.CTkFont(size=11),
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

        self.add_message("You", query, is_user=True)
        self.input_box.delete(0, "end")

        self.add_message("Assistant", f"🌐 Checking Blinkit & Amazon for '{query}'...")
        open_product_urls(query)
        self.add_message("Assistant", "✅ Tabs opened. Waiting...")

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

        if os.path.exists(blinkit_path): os.remove(blinkit_path)
        if os.path.exists(amazon_path): os.remove(amazon_path)

        self.add_message("Assistant", "✨ Done!")


if __name__ == "__main__":
    app = GroceryApp()
    app.mainloop()
