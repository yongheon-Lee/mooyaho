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
        all_notice = Notice.objects.all().order_by('-create_at')
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
def delete_notice(request, id):
    my_notice = Notice.objects.get(id=id)
    if request.user.id == my_notice.user_id :
        my_notice.deleted = True
        my_notice.save()
        return redirect('/help/notice')
    else :
        return redirect('/help/notice')

@login_required(login_url='/login')
def review(request):
    all_review = Review.objects.all()
    return render(request, 'help/review.html', {'all_review':all_review})

@login_required(login_url='/login')
def post_review(request):
    if request.method == 'GET':
        return render(request, 'help/post_review.html')
    elif request.method == 'POST':
        author = MooyahoUser.objects.get(id=request.user.id)

        new_review = Review.objects.create(
            author=author.nickname,
            content=request.POST.get('textarea-name')
        )
        new_review.save()


        return redirect('/help/review')


@login_required(login_url='/login')
def delete_review(request, id):
    review = Review.objects.get(id=id)
    # 글 작성자와 요청한 유저가 같은지 확인
    if review.author.id == request.user.id:
        review.deleted = True
        review.save()
        return redirect('/help/review')
    else :
        return redirect('/help/review')