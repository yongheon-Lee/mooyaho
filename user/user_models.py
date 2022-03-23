import os.path
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.db import models


# 프로필사진 업로드 설정 함수
def profile_img_upload_path(instance, filename):
    # 날짜로 세분화
    prefix = timezone.now().strftime('%Y/%m/%d')
    # 길이 32인 uuid값
    file_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 파일명 설정
    custom_file_name = '/'.join([prefix, file_name, extension])
    return custom_file_name


# 모델 객체 정의
class MooyahoUser(AbstractUser):
    # 모델의 DB 기본 정보
    class Meta:
        app_label = 'user'
        # 테이블명 설정
        db_table = 'mooyaho_user'

    # ('DB에 저장되는 값', 'admin페이지, 폼에서 표시되는 값')
    # 성별 분류값
    gender_conf = [
        ('0', '남'),
        ('1', '여'),
    ]

    # 연령대 분류값
    age_gr_conf = [
        ('0', '10대'),
        ('1', '20대'),
        ('2', '30대'),
        ('3', '40대'),
        ('4', '50대'),
        ('5', '60대'),
        ('6', '70대 이상'),
    ]

    # 등산 경력 분류값
    exp_conf = [
        ('0', '초급'),
        ('1', '중급'),
        ('2', '고급'),
    ]

    # 등산 목적 분류값
    reason_conf = [
        ('0', '친목모임'),
        ('1', '건강관리'),
        ('2', '탐험'),
        ('3', '친환경'),
        ('4', '취미'),
        ('5', '사진'),
    ]

    # 필드
    nickname = models.CharField(max_length=10, unique=True, verbose_name='닉네임')
    gender = models.CharField(max_length=2, choices=gender_conf, verbose_name='성별')
    age_gr = models.CharField(max_length=10, choices=age_gr_conf, verbose_name='연령대')
    disabled = models.BooleanField(default=False, verbose_name='탈퇴 여부')
    superuser = models.BooleanField(default=False, verbose_name='관리자 여부')
    profile_img = models.ImageField(blank=True, upload_to=profile_img_upload_path, verbose_name='프로필 사진')
    exp = models.CharField(max_length=10, choices=exp_conf, verbose_name='등산 경력')
    reason = models.CharField(max_length=100, choices=reason_conf, verbose_name='등산 목적')
    latitude = models.FloatField(default=0, verbose_name='유저 위치 위도')
    longitude = models.FloatField(default=0, verbose_name='유저 위치 경도')

    # 각 유저 객체가 유저 아이디로 표시되도록 설정
    def __str__(self):
        return self.nickname
