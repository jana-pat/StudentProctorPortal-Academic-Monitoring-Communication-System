import streamlit as st
from data_store import get_users, add_user

def login_page():
    st.subheader("Welcome to Student Proctor Management System")

    # Add some educational styling
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton button {
        background-color: #1f77b4;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_button"):
            if not username or not password:
                st.error("Please enter both username and password")
                return

            users = get_users()
            if username in users and users[username]["password"] == password:
                # Set session state
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = users[username]["role"]
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    with tab2:
        st.subheader("New User Registration")

        reg_username = st.text_input("Choose Username", key="reg_username")
        reg_password = st.text_input("Choose Password", type="password", key="reg_password")
        role = st.selectbox("Select Role", ["student", "teacher"])
        department = st.text_input("Department")

        # Role-specific educational background fields
        user_data = {
            "password": reg_password,
            "role": role,
            "department": department
        }

        if role == "student":
            semester = st.selectbox("Semester", range(1, 9))
            roll_number = st.text_input("Roll Number")
            user_data.update({
                "semester": semester,
                "roll_number": roll_number
            })
        else:  # teacher
            specialization = st.text_input("Specialization")
            years_of_experience = st.number_input("Years of Experience", min_value=0)
            user_data.update({
                "specialization": specialization,
                "years_of_experience": years_of_experience
            })

        if st.button("Register", key="register_button"):
            if not reg_username or not reg_password or not department:
                st.error("Please fill all required fields!")
                return

            users = get_users()
            if reg_username in users:
                st.error("Username already exists!")
            else:
                add_user(reg_username, user_data)
                st.success("Registration successful! Please login.")

def logout():
    for key in ['logged_in', 'user_role', 'username']:
        if key in st.session_state:
            del st.session_state[key]