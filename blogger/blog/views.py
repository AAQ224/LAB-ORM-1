from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    return render(request, "blog/home.html", {"posts": posts})

def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        is_published = request.POST.get("is_published") == "on"
        image = request.FILES.get("image")
        Post.objects.create(
            title=title,
            content=content,
            is_published=is_published,
            image=image
        )
        return redirect("blog:home")
    return render(request, "blog/add_post.html")

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {"post": post})

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.is_published = request.POST.get("is_published") == "on"
        image = request.FILES.get("image")
        if image:
            post.image = image
        post.save()
        return redirect("blog:post_detail", post_id=post.id)
    return render(request, "blog/edit_post.html", {"post": post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:home")
    return render(request, "blog/delete_post.html", {"post": post})

def drafts(request):
    posts = Post.objects.filter(is_published=False).order_by('-published_at')
    return render(request, "blog/drafts.html", {"posts": posts})

