# dashboard_ui.py
import customtkinter as ctk
from PIL import Image

BASE_COLOR = "#06a13f"
BG_COLOR = "#1E1E1E"
CARD_COLOR = "#2A2A2A"

class DashboardUI:
    def __init__(self, parent, user_name="User"):
        self.parent = parent
        self.user_name = user_name

        # Main frame
        self.main_frame = ctk.CTkFrame(parent, fg_color=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Top frame with back button
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        self.top_frame.pack(fill="x", pady=(0, 10))

        # Modern circular back button
        try:
            arrow_img = ctk.CTkImage(
                light_image=Image.open("back_arrow.png"),
                dark_image=Image.open("back_arrow.png"),
                size=(22, 22)
            )
            self.back_button = ctk.CTkButton(
                self.top_frame,
                text="",
                image=arrow_img,
                width=45,
                height=45,
                fg_color=CARD_COLOR,
                hover_color=BASE_COLOR,
                corner_radius=22,  # circular
                command=self.go_back
            )
            self.back_button.image = arrow_img
            self.back_button.pack(side="left", padx=10, pady=5)
        except Exception as e:
            print("⚠️ Back icon missing, fallback to text:", e)
            self.back_button = ctk.CTkButton(
                self.top_frame,
                text="←",
                width=45,
                height=45,
                fg_color=CARD_COLOR,
                hover_color=BASE_COLOR,
                corner_radius=22,
                font=ctk.CTkFont(size=18, weight="bold"),
                command=self.go_back
            )
            self.back_button.pack(side="left", padx=10, pady=5)

        # Content frame for logo + buttons
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        self.content_frame.pack(fill="both", expand=False, pady=10)

        # Logo at the top
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("logo.png"),
                dark_image=Image.open("logo.png"),
                size=(140, 140)
            )
            self.logo_label = ctk.CTkLabel(self.content_frame, image=logo_image, text="")
            self.logo_label.image = logo_image
            self.logo_label.pack(pady=(0, 20))
        except Exception as e:
            print("⚠️ Logo could not be loaded:", e)

        # Cards (buttons) immediately below logo
        self.create_card("👤 My Profile & Info", self.my_profile)
        self.create_card("📜 Order History", self.order_history)
        self.create_card("🚪 Logout", self.logout)

        # Footer at the bottom
        footer = ctk.CTkLabel(
            self.main_frame,
            text="Made with ♡ for India",
            font=ctk.CTkFont(size=12, family="Calibri"),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=(10, 5))

    # -------------------------
    # Card creation helper
    # -------------------------
    def create_card(self, text, command):
        card = ctk.CTkButton(
            self.content_frame,
            text=text,
            width=200,
            height=50,
            fg_color=CARD_COLOR,
            hover_color=BASE_COLOR,
            corner_radius=14,
            font=ctk.CTkFont(family="Calibri", size=12, weight="bold"),
            command=command
        )
        card.pack(pady=10)

    # -------------------------
    # Placeholder functionality
    # -------------------------
    def my_profile(self):
        print("Profile clicked")

    def order_history(self):
        print("Order history clicked")

    def logout(self):
        print("Logout clicked")
        self.main_frame.destroy()

    # -------------------------
    # Back navigation
    # -------------------------
    def go_back(self):
        self.main_frame.destroy()
        from chat_ui import ChatUI
        ChatUI(self.parent, self.user_name)
