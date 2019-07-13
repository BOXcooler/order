from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from order.forms import OrderForm
from .models import Order
from django.core.paginator import Paginator
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page.




def add_order(request):
    username = None
    email = ''
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.author = request.user
            new_order.save()
            if new_order.created_on.hour in (13,14):
                print('!!!INFO!!! will send email to admin',new_order.created_on)
            return redirect('order.html') # редиректим на страницу заказа
    else:
        form =OrderForm()
    return render(request, 'order.html', {'form': form})




def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})



