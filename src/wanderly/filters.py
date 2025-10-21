def safe_default(value):
    return value if value else ''

def safe_default_money(value):
    return f'${value:,.0f}' if value else '$0'


def formatted_date(date):
    return date if isinstance(date, str) else date.strftime("%b %d")

def formatted_title_date(date):
    return date.strftime("%b %d, %Y") if date else 'No Dates Yet'

def formatted_time(time):
    return time.strftime("%I:%M %p") if time else ''