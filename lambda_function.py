import os
import boto3

from boto3.session import Session
from twilio.twiml.messaging_response import MessagingResponse

# Add DynamoDB session
session = Session()

# Add Twilio credentials
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']

# Add DynamoDB
dynamodb = boto3.resource('dynamodb','us-west-2')
table_users = dynamodb.Table('User_Data')

def lambda_handler(event, context):
    response = MessagingResponse()
    welcome_message = 'Hi! Welcome to our Vize Survey about your workplace! Would you like to respond to this ' \
                      'survey? (Yes/No)'

    twilio_send_number = 'send number'

    with open('Survey-Numbers.txt', 'r') as number_file:
        survey_location = number_file.readline()
        for line in number_file:
            table_users.put_item(Item={'Survey_Code': survey_location, 'Code': 1, 'Number': line.split(), 'Questions': [],
                                       'Responded': 0, 'Completed': 0, })
            response.message(welcome_message, to=line.split(), from_=twilio_send_number)

    return str(response)
