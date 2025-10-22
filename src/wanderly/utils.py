
def error_for_trips(destination, start_date, end_date):
    if not destination:
        return "You must provide trip information."

    if start_date and end_date:
        if start_date > end_date:
            return "The return date must be after the departure date"
    
    return None

def error_for_create_user(name, email, password):
    if any(not t for t in [name, email, password]):
        return "The fields are required."
    return None

def error_for_activity_title(text):
    if not text:
        return "You must provide an activity."
    return None


def clean_cost_input(cost):
    return cost.replace(',', '')