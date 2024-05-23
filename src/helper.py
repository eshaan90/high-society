from datetime import datetime
from dateutil.relativedelta import relativedelta

def convert_str_to_datetime(date_time_str: str, format: str='%d/%m/%Y'): 
    return datetime.strptime(date_time_str, format) 
  
def find_age_from_dob(dob: datetime):
    return  relativedelta(datetime.today(), dob)

# dob='20/03/1961'
# out=find_age_from_dob(convert_str_to_datetime(dob))
# print(out)
# print(f"years:{out.years}, months:{out.months}, days:{out.days}")