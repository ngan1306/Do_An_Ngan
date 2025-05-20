from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('novels:novel_list')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('novels:novel_list')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('novels:novel_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.bio = request.POST.get('bio', '')
        user.birth_date = request.POST.get('birth_date')
        user.gender = request.POST.get('gender')
        user.location = request.POST.get('location', '')
        user.website = request.POST.get('website', '')
        user.save()
        messages.success(request, 'Thông tin cá nhân đã được cập nhật thành công!')
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html', {'user': request.user}) 