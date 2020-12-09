from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth
from admin.models import *

# Create your views here.

def login_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            print("인증")
            login(request, user)
            return redirect('honssauser:main')
        else:
            print("실패")
            return redirect('user:login')

    return render(request,  "user/login.html")

def logout_view(request):
    logout(request)
    return redirect("user:login")

def signup_view(request):

    if request.method == 'POST':
        # if member_tbl.object.filter(member_id = user_id).exists:
        #     print('중복아님')
            if request.POST['password'] == request.POST['password2']:
                print(request.POST)
                username = request.POST['username']
                useremail = request.POST['useremail']
                user_id = request.POST['user_id']
                password = request.POST['password']
                hpon = request.POST['hpon']

                print(request.POST)
                New_data = member_tbl(
                    member_name = username,
                    member_email = useremail,
                    member_id = user_id,
                    member_password = password,
                    member_contact_number = hpon,
                )
                users = User.objects.create_user(user_id, useremail, password)
                users.last_name = 'x'
                users.first_name = 'x'
                users.save()
                New_data.save()
                return redirect("user:login")
                # return render("user:login")
            else:
                print('패스워드 틀림')
        # else:
        #     print('중복')
    return render(request, "user/signup.html")

def find_id(request):
    member = []
    msg = ''
    if request.method == 'POST':
        member = member_tbl.objects.filter(member_name=request.POST['username'], member_email=request.POST['useremail'])
        if member:
            member = member[0]
        else:
            msg = '이름 혹은 이메일이 일치하지 않습니다.'
    print(request.POST)
    content = {'member': member, 'msg': msg}
    return render(request, 'user/find_id.html', content)

def find_password(request):
    member = []
    msg = ''
    if request.method == 'POST':
        member = member_tbl.objects.filter(member_id = request.POST['username'], member_email=request.POST['useremail'])
        if member:
            member = member[0]
        else:
            msg = '아이디 혹은 이메일이 일치하지 않습니다.'
    content = {'member': member, 'msg': msg}
    return render(request, 'user/find_password.html', content)