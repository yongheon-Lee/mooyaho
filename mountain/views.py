from django.shortcuts import render
from .models import Mountain
from django.contrib.auth.decorators import login_required
import requests

def home(request):
    #AI서버와 통신
    URL="http://127.0.0.1:5000/userviewlog"
    payload={'userid': request.user.id}

    res=requests.post(URL,data=payload)  #post형식으로 data를 url에 넣어 요청후 응답받음
    res=res.json() #응답 json으로 바꾸기
    print(res)

    return render(request, 'mountain/main.html')


# @login_required()
def mountains(request):
    # user = request.user.is_authenticated
    all_mountain = Mountain.objects.all()
    return render(request, 'mountain/all_mountain.html', {'mountains': all_mountain})


def mountains_detail(request, id):
    my_mountain = Mountain.objects.get(id=id)
    return render(request, 'mountain/mountains_detail.html', {'mountain_info': my_mountain})
