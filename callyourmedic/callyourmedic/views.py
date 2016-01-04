import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

def index(request):
	temp = get_template('index1.html')
	html = temp.render()
	return HttpResponse(html)


def test(request):
	path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'static')
	#html = "<html><head></head><body>{path} Hello world</body></html>"
	html = path
	return HttpResponse(html)