from ast import arg
import re
import os
import logging
import requests
import argparse

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

'''
SLACK BOT
'''
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from prettytable import PrettyTable


app = App()

'''
*** Simple Text Parser for Slackbot ***
Note: 
1. Support single condition (e.g with user_profile can find by either fname or lname or email)
2. It will require a table name to match the message (get -t <name> or get --table <name>)
   Other argrument will be depends on the table
'''
class SlackMessageParseError(Exception):
    pass

class SlackMessageParser(argparse.ArgumentParser):
    '''
    Custom error handling. Since originally argsparse will exit only
    '''
    def error(self, message):
        raise SlackMessageParseError(message)


parser = SlackMessageParser()
parser.add_argument('-t', '--table',
                    choices=["user_profile", "country"], 
                    type=str,
                    required=True)  # Table name
'''
Table: user_profile supporting arguments
1. --fname: First name
2. --lname: Last name
3. --email: User email
'''
parser.add_argument('--fname', type=str)
parser.add_argument('--lname', type=str)
parser.add_argument('--email', type=str)

'''
Table: country supporting arguments
1. --code: Country code
2. --name: Country name
'''
parser.add_argument('--code', type=str)
parser.add_argument('--name', type=str)


@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.message(re.compile("(get([\s]+(-t|--table)[\s]+[-\w\s\d]+))"))
def reply_to(say, context):
    try:
        args = parser.parse_args(context.matches[1].strip().split())

        '''
        Step 0: Build payload based on the give table
        ''' 
        payload = dict()       
        if args.table == "user_profile":
            if args.fname:
                payload["fname"] = f"eq.{args.fname}"
            elif args.lname:
                payload["lname"] = f"eq.{args.lname}"
            elif args.email:
                payload["email"] = f"eq.{args.email}" 
        elif args.table == "country":
            if args.code:
                payload["code"] = f"eq.{args.code}"
            elif args.name:
                payload["name"] = f"eq.{args.name}"

        '''
        Step 1: Send request to PostgREST and get a response
        '''
        r = requests.get(
            f"{os.getenv('POSTGREST_API_ENDPOINT')}/{args.table}", 
            params=payload
        )
        result = r.json()
        
        '''
        Step 2: Prepare a pretty table to display
        '''
        ptable = PrettyTable()
        ptable.align = "l"
        
        # If there is nothing then display "no data"
        if len(result) == 0:
            ptable.field_names = ["Result"]
            ptable.add_row(["No data"]) 
        
        # If there is data then add row to table 
        for idx, item in enumerate(result):
            if idx == 0:
                ptable.field_names = item.keys()
            ptable.add_row(item.values())

        # Finally print the table on Slack
        say(f"```{ptable.get_string()}```")
    except SlackMessageParseError as e0:
        say(f"Error: {e0}")
    except Exception as e:
        say("Something went wrong :(")
        raise e
    
'''
END SLACK BOT
'''

'''
FLASk APP
'''
from flask import Flask, request, jsonify

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

'''
END FLASK APP
'''

if __name__ == "__main__":
    flask_app.run(port=os.getenv("APP_PORT"))
