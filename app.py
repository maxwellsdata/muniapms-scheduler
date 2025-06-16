
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from collections import defaultdict
import io
import base64

# Page configuration
st.set_page_config(
    page_title="MuniAPMs Task Scheduler",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for MuniAPMs branding and improved contrast
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #00BFFF 0%, #000080 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .section-header {
        background-color: #00BFFF;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-weight: bold;
    }
    
    .info-box {
        background-color: #f0f8ff;
        border-left: 4px solid #00BFFF;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #1a365d !important;
        font-weight: 500;
    }
    
    .warning-box {
        background-color: #fff5f5;
        border-left: 4px solid #ff6b6b;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #742a2a !important;
        font-weight: 500;
    }
    
    .success-box {
        background-color: #f0fff4;
        border-left: 4px solid #68d391;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #22543d !important;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00BFFF 0%, #000080 100%);
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white !important;
    }
    
    .schedule-table {
        border: 2px solid #00BFFF;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    /* Center text in all dataframe tables and ensure proper contrast */
    .stDataFrame > div > div > div > div > table {
        text-align: center;
    }
    
    .stDataFrame > div > div > div > div > table td {
        text-align: center !important;
        color: #1a202c !important;
        font-weight: 500 !important;
    }
    
    .stDataFrame > div > div > div > div > table th {
        text-align: center !important;
        color: #1a202c !important;
        font-weight: 600 !important;
        background-color: #f8f9fa !important;
    }
    
    /* Additional styling for better table appearance */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 2px solid #00BFFF;
    }
    
    /* CRITICAL: Fix team member name visibility in tables */
    .stDataFrame table tbody tr td {
        color: #1a202c !important;
        font-weight: 600 !important;
        background-color: white !important;
    }
    
    .stDataFrame table thead tr th {
        color: #1a202c !important;
        font-weight: 700 !important;
        background-color: #f8f9fa !important;
    }
    
    /* Ensure all text elements have proper contrast */
    .stMarkdown, .stText, p, span, div {
        color: #1a202c !important;
    }
    
    /* Fix multiselect styling for better readability */
    .stMultiSelect > div > div > div {
        background-color: white !important;
        color: #1a202c !important;
    }
    
    .stMultiSelect > div > div > div > div {
        color: #1a202c !important;
        font-weight: 500 !important;
    }
    
    /* Ensure selectbox text is readable */
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: #1a202c !important;
    }
    
    /* Fix form labels and ensure high contrast */
    .stSelectbox label, .stMultiSelect label, label {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* CRITICAL FIX: Ensure team member names are highly visible with bright contrast */
    .stMarkdown strong, strong {
        color: #00BFFF !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        display: inline-block !important;
    }
    
    /* Additional fix for team member name visibility in all contexts */
    .stMarkdown p strong, p strong {
        color: #00BFFF !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        display: inline-block !important;
    }
    
    /* Ensure metric labels (team member names in stats) are visible */
    .stMetric label, .stMetric > div > div > div {
        color: #000080 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 2px 4px !important;
        border-radius: 3px !important;
    }
    
    /* Fix any remaining text visibility issues */
    .stApp > div > div > div > div {
        color: #1a202c !important;
    }
    
    /* Make sure instruction text is clearly visible */
    .stMarkdown p {
        color: #1a202c !important;
        line-height: 1.6;
        font-weight: 500 !important;
    }
    
    /* Ensure metric labels are visible */
    .metric-container label {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
    /* Fix tab text visibility */
    .stTabs [data-baseweb="tab-list"] button {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
    /* Ensure download button text is visible */
    .stDownloadButton > button {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
    /* Hide sidebar completely */
    .css-1d391kg {
        display: none !important;
    }
    
    .css-1cypcdb {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Adjust main content to use full width */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Configuration class
class Config:
    PEOPLE = ["Grace", "Bouj", "Zi", "Dapper", "Max", "Mark"]
    
    TASKS = [
        "Opti (Urgent and Standard)",
        "Sizing", 
        "1st & 2nd File, 2nd round raises",
        "Algo sales, Review 2nd round raises",
        "Review AM Raises, 3rd file"
    ]
    
    TASK_WEIGHTS = {
        "Opti (Urgent and Standard)": 3,
        "Sizing": 2,
        "1st & 2nd File, 2nd round raises": 3,
        "Algo sales, Review 2nd round raises": 2,
        "Review AM Raises, 3rd file": 2
    }
    
    NO_SIZING = ["Zi", "Mark"]
    
    DAY_MAPPING = {
        'monday': 'mon', 'mon': 'mon', 'm': 'mon',
        'tuesday': 'tue', 'tue': 'tue', 'tu': 'tue', 't': 'tue',
        'wednesday': 'wed', 'wed': 'wed', 'w': 'wed',
        'thursday': 'thu', 'thu': 'thu', 'th': 'thu', 'r': 'thu',
        'friday': 'fri', 'fri': 'fri', 'f': 'fri'
    }
    
    WEEKDAYS = ["mon", "tue", "wed", "thu", "fri"]
    WEEKDAY_DISPLAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Task Scheduler class
class TaskScheduler:
    def __init__(self):
        self.people = Config.PEOPLE
        self.tasks = Config.TASKS
        self.task_weights = Config.TASK_WEIGHTS
        self.no_sizing = Config.NO_SIZING
        self.weekdays = Config.WEEKDAYS
        self.weekday_display = Config.WEEKDAY_DISPLAY
        
    def is_valid_assignment(self, person, task, day, availability):
        """Check if a person can be assigned a task on a given day"""
        if day in availability.get(person, []):
            return False
        if task == "Sizing" and person in self.no_sizing:
            return False
        return True
    
    def generate_schedule(self, availability, holidays):
        """Generate the task schedule based on availability and holidays"""
        schedule = {}
        person_tasks = defaultdict(lambda: defaultdict(list))
        person_task_count = defaultdict(lambda: defaultdict(int))
        daily_task_count = defaultdict(lambda: defaultdict(int))
        
        for day in self.weekdays:
            schedule[day] = {}
            
            if day in holidays:
                for task in self.tasks:
                    schedule[day][task] = "🏝️ Holiday"
                continue
            
            for task in self.tasks:
                eligible_people = [
                    person for person in self.people
                    if self.is_valid_assignment(person, task, day, availability)
                ]
                
                if not eligible_people:
                    schedule[day][task] = "❌ No one available"
                    continue
                
                # Priority 1: People with 0 tasks today
                zero_task_people = [p for p in eligible_people if daily_task_count[day][p] == 0]
                
                if zero_task_people:
                    # Among zero-task people, prefer those who haven't done this task
                    never_done_task = [p for p in zero_task_people if person_task_count[p][task] == 0]
                    if never_done_task:
                        chosen = random.choice(never_done_task)
                    else:
                        chosen = random.choice(zero_task_people)
                else:
                    # Priority 2: People who haven't done this task
                    never_done_task = [p for p in eligible_people if person_task_count[p][task] == 0]
                    if never_done_task:
                        chosen = random.choice(never_done_task)
                    else:
                        # Priority 3: Least loaded person
                        min_tasks = min(daily_task_count[day][p] for p in eligible_people)
                        least_loaded = [p for p in eligible_people if daily_task_count[day][p] == min_tasks]
                        chosen = random.choice(least_loaded)
                
                schedule[day][task] = chosen
                person_tasks[chosen][day].append(task)
                person_task_count[chosen][task] += 1
                daily_task_count[day][chosen] += 1
        
        return schedule, person_tasks

def create_schedule_dataframes(schedule):
    """Create DataFrames for display"""
    # Task-by-day view
    task_df = pd.DataFrame(schedule).T
    task_df.index.name = "Day"
    
    # Person-by-day view
    person_schedule = defaultdict(dict)
    for day, tasks in schedule.items():
        for task, person in tasks.items():
            if person not in ["🏝️ Holiday", "❌ No one available"]:
                if person not in person_schedule:
                    person_schedule[person] = {d: [] for d in Config.WEEKDAY_DISPLAY}
                day_display = Config.WEEKDAY_DISPLAY[Config.WEEKDAYS.index(day)]
                person_schedule[person][day_display].append(task)
    
    # Convert to DataFrame
    person_data = {}
    for person in Config.PEOPLE:
        person_data[person] = {}
        for day_display in Config.WEEKDAY_DISPLAY:
            day = Config.WEEKDAYS[Config.WEEKDAY_DISPLAY.index(day_display)]
            if day in schedule and any(schedule[day][task] == person for task in Config.TASKS):
                tasks = [task for task, assigned_person in schedule[day].items() if assigned_person == person]
                person_data[person][day_display] = "; ".join(tasks) if tasks else "😎"
            else:
                person_data[person][day_display] = "😎"
    
    person_df = pd.DataFrame(person_data).T
    person_df.index.name = "Person"
    
    return task_df, person_df

def create_csv_download(df, filename):
    """Create a CSV download link"""
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    # Header
    st.markdown('<div class="main-header">📅 MuniAPMs Task Scheduler</div>', unsafe_allow_html=True)
    
    # Brief instructions
    st.markdown('<div class="info-box"><strong>Quick Start:</strong> Set team availability → Mark holidays → Generate schedule → Download CSV files. Note: Zi and Mark cannot do Sizing tasks.</div>', unsafe_allow_html=True)

    # Initialize session state
    if 'availability' not in st.session_state:
        st.session_state.availability = {}
    if 'holidays' not in st.session_state:
        st.session_state.holidays = []
    if 'schedule_generated' not in st.session_state:
        st.session_state.schedule_generated = False

    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">👥 Team Availability</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">Select the days when each team member is <strong>unavailable</strong> (days off, vacation, etc.)</div>', unsafe_allow_html=True)
        
        availability = {}
        for person in Config.PEOPLE:
            st.write(f"**{person}** - Days unavailable:")
            unavailable_days = st.multiselect(
                f"Select unavailable days for {person}",
                Config.WEEKDAY_DISPLAY,
                key=f"availability_{person}",
                label_visibility="collapsed"
            )
            # Convert to internal format
            availability[person] = [Config.WEEKDAYS[Config.WEEKDAY_DISPLAY.index(day)] for day in unavailable_days]
        
        st.session_state.availability = availability
    
    with col2:
        st.markdown('<div class="section-header">🏝️ Company Holidays</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">Select days when the entire company is closed (holidays, company events, etc.)</div>', unsafe_allow_html=True)
        
        holidays = st.multiselect(
            "Select company-wide holidays",
            Config.WEEKDAY_DISPLAY,
            key="holidays_select"
        )
        # Convert to internal format
        st.session_state.holidays = [Config.WEEKDAYS[Config.WEEKDAY_DISPLAY.index(day)] for day in holidays]
    
    # Generate schedule button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Weekly Schedule", use_container_width=True):
            scheduler = TaskScheduler()
            schedule, person_tasks = scheduler.generate_schedule(
                st.session_state.availability, 
                st.session_state.holidays
            )
            st.session_state.schedule = schedule
            st.session_state.person_tasks = person_tasks
            st.session_state.schedule_generated = True
            st.success("✅ Schedule generated successfully!")
    
    # Display schedule if generated
    if st.session_state.schedule_generated and 'schedule' in st.session_state:
        st.markdown("---")
        st.markdown('<div class="section-header">📊 Generated Schedule</div>', unsafe_allow_html=True)
        
        # Create DataFrames
        task_df, person_df = create_schedule_dataframes(st.session_state.schedule)
        
        # Display tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Task Assignment View", "👤 Individual View", "📈 Statistics"])
        
        with tab1:
            st.markdown("**Task-by-Day Schedule** - Shows who is assigned to each task each day")
            st.dataframe(task_df, use_container_width=True)
            
            # Download button
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_task = task_df.to_csv()
            st.download_button(
                label="📥 Download Task Schedule CSV",
                data=csv_task,
                file_name=f"MuniAPMs_Task_Schedule_{timestamp}.csv",
                mime="text/csv"
            )
        
        with tab2:
            st.markdown("**Person-by-Day Schedule** - Shows what each person is doing each day")
            st.dataframe(person_df, use_container_width=True)
            
            # Download button
            csv_person = person_df.to_csv()
            st.download_button(
                label="📥 Download Individual Schedule CSV",
                data=csv_person,
                file_name=f"MuniAPMs_Individual_Schedule_{timestamp}.csv",
                mime="text/csv"
            )
        
        with tab3:
            st.markdown("**Workload Distribution Statistics**")
            
            # Calculate statistics
            task_counts = defaultdict(int)
            person_task_counts = defaultdict(int)
            
            for day, tasks in st.session_state.schedule.items():
                for task, person in tasks.items():
                    if person not in ["🏝️ Holiday", "❌ No one available"]:
                        task_counts[task] += 1
                        person_task_counts[person] += 1
            
            # Display metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Tasks per Person**")
                for person in Config.PEOPLE:
                    count = person_task_counts[person]
                    st.metric(person, count)
            
            with col2:
                st.markdown("**Task Distribution**")
                for task in Config.TASKS:
                    count = task_counts[task]
                    st.metric(task.split()[0], count)  # Shortened task name
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; padding: 1rem;">© 2024 MuniAPMs Task Scheduler - Optimizing team productivity</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
