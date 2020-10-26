from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def faq(request):
    return render(request, 'home/faq.html')


def terms(request):
    return render(request, 'home/terms.html')


def privacy(request):
    return render(request, 'home/privacy.html')
