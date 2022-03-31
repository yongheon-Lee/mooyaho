from django.db import models

from post.post_models import Post
from user.user_models import MooyahoUser


class Comment(models.Model):
    # 모델의 DB 기본 정보
    class Meta:
        # 테이블명 설정
        db_table = 'mooyaho_post_comment'

    # 필드
    post = models.ForeignKey(Post, related_name='post_comment_ref', on_delete=models.CASCADE)
    author = models.ForeignKey(MooyahoUser, related_name='user_comment_ref', on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=False, null=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # 각 댓글 객체가 닉네임 + 댓글 세 글자로 표시되도록 설정
    def __str__(self):
        return self.author.nickname + ' / ' + self.comment[:3] + '...'
