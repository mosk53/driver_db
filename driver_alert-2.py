import mysql.connector
import logging as log
import logging.handlers as handlers
from twilio.rest import Client
from time import sleep
import smtplib
from pythonping import ping
import pickle
from einst import *


# configure logging
log.basicConfig(
    level=log.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    handlers=[
        handlers.RotatingFileHandler("log.log", maxBytes=1000000000, backupCount=5)
    ],
)


class alert_bot:
    def __init__(self):
        log.info("Initializing")
        try:
            log.info("Connecting to database")
            self.db = mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database=db_name
            )
        except Exception as e:
            log.error(e)
            log.error("Could not connect to database")
            self.send_email("Error", "Could not connect to database")
            try:
                log.info(ping("db-web9.alfahosting-server.de", verbose=True))
            except Exception as e:
                log.error(e)
                log.error("Datenbank offline")
                self.send_email("Error", e)
        try:
            log.info("Creating Twilio client")
            self.client = Client(tw_account_sid, tw_auth_token)
        except Exception as e:
            log.error(e)
            log.error("Could not create Twilio client")
            self.send_email("Error", e)

    def check_db(self):
        query = "SELECT * FROM jo348_alarm WHERE Alarmzeit < NOW() AND abfrage = 0;"
        try:
            log.info("Executing query")
            self.cursor = self.db.cursor()
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.check_row(rows)
        except Exception as e:
            log.error(e)
            log.error("Could not execute query")
            self.send_email("Error", e)

    def check_row(self, rows):
        log.info("Checking if rows exist")
        if rows:
            log.info("Rows found")
            self.call_me()
            self.send_email("Successful", "Rows found, calling user")
        else:
            log.info("No rows found")

    def call_me(self):
        try:
            log.info("Calling user")
            call = self.client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to="+4917663385873",
                from_="+19135132511",
            )
        except Exception as e:
            log.error(e)
            log.error("Could not call user")
            self.send_email("Error", e)

    def send_email(self, subject, message):
        try:
            server = smtplib.SMTP("smtp-mail.outlook.com", 587)
            server.ehlo()
            server.starttls()
            server.login(e_sender_email, e_password)
            server.sendmail(
                e_sender_email, e_receiver_email, f"Subject: {subject}\n\n{message}"
            )
            server.quit()
            log.INFO("Email sent")
        except Exception as e:
            log.INFO(e)
            log.INFO("Could not send email")

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
            log.info("Closing database connection")
        except Exception as e:
            log.error(e)
            log.error("Could not close database connection")
            self.send_email("Error", e)


if __name__ == "__main__":
    while True:
        bot = alert_bot()
        bot.check_db()
        del bot
        sleep(375)
