# from django.shortcuts import render

# # def index(request):
# #     return render(request, 'dashboard/index.html')

# # from django.shortcuts import render

# # # Create your views here.
# # def index(request):
# #     return render(request,'dashboard/index.html')
# def show(request):
#     return render(request, 'dashboard/show.html')
                  
# def insert(request):

#     return render(request, 'dashboard/insert.html')                

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from functools import wraps
from .models import User
from .helpers import is_valid_mobile_number, is_valid_password

# from .helpers import *

import random

# Create your views here.

def sign_in(request):
    return render(request, 'dashboard/sign_in.html')

def sign_up(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        # Remove this line: if not is_email_verified:

        if User.objects.filter(email=email_).exists():
            print("Email already exists")
            return redirect('sign_up')
        
        if not is_valid_mobile_number(mobile_):
            print("Invalid mobile number")
            return redirect('sign_up')
        
        if User.objects.filter(mobile=mobile_).exists():
            print("Mobile already exists")
            return redirect('sign_up')
        
        if password_ != confirm_password_:
            print("Passwords do not match")
            return redirect('sign_up')
        
        is_valid, message = is_valid_password(password_)
        if not is_valid:
            print(message)
            return redirect('sign_up')
        
        # Create User but mark as inactive until OTP is verified
        new_User = User.objects.create(
            email=email_,
            mobile=mobile_,
            password=make_password(password_),
            is_active=False  # assuming this field exists
        )

        # Generate and save OTP
        otp = random.randint(111111, 999999)
        new_User.otp = otp
        new_User.save()

        # Send email with OTP
        subject = "Email Confirmation | Workbook"
        message = f"""
Hello,

Thank you for registering with Workbook.

Your One-Time Password (OTP) for email verification is: {otp}

Enter this OTP to complete your registration.

If you did not initiate this request, you can ignore this email.

— Workbook Team
"""
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email_])

        print("Registration successful. OTP sent.")
        return render(request, 'dashboard/email_verify.html', {'email': email_})

    return render(request, 'dashboard/sign_up.html')

def forgot_password(request):
    return render(request, 'dashboard/forgot_password.html')

def email_verify(request):
    if request.method == 'POST':
        email_ = request.POST.get('email')
        otp_ = request.POST.get('otp')

        try:
            get_labour = User.objects.get(email=email_)
        except User.DoesNotExist:
            messages.error(request, "Email does not exist.")
            return redirect('sign_up')  # or show error page

        if otp_ != get_labour.otp:
            messages.error(request, "Invalid OTP. Please try again.")
            context = {'email': email_}
            return render(request, 'dashboard/email_verify.html', context)

        get_labour.is_active = True
        get_labour.save()
        messages.success(request, "Email verified successfully.")
        return redirect('sign_in')

    return render(request, 'dashboard/email_verify.html')

def index(request):
    return render(request, 'dashboard/index.html')


def show(request):
    # posts = Post.objects.all().order_by('-id')[:2]
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request, 'dashboard/show.html', context)

def insert(request):
    if request.method == 'POST':
        image_ = request.FILES['post_image']
        title_ = request.POST['title']
        content_ = request.POST['content']

        new_post = Post.objects.create(
            image = image_,
            title = title_,
            content = content_
        )
        new_post.save()

    return render(request, 'dashboard/insert.html')

def update_post(request, post_id):
    update_data = Post.objects.get(id=post_id)
    if request.method == 'POST':
        if request.FILES:
            update_data.image = request.FILES['post_image']

        update_data.title = request.POST['title']
        update_data.content = request.POST['content']
        update_data.save()
        return redirect('show')

    context = {
        'post': update_data
    }
    return render(request, 'dashboard/update.html', context)

def delete_post(request, post_id):
    delete_post = Post.objects.get(id=post_id)
    delete_post.delete()
    return redirect('show')

def profile(request):
     return render(request, 'dashboard/profile.html')

def edit_profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        occupation = request.POST['occupation']
        profile_image = request.FILES.get('profile_image')
        # Save data to your model here...
        return redirect('profile')
    return render(request, 'dashboard/edit_profile.html')
