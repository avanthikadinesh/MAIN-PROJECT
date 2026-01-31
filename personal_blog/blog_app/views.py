from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.db.models import Count
from .models import Category
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post,Like,SavedPost
from personal_app.models import Profile
from blog_app.models import Notification

def blog_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', 'All')

    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    if search_query:
        posts = posts.filter(title__icontains=search_query)

    if category_id and category_id != "All":
        posts = posts.filter(category_id=category_id)

    return render(request, 'blog_list.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query
    })




@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        
        like.delete()

    return redirect('post_detail', post_id=post.id)

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   
            post.save()
            return redirect("blog_list")
    else:
        form = PostForm()

    return render(request, "add_post.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # security: only author can edit
    if post.author != request.user:
        return redirect('blog_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('blog_list')

    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')

    return render(request, 'delete_post.html', {'post': post})



@login_required(login_url='login')
def dashboard(request):
    total_posts = Post.objects.count()
    my_posts = Post.objects.filter(author=request.user).count()
    total_comments = Post.objects.annotate(
        comment_count=Count('comments')
    ).aggregate(total=Count('comment_count'))['total']

    recent_posts = Post.objects.filter(author=request.user).order_by('-created_at')[:5]

    context = {
        'total_posts': total_posts,
        'my_posts': my_posts,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
    }

    return render(request, 'dashboard.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'delete_post.html', {'post': post})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST.get('content')  

        if text:
            Comment.objects.create(
                post=post,
                user=request.user,   
                text=text            
            )
            return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user:
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', post_id=post_id)

    return redirect('post_detail', post_id=comment.post.id)


def blog_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    if category_id:
        posts = posts.filter(category_id=category_id)

    return render(request, 'blog_list.html', {
        'posts': posts,
        'categories': categories
    })

def author_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile  

    followers = profile.followers.all()  
    following = User.objects.filter(profile__followers=profile_user)  

    is_following = False
    if request.user.is_authenticated:
        is_following = request.user in followers

    return render(request, 'author_profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': profile_user.post_set.all(),
        'followers_count': followers.count(),
        'following_count': following.count(),
        'is_following': is_following,
    })


@login_required
def toggle_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile

    if request.user != profile_user:
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)  
        else:
            profile.followers.add(request.user)     

    return redirect('author_profile', username=username)



@login_required
def follow_author(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = user_to_follow.profile  

    if request.user != user_to_follow:
        
        profile.followers.add(request.user)

    return redirect('author_profile', username=username)


@login_required
def unfollow_author(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    profile = user_to_unfollow.profile  
    profile.followers.remove(request.user)

    return redirect('author_profile', username=username)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('author_profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    users = user.profile.followers.all()

    return render(request, 'follow_list.html', {
        'title': 'Followers',
        'users': users,
        'profile_user': user,
    })


def following_list(request, username):
    user = get_object_or_404(User, username=username)
    users = User.objects.filter(profile__followers=user)

    return render(request, 'follow_list.html', {
        'title': 'Following',
        'users': users,
        'profile_user': user,
    })    

@login_required
def toggle_save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    saved = SavedPost.objects.filter(user=request.user, post=post)
    if saved.exists():
        saved.delete()
    else:
        SavedPost.objects.create(user=request.user, post=post)

    return redirect(request.META.get('HTTP_REFERER', 'blog_list'))

    
@login_required
def saved_posts(request):
    posts = Post.objects.filter(savedpost__user=request.user)
    return render(request, 'saved_posts.html', {'posts': posts})



def notify_followers(post):
    author_profile = post.author.profile
    followers = author_profile.followers.all()

    for follower in followers:
        Notification.objects.create(
            user=follower,
            from_user=post.author,
            message=f"{post.author.username} posted a new blog",
            link=f"/blog/post/{post.id}/"
        )

@login_required
def notifications_view(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'notifications.html', {
        'notifications': notifications
    })       