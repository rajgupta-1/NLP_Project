import tkinter as tk
from tkinter import messagebox

def submit_form():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()

    if name and age and city and contact and email:
        result_label.config(text=f"Name: {name}\nAge: {age}\nCity: {city}\nContact: {contact}\nEmail: {email}")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# Create main window
root = tk.Tk()
root.title("Registration Form by Raj")
root.geometry("500x600")

# Labels and Entry fields
tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Age:").pack(pady=5)
age_entry = tk.Entry(root)
age_entry.pack(pady=5)

tk.Label(root, text="City:").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

tk.Label(root, text="Contact:").pack(pady=5)
contact_entry = tk.Entry(root)
contact_entry.pack(pady=5)

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

# Submit Button
submit_btn = tk.Button(root, text="Submit", command=submit_form)
submit_btn.pack(pady=10)

# Label to display submitted data
result_label = tk.Label(root, text="", fg="blue", font=("Arial", 10, "bold"))
result_label.pack(pady=10)

# Run the application
root.mainloop()
