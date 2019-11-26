from src.EmailAccount.models import EmailAccount
import httplib2

from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .models import CredentialsModel
from src import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
from httplib2 import Http

from src.users.models import User

#Address: "localhost/auth"


def gmailauth(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    storage = DjangoORMStorage(CredentialsModel, 'id',
                               request.user, 'credential')
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
    storage = DjangoORMStorage(CredentialsModel, 'id',
                               request.user, 'credential')
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
    #print("get_state is ",get_state)

    # <<<<ATTENTION>>>>
    # It sometimes causes an error for this step but it seems to work right now
    # When already loged in, it doesn't cause an error
    # But when someone start from logging in and authenticate it causes an error

    # Create new EmailAccount entry for this specific Gmail account
    curUser = User.objects.get(id=request.user.id)
    curUser.emailaccount.create(email_type='Gmail')

    # Create new credential entry for the user and save it in CredentialsModel
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id',
                               request.user, 'credential')
    storage.put(credential)

    return HttpResponseRedirect("/")
