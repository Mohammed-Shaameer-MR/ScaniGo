#clean console viewing
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  #Hide all except crash and fatals

#hide depreciation warnings
import tensorflow as tf
tf.get_logger().setLevel("ERROR")

#Function to fix up the query for now 
def query_fixer(query):
    q = query.lower()
    additions = []

    # direction hints
    if "college" in q:
        if "to college" in q or "going to college" in q:
            additions.append("TripType: HomeToCollege")

    if "home" in q and "college" in q:
        if "to home" in q or "from college" in q or "return" in q or "back" in q:
            additions.append("TripType: CollegeToHome")

    # implicit home arrival = exit
    if "reach home" in q or "reached home" in q or "arrive home" in q:
        additions.append("Action: Exit")
        additions.append("TripType: CollegeToHome")

    # action hints
    if "board" in q or "boarding" in q:
        additions.append("Action: Board")
    if "exit" in q or "drop" in q:
        additions.append("Action: Exit")

    # student hint
    if "hemal" in q:
        additions.append("StudentName: Hemal Ramm S")
    elif "karthick" in q:
        additions.append("StudentName: Karthick S")

    if additions:
        return query + " | " + " | ".join(additions)

    return query


