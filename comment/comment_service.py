from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from post.post_models import Post
from user.user_models import MooyahoUser
from .comment_models import Comment

import json


@login_required(login_url='login')
def comments(request, pk):
    json_object = json.loads(request.body)

    # 댓글 작성 요청
    if request.method == 'POST':
        # 댓글 생성
        comment = Comment.objects.create(
            author=MooyahoUser.objects.get(id=request.user.id),
            post=Post.objects.get(id=pk),
            comment=json_object.get('comment')
        )
        comment.save()

        # 프론트로 넘길 댓글 아이디 추가
        comment_id = comment.id

        # 프론트로 넘길 데이터 담기
        context = {
            'author': request.user.nickname,
            'comment': comment.comment,
            'comment_id': comment_id,
            'post_id': pk,
        }
        return JsonResponse(context)

    # 댓글 삭제 요청
    elif request.method == 'DELETE':
        # 댓글 id에 맞는 댓글 가져오기
        comment = Comment.objects.get(id=json_object.get('comment_id'))

        # 댓글 작성자와 요청자가 같은지 확인
        if request.user == comment.author:
            # 댓글 삭제 처리
            comment.deleted = True
            comment.save()

            # 프론트로 넘길 데이터 담기
            context = {'result': 'ok'}
            return JsonResponse(context)
        else:
            context = {'result': 'no'}
            return JsonResponse(context)
