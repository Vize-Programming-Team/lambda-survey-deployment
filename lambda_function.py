import os
import boto3
from math import floor

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
    numbers = []
    phase_size = 20

    welcome_message = 'Hi! Welcome to our Vize Survey about your workplace! Would you like to respond to this ' \
                      'survey? (Yes/No)'

    twilio_send_number = '+17075959842'

    input_message = event['Body'].split()
    command = input_message[0]

    with open('Survey-Numbers.txt', 'r') as number_file:
        survey_location = number_file.readline()

        for line in number_file:
            table_users.put_item(Item={'Survey_Code': survey_location, 'Code': 1, 'Number': line.split(), 'Questions': [],
                                       'Responded': 0, 'Completed': 0, })
            numbers.append(line.strip())

    phases = [[numbers[n] for n in range(i*phase_size, (i+1)*phase_size)] for i in range(int(floor(len(numbers) /
                                                                                                   phase_size)))]
    phases.append(numbers[(len(phases)*phase_size):])

    if command.lower() == 'deploy':
        phase = int(input_message[1])
    else:
        return str(response.message('Command not recognized'))

    if (phase <= len(phases)) and phase > 0:
        for number in phases[phase-1]:
            response.message(welcome_message, to=numbers[number], from_=twilio_send_number)
    else:
        return str(response.message('There are not that many phases. There are a total of %i phases.' % len(phases)))

    return str(response)
