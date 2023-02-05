import mysql.connector
import logging as log
from twilio.rest import Client
from time import sleep

log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class alert_bot():
    log.info("Starting")
    def __init__(self):
        log.info("Initializing")
        cache = []
        try:
            print("Connecting to database")
            log.info("Connecting to database") 
            self.db = mysql.connector.connect(
                host="db-web9.alfahosting-server.de",
                user="up6hge6e_driver",
                password="HJScs@!16031955",
                database="up6hge6e_jom")
        except Exception as e:
            print(e)
            log.error("Could not connect to database")
            
        try:
            print("Creating Twilio client")
            log.info("Creating Twilio client")
            account_sid = "AC5d5567ee7f64c99283cd6dc5fb9c7fe0"
            auth_token = "c7c8a7bdbccd7ac05ef7b8e64d265d76"
            self.client = Client(account_sid, auth_token)
        except Exception as e:
            print(e)
            log.error("Could not create Twilio client")

    def check_db(self):
        print("Starting")
        # Query the database
        log.info("Querying database")
        print("Querying database")
        query = (
            "SELECT * FROM jo348_chro_cf_dtb_order WHERE driverrealstart BETWEEN DATE_SUB(NOW(), INTERVAL 10 MINUTE) AND DATE_ADD(driverplanstart, INTERVAL 5 MINUTE)"
        )
        # Execute the query and fetch the rows
        try:
            log.info("Executing query")
            self.cursor = self.db.cursor()
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except Exception as e:
            print(e)
            log.error("Could not execute query")

    def check_rows(rows, self):
        # Check if exists
        try:
            if rows:
                print("Rows found")
                log.info("New rows found")
                self.call_me()
        except Exception as e:
            log.error(e)
            log.error("Could not check rows")



    def call_me(self):
        log.info("Calling User")
        print("Calling User")
        try:
            call = self.client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to="+4917663385873",
                from_="+19135132511"
                )
        except Exception as e:
            print(e)
            log.error("Could not call user")

    def clear_cache(self):
        self.cache = []

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print("Closing database connection")
        log.info("Closing database connection")
    

if __name__ == "__main__":
    bot = alert_bot()
    while True:
        bot.check_db()
        sleep(600)
