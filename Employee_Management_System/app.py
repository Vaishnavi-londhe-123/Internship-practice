from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from models import db, Employee, User
from datetime import datetime, timedelta
import config
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

app.secret_key = "employee_login_api"

app.config["JWT_SECRET_KEY"] = "my_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize Database
db.init_app(app)

# Create Table
with app.app_context():
    db.create_all()
  
# ------------------ HOME ------------------

@app.route('/')
def home():
    return render_template("login.html")


# ------------------ REGISTER PAGE ------------------

@app.route('/register')
def register():
    return render_template("register.html")    


# ------------------ ADD EMPLOYEE ------------------

@app.route('/employee', methods=['POST'])
def add_employee():

    try:
        data = request.json

        # Validation

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
        
        if not data.get("Mobile_Number"):
            return jsonify({"message": "Mobile Number is required"}), 400

        if not data.get("City"):
            return jsonify({"message": "City is required"}), 400

        # Mobile Number Validation
        if not data.get("Mobile_Number"):
           return jsonify({"message": "Mobile Number is required"}), 400

        if not data["Mobile_Number"].isdigit():
           return jsonify({"message": "Mobile Number must contain only digits"}), 400

        if len(data["Mobile_Number"]) != 10:
           return jsonify({"message": "Mobile Number must be exactly 10 digits"}), 400

        emp = Employee(
            Emp_Name=data["Emp_Name"],
            Department_Name=data["Department_Name"],
            Salary=float(data["Salary"]),
            Joining_Date=datetime.strptime(
                data["Joining_Date"], "%Y-%m-%d"
            ).date(),
            Email=data["Email"],
            Mobile_Number=data["Mobile_Number"],
            City=data["City"]
        )

        db.session.add(emp)
        db.session.commit()

        return jsonify({
            "message": "Employee Added Successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

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
       
        if not data.get("Mobile_Number"):
           return jsonify({"message": "Mobile Number is required"}), 400

        if not data.get("City"):
           return jsonify({"message": "City is required"}), 400

        # Mobile Number Validation
        if not data.get("Mobile_Number"):
           return jsonify({"message": "Mobile Number is required"}), 400

        if not data["Mobile_Number"].isdigit():
          return jsonify({"message": "Mobile Number must contain only digits"}), 400

        if len(data["Mobile_Number"]) != 10:
          return jsonify({"message": "Mobile Number must be exactly 10 digits"}), 400

        emp.Emp_Name = data["Emp_Name"]
        emp.Department_Name = data["Department_Name"]
        emp.Salary = float(data["Salary"])
        emp.Joining_Date = datetime.strptime(
            data["Joining_Date"], "%Y-%m-%d"
        ).date()
        emp.Email = data["Email"]
        emp.Mobile_Number = data["Mobile_Number"]
        emp.City = data["City"]

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

# ------------------ SEARCH EMPLOYEE BY EMAIL ------------------

@app.route('/employee/search/email', methods=['GET'])
def search_by_email():

    email = request.args.get("email")

    employees = Employee.query.filter(
        Employee.Email.ilike(f"%{email}%")
    ).all()

    return jsonify([emp.to_dict() for emp in employees])


# ------------------ SEARCH EMPLOYEE BY DEPARTMENT ------------------

@app.route('/employee/search/department', methods=['GET'])
def search_by_department():

    department = request.args.get("department")

    employees = Employee.query.filter(
        Employee.Department_Name.ilike(f"%{department}%")
    ).all()

    return jsonify([emp.to_dict() for emp in employees])


# ------------------ SEARCH EMPLOYEE BY CITY ------------------

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

    data = request.form

    # Validation

    if not data.get("Name"):
        return "Name is required"

    if not data.get("Email"):
        return "Email is required"

    if not data.get("Password"):
        return "Password is required"

    existing_user = User.query.filter_by(Email=data["Email"]).first()

    if existing_user:
        return "Email already exists"

    new_user = User(
        Name=data["Name"],
        Email=data["Email"],
        Password=data["Password"],
        Role="user"
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))

# ------------------ LOGIN ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        return render_template("login.html")

    data = request.form

    if not data.get("Email"):
        return "Email is required"

    if not data.get("Password"):
        return "Password is required"

    user = User.query.filter_by(
        Email=data["Email"],
        Password=data["Password"]
    ).first()

    if user:
        
        access_token = create_access_token(identity=user.User_ID)
        refresh_token = create_refresh_token(identity=user.User_ID)

        # Save Session
        session["user_id"] = user.User_ID
        session["user_name"] = user.Name
        session["user_role"] = user.Role

        # Role Based Login
        if user.Role.lower() == "admin":
            return redirect(url_for("dashboard"))

        return redirect(url_for("user_dashboard"))

    return "Invalid Email or Password"

    
# ---------------- USER DASHBOARD ----------------

@app.route("/user-dashboard")
def user_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"].lower() != "user":
        return redirect(url_for("dashboard"))

    user = User.query.get(session["user_id"])

    return render_template(
        "user_dashboard.html",
        user=user
    )
    
# ------------------ DASHBOARD ------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"].lower() != "admin":
        return redirect(url_for("user_dashboard"))

    total_employees = Employee.query.count()

    active_records = Employee.query.count()

    recent_employees = Employee.query.order_by(
        Employee.Emp_ID.desc()
    ).limit(5).all()

    hr_count = Employee.query.filter_by(
        Department_Name="HR"
    ).count()

    it_count = Employee.query.filter_by(
        Department_Name="IT"
    ).count()

    sales_count = Employee.query.filter_by(
        Department_Name="Sales"
    ).count()
    
    finance_count = Employee.query.filter_by(
    Department_Name="Finance"
    ).count()

    employees = Employee.query.all()

    joining_data = {}

    for emp in employees:
        month = emp.Joining_Date.strftime("%b-%Y")   # Example: Jul-2025

        if month in joining_data:
          joining_data[month] += 1
        else:
          joining_data[month] = 1

    # Sort by actual date
    sorted_data = sorted(
    joining_data.items(),
    key=lambda x: datetime.strptime(x[0], "%b-%Y")
    )

    joining_months = [item[0] for item in sorted_data]
    joining_counts = [item[1] for item in sorted_data]
    
    print(joining_months)
    print(joining_counts)
    
    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        active_records=active_records,
        recent_employees=recent_employees,
        hr_count=hr_count,
        it_count=it_count,
        sales_count=sales_count,
        finance_count=finance_count,
        joining_months=joining_months,
        joining_counts=joining_counts
    )
# ------------------ EMPLOYEES LIST PAGE ------------------
    
@app.route('/employees-list')
def employees_list():
    
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"].lower() != "admin":
        return redirect(url_for("user_dashboard"))

    page = request.args.get("page", 1, type=int)

    employees = Employee.query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "employees.html",
        employees=employees.items,
        title="Employees",
        page=page,
        total_pages=employees.pages
    )
    
# ------------------ SEARCH EMPLOYEE PAGE ------------------

@app.route('/employee-search')
def employee_search():

    name = request.args.get("name", "")
    order = request.args.get("order", "")

    employees = Employee.query.filter(
        Employee.Emp_Name.ilike(f"%{name}%")
    )

    if order == "asc":
        employees = employees.order_by(Employee.Emp_Name.asc())

    elif order == "desc":
        employees = employees.order_by(Employee.Emp_Name.desc())

    employees = employees.all()

    return render_template(
        "employees.html",
        employees=employees,
        title="Employees"
    )
    
# ------------------ SORT EMPLOYEE ------------------

@app.route('/employee-sort')
def employee_sort():

    order = request.args.get("order")

    if order == "asc":
        employees = Employee.query.order_by(Employee.Emp_Name.asc()).all()
    else:
        employees = Employee.query.order_by(Employee.Emp_Name.desc()).all()

    return render_template(
        "employees.html",
        employees=employees,
        title="Employees"
    )    

# ------------------ TOTAL EMPLOYEES ------------------

@app.route('/total-employees')
def total_employees_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"].lower() != "admin":
        return redirect(url_for("user_dashboard"))

    page = request.args.get("page", 1, type=int)

    employees = Employee.query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "employees.html",
        employees=employees.items,
        title="Total Employees",
        page=page,
        total_pages=employees.pages
    )

# ------------------ ACTIVE RECORDS ------------------

@app.route('/active-records')
def active_records_page():

    page = request.args.get("page", 1, type=int)

    employees = Employee.query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "employees.html",
        employees=employees.items,
        title="Active Records",
        page=page,
        total_pages=employees.pages
    )


# ------------------ RECENTLY ADDED ------------------

@app.route('/recently-added')
def recently_added_page():

    employees = Employee.query.order_by(
        Employee.Emp_ID.desc()
    ).limit(5).all()

    return render_template(
        "employees.html",
        employees=employees,
        title="Recently Added Employees",
        page=1,
        total_pages=1
    ) 
    
# ------------------ SAVE EMPLOYEE ------------------

@app.route('/save-employee', methods=['POST'])
def save_employee():

    data = request.form

    emp = Employee(
        Emp_Name=data["Emp_Name"],
        Department_Name=data["Department_Name"],
        Salary=float(data["Salary"]),
        Joining_Date=datetime.strptime(
            data["Joining_Date"], "%Y-%m-%d"
        ).date(),
        Email=data["Email"],
        Mobile_Number=data["Mobile_Number"],
        City=data["City"]
    )
    
    mobile = request.form["Mobile_No"]

    if not mobile.isdigit():
       return "Mobile Number must contain only digits"

    if len(mobile) != 10:
      return "Mobile Number must be exactly 10 digits"
    
    db.session.add(emp)
    db.session.commit()

    return redirect(url_for("dashboard"))  

# ------------------ UPDATE USER ------------------   

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):

    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    data = request.json

    user.Name = data["Name"]
    user.Email = data["Email"]
    user.Password = data["Password"]
    user.Status = data["Status"]

    db.session.commit()

    return jsonify({"message": "User Updated Successfully"})

# ------------------ DELETE USER ------------------

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User Deleted Successfully"})      

# ------------------ GET ALL USER ------------------

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()

    return jsonify([user.to_dict() for user in users]) 

# ------------------ SEARCH USER BY NAME ------------------

@app.route('/user/search', methods=['GET'])
def search_user():

    name = request.args.get("name")

    users = User.query.filter(
        User.Name.ilike(f"%{name}%")
    ).all()

    total_employees = Employee.query.count()

    active_records = Employee.query.count()

    recent_employees = Employee.query.order_by(
        Employee.Emp_ID.desc()
    ).all()

    return render_template(
    "dashboard.html",
    total_employees=total_employees,
    active_records=active_records,
    recent_employees=recent_employees,
    users=users,
    page=1,
    total_pages=1
)

# ------------------ SEARCH USER BY STATUS ------------------

@app.route('/user/filter', methods=['GET'])
def filter_user():

    status = request.args.get("status")

    users = User.query.filter_by(Status=status).all()

    total_employees = Employee.query.count()

    active_records = Employee.query.count()

    recent_employees = Employee.query.order_by(
        Employee.Emp_ID.desc()
    ).all()

    return render_template(
    "dashboard.html",
    total_employees=total_employees,
    active_records=active_records,
    recent_employees=recent_employees,
    users=users,
    page=1,
    total_pages=1
)

# ------------------ PAGINATION ------------------

@app.route('/users/page')
def user_pagination():

    page = request.args.get("page", 1, type=int)

    users = User.query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    total_employees = Employee.query.count()
    active_records = Employee.query.count()

    recent_employees = Employee.query.order_by(
        Employee.Emp_ID.desc()
    ).all()

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        active_records=active_records,
        recent_employees=recent_employees,
        users=users.items,
        page=page,
        total_pages=users.pages
    )

# ------------------ SORT BY NAME ------------------

@app.route('/users/sort/name', methods=['GET'])
def sort_name():

    users = User.query.order_by(User.Name.asc()).all()

    return jsonify([user.to_dict() for user in users])

# ------------------ SORT BY CREATED DATE ------------------

@app.route('/users/sort/date', methods=['GET'])
def sort_date():

    users = User.query.order_by(User.Created_Date.desc()).all()

    return jsonify([user.to_dict() for user in users])

# ------------------ USER LIST PAGE ------------------

@app.route('/users-list')
def users_list():
    
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"].lower() != "admin":
        return redirect(url_for("user_dashboard"))


    page = request.args.get("page", 1, type=int)

    users = User.query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "users.html",
        users=users.items,
        page=page,
        total_pages=users.pages
    )
    
# ------------------ EDIT USER PAGE ------------------

@app.route('/edit-user/<int:id>')
def edit_user_page(id):

    user = User.query.get(id)

    return render_template(
        "edit_user.html",
        user=user
    )    
    
# ------------------ ADD EMPLOYEE PAGE ------------------

@app.route("/add-employee")
def add_employee_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_role"].lower() != "admin":
        return redirect(url_for("user_dashboard"))

    return render_template("add_employee.html")    
    
# ------------------ EDIT EMPLOYEE PAGE ------------------

@app.route('/edit-employee/<int:id>')
def edit_employee_page(id):

    emp = Employee.query.get(id)

    return render_template(
        "edit_employee.html",
        emp=emp
    )    
 
# ------------------ UPDATE USER PAGE ------------------
    
@app.route('/update-user/<int:id>', methods=['POST'])
def update_user_page(id):

    user = User.query.get(id)

    user.Name = request.form["Name"]
    user.Email = request.form["Email"]
    user.Password = request.form["Password"]
    user.Status = request.form["Status"]

    db.session.commit()

    return redirect(url_for("dashboard"))    

# ------------------ DELETE USER PAGE ------------------

@app.route('/delete-user/<int:id>')
def delete_user_page(id):

    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("dashboard"))
    
# ------------------ UPDATE EMPLOYEE PAGE ------------------

@app.route('/update-employee/<int:id>', methods=['POST'])
def update_employee_page(id):

    emp = Employee.query.get(id)

    emp.Emp_Name = request.form["Emp_Name"]
    emp.Department_Name = request.form["Department_Name"]
    emp.Salary = float(request.form["Salary"])

    emp.Joining_Date = datetime.strptime(
        request.form["Joining_Date"],
        "%Y-%m-%d"
    ).date()

    emp.Email = request.form["Email"]
    emp.Mobile_Number = request.form["Mobile_Number"]
    emp.City = request.form["City"]
    
    mobile=request.form["Mobile_Number"]

    if not mobile.isdigit():
      return "Mobile Number must contain only digits"

    if len(mobile)!=10:
      return "Mobile Number must be exactly 10 digits"

    db.session.commit()

    return redirect(url_for("employees_list"))    

# ------------------ DELETE EMPLOYEE PAGE ------------------
    
@app.route('/delete-employee/<int:id>')
def delete_employee_page(id):

    emp = Employee.query.get(id)

    if emp:
        db.session.delete(emp)
        db.session.commit()

    return redirect(url_for("employees_list"))    

# ------------------ REPORTS  PAGE  ------------------   

@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("login"))

    employees = Employee.query.all()

    return render_template(
        "reports.html",
        employees=employees
    )

# ------------------ SETTINGS  PAGE  ------------------ 
@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "settings.html",
        user=user
    )   
# ------------------ Update Settings Route  ------------------ 
@app.route("/update-settings", methods=["POST"])
def update_settings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    user.Name = request.form["Name"]
    user.Email = request.form["Email"]

    if request.form["Password"]:
        user.Password = request.form["Password"]

    db.session.commit()

    return redirect(url_for("settings"))

# ------------------ Protected Route  ------------------
    
@app.route("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify(user.to_dict())    

# ------------------ JWT LOGIN API ------------------

@app.route("/api/login", methods=["POST"])
def api_login():

    data = request.json

    # Validation
    if not data:
        return jsonify({"message": "Request body is required"}), 400

    if not data.get("Email"):
        return jsonify({"message": "Email is required"}), 400

    if not data.get("Password"):
        return jsonify({"message": "Password is required"}), 400

    user = User.query.filter_by(
        Email=data["Email"],
        Password=data["Password"]
    ).first()

    if not user:
        return jsonify({"message": "Invalid Email or Password"}), 401

    access_token = create_access_token(identity=user.User_ID)
    refresh_token = create_refresh_token(identity=user.User_ID)

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.Role
    }), 200
    
# ------------------ Refresh Token API  ------------------

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    current_user = get_jwt_identity()

    new_access = create_access_token(identity=current_user)

    return jsonify({

        "access_token": new_access

    })

# ------------------ LOG OUT  ------------------

@app.route("/logout")
def logout():
    
    session.clear()
    return redirect(url_for("login"))

# ------------------ RUN APP ------------------

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
