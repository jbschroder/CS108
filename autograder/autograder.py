import csv
import unittest, sys, os, importlib
from io import StringIO
import pandas as pd

def grade_homework(TestClass, csv_filename, test_names, test_points, test_feedbacks):
    ## Copy Roster to Initial Homework0 Grade CSV File

    # When reading from CSV, two things to pay attention to.
    #  - The first column has no header, so we have to tell pandas that this is the index column
    #  - Force student ID to be a string for printing to file.  The ID is really an integer,
    #    but the ID integers are too big to fit into a regular int with max value of 32K.
    #    By default, pandas will treat the ID as a string
    df = pd.read_csv(csv_filename, index_col=[0], dtype={"ID": str})


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
                tests = [TestClass('test_load', filename), TestClass('test_output', filename)]
                test_points = [50, 50]
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
        if "Homework 0" in header:
            col_name = header
            break

    # store grades in df
    for i in range(len(hw_scores)):
        df.at[i+1, col_name] = hw_scores[i]

    # save updated grades to csv file
    df.to_csv(csv_filename)

    # write separate feedback file
    df = pd.DataFrame(data={'Name' : names[1:], 'Score' : hw_scores, 'Feedback' : hw_feedback})
    df.to_csv("feedback.csv")
