# register.py
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

# --- Register Logic ---
def register_user(email, password):
    users = load_users()
    if email in users:
        return False, "User already exists"
    users[email] = password
    save_users(users)
    return True, "Registration successful"

# --- Switch to Login ---
def switch_to_login(current_frame, parent, on_success):
    current_frame.destroy()
    from login import create_login_frame
    create_login_frame(parent, on_success)

# --- UI Frame ---
def create_register_frame(parent, on_success):
    register_frame = ctk.CTkFrame(
        parent, width=300, height=420, corner_radius=20,
        fg_color=parent.cget("fg_color")
    )
    register_frame.place(relx=0.5, rely=0.45, anchor="center")

    # --- Logo ---
    try:
        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),
            dark_image=Image.open("logo.png"),
            size=(160, 160)
        )
        logo_label = ctk.CTkLabel(register_frame, image=logo_image, text="")
        logo_label.image = logo_image
        logo_label.pack(pady=(3.5, 3.5))
    except Exception as e:
        print("⚠️ Could not load logo:", e)

    # --- Title ---
    ctk.CTkLabel(
        register_frame,
        text="Create your account",
        font=ctk.CTkFont(family="Calibri", size=16, weight="bold")
    ).pack(pady=(0, 15))

    # --- Entries ---
    name_entry = ctk.CTkEntry(register_frame, placeholder_text="Full Name", width=220)
    name_entry.pack(pady=(5, 8))

    email_entry = ctk.CTkEntry(register_frame, placeholder_text="Email", width=220)
    email_entry.pack(pady=(5, 8))

    password_entry = ctk.CTkEntry(register_frame, placeholder_text="Password", width=220, show="*")
    password_entry.pack(pady=(5, 8))

    confirm_password_entry = ctk.CTkEntry(register_frame, placeholder_text="Re-enter Password", width=220, show="*")
    confirm_password_entry.pack(pady=(5, 12))

    status_label = ctk.CTkLabel(register_frame, text="", text_color="red")
    status_label.pack(pady=(0, 8))

    # --- Buttons ---
    btn_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
    btn_frame.pack(pady=(0, 10))

    def handle_register():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_password_entry.get().strip()

        if not name or not email or not password or not confirm_password:
            status_label.configure(text="All fields are required")
            return

        if password != confirm_password:
            status_label.configure(text="Passwords do not match")
            return

        users = load_users()
        if email in users:
            status_label.configure(text="User already exists")
            return

        users[email] = {"name": name, "password": password}
        save_users(users)
        status_label.configure(text="Registration successful", text_color="green")

    register_btn = ctk.CTkButton(
        btn_frame, text="Register", width=90,
        fg_color=BASE_COLOR, hover_color="#059133",
        command=handle_register
    )
    register_btn.pack(side="left", padx=5)

    from login import create_login_frame
    login_btn = ctk.CTkButton(
        btn_frame, text="Login", width=90,
        fg_color=BASE_COLOR, hover_color="#059133",
        command=lambda: switch_to_login(register_frame, parent, on_success)
    )
    login_btn.pack(side="right", padx=5)

    # Footer
    ctk.CTkLabel(
        register_frame,
        text="Made with ❤️ for India",
        font=ctk.CTkFont(family="Calibri", size=12),
        text_color="gray"
    ).pack(side="bottom", pady=(10, 5))

    return register_frame
