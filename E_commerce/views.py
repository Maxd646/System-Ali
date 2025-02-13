from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')

def menu(request):
    return render(request, 'menu.html')
