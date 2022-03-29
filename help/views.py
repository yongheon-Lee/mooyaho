from django.shortcuts import render, redirect
from .models import Notice, Review
from django.contrib.auth.decorators import login_required

from user.user_models import MooyahoUser
# Create your views here.

@login_required(login_url='/login')
def index(request):
    return render(request, 'help/help.html')

@login_required(login_url='/login')
def notice(request):
    user = request.user.is_authenticated
    if user:
        all_notice = Notice.objects.filter(deleted=False).order_by('-create_at')
        return render(request, 'help/notice.html', {'notice': all_notice})
    else:
        return redirect('/login')

def post_notice(request):
    if request.method == "GET":
        return render(request, 'help/post_notice.html')
    elif request.method == 'POST':
        # user가 슈퍼인지 아닌지
        if request.user.is_superuser is True :
        # 여기서부터
            new_notice = Notice.objects.create(
                user_id=MooyahoUser.objects.get(id=request.user.id),
                title=request.POST.get('title'),
                content=request.POST.get('textarea-name')
            )
            new_notice.save()
        #여기까지 이호진이 작성.

        # user = request.user
        # my_notice = Notice
        # my_notice.title = request.POST.get('textarea-name')
        # my_notice.content = request.POST.get('textarea-name')
        # my_notice.user_id = user.id
        # my_notice.save()
            return redirect('/help/notice')
        else :
            return redirect('/help/notice')

@login_required(login_url='/login')
def edit_notice(request, id):
    update_notice = Notice.objects.get(id=id)
    print(request.user.id)
    print(update_notice.user_id.id)
    if request.user.id == update_notice.user_id.id:
        if request.method == 'GET':
            return render(request, 'help/edit_notice.html', {'notice': update_notice})
        elif request.method == 'POST':
            update_notice.title = request.POST.get('title')
            update_notice.content = request.POST.get('content')
            update_notice.save()
            return redirect('notice')


@login_required(login_url='/login')
def delete_notice(request, id):
    my_notice = Notice.objects.get(id=id)

    now_user_id = MooyahoUser.objects.get(nickname=my_notice.user_id)
    print(request.user.id)
    print(my_notice.user_id)
    print(now_user_id)
    if request.user.id == now_user_id.id :

        print("사용자가 맞음.")
        my_notice.deleted = True
        my_notice.save()
        return redirect('notice')
    else :
        print("사용자 틀림.")
        return redirect('notice')

@login_required(login_url='/login')
def review(request):
    # all_review = Review.objects.all()
    all_review = Review.objects.filter(deleted=0)
    return render(request, 'help/review.html', {'all_review':all_review})


@login_required(login_url='/login')
def post_review(request):
    if request.method == 'GET':
        return render(request, 'help/post_review.html')
    elif request.method == 'POST':
        if request.POST.get('checkbox') == 'on':
            checkbox = True
        else :
            checkbox = False

        new_review = Review.objects.create(
            author= MooyahoUser.objects.get(id=request.user.id),
            content=request.POST.get('textarea'),
            secret=checkbox,

        )
        new_review.save()
        return redirect('review')


@login_required(login_url='/login')
def delete_review(request, id):
    review = Review.objects.get(id=id)
    # 글 작성자와 요청한 유저가 같은지 확인
    if review.author.id == request.user.id or request.user.is_superuser:
        review.deleted = True
        review.save()
        return redirect('/help/review')
    else :
        return redirect('/help/review') 

# 2022-03-29
@login_required(login_url='/login')
def update_review(request, id) :
    ut_review = Review.objects.get(id=id) #업데이트할 리뷰
    if ut_review.author.id == request.user.id :
        if request.method == 'GET':
            return render(request, 'help/edit_review.html', {'ut_review': ut_review})
        elif request.method == 'POST' : # 포스트 방식일때
            ut_review.content = request.POST.get('textarea') # 수정한 내용 바꾸기
            if request.POST.get('checkbox') == 'on':
                checkbox = True
            else:
                checkbox = False
            ut_review.secret = checkbox
            ut_review.save() # 저장
            return redirect('review') # 리뷰로 돌아가기


@login_required(login_url='/login')
def answer_review(request, id) :
    as_review = Review.objects.get(id=id)
    if request.method == 'POST':
        as_review.answer = request.POST.get('modal_form')
        as_review.save()
        return redirect('review')
