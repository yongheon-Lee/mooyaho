import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from help.models import Review
from mountain.models import Mountain
from post.post_form import PostForm
from post.post_models import Post
from user.user_models import MooyahoUser
from comment.comment_models import Comment
from user.user_models import UserViewLog


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

        if clicked_post.deleted:  # 삭제된 게시물일 경우
            if request.user.is_superuser:
                pass
            else:  # 삭제된 게시물을 일반유저가 보려고 하면
                return render(request, 'post/404error.html')

        # 별점 표시
        rating = ['⭐' for _ in range(int(clicked_post.rating))]

        # 해당 글의 댓글 중 삭제 처리되지 않은 댓글 모두 가져오기
        comments = Comment.objects.filter(post_id=clicked_post.id, deleted=False)

        post_detail_context = {
            'clicked_post': clicked_post,
            'all_comment': comments,
            'rating': rating
        }
        # userviewlog에 게시물의 산의 id 넣기
        userviewlog=UserViewLog(user_id=request.user.id,
                                post_mountain_id=clicked_post.mountain_id)
        userviewlog.save()

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

        get_hiking_img = request.FILES.get('hiking_img')
        if get_hiking_img is None:
            message = '사진을 다시 등록해 주세요!'
            return render(request, 'post/new.html', {'message': message})
        else:
            hiking_img = get_hiking_img

        # 포스팅 생성
        new_posting = Post.objects.create(
            user=MooyahoUser.objects.get(id=request.user.id),
            hiking_img=hiking_img,
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
def change_post(request, pk):
    posting = Post.objects.get(id=pk)

    # 글 수정 접근 요청
    if request.method == 'GET':
        # 글 작성자와 요청한 유저가 같은지 확인
        if posting.user.id == request.user.id:

            # 기존 글 내용 가져오기
            form = PostForm(instance=posting)

            # 산 이름 검색창을 위해 전체 산 데이터 가져오기
            mt = Mountain.objects.all()

            # 프론트로 넘길 데이터 담기
            context = {
                'post_id': posting.id,
                'form': form,
                'mountains': mt,
            }
            return render(request, 'post/new.html', context)

    # 글 수정 요청
    elif request.method == 'POST':
        # 글 작성자와 요청한 유저가 같은지 확인
        if posting.user.id == request.user.id:

            form = PostForm(request.POST, request.FILES, instance=posting)

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

            # 글 수정 페이지 이미지 처리
            new_or_old_hiking_img = request.FILES.get('hiking_img')
            if new_or_old_hiking_img is None:
                hiking_img = posting.hiking_img
            else:
                hiking_img = new_or_old_hiking_img

            posting.hiking_img = hiking_img
            posting.title = form.data['title']
            posting.mountain_name = post_mountain_name
            posting.mountain_id = mountain_id
            posting.content = form.data['inputReview']
            posting.rating = form.data['rating']
            posting.save()

            # if form.is_valid():
            #     # 넘겨진 데이터를 바로 모델에 저장하지 않는다.
            #     posting = form.save(commit=False)
            #
            #     # # 수정 내용 반영
            #     posting.hiking_img = hiking_img
            #     posting.title = request.POST['title']
            #     posting.mountain_name = post_mountain_name
            #     posting.mountain_id = mountain_id
            #     posting.content = request.POST['inputReview']
            #     posting.rating = request.POST['rating']
            #     posting.save()

            context = {'result': 'ok'}
            return redirect(f'/posts/{posting.id}/', pk)

            # else:
            #     # context = {'result': 'no'}
            #     form = PostForm(instance=posting)
            #     context = {'form': form}
            #     return render(request, 'post/new.html', context)

    # 글 삭제 요청
    elif request.method == 'DELETE':

        # 글 작성자와 요청한 유저가 같은지 확인
        if posting.user.id == request.user.id:
            # 글을 실제로 삭제하지 않고 삭제된 것처럼 처리
            posting.deleted = True
            posting.save()

            # 프론트로 넘길 데이터 담기
            context = {'result': 'ok'}
            return JsonResponse(context)

        else:
            context = {'result': 'no'}
            return JsonResponse(context)


# 글 좋아요 기능
@login_required(login_url='login')
def like_post(request, pk):
    posting = Post.objects.get(id=pk)
    user = request.user

    if posting.likes.filter(id=user.id).exists():
        posting.likes.remove(user)
        posting.save()
        message = '좋아요 취소'

    else:
        posting.likes.add(user)
        posting.save()
        message = '좋아요'

    # 좋아요 개수, 메시지
    context = {
        'likes_count': posting.count_likes(),
        'message': message,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


# 글 신고 기능
@login_required(login_url='login')
def report_post(request, pk):
    json_object = json.loads(request.body)

    author = MooyahoUser.objects.get(id=request.user.id)
    reported_post = Post.objects.get(id=pk)

    # 글 신고
    new_report = Review.objects.create(
        author=author,
        content=json_object.get('content'),
        report=True,
        post_id=reported_post,
    )
    new_report.save()
    # 해당 글 신고된 횟수 증가
    reported_post.reported += 1
    reported_post.save()

    context = {
        'author': request.user.nickname,
        'content': json_object.get('content')
    }
    return HttpResponse(json.dumps(context), content_type='application/json')
