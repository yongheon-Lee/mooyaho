from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mountain.models import Mountain
from post.post_models import Post
from user.user_models import MooyahoUser


@ login_required(login_url='login')
def post_list(request):
    if request.method == 'GET':
        # 모든 글 가져오기, 포스팅 날짜 역순으로 정렬
        all_post = Post.objects.all().order_by('-created_at')
        post_list_context = {
            'all_post': all_post
        }
        return render(request, 'post/posts.html', post_list_context)


@login_required(login_url='login')
def post_detail(request, pk):
    if request.method == 'GET':
        # 선택한 글의 id를 받아서 해당 id에 맞는 글 가져오기
        clicked_post = Post.objects.get(id=pk)
        post_detail_context = {
            'clicked_post': clicked_post
        }
        return render(request, 'post/detail.html', post_detail_context)


@login_required(login_url='login')
def post(request):
    if request.method == 'GET':
        return render(request, 'post/new.html')

    elif request.method == 'POST':

        input_mt = request.POST['inputMt']
        mountain_name = Mountain.objects.get(mountain_name=input_mt).mountain_name
        if input_mt == mountain_name:
            location = input_mt
        else:
            mountain = Mountain()
            mountain.mountain_name = input_mt
            mountain.save()
            location = input_mt

        new_posting = Post.objects.create(
            user=MooyahoUser.objects.get(id=request.user.id),
            hiking_img=request.FILES.get('hiking_img'),
            title=request.POST['title'],
            location=location,
            content=request.POST['inputReview'],
            rating=request.POST['rating']
        )
        new_posting.save()
        return redirect('/posts/' + str(new_posting.id))

    elif request.method == 'PUT':
        posting = Post.objects.get(id=id)
        return redirect('/posts/' + str(posting.id))

    elif request.method == 'DELETE':
        posting = Post.objects.get(id=id)
        posting.delete()
        return redirect('posts')


# https://velog.io/@limsw/Django-Rest-framework-%EB%8B%A4%EB%A3%A8%EA%B8%B0-2
# https://itsource.tistory.com/50
# https://wayhome25.github.io/django/2017/05/10/media-file/#%ED%8C%8C%EC%9D%BC-%EC%97%85%EB%A1%9C%EB%93%9C%EC%8B%9C%EC%9D%98-form-enctype-%ED%85%9C%ED%94%8C%EB%A6%BF%EB%82%B4-media-url-%EC%B2%98%EB%A6%AC-template
# https://hangbokcoding.tistory.com/m/45

