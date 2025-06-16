
"""
Utility functions for the MuniAPMs Task Scheduler
"""

import pandas as pd
from datetime import datetime
from collections import defaultdict

def validate_availability_input(availability_data):
    """
    Validate availability input data
    
    Args:
        availability_data (dict): Dictionary of person -> list of unavailable days
    
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check if all required people are present
    required_people = ["MG", "Anna", "Zi", "Dan", "Max", "Mark"]
    for person in required_people:
        if person not in availability_data:
            errors.append(f"Missing availability data for {person}")
    
    # Check for valid day formats
    valid_days = ["mon", "tue", "wed", "thu", "fri"]
    for person, days in availability_data.items():
        for day in days:
            if day not in valid_days:
                errors.append(f"Invalid day '{day}' for {person}")
    
    return len(errors) == 0, errors

def calculate_workload_statistics(schedule):
    """
    Calculate workload distribution statistics
    
    Args:
        schedule (dict): Generated schedule dictionary
    
    Returns:
        dict: Statistics including task counts, person loads, etc.
    """
    stats = {
        'person_task_counts': defaultdict(int),
        'task_distribution': defaultdict(int),
        'daily_loads': defaultdict(lambda: defaultdict(int)),
        'total_tasks': 0,
        'holiday_days': 0,
        'unassigned_tasks': 0
    }
    
    for day, tasks in schedule.items():
        for task, person in tasks.items():
            if person == "🏝️ Holiday":
                stats['holiday_days'] += 1
            elif person == "❌ No one available":
                stats['unassigned_tasks'] += 1
            else:
                stats['person_task_counts'][person] += 1
                stats['task_distribution'][task] += 1
                stats['daily_loads'][day][person] += 1
                stats['total_tasks'] += 1
    
    return stats

def format_schedule_for_export(schedule, format_type="task_view"):
    """
    Format schedule data for export
    
    Args:
        schedule (dict): Generated schedule dictionary
        format_type (str): "task_view" or "person_view"
    
    Returns:
        pd.DataFrame: Formatted DataFrame ready for export
    """
    if format_type == "task_view":
        # Task-by-day view
        df = pd.DataFrame(schedule).T
        df.index.name = "Day"
        
        # Add day names
        day_mapping = {
            "mon": "Monday",
            "tue": "Tuesday", 
            "wed": "Wednesday",
            "thu": "Thursday",
            "fri": "Friday"
        }
        df.index = [day_mapping.get(day, day) for day in df.index]
        
    else:  # person_view
        # Person-by-day view
        person_schedule = defaultdict(dict)
        weekdays = ["mon", "tue", "wed", "thu", "fri"]
        weekday_display = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        people = ["MG", "Anna", "Zi", "Dan", "Max", "Mark"]
        
        for day, tasks in schedule.items():
            for task, person in tasks.items():
                if person not in ["🏝️ Holiday", "❌ No one available"]:
                    if person not in person_schedule:
                        person_schedule[person] = {d: [] for d in weekday_display}
                    day_display = weekday_display[weekdays.index(day)]
                    person_schedule[person][day_display].append(task)
        
        # Convert to DataFrame
        person_data = {}
        for person in people:
            person_data[person] = {}
            for day_display in weekday_display:
                day = weekdays[weekday_display.index(day_display)]
                if day in schedule and any(schedule[day][task] == person for task in schedule[day].keys()):
                    tasks = [task for task, assigned_person in schedule[day].items() if assigned_person == person]
                    person_data[person][day_display] = "; ".join(tasks) if tasks else "😎"
                else:
                    person_data[person][day_display] = "😎"
        
        df = pd.DataFrame(person_data).T
        df.index.name = "Person"
    
    return df

def generate_filename(base_name, file_type="csv"):
    """
    Generate timestamped filename
    
    Args:
        base_name (str): Base name for the file
        file_type (str): File extension
    
    Returns:
        str: Timestamped filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"MuniAPMs_{base_name}_{timestamp}.{file_type}"

def check_schedule_conflicts(schedule):
    """
    Check for potential conflicts in the schedule
    
    Args:
        schedule (dict): Generated schedule dictionary
    
    Returns:
        list: List of conflict descriptions
    """
    conflicts = []
    
    # Check for unassigned tasks
    for day, tasks in schedule.items():
        for task, person in tasks.items():
            if person == "❌ No one available":
                conflicts.append(f"No one available for '{task}' on {day}")
    
    # Check for overloaded days
    daily_loads = defaultdict(lambda: defaultdict(int))
    for day, tasks in schedule.items():
        for task, person in tasks.items():
            if person not in ["🏝️ Holiday", "❌ No one available"]:
                daily_loads[day][person] += 1
    
    for day, person_loads in daily_loads.items():
        for person, load in person_loads.items():
            if load > 3:  # More than 3 tasks per day might be too much
                conflicts.append(f"{person} has {load} tasks on {day} - consider redistributing")
    
    return conflicts
