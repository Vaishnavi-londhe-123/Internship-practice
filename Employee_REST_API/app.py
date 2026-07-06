from flask import Flask, request, jsonify
from models import db, Employee
from datetime import datetime
import config

app = Flask(__name__)

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

        emp = Employee(
            Emp_Name=data["Emp_Name"],
            Department_Name=data["Department_Name"],
            Salary=float(data["Salary"]),
            Joining_Date=datetime.strptime(
                data["Joining_Date"], "%Y-%m-%d"
            ).date()
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

        emp.Emp_Name = data["Emp_Name"]
        emp.Department_Name = data["Department_Name"]
        emp.Salary = float(data["Salary"])
        emp.Joining_Date = datetime.strptime(
            data["Joining_Date"], "%Y-%m-%d"
        ).date()

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


# ------------------ RUN APP ------------------

if __name__ == "__main__":
    app.run(debug=True)