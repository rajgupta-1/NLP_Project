import streamlit as st
import random
import requests
import csv
import os

# Your Fast2SMS API key
FAST2SMS_API_KEY = "YOUR_FAST2SMS_API_KEY_HERE"

st.set_page_config(page_title="Beauty Parlour Admission", page_icon="💄")

# Initialize session state
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'otp' not in st.session_state:
    st.session_state.otp = None
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Function to send OTP
def send_otp(phone):
    otp = str(random.randint(1000, 9999))
    st.session_state.otp = otp

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "authorization": FAST2SMS_API_KEY,
        "sender_id": "TXTIND",
        "message": f"Your OTP for admission is {otp}",
        "language": "english",
        "route": "q",
        "numbers": phone,
    }
    headers = {'cache-control': "no-cache"}
    try:
        response = requests.post(url, data=payload, headers=headers)
        st.write("📲 OTP sent to your phone.")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error sending OTP: {e}")
        return False

# Save form data
def save_to_csv(data):
    file_exists = os.path.isfile("admissions.csv")
    try:
        with open("admissions.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Email", "Phone", "Course", "Batch", "Password"])
            writer.writerow([
                data['name'],
                data['email'],
                data['phone'],
                data['course'],
                data['batch'],
                data['password']
            ])
        st.success("🎉 Registration completed and saved successfully!")
    except Exception as e:
        st.error(f"Error saving to file: {e}")

# UI
st.markdown("## 💄 Beauty Parlour Academy - Admission Form")

with st.form("admission_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    course = st.text_input("Course Name (e.g., Makeup, Hair Styling)")
    batch = st.text_input("Preferred Batch Time (Morning/Evening)")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Submit")

    if submit:
        if not all([name, email, phone, course, batch, password, confirm_password]):
            st.error("Please fill all the fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif len(phone) != 10 or not phone.isdigit():
            st.error("Invalid phone number.")
        else:
            st.session_state.form_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "course": course,
                "batch": batch,
                "password": password
            }
            if send_otp(phone):
                st.session_state.otp_sent = True
            else:
                st.error("OTP sending failed. Check your internet or API key.")

# OTP Verification
if st.session_state.otp_sent:
    st.markdown("### 🔐 Enter OTP sent to your phone")
    otp_input = st.text_input("Enter OTP")
    if st.button("Verify OTP"):
        if otp_input == st.session_state.otp:
            save_to_csv(st.session_state.form_data)
            st.session_state.otp_sent = False  # Reset
        else:
            st.error("Incorrect OTP. Please try again.")
