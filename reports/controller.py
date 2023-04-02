from core.db.db import connect_db


def get_visitor_statistics():

    conn = connect_db()

    with conn.cursor() as cur:
        # Fetching the data from the survey_responses table
        cur.execute("SELECT visit_purpose, visitor_status, first_time FROM survey_responses;")
        results = cur.fetchall()

        # Creating dictionaries to store the results
        visit_purpose = {"Admission": 0, "Events": 0, "Others": 0}
        visitor_status = {"Student": 0, "Parent": 0, "Other College Student": 0}
        first_time = {"Yes": 0, "No": 0}

        # Calculating the totals for each category
        for result in results:
            if result[0] == "admission":
                visit_purpose["Admission"] += 1
            elif result[0] == "events":
                visit_purpose["Events"] += 1
            else:
                visit_purpose["Others"] += 1

            if result[1] == "student":
                visitor_status["Student"] += 1
            elif result[1] == "Parent":
                visitor_status["parent"] += 1
            else:
                visitor_status["Other College Student"] += 1

            if result[2] == True:
                first_time["Yes"] += 1
            else:
                first_time["No"] += 1

        # Creating a dictionary to store the final results
        final_results = {"visit_purpose": visit_purpose, "visitor_status": visitor_status, "first_time": first_time}

        cur.close()
        conn.close()

    return final_results

