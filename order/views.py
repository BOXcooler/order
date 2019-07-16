from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from order.forms import CommentForm, UserForm
from .models import Post, Tag, Comment
from django.core.paginator import Paginator
from django.contrib.auth import logout

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderForm
        fields = ('order_list', 'cost', 'content')




def add_order(request, slug):
    order_list = get_object_or_404(Order, slug=slug)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'base.html', context={'tags': tags})


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'tag_detail.html', context={'tag': tag})


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


def logout_view(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page.


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'registration/registration.html',
                  {'user_form': user_form,
                   'registered': registered})



if order.created_on