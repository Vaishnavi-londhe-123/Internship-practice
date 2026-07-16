create database empmgt;
use empmgt;
-- CREATE DEPARTMENT TABLE --

CREATE TABLE Department
(
    Department_Name VARCHAR(50) PRIMARY KEY
);

INSERT INTO Department VALUES
('HR'),
('IT'),
('Finance'),
('Sales'),
('Marketing');

-- CREATE EMPLOYEE TABLE --
CREATE TABLE Employee
(
    Emp_ID INT PRIMARY KEY,
    Emp_Name VARCHAR(50),
    Department_Name VARCHAR(50),
    Salary DECIMAL(10,2),
    Joining_Date DATE,
    FOREIGN KEY (Department_Name) REFERENCES Department(Department_Name)
);

-- INSERT EMPLOYEE RECORDS --
INSERT INTO Employee VALUES
(1,'Amit','HR',35000,'2025-01-15'),
(2,'Priya','IT',45000,'2024-12-20'),
(3,'Rahul','Finance',55000,'2024-10-18'),
(4,'Sneha','IT',65000,'2025-03-05'),
(5,'Rohan','Sales',40000,'2025-02-10'),
(6,'Neha','Marketing',48000,'2024-11-25'),
(7,'Karan','HR',37000,'2025-04-12'),
(8,'Pooja','Sales',52000,'2025-05-08'),
(9,'Akash','Finance',70000,'2024-09-01'),
(10,'Meena','Marketing',60000,'2025-06-15'),
(11,'Riya','HR',42000,'2025-03-12'),
(12,'Riya','HR',42000,'2025-03-12');

-- DISPLAY TABLES --
SELECT * FROM Department;

SELECT * FROM Employee;

-- TOP 5 HIGHEST SALARY --
SELECT *
FROM Employee
ORDER BY Salary DESC
LIMIT 5;

-- DEPARTMENT WISE EMPLOYEE COUNT --
SELECT Department_Name,
COUNT(*) AS Employee_Count
FROM Employee
GROUP BY Department_Name;

-- SECOND HIGHEST SALARY --
SELECT MAX(Salary) AS Second_Highest_Salary
FROM Employee
WHERE Salary <
(
SELECT MAX(Salary)
FROM Employee
);

-- EMPLOYEES WHOSE SALARY > DEPARTMENT AVERAGE SALARY --
SELECT *
FROM Employee e
WHERE Salary >
(
SELECT AVG(Salary)
FROM Employee
WHERE Department_Name=e.Department_Name
);

-- INNER JOIN --
SELECT
e.Emp_ID,
e.Emp_Name,
d.Department_Name,
e.Salary
FROM Employee e
INNER JOIN Department d
ON e.Department_Name=d.Department_Name;

-- LEFT JOIN --
SELECT
e.Emp_ID,
e.Emp_Name,
d.Department_Name,
e.Salary
FROM Employee e
LEFT JOIN Department d
ON e.Department_Name=d.Department_Name;

-- GROUP BY WITH HAVING --
SELECT Department_Name,
COUNT(*) AS Employee_Count
FROM Employee
GROUP BY Department_Name
HAVING COUNT(*)>1;

-- EMPLOYEES HIRED IN LAST 6 MONTHS --
SELECT *
FROM Employee
WHERE Joining_Date>=DATE_SUB(CURDATE(),INTERVAL 6 MONTH);

-- FIND DUPLICATE RECORDSm --
SELECT
Emp_Name,
Department_Name,
Salary,
Joining_Date,
COUNT(*) AS Duplicate_Count
FROM Employee
GROUP BY
Emp_Name,
Department_Name,
Salary,
Joining_Date
HAVING COUNT(*)>1;

-- REMOVE DUPLICATE RECORDS --
DELETE e1
FROM Employee e1
JOIN Employee e2
ON e1.Emp_Name=e2.Emp_Name
AND e1.Department_Name=e2.Department_Name
AND e1.Salary=e2.Salary
AND e1.Joining_Date=e2.Joining_Date
AND e1.Emp_ID>e2.Emp_ID;

-- WINDOW FUNCTION --
SELECT
Emp_ID,
Emp_Name,
Department_Name,
Salary,
RANK() OVER(ORDER BY Salary DESC) AS Salary_Rank
FROM Employee;

-- VIEW --
CREATE VIEW Employee_Details AS
SELECT
Emp_ID,
Emp_Name,
Department_Name,
Salary
FROM Employee;

SELECT * FROM Employee_Details;

-- TRIGGER --
CREATE TABLE Employee_Log
(
Log_ID INT AUTO_INCREMENT PRIMARY KEY,
Emp_ID INT,
Message VARCHAR(100)
);

DELIMITER $$

CREATE TRIGGER Employee_Insert
AFTER INSERT
ON Employee
FOR EACH ROW
BEGIN
INSERT INTO Employee_Log(Emp_ID,Message)
VALUES(NEW.Emp_ID,'New Employee Added');
END$$

DELIMITER ;

INSERT INTO Employee VALUES
(13,'Kunal','IT',55000,'2025-06-10');

SELECT * FROM Employee_Log;

-- CASE WHEN --
SELECT
Emp_ID,
Emp_Name,
Salary,
CASE
WHEN Salary>=60000 THEN 'High Salary'
WHEN Salary>=45000 THEN 'Medium Salary'
ELSE 'Low Salary'
END AS Salary_Status
FROM Employee;

Alter table employee
Modify Emp_id int not null auto_increment;

-- Search,Filter & Pagination --
Use empmgt;
Alter table employee
Add Email varchar(50),
Add City varchar(50);
Update employee
SET
Email='aaru01@gmail.com',
City='Satara'
Where Emp_ID=1;
Update employee
SET
Email='ruhi02@gmail.com',
City='Kolhapur'
Where Emp_ID=2;
Update employee
SET
Email='kedar03@gmail.com',
City='Pune'
Where Emp_ID=3;
Update employee
SET
Email='aasha04@gmail.com',
City='Mumbai'
Where Emp_ID=4;
Update employee
SET
Email='viraj05@gmail.com',
City='Sangli'
Where Emp_ID=5;
Update employee
SET
Email='vrunda06@gmail.com',
City='Satara'
Where Emp_ID=6;
Update Employee
SET Email = 'sonu@gmail.com'
Where Emp_Name = "Sonu";
Update Employee
SET Email = 'priya@gmail.com'
Where Emp_Name = "Priya";
Update Employee
SET Email = 'rahul@gmail.com'
Where Emp_Name = "Rahul";
Update Employee
SET Email = 'sneha@gmail.com'
Where Emp_Name = "Sneha";
Update Employee
SET Email = 'rohan@gmail.com'
Where Emp_Name = "Rohan";
Update Employee
SET Email = 'neha@gmail.com'
Where Emp_Name = "Neha";

CREATE TABLE users (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL
);

