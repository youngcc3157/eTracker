from __future__ import print_function
import os.path
import httplib2
import base64
from oauth2client    import file, client, tools
from apiclient       import discovery
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from eTracker.gmailauth.models import CredentialsModel

from eTracker.email_object import Email
from django.conf import settings
import argparse

class Gmail:
    """
        Gmail class plays the connector role between eTracker and Gmail API
    """
    def __init__(self, request):
        self.request = request
        self.APPLICATION_NAME = 'eTracker'
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)
        self.msgs = self.service.users().messages()

    def getCredentials(self):
        """
            Gets valid user credentials from storage.
    
            If nothing has been stored, or if stored credentials are invalid,
            the OAuth2 flow is completed to obtain the new credentials.

            Returns:
                Credentials, the obtained credential.
        """
        storage = DjangoORMStorage(CredentialsModel, 'id', 
                                    self.request.user, 'credential')
        credentials = storage.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON, 
                    settings.GMAIL_SCOPES)
            flow.user_agent = self.APPLICATION_NAME

            #Setting up flags
            #argparser = argparse.ArgumentParser(parents=[tools.argparser])
            #flags = argparser.parse_args()

            credentials = tools.run_flow(flow, storage, flags)
            
        return credentials


    def getLastNEmails(self, N):
        """
            returns a list of N Email objects
        """

        # <<<<<ATTENTION>>>>>
        # This line should be modified so that it only collects important(label)
        # and received emails
        response = self.msgs.list(userId='me', maxResults=N).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        emails = {}
        for message in messages:
            email = self.createEmailObject(message['id'])
            emails[message['id']] = email

        return emails

    def createEmailObject(self, message_id):
        """
            creates and returns an Email object given message_id
        """
        msg = self.msgs.get(userId='me', id=message_id).execute()
        payld = msg['payload']

        #Get body paragraph
        paragraph = ""
        if 'parts' in payld:
            mssg_parts = payld['parts'] 
            part_one  = mssg_parts[0] 
            part_body = part_one['body'] 
            if 'data' in part_body:
                part_data = part_body['data']
                #Decoding from Base64 to UTF-8 (human readable texts)
                cleaned_base64 = part_data.replace("-","+") 
                cleaned_base64 = cleaned_base64.replace("_","/")
                paragraph = base64.b64decode(cleaned_base64.encode('utf-8'))
                paragraph = paragraph.decode("utf-8")
        
        #Get subject and email sender
        subject = ""
        sender_email = ""
        if 'headers' in payld:
            msg_headers = payld['headers']
            for i in range(len(msg_headers)):
                if subject and sender_email:
                    break
                if msg_headers[i]['name'] == "Subject":
                    subject = msg_headers[i]['value']
                if msg_headers[i]['name'] == "From":
                    sender_email = msg_headers[i]['value']

        #Get label ids
        label_id = ""
        if 'labelIds' in msg:
            label_id = msg['labelIds']

        email = Email(message_id, msg['threadId'], label_id,
                    msg['historyId'], subject, sender_email, paragraph)
        return email


"""

    def getBodyParagraph(self, message_id):
        msg = self.msgs.get(userId='me', id=message_id).execute()
        payld = msg['payload']

        paragraph = ""
        if 'parts' in payld:
            mssg_parts = payld['parts'] # fetching the message parts
            part_one  = mssg_parts[0] # fetching first element of the part 
            part_body = part_one['body'] # fetching body of the message
            if 'data' in part_body:
                part_data = part_body['data'] # fetching data from the body
                cleaned_base64 = part_data.replace("-","+") # decoding from Base64 to UTF-8
                cleaned_base64 = cleaned_base64.replace("_","/") # decoding from Base64 to UTF-8
                paragraph = base64.b64decode(str(cleaned_base64).encode('utf-8')) # decoding from Base64 to UTF-8
        return paragraph

    def getTitle(self, message_id):
        msg = self.msgs.get(userId='me', id=message_id).execute()
        payld = msg['payload']

        title = ''
        if 'headers' in payld:
            mssg_headers = payld['headers'] # fetching the message parts
            part_one  = mssg_headers[-4] # fetching first element of the part 
            title = part_one['value'] # fetching body of the message
        return title

    def getMostRecentNEmailSamples(self, N):
        #Get last N messages (Only messageId and threadId are returned in 'messages')
        response = self.msgs.list(userId='me', maxResults=N).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        id_to_body = {}
        for message in messages:
            para = self.getBodyParagraph(message['id'])
            id_to_body[message['id']] = para[:100] #Only show first 100 chars
        return id_to_body

    def getMostUsedNWords(self, topN):
        #Get last 10 messages (Only messageId and threadId are returned in 'messages')
        response = self.msgs.list(userId='me', maxResults=10).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        #Save unique words
        unique_words = {}

        for message in messages:
            para = self.getBodyParagraph(message['id'])

            #Split a paragraph into words and find frequency of each word
            words = para.split()
            for word in words:
                if len(word) > 1:
                    if word not in unique_words:
                        unique_words[word] = 0
                    unique_words[word] += 1

        #Sort the unique words by occurance and return top N
        return sorted(unique_words.items(), key=lambda x: x[1], reverse = True)[:topN]"""
