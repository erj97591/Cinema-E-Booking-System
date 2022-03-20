from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index (response):
	return HttpResponse("<b>Hmm I can get this to work but when I copy and paste the html code from the github it thrwos 18 million erros man my spelling sucks</b>")