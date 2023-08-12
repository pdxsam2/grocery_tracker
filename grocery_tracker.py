from __future__ import print_function

import os.path
import json
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def getCredentials(docId, scope):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def main():
    with open('documentInfo.json', 'r') as file:
        documentInfo = json.load(file)
    scope = documentInfo['scope']
    docId = documentInfo['documentId']
    creds = getCredentials(docId, scope)
    groceryTable = open('groceryTable.txt', 'r').read().split()
    maxGroceryIndex = len(groceryTable) - 1
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 39
                },
                'text': ''
            }
        }
    ]


    try:
        service = build('docs', 'v1', credentials=creds)
        document = service.documents().get(documentId=docId).execute()

        while 1:
            print('enter your index:')
            groceryIndex = int(input())
            groceryIndex -= 1

            if groceryIndex > maxGroceryIndex:
                print("grocery index out of bounds")
                continue
            
            groceryItem = groceryTable[groceryIndex]
            requests[0]['insertText']['text'] = groceryItem + '\n'
            service.documents().batchUpdate(
                documentId=docId, 
                body={'requests': requests}
            ).execute()

    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()