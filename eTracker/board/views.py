from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from eTracker.gmail_api import Gmail


#Address: "localhost/board"
def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/') #Will be replaced to go to log-in page
	gmail = Gmail(request)
	emails = gmail.getLastNEmails(20)
	context = {'emails': emails}
	return render(request, 'board/index.html', context)

#Address: "localhost/board/words"
def words(request):
	gmail = gmail_api.Gmail()
	most_used_words = gmail.getMostUsedNWords(20)
	context = {'most_used_words': most_used_words}
	return render(request, 'board/words.html', context)