import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Paths to images
IMAGE_ABONG_PATH = "Dara.jpg"  # Profile image
IMAGE_ANDREI_PATH = "luther.jpg"  # Profile image
IMAGE_BOSSING_PATH = "arnila.jpg"  # Profile image

# Hover effect functions
def on_hover(event):
    event.widget.config(bg="#e6e6e6", fg="#000000")

def on_leave(event):
    event.widget.config(bg="white", fg="#333333")

# Function to display the dashboard
def show_dashboard(container, switch_to_frame):
    for widget in container.winfo_children():
        widget.destroy()  # Clear the container

    tk.Label(container, text="Home", font=("Helvetica", 20, "bold")).pack(pady=20)

    profiles = [
        ("Sandara Bacus", IMAGE_ABONG_PATH, {
            "First Name": "Sandarah Rich",
            "Middle Name": "Bagares",
            "Last Name": "Bacus",
            "Birth Date": "June 16, 2004",
            "Place of Birth": "Baroy, Lanao Del Norte",
            "Address": "Pob. Sapad, Lanao Del Norte",
            "Status": "Single",
            "Favorite Food": "Hotdog, Humba, Adobo",
            "Hobbies": "Reading, Watching SPG, Playing Badminton"
        }),
        ("Luther Quimbo", IMAGE_ANDREI_PATH, {
            "First Name": "Luther",
            "Middle Name": "Palanas",
            "Last Name": "Quimbo",
            "Birth Date": "Febuary 9, 2002",
            "Place of Birth": "P-7 Butadon Lanao Del Norte",
            "Address": "P-7 Butadon, kapatagan Lanao Del Norte",
            "Status": "Married",
            "Favorite Food": "Pussy",
            "Hobbies": "Playing Basketball"
        }),
        ("Arnila Cajelo", IMAGE_BOSSING_PATH, {
            "First Name": "Arnila",
            "Middle Name": "Ramos",
            "Last Name": "Cajelo",
            "Birth Date": "March 7, 2004",
            "Place of Birth": "Kolambugan Provincial Hospital",
            "Address": "Segapod, Maigo Lanao Del Norte",
            "Status": "Single",
            "Favorite Food": "Lechon manok",
            "Hobbies": "Watching movies"
        }),
    ]

    for profile_name, image_path, profile_details in profiles:
        profile_frame = tk.Frame(container, bg="white", relief="raised", borderwidth=2)
        profile_frame.pack(pady=10, padx=20, fill="x")

        try:
            profile_img = Image.open(image_path).resize((50, 50), Image.LANCZOS)
            profile_photo = ImageTk.PhotoImage(profile_img)
            img_label = tk.Label(profile_frame, image=profile_photo, bg="white")
            img_label.image = profile_photo  # Keep reference
            img_label.pack(side="left", padx=10)
        except:
            tk.Label(profile_frame, text="Image Error", bg="white").pack(side="left", padx=10)

        tk.Label(profile_frame, text=profile_name, font=("Helvetica", 14), bg="white").pack(side="left", padx=20)
        tk.Button(profile_frame, text="View Profile", bg="#555555", fg="white",
                  command=lambda name=profile_name, details=profile_details, path=image_path: switch_to_frame("profile", name, details, path)
                  ).pack(side="right", padx=10)

# Function to display the profile
def show_profile(container, profile_name, profile_details, image_path, switch_to_frame):
    for widget in container.winfo_children():
        widget.destroy()  # Clear the container

    tk.Label(container, text=f"{profile_name}'s Profile", font=("Helvetica", 20, "bold")).pack(pady=20)

    try:
        profile_img = Image.open(image_path).resize((150, 150), Image.LANCZOS)
        profile_photo = ImageTk.PhotoImage(profile_img)
        img_label = tk.Label(container, image=profile_photo, bg="white")
        img_label.image = profile_photo  # Keep reference
        img_label.pack(pady=10)
    except:
        tk.Label(container, text="Image Error", bg="white").pack(pady=10)

    for key, value in profile_details.items():
        tk.Label(container, text=f"{key}: {value}", font=("Helvetica", 14), bg="white").pack(anchor="w", padx=50)

    tk.Button(container, text="Back to Home", command=lambda: switch_to_frame("dashboard"), bg="#555555", fg="white").pack(pady=20)

# Main dashboard function with sidebar integration
def open_dashboard(username, show_login_form):
    """
    Opens a simple dashboard window with a sidebar on the left.
    :param username: The username of the logged-in user.
    :param show_login_form: Function to return to the login form.
    """

    # Create main dashboard window
    dashboard_window = tk.Tk()
    dashboard_window.title("User Dashboard")
    
    # Maximize the window
    dashboard_window.state('zoomed')  # This maximizes the window

    # Create a frame for the sidebar
    sidebar = tk.Frame(dashboard_window, width=350, bg="#2C3E50", height=600)  # Expanded width
    sidebar.pack(side="left", fill="y")

    # Sidebar contents (buttons or labels)
    tk.Button(
        sidebar,
        text="Home",
        command=lambda: show_dashboard(main_content, switch_to_frame),
        font=('Helvetica', 12),
        padx=35,
        pady=5,
        bg="#34495E",
        fg="white",
        anchor="w"
    ).pack(fill="x", pady=5)


    # Logout button placed below in the sidebar
    def logout():
        dashboard_window.destroy()  # Close dashboard window
        show_login_form()  # Return to login UI

    tk.Button(
        sidebar,
        text="Logout",
        command=logout,
        font=('Helvetica', 12),
        padx=10,
        pady=5,
        bg="#E74C3C",  # Red color for logout
        fg="white",
        anchor="w"
    ).pack(fill="x", pady=20)

    # Main content frame (to the right of the sidebar)
    main_content = tk.Frame(dashboard_window, bg="#ECF0F1")
    main_content.pack(side="left", fill="both", expand=True)

    # Function to switch between pages (Dashboard and Profile)
    def switch_to_frame(page, *args):
        if page == "dashboard":
            show_dashboard(main_content, switch_to_frame)
        elif page == "profile":
            profile_name, profile_details, image_path = args
            show_profile(main_content, profile_name, profile_details, image_path, switch_to_frame)

    # Start with the dashboard
    show_dashboard(main_content, switch_to_frame)

    # Main event loop
    dashboard_window.mainloop()

