from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from .models import Mountain
from user.user_models import UserViewLog
from django.contrib.auth.decorators import login_required
import urllib.request
import json
from config.my_settings import MY_NAVER_SEARCH

cc = []
# 받아온 산 아이디 +1시켜주는 함수
def mountain_id_plus(x) :
    for i in x :
        cc.append(i+1)
    return cc

@login_required(login_url='/login/')
def home(request):
    payload = {'userid': request.user.id}
    #AI서버와 통신(userviewlog)
    URL1="http://127.0.0.1:5000/userviewlog"
    res1=requests.post(URL1,data=payload)  #post형식으로 data를 url에 넣어 요청후 응답받음
    res1=res1.json() #응답 json으로 바꾸기
    print(res1)

    # AI서버와 통신(userpost)
    URL2 = "http://127.0.0.1:5000/userpost"
    res2 = requests.post(URL2, data=payload)
    res2=res2.json()
    print(res2)

    if res1['data']==0:  #활동로그없을경우
        recommand_mountain=[]
        keyword=[]
    else:  #활동로그있을경우
        keyword = res1['keyword'] #키워드 값만 분리
        request_recommand_mountain = res1['mountain'] #산 아이디만 분리

        recommand_mountain = mountain_id_plus(request_recommand_mountain) # 받은 산 id에서 1씩 더하기
        recommand_mountain = Mountain.objects.filter(id__in=recommand_mountain) # 리스트 요소들에 해당하는 id와 같은 객체 가져오기
        print(recommand_mountain)

    if res2['data']==0:  #게시물이 없을경우
        # _____님! 게시물을 업로드해보세요~
        user=[]
    else:
        # 세유저의 최근 게시물 하나씩 보여주기
        user = res2['user']
        print(user)

    user = request.user
    # 유저가 로그인했을때
    if user.is_authenticated :
        # 만약 지역 정보가 0.0일떄,
        if user.longitude == 0.0 and user.latitude == 0.0 :
            # return render(request, 'mountain/main.html', {'total': {'recommand_mountain': recommand_mountain},
            #                                               'keyword': keyword})
            local_mountain = []
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
        return render(request, 'mountain/main.html', {'total': {'local_mountain': local_mountain,
                                                                'recommand_mountain': recommand_mountain},
                                                      'keyword': keyword})
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
    # userviewlog 데이터 넣기
    user = request.user

    user_id = user.id
    mountain_id = Mountain.objects.get(id=id).id

    b = UserViewLog(mountain_id=mountain_id,
                    user_id=user_id)
    b.save()

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

# def userviewlog(request, id) :
#     if request.method == 'POST' :
#         user = request.user
#         log = UserViewLog
#
#         log.mountain_id =
#         log.user_id = user.id


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
