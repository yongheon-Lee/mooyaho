from django.db import models
from user.user_models import MooyahoUser
from post.post_models import Post


# Create your models here.
class Notice(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    user_id = models.ForeignKey(MooyahoUser, on_delete=models.CASCADE, db_column='user_id')
    create_at = models.DateField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'notice'

    # 각 객체가 공지사항 제목으로 표시되도록 설정
    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(MooyahoUser, on_delete=models.CASCADE, db_column='author')
    content = models.TextField(null=False, blank=False)
    secret = models.BooleanField(default=False)
    report = models.BooleanField(default=False)
    answer = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_id', null=True)

    class Meta:
        db_table = 'review'

    # 각 객체가 글 작성자, 내용 일부로 표시되도록 설정
    def __str__(self):
        author_nickname = self.author.nickname
        part_of_content = self.content[:5]
        return author_nickname + ' / ' + part_of_content + '...'
