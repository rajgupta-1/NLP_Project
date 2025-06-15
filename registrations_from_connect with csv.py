import tkinter as tk
from tkinter import messagebox
import random
import re
import csv
import os

# Globals
otp_generated = ""
user_data = {}

# OTP Generator
def generate_otp():
    return str(random.randint(1000, 9999))

# Input Validation
def validate_inputs(name, email, phone, password, confirm_password):
    if not all([name, email, phone, password, confirm_password]):
        return "All fields are required."
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format."
    if password != confirm_password:
        return "Passwords do not match."
    if not phone.isdigit() or len(phone) != 10:
        return "Phone number must be 10 digits."
    return None

# Save to CSV File
def save_to_csv(data, filename="registrations.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "email", "phone", "password"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Submit Form
def submit_form():
    global otp_generated, user_data

    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    error = validate_inputs(name, email, phone, password, confirm_password)
    if error:
        messagebox.showerror("Error", error)
        return

    otp_generated = generate_otp()
    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }

    print(f"[Console OTP] Your OTP is: {otp_generated}")  # Simulate SMS
    root.withdraw()
    show_otp_window()

# OTP Window
def show_otp_window():
    global otp_entry, otp_window

    otp_window = tk.Toplevel()
    otp_window.title("Enter OTP")
    otp_window.geometry("300x150")

    tk.Label(otp_window, text="Enter OTP:").pack(pady=10)
    otp_entry = tk.Entry(otp_window)
    otp_entry.pack()

    tk.Button(otp_window, text="Verify OTP", command=verify_otp).pack(pady=10)

# OTP Verification
def verify_otp():
    entered_otp = otp_entry.get()
    if entered_otp == otp_generated:
        save_to_csv(user_data)
        messagebox.showinfo("Success", "🎉 Registration Confirmed and Saved in CSV!")
        otp_window.destroy()
        root.destroy()
    else:
        messagebox.showerror("Failed", "❌ Invalid OTP. Please try again.")

# GUI Setup
root = tk.Tk()
root.title("Beauty Academy Registration")
root.geometry("400x400")

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Phone Number").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Label(root, text="Confirm Password").pack()
entry_confirm_password = tk.Entry(root, show="*")
entry_confirm_password.pack()

tk.Button(root, text="Submit", command=submit_form, bg="blue", fg="white").pack(pady=20)

root.mainloop()
