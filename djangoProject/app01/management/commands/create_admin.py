from django.core.management.base import BaseCommand
from app01.models import User
import hashlib

class Command(BaseCommand):
    help = '创建管理员账号'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str, help='管理员手机号')
        parser.add_argument('username', type=str, help='管理员用户名')
        parser.add_argument('password', type=str, help='管理员密码')

    def handle(self, *args, **options):
        phone = options['phone']
        username = options['username']
        password = options['password']

        # 检查手机号是否已存在
        if User.objects.filter(phone=phone).exists():
            self.stdout.write(self.style.ERROR(f'手机号 {phone} 已存在'))
            return

        # 创建管理员用户
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        encrypted_password = md5.hexdigest()

        User.objects.create(
            phone=phone,
            username=username,
            password=encrypted_password,
            is_admin=True
        )

        self.stdout.write(self.style.SUCCESS(f'成功创建管理员账号 {username}')) 