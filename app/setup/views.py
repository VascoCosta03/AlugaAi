from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def dasboard(request):
    return render(request, 'dasboard.html')
