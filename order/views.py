from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.mail import send_mail
from django.template import RequestContext

from .forms import OrderForm, OrderString
from .models import Order


def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('list_view')
        else:
            return redirect('order_view')
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def add_order(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.author = request.user
                new_order.save()
                if new_order.created_on.hour in (13, 14):
                    send_mail('Order between 13:00 and 15:00',
                              'Order was created on {} by user {}'.format(new_order.created_on.isoformat(),
                                                                          new_order.author.username),
                              'project-for-order@yandex.ru', [x.email for x in User.objects.filter(is_staff=True)])
                    print('!!!INFO!!! will send email to staff')
                return render(request, 'thanks_for_order.html')
        return render(request, 'order.html',
                      {'form': OrderForm(use_required_attribute=False), 'labels': OrderForm.Meta.labels})
    return redirect('home_view')


def order_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            form = OrderString(request.POST)
            if form.is_valid():
                c = get_object_or_404(Order, slug=form.cleaned_data['slug'])
                if form.cleaned_data['action'] == 'Update':
                    c.order_item = form.cleaned_data['order_item']
                    c.cost = form.cleaned_data['cost']
                    c.comment = ''.join(form.cleaned_data['comment'])
                    send_mail('Changes on order', 'your order was updated', 'project-for-order@yandex.ru',
                              [c.author.email, ])
                    print('!!!INFO!!! send message to {} as order updated'.format(c.author.email))
                    c.save()
                elif form.cleaned_data['action'] == 'Delete':
                    send_mail('Changes on order', 'your order was deleted', 'project-for-order@yandex.ru',
                              [c.author.email, ])
                    print('!!!INFO!!! send message to {} as order deleted'.format(c.author.email))
                    c.delete()
        orders = Order.objects.all()
        total_cost = orders.aggregate(Sum('cost'))['cost__sum']
        return render(request, 'orderlist.html', {'orders': orders, 'total_cost': total_cost})
    return redirect('home_view')


def e_handler404(request, exception):
    context = RequestContext(request)
    response = render_to_response('404.html', context)
    response.status_code = 404
    return response
