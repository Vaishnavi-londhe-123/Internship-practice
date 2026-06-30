import json
import os

FILE_NAME = "employees.json"


def load_data():
    try:
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, "w") as file:
                json.dump([], file)

        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except:
        return []


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:
        if emp["Emp ID"] == emp_id:
            print("Employee ID already exists.")
            return

    name = input("Enter Employee Name: ")
    department = input("Enter Department: ")

    try:
        salary = float(input("Enter Salary: "))
    except:
        print("Invalid Salary")
        return

    joining_date = input("Enter Joining Date (YYYY-MM-DD): ")

    employee = {
        "Emp ID": emp_id,
        "Name": name,
        "Department": department,
        "Salary": salary,
        "Joining Date": joining_date
    }

    employees.append(employee)
    save_data(employees)

    print("Employee Added Successfully.")


def view_employee():
    employees = load_data()

    if len(employees) == 0:
        print("No Employee Found")
        return

    print("\nEmployee Records\n")

    for emp in employees:
        print(emp)
        print("-" * 40)


def search_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:
        if emp["Emp ID"] == emp_id:
            print(emp)
            return

    print("Employee Not Found")


def update_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID to Update: ")

    for emp in employees:
        if emp["Emp ID"] == emp_id:

            emp["Name"] = input("Enter New Name: ")
            emp["Department"] = input("Enter New Department: ")

            try:
                emp["Salary"] = float(input("Enter New Salary: "))
            except:
                print("Invalid Salary")
                return

            emp["Joining Date"] = input("Enter New Joining Date: ")

            save_data(employees)

            print("Employee Updated Successfully")
            return

    print("Employee Not Found")


def delete_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID to Delete: ")

    for emp in employees:
        if emp["Emp ID"] == emp_id:
            employees.remove(emp)
            save_data(employees)

            print("Employee Deleted Successfully")
            return

    print("Employee Not Found")


while True:

    print("\n========== Employee Management System ==========")
    print("1. Add Employee")
    print("2. View Employee")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employee()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_employee()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        print("Thank You")
        break

    else:
        print("Invalid Choice")