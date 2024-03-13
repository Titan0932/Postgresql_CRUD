import datetime
import time
import psycopg2
from config import load_config

"""
  Display a menu for user selection and return an input.
"""
def menu():
  print("\n================ Menu ================")
  print(" Enter 1: View all the student records")
  print(" Enter 2: Add a new student Record")
  print(" Enter 3: Update Student Email")
  print(" Enter 4: Delete student")
  print(" Enter 5 or other number: Exit Program")
  print("=============== ---- ================")
  return getInput()


"""
Receive input from the user.
"""
def getInput():
  option = -1
  while(1):  
    try:
      option = input('Enter your option: ')
      break
    except Exception as e:
      print("Error: Try again!")
  return option


"""
  Prompts the user to enter an email address and handles exceptions
  if any occur.
  :return: The email entered by the user.
"""
def inputStudentEmail():
  email = ""
  while(1):
    try:
      email = input("Enter email: ")
      break
    except Exception as e:
      print("Error: Enter again!")
      continue
  return email
    

"""
  Prompts the user to enter a student ID, validates the input to ensure it is an integer, and returns the ID.
  :return: The student ID entered by the user.
"""
def inputStudentID():
  id = ""
  while(1):
    try:
      id = int(input("Enter id: "))
      break
    except Exception as e:
      print("Error: Enter again!")
      continue
  return id


"""
  Prompts the user to enter a first name, handling exceptions if any
  occur.
  :return: The first name of a student that is entered
  by the user.
"""
def inputStudentFname():
  firstName = ""
  while(1):
    try:
      firstName = input("Enter firstName: ")
      break
    except Exception as e:
      print("Error: Enter again!")
      continue
  return firstName

"""
  Prompts the user to enter a last name, handling exceptions if any
  occur.
  :return: The last name of a student that is entered
  by the user.
"""
def inputStudentLname():
  lname = ""
  while(1):
    try:
      lname = input("Enter lname: ")
      break
    except Exception as e:
      print("Error: Enter again!")
      continue
  return lname



"""
  Prompts the user to input a date and handles any exceptions
  that may occur.
  :return: Returning a `datetime.date` object representing the date entered by the user after validating the input for day, month, and year.
"""
def inputStudentEnrollment():
  day = -1
  year = -1
  month = -1
  date = ""
  while(1):
    try:
      day = input("Enter day (1 - 31): ")
      month = input("Enter month (1 - 12): ")
      year = input("Enter year: ")
      date = datetime.date(int(year), int(month), int(day))
      break
    except Exception as e:
      print(e)
      print("Error: Enter again!")
      continue
  return date



"""
  Retrieves all student records from a database connection and prints them out.
  
  :param conn: A connection object that represents a connection to a database. 
"""
def getAllStudents(conn):
  print("Getting all student records")
  cur = conn.cursor()
  sqlQuery = "Select * from public.students"
  cur.execute(sqlQuery)
  result = cur.fetchall()
  for row in result:
    print(row)



"""
  Add a new student record to the database.

  :param email: The email address of the student.
  :param fName: The first name of the student.
  :param lName: The last name of the student.
  :param enrollment: The enrollment date of the student.
  :param conn: A connection object representing a connection to the database.
"""
def addStudent(email, fName, lName, enrollment, conn):
  print("Adding student")
  sqlQuery = "INSERT INTO Students(email, first_name, last_name, enrollment_date) VALUES (%s, %s, %s, %s)"
  cur= conn.cursor()
  cur.execute(sqlQuery, (email, fName, lName, enrollment))
  conn.commit()


"""
  Update the email address of a student in the database.

  :param student_id: The ID of the student whose email address is to be updated.
  :param new_email: The new email address to be assigned to the student.
  :param conn: A connection object representing a connection to the database.
"""
def updateStudentEmail(student_id, new_email, conn): 
  print("Updating student email")
  sqlQuery = "UPDATE students SET email = %s where student_id = %s"
  cur= conn.cursor()
  cur.execute(sqlQuery, (new_email, student_id))
  conn.commit()
  if cur.rowcount > 0:
    print("Student email updated successfully.")
  else:
    print("No student found with the specified ID.")


"""
  Delete a student record from the database.

  :param student_id: The ID of the student to be deleted.
  :param conn: A connection object representing a connection to the database.
"""
def deleteStudent(student_id, conn):
  print("Deleting Student")
  sqlQuery = "DELETE FROM students where student_id = %s"
  cur= conn.cursor()
  cur.execute(sqlQuery, (student_id,))
  conn.commit()
  if cur.rowcount > 0:
    print("Student Record deleted successfully.")
  else:
    print("No student found with the specified ID.")


"""
  Establishes a connection to a PostgreSQL database server using the provided configuration parameters.

  :param config: A dictionary containing the configuration details required to connect to a PostgreSQL database server. 
  :return: Either a connection to the PostgreSQL server if the  connection is successful, or -1 if there is an error during the connection attempt.
"""
def connect(config):
    """ Connecting to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return -1


def initDB():
  config = load_config()
  conn = connect(config)
  return conn


def main():
  print("Starting Program")
  conn = initDB()
  if(conn == -1):
    print("ERROR: Failed to connect to db. Exiting....")
    return
  while(True):
    choice = menu()
    if(choice == "1"):
      getAllStudents(conn)
    elif(choice == "2"):
      print("Enter Student Records:")
      addStudent(inputStudentEmail(), inputStudentFname(), inputStudentLname(), inputStudentEnrollment(), conn)
      
    elif(choice == "3"):
      print("Enter Student to find and email to replace.")
      updateStudentEmail(inputStudentID(), inputStudentEmail(), conn)
    elif(choice == "4"):
      print("Enter Student ID to delete.")
      deleteStudent(inputStudentID(), conn)
    else:
      print("Exiting!!")
      break
    time.sleep(1)
  conn.close()


if __name__ == "__main__":
  main()