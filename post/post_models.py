import os.path
from uuid import uuid4

from django.utils import timezone

from django.db import models

from mountain.models import Mountain
from user.user_models import MooyahoUser


# 등산 사진 업로드명 설정 함수
def hiking_img_upload_path(instance, filename):
    # 날짜로 세분화
    prefix = timezone.now().strftime('%Y/%m/%d')
    # 길이 32인 uuid값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 파일명 설정
    custom_file_name = '/'.join([prefix, uuid_name, extension])
    return custom_file_name


# 모델 객체 정의
class Post(models.Model):
    # 모델의 DB 기본 정보
    class Meta:
        # 테이블명 설정
        db_table = 'mooyaho_post'

    # 필드
    # 정참조: ForeignKey 갖고 있는 모델에서 해당 모델 참조
    # 역참조: 정참조 반대 방향. 참조되는 모델에서 ForeignKey를 갖고 있는 모델 참조

    # User모델을 참조하기 위한 외래키(참조되는 모델, User에서 Post 역참조 시 'post_set' 대체명, 컬럼명)
    user = models.ForeignKey(MooyahoUser, related_name='user_post_ref',
                             db_column='author_id', on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=20, null=False)
    mountain_name = models.CharField(max_length=20, null=False, default='')
    # Mountain모델을 참조하기 위한 외래키(참조되는 모델, Mountain에서 Post 역참조 시 'post_set' 대체명, 컬럼명)
    mountain = models.ForeignKey(Mountain, related_name='post_mt_ref', on_delete=models.CASCADE)
    content = models.TextField(null=False)
    rating = models.CharField(max_length=10, null=False)
    hiking_img = models.ImageField(null=False, blank=False, upload_to=hiking_img_upload_path)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(MooyahoUser, related_name='post_likes')

    # 글의 좋아요 개수 세기
    def count_likes(self):
        return self.likes.count()

    # 각 글 객체가 제목으로 표시되도록 설정
    def __str__(self):
        return self.title
