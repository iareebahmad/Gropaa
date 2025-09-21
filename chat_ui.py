# chat_ui.py
import customtkinter as ctk
from browser import open_product_urls
from capture import take_screenshot
from compare import compare_prices
from dashboard_ui import DashboardUI  # Import dashboard for navigation
from PIL import Image
import time, os

BASE_COLOR = "#06a13f"
USER_BUBBLE_COLOR = "#06a13f"
ASSISTANT_BUBBLE_COLOR = "#2E2E2E"
BG_COLOR = "#1E1E1E"


class ChatUI:
    def __init__(self, parent, user_name):
        self.parent = parent
        self.chat_widgets = []

        # Top frame for Logo, Welcome label, and Home button
        self.top_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        self.top_frame.pack(fill="x", padx=8, pady=(8,0))

        # Logo
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("logo.png"),
                dark_image=Image.open("logo.png"),
                size=(36,36)
            )
            self.logo_label = ctk.CTkLabel(self.top_frame, image=logo_image, text="")
            self.logo_label.image = logo_image  # Keep reference
            self.logo_label.pack(side="left", padx=(0,8), pady=6)
        except Exception as e:
            print("⚠️ Logo could not be loaded:", e)

        # Welcome label
        self.welcome_label = ctk.CTkLabel(
            self.top_frame,
            text=f'Welcome, {user_name}!',
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=BG_COLOR,
            text_color="white"
        )
        self.welcome_label.pack(side="left", padx=4, pady=6)

        # Home button on the far right
        self.home_button = ctk.CTkButton(
            self.top_frame,
            text="🏠",
            width=40,
            height=32,
            fg_color=BASE_COLOR,
            hover_color="#059133",
            command=self.go_home
        )
        self.home_button.pack(side="right", padx=(0,8), pady=6)

        # Chat frame
        self.chat_frame_main = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        self.chat_frame_main.pack(fill="both", expand=True, padx=8, pady=(0,8))

        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_frame_main, width=340, height=320, fg_color=BG_COLOR, corner_radius=12
        )
        self.chat_frame.pack(padx=8, pady=8, fill="both", expand=True)

        # Input area
        self.input_frame = ctk.CTkFrame(self.chat_frame_main, fg_color="#2A2A2A", corner_radius=12)
        self.input_frame.pack(fill="x", padx=10, pady=(0, 8))

        self.input_box = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type product...",
            width=240,
            fg_color="#3A3A3A",
            corner_radius=8,
            height=32,
            text_color="white",
        )
        self.input_box.pack(side="left", padx=(8, 6), pady=6)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Search!",
            width=70,
            height=32,
            fg_color=BASE_COLOR,
            hover_color="#059133",
            corner_radius=8,
            command=self.handle_query,
        )
        self.send_button.pack(side="right", padx=(0, 8), pady=6)

    # -------------------------
    # Chat functions
    # -------------------------
    def add_message(self, sender, message, is_user=False):
        bubble_color = USER_BUBBLE_COLOR if is_user else ASSISTANT_BUBBLE_COLOR
        anchor_side = "e" if is_user else "w"

        label = ctk.CTkLabel(
            self.chat_frame,
            text=message,
            wraplength=240,
            justify="left",
            anchor="w",
            fg_color=bubble_color,
            corner_radius=12,
            text_color="white",
            padx=8,
            pady=6,
        )
        label.pack(anchor=anchor_side, pady=4, padx=6)
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

        self.parent.after(2000, self.capture_screenshots)

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

    # -------------------------
    # Navigation
    # -------------------------
    def go_home(self):
        # Destroy chat UI
        self.top_frame.destroy()
        self.chat_frame_main.destroy()
        # Open dashboard
        DashboardUI(self.parent)
