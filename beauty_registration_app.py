import streamlit as st
import random
import re
import csv
import os

# Session state initialization
if 'otp' not in st.session_state:
    st.session_state.otp = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'otp_verified' not in st.session_state:
    st.session_state.otp_verified = False

# Function to generate OTP
def generate_otp():
    return str(random.randint(1000, 9999))

# Function to validate inputs
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

# Function to save data in CSV
def save_to_csv(data, filename="registrations.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "email", "phone", "password"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# UI
st.title("💅 Beauty Academy Admission Form")

# Form
with st.form("registration_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submitted = st.form_submit_button("Submit")

    if submitted:
        error = validate_inputs(name, email, phone, password, confirm_password)
        if error:
            st.error(error)
        else:
            st.session_state.otp = generate_otp()
            st.session_state.user_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": password
            }
            st.success("✅ OTP Sent! (Check below for demo OTP)")
            st.info(f"🔐 Your OTP is: **{st.session_state.otp}**")

# OTP Verification
if st.session_state.otp:
    entered_otp = st.text_input("Enter OTP")
    if st.button("Verify OTP"):
        if entered_otp == st.session_state.otp:
            save_to_csv(st.session_state.user_data)
            st.success("🎉 Registration Confirmed and Saved in CSV!")
            st.session_state.otp_verified = True
            st.session_state.otp = None  # reset OTP
        else:
            st.error("❌ Invalid OTP. Try again.")
