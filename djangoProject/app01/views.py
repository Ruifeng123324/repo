from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from app01.models import User, MusicStyle, UserPreference, Artist
import hashlib
from django.templatetags.static import static
from django.contrib import messages


def encrypt_password(password):
    """密码加密"""
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def login(request):
    """登录视图"""
    if request.method == 'GET':
        return render(request, 'login.html')

    phone = request.POST.get('phone')
    password = request.POST.get('password')

    # 数据验证
    if not all([phone, password]):
        return render(request, 'login.html', {'error_msg': '请填写完整信息'})

    # 验证用户
    try:
        user = User.objects.get(phone=phone)
        print(f"找到用户: {user.username}, 是否管理员: {user.is_admin}")  # 添加调试信息
        if user.password == encrypt_password(password):
            # 登录成功，保存用户信息到session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_admin'] = user.is_admin
            print(f"Session设置完成: {request.session['is_admin']}")  # 添加调试信息
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_msg': '密码错误'})
    except User.DoesNotExist:
        return render(request, 'login.html', {'error_msg': '用户不存在'})


def register(request):
    """注册视图"""
    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST.get('username')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    # 数据验证
    if not all([username, phone, password, confirm_password]):
        return render(request, 'register.html', {'error_msg': '请填写完整信息'})

    if password != confirm_password:
        return render(request, 'register.html', {'error_msg': '两次密码不一致'})

    if len(phone) != 11:
        return render(request, 'register.html', {'error_msg': '手机号格式不正确'})

    # 验证手机号是否已注册
    if User.objects.filter(phone=phone).exists():
        return render(request, 'register.html', {'error_msg': '该手机号已注册'})

    # 创建新用户
    try:
        User.objects.create(
            username=username,
            phone=phone,
            password=encrypt_password(password)
        )
        return redirect(reverse('login'))
    except Exception as e:
        return render(request, 'register.html', {'error_msg': '注册失败，请稍后重试'})


def logout(request):
    """退出登录"""
    request.session.flush()
    return redirect(reverse('login'))


def index(request):
    """首页视图"""
    # 测试数据
    recommended_songs = [
        {
            'title': '告白气球',
            'artist': '周杰伦',
            'cover': 'https://via.placeholder.com/200x200?text=Music',  # 使用占位图
        },
        {
            'title': '光年之外',
            'artist': '邓紫棋',
            'cover': 'https://via.placeholder.com/200x200?text=Music',
        },
    ]

    hot_playlists = [
        {
            'title': '华语经典',
            'play_count': '100万',
            'cover': 'https://via.placeholder.com/200x200?text=Playlist',
        },
        {
            'title': '欧美热歌',
            'play_count': '80万',
            'cover': 'https://via.placeholder.com/200x200?text=Playlist',
        },
    ]

    hot_artists = [
        {
            'name': '周杰伦',
            'songs_count': 108,
            'avatar': 'https://via.placeholder.com/120x120?text=Artist',
        },
        {
            'name': '邓紫棋',
            'songs_count': 89,
            'avatar': 'https://via.placeholder.com/120x120?text=Artist',
        },
    ]

    context = {
        'recommended_songs': recommended_songs,
        'hot_playlists': hot_playlists,
        'hot_artists': hot_artists,
    }

    return render(request, 'index.html', context)


def profile(request):
    """个人中心视图"""
    # 检查用户是否登录
    if not request.session.get('user_id'):
        return redirect('login')

    # 获取用户信息
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    # 测试数据 - 收藏的歌曲
    favorite_songs = [
        {
            'title': '告白气球',
            'artist': '周杰伦',
            'cover': 'https://via.placeholder.com/60x60?text=Music',
        },
        {
            'title': '光年之外',
            'artist': '邓紫棋',
            'cover': 'https://via.placeholder.com/60x60?text=Music',
        },
    ]

    context = {
        'user': user,
        'favorite_songs': favorite_songs,
    }

    return render(request, 'profile.html', context)


def song_list(request):
    """歌曲列表页面"""
    songs = [
        {
            'title': '告白气球',
            'artist': '周杰伦',
            'duration': '03:35',
        },
        {
            'title': '光年之外',
            'artist': '邓紫棋',
            'duration': '03:42',
        },
        {
            'title': '起风了',
            'artist': '买辣椒也用券',
            'duration': '05:11',
        },
        {
            'title': '我和我的祖国',
            'artist': '王菲',
            'duration': '04:12',
        },
        {
            'title': '青花瓷',
            'artist': '周杰伦',
            'duration': '03:35',
        },
        {
            'title': '平凡之路',
            'artist': '朴树',
            'duration': '04:39',
        },
        {
            'title': '稻香',
            'artist': '周杰伦',
            'duration': '03:42',
        },
        {
            'title': '可惜没如果',
            'artist': '林俊杰',
            'duration': '04:21',
        },
    ]
    return render(request, 'song_list.html', {'songs': songs})


def playlist_list(request):
    """歌单列表页面"""
    playlists = [
        {
            'title': '华语经典',
            'creator': '音乐推荐',
            'play_count': '100万',
            'song_count': 100,
            'cover': 'https://via.placeholder.com/300x300?text=Playlist1',
        },
        {
            'title': '欧美热歌',
            'creator': '音乐推荐',
            'play_count': '80万',
            'song_count': 85,
            'cover': 'https://via.placeholder.com/300x300?text=Playlist2',
        },
        {
            'title': '流行音乐',
            'creator': '音乐推荐',
            'play_count': '60万',
            'song_count': 75,
            'cover': 'https://via.placeholder.com/300x300?text=Playlist3',
        },
    ]
    return render(request, 'playlist_list.html', {'playlists': playlists})


def artist_list(request):
    """歌手列表页面"""
    artists = [
        {
            'name': '周杰伦',
            'songs_count': 108,
            'fans_count': '1000万',
            'avatar': 'https://via.placeholder.com/300x300?text=Artist1',
        },
        {
            'name': '邓紫棋',
            'songs_count': 89,
            'fans_count': '800万',
            'avatar': 'https://via.placeholder.com/300x300?text=Artist2',
        },
        {
            'name': '林俊杰',
            'songs_count': 95,
            'fans_count': '900万',
            'avatar': 'https://via.placeholder.com/300x300?text=Artist3',
        },
    ]
    return render(request, 'artist_list.html', {'artists': artists})


def login_required(view_func):
    """登录验证装饰器"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, '请先登录')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def admin_dashboard(request):
    """管理后台首页"""
    return render(request, 'dashboard.html')


@login_required
def user_preference(request):
    """用户偏好设置"""
    user = User.objects.get(id=request.session['user_id'])
    
    if request.method == 'POST':
        favorite_artists = request.POST.get('favorite_artists', '')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        
        preference, _ = UserPreference.objects.get_or_create(user=user)
        preference.favorite_artists = favorite_artists
        preference.age = age
        preference.gender = gender
        preference.save()
        
        messages.success(request, '偏好设置已更新')
        return redirect('admin_dashboard')
    
    # 获取或创建用户偏好
    preference, _ = UserPreference.objects.get_or_create(user=user)
    return render(request, 'user_preference.html', {'preference': preference})


@login_required
def user_management(request):
    """用户管理"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # 添加用户
            username = request.POST.get('username')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            
            if User.objects.filter(phone=phone).exists():
                messages.error(request, '该手机号已被注册')
            else:
                User.objects.create(
                    username=username,
                    phone=phone,
                    password=encrypt_password(password)
                )
                messages.success(request, '用户添加成功')
            
        elif action == 'edit':
            # 编辑用户
            user_id = request.POST.get('user_id')
            username = request.POST.get('username')
            phone = request.POST.get('phone')
            
            if User.objects.exclude(id=user_id).filter(phone=phone).exists():
                messages.error(request, '该手机号已被其他用户使用')
            else:
                User.objects.filter(id=user_id).update(
                    username=username,
                    phone=phone
                )
                messages.success(request, '用户信息已更新')
    
    users = User.objects.all().order_by('-create_time')
    return render(request, 'user_management.html', {'users': users})


@login_required
def artist_management(request):
    """歌手管理"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # 添加歌手
            name = request.POST.get('name')
            introduction = request.POST.get('introduction')
            avatar = request.POST.get('avatar')
            popularity = request.POST.get('popularity', 0)
            
            Artist.objects.create(
                name=name,
                introduction=introduction,
                avatar=avatar,
                popularity=popularity
            )
            messages.success(request, '歌手添加成功')
            
        elif action == 'edit':
            # 编辑歌手
            artist_id = request.POST.get('artist_id')
            name = request.POST.get('name')
            introduction = request.POST.get('introduction')
            avatar = request.POST.get('avatar')
            popularity = request.POST.get('popularity')
            
            Artist.objects.filter(id=artist_id).update(
                name=name,
                introduction=introduction,
                avatar=avatar,
                popularity=popularity
            )
            messages.success(request, '歌手信息已更新')
    
    artists = Artist.objects.all().order_by('-popularity')
    return render(request, 'artist_management.html', {'artists': artists})


@login_required
def user_delete(request, user_id):
    """删除用户"""
    if request.method == 'POST':
        User.objects.filter(id=user_id).delete()
        messages.success(request, '用户已删除')
    return redirect('user_management')


@login_required
def artist_delete(request, artist_id):
    """删除歌手"""
    if request.method == 'POST':
        Artist.objects.filter(id=artist_id).delete()
        messages.success(request, '歌手已删除')
    return redirect('artist_management')


@login_required
def user_get(request, user_id):
    """获取用户信息"""
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'phone': user.phone,
            'is_admin': user.is_admin
        })
    except User.DoesNotExist:
        return JsonResponse({
            'error': '用户不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def artist_get(request, artist_id):
    """获取歌手信息"""
    try:
        artist = Artist.objects.get(id=artist_id)
        return JsonResponse({
            'id': artist.id,
            'name': artist.name,
            'introduction': artist.introduction,
            'avatar': artist.avatar,
            'popularity': artist.popularity
        })
    except Artist.DoesNotExist:
        return JsonResponse({'error': '歌手不存在'}, status=404)
