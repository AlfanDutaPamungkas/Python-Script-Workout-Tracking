import requests
import os
from requests.auth import HTTPBasicAuth
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
USERNAME = os.getenv("USERNAME_SHEETY")
PASSWORD = os.getenv("PASSWORD")
AUTHORIZATION = os.getenv("AUTHORIZATION_SHEETY")

basic = HTTPBasicAuth(username=USERNAME,password=PASSWORD)


today = dt.datetime.now()
format_day = today.strftime("%d/%m/%Y")
format_time = today.strftime("%H:%M:%S")

gender = input("Gender [male/female] : ")
weight = input("Weight (kg) : ")
height = input("Height (cm) : ")
age = input("Age : ")
user_exercise = input("Tell me which exercise you did : ")

user_param = {
    "query":user_exercise,
    "gender":gender,
    "weight_kg":weight,
    "height_cm":height,
    "age":age
}

headers = {
    "x-app-id":APP_ID,
    "x-app-key":APP_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url=NUTRITIONIX_ENDPOINT, json=user_param, headers=headers)
response.raise_for_status()
exercise_data = response.json()
# exercise_name = exercise_data["exercises"][0]["name"]
# exercise_duration = exercise_data["exercises"][0]["duration_min"]
# exercise_calories = exercise_data["exercises"][0]["nf_calories"]

headers_sheety ={
    'Authorization': AUTHORIZATION
}

for exercise in exercise_data["exercises"]:
    sheety_param = {
        "workout":{
            "date":format_day,
            "time":format_time,
            "exercise":exercise["name"].title(),
            "duration":exercise["duration_min"],
            "calories":exercise["nf_calories"]
        }
    }

    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_param, auth=basic, headers=headers_sheety)
    sheety_response.raise_for_status()
    print(sheety_response.text)