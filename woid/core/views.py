from django.shortcuts import render

def home(request):
	return render(request, 'core/home.html')

def icons(request):
	return render(request, 'core/icons.html')