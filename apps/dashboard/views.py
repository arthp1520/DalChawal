from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User, Post  # Ensure both models exist
from .helpers import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.conf import settings
import random
from functools import wraps
# from django.contrib.auth.models import User
from .models import User  # or from apps.dashboard.models import User


# ================================
# USER AUTHENTICATION VIEWS
# ================================

from django.contrib.auth import authenticate, login  # Make sure these are imported
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import User  # your custom model
from django.contrib.auth.hashers import check_password

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('sign_in')  # redirect to login page
        return view_func(request, *args, **kwargs)
    return wrapper

def sign_in(request):
    if request.method == 'POST':
        email_ = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email_)
        except User.DoesNotExist:
            print("User does not exist")
            return redirect('sign_in')

        if not user.is_active:
            print("Account not verified")
            return redirect('sign_in')

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect('index')
        else:
            print("Wrong password")
            return redirect('sign_in')
    #return redirect('index')
    return render(request, 'dashboard/sign_in.html')

    

def sign_up(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        if User.objects.filter(email=email_).exists():
            messages.error(request, "Email already exists")
            return redirect('sign_up')

        if not is_valid_mobile_number(mobile_):
            messages.error(request, "Invalid mobile number")
            return redirect('sign_up')

        if User.objects.filter(mobile=mobile_).exists():
            messages.error(request, "Mobile already exists")
            return redirect('sign_up')

        if password_ != confirm_password_:
            messages.error(request, "Passwords do not match")
            return redirect('sign_up')

        is_valid = is_valid_password(password_)
        if not is_valid:
            messages.error(request,"not valid pass")
            return redirect('sign_up')

        otp_ = random.randint(111111, 999999)

        user = User(
            email=email_,
            mobile=mobile_,
            password=make_password(password_),
            otp=otp_,
            is_active=False  # False until OTP verified
        )

        subject = "Email Confirmation mail | ParaDox"
        message = f"welcome to ParDox your OTP is | {otp_} , Keep learning and Sharing your Dox 👍"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_]

        if send_mail(subject, message, from_email, recipient_list):
            print("Email Sent")
            user.save()  
            context = {
                'email': email_
            }
            return render(request,'dashboard/email_verify.html', context)
            # return redirect(f"/email_verify/&email={user.email}")
        
    return render(request, 'dashboard/sign_up.html')

@login_required
def email_verify(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']

        user = User.objects.get(email=email_)
        

        if str(otp_) != str(user.otp):
            messages.error(request, "Invalid OTP")
            return render(request, 'dashboard/email_verify.html', {'email': email_})

        user.is_active = True
        user.save()
        messages.success(request, "Email verified! Please log in.")
        return redirect('sign_in')

    #  This line is needed for initial page load (GET request)
    return render(request, 'dashboard/email_verify.html')

def logout(request):
    del request.session['user_id']
    print("Now, you are logged Out")
    messages.success(request,"You are Logout From ParaDox")
    return redirect('sign_in')

@login_required
def forgot_password(request):
    return render(request, 'dashboard/forgot_password.html')


# ================================
# DASHBOARD VIEWS
# ================================
@login_required
def index(request):
    return render(request, 'dashboard/index.html')

@login_required
def show(request):
    posts = Post.objects.all()
    return render(request, 'dashboard/show.html', {'posts': posts})

@login_required
def insert(request):
    if request.method == 'POST':
        image_ = request.FILES['post_image']
        title_ = request.POST['title']
        content_ = request.POST['content']

        Post.objects.create(
            image=image_,
            title=title_,
            content=content_
        )
        return redirect('show')

    return render(request, 'dashboard/insert.html')

@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        if request.FILES.get('post_image'):
            post.image = request.FILES['post_image']
        post.save()
        return redirect('show')

    return render(request, 'dashboard/update.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('show')


# ================================
# PROFILE VIEWS
# ================================
@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        occupation = request.POST['occupation']
        profile_image = request.FILES.get('profile_image')
        # Update logic here if using request.user
        return redirect('profile')

    return render(request, 'dashboard/edit_profile.html')