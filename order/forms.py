from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_item', 'cost', 'comment')
        labels = { 'order_item':'Ваш заказ', 'cost':'Стоимость', 'comment':'Комментарий' }


class OrderString(forms.Form):
    slug = forms.SlugField()
    order_item = forms.CharField(max_length=200)
    cost = forms.DecimalField()
    comment = forms.CharField()
    action = forms.CharField()