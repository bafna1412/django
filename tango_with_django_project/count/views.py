# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    context = RequestContext(request)
    dict = {'message': 'Displays IP of live users and their count'}

    return render_to_response('count/index.html', dict, context)
