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
from .models import Post
# Create your views here.
# def index(request):
#     return render(request, 'dashboard/index.html')


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