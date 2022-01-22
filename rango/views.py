from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy cookie, candy, cupcake!'}
    # returns rendered response to client, with the template we've set up
    # and the context dict
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return HttpResponse("Rango says here is the about page. (<a href='/rango/'>Index</a>)")
