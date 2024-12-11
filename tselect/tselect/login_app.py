import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import configparser
from PIL import Image, ImageTk
from dashboard import open_dashboard  # Import the dashboard module

# Path to the static images
IMAGE_PATH = "bckgrd.jpg"  # Ensure this image is in the same folder as your script
CONFIG_FILE = "config.ini"

# Function to initialize the SQLite database
def initialize_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to save credentials to config file
def save_credentials(username, password, remember_me):
    config = configparser.ConfigParser()
    config["CREDENTIALS"] = {
        "username": username if remember_me else "",
        "password": password if remember_me else "",
        "remember_me": str(remember_me)
    }
    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)

# Function to load credentials from config file
def load_credentials():
    config = configparser.ConfigParser()
    if config.read(CONFIG_FILE) and "CREDENTIALS" in config:
        username = config["CREDENTIALS"].get("username", "")
        password = config["CREDENTIALS"].get("password", "")
        remember_me = config["CREDENTIALS"].getboolean("remember_me", False)
        return username, password, remember_me
    return "", "", False

# Function to register user
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please fill out both fields.")
        return

    hashed_password = hash_password(password)

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        toggle_to_login()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

# Function to validate login
def login_user():
    username = entry_username.get()
    password = entry_password.get()
    hashed_password = hash_password(password)
    remember_me = remember_me_var.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        save_credentials(username, password, remember_me)  # Save credentials if "Remember Me" is checked
        main_window.destroy()  # Close the login/register window
        open_dashboard(username, show_login_form)  # Pass the show_login_form to the dashboard
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to toggle between Login and Register forms
def toggle_to_register():
    label_title.config(text="Register!")
    button_submit.config(text="Register", command=register_user)
    toggle_button.config(text="Already have an account? Login", command=toggle_to_login)

def toggle_to_login():
    label_title.config(text="Login")
    button_submit.config(text="Login", command=login_user)
    toggle_button.config(text="Don't have an account? Register", command=toggle_to_register)

# Function to center the form dynamically
def center_form():
    window_width = main_window.winfo_width()
    window_height = main_window.winfo_height()
    form_width = frame_form.winfo_width()
    form_height = frame_form.winfo_height()

    # Calculate right-aligned position (on the right side of the window)
    x = window_width - form_width - 0  # 20 for padding from the right edge
    y = (window_height - form_height) // 5  # Keep the vertical center

    # Move the form to the desired position
    canvas.coords(frame_form_window, x, y)

# Function to show the login form
def show_login_form():
    global main_window, frame_form, canvas, frame_form_window, label_title
    global entry_username, entry_password, button_submit, toggle_button, remember_me_var, bg_image_label

    main_window = tk.Tk()
    main_window.title("Login/Register")
    main_window.geometry("800x600")

    # Automatically maximize the window
    main_window.state('zoomed')

    # Create a Canvas to hold the background image
    canvas = tk.Canvas(main_window, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Dynamically resize background image to fit the screen
    def resize_background(event):
        canvas_width = main_window.winfo_width()
        canvas_height = main_window.winfo_height()

        # Resize the image while keeping the aspect ratio
        pil_image_resized = pil_image.resize((canvas_width, canvas_height), Image.LANCZOS)
        bg_resized_image = ImageTk.PhotoImage(pil_image_resized)
 
        # Update the background image
        canvas.create_image(0, 0, image=bg_resized_image, anchor="nw")
        canvas.image = bg_resized_image  # Keep a reference to avoid garbage collection

    # Load and set the static background image using Pillow
    try:
        pil_image = Image.open(IMAGE_PATH)
        bg_image = ImageTk.PhotoImage(pil_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        main_window.destroy()
        return

    # Set the initial background image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.image = bg_image  # Keep a reference to avoid garbage collection

    # Resize background dynamically
    main_window.bind("<Configure>", resize_background)

    # Right-aligned Frame for Form with colors matching the image
    frame_form = tk.Frame(main_window, bg="black", padx=30, pady=215, relief="groove", borderwidth=2)
    frame_form_window = canvas.create_window(0, 0, window=frame_form, anchor="nw")

    # Title with lighter text for contrast
    label_title = tk.Label(frame_form, text="Login", font=('Arial', 30, 'bold'), bg="black", fg="#FFFFFF")
    label_title.grid(row=0, column=0, columnspan=2, pady=100)

    # Username Label and Entry fields
    tk.Label(frame_form, text="Username:", font=('Helvetica', 12), bg="black", fg="#FFFFFF").grid(
        row=1, column=0, sticky="e", padx=10, pady=5)
    entry_username = tk.Entry(frame_form, bg="#FFFFFF", fg="#000000", justify="center", width=25)
    entry_username.grid(row=1, column=1, padx=10, pady=5)

    # Password Label and Entry fields
    tk.Label(frame_form, text="Password:", font=('Helvetica', 12), bg="black", fg="#FFFFFF").grid(
        row=2, column=0, sticky="e", padx=10, pady=5)
    entry_password = tk.Entry(frame_form, show="*", bg="#FFFFFF", fg="#000000", justify="center", width=25)
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    # Load credentials if saved
    username, password, remember_me = load_credentials()
    entry_username.insert(0, username)
    entry_password.insert(0, password)

    remember_me_var = tk.BooleanVar(value=remember_me)

    # Remember Me Checkbox
    checkbox_frame = tk.Frame(frame_form, bg="black")
    checkbox_frame.grid(row=3, column=0, columnspan=2, pady=5)

    check_remember_me = tk.Checkbutton(
        checkbox_frame,
        text="Remember Me",
        variable=remember_me_var,
        bg="black",
        fg="#FFFFFF",
        selectcolor="#444444",
        font=('Helvetica', 10)
    )
    check_remember_me.pack(side="left", padx=10)

    # Show Password Checkbox
    show_password_var = tk.BooleanVar(value=False)

    def toggle_password_visibility():
        if show_password_var.get():
            entry_password.config(show="")  # Show password
        else:
            entry_password.config(show="*")  # Hide password

    check_show_password = tk.Checkbutton(
        checkbox_frame,
        text="Show Password",
        variable=show_password_var,
        command=toggle_password_visibility,
        bg="black",
        fg="#FFFFFF",
        selectcolor="#444444",
        font=('Helvetica', 10)
    )
    check_show_password.pack(side="left", padx=10)

    # Submit Button with gray color and hover effect
    def on_enter(event):
        button_submit.config(bg="#A9A9A9", fg="#000000")  # Lighter gray on hover

    def on_leave(event):
        button_submit.config(bg="#808080", fg="#FFFFFF")  # Return to original color

    button_submit = tk.Button(frame_form, text="Login", font=('Helvetica', 12), command=login_user, 
                               bg="#808080", fg="#FFFFFF", relief="flat", width=20)
    button_submit.bind("<Enter>", on_enter)
    button_submit.bind("<Leave>", on_leave)
    button_submit.grid(row=4, column=0, columnspan=2, pady=15)

    # Toggle to Register Button remains unchanged
    toggle_button = tk.Button(frame_form, text="Don't have an account? Register", command=toggle_to_register,
                               bg="black", fg="#FFFFFF", relief="flat", font=('Helvetica', 10, 'italic'))
    toggle_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Center the Form Dynamically
    main_window.update_idletasks()
    center_form()

    main_window.mainloop()

# Initialize database and show login form
initialize_db()
show_login_form()
