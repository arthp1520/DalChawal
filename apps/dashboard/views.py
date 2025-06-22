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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Document
from .models import User, Post, Document  # ✅ Make sure Document is added here

from django.shortcuts import render, get_object_or_404, redirect
from .models import Document  
from django.contrib import messages 

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
            return render(request, 'dashboard/sign_in.html', {'error': "User Does Not exist"})
            # return redirect('sign_in') it was commented while we want to show message on front

        if not user.is_active:
            print("Account not verified")
            return render(request, 'dashboard/sign_in.html', {'error': "Your Account is not verified"})
            # return redirect('sign_in')it was commented while we want to show message on front

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect('index')
        else:
            print("Wrong password")
            return render(request, 'dashboard/sign_in.html', {'error': "Wrong Password Please Try Again"})
            # return redirect('sign_in')it was commented while we want to show message on front
            # return redirect('index')
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
            return render(request, 'dashboard/sign_up.html', {'error': "Provide Valid Mail id"})
            # return redirect('sign_up')it was commented while we want to show message on front
            
        if User.objects.filter(email=email_).exists():
            print(request, "Email already exists")
            return render(request, 'dashboard/sign_up.html', {'error': "Email Already exist please Login"})
            # return redirect('sign_up')it was commented while we want to show message on front

        if not is_valid_mobile_number(mobile_):
            messages.error(request, "Invalid mobile number")
            return render(request, 'dashboard/sign_up.html', {'error': "please provide +91 "})
            # return redirect('sign_up')it was commented while we want to show message on front

        if User.objects.filter(mobile=mobile_).exists():
            messages.error(request, "Mobile already exists")
            return render(request, 'dashboard/sign_up.html', {'error': "Mobile Already Exist"})
            # return redirect('sign_up')it was commented while we want to show message on front

        if password_ != confirm_password_:
            messages.error(request, "Passwords do not match")
            return render(request, 'dashboard/sign_up.html', {'error': "Password Does Not Match"})
            # return redirect('sign_up')it was commented while we want to show message on front
        
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
        user = User.objects.filter(email=email_).first()
        print(user.email)
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
            print(user.email) # this part shows the euser mail id to pass in html form
            context = {
            'email' : user.email, #this passes the user mail id
            'email': email_ #this passes admin  mail id (agrearth22@gmail.com)
            }
            return render(request, 'dashboard/email_verify.html', context)

        
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
    user = User.objects.get(id=request.session['user_id']) 
    messages.success(request, f"{user.name}, you have successfully logged out from ParaDox. Keep Learning! ✌️🤞", extra_tags='logout')
    del request.session['user_id']
    print("Now, you are logged Out")
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
@login_required
def index(request):
    query = request.GET.get('query')
    user_id = request.session.get('user_id')
    current_user = User.objects.get(id=user_id)

    if query:
        users = User.objects.filter(name__icontains=query).exclude(id=user_id)
    else:
        users = User.objects.exclude(id=user_id)

    return render(request, 'dashboard/index.html', {
        'users': users,
        'current_user': current_user
    })

@login_required
def public_profile(request, user_id):
    user_profile = User.objects.get(id=user_id)
    documents = Document.objects.filter(user=user_profile).order_by('-uploaded_at')

    followers_count = user_profile.followers.count()
    following_count = user_profile.following.count()

    return render(request, 'dashboard/public_profile.html', {
        'user_profile': user_profile,
        'documents': documents,
        'followers_count': followers_count,
        'following_count': following_count
    })

@login_required
def toggle_follow(request, user_id):
    current_user = User.objects.get(id=request.session['user_id'])
    target_user = User.objects.get(id=user_id)

    if target_user in current_user.following.all():
        current_user.following.remove(target_user)
    else:
        current_user.following.add(target_user)

    return redirect('index')

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
def update_document(request, doc_id):
    document = Document.objects.get(id=doc_id)

    if request.method == 'POST':
        document.title = request.POST.get('title')
        document.description = request.POST.get('description')

        if request.FILES.get('document'):
            document.file = request.FILES['document']
        
        document.save()
        return redirect('profile')  # or wherever you want to redirect

    return render(request, 'dashboard/update_document.html', {'document': document})



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
    user_id = request.session.get('user_id')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('sign_in')

    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')

        Document.objects.create(
            user=user,
            file=uploaded_file,
            title=title,
            description=description
        )
        messages.success(request, "Document uploaded successfully.")

    uploaded_docs = Document.objects.filter(user=user).order_by('-uploaded_at')
    followers_count = user.followers.count()
    following_count = user.following.count()

    return render(request, 'dashboard/profile.html', {
        'user': user,
        'uploaded_docs': uploaded_docs,
        'followers_count': followers_count,
        'following_count': following_count
    })


            
   


@login_required
def edit_profile(request):
    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')

        user.name = name
        user.bio = bio
        user.save()

        return redirect('profile')

    return render(request, 'dashboard/edit_profile.html', {'user': user})


def delete_document(request, doc_id):
    user_id = request.session.get('user_id')
    try:
        document = Document.objects.get(id=doc_id, user_id=user_id)
        document.file.delete()  # Delete the file from media folder
        document.delete()       # Delete the DB record
        messages.success(request, "Document deleted successfully.")
    except Document.DoesNotExist:
        messages.error(request, "Document not found or not authorized.")
    
    return redirect('profile')

