from django.shortcuts import render



def index(request):
    return render(request, 'pages/index.html', {'title': 'Index'})

def brand(request):
    return render(request, 'pages/brand.html', {'title': 'Brand'})

def contact(request):
    return render(request, 'pages/contact.html', {'title': 'Contact'})
