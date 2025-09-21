# dashboard_ui.py
import customtkinter as ctk

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

        # Top frame with back button and title
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR, corner_radius=12)
        self.top_frame.pack(fill="x", pady=(0, 20), padx=5)

        self.back_button = ctk.CTkButton(
            self.top_frame,
            text="← Back",
            width=80,
            fg_color=BASE_COLOR,
            hover_color="#059133",
            corner_radius=8,
            command=self.go_back
        )
        self.back_button.pack(side="left", padx=(5, 10), pady=10)

        ctk.CTkLabel(
            self.top_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=10)

        # Content frame for cards
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        self.content_frame.pack(fill="both", expand=True)

        # Cards layout
        self.create_card("👤 My Profile & Information", self.my_profile)
        self.create_card("📜 Order History", self.order_history)
        self.create_card("🚪 Logout", self.logout)

    # -------------------------
    # Card creation helper
    # -------------------------
    def create_card(self, text, command):
        card = ctk.CTkButton(
            self.content_frame,
            text=text,
            width=240,
            height=70,
            fg_color=CARD_COLOR,
            hover_color="#3A3A3A",
            corner_radius=15,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=command
        )
        card.pack(pady=15)

    # -------------------------
    # Placeholder functionality
    # -------------------------
    def my_profile(self):
        print("Profile clicked")  # TODO: Replace with profile UI

    def order_history(self):
        print("Order history clicked")  # TODO: Replace with order history UI

    def logout(self):
        print("Logout clicked")  # TODO: Implement logout functionality
        self.main_frame.destroy()

    # -------------------------
    # Back navigation (late import to avoid circular import)
    # -------------------------
    def go_back(self):
        self.main_frame.destroy()
        # Late import to avoid circular import
        from chat_ui import ChatUI
        ChatUI(self.parent, self.user_name)
