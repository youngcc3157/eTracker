from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from src.gmail_api import Gmail


#Address: "localhost/board"
def index(request):
    if not request.user.is_authenticated:
        # Will be replaced to go to log-in page
        return HttpResponseRedirect('/')
    gmail = Gmail(request)
    emails = gmail.getLastNEmails(20)
    context = {'emails': emails}
    return render(request, 'board/index.html', context)


#Address: "localhost/board/words"
"""
	Not functional for now  
"""


def words(request):
    gmail = Gmail(request)
    most_used_words = gmail.getMostUsedNWords(20)
    context = {'most_used_words': most_used_words}
    return render(request, 'board/words.html', context)
