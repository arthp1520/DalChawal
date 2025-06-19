from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User, Post  # Ensure both models exist
from .helpers import *
from django.core.mail import send_mail
from django.conf import settings
import random


# ================================
# USER AUTHENTICATION VIEWS
# ================================

def sign_in(request):
    return render(request, 'dashboard/sign_in.html')


def sign_up(request):
    if request.method == 'POST':
        email_ = request.POST.gets('email')
        mobile_ = request.POST.get('mobile')
        password_ = request.POST.ge('password')
        confirm_password_ = request.POST.get('confirm_password')

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

        is_valid, message = is_valid_password(password_, message)
        if not is_valid:
            messages.error(request, message)
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
            user.save()  # ✅ FIXED
            context = {
                'email': email_
            }
            return redirect(request, 'dashboard/email_verify.html', context)

        messages.success(request, "Account created successfully. Please sign in.")
        return redirect('email_verify')

    return render(request, 'dashboard/sign_up.html')
def sign_up(request):
    if request.method == 'POST':
        email_ = request.POST.get('email')
        # 
        mobile_ = request.POST.get('mobile') 

        password_ = request.POST.get('password')
        confirm_password_ = request.POST.get('confirm_password')

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
            messages.error(request, message)
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
        message = f"OTP | {otp_}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_]

        if send_mail(subject, message, from_email, recipient_list):
            print("Email  Sent")
            user.save()
            context = {
                'email': email_
            }
            return render(request, 'dashboard/email_verify.html', context)

        messages.success(request, "Account created successfully. Please sign in.")
        return redirect('email_verify')

    return render(request, 'dashboard/sign_up.html')


def forgot_password(request):
    return render(request, 'dashboard/forgot_password.html')


# ================================
# DASHBOARD VIEWS
# ================================

def index(request):
    return render(request, 'dashboard/index.html')


def show(request):
    posts = Post.objects.all()
    return render(request, 'dashboard/show.html', {'posts': posts})


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


def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('show')


# ================================
# PROFILE VIEWS
# ================================

def profile(request):
    return render(request, 'dashboard/profile.html')


def edit_profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        occupation = request.POST['occupation']
        profile_image = request.FILES.get('profile_image')
        # Update logic here if using request.user
        return redirect('profile')

    return render(request, 'dashboard/edit_profile.html')
