import streamlit as st
from datetime import datetime

def initialize_data():
    """Initialize session state data"""
    if 'users' not in st.session_state:
        st.session_state.users = {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "department": "Administration"
            }
        }

    if 'meetings' not in st.session_state:
        st.session_state.meetings = []

    if 'attendance' not in st.session_state:
        st.session_state.attendance = []

    if 'marks' not in st.session_state:
        st.session_state.marks = []

    if 'proctor_assignments' not in st.session_state:
        st.session_state.proctor_assignments = {}

def get_users():
    """Get all users from session state"""
    if 'users' not in st.session_state:
        initialize_data()
    return st.session_state.users

def add_user(username, user_data):
    """Add a new user to session state"""
    if 'users' not in st.session_state:
        initialize_data()
    st.session_state.users[username] = user_data

def assign_proctor(student, teacher):
    """Assign a teacher as proctor to a student"""
    if 'proctor_assignments' not in st.session_state:
        initialize_data()
    st.session_state.proctor_assignments[student] = teacher

def get_proctor_assignment(student):
    """Get the assigned proctor for a student"""
    return st.session_state.proctor_assignments.get(student)

def get_users_by_role(role):
    """Get all users with a specific role"""
    users = get_users()
    return {username: data for username, data in users.items() 
            if data["role"] == role}

def get_unassigned_students():
    """Get students who don't have an assigned proctor"""
    students = get_users_by_role("student")
    return {username: data for username, data in students.items()
            if username not in st.session_state.proctor_assignments}

def get_teacher_load():
    """Get the number of students assigned to each teacher"""
    teacher_load = {}
    for student, teacher in st.session_state.proctor_assignments.items():
        teacher_load[teacher] = teacher_load.get(teacher, 0) + 1
    return teacher_load

def get_meetings():
    return st.session_state.meetings

def add_meeting(teacher, student, date, time, agenda):
    st.session_state.meetings.append({
        "teacher": teacher,
        "student": student,
        "date": date,
        "time": time,
        "agenda": agenda,
        "id": len(st.session_state.meetings)
    })

def get_student_attendance(student):
    """Get attendance records for a specific student"""
    return [a for a in st.session_state.attendance if a["student"] == student]

def get_teacher_students(teacher):
    """Get all students assigned to a teacher"""
    users = get_users()
    return [username for username, data in users.items() 
            if data["role"] == "student" and 
            data.get("department") == users[teacher].get("department")]

def record_attendance(student, date, status, teacher):
    """Record attendance with more details"""
    st.session_state.attendance.append({
        "student": student,
        "date": date,
        "status": status,
        "teacher": teacher,
        "timestamp": datetime.now()
    })

def get_student_marks(student):
    """Get marks for a specific student"""
    return [m for m in st.session_state.marks if m["student"] == student]

def add_marks(student, subject, marks, assessment_type, teacher, date=None):
    """Add marks with more details"""
    st.session_state.marks.append({
        "student": student,
        "subject": subject,
        "marks": marks,
        "assessment_type": assessment_type,
        "teacher": teacher,
        "date": date or datetime.now()
    })

def update_marks(student, subject, marks, assessment_type, teacher):
    """Update existing marks"""
    # Find and update existing marks or add new entry
    for mark in st.session_state.marks:
        if (mark["student"] == student and 
            mark["subject"] == subject and 
            mark["assessment_type"] == assessment_type):
            mark["marks"] = marks
            mark["teacher"] = teacher
            mark["date"] = datetime.now()
            return True
    return False

def get_department_users(department, role=None):
    """Get all users from a specific department with optional role filter"""
    users = get_users()
    return {
        username: data for username, data in users.items()
        if data.get("department") == department
        and (role is None or data["role"] == role)
    }