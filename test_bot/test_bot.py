#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import smtplib
import datetime
from os import listdir
from email.mime.text import MIMEText
from selenium.webdriver.chrome.options import Options
from decimal import Decimal
import twilio
from twilio.rest import Client

chromeOptions = Options()
chromeOptions.headless = False

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = #add port information for email server 
SMTP_USERNAME = #add personal email here, for example "email0"
SMTP_PASSWORD = #add smtp email password here

EMAIL_TO = #add email address you want to sent to here, for example ["email1", "email2"]
EMAIL_FROM = #add email address sending from here, for example "email0@gmail.com"
EMAIL_SUBJECT = "In Stock Ammo"

DATE_FORMAT = "%d/%m/%Y"
EMAIL_SPACE = ", "

PATH = "/usr/local/bin/chromedriver 9"

#Twilio Account Informationchromedriver 7
account_sid = #add Twilio account ID here
auth_token = #add Twilio authorization token here
client = Client(account_sid, auth_token)

driver = webdriver.Chrome(executable_path=PATH, options=chromeOptions)
folder = #add folder where webdriver is located [listdir("/Users/")]

def searchforammo():
	
	driver.get("https://www.targetsportsusa.com")

	search = driver.find_element_by_id("header-search-input")
	search.clear()
	#search.send_keys("22 long rifle 40 grain ammo")
	#search.send_keys("30-06 ammo")
	search.send_keys("ammo")
	search.send_keys(Keys.RETURN)

	try:
		#Click on Add to Cart for first option shown
		main = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//body/form/main/div/table/tbody/tr/td/table[3]/tbody/tr/td/ul/li[1]/a/button"))
			)
	
		driver.execute_script("arguments[0].click();", main);

		#Click on Select Box
		main = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "product-select-1"))
			)
	
		driver.execute_script("arguments[0].click();", main);

		#Click on Second Option in Drop Down
		url = driver.current_url
		main = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//main/div/div/div/div[3]/div[2]/div/select/option[2]"))
			)

		driver.execute_script("arguments[0].click();", main);


		#Click on Add to Cart Button on site
		main = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.XPATH, "//body/form/main/div/div/div/div[3]/div[2]/vinv/div/div[2]/div/span[3]/input"))
		#EC.presence_of_element_located((By.XPATH, "//body/form/header/div/div[2]/ul/li/a"))
			)
		driver.execute_script("arguments[0].click();", main);


		time.sleep(1)
		#Click on cart icon
		main = WebDriverWait(driver, 10).until(
		#EC.presence_of_element_located((By.XPATH, "//body/form/header/div[2]/ul/li[2]/a"))
		EC.presence_of_element_located((By.XPATH, "//body/form/header/div/div[2]/ul/li[2]/a"))
			)
		driver.execute_script("arguments[0].click();", main);

		# #Get the price
		cost = WebDriverWait(driver, 10).until(
		 	EC.presence_of_element_located((By.XPATH, "//main/div/div/div[5]/div/div/div[2]/div/div/div[2]/div/span"))
		 	)
		 
		cost = Decimal(cost.text.strip('$'))
		#print(cost)

		if int(cost) <= 40:
	
			#Click on Checkout
			main = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//main/div/div/div[4]/div[2]/input[2]"))
				)
			driver.execute_script("arguments[0].click();", main);
			time.sleep(1)

			main = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//main/div/div/div/table/tbody/tr/td/div/div/div[2]/input"))
				)
			driver.execute_script("arguments[0].click();", main);
			main.send_keys("lilo2k19@gmail.com")

			main = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//main/div/div/div/table/tbody/tr/td/div/div/div[3]/input"))
				)
			driver.execute_script("arguments[0].click();", main);
			main.send_keys("callierules!")
			main.send_keys(Keys.RETURN)

			time.sleep(1)
		
			contact_in_cart(url)
		else:
			contact_exceeded_budget(url)

	except:
		driver.quit()
		log("Out of Stock")

def contact_in_cart(url):
	DATA = url
	emailaddy = #add email0 here 
	port_number = 1025
	msg = MIMEText(DATA)
	msg['From'] = emailaddy
	msg['To'] = emailaddy
	msg['Subject'] = 'Ammo In Cart'
	mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	mail.starttls()
	mail.login(SMTP_USERNAME, SMTP_PASSWORD)
	mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
	mail.quit()

	message_text = 'In Stock Ammo In Cart' + ' ' + DATA

	message = client.messages \
                	.create(
                     	body=message_text,
                     	from_= #add from phone number here, in the format ['+5555555555'],
                     	to= #add from phone number here, in the format ['+5555555555']
                 )

	message = client.messages \
                	.create(
                     	body=message_text,
                     	from_= #add from phone number here, in the format ['+5555555555'],
                     	to= #add from phone number here, in the format ['+5555555555']
                 )


	x = open("kill.txt", "x")
	x.close()
	log("In Stock")

def contact_exceeded_budget(url):
	DATA = url
	emailaddy = #add email0 here 
	port_number = 1025
	msg = MIMEText(DATA)
	msg['From'] = emailaddy
	msg['To'] = emailaddy
	msg['Subject'] = 'Ammo Available but Need Additional Money'
	mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	mail.starttls()
	mail.login(SMTP_USERNAME, SMTP_PASSWORD)
	mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
	mail.quit()
	
	message_text = 'In Stock Ammo Exceeds Budget' + ' ' + DATA

	message = client.messages \
                	.create(
                     	body=message_text,
                     	from_=#add from phone number here, in the format ['+5555555555'],
                     	to= #add from phone number here, in the format ['+5555555555']
                 )

	message = client.messages \
                	.create(
                     	body=message_text,
                     	from_=#add from phone number here, in the format ['+5555555555'],
                     	to= #add from phone number here, in the format ['+5555555555']
                 )
           	

	log("In Stock Exceeds Available Funds")

def log(result):
    now = datetime.datetime.now()
    time = now.strftime("%X")
    date = now.strftime("%x")
    f = open("log.txt", "a")
    f.write(f"{result} {date} {time} \n")
    f.close()

for file in folder:
	if "kill.txt" in file:
		log("abort")
		
	else:
		searchforammo()

driver.quit()
