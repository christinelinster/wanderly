def safe_default(value):
    return value if value else ''

def safe_default_money(value):
    return f'{value:,.0f}' if value else '0'

def formatted_date_activity(date):
    return date.strftime("%b %d / %y") if date else ''

def formatted_date(date):
    return date.strftime("%b %d, %Y") if date else 'No Dates'

def formatted_time(time):
    return time.strftime("%I:%M %p") if time else ''