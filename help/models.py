from django.db import models
from user.user_models import MooyahoUser

# Create your models here.
class Notice(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    user_id = models.ForeignKey(MooyahoUser, on_delete=models.CASCADE, db_column='user_id')
    create_at = models.DateField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta :
        db_table = 'notice'