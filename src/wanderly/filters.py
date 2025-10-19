def safe_default(value):
    return value if value else ''

def formatted_date(date):
    return date if isinstance(date, str) else date.strftime("%b %d")

def formatted_title_date(date):
    return date.strftime("%b %d, %Y")

def formatted_time(time):
    return time.strftime("%I:%M %p") if time else ''