from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail

from .forms import OrderForm, OrderString
from .models import Order
def home_view(request):
    pass


def logout_view(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page.


def add_order(request):
    pass

def add_order(request):
    if request.user.is_authenticated and not request.user.is_staff:
        # if request.user.is_staff:
        #     template = 'orderlist.html'
        # else:
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.author = request.user
                new_order.save()
                # print(new_order.created_on.hour)
                if new_order.created_on.hour in (13, 14):
                    send_mail('Order between 13:00 and 15:00', 'Order was created on {} by user {}'.format(new_order.created_on.isoformat(),new_order.author.username), 'noreply@localho.st', [x.email for x in User.objects.filter(is_staff=True)])
                    # print([x.email for x in User.objects.filter(is_staff=True)])
                    print('!!!INFO!!! will send email to staff')
                return redirect('order_view')  # редиректим на страницу заказа
        return render(request, 'order.html', {'form': OrderForm()})
    return redirect('home_view')







