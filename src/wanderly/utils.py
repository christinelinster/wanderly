from datetime import datetime
import re

def check_date_range(date, trip):
    if date:
        format_string = '%Y-%m-%d'
        date = datetime.strptime(date, format_string).date()
        print(date)
        print(trip['depart_date'])
        print(trip['return_date'])
        print(trip['depart_date'] > date)
        if trip['depart_date'] > date or date > trip['return_date']:
            return "The activity date is outside of trip dates!"
    return None


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

def plans_by_date(all_plans):
    plans_by_date = {}
    for activity in all_plans:
        date = activity['at_date'] or ""
        if date not in plans_by_date:
            plans_by_date[date] = []
        plans_by_date[date].append(activity)
    return plans_by_date

def plans_per_page(itinerary, page, days_per_page):
    start = (page - 1) * days_per_page
    end = start + days_per_page
    valid_days = list(itinerary.keys())[start:end]
    page_days = {date:itinerary[date] for date in valid_days}
    return page_days

def error_for_page(page, pages):
    temp_page = page
    if temp_page > pages:
        temp_page = pages
    elif temp_page < 1:
        temp_page = 1

    if temp_page != page:
        return {'message': 'Page not found. Redirected.', 'page': temp_page}
    return None

def total_pages(total_items, items_per_page):
    pages = ((total_items + items_per_page - 1) // items_per_page) or 1
    return pages

def remove_punc_for_cost(cost):
    return cost.replace(',', '')
