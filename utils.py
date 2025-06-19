from datetime import datetime
import pandas as pd

def format_datetime(date, time):
    """Combine date and time into datetime object"""
    return datetime.combine(date, time)

def validate_date(date):
    """Validate if the date is not in the past"""
    return date >= datetime.now().date()

def calculate_attendance_percentage(present_count, total_meetings):
    """Calculate attendance percentage"""
    if total_meetings == 0:
        return 0
    return (present_count / total_meetings) * 100

def generate_meeting_summary(meetings, username=None, role=None):
    """Generate an automated summary of meetings"""
    if not meetings:
        return "No meetings found for the specified period."

    df = pd.DataFrame(meetings)

    # Filter based on role and username
    if username and role:
        if role == "teacher":
            df = df[df['teacher'] == username]
        elif role == "student":
            df = df[df['student'] == username]

    summary = []

    # Total meetings
    total_meetings = len(df)
    summary.append(f"Total Meetings: {total_meetings}")

    # Recent meetings
    recent_meetings = df[pd.to_datetime(df['date']) >= (datetime.now() - pd.Timedelta(days=30))]
    summary.append(f"Meetings in Last 30 Days: {len(recent_meetings)}")

    # Most common agenda topics (simple keyword extraction)
    if 'agenda' in df.columns and not df['agenda'].empty:
        agendas = ' '.join(df['agenda'].astype(str)).lower()
        common_keywords = pd.Series(agendas.split()).value_counts().head(5)
        summary.append("\nCommon Discussion Topics:")
        for keyword, count in common_keywords.items():
            if len(keyword) > 3:  # Filter out small words
                summary.append(f"- {keyword.title()}: {count} times")

    # Meeting distribution by month
    if not df.empty:
        df['month'] = pd.to_datetime(df['date']).dt.strftime('%B %Y')
        monthly_counts = df['month'].value_counts().sort_index()
        summary.append("\nMonthly Meeting Distribution:")
        for month, count in monthly_counts.items():
            summary.append(f"- {month}: {count} meetings")

    return "\n".join(summary)