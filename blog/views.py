from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, PostImage, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.http import HttpResponseForbidden

# 1. ЛИСТА НА ПОСТОВИ СО ЖИВО ПРЕБАРУВАЊЕ И КОМЕНТАРИ
def post_list(request):
    # Зачувување коментар доколку има POST барање од почетна страница
    if request.method == "POST" and 'post_id' in request.POST:
        # Правиме копија и сами му допишуваме "Анонимен корисник" бидејќи го тргнавме полето од HTML
        data = request.POST.copy()
        if not data.get('author'):
            data['author'] = "Анонимен корисник"

        form = CommentForm(data)
        post_id = request.POST.get('post_id')
        if form.is_valid() and post_id:
            post = get_object_or_404(Post, pk=post_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_list')

    # Логика за пребарување
    query = request.GET.get('search', '')
    if query:
        query = query.strip()

    if query:
        posts = Post.objects.filter(
            models.Q(title__icontains=query) | models.Q(text__icontains=query)
        ).order_by('-published_date')
    else:
        posts = Post.objects.all().order_by('-published_date')
        
    comment_form = CommentForm()
    return render(request, 'blog/post_list.html', {
        'posts': posts, 
        'query': query, 
        'comment_form': comment_form
    })

# 2. ПРЕГЛЕД НА СЕКОЈ ПОСТ ПОЕДИНЕЧНО
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # Исто и тука правиме копија за да работи анонимно и на внатрешната страна
        data = request.POST.copy()
        if not data.get('author'):
            data['author'] = "Анонимен корисник"

        form = CommentForm(data)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

# 3. НОВ ПОСТ
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            files = request.FILES.getlist('extra_images')
            for f in files:
                PostImage.objects.create(post=post, image=f)

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# 4. РЕГИСТРАЦИЈА
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# 5. ИЗМЕНА НА ПОСТ
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # СИГУРНОСНА ПРОВЕРКА: Ако корисникот не е авторот и не е супер-администратор, му забрануваме пристап
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("Немаш дозвола да ја менуваш оваа пријава!")
        
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})