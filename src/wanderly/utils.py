from datetime import datetime
import re

def remove_punc_for_cost(cost):
    return cost.replace(',', '')

def error_for_trips(destination, start_date, end_date):
    if not destination:
        return "You must provide a the trip name."

    if start_date and end_date:
        if start_date > end_date:
            return "The return date must be after the departure date."
    
    return None

def error_for_create_user(name, email, password):
    if not all([name, email, password]):
        return "All fields are required."
    return None

def error_for_login(email, password):
    if not all([email, password]):
        return "Please enter your email and password."
    return None

def error_for_activity_input(date, time, activity, cost):
    errors = []
    if not activity:
        errors.append("Activity description is required.")

    if date:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            errors.append("Date must be in YYY-MM-DD format.")
    
    if time:
        if not re.match('^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)$', time.strip(), re.IGNORECASE):
            errors.append("Time must in HH:MM AM/PM format.")
    
    if cost:
        try: 
            value = float(cost)
            if value < 0: 
                errors.append("Cost must be greater than or equal to 0.")
        except ValueError:
            errors.append("Cost must be a valid number.")
    return errors

def get_first_name(trips, user_id, storage):
    if trips:
        name = trips[0]['name']
    else:
        name = storage.get_name_by_id(user_id)

    return name.split()[0]

def get_trip_heading(schedule, trip_id, storage):
    if schedule:
       row = schedule[0]
       trip = {
           'id': row['trip_id'],
           'destination': row['destination'],
           'depart_date': row['depart_date'],
           'return_date': row['return_date']
       }
    else:
        trip = storage.find_trip_by_id(trip_id)
    return trip