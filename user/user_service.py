from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from post.post_models import Post
from .user_models import MooyahoUser


# 로그인
def login(request):
    # 로그인한 상태인지 확인
    if request.user.is_authenticated:
        # 로그인 한 상태면 메인 페이지로 넘김
        return redirect('main')

    else:
        if request.method == 'GET':
            return render(request, 'user/login.html')

        elif request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']

            exist_user = auth.authenticate(request, username=email, password=password)
            if exist_user is not None:
                exist_user.latitude = latitude
                exist_user.longitude = longitude
                exist_user.save()
                auth.login(request, exist_user)
                return redirect('main')

            else:
                return render(request, 'user/login.html', {'error': '입력하신 사용자가 없습니다.'})


# 회원가입
def signup(request):
    # 로그인한 상태인지 확인
    if request.user.is_authenticated:
        # 로그인 한 상태면 메인 페이지로 넘김
        return redirect('main')

    else:
        if request.method == 'GET':
            return render(request, 'user/signup.html')

        elif request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            nickname = request.POST['nickname']
            gender = request.POST['gender']
            age_gr = request.POST['age_gr']
            exp = request.POST['exp']
            reasons = request.POST.getlist('reason')

            # 성별 분류값 변환
            if gender == '0':
                gender = '남'
            elif gender == '1':
                gender = '여'

            # 연령대 분류값 변환
            if age_gr == '0':
                age_gr = '10대'
            elif age_gr == '1':
                age_gr = '20대'
            elif age_gr == '2':
                age_gr = '30대'
            elif age_gr == '3':
                age_gr = '40대'
            elif age_gr == '4':
                age_gr = '50대'
            elif age_gr == '5':
                age_gr = '60대'
            elif age_gr == '6':
                age_gr = '70대 이상'

            # 등산 경력 분류값 변환
            if exp == '0':
                exp = '초급'
            elif exp == '1':
                exp = '중급'
            elif exp == '2':
                exp = '고급'

            # 등산 목적 분류값 변환
            int_to_str_reasons = []
            for reason in reasons:
                if reason == '0':
                    reason = '친목모임'
                    int_to_str_reasons.append(reason)
                elif reason == '1':
                    reason = '친환경'
                    int_to_str_reasons.append(reason)
                elif reason == '2':
                    reason = '건강관리'
                    int_to_str_reasons.append(reason)
                elif reason == '3':
                    reason = '취미활동'
                    int_to_str_reasons.append(reason)
                elif reason == '4':
                    reason = '탐험'
                    int_to_str_reasons.append(reason)
                elif reason == '5':
                    reason = '사진'
                    int_to_str_reasons.append(reason)

            exist_user = MooyahoUser.objects.filter(username=email)
            if len(exist_user) > 0:
                return render(request, 'user/signup.html', {'error': '존재하는 사용자입니다.'})
            else:
                if password != password_confirm:
                    return render(request, 'user/signup.html', {'error': '비밀번호가 서로 다릅니다.'})
                else:
                    new_user = MooyahoUser.objects.create_user(username=email, password=password,
                                                               nickname=nickname, gender=gender,
                                                               age_gr=age_gr, exp=exp,
                                                               reason=int_to_str_reasons)
                    # 회원가입 후 바로 로그인 처리
                    auth.login(request, new_user)
                    return redirect('main')


# 로그아웃
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


# 마이 페이지
@login_required(login_url='login')
def my_page(request):

    # 현재 유저 id
    user_id = request.user.id

    # 현재 유저 id에 맞는 유저 모델 호출
    current_user = MooyahoUser.objects.get(id=user_id)

    # 현재 유저가 작성한 게시글 중 삭제 처리 되지 않은 글 모두 가져오기
    my_post = Post.objects.filter(user=current_user, deleted=False)

    # 현재 유저가 좋아요한 게시글 중 삭제 처리 되지 않은 글 모두 가져오기
    # 참고 자료
    # https://velog.io/@swhan9404/ManyToMany-Relationship%EC%A2%8B%EC%95%84%EC%9A%94-%ED%94%84%EB%A1%9C%ED%95%84-Follow-QuerySet%EC%9D%80-lazy%ED%95%98%EB%8B%A4-Pagination
    my_favorite = current_user.post_likes.filter(deleted=False)

    # 프론트로 보낼 데이터 담기
    context = {
        'myinfo': current_user,
        'myposts': my_post,
        'myfavorite': my_favorite,
    }

    if request.method == 'GET':
        return render(request, 'user/mypage.html', context)

    # 프로필 수정
    if request.method == 'POST':
        try:
            current_user.profile_img = request.FILES.get('profile_img')
            current_user.save()
            return JsonResponse({'result': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'result': 'fail', 'msg': '프로필 사진 변경에 실패하였습니다'})
