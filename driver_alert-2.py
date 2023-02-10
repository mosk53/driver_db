import mysql.connector
import logging as log
from twilio.rest import Client
from time import sleep
import smtplib
from pythonping import ping
import pickle
from einst import *


log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


first_run = True

class alert_bot():
    log.info("Starting")

    def __init__(self):
        log.info("Initializing")
        self.query = "SELECT * FROM jo348_alarm WHERE Alarmzeit < NOW() AND abfrage = 0;"
        try:
            log.info("Connecting to database") 
            self.db = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name)
        except Exception as e:
            log.error(e)
            log.error("Could not connect to database")
            try:
                log.info(ping('db-web9.alfahosting-server.de', verbose=True))
            except Exception as e:
                log.error(e)
                log.error("Datenbank offline")
        try:
            log.info("Creating Twilio client")
            self.client = Client(tw_account_sid, tw_auth_token)
        except Exception as e:
            log.error(e)
            log.error("Could not create Twilio client")
        self.cache = self.get_all_uniq_id()

        
    def check_db(self):
        try:
            log.info("Executing query")
            self.cursor = self.db.cursor()
            self.cursor.execute(self.query)
            rows = self.cursor.fetchall()
            self.check_row(rows)
        except Exception as e:
            log.error(e)
            log.error("Could not execute query")

    def check_row(self, rows):
        log.info("Checking rows")
        found = False
        try:
            for row in rows:
                uniq_id = row[0]
                if uniq_id not in self.cache:
                    self.cache.append(uniq_id)
                    found = True
                else:
                    continue
            if found:
                log.info("New row found")
                self.call_me()
                self.send_email(e_message_done)
            else:
                log.info("Rows already in cache")
                log.info("Not calling user")

        except Exception as e:
            log.error(e)
            log.error("Could not check rows")

    def call_me(self):
        try:
            print("Calling user")
            log.info("Calling user")
            call = self.client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to="+4917663385873",
                from_="+19135132511"
                )
        except Exception as e:
            log.error(e)
            log.error("Could not call user")

    def send_email(self, msg):
        try:
            print("Sending email")
            log.info("Sending email")
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(e_sender_email, e_password)
            server.sendmail(e_sender_email, e_receiver_email, msg)
            server.quit()
            log.info("Email sent")
            print("Email sent")
        except Exception as e:
            log.error(e)
            log.error("Could not send email")

    def get_all_uniq_id(self):
        log.info("Getting all uniq_id")
        print("Getting all uniq_id")        
        # check if cache exists and load it
        try:
            with open('cache.pickle', 'rb') as handle:
                self.cache = pickle.load(handle)
                log.info("Cache loaded")
                print("Cache loaded")
                return self.cache
        except Exception as e:
            log.error(e)
            log.error("Could not load cache")
            try:
                log.info("Executing init query")
                self.cursor = self.db.cursor()
                self.cursor.execute(self.query)
                cache = self.cursor.fetchall()
                return cache
            except Exception as e:
                print(e)
                log.error("Could not get all uniq_id")

        

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print("Closing database connection")
        log.info("Closing database connection")


if __name__ == "__main__":
    while True:
        bot = alert_bot()
        bot.check_db()
        # Save cache
        try:
            with open('cache.pickle', 'wb') as handle:
                pickle.dump(bot.cache, handle, protocol=pickle.HIGHEST_PROTOCOL)
                log.info("Cache saved")
                print("Cache saved")
        except Exception as e:
            log.error(e)
            log.error("Could not save cache")
        del bot
        sleep(120)
