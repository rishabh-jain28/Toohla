# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import html
import pandas as pd
from  furl import furl

# creating a Flask app
app = Flask(__name__)
chrome_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
options = webdriver.ChromeOptions()
options.binary_location = chrome_path
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome("C:/Users/risha/Downloads/chromedriver_win32/chromedriver.exe", chrome_options=options)
df=pd.read_csv("carbon-footprint-travel-mode.csv",sep=',')

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/car', methods = ['GET'])
def car():
    f_url=furl(request)
    car = f_url.args.get('vehical')
    origin  = f_url.args.get('origin')
    destination = f_url.args.get('destination')
    url = "https://www.google.com/maps/dir/{}/{}".format(origin.replace(" ","+"),destination.replace(" ","+"))
    browser.get(url)
    tree=html.fromstring(browser.page_source)
    car_time=tree.xpath('//span[@jstcache="198"]/text()')
    car_distance=tree.xpath('//div[@jstcache="202"]/text()')
    carbon_emmision = (df.loc[df['Entity'] == 'Light rail and tram']['GHG emissions (gCO2e/km)'])*1.60934*float(car_distance[0].split(' miles')[0])
    browser.close()
    return {"c_distance":car_distance[0],"c_time":car_time[0],"carbon_emmision":"{}".format(carbon_emmision)}

@app.route('/walk',methods=['GET'])
def walking():
    f_url=furl(request)
    origin  = f_url.args.get('origin')
    destination = f_url.args.get('destination')
    url = "https://www.google.com/maps/dir/{}/{},13z/data=!4m14!4m13!1m5!1m1!1s0x880fd2681bcde519:0x90d89a1d3411f46a!2m2!1d-87.6783043!2d41.9467483!1m5!1m1!1s0x880fd37a4ede229d:0xd8b253a60b7a3745!2m2!1d-87.6285313!2d41.8996995!3e2".format(origin.replace(" ","+"),destination.replace(" ","+"))
    browser.get(url)
    tree=html.fromstring(browser.page_source)
    walkdistance=tree.xpath('//div[@class="XdKEzd"]//div[@jstcache="360"]/text()')
    walktime=tree.xpath('//div[@class="XdKEzd"]//div[@jstcache="361"]/text()')
    return {"walk_distance":walkdistance[0],"walk_time":walktime[0]}


@app.route('/', methods = ['GET'])
def home():
   return "Hello Worldsssssasdsg"
# driver function
if __name__ == '__main__':

	app.run(debug = True)
