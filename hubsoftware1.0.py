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
import tkcalendar
from tktimepicker import AnalogPicker,constants

#import sv_ttk

##mainscreen 
mainscreen = Tk()
mainscreen.title("Hub App 1.0")
mainscreen.geometry("1024x600")
mainscreen.config(bg = "gray69")
mainscreen.attributes('-fullscreen', 1)
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

Hubtextfont = font.Font(family="Helvetica", size = 10, weight = "bold")

torontolat = 43.651070
torontolon = -79.347015


reminderpath = '/home/paolodimaano/Desktop/testreminder.txt'

cred = credentials.Certificate("/home/paolodimaano/Desktop/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
docs  = {}
teamaddress = {
    "Paolo2": "00:3D:E8:40:73:01",
    "Paolo": "C8:F3:19:F3:0B:B4",
    "Paolo3": "F0:03:8C:F2:0F:3C",
    "Anthony": "FC:AA:81:56:84:DD",
    "Cavin": "48:4B:AA:39:AF:C8",
    "Aisha": "FC:4E:A4:5D:2B:D0"
    }

switchurl = "http://10.0.0.69:8081/zeroconf/switch"
colorurl = "http://10.0.0.69:8081/zeroconf/dimmable"

is_on = True

def clear_frame():
   for widgets in frame.winfo_children():
      widgets.place_forget()

def get_keys_from_value(d, val):
    keys = [k for k, v in teamaddress.items() if v == val]
    if keys:
        return keys[0]
    return None
    
def bluetooth_classic_scan(timeout):
        return bluetooth.discover_devices(duration=2, flush_cache=True,lookup_names=True)

def teamview():
    clear_frame()
    employeelist = ["Aisha", "Anthony","Cavin","Paolo"]
    
    memberlist = []
    #print("Found {} devices.".format(len(nearby_devices)))
    nearby_devices = bluetooth_classic_scan(10)
    for addr, name in nearby_devices:
        for keys, value in teamaddress.items():
            
            if addr == value:
            #print("  {} - {}".format(addr, name))
                membername = get_keys_from_value(teamaddress, value)
                memberlist.append(membername)
                timestamp = datetime.now()
                data = {
                    membername: 'Present',
                    'Time': timestamp
                }
                db.collection('attendance').add(data)
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

def officecontrol():
    clear_frame()
    
    #on
    def lightson():
        lightswitchon = {
            "deviceid": "10014a2701",
            "data": {
                "switch": "on"
            }
        }
        turnon = requests.post(switchurl, json = lightswitchon,timeout = 0.5)
        print(turnon.text)

    #off
    def lightsoff():
        lightswitchoff = {
            "deviceid": "10014a2701",
            "data": {
                "switch": "off"
            }
        }
        turnoff = requests.post(switchurl, json = lightswitchoff,timeout = 0.5)
        print(turnoff.text)

    #red
    def redlight():
        redlighton = {
            "deviceid": "10014a2701",
            "data": {
                "ltype": "color",
                "color": {"br": 100, "r": 255, "g": 0, "b": 0}
            }
        }
        redlightswitch = requests.post(colorurl,json = redlighton,timeout = 0.5)
        print(redlightswitch.text)

    #blue
    def bluelight():
        bluelighton = {
            "deviceid": "10014a2701",
            "data": {
                "ltype": "color",
                "color": {"br": 100, "r": 0, "g": 0, "b": 255}
            }
        }

        bluelightswitch = requests.post(colorurl,json = bluelighton,timeout = 0.5)
        print(bluelightswitch.text)

    #purple
    def purplelight():
        purplelighton = {
            "deviceid": "10014a2701",
            "data": {
                "ltype": "color",
                "color": {"br": 100, "r": 255, "g": 0, "b": 255}
            }
        }

        purplelightswitch = requests.post(colorurl,json = purplelighton,timeout = 0.5)
        print(purplelightswitch.text)

    #white
    def whitelight():
        whitelighton = {
            "deviceid": "10014a2701",
            "data": {
                "ltype": "color",
                "color": {"br": 100, "r": 255, "g": 255, "b": 255}
            }
        }

        whitelightswitch = requests.post(colorurl,json = whitelighton,timeout = 0.5)
        print(whitelightswitch.text)

    def switch():
        global is_on
        
        # Determine is on or off
        if is_on:
            on_button.config(image = off)
            #my_label.config(text = "The Switch is Off",
            #                fg = "grey")
            is_on = False
            lightsoff()
        else:
        
            on_button.config(image = on)
            #my_label.config(text = "The Switch is On", fg = "green")
            is_on = True
            lightson()

    def setcolor():
        colorchosen = color_combobox.get()

        if colorchosen == 'White':
            whitelight()
        elif colorchosen == 'Blue':
            bluelight()
        elif colorchosen == 'Red':
            redlight()
        elif colorchosen == 'Purple':
            purplelight()
        else:
            whitelight()
        #match colorchosen:
            #case 'White' as value:
                #whitelight()
            #case 'Blue' as value:
            #    bluelight()
            #case 'Red' as value:
            #    redlight()
           # case 'Purple' as value:
             #   purplelight()
            #case value:
            #    whitelight()

    on = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/ui images/on.png")
    off = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/ui images/off.png")
    
    # Create A Button
    on_button = Button(frame, image = on, bd = 0,bg = "gray69", command = switch)
    on_button.place(x = 460, y = 140)

    Officelights = Label(frame, font = "Helvetica 20 bold", fg = "black", bg = "gray69", text = "Office Lights")
    Officelights.place(x = 425, y = 90)

    colorlabel = Label(frame, font = "Helvetica 20 bold", fg = "black", bg = "gray69", text = "Color")
    colorlabel.place(x = 470, y = 280)

    coloroption = [
        "White",
        "Blue",
        "Red",
        "Purple",
    ]
    selectcolor = StringVar()
    selectcolor.set(coloroption[0])
    color_combobox = ttk.Combobox(frame, value = coloroption)
    color_combobox.place(x = 440,y = 330)

    colorsetbutton = Button(frame, text = "Set", fg = "black", bg = "gray85", font=buttonfont, command = setcolor)
    colorsetbutton.place(x = 485, y = 380)

    #lightbulbicon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/ui images/lightbulb.png")
    #lightbulbdisplay = Label(frame,width = 100, height = 124, image = lightbulbicon)
    #lightbulbdisplay.place(x = 460, y = 140)

def calendarpage():

    clear_frame()
    date = datetime.now()
    convertedtime = StringVar()


    cal = tkcalendar.Calendar(frame, selectmode = "day", year = date.year, month = date.month, day = date.day,font = "Helvetica 20",date_pattern = 'dd/MM/yyyy')
    cal.place(x=20,y=210)

    clockdisplay = AnalogPicker(frame)
    clockdisplay.place(x = 600, y = 210)

    def grabdate():
        #datelabel.config(text=cal.get_date())
        setdate = cal.get_date()
        dateentry.insert(0, setdate)
        print(setdate)

    def grabtime(time):
        unconvertedtime = "{}:{} {}".format(*time)
        print(unconvertedtime)
        #timelabel.config(text ="{}:{} {}".format(*time))
        converttime(unconvertedtime)
        
    def converttime(time):
        inputtime = datetime.strptime(time, "%I:%M %p")
        outputtime = datetime.strftime(inputtime, "%H:%M")
        convertedtime.set(outputtime)
        print(outputtime)
        

    def addstarttime():
        grabtime(clockdisplay.time())
        starttime = convertedtime.get()
        #datelabel.config(text = starttime)
        starttimeentry.insert(0, starttime)

    def addendtime():
        grabtime(clockdisplay.time())
        endtime = convertedtime.get()
        endtimeentry.insert(0, endtime)

    def setmeeting():
        eventName = meetingtitleentry.get()
        print(eventName)
        timeStart = dateentry.get() + " " + starttimeentry.get()
        print(timeStart)
        timeEnd = dateentry.get() + " " + endtimeentry.get()
        print(timeEnd)

        data ={
            'eventName': eventName,
            'timeStart': timeStart,
            'timeEnd': timeEnd
        }
        db.collection('meetings').add(data)
        calendarpage()

    selectmeetinglabel = Label(frame, font ="Helvetica 15 bold", text="Meeting Name", bg = "gray69")
    selectmeetinglabel.place(x=20, y=90)
        
    selectdatelabel = Label(frame, font ="Helvetica 15 bold", text="Select Date", bg = "gray69")
    selectdatelabel.place(x=20, y=170)

    selecttimelabel = Label(frame, font= "Helvetica 15 bold", text = "Select Meeting time", bg = "gray69")
    selecttimelabel.place(x = 600, y=125)

    getdatebutton = Button(frame, font = "Helvetica 10 bold", text = "Set Date", command = grabdate)
    getdatebutton.place(x=445, y=175)

    #gettimebutton= Button(frame, font = "Helvetica 10 bold", text = "Get Time", command = lambda: grabtime(clockdisplay.time()))
    #gettimebutton.place(x= 900, y = 170)

    starttimeentry = Entry(frame, font = Hubtextfont, bg = "white", fg = "black")
    starttimeentry.place(x = 600, y = 170, width = 100)

    starttimebutton = Button(frame, font = "Helvetica 10 bold", text = "Set Start", command = addstarttime)
    starttimebutton.place(x=715, y = 165)

    endtimeentry = Entry(frame, font = Hubtextfont, bg = "white", fg = "black")
    endtimeentry.place(x = 805, y = 170, width = 100)

    endtimebutton = Button(frame, font = "Helvetica 10 bold", text = "Set End", command = addendtime)
    endtimebutton.place(x=920, y = 165)

    dateentry = Entry(frame, font = Hubtextfont, bg = "white", fg = "black")
    dateentry.place(x = 275, y = 180)

    meetingtitleentry = Entry(frame, font = Hubtextfont, bg = "white", fg = "black")
    meetingtitleentry.place(x = 20, y =130, width=490)

    #setmeetingtitlebutton = Button(frame, font = "Helvetica 10 bold", text = "Set Title", command = addstarttime)
    #setmeetingtitlebutton.place(x=445, y=125)

    setmeetingbutton = endtimebutton = Button(frame, font = buttonfont, text = "Set Meeting", command = setmeeting)
    setmeetingbutton.place(x = 850, y = 90)


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
            day1icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day1image}.png")
            day1img.config(image=day1icon)
            day1img.image = day1icon
            
            #day2
            day2image = json_data['daily'][1]['weather'][0]['icon']
            day2icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day2image}.png")
            day2img.config(image=day2icon)
            day2img.image = day2icon
            temp2 = json_data['daily'][1]['temp']['day']
            day2temp.config(text =f"Temp: {temp2}")

            #day3
            day3image = json_data['daily'][2]['weather'][0]['icon']
            day3icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day3image}.png")
            day3img.config(image=day3icon)
            day3img.image = day3icon
            temp3 = json_data['daily'][2]['temp']['day']
            day3temp.config(text =f"Temp: {temp3}")

            #day4
            day4image = json_data['daily'][3]['weather'][0]['icon']
            day4icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day4image}.png")
            day4img.config(image=day4icon)
            day4img.image = day4icon
            temp4 = json_data['daily'][3]['temp']['day']
            day4temp.config(text =f"Temp: {temp4}")

            #day5
            day5image = json_data['daily'][4]['weather'][0]['icon']
            day5icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day5image}.png")
            day5img.config(image=day5icon)
            day5img.image = day5icon
            temp5 = json_data['daily'][4]['temp']['day']
            day5temp.config(text =f"Temp: {temp5}")
            
            #day6
            day6image = json_data['daily'][5]['weather'][0]['icon']
            day6icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day6image}.png")
            day6img.config(image=day6icon)
            day6img.image = day6icon
            temp6 = json_data['daily'][5]['temp']['day']
            day6temp.config(text =f"Temp: {temp6}")

            #day7
            day7image = json_data['daily'][6]['weather'][0]['icon']
            day7icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day7image}.png")
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
            reminder_tabs = ttk.Treeview(frame,height = 10)


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
                reminder_tabs.place(x=500, y = 250)

        def homemeetings():
            meeting_tabs = ttk.Treeview(frame, height = 10)

            meeting_tabs['columns'] = ("Meeting Title", "Start Date", "End Date")

            meeting_tabs.column("#0", width = 0, stretch= NO)
            meeting_tabs.column("Meeting Title", width = 200)
            meeting_tabs.column("Start Date",width =130)
            meeting_tabs.column("End Date",width = 130)

            meeting_tabs.heading("Meeting Title", text = "Meeting Title")
            meeting_tabs.heading("Start Date", text = "Start Date")
            meeting_tabs.heading("End Date", text = "End Date")

            retrieveresults = db.collection('meetings').get()
                #if retrieveresults.each() is not None:
            for doc in retrieveresults:
                #docs = {}
                docs = doc.to_dict()
                #print(doc.to_dict())
                #for keys in docs:
                    #for values in docs:
                x = docs.get("eventName")
                y = docs.get("timeStart")
                z = docs.get("timeEnd")
                meeting_tabs.insert(parent = '', index = 'end', text = "",values = (x,y,z))
                meeting_tabs.place(x=20, y = 250)
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
            day1icon = ImageTk.PhotoImage(file=f"/home/paolodimaano/Desktop/weather icons/{day1image}.png")
            day1img.config(image=day1icon)
            day1img.image = day1icon

            firstday = datetime.now()
            day1.config(text = firstday.strftime("%A"))
        clear_frame()


        ##welcome to
        welcomefont = font.Font(family="Garamond", size = 25, weight = "bold")
        welcomelabel = Label(frame, text = "Welcome to the", fg = "black", bg = "gray80", font = welcomefont)
        welcomelabel.place(x=20, y=90)
        ##GK02
        gk02font = font.Font(family="Garamond", size = 40, weight = "bold")
        gk02label = Label(frame, text = "GK02 Central Hub", fg = "black", bg = "gray80", font = gk02font)
        gk02label.place(x= 20, y = 130)
        ##home button
        home_button = Button(mainscreen, text = "Home", fg = "black", bg = "gray69", bd = 0, font=buttonfont, command = homescreen)
        home_button.place(x = 20, y = 30)

        #reminder button
        reminder_button = Button(mainscreen, text = "Reminders", fg = "black", bg = "gray69", bd = 0, font=buttonfont, command=reminder)
        reminder_button.place(x = 93, y = 30)

        ##calendar button
        calendar_button = Button(mainscreen, text = "Calendar", fg = "black", bg = "gray69", bd = 0, font=buttonfont, command = calendarpage)
        #calendar_button.grid(row = 1, column = 2)
        calendar_button.place(x = 213, y = 30)

        ##weather button
        weather_button = Button(mainscreen, text = "Weather", fg = "black",bg = "gray69", bd = 0, font=buttonfont, command = weatherpage)
        #weather_button.grid(row = 1, column = 3)
        weather_button.place(x = 316, y = 30)

        ##office button
        office_button = Button(mainscreen, text = "Office Controls", fg = "black", bg = "gray69", bd = 0, font=buttonfont, command = officecontrol)
        #weather_button.grid(row = 1, column = 3)
        office_button.place(x = 414, y = 30)

        ##team button
        team_button = Button(mainscreen, text = "Team", fg = "black", bg = "gray69", bd = 0, font=buttonfont, command = teamview)
        #weather_button.grid(row = 1, column = 3)
        team_button.place(x = 577, y = 30)

        ##exit button
        exit_button = Button(mainscreen, text = "Exit", fg = "black", bg = "gray69", bd = 0, font=buttonfont, command = mainscreen.destroy)
        #weather_button.grid(row = 1, column = 3)
        exit_button.place(x = 648, y = 30)

        #Main current weather
        temp1 = Label(frame, text = "Temperature", font = Hubtextfont, fg = "black", bg = "gray69")
        temp1.place(x = 800, y = 120)
        tempans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        tempans1.place(x = 900, y = 120)

        hum1 = Label(frame, text = "Humidity", font = Hubtextfont, fg = "black", bg = "gray69")
        hum1.place(x = 800, y = 140)
        humans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        humans1.place(x = 900, y = 140)

        pres1 = Label(frame, text = "Pressure", font = Hubtextfont, fg = "black", bg = "gray69")
        pres1.place(x = 800, y = 160)
        presans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        presans1.place(x = 900, y = 160)

        winsp1 = Label(frame, text = "Wind Speed", font = Hubtextfont, fg = "black", bg = "gray69")
        winsp1.place(x = 800, y = 180)
        winspans1 = Label(frame, font = Hubtextfont, fg= "black", bg = "gray69")
        winspans1.place(x = 900, y = 180)

        desc1 = Label(frame, text = "Description", font = Hubtextfont, fg = "black", bg = "gray69")
        desc1.place(x = 800, y = 200)
        descans1 = Label(frame,font = Hubtextfont, fg= "black", bg = "gray69")
        descans1.place(x = 900, y = 200)

        #day1
        day1 = Label(frame, font = "Helvetica 15 bold", fg = "black", bg = "gray69")
        day1.place(x = 680, y = 90)
        day1img = Label(frame, width = 100, height = 100, bg = "gray69")
        day1img.place(x=670,y = 120)

        #reminder tabs
        #remindertabs['columns'] = ()
        homeweather()
        homereminder()
        homemeetings()

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

    reminder_tabs = ttk.Treeview(frame, height = 15)

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
    removereminder.place(x = 500, y = 455)


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