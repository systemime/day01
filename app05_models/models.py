# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=50)
    qq = models.CharField(max_length=10)
    addr = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=50)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()  # 文章的打分

    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, help_text="标签名称")
    commit = models.CharField(max_length=20, verbose_name="描述", help_text="测试描述")

    def __str__(self):
        return self.name
