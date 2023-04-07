from tkinter import *
from tkinter import ttk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import *
from PIL import Image, ImageTk
import tkinter.font as font
import time
import os
import os.path
from firebase import firebase
import json
import jwt
from pyrebase import pyrebase
import bluetooth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#import sv_ttk

##mainscreen 
mainscreen = Tk()
mainscreen.title("Hub App 1.0")
mainscreen.geometry("1024x600")
mainscreen.config(bg = "gray69")
#mainscreen.attributes('-type', 'dock') #turn on when in raspberry pi
frame = Frame(mainscreen)
frame.config(bg = "gray69")
frame.place(height=600, width = 1024)
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                font = ('Helvetica', 10),
                background = "gray80",
                foreground = "black",
                fieldbackground = "silver"
                )

style.map('Treeview',
          background = [('selected','green')]
          )
torontolat = 43.651070
torontolon = -79.347015

Hubtextfont = font.Font(family="Helvetica", size = 10, weight = "bold")
reminderpath = 'C:/Users/dimaa/python codes/testreminder.txt'

cred = credentials.Certificate("C:/Users/dimaa/python codes/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
docs  = {}

def clear_frame():
   for widgets in frame.winfo_children():
      widgets.place_forget()

def teamview():
    clear_frame()
    teamaddress = {
    "Paolo2": "00:3D:E8:40:73:01",
    "Paolo": "C8:F3:19:F3:0B:B4",
    "Anthony": "FC:AA:81:56:84:DD"
    }
    employeelist = ["Aisha", "Anthony","Cavin","Paolo"]
    def get_keys_from_value(d, val):
        keys = [k for k, v in teamaddress.items() if v == val]
        if keys:
            return keys[0]
        return None
    
    def bluetooth_classic_scan():
        return bluetooth.discover_devices(duration=1, flush_cache=True,lookup_names=True)

    memberlist = []
    #print("Found {} devices.".format(len(nearby_devices)))
    nearby_devices = bluetooth_classic_scan()
    for addr, name in nearby_devices:
        for keys, value in teamaddress.items():
            
            if addr == value:
            #print("  {} - {}".format(addr, name))
                membername = get_keys_from_value(teamaddress, value)
                memberlist.append(membername)
                #print("In the office: " + membername)
                
    presentmember = Label(frame, font = "Helvetica 20 bold", fg = "black", bg = "gray69", text = "Employees in the Office:")
    presentmember.place(x = 20, y = 90)
    labels = {}
    for i in range(len(memberlist)):
        #print(i)
        labels[i] = Label(frame, font = "Helvetica 18 bold", fg = "black", bg = "gray69", text = memberlist[i])
        labels[i].place(x = 20, y = 150 + i*40)  

    allmembers = Label(frame, font = "Helvetica 20 bold", fg = "black", bg = "gray69", text = "All Employees:")
    allmembers.place(x = 650, y = 90)
    labels2 = {}
    for j in range(len(employeelist)):
        labels2[j] = Label(frame, font = "Helvetica 18 bold", fg = "black", bg = "gray69", text = employeelist[j])
        labels2[j].place(x = 650, y = 150 + j*40)  

def weatherpage():
    def getWeather():
            #city = "Toronto"

            #geolocator = Nominatim(user_agent="geoapiExercises", timeout = 3)
            #location = geolocator.geocode(city)
            #obj = TimezoneFinder()

            #result = obj.timezone_at(lng= location.longitude, lat = location.latitude)

            #weather
            api = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(torontolat) + "&lon=" + str(torontolon) +"&units=metric&exclude=hourly&appid=7b59cd754b54062a05bf03947a109eb7"
            json_data = requests.get(api).json()

            #current
            temp = json_data['current']['temp']
            humidity = json_data['current']['humidity']
            pressure = json_data['current']['pressure']
            wind = json_data['current']['wind_speed']
            description = json_data['current']['weather'][0]['description']

            tempans1.config(text = (temp, "°C"))
            humans1.config(text = (humidity, "%"))
            presans1.config(text = (pressure, "hPa"))
            winspans1.config(text = (wind, "m/s"))
            descans1.config(text = (description))

            #day1
            day1image = json_data['daily'][0]['weather'][0]['icon']
            day1icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day1image}.png")
            day1img.config(image=day1icon)
            day1img.image = day1icon
            
            #day2
            day2image = json_data['daily'][1]['weather'][0]['icon']
            day2icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day2image}.png")
            day2img.config(image=day2icon)
            day2img.image = day2icon
            temp2 = json_data['daily'][1]['temp']['day']
            day2temp.config(text =f"Temp: {temp2}")

            #day3
            day3image = json_data['daily'][2]['weather'][0]['icon']
            day3icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day3image}.png")
            day3img.config(image=day3icon)
            day3img.image = day3icon
            temp3 = json_data['daily'][2]['temp']['day']
            day3temp.config(text =f"Temp: {temp3}")

            #day4
            day4image = json_data['daily'][3]['weather'][0]['icon']
            day4icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day4image}.png")
            day4img.config(image=day4icon)
            day4img.image = day4icon
            temp4 = json_data['daily'][3]['temp']['day']
            day4temp.config(text =f"Temp: {temp4}")

            #day5
            day5image = json_data['daily'][4]['weather'][0]['icon']
            day5icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day5image}.png")
            day5img.config(image=day5icon)
            day5img.image = day5icon
            temp5 = json_data['daily'][4]['temp']['day']
            day5temp.config(text =f"Temp: {temp5}")
            
            #day6
            day6image = json_data['daily'][5]['weather'][0]['icon']
            day6icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day6image}.png")
            day6img.config(image=day6icon)
            day6img.image = day6icon
            temp6 = json_data['daily'][5]['temp']['day']
            day6temp.config(text =f"Temp: {temp6}")

            #day7
            day7image = json_data['daily'][6]['weather'][0]['icon']
            day7icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day7image}.png")
            day7img.config(image=day7icon)
            day7img.image = day7icon
            temp7 = json_data['daily'][6]['temp']['day']
            day7temp.config(text =f"Temp: {temp6}")

            #days label
            firstday = datetime.now()
            day1.config(text = firstday.strftime("%A"))

            secondday = firstday+timedelta(days = 1)
            day2.config(text = secondday.strftime("%A"))

            thirdday = firstday+timedelta(days = 2)
            day3.config(text = thirdday.strftime("%A"))

            fourthday = firstday+timedelta(days = 3)
            day4.config(text = fourthday.strftime("%A"))

            fifthday = firstday+timedelta(days = 4)
            day5.config(text = fifthday.strftime("%A"))

            sixthday = firstday+timedelta(days = 5)
            day6.config(text = sixthday.strftime("%A"))

            seventhday = firstday+timedelta(days = 6)
            day7.config(text = seventhday.strftime("%A"))

    clear_frame()

    #Main current weather
    temp1 = Label(frame, text = "Temperature", font = Hubtextfont, fg = "black", bg = "gray69")
    temp1.place(x = 150, y = 120)
    tempans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
    tempans1.place(x = 250, y = 120)

    hum1 = Label(frame, text = "Humidity", font = Hubtextfont, fg = "black", bg = "gray69")
    hum1.place(x = 150, y = 140)
    humans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
    humans1.place(x = 250, y = 140)

    pres1 = Label(frame, text = "Pressure", font = Hubtextfont, fg = "black", bg = "gray69")
    pres1.place(x = 150, y = 160)
    presans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
    presans1.place(x = 250, y = 160)

    winsp1 = Label(frame, text = "Wind Speed", font = Hubtextfont, fg = "black", bg = "gray69")
    winsp1.place(x = 150, y = 180)
    winspans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
    winspans1.place(x = 250, y = 180)

    desc1 = Label(frame, text = "Description", font = Hubtextfont, fg = "black", bg = "gray69")
    desc1.place(x = 150, y = 200)
    descans1 = Label(frame,font = Hubtextfont, fg= "black", bg = "gray69")
    descans1.place(x = 250, y = 200)

    #day1
    day1 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day1.place(x = 20, y = 90)
    day1img = Label(frame, width = 100, height = 100, bg = "gray69")
    day1img.place(x=20,y = 120)

    #day2
    day2 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day2.place(x = 20, y = 250)
    day2img = Label(frame, width = 100, height = 100, bg = "gray69")
    day2img.place(x=20,y = 280)
    day2temp = Label(frame, font = Hubtextfont, fg = "black", bg = "gray69")
    day2temp.place(x=20, y = 400)

    #day3
    day3 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day3.place(x = 170, y = 250)
    day3img = Label(frame, width = 100, height = 100, bg = "gray69")
    day3img.place(x=170,y = 280)
    day3temp = Label(frame, font = Hubtextfont, fg = "black", bg = "gray69")
    day3temp.place(x=170, y = 400)

    #day4
    day4 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day4.place(x = 320, y = 250)
    day4img = Label(frame, width = 100, height = 100, bg = "gray69")
    day4img.place(x=320,y = 280)
    day4temp = Label(frame, font = Hubtextfont, fg = "black", bg = "gray69")
    day4temp.place(x=320, y = 400)

    #day5
    day5 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day5.place(x = 470, y = 250)
    day5img = Label(frame, width = 100, height = 100, bg = "gray69")
    day5img.place(x=470,y = 280)
    day5temp = Label(frame, font = Hubtextfont, fg = "black", bg = "gray69")
    day5temp.place(x=470, y = 400)

    #day6
    day6 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day6.place(x = 620, y = 250)
    day6img = Label(frame, width = 100, height = 100, bg = "gray69")
    day6img.place(x=620,y = 280)
    day6temp = Label(frame, font = Hubtextfont, fg = "black", bg = "gray69")
    day6temp.place(x=620, y = 400)

    #day7
    day7 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
    day7.place(x = 770, y = 250)
    day7img = Label(frame, width = 100, height = 100, bg = "gray69")
    day7img.place(x=770,y = 280)
    day7temp = Label(frame, font = Hubtextfont, fg = "black", bg = "gray69")
    day7temp.place(x=770, y = 400)

    getWeather()

def homescreen():
        def homereminder():
            db = firestore.client()
            docs  = {}
            reminder_tabs = ttk.Treeview(frame)


            reminder_tabs['columns'] = ("Name", "Reminder")

            reminder_tabs.column("#0", width = 0, stretch= NO)
            reminder_tabs.column("Name", width = 80)
            reminder_tabs.column("Reminder",width = 400)

            reminder_tabs.heading("Name", text = "Name")
            reminder_tabs.heading("Reminder", text = "Reminder")

            retrieveresults = db.collection('reminders').get()
            #if retrieveresults.each() is not None:
            for doc in retrieveresults:
                #docs = {}
                docs = doc.to_dict()
                #print(doc.to_dict())
                #for keys in docs:
                    #for values in docs:
                x = docs.get("name")
                y = docs.get('reminder')
                reminder_tabs.insert(parent = '', index = 'end', text = "",values = (x,y))
                reminder_tabs.place(x=500, y = 120)

        def homeweather():
            #city = "Toronto"
            #geolocator = Nominatim(user_agent="geoapiExercises")
            #location = geolocator.geocode(city)
            #obj = TimezoneFinder()
            #result = obj.timezone_at(lng= location.longitude, lat = location.latitude)
            

            #weather
            api = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(torontolat) +"&lon=" +str(torontolon)+"&units=metric&exclude=hourly&appid=7b59cd754b54062a05bf03947a109eb7"
            json_data = requests.get(api).json()

            #current
            temp = json_data['current']['temp']
            humidity = json_data['current']['humidity']
            pressure = json_data['current']['pressure']
            wind = json_data['current']['wind_speed']
            description = json_data['current']['weather'][0]['description']

            tempans1.config(text = (temp, "°C"))
            humans1.config(text = (humidity, "%"))
            presans1.config(text = (pressure, "hPa"))
            winspans1.config(text = (wind, "m/s"))
            descans1.config(text = (description))

            #day1
            day1image = json_data['daily'][0]['weather'][0]['icon']
            day1icon = ImageTk.PhotoImage(file=f"C:/Users/dimaa/python codes/weather icons/{day1image}.png")
            day1img.config(image=day1icon)
            day1img.image = day1icon

            firstday = datetime.now()
            day1.config(text = firstday.strftime("%A"))
        clear_frame()

        ##home button
        home_button = Button(mainscreen, text = "Home", fg = "black", bg = "gray85", font=buttonfont, command = homescreen)
        home_button.place(x = 20, y = 30)

        #reminder button
        reminder_button = Button(mainscreen, text = "Reminders", fg = "black", bg = "gray85", font=buttonfont, command=reminder)
        reminder_button.place(x = 93, y = 30)

        ##calendar button
        calendar_button = Button(mainscreen, text = "Calendar", fg = "black", bg = "gray85", font=buttonfont)
        #calendar_button.grid(row = 1, column = 2)
        calendar_button.place(x = 213, y = 30)

        ##weather button
        weather_button = Button(mainscreen, text = "Weather", fg = "black", bg = "gray85", font=buttonfont, command = weatherpage)
        #weather_button.grid(row = 1, column = 3)
        weather_button.place(x = 316, y = 30)

        ##office button
        office_button = Button(mainscreen, text = "Office Controls", fg = "black", bg = "gray85", font=buttonfont)
        #weather_button.grid(row = 1, column = 3)
        office_button.place(x = 414, y = 30)

        ##team button
        team_button = Button(mainscreen, text = "Team", fg = "black", bg = "gray85", font=buttonfont, command = teamview)
        #weather_button.grid(row = 1, column = 3)
        team_button.place(x = 577, y = 30)

        #Main current weather
        temp1 = Label(frame, text = "Temperature", font = Hubtextfont, fg = "black", bg = "gray69")
        temp1.place(x = 150, y = 120)
        tempans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        tempans1.place(x = 250, y = 120)

        hum1 = Label(frame, text = "Humidity", font = Hubtextfont, fg = "black", bg = "gray69")
        hum1.place(x = 150, y = 140)
        humans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        humans1.place(x = 250, y = 140)

        pres1 = Label(frame, text = "Pressure", font = Hubtextfont, fg = "black", bg = "gray69")
        pres1.place(x = 150, y = 160)
        presans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        presans1.place(x = 250, y = 160)

        winsp1 = Label(frame, text = "Wind Speed", font = Hubtextfont, fg = "black", bg = "gray69")
        winsp1.place(x = 150, y = 180)
        winspans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        winspans1.place(x = 250, y = 180)

        desc1 = Label(frame, text = "Description", font = Hubtextfont, fg = "black", bg = "gray69")
        desc1.place(x = 150, y = 200)
        descans1 = Label(frame,font = Hubtextfont, fg= "black", bg = "gray69")
        descans1.place(x = 250, y = 200)

        #day1
        day1 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
        day1.place(x = 20, y = 90)
        day1img = Label(frame, width = 100, height = 100, bg = "gray69")
        day1img.place(x=20,y = 120)

        #reminder tabs
        #remindertabs['columns'] = ()
        homeweather()
        homereminder()

##login func
def login():
    username = "admin"
    password = "admin"
    if username_entry.get() == username and password_entry.get() == password:
        username_label.destroy()
        username_entry.destroy()
        password_label.destroy()
        password_entry.destroy()
        login_button.destroy()
        
        homescreen()
    else:
        loginfailed_label = Label(mainscreen, text = "Login Failed",font = Hubtextfont, fg = "black", bg= "gray69")
        #loginfailed_label.place(x=500,y=400)


##Clock func
def clock():
    hour = time.strftime("%I")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    am_pm = time.strftime("%p")
    day = time.strftime("%a")
    month = time.strftime("%b")
    monthday = time.strftime("%e")
    time_widget.config(text=hour + ":" + minute + ":" + second + " " + am_pm + " " + day + ", " + month + " " + monthday)
    time_widget.after(1000, clock)

time_widget = Label(mainscreen, text=" ", font = Hubtextfont, fg = "black", bg= "gray69")
time_widget.place(x = 865, y = 0)
clock()

##reminder feature
def reminder():
    db = firestore.client()
    docs  = {}
    def sendreminder():
        #reminder_file = open(reminderpath, "w")
        #reminder_file.write(recepient_combobox.get() + " " + reminder_text_textbox.get(1.0, END))
        #reminder_file.close()

        data = {
        'name':recepient_combobox.get(),
        'reminder':reminder_text_textbox.get(1.0, "end-1c")
        }
        #db.collection("Team").child("Reminders").child(recepient_combobox.get()).set(data)
        db.collection('reminders').add(data)
        reminder()

    def deletereminder():
        curItem = reminder_tabs.focus()
        details = reminder_tabs.item(curItem)
        itemname = details.get("values")[0]
        itemname2 = details.get("values")[1]
        print(itemname)
        print(itemname2)
        delete = db.collection('reminders').where('reminder', "==", itemname2).get()
        for doc in delete:
            key = doc.id
            db.collection('reminders').document(key).delete()
        reminder()

    clear_frame()

    reminder_person_label = Label(frame, text = "Recepient",font = Hubtextfont, fg = "black", bg= "gray69")
    reminder_person_label.place(x=20,y=80)
    recipientoption = [
            "Anthony",
            "Paolo",
            "Cavin",
            "Aisha",
    ]
    selectrecipient = StringVar()
    selectrecipient.set(recipientoption[0])
    recepient_combobox = ttk.Combobox(frame, value = recipientoption)
    recepient_combobox.place(x = 120,y = 80)

    reminder_text_label = Label(frame, text = "Message",font = Hubtextfont, fg = "black", bg= "gray69")
    reminder_text_label.place(x = 20, y = 120)
    reminder_text_textbox = Text(frame, font = Hubtextfont, width = 50, height = 5)
    reminder_text_textbox.place(x = 120, y = 120)

    reminder_text_button = Button(frame, text = "Send", fg = "black", bg = "gray85", font=buttonfont, command = sendreminder)
    reminder_text_button.place(x = 120, y = 210)

    reminder_tabs = ttk.Treeview(frame)

    reminder_tabs['columns'] = ("Name", "Reminder")

    reminder_tabs.column("#0", width = 0, stretch= NO)
    reminder_tabs.column("Name", width = 80)
    reminder_tabs.column("Reminder",width = 400)

    reminder_tabs.heading("Name", text = "Name")
    reminder_tabs.heading("Reminder", text = "Reminder")

    retrieveresults = db.collection('reminders').get()
    #if retrieveresults.each() is not None:
    for doc in retrieveresults:
        #docs = {}
        docs = doc.to_dict()
        #print(doc.to_dict())
        #for keys in docs:
            #for values in docs:
        x = docs.get("name")
        y = docs.get('reminder')
        reminder_tabs.insert(parent = '', index = 'end', text = "",values = (x,y))
        reminder_tabs.place(x=500, y = 120)

    removereminder = Button(frame, text = "Remove Selected", fg = "black", bg = "gray85", font=buttonfont,command= deletereminder)
    removereminder.place(x = 500, y = 355)


Hubapp = Label(mainscreen, text = "Hub App 1.0", font = Hubtextfont, bg = "gray69")
Hubapp.place(x = 0, y = 0)

##buttons func
buttonfont = font.Font(family="Helvetica", size = 15, weight = "bold")

##username field
username_label = Label(mainscreen, text = "Username",font = Hubtextfont, fg = "black", bg= "gray69")
username_entry = Entry(mainscreen)
username_label.place(x = 400, y =250)
username_entry.place(x = 500, y = 250)

##password field
password_label = Label(mainscreen, text = "Password",font = Hubtextfont, fg = "black", bg= "gray69")
password_entry = Entry(mainscreen)
password_label.place(x = 400, y = 300)
password_entry.place(x = 500, y = 300)

##login button
login_button = Button(mainscreen, text = "Login", fg = "black", bg = "gray85", font=buttonfont, command = login)
login_button.place(x = 500, y = 350)

#sv_ttk.set_theme("dark")
mainscreen.mainloop()