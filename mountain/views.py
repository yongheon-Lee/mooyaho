from django.contrib import auth
from django.shortcuts import render, redirect
from .models import Mountain
from django.contrib.auth.decorators import login_required


# def home(request):
#     user = request.user
#     if user.is_authenticated :
#         user_x = user.longitude
#         user_y = user.latitude
#         user_max_x = user_x + 0.3
#         user_max_y = user_y + 0.3
#         user_min_x = user_x - 0.3
#         user_min_y = user_y - 0.3
#         local_mountain = Mountain.objects.filter(maxx__lt = user_max_x,
#                                                  maxx__gt = user_min_x,
#                                                  maxy__lt = user_max_y,
#                                                  maxy__gt = user_min_y)
#         return render(request, 'mountain/main.html', {'local_mountains': local_mountain})
#     else :
#         return redirect('/login')

def home(request):
    user = request.user
    if user.is_authenticated :
        user_data = user.reason_conf
        return render(request, 'mountain/mtest.html', {'user_data': user_data})
    else :
        return redirect('/login')


# @login_required()
def mountains(request):
    # user = request.user.is_authenticated
    # 산 모델 중에서 100번째까지만 나타내게 하는 필터값
    all_mountain = Mountain.objects.filter(id__lt=101)
    return render(request, 'mountain/all_mountain.html', {'mountains': all_mountain})


def mountains_detail(request, id):
    my_mountain = Mountain.objects.get(id=id)
    return render(request, 'mountain/mountains_detail.html', {'mountain_info': my_mountain})

# main이랑 연결하기
# def main(request) :
#     # 만약 유저뷰로그가 안 쌓이고 기본 위치정보를 허용할 때, 허용 안 할땐 정보없음으로 나타내기
#     if 위치정보 is True :
#         유저의 위치 정보 = 위도+-0.3, 경도+-0.3
#         if maxx in range(유저의 최소 위도 정보 : 유저의 최대 위도정보):
#         if maxy in range(유저의 최소 경도 정보 : 유저의 최대 경도정보):
#           해당하는 값 나타내기
#         산 위도에 일치하는 값 = Mountain.object.filter(유저 위치의 범위 내에 있는 maxx)
#         산 경도에 일치하는 값 = Mountain.objcet.filter(유저 위치의 범위 내에 있는 maxy)
#     else :
#         return render(request, 'index.html', {'error': '위치 정보가 존재하지 않습니다. '})

# 위도 경도 +-30분씩 차이나게 하기


# 산 모델 중에서 100번째까지만 나타내게 하는 필터값
# my = 유저의 위도 정보 - 0.3
# My = 유저의 위도 정보 + 0.3
# Mountain.objects.filter(maxy <= my and mixy >= My and maxx <= mx and minx >= Mx)
# Mountain.objects.filter(maxx__lt=a)






