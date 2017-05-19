import os
import boto3
from math import floor
import urllib

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

identify_key = 'Survey_Code'

def lambda_handler(event, context):
    print(event)
    response = MessagingResponse()
    numbers = []
    phase_size = 20

    welcome_message = 'Hi! Welcome to our Vize Survey about your workplace! To go back and continue an answer ' \
                      'for a question, send "<<"\n'
    questions = table_users.get_item(Key={identify_key: 'Questions'})['Item']['Questions']
    first_question = questions[0]

    twilio_send_number = '+17075959842'

    from_number = urllib.parse.unquote(event['From'])
    input_message = event['Body'].replace('+', ' ')
    input_message = input_message.split()
    print(input_message)
    command = input_message[0]

    if command.lower() == 'deploy':
        if len(input_message) > 1:

            with open('Survey-Numbers.txt', 'r') as number_file:
                survey_location = number_file.readline().strip()

                for line in number_file:
                    numbers.append(line.strip())

            phases = [[numbers[n] for n in range(i * phase_size, (i + 1) * phase_size)] for i in
                      range(int(floor(len(numbers) /
                                      phase_size)))]
            phases.append(numbers[(len(phases) * phase_size):])

            phase = int(input_message[1])

            if (phase <= len(phases)) and phase > 0:
                for number in range(len(phases[phase - 1])):
                    response.message(welcome_message+first_question, to=numbers[number], from_=twilio_send_number)

                response.message('Phase %i has been deployed' % phase)
            else:
                return str(response.message('There are not that many phases. There are a total of %i phases.'
                                            % len(phases)))

            for num in range(len(numbers)):
                table_users.put_item(Item={identify_key: numbers[num], 'Code': phase, 'Location': survey_location,
                                           'Questions': [], 'Responded': 0, 'Completed': 0, })
        else:
            response.message('Error: Missing a phase number')
    elif command.lower() == 'clear':
        if len(input_message) > 1:
            response.message('Error: Too many parameters')
        else:
            table_users.delete_item(Key={identify_key: from_number})
            response.message("Your data has been cleared")
    else:
        response.message('Error: Command not recognized')

    return str(response)
