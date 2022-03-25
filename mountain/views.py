from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from .models import Mountain
from django.contrib.auth.decorators import login_required
import urllib.request
import json
from config.my_settings import MY_NAVER_SEARCH

@login_required(login_url='/login/')
def home(request):
    # #AI서버와 통신
    # URL="http://127.0.0.1:5000/userviewlog"
    # payload={'userid': request.user.id}
    #
    # res=requests.post(URL,data=payload)  #post형식으로 data를 url에 넣어 요청후 응답받음
    # res=res.json() #응답 json으로 바꾸기
    # print(res)
    #
    # return render(request, 'mountain/main.html')
    user = request.user
    # 유저가 로그인했을때
    if user.is_authenticated :
        # 만약 지역 정보가 0.0일떄,
        if user.longitude == 0.0 and user.latitude == 0.0 :
            return render(request, 'mountain/main.html', {'noinform': '추천해줄 산이 없습니다.'})
        else :
            user_x = user.longitude
            user_y = user.latitude
            user_max_x = user_x + 0.3
            user_max_y = user_y + 0.3
            user_min_x = user_x - 0.3
            user_min_y = user_y - 0.3
            local_mountain = Mountain.objects.filter(maxx__lt = user_max_x,
                                                     maxx__gt = user_min_x,
                                                     maxy__lt = user_max_y,
                                                     maxy__gt = user_min_y)
            return render(request, 'mountain/main.html', {'local_mountain': local_mountain})
    else :
        return redirect('/login')

@login_required(login_url='/login/')
def mountains(request):
    # user = request.user.is_authenticated
    # 산 모델 중에서 100번째까지만 나타내게 하는 필터값
    all_mountain = Mountain.objects.filter(id__lt=101)
    return render(request, 'mountain/all_mountain.html', {'mountains': all_mountain})

@login_required(login_url='/login/')
def mountains_detail(request, id):
    my_mountain = Mountain.objects.get(id=id)

    # 맛집 정보 요청
    client_id = MY_NAVER_SEARCH['CLIENT_ID']
    client_secret = MY_NAVER_SEARCH['CLIENT_SECRET']
    enc_text = urllib.parse.quote(f"{my_mountain.location.split(' ')[0]} {my_mountain.mountain_name} 맛집") # 검색어ex) 화촌면 가리산 맛집 
    url = f"https://openapi.naver.com/v1/search/local.json?query={enc_text}&display=5"
    
    restaurant_req = urllib.request.Request(url)
    restaurant_req.add_header("X-Naver-Client-Id", client_id)
    restaurant_req.add_header("X-Naver-Client-Secret", client_secret)
    
    response = urllib.request.urlopen(restaurant_req)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        restaurant_info = json.loads(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
    return render(request, 'mountain/mountains_detail.html', {'mountain_info': my_mountain, 'restaurant_info': json.dumps(restaurant_info)})


@login_required(login_url='/login/')
def mountain_list(request):
    result = True
    mountains_name = []
    try:
        mountains = Mountain.objects.filter(id__lt=101)
        for mountain in mountains:
            mountains_name.append(mountain.mountain_name)
    except Exception as e:
        print(e)
        result = False
    
    response_value = {
        'result': 'success' if result else 'fail',
        'mountains': mountains_name
    }
    
    return JsonResponse(response_value)