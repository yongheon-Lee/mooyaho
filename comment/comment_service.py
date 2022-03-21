from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@ login_required(login_url='login')
def comment(request, post_id):

    return render(request, 'post/posts.html')
