# Student Marks Sheet Management System
# Author: OpenAI ChatGPT
# Date: 2024-04-27

import json
import os

# File to store student data
DATA_FILE = 'students_data.json'

# Subjects list
SUBJECTS = ['Mathematics', 'Physics', 'Chemistry', 'English', 'Computer Science']

def load_data():
    """Load student data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            return {}

def save_data(data):
    """Save student data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_student_id(data):
    """Generate a unique student ID."""
    if not data:
        return 'S001'
    else:
        ids = [int(sid[1:]) for sid in data.keys()]
        new_id = max(ids) + 1
        return f'S{new_id:03}'

def add_student(data):
    """Add a new student to the system."""
    print("\n--- Add New Student ---")
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    student_id = generate_student_id(data)
    data[student_id] = {
        'name': name,
        'marks': {subject: 0 for subject in SUBJECTS}
    }
    save_data(data)
    print(f"Student '{name}' added with ID: {student_id}")

def add_marks(data):
    """Add or update marks for a student."""
    print("\n--- Add/Update Marks ---")
    student_id = input("Enter student ID: ").strip().upper()
    if student_id not in data:
        print("Student ID not found.")
        return
    print(f"Entering marks for {data[student_id]['name']}:")
    for subject in SUBJECTS:
        while True:
            try:
                mark = float(input(f"Enter marks for {subject}: "))
                if 0 <= mark <= 100:
                    data[student_id]['marks'][subject] = mark
                    break
                else:
                    print("Please enter a mark between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
    save_data(data)
    print(f"Marks updated for student ID: {student_id}")

def view_marks(data):
    """View marks of all students."""
    print("\n--- View All Students' Marks ---")
    if not data:
        print("No student data available.")
        return
    header = f"{'ID':<6} {'Name':<20}" + "".join([f"{sub[:4]:<10}" for sub in SUBJECTS]) + f"{'Total':<10} {'Average':<10} {'Grade':<6}"
    print(header)
    print("-" * len(header))
    for sid, info in data.items():
        marks = info['marks']
        total = sum(marks.values())
        average = total / len(SUBJECTS)
        grade = calculate_grade(average)
        marks_str = "".join([f"{marks[sub]:<10}" for sub in SUBJECTS])
        print(f"{sid:<6} {info['name']:<20}{marks_str}{total:<10}{average:<10.2f}{grade:<6}")

def calculate_grade(average):
    """Calculate grade based on average marks."""
    if average >= 90:
        return 'A+'
    elif average >= 80:
        return 'A'
    elif average >= 70:
        return 'B'
    elif average >= 60:
        return 'C'
    elif average >= 50:
        return 'D'
    else:
        return 'F'

def search_student(data):
    """Search for a student by ID or name."""
    print("\n--- Search Student ---")
    choice = input("Search by (1) ID or (2) Name? Enter 1 or 2: ").strip()
    if choice == '1':
        student_id = input("Enter student ID: ").strip().upper()
        if student_id in data:
            display_student(student_id, data)
        else:
            print("Student ID not found.")
    elif choice == '2':
        name = input("Enter student name: ").strip().lower()
        found = False
        for sid, info in data.items():
            if info['name'].lower() == name:
                display_student(sid, data)
                found = True
        if not found:
            print("No student found with that name.")
    else:
        print("Invalid choice.")

def display_student(sid, data):
    """Display a single student's details."""
    info = data[sid]
    print(f"\nStudent ID: {sid}")
    print(f"Name: {info['name']}")
    print("Marks:")
    for subject, mark in info['marks'].items():
        print(f"  {subject}: {mark}")
    total = sum(info['marks'].values())
    average = total / len(SUBJECTS)
    grade = calculate_grade(average)
    print(f"Total: {total}")
    print(f"Average: {average:.2f}")
    print(f"Grade: {grade}")

def update_marks(data):
    """Update marks for a specific student."""
    print("\n--- Update Marks ---")
    student_id = input("Enter student ID: ").strip().upper()
    if student_id not in data:
        print("Student ID not found.")
        return
    print(f"Updating marks for {data[student_id]['name']}:")
    for subject in SUBJECTS:
        while True:
            try:
                mark = float(input(f"Enter new marks for {subject} (current: {data[student_id]['marks'][subject]}): "))
                if 0 <= mark <= 100:
                    data[student_id]['marks'][subject] = mark
                    break
                else:
                    print("Please enter a mark between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
    save_data(data)
    print("Marks updated successfully.")

def delete_student(data):
    """Delete a student from the system."""
    print("\n--- Delete Student ---")
    student_id = input("Enter student ID to delete: ").strip().upper()
    if student_id in data:
        confirm = input(f"Are you sure you want to delete {data[student_id]['name']}? (y/n): ").strip().lower()
        if confirm == 'y':
            del data[student_id]
            save_data(data)
            print("Student deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("Student ID not found.")

def generate_report(data):
    """Generate a summary report."""
    print("\n--- Summary Report ---")
    total_students = len(data)
    if total_students == 0:
        print("No data available.")
        return
    total_marks = {subject: 0 for subject in SUBJECTS}
    grade_distribution = {'A+':0, 'A':0, 'B':0, 'C':0, 'D':0, 'F':0}
    for info in data.values():
        for subject, mark in info['marks'].items():
            total_marks[subject] += mark
        average = sum(info['marks'].values()) / len(SUBJECTS)
        grade = calculate_grade(average)
        grade_distribution[grade] += 1
    print(f"Total Students: {total_students}")
    print("\nAverage Marks per Subject:")
    for subject in SUBJECTS:
        avg = total_marks[subject] / total_students
        print(f"  {subject}: {avg:.2f}")
    print("\nGrade Distribution:")
    for grade, count in grade_distribution.items():
        print(f"  {grade}: {count}")

def display_main_menu():

    print("\n=== Student Marks Sheet Management System ===")
    print("1. Add New Student")
    print("2. Add/Update Marks")
    print("3. View All Marks")
    print("4. Search Student")
    print("5. Update Marks")
    print("6. Delete Student")
    print("7. Generate Report")
    print("8. Exit")


def main_menu(user_choice):
    """Display the main menu and handle user choices."""
    data = load_data()
    print("\n=== Student Marks Sheet Management System ===")
    print("1. Add New Student")
    print("2. Add/Update Marks")
    print("3. View All Marks")
    print("4. Search Student")
    print("5. Update Marks")
    print("6. Delete Student")
    print("7. Generate Report")
    print("8. Exit")
    if user_choice == '1':
        add_student(data)
    elif user_choice == '2':
        add_marks(data)
    elif user_choice == '3':
        view_marks(data)
    elif user_choice == '4':
        search_student(data)
    elif user_choice == '5':
        update_marks(data)
    elif user_choice == '6':
        delete_student(data)
    elif user_choice == '7':
        generate_report(data)
    elif user_choice == '8':
        print("Exiting the system. Goodbye!")
    else:
        print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":

    display_main_menu()
    while 1:
        choice = input("Enter your choice: ")
        main_menu(choice)
