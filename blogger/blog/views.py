from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post

def home(request):
    posts_qs = Post.objects.filter(is_published=True).order_by("-published_at")
    q = request.GET.get("q", "").strip()
    if q:
        posts_qs = posts_qs.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )
    order = request.GET.get("order", "")
    if order == "oldest":
        posts_qs = posts_qs.order_by("published_at")
    elif order == "title":
        posts_qs = posts_qs.order_by("title")
    posts = posts_qs[:10]
    total_posts = Post.objects.filter(is_published=True).count()
    drafts_count = Post.objects.filter(is_published=False).count()
    context = {
        "posts": posts,
        "q": q,
        "order": order,
        "total_posts": total_posts,
        "drafts_count": drafts_count,
    }
    return render(request, "blog/home.html", context)

def drafts(request):
    posts = Post.objects.filter(is_published=False).order_by("-published_at")
    drafts_count = posts.count()
    total_posts = Post.objects.filter(is_published=True).count()
    context = {
        "posts": posts,
        "drafts_count": drafts_count,
        "total_posts": total_posts,
    }
    return render(request, "blog/drafts.html", context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    total_posts = Post.objects.filter(is_published=True).count()
    drafts_count = Post.objects.filter(is_published=False).count()
    context = {
        "post": post,
        "total_posts": total_posts,
        "drafts_count": drafts_count,
    }
    return render(request, "blog/post_detail.html", context)

def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        is_published = request.POST.get("is_published") == "on"
        image = request.FILES.get("image")
        post = Post(
            title=title,
            content=content,
            is_published=is_published,
            image=image,
        )
        post.save()
        return redirect("blog:home")
    total_posts = Post.objects.filter(is_published=True).count()
    drafts_count = Post.objects.filter(is_published=False).count()
    context = {
        "total_posts": total_posts,
        "drafts_count": drafts_count,
    }
    return render(request, "blog/add_post.html", context)

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
    total_posts = Post.objects.filter(is_published=True).count()
    drafts_count = Post.objects.filter(is_published=False).count()
    context = {
        "post": post,
        "total_posts": total_posts,
        "drafts_count": drafts_count,
    }
    return render(request, "blog/edit_post.html", context)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:home")
    total_posts = Post.objects.filter(is_published=True).count()
    drafts_count = Post.objects.filter(is_published=False).count()
    context = {
        "post": post,
        "total_posts": total_posts,
        "drafts_count": drafts_count,
    }
    return render(request, "blog/delete_post.html", context)
