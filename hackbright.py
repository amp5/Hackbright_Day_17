"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github) 

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github) 

        elif command == "project_title":
            title = args[0]
            project_title(title)

        elif command == "student_grade":
            student_github, project_title = args
            student_grade(student_github, project_title)

        elif command == "assign_grade":
            grade, student_github, project_title = args
            assign_grade(grade, student_github, project_title)

def assign_grade(grade, student_github, project_title):

    QUERY = """
            INSERT INTO Grades (grade, student_github, project_title) VALUES (?, ?, ?)
            """

    db_cursor.execute(QUERY, (grade, student_github, project_title))
    db_connection.commit()

    print "You have added the grade of %s ." % (grade)


def student_grade(student_github,project_title):
    QUERY = """
            SELECT grade FROM Grades WHERE student_github = ? AND project_title = ?
            """
    db_cursor.execute(QUERY, (student_github, project_title))
    results = db_cursor.fetchone()
    print results
    print "This is %s's grade." %(student_github)


def project_title(title):

    QUERY = """
            SELECT * FROM Projects WHERE title = ?
            """

    db_cursor.execute(QUERY, (title,))

    results = db_cursor.fetchall()

    print results

    print "These are the project details for %s" % (title)    


#def get_student_by_github():

def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
            INSERT INTO Students     
            VALUES (?, ?, ?)
            """
    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
