from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo
from django.views.decorators.clickjacking import xframe_options_sameorigin


# 用户登录视图
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse('Wellcome You. You have been authenticated succesfully')
            else:
                return HttpResponse('Sorry. Your username or password is not right.')
        else:
            return HttpResponse('Invalid login')
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})

# 用户注册视图
def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        print(userprofile_form.is_valid())
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)  # 保存用户注册信息后，同时在userinfo表中写入该用户的id信息
            return HttpResponseRedirect(reverse('account:login'))
        else:
            return HttpResponse('Sorry, you can not register!')
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})

# 用户信息展示视图
@login_required(login_url='/account/login/') #最前面必须有/，否则重定向错误
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, 'account/myself.html',
                  {'user': user, 'userprofile': userprofile, 'userinfo': userinfo})


@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    print(request.method)
    if request.method=="POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid()*userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()

        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={'birth':userprofile.birth,
                                                    'phone':userprofile.phone})
        userinfo_form = UserInfoForm(initial={'company':userinfo.company,
                                              'school':userinfo.school,
                                              'profession':userinfo.profession,
                                              'address':userinfo.address,
                                              'aboutme':userinfo.aboutme})
        return render(request, 'account/myself_edit.html',
                      {'user_form': user_form,
                       'userprofile_form': userprofile_form,
                       'userinfo_form': userinfo_form})

@xframe_options_sameorigin  # 告诉中间件在该视图frame中可以展示同域名网页
@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        user_info = UserInfo.objects.get(user=request.user.id)
        user_info.image = img
        user_info.save()
        return HttpResponse('1')
    else:
        return render(request, 'account/imagecrop.html')