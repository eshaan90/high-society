from datetime import datetime
from dateutil.relativedelta import relativedelta
import cv2
import matplotlib.pyplot as plt
import numpy as np

def convert_str_to_datetime(date_time_str: str, format: str='%d/%m/%Y'): 
    return datetime.strptime(date_time_str, format) 
  
def find_age_from_dob(dob: datetime):
    return  relativedelta(datetime.today(), dob)


def show_image(figure:int,figure_name:str,img:np.ndarray):
    """
    Displays the passed img in the figure window
    Args:
        figure: Window number
        figure_name: Window name
        img: Image
    """
    plt.figure(figure)
    cv2.imshow(figure_name, img)


# dob='20/03/1961'
# out=find_age_from_dob(convert_str_to_datetime(dob))
# print(out)
# print(f"years:{out.years}, months:{out.months}, days:{out.days}")