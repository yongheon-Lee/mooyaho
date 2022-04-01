from django.shortcuts import render, redirect
from .models import Notice, Review
from django.contrib.auth.decorators import login_required

from user.user_models import MooyahoUser


# 고객센터 둘러보기 가능(login 불필요)
def index(request):
    if request.method == 'GET':
        return render(request, 'help/help.html')


# 공지사항 둘러보기 가능(login 불필요)
def notice(request):
    if request.method == 'GET':
        all_notice = Notice.objects.filter(deleted=False).order_by('-id')
        return render(request, 'help/notice.html', {'notice': all_notice})


@login_required(login_url='login')
def post_notice(request):
    # 관리자 정의
    superuser = request.user.is_superuser

    # 관리자라면,
    if superuser:
        if request.method == "GET":
            return render(request, 'help/post_notice.html')

        elif request.method == 'POST':
            new_notice = Notice.objects.create(
                user_id=MooyahoUser.objects.get(id=request.user.id),
                title=request.POST.get('title'),
                content=request.POST.get('textarea-name')
            )
            new_notice.save()
            return redirect('notice')

    # 아니라면,
    else:
        return redirect('login')


@login_required(login_url='login')
def edit_notice(request, id):
    # 관리자 정의
    superuser = request.user.is_superuser

    # 관리자라면,
    if superuser:
        update_notice = Notice.objects.get(id=id)

        if request.user.id == update_notice.user_id.id:
            if request.method == 'GET':
                return render(request, 'help/edit_notice.html', {'notice': update_notice})

            elif request.method == 'POST':
                update_notice.title = request.POST.get('title')
                update_notice.content = request.POST.get('content')
                update_notice.save()
                return redirect('notice')
    # 아니라면,
    else:
        return redirect('notice')


@login_required(login_url='login')
def delete_notice(request, id):
    # 관리자 정의
    superuser = request.user.is_superuser

    # 관리자라면,
    if superuser:
        my_notice = Notice.objects.get(id=id)
        now_user_id = MooyahoUser.objects.get(nickname=my_notice.user_id)

        if request.user.id == now_user_id.id:
            my_notice.deleted = True
            my_notice.save()
            return redirect('notice')

    # 아니라면,
    else:
        return redirect('notice')


# 리뷰 둘러보기 가능(login 불필요)
def review(request):
    if request.method == 'GET':
        all_review = Review.objects.filter(deleted=0).order_by('-id')
        return render(request, 'help/review.html', {'all_review': all_review})


@login_required(login_url='login')
def post_review(request):
    # 사용자 인증받은 요청자를 유저로 정의
    user = request.user.is_authenticated

    # 인증된 유저라면,
    if user:
        if request.method == 'GET':
            return render(request, 'help/post_review.html')

        elif request.method == 'POST':
            if request.POST.get('checkbox') == 'on':
                checkbox = True
            else:
                checkbox = False

            new_review = Review.objects.create(
                author=MooyahoUser.objects.get(id=request.user.id),
                content=request.POST.get('textarea'),
                secret=checkbox,

            )
            new_review.save()
            return redirect('review')

    # 아니라면,
    else:
        return redirect('login')


@login_required(login_url='login')
def delete_review(request, id):
    # 사용자 인증받은 요청자를 유저로 정의
    user = request.user.is_authenticated

    # 인증된 유저라면,
    if user:
        review = Review.objects.get(id=id)

        # 글 작성자와 요청한 유저와 같거나 관리자라면,
        if review.author.id == request.user.id or request.user.is_superuser:
            review.deleted = True
            review.save()
            return redirect('review')

        # 글 작성자와 요청한 유저 및 관리자가 아니면,
        else:
            return redirect('review')

    # 아니라면,
    else:
        return redirect('login')


@login_required(login_url='login')
def update_review(request, id):
    # 사용자 인증받은 요청자를 유저로 정의
    user = request.user.is_authenticated

    # 인증된 유저라면,
    if user:
        ut_review = Review.objects.get(id=id)  # 업데이트할 리뷰
        if ut_review.author.id == request.user.id:
            if request.method == 'GET':
                return render(request, 'help/edit_review.html', {'ut_review': ut_review})

            elif request.method == 'POST':  # 포스트 방식일 때
                ut_review.content = request.POST.get('textarea')  # 수정한 내용 바꾸기
                if request.POST.get('checkbox') == 'on':
                    checkbox = True

                else:
                    checkbox = False

                ut_review.secret = checkbox
                ut_review.save()  # 저장
                return redirect('review')  # 리뷰로 돌아가기
    # 아니라면,
    else:
        return redirect('login')


@login_required(login_url='login')
def answer_review(request, id):
    if request.method == 'POST':
        as_review = Review.objects.get(id=id)
        as_review.answer = request.POST.get('modal_form')
        as_review.save()
        return redirect('review')
