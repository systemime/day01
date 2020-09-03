from django.db import models
from app01.models import UserProfile

# Create your models here.


class TalkGroup(models.Model):
    group_name = models.CharField(max_length=20, null=False, blank=False, verbose_name="组名")
    brief = models.CharField(max_length=255, null=True, blank=True, default="管理层很懒，不想写简介...", verbose_name="简介")
    owner = models.ForeignKey(UserProfile, verbose_name="所属用户", related_name="group_owner", on_delete=models.CASCADE)
    admins = models.ManyToManyField(UserProfile, blank=True, related_name="group_admin", verbose_name='管理员')
    members = models.ManyToManyField(UserProfile, blank=True, related_name="group_member", verbose_name='群员')

    class Meta:
        verbose_name = u"聊天组"
        verbose_name_plural = u"聊天组"
