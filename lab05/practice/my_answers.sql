-- Write ONE query under each marker. Do not delete the markers.
-- Check with:  python check.py
-- Q1  (all columns of all students)
SELECT *
FROM students;
-- Q2  (name and year of every student)
SELECT name, year
FROM students;
-- Q3  (names of CS students)
SELECT name
FROM students
WHERE program = 'CS';
-- Q4  (name and year of students in year 3 or higher)
SELECT name, year
FROM students
WHERE year >= 3;
-- Q5  (student names, Z to A)
SELECT name
FROM students
ORDER BY name DESC;
-- Q6  (title and credits of 4-credit courses, by title)
SELECT title, credits
FROM courses
WHERE credits = 4
ORDER BY title ASC;
-- Q7
SELECT COUNT(*) AS student_count
FROM students;
-- Q8
SELECT program, COUNT(*) AS student_count
FROM students
GROUP BY program
ORDER BY program;
-- Q9
SELECT ROUND(AVG(grade), 2) AS average_grade
FROM enrollments
WHERE course_code = 'CSC10004';
-- Q10
SELECT student_id, course_code
FROM enrollments
WHERE grade IS NULL
ORDER BY student_id, course_code;
-- Q11
SELECT s.name, e.grade
FROM students AS s
JOIN enrollments AS e ON e.student_id = s.id
WHERE e.course_code = 'CSC10014' AND e.grade IS NOT NULL
ORDER BY s.name;
-- Q12
SELECT c.title, COUNT(e.student_id) AS student_count
FROM courses AS c
LEFT JOIN enrollments AS e ON e.course_code = c.code
GROUP BY c.code, c.title
ORDER BY student_count DESC, c.title;
-- Q13
SELECT s.name
FROM students AS s
WHERE EXISTS (
    SELECT 1
    FROM enrollments AS e
    WHERE e.student_id = s.id AND e.grade < 5
)
ORDER BY s.name;
-- Q14
SELECT s.name, COALESCE(SUM(c.credits), 0) AS total_credits
FROM students AS s
LEFT JOIN enrollments AS e ON e.student_id = s.id
LEFT JOIN courses AS c ON c.code = e.course_code
GROUP BY s.id, s.name
ORDER BY total_credits DESC, s.name;
-- Q15
SELECT s.name
FROM students AS s
LEFT JOIN enrollments AS e
    ON e.student_id = s.id AND e.course_code = 'CSC10014'
WHERE e.student_id IS NULL
ORDER BY s.name;