import httplib2

from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .models import CredentialsModel
from eTracker import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
from httplib2 import Http

#Address: "localhost/auth"
def home(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin')

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
        print('Not Found')

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

def gmailAuthenticate(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', 
    							request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('gmail', 'v1', http=http)
        #print('access_token = ', credential.access_token)
        status = True

        return render(request, 'gmailauth/index.html', {'status': status})


def authReturn(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    #If received state is not valid, show bad request page
    #print("get_state is ",get_state)

    #<<<<ATTENTION>>>>
    #It sometimes causes an error for this step but it seems to work right now
    #When already loged in, it doesn't cause an error
    #But when someone start from logging in and authenticate it causes an error
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', 
    							request.user, 'credential')
    storage.put(credential)
    #print("access_token: %s" % credential.access_token)
    return HttpResponseRedirect("/")