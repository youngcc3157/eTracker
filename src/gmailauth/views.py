import httplib2
from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
from apiclient import discovery

from src import settings
from src.EmailAccount.models import GmailCredential
from src.users.models import User


def gmailauth(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    # To Do: Modify so that User can select the Email he wants to see
    # instead of getting the first verified Email object
    first_email_object = User.objects.get(
        id=request.user.id).emailaccount.first()
    storage = DjangoORMStorage(GmailCredential, 'id_id',
                               first_email_object.id if first_email_object else -1, 'credential')
    credential = storage.get()
    try:
        access_token = credential.access_token
        resp, cont = Http().request(
            "https://www.googleapis.com/auth/gmail.readonly",
            headers={'Host': 'www.googleapis.com',
                     'Authorization': access_token})
    except:
        status = False

    return render(request, 'gmailauth/index.html', {'status': status})


################################
#   GMAIL API IMPLEMENTATION   #
################################

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    settings.GMAIL_SCOPES,
    redirect_uri=settings.REDIRECT_URI,
    prompt='consent')


"""
    gmailAuthenticate: view to authorize a credential for specfic user.
        If already authroized, then preceeds as is.
"""


def gmailAuthenticate(request):

    # To Do: Modify so that User can select the Email he wants to see
    # instead of getting the first verified Email object
    first_email_object = User.objects.get(
        id=request.user.id).emailaccount.first()
    storage = DjangoORMStorage(GmailCredential, 'id_id',
                               first_email_object.id if first_email_object else -1, 'credential')
    credential = storage.get()

    # if Credential is invalid or doesn't exist, get a new one through Gmail url
    # else, preceeds as Email is authorized already
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('gmail', 'v1', http=http)
        status = True

        return render(request, 'gmailauth/index.html', {'status': status})


"""
    authReturn: view to land after authorization is done.
        If already authroized, then preceeds as is.
"""


def authReturn(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    # If received state is not valid, show bad request page
    # print("get_state is ",get_state)

    # <<<<ATTENTION>>>>
    # It sometimes causes an error for this step but it seems to work right now
    # When already loged in, it doesn't cause an error
    # But when someone start from logging in and authenticate it causes an error

    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()

    # Get the list of authorized emails for current user
    email_objects = User.objects.get(id=request.user.id).emailaccount.all()
    verified_emails = [obj.email for obj in email_objects]

    # Get email address for authorized account
    credential = FLOW.step2_exchange(request.GET.get('code'))
    http = credential.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    profile_json = service.users().getProfile(userId='me').execute()
    authorized_email_addr = profile_json['emailAddress']

    if not authorized_email_addr in verified_emails:
        # Create new EmailAccount entry and save it
        curUser = User.objects.get(id=request.user.id)
        new_email_acc = curUser.emailaccount.create(
            email=authorized_email_addr, email_type='Gmail')

        # Create new credential entry for the email and save it in CredentialsModel
        storage = DjangoORMStorage(GmailCredential, 'id_id',
                                   new_email_acc.id, 'credential')
        storage.put(credential)

        return HttpResponseRedirect("/")
    else:
        # TO DO: Add a request to the client to try different Gmail account
        return HttpResponseRedirect("/gmailauth/gmailAuthenticate")
