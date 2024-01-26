import csv
import unittest, sys, os, importlib
from io import StringIO
import pandas as pd

def grade_homework(TestClass, hw_number, test_names, test_points, test_feedbacks):
    '''
    TestClass: 
        Class like hw0/hw0_grader.py, which defines the tests for the homework

    hw_number:
        integer, like 0, 1, 2, 3... indicating which homework this is

    test_names, test_points, test_feedbacks
        Lists that define the tests that you want to run form TestClass 
        
        test_names[k] : names of kth test to run (run test with name TestClass.test_names[k])
        test_points[k] : how many points kth test is worth
        test_feedbacks[k] : string of feedback to give if test fails


    Output: Writes grades and feedback to hw#_grades.csv and hw#_feedback.csv

    '''

    csv_filename = 'hw'+str(hw_number)+'_grades.csv'

    if len(test_names) != len(test_points) != len(test_feedbacks):
        raise ValueError("test_* lists need to be the same length!")


    # When reading from CSV, we need to force student ID to be a string for
    # printing to file.  The ID is really an integer, but the ID integers are
    # too big to fit into a regular int with max value of 32K.  By default,
    # pandas will treat the ID as a string
    df = pd.read_csv(csv_filename, dtype={"ID": str})


    hw_scores = list()
    hw_feedback = list()


    ## Step through each student in roster file
    names = df.loc[:, "Student"]
    for name in names[1:]:
        name_str = ""
        for letter in name:
            if letter.isalpha():
                name_str += letter
        name_str = name_str.lower()

        # Run Tests on filename that contains name_str and .py
        found_file = False
        for file in os.listdir("."):
            if file.startswith(name_str) and file.endswith(".py"):
                found_file = True

                # Disable standard error so student errors don't print during grading
                backup = sys.stderr
                sys.stderr = StringIO()

                filename = file[0:-3]
                #tests = [TestClass('test_load', filename), TestClass('test_output', filename)]
                tests = [ TestClass(name, filename) for name in test_names ]
                suite = unittest.TestSuite()
                suite.addTests(tests)
                results = unittest.TextTestRunner().run(suite)

    
                # Reset stderr
                out = sys.stderr.getvalue() # release output
                sys.stderr.close()  # close the stream 
                sys.stderr = backup # restore original stderr

                # Display Test Results
                score = 100
                feedback = ""
                if not results.wasSuccessful():
                    #import pdb; pdb.set_trace()
                    feedback += "Tests that failed:"
                    for error in results.failures:
                        score -= test_points[tests.index(error[0])]
                        feedback += test_feedbacks[tests.index(error[0])] + ";" 
                else:
                    feedback += "Passed All Tests"
                hw_scores.append(score)
                hw_feedback.append(feedback)
                 
                break

        if not found_file:
            hw_scores.append(0)
            hw_feedback.append("No .py file found")

    col_name = ""
    for header in list(df):
        column_name = "Homework " + str(hw_number)
        if column_name in header:
            col_name = header
            break

    # store grades in df
    for i in range(len(hw_scores)):
        df.at[i+1, col_name] = hw_scores[i]

    # save updated grades to csv file, note Canvas does not want the index column
    df.to_csv(csv_filename, index=False)

    # write separate feedback file
    df = pd.DataFrame(data={'Name' : names[1:], 'Score' : hw_scores, 'Feedback' : hw_feedback})
    df.to_csv("feedback.csv")
