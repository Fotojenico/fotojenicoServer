from django.shortcuts import render, redirect


def index(request):
    return render(request, 'home/index.html')


def contact(request):
    return redirect('https://forms.gle/tkNCJcRuzMb2vWLL9')


def about(request):
    return render(request, 'home/about.html')


def faq(request):
    return render(request, 'home/faq.html')


def terms(request):
    return render(request, 'home/terms.html')


def privacy(request):
    return render(request, 'home/privacy.html')
