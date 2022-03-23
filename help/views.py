from django.shortcuts import render, redirect
from .models import Notice
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, 'help/help.html')


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
        user = request.user
        my_notice = Notice
        my_notice.title = request.POST.get('textarea-name')
        my_notice.content = request.POST.get('textarea-name')
        my_notice.user_id = user.id
        my_notice.save()
        return redirect('/post_notice')

#
# @login_required()
# def delete_notice(request, id):
#     my_notice = Notice.objects.get(id=id)
#     my_notice.delete()
#     return redirect('/tweet')


def review(request):
    return render(request, 'help/review.html')
