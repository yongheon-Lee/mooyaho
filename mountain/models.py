from django.db import models


class Mountain(models.Model):
    id = models.BigIntegerField(primary_key=True)
    mountain_id = models.FloatField(blank=True, null=True)
    mountain_name = models.CharField(max_length=30, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    selection_reason = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    course_information = models.TextField(blank=True, null=True)
    mountain_information = models.TextField(blank=True, null=True)
    stay = models.TextField(blank=True, null=True)
    transportation = models.TextField(blank=True, null=True)
    local_code = models.FloatField(blank=True, null=True)
    local_name = models.TextField(blank=True, null=True)
    maxy = models.FloatField(blank=True, null=True)
    maxx = models.FloatField(blank=True, null=True)
    miny = models.FloatField(blank=True, null=True)
    minx = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mountain'

    # 각 객체가 산 이름으로 표시되도록 설정
    def __str__(self):
        return self.mountain_name
