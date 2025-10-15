
def error_for_trips(start_date, end_date):
    if start_date > end_date:
        return "The return date must be after the departure date"
    return None