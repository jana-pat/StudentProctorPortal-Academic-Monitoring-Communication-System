import streamlit as st
import auth
import components.admin as admin
import components.teacher as teacher
import components.student as student
from data_store import initialize_data

st.set_page_config(
    page_title="Student Proctor Management System",
    page_icon="📚",
    layout="wide"
)

def main():
    # Initialize session state
    if 'initialized' not in st.session_state:
        initialize_data()
        st.session_state.initialized = True

    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None

    # Display header
    st.title("Student Proctor Management System")

    if not st.session_state.logged_in:
        auth.login_page()
    else:
        # Display logout button
        col1, col2 = st.columns([6,1])
        with col2:
            if st.button("Logout"):
                auth.logout()
                st.experimental_rerun()
        
        with col1:
            st.write(f"Welcome, {st.session_state.username} ({st.session_state.user_role})")

        # Role-based rendering
        if st.session_state.user_role == "admin":
            admin.render_admin_page()
        elif st.session_state.user_role == "teacher":
            teacher.render_teacher_page()
        elif st.session_state.user_role == "student":
            student.render_student_page()

if __name__ == "__main__":
    main()
