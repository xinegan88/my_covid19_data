# my_covid_data.py
# the draft final program that combines all the data (maps,tables,charts)

from datetime import datetime
import us_charts
from us_charts import state_data,usa_data,county_data

def error_one(user_choice):
        print("\nInput not recognized.\n")
        print("To generate data for your state, type [1]\nTo generate United States data, type [2]\nTo exit, type [3]\n\n")
        user_choice = input()
        options(user_choice)

def options(user_choice):
    while user_choice not in ["1","2","3"]:
        error_one(user_choice)

    if user_choice == "1":
        print("\nNow entering state-mode...\n")
        state_name = input("Enter a state: ")
        state_data(state_name)
        county_data(state_name)

    elif user_choice == "2":
        print("\nNow entering USA-mode...\n")
        usa_data()

    elif user_choice == "3":
        print("\nThank you for using \"My COVID-19 Data.\" Have a nice day.")
        exit()

def run_date():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    print("Today is: " + dt_string,"\n")

def greet_user(user):
    print("Hi ",user,"\nWelcome to \"My COVID-19 Data\"\n")
    run_date()
    print("To generate data for your state, type [1]]\nTo generate United States data, type [2]\nTo exit, type [3]\n")
    user_choice = input()
    options(user_choice)
    while user_choice not in ["1","2","3"]:
        error_one(user_choice)

user = input("Please enter your name: \n")
greet_user(user)
