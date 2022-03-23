from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from post.post_models import Post
from user.user_models import MooyahoUser
from .comment_models import Comment

import json


@ login_required(login_url='login')
def new_comment(request):
    json_object = json.loads(request.body)

    comment = Comment.objects.create(
        author=json_object.get('author'),
        post=json_object.get('post'),
        comment=json_object.get('comment')
    )
    comment.save()

    context = {
        'author': request.user.nickname,
        'comment': comment.comment,
    }
    return JsonResponse(context)
