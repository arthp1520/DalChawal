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
from django.contrib import messages

#for forgot pass
from django.contrib.auth.models import User  # Or your custom user model



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
    print("here....1")
    if request.method == 'POST':
        print("here....2")
        name_= request.POST['name']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']
        
        if not  is_email_verified:
            print("Invalid Email")
            return redirect('sign_up')
            
        if User.objects.filter(email=email_).exists():
            print(request, "Email already exists")
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
        
        if not is_valid_password(password_)[0]:
            print(is_valid_password(password_)[1])
            return redirect('signu_up')
        
        
        print(make_password(password_),'-------')
        
        print("here....3")

        user = User.objects.create(
            name=name_,
            email=email_,
            mobile=mobile_,
            password=make_password(password_),
        )
        user.save()
        otp_ = random.randint(111111, 999999)
        print("here....4")
        subject = "Email Confirmation mail | ParaDox"
        message = f"Welcome to ParaDox, {name_}! Your OTP is: {otp_}. Keep learning and sharing your Dox 👍"

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [f"{email_}"]
        send_mail(subject, message, from_email, recipient_list)
        user.otp=otp_
        user.save()  
        print("Email Sent check your Mail Acount")
        context = {
            'email': email_
             }
        return render(request,'dashboard/email_verify.html', context)
        
    return render(request, 'dashboard/sign_up.html')

def email_verify(request):
    print("e1----")
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']
        print("e1----el")

        if not User.objects.filter(email=email_).exists():
            messages.info(request, "email doesnot exists")
            print("e1----e1----e1---e1")
            return render(request, 'dashboard/email_verify.html', {'email' : email_})

        
        user = User.objects.get(email=email_)
      
        if int(otp_) == int(user.otp):
            user.is_active = True
            print("e2----")
            user.save()
            return redirect('sign_in')
        messages.error(request,"Invalid OTP")
        return render(request, 'dashboard/sign_in.html', {'email' : email_})
       
        
    
    return render(request, 'dashboard/email_verify.html')

def logout(request):
    del request.session['user_id']
    print("Now, you are logged Out")
    messages.success(request,"You are Logout From ParaDox")
    return redirect('sign_in')

def forgot_password(request):
    # message = ""
    
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     try:
    #         user = User.objects.get(email=email)
    #         # WARNING: This assumes password is stored in plaintext (NOT recommended)
    #         send_mail(
    #             subject='Your Password Recovery',
    #             message=f'Hello {user.name}, your password is: {user.password}',
    #             from_email=settings.DEFAULT_FROM_EMAIL,
    #             recipient_list=[email],
    #             fail_silently=False,
    #         )
    #         message = "Password sent to your email."
    #     except User.DoesNotExist:
    #         message = "No user found with this email."
    
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
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('sign_in')  # Or your login view name

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('sign_in')

    return render(request, 'dashboard/profile.html', {'user': user})



def edit_profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        occupation = request.POST['occupation']
        profile_image = request.FILES.get('profile_image')
        # Update logic here if using request.user
        return redirect('profile')

    return render(request, 'dashboard/edit_profile.html')