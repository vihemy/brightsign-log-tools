from datetime import date


def get_date():
    today = date.today()
    today = today.strftime("%d-%m-%Y")  # converts to danish date-format
    return today
