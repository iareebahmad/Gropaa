# register.py
import customtkinter as ctk
from PIL import Image
from supabase_client import supabase

BASE_COLOR = "#06a13f"


# -------------------
# Switch to login frame
# -------------------
def switch_to_login(current_frame, parent, on_success):
    current_frame.destroy()
    from login import create_login_frame
    create_login_frame(parent, on_success)


# -------------------
# Supabase registration
# -------------------
def register_user(name, email, password):
    response = supabase.auth.sign_up({"email": email, "password": password})
    if response.get("user"):
        user_id = response["user"]["id"]
        supabase.table("profiles").insert({"id": user_id, "name": name}).execute()
        return True, "Registration successful!"
    return False, response.get("error") or "Registration failed"


# -------------------
# UI frame
# -------------------
def create_register_frame(parent, on_success):
    # Fonts
    default_font = ctk.CTkFont(family="Calibri", size=14)
    heading_font = ctk.CTkFont(family="Calibri", size=16, weight="bold")
    footer_font = ctk.CTkFont(family="Calibri", size=12)

    frame = ctk.CTkFrame(parent, width=320, height=460, corner_radius=20,
                         fg_color=parent.cget("fg_color"))
    frame.place(relx=0.5, rely=0.45, anchor="center")

    # Logo
    try:
        logo_image = ctk.CTkImage(light_image=Image.open("logo.png"),
                                  dark_image=Image.open("logo.png"),
                                  size=(160, 160))
        logo_label = ctk.CTkLabel(frame, image=logo_image, text="")
        logo_label.image = logo_image
        logo_label.pack(pady=(3.5, 3.5))
    except:
        pass

    # Heading
    ctk.CTkLabel(frame, text="Create your Account", font=heading_font).pack(pady=(0, 10))

    # Input fields
    name_entry = ctk.CTkEntry(frame, placeholder_text="Full Name", width=220,
                              corner_radius=16, font=default_font)
    name_entry.pack(pady=(5, 8))

    email_entry = ctk.CTkEntry(frame, placeholder_text="Email", width=220,
                               corner_radius=16, font=default_font)
    email_entry.pack(pady=(5, 8))

    password_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=220,
                                  show="*", corner_radius=16, font=default_font)
    password_entry.pack(pady=(5, 8))

    confirm_entry = ctk.CTkEntry(frame, placeholder_text="Re-enter Password", width=220,
                                 show="*", corner_radius=16, font=default_font)
    confirm_entry.pack(pady=(5, 12))

    # Status label
    status_label = ctk.CTkLabel(frame, text="", text_color="red", font=default_font)
    status_label.pack(pady=(0, 8))

    # Buttons side by side
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(pady=(0, 10))

    def handle_register():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        confirm = confirm_entry.get().strip()

        if not name or not email or not password or not confirm:
            status_label.configure(text="All fields required")
            return
        if password != confirm:
            status_label.configure(text="Passwords do not match")
            return

        success, msg = register_user(name, email, password)
        status_label.configure(text=msg, text_color="green" if success else "red")
        if success:
            switch_to_login(frame, parent, on_success)

    reg_btn = ctk.CTkButton(btn_frame, text="Register", width=90,
                            fg_color=BASE_COLOR, hover_color="#059133",
                            corner_radius=16, font=default_font,
                            command=handle_register)
    reg_btn.pack(side="left", padx=5)

    login_btn = ctk.CTkButton(btn_frame, text="Back to Login", width=90,
                              fg_color=BASE_COLOR, hover_color="#059133",
                              corner_radius=16, font=default_font,
                              command=lambda: switch_to_login(frame, parent, on_success))
    login_btn.pack(side="right", padx=5)

    # Footer
    ctk.CTkLabel(frame, text="Made with ♡ for India",
                 font=footer_font, text_color="gray").pack(side="bottom", pady=(10, 5))

    return frame
