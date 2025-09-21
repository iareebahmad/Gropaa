# login.py
import customtkinter as ctk
from PIL import Image
import json, os

BASE_COLOR = "#06a13f"
USERS_FILE = "users.json"

# --- Utilities ---
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# --- Login Logic ---
def login_user(email, password):
    users = load_users()
    if email in users and users[email] == password:
        return True, "Login successful"
    return False, "Invalid credentials"

# --- Switch to Register ---
def switch_to_register(current_frame, parent, on_success):
    current_frame.destroy()
    from register import create_register_frame
    create_register_frame(parent, on_success)

# --- UI Frame ---
def create_login_frame(parent, on_success):
    login_frame = ctk.CTkFrame(
        parent, width=300, height=340, corner_radius=20,
        fg_color=parent.cget("fg_color")
    )
    login_frame.place(relx=0.5, rely=0.45, anchor="center")  # slightly up to avoid footer overlap

    # --- Logo ---
    try:
        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),
            dark_image=Image.open("logo.png"),
            size=(180, 180)
        )
        logo_label = ctk.CTkLabel(login_frame, image=logo_image, text="")
        logo_label.image = logo_image
        logo_label.pack(pady=(3.5, 3.5))
    except Exception as e:
        print("⚠️ Could not load logo:", e)

    # --- Title ---
    ctk.CTkLabel(
        login_frame,
        text="Welcome to Gropaa",
        font=ctk.CTkFont(family="Calibri", size=16, weight="bold")
    ).pack(pady=(0, 15))

    # --- Entries ---
    email_entry = ctk.CTkEntry(login_frame, placeholder_text="Email", width=220)
    email_entry.pack(pady=(5, 10))

    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", width=220, show="*")
    password_entry.pack(pady=(0, 12))

    status_label = ctk.CTkLabel(login_frame, text="", text_color="red")
    status_label.pack(pady=(0, 8))

    # --- Buttons ---
    btn_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
    btn_frame.pack(pady=(0, 10))

    def handle_login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password:
            status_label.configure(text="Enter email and password")
            return
        success, msg = login_user(email, password)
        status_label.configure(text=msg, text_color="green" if success else "red")
        if success:
            login_frame.destroy()
            on_success()

    login_btn = ctk.CTkButton(
        btn_frame, text="Login", width=90,
        fg_color=BASE_COLOR, hover_color="#059133",
        command=handle_login
    )
    login_btn.pack(side="left", padx=5)

    register_btn = ctk.CTkButton(
        btn_frame, text="Register", width=90,
        fg_color=BASE_COLOR, hover_color="#059133",
        command=lambda: switch_to_register(login_frame, parent, on_success)
    )
    register_btn.pack(side="right", padx=5)

    # --- Footer ---
    ctk.CTkLabel(
        login_frame,
        text="Made with ❤️ for India",
        font=ctk.CTkFont(family="Calibri", size=12),
        text_color="gray"
    ).pack(side="bottom", pady=(10, 5))

    return login_frame
