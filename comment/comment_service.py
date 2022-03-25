from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from post.post_models import Post
from user.user_models import MooyahoUser
from .comment_models import Comment

import json


@ login_required(login_url='login')
def new_comment(request, pk):
    json_object = json.loads(request.body)

    comment = Comment.objects.create(
        author=MooyahoUser.objects.get(id=request.user.id),
        post=Post.objects.get(id=pk),
        comment=json_object.get('comment')
    )
    comment.save()

    context = {
        'author': request.user.nickname,
        'comment': comment.comment,
    }
    return JsonResponse(context)


@login_required(login_url='login')
def delete_comment(request, pk):
    json_object = json.loads(request.body)

    comment = Comment.objects.get(id=json_object.get('comment_id'))

    if request.user == comment.author:
        comment.deleted = True
        comment.save()
        context = {'result': 'ok'}
        return JsonResponse(context)
    else:
        context = {'result': 'no'}
        return JsonResponse(context)
