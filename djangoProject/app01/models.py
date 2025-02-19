from django.db import models


class User(models.Model):
    """用户模型"""
    username = models.CharField(max_length=50, verbose_name='用户名')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    password = models.CharField(max_length=32, verbose_name='密码')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class MusicStyle(models.Model):
    """音乐风格"""
    name = models.CharField(max_length=32, unique=True, verbose_name='风格名称')

    class Meta:
        db_table = 'music_style'
        verbose_name = '音乐风格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserPreference(models.Model):
    """用户偏好设置"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    favorite_artists = models.TextField(blank=True, verbose_name='喜欢的歌手')
    age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='性别')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户偏好'
        verbose_name_plural = verbose_name


class Artist(models.Model):
    """歌手模型"""
    name = models.CharField(max_length=100, verbose_name='歌手名')
    introduction = models.TextField(blank=True, verbose_name='简介')
    avatar = models.URLField(blank=True, verbose_name='头像URL')
    popularity = models.IntegerField(default=0, verbose_name='热度')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '歌手'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
