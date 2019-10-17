from django.urls import path 
from django.conf import settings

from . import views

urlpatterns = [ 
	path('', 
    	views.gmailauth, 
    	name ='gmailauth'), 
    path('gmailAuthenticate/', 
    	views.gmailAuthenticate, 
    	name ='gmailAuthenticate'), 
    path('oauth2callback/', 
    	views.authReturn, 
    	name = 'oauth2callback'), 
] 