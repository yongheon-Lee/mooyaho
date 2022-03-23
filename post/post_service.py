from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mountain.models import Mountain
from post.post_models import Post
from user.user_models import MooyahoUser
from comment.comment_models import Comment


# 글 전체 페이지 기능
@ login_required(login_url='login')
def post_list(request):
    if request.method == 'GET':
        # 삭제처리 되지 않은 모든 글 가져오기, 포스팅 날짜 역순으로 정렬
        all_post = Post.objects.filter(deleted=0).order_by('-created_at')
        post_list_context = {
            'all_post': all_post
        }
        return render(request, 'post/posts.html', post_list_context)


# 글 상세 페이지 기능
@login_required(login_url='login')
def post_detail(request, pk):
    if request.method == 'GET':
        # 선택한 글의 id를 받아서 해당 id에 맞는 글 가져오기
        clicked_post = Post.objects.get(id=pk)

        # 해당 글의 댓글 중 삭제 처리되지 않은 댓글 모두 가져오기
        comments = Comment.objects.filter(post_id=clicked_post.id, deleted=False)

        post_detail_context = {
            'clicked_post': clicked_post,
            'all_comment': comments
        }
        return render(request, 'post/detail.html', post_detail_context)


# 글 쓰기 기능
@login_required(login_url='login')
def post(request):
    if request.method == 'GET':
        # 산 이름 검색창을 위해 전체 산 데이터 가져오기
        mt = Mountain.objects.all()
        return render(request, 'post/new.html', {'mountains': mt})

    elif request.method == 'POST':
        # 산 이름 입력 받기
        input_mt = request.POST['inputMt']

        # Mountain 참조
        get_mt = Mountain.objects.filter(mountain_name=input_mt)

        # 해당 이름의 산 있으면,
        if get_mt:
            # 산 이름 가져오기
            post_mountain_name = Mountain.objects.get(mountain_name=input_mt).mountain_name
            # 산 id 가져오기
            mountain_id = Mountain.objects.get(mountain_name=post_mountain_name).id

        # 없으면,
        else:
            # 산 DB에 없는 산 이름 새로 추가
            mt = Mountain()
            mt.id = Mountain.objects.all().last().id + 1
            mt.mountain_name = input_mt
            mt.save()

            # 입력값을 산 이름에 적용
            post_mountain_name = input_mt
            # 추가된 산 id 적용
            mountain_id = mt.id

        # 포스팅 생성
        new_posting = Post.objects.create(
            user=MooyahoUser.objects.get(id=request.user.id),
            hiking_img=request.FILES.get('hiking_img'),
            title=request.POST['title'],
            mountain_name=post_mountain_name,
            mountain=Mountain.objects.get(id=mountain_id),
            content=request.POST['inputReview'],
            rating=request.POST['rating']
        )
        new_posting.save()
        return redirect(f'/posts/{str(new_posting.id)}/')


# 글 수정 기능
@login_required(login_url='login')
def edit_post(request, pk):
    posting = Post.objects.get(id=pk)

    # 글 작성자와 요청한 유저가 같은지 확인
    if posting.user.id == request.user.id:
        if request.method == 'GET':
            # 산 이름 검색창을 위해 전체 산 데이터 가져오기
            mt = Mountain.objects.all()
            return render(request, 'post/new.html', {'mountains': mt})

        elif request.method == 'PUT':

            # 산 이름 입력 받기
            input_mt = request.POST['inputMt']

            # Mountain 참조
            get_mt = Mountain.objects.filter(mountain_name=input_mt)

            # 해당 이름의 산 있으면,
            if get_mt:
                # 산 이름 가져오기
                post_mountain_name = Mountain.objects.get(mountain_name=input_mt).mountain_name
                # 산 id 가져오기
                mountain_id = Mountain.objects.get(mountain_name=post_mountain_name).id

            # 없으면,
            else:
                # 산 DB에 없는 산 이름 새로 추가
                mt = Mountain()
                mt.id = Mountain.objects.all().last().id + 1
                mt.mountain_name = input_mt
                mt.save()

                # 입력값을 산 이름에 적용
                post_mountain_name = input_mt
                # 추가된 산 id 적용
                mountain_id = mt.id

            # 수정 내용 반영
            posting.hiking_img = request.FILES.get('hiking_img')
            posting.title = request.POST['title']
            posting.mountain_name = post_mountain_name
            posting.mountain = mountain_id
            posting.content = request.POST['inputReview']
            posting.rating = request.POST['rating']
            posting.save()
            return redirect(f'/posts/{str(posting.id)}/')


# 글 삭제 기능
@login_required(login_url='login')
def delete_post(request, pk):
    posting = Post.objects.get(id=pk)

    # 글 작성자와 요청한 유저가 같은지 확인
    if posting.user.id == request.user.id:
        # 글을 실제로 삭제하지 않고 삭제된 것처럼 처리
        posting.deleted = True
        posting.save()
        # posting.delete()
        return redirect('posts')
