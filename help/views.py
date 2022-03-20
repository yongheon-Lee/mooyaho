from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'help/help.html')


def notice(request):
    return render(request, 'help/notice.html')


def review(request):
    return render(request, 'help/review.html')
