from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = "employee"

    Emp_ID = db.Column(db.Integer, primary_key=True)
    Emp_Name = db.Column(db.String(100), nullable=False)
    Department_Name = db.Column(db.String(100), nullable=False)
    Salary = db.Column(db.Float, nullable=False)
    Joining_Date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "Emp_ID": self.Emp_ID,
            "Emp_Name": self.Emp_Name,
            "Department_Name": self.Department_Name,
            "Salary": self.Salary,
            "Joining_Date": str(self.Joining_Date)
        }