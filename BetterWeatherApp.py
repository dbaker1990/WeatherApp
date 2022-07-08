#This is for the app design
from distutils.command.config import config
from msilib.schema import Icon
from re import search
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from configparser import ConfigParser
import pip._vendor.requests
from pip._vendor import requests

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # Get a Tuple with (City, Country, temp_celsius, temp_fahrenheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        description = json["weather"][0]['description']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather, description)
        return final
    else:
        return None

def search():
    city = city_entry.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        img2 = PhotoImage('{}.png'.format(weather[4]))
        image_lbl.config(image=img2)
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]
        description_lbl['text'] = weather[6]
        print(image_lbl)
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))
        
#Under this will be the design of the app
app =Tk()
#title of app
app.title("Weather App")
#window size of app
app.geometry('640x480')

#creates the textbox for the city entry
city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

#Creates the button for the app
search_btn = Button(app, text='Search Weather', width=12, command=search)
search_btn.pack()

#create label for the location name
location_lbl = Label(app, text='', font=('bold', 20))
location_lbl.pack()

#image for weather condition
test = ImageTk.PhotoImage(Image.open("50n.png"))
image_lbl = Label(app, image=test)
image_lbl.pack()

#label for temperature
temp_lbl = Label(app, text='')
temp_lbl.pack()

#label for weather
weather_lbl = Label(app, text="")
weather_lbl.pack()

#label for description
description_lbl = Label(app, text='')
description_lbl.pack()

app.mainloop()