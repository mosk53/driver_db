import mysql.connector
import logging as log
from twilio.rest import Client
from time import sleep

log.basicConfig(filename='log.log', level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

frist_run = True

class alert_bot():
    log.info("Starting")
    def __init__(self):
        log.info("Initializing")
        try:
            print("Connecting to database")
            log.info("Connecting to database") 
            self.db = mysql.connector.connect(
                host="db-web9.alfahosting-server.de",
                user="up6hge6e_driver",
                password="xxxx",
                database="xxxx")
        except Exception as e:
            print(e)
            log.error("Could not connect to database")
            
        try:
            print("Creating Twilio client")
            log.info("Creating Twilio client")
            account_sid = "xxxxx"
            auth_token = "xxxxx"
            self.client = Client(account_sid, auth_token)
        except Exception as e:
            log.error(e)
            log.error("Could not create Twilio client")

        self.cache = self.get_all_uniq_id()

    def check_db(self):
        print("Starting")
        # Query the database
        log.info("Querying database")
        print("Querying database")
        query = ("SELECT uniq_id FROM jo348_chro_cf_dtb_order WHERE driverrealstart > driverplanstart + INTERVAL 5 MINUTE;")
        # Execute the query and fetch the rows
        try:
            log.info("Executing query")
            self.cursor = self.db.cursor()
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.check_row(rows)
        except Exception as e:
            log.error(e)
            log.error("Could not execute query")

    def check_row(self, rows):
        log.info("Checking rows")
        print("Checking rows")
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
                print("New row found")
                log.info("New row found")
                self.call_me()
            else:
                log.info("Rows already in cache")
                print("Rows already in cache")
                log.info("Not calling user")
                print("Not calling user")

        except Exception as e:
            log.error(e)
            log.error("Could not check rows")

    def call_me(self):
        global frist_run
        if first_run:
            log.info("Cache does not exist")
            print("Cache does not exist")
            log.info("Not calling user")
            print("Not calling user")
            first_run = False
        else:
            try:
                print("Calling user")
                log.info("Calling user")
                call = self.client.calls.create(
                    url="http://demo.twilio.com/docs/voice.xml",
                    to="+xxxx",
                    from_="+xx"
                    )
            except Exception as e:
                log.error(e)
                log.error("Could not call user")
            

    def get_all_uniq_id(self):
        log.info("Getting all uniq_id")
        print("Getting all uniq_id")
        query = (
            "SELECT uniq_id FROM jo348_chro_cf_dtb_order"
        )
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(query)
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
    bot = alert_bot()
    while True:
        bot.check_db()
        sleep(600)
