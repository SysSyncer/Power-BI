import pandas as pd
import random
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()
Faker.seed(0)

# Constants
departments = [
    "Computer Science",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering",
    "Biotechnology",
]
years = [1, 2, 3, 4]
roles = ["Day Scholar", "Hosteller"]
purposes = ["Medical", "Personal", "Academic", "Sports", "Other", "On-Duty"]
statuses = ["Approved", "Rejected"]
tamil_nadu_cities = [
    "Chennai",
    "Coimbatore",
    "Madurai",
    "Tiruchirappalli",
    "Salem",
    "Tirunelveli",
    "Erode",
    "Vellore",
    "Thoothukudi",
    "Nagercoil",
    "Thanjavur",
    "Dindigul",
    "Kanchipuram",
    "Karur",
    "Kumbakonam",
    "Hosur",
    "Pollachi",
    "Rajapalayam",
    "Sivakasi",
    "Udhagamandalam (Ooty)",
]


# Function to generate non-consecutive leave dates
def generate_leave_dates(start_date, num_days):
    dates = [start_date]
    for _ in range(num_days - 1):
        # Add random number of days (1 to 3) for non-consecutive pattern
        start_date += datetime.timedelta(days=random.choice([1, 2, 3]))
        dates.append(start_date)
    return dates


# Generate records for Main Table and Leave Dates Table
num_records = 1000  # Adjust as needed
main_data = []
leave_dates_data = []

for leave_id in range(1, num_records + 1):
    student_id = fake.uuid4()
    student_name = fake.name()
    department = random.choice(departments)
    year = random.choice(years)
    role = random.choice(roles)
    leave_purpose = random.choice(purposes)
    proof_attached = random.choice(["Yes", "No"])
    location = random.choice(tamil_nadu_cities)

    # Generate random start date and non-consecutive leave dates
    start_date = fake.date_between(start_date="-2y", end_date="today")
    num_days = random.randint(1, 5)
    leave_dates = generate_leave_dates(start_date, num_days)

    # Approval statuses for each authority
    class_advisor_status = random.choice(statuses)
    hod_status = random.choice(statuses) if class_advisor_status == "Approved" else None
    warden_status = (
        random.choice(statuses)
        if role == "Hosteller" and hod_status == "Approved"
        else None
    )
    guardian_status = (
        random.choice(statuses)
        if role == "Day Scholar" and hod_status == "Approved"
        else None
    )

    # Append data to the main table
    main_data.append(
        [
            leave_id,
            student_id,
            student_name,
            department,
            year,
            role,
            start_date,
            leave_purpose,
            proof_attached,
            location,
            class_advisor_status,
            hod_status,
            warden_status,
            guardian_status,
        ]
    )

    # Append each leave date to the leave dates table
    for leave_date in leave_dates:
        leave_dates_data.append([leave_id, leave_date])

# Create DataFrames
main_columns = [
    "Leave_ID",
    "Student_ID",
    "Student_Name",
    "Department",
    "Year",
    "Role",
    "Start_Date",
    "Leave_Purpose",
    "Proof_Attached",
    "Location",
    "Class_Advisor_Status",
    "HoD_Status",
    "Warden_Status",
    "Guardian_Status",
]
leave_dates_columns = ["Leave_ID", "Leave_Date"]

df_main = pd.DataFrame(main_data, columns=main_columns)
df_leave_dates = pd.DataFrame(leave_dates_data, columns=leave_dates_columns)

# Save both DataFrames to Excel
with pd.ExcelWriter("leave_management_normalized.xlsx") as writer:
    df_main.to_excel(writer, sheet_name="Main_Leave_Table", index=False)
    df_leave_dates.to_excel(writer, sheet_name="Leave_Dates_Table", index=False)

print("Normalized dataset generated and saved as 'leave_management_normalized.xlsx'")
