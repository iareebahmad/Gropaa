# login.py
import customtkinter as ctk
from PIL import Image
from supabase_client import supabase  # your initialized supabase client

BASE_COLOR = "#06a13f"


# -------------------
# Supabase login
# -------------------
def login_user(email, password):
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})

    if response.user:
        user_id = response.user.id
        profile = supabase.table("profiles").select("name").eq("id", user_id).execute()
        if profile.data and len(profile.data) > 0:
            name = profile.data[0]["name"]
        else:
            name = "User"
        return True, name

    error_msg = response.error.message if response.error else "Login failed"
    return False, error_msg


# -------------------
# Switch to Register
# -------------------
def switch_to_register(current_frame, parent, on_success):
    current_frame.destroy()
    from register import create_register_frame
    create_register_frame(parent, on_success)


# -------------------
# Login UI
# -------------------
def create_login_frame(parent, on_success):
    frame = ctk.CTkFrame(parent, width=300, height=340, corner_radius=20,
                         fg_color=parent.cget("fg_color"))
    frame.place(relx=0.5, rely=0.45, anchor="center")

    try:
        logo_image = ctk.CTkImage(light_image=Image.open("logo.png"),
                                  dark_image=Image.open("logo.png"), size=(180, 180))
        logo_label = ctk.CTkLabel(frame, image=logo_image, text="")
        logo_label.image = logo_image
        logo_label.pack(pady=(3.5, 3.5))
    except:
        pass

    ctk.CTkLabel(frame, text="Welcome to Gropaa", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 15))

    email_entry = ctk.CTkEntry(frame, placeholder_text="Email", width=220)
    email_entry.pack(pady=(5, 10))
    password_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=220, show="*")
    password_entry.pack(pady=(0, 12))

    status_label = ctk.CTkLabel(frame, text="", text_color="red")
    status_label.pack(pady=(0, 8))

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(pady=(0, 10))

    def handle_login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password:
            status_label.configure(text="Enter email & password")
            return

        success, name_or_msg = login_user(email, password)
        if success:
            status_label.configure(text="Login successful", text_color="green")
            frame.destroy()
            on_success(name_or_msg)
        else:
            status_label.configure(text=name_or_msg, text_color="red")

    login_btn = ctk.CTkButton(btn_frame, text="Login", width=90,
                              fg_color=BASE_COLOR, hover_color="#059133",
                              command=handle_login)
    login_btn.pack(side="left", padx=5)

    register_btn = ctk.CTkButton(btn_frame, text="Register", width=90,
                                 fg_color=BASE_COLOR, hover_color="#059133",
                                 command=lambda: switch_to_register(frame, parent, on_success))
    register_btn.pack(side="right", padx=5)

    ctk.CTkLabel(frame, text="Made with ♡ for India", font=ctk.CTkFont(size=12),
                 text_color="gray").pack(side="bottom", pady=(10, 5))

    return frame