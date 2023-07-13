from __future__ import print_function

import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    with open('docs_info.json', 'r') as file:
        doc_info = json.load(file)

    docId = doc_info['documentId']
    scope = doc_info['scope']
    creds = None
    print(docId)
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

    try:
        service = build('docs', 'v1', credentials=creds)
        document = service.documents().get(documentId=docId).execute()

        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 25
                    },
                    'text': 'onions'
                }
            }
        ]

        result = service.documents().batchUpdate(
            documentId=docId, body={'requests': requests}).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()