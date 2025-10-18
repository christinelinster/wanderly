
def error_for_trips(destination, start_date, end_date):
    if any(not t for t in [destination, start_date, end_date]):
        return "You must provide trip information."

    if start_date > end_date:
        return "The return date must be after the departure date"
    
    return None