from flask import Flask, request, jsonify
from models import db, Employee, User
from datetime import datetime
import config

app = Flask(__name__)
app.secret_key = "employee_login_api"

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize Database
db.init_app(app)

# Create Table
with app.app_context():
    db.create_all()


# ------------------ ADD EMPLOYEE ------------------

@app.route('/employee', methods=['POST'])
def add_employee():
    try:
        data = request.json
        
        # -------- Validation --------

        if not data.get("Emp_Name"):
            return jsonify({"message": "Employee Name is required"}), 400

        if not data.get("Department_Name"):
            return jsonify({"message": "Department Name is required"}), 400

        if not data.get("Salary"):
            return jsonify({"message": "Salary is required"}), 400

        if not data.get("Joining_Date"):
            return jsonify({"message": "Joining Date is required"}), 400

        if not data.get("Email"):
            return jsonify({"message": "Email is required"}), 400

        if not data.get("City"):
            return jsonify({"message": "City is required"}), 400

        # -------- Employee Object --------

        emp = Employee(
            Emp_Name=data["Emp_Name"],
            Department_Name=data["Department_Name"],
            Salary=float(data["Salary"]),
            Joining_Date=datetime.strptime(
                data["Joining_Date"], "%Y-%m-%d"
            ).date(),
            Email=data["Email"],
            City=data["City"]
        )

        db.session.add(emp)
        db.session.commit()

        return jsonify({"message": "Employee Added Successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ GET ALL EMPLOYEES ------------------

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])


# ------------------ GET EMPLOYEE BY ID ------------------

@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    emp = Employee.query.get(id)

    if emp:
        return jsonify(emp.to_dict())

    return jsonify({"message": "Employee Not Found"}), 404


# ------------------ UPDATE EMPLOYEE ------------------

@app.route('/employee/<int:id>', methods=['PUT'])
def update_employee(id):
    emp = Employee.query.get(id)

    if not emp:
        return jsonify({"message": "Employee Not Found"}), 404

    try:
        data = request.json

        # -------- Validation --------

        if not data.get("Emp_Name"):
            return jsonify({"message": "Employee Name is required"}), 400

        if not data.get("Department_Name"):
            return jsonify({"message": "Department Name is required"}), 400

        if not data.get("Salary"):
            return jsonify({"message": "Salary is required"}), 400

        if not data.get("Joining_Date"):
            return jsonify({"message": "Joining Date is required"}), 400

        if not data.get("Email"):
            return jsonify({"message": "Email is required"}), 400

        if not data.get("City"):
            return jsonify({"message": "City is required"}), 400

        # -------- Employee Object --------

        emp.Emp_Name = data["Emp_Name"]
        emp.Department_Name = data["Department_Name"]
        emp.Salary = float(data["Salary"])
        emp.Joining_Date = datetime.strptime(
            data["Joining_Date"], "%Y-%m-%d"
        ).date()
        emp.Email=data["Email"]
        emp.City=data["City"]

        db.session.commit()

        return jsonify({"message": "Employee Updated Successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ DELETE EMPLOYEE ------------------

@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    emp = Employee.query.get(id)

    if not emp:
        return jsonify({"message": "Employee Not Found"}), 404

    db.session.delete(emp)
    db.session.commit()

    return jsonify({"message": "Employee Deleted Successfully"})

# ------------------ SEARCH EMPLOYEE BY NAME ------------------

@app.route('/employee/search/name', methods=['GET'])
def search_by_name():

    name = request.args.get("name")

    employees = Employee.query.filter(Employee.Emp_Name.ilike(f"%{name}%")).all()

    return jsonify([emp.to_dict() for emp in employees])

# ------------------ SEARCH EMPLOEE BY EMAIL ------------------

@app.route('/employee/search/email', methods=['GET'])
def search_by_email():

    email = request.args.get("email")

    employees = Employee.query.filter(
        Employee.Email.ilike(f"%{email}%")
    ).all()

    return jsonify([emp.to_dict() for emp in employees])


# ------------------ SEARCH EMPLOEE BY DEPARTMENT ------------------

@app.route('/employee/search/department', methods=['GET'])
def search_by_department():

    department = request.args.get("department")

    employees = Employee.query.filter(
        Employee.Department_Name.ilike(f"%{department}%")
    ).all()

    return jsonify([emp.to_dict() for emp in employees])


# ------------------ SEARCH EMPLOEE BY CITY ------------------

@app.route('/employee/search/city', methods=['GET'])
def search_by_city():

    city = request.args.get("city")

    employees = Employee.query.filter(
        Employee.City.ilike(f"%{city}%")
    ).all()

    return jsonify([emp.to_dict() for emp in employees])


# ------------------ PAGINATION ------------------

@app.route('/employees/page', methods=['GET'])
def pagination():

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    employees = Employee.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": employees.total,
        "employees": [emp.to_dict() for emp in employees.items]
    })


# ------------------ SORT ASCENDING ------------------

@app.route('/employees/sort/asc', methods=['GET'])
def sort_ascending():

    employees = Employee.query.order_by(Employee.Emp_Name.asc()).all()

    return jsonify([emp.to_dict() for emp in employees])


# ------------------ SORT DESCENDING ------------------

@app.route('/employees/sort/desc', methods=['GET'])
def sort_descending():

    employees = Employee.query.order_by(Employee.Emp_Name.desc()).all()

    return jsonify([emp.to_dict() for emp in employees])

# ------------------ SIGN UP ------------------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    if not data.get("Name"):
       return jsonify({"message":"Name is required"}),400

    if not data.get("Email"):
       return jsonify({"message":"Email is required"}),400

    if not data.get("Password"):
       return jsonify({"message":"Password is required"}),400

    existing_user = User.query.filter_by(Email=data["Email"]).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(
        Name=data["Name"],
        Email=data["Email"],
        Password=data["Password"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup Successful"})

# ------------------ LOGIN  ------------------

@app.route('/login', methods=['POST'])
def login():

    data = request.json
    
    if not data.get("Email"):
       return jsonify({"message":"Email is required"}),400

    if not data.get("Password"):
       return jsonify({"message":"Password is required"}),400

    user = User.query.filter_by(
        Email=data["Email"],
        Password=data["Password"]
    ).first()

    if user:
        return jsonify({
            "message": "Login Successful"
        })

    return jsonify({
        "message": "Invalid Email or Password"
    }), 401
    
# ------------------ LOG OUT  ------------------

@app.route('/logout', methods=['POST'])
def logout():

    return jsonify({
        "message": "Logout Successful"
    })    
    
# ------------------ RUN APP ------------------

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)