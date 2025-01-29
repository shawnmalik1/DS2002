-- SQL Exercises (With Answers)

-- 1. Retrieve all students who enrolled in 2023.
SELECT * FROM students WHERE YEAR(EnrollmentDate) = 2023;

-- 2. Find students whose email contains 'gmail.com'.
SELECT * FROM students WHERE Email LIKE "%gmail.com%";


-- 3. Count how many students are enrolled in the database.
SELECT COUNT(*) AS TotalStudents FROM Students;

-- 4. Find students born between 2000 and 2005.
SELECT * FROM Students WHERE DateOfBirth BETWEEN '2000-01-01' AND '2005-12-31';

-- 5. List students sorted by last name in descending order.
SELECT * FROM Students ORDER BY LastName DESC;

-- 6. Find the names of students and the courses they are enrolled in.
SELECT CONCAT(Students.FirstName, ' ', Students.LastName) AS StudentName, Courses.CourseName

FROM Students
JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
JOIN Courses ON Enrollments.CourseID = Courses.CourseID;

-- 7. List all students and their courses, ensuring students without courses are included (LEFT JOIN).
SELECT CONCAT(Students.FirstName, ' ', Students.LastName) AS StudentName, Courses.CourseName

FROM Students
LEFT JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
LEFT JOIN Courses ON Enrollments.CourseID = Courses.CourseID;


-- 8. Find all courses with no students enrolled (LEFT JOIN).
SELECT Courses.CourseName
FROM Courses
LEFT JOIN Enrollments ON Courses.CourseID = Enrollments.CourseID
WHERE Enrollments.StudentID IS NULL;


-- 10. List courses and show the number of students enrolled in each course.
SELECT Courses.CourseName, COUNT(Enrollments.StudentID) AS StudentCount
FROM Courses
LEFT JOIN Enrollments ON Courses.CourseID = Enrollments.CourseID
GROUP BY Courses.CourseID, Courses.CourseName;



