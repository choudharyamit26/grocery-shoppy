from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, TemplateView, CreateView, ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, AddressForm
from .models import User, Category, Product, Order, SpecialOfferProduct, Payment

user = get_user_model()


class HomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        nuts = Product.objects.filter(category__category_name='Nuts')
        oil = Product.objects.filter(category__category_name='Oil')
        pasta = Product.objects.filter(category__category_name='Pasta & Noodles')
        spl = SpecialOfferProduct.objects.all()
        return render(self.request, 'index.html',
                      {'categories': categories, 'nuts': nuts, 'oil': oil, 'pasta': pasta, 'spl': spl})

    def post(self, request, *args, **kwargs):

        name = self.request.POST.get('name' or None)
        email = self.request.POST.get('email' or None)
        password = self.request.POST.get('password' or None)
        confirm_password = self.request.POST.get('confirm_password' or None)
        if name and email and password and confirm_password:
            if password != confirm_password:
                messages.info(self.request, 'Password and Confirm password did not match')
                return redirect(self.request.path_info)
            else:
                user_obj = User.objects.create(
                    name=name,
                    email=email
                )
                user_obj.set_password(password)
                user_obj.save()
        else:
            try:
                user_object = user.objects.get(email=email)
                if user_object.check_password(password):
                    login(self.request, user_object)
                    messages.success(self.request, 'Logged in successfully')
                    return redirect('src:home')
                else:
                    messages.error(self.request, "Incorrect Password")
                    # return render(request, 'login.html', {"status": 400})
                    return redirect(self.request.path_info)
            except Exception as e:
                print(e)
                messages.error(self.request, "User doesn't exists. Please sign up")
                return redirect(self.request.path_info)
        return redirect('src:home')


class AboutUs(TemplateView):
    template_name = 'about.html'

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        name = self.request.POST.get('name' or None)
        email = self.request.POST.get('email' or None)
        password = self.request.POST.get('password' or None)
        confirm_password = self.request.POST.get('confirm_password' or None)
        if name and email and password and confirm_password:
            if password != confirm_password:
                messages.info(self.request, 'Password and Confirm password did not match')
                return redirect(self.request.path_info)
            else:
                user_obj = User.objects.create(
                    name=name,
                    email=email
                )
                user_obj.set_password(password)
                user_obj.save()
        else:
            try:
                user_object = user.objects.get(email=email)
                if user_object.check_password(password):
                    login(self.request, user_object)
                    messages.success(self.request, 'Logged in successfully')
                    return redirect('src:home')
                else:
                    messages.error(self.request, "Incorrect Password")
                    # return render(request, 'login.html', {"status": 400})
                    return redirect(self.request.path_info)
            except Exception as e:
                print(e)
                messages.error(self.request, "User doesn't exists. Please sign up")
                return redirect(self.request.path_info)
        return redirect('src:home')


class SignUpView(CreateView):
    model = User
    template_name = 'base.html'
    success_url = 'src:home'
    form_class = SignUpForm


class ContactView(TemplateView):
    template_name = 'contact.html'


class FaqView(TemplateView):
    template_name = 'faqs.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy.html'


class TermsOfUseView(TemplateView):
    template_name = 'terms.html'


class FilterByCategory(View):
    model = Product
    template_name = 'category.html'

    def get(self, request, *args, **kwargs):
        category_name = self.request.GET.get('category')
        try:
            category_obj = Category.objects.get(category_name=category_name)
            print(category_obj.category_name)
            products = Product.objects.filter(category=category_obj.id)
            print(products)
            context = {
                'category': category_name,
                'products': products
            }
            return render(self.request, 'category.html', context)
        except Exception as e:
            print(e)
            context = {
                'category': category_name,
            }
            return render(self.request, 'category.html', context)


class MyOrdersView(ListView):
    model = Order
    template_name = 'orders.html'

    def get(self, request, *args, **kwargs):
        orders = self.model.objects.filter(user=self.request.user)
        if orders.count() > 0:
            context = {
                'orders': orders
            }
            return render(self.request, 'orders.html', context)
        else:
            return render(self.request, 'orders.html')


class OrderDetail(DetailView):
    model = Order
    template_name = 'order-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_obj = Order.objects.get(id=self.kwargs.get('pk'))

        # print(Order.item.all()[0].get_order_item_total)
        total = 0
        for order in order_obj.item.all():
            # for order in order.item.all():
            print(order.get_order_item_total())
            total += order.get_order_item_total()
        print(total)
        try:
            context['total'] = total
        except Exception as e:
            print(e)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'single.html'


class SPlOfferDetail(DetailView):
    model = SpecialOfferProduct
    template_name = 'single.html'


class SearchView(View):
    model = Product
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(self.request, 'product.html', {'products': products})

    def post(self, request, *args, **kwargs):
        qs = self.request.POST['searchedVal']
        print(qs)
        products = Product.objects.filter(Q(category__category_name__icontains=qs.capitalize()) |
                                          Q(name__icontains=qs))
        print(products)
        print(self.request.META['HTTP_REFERER'])
        if qs is '':
            print(self.request.path_info)
            messages.error(self.request, "Cannot search for empty.Please enter some text.")
            return redirect(self.request.META['HTTP_REFERER'])
        elif products.count() > 0:
            return render(self.request, 'product.html', {'products': products})
        else:
            messages.error(self.request, "No result found")
            return redirect(self.request.META['HTTP_REFERER'])


class CheckoutView(ListView):
    model = Order
    template_name = 'checkout.html'
    form_class = AddressForm

    def get(self, request, *args, **kwargs):
        # print(self.request.GET.getlist('cartItemList'))
        x = self.request.GET.getlist('cartItemList')
        incoming_id_list = []
        for y in x:
            print(y)
            for z in y:
                if z.isdigit():
                    incoming_id_list.append(int(z))
        products = []
        for obj in incoming_id_list:
            products.append(Product.objects.get(id=obj))
        return render(self.request, 'checkout.html', {'count': len(incoming_id_list), 'products': products})

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        if self.request.user.is_anonymous:
            messages.error(self.request, 'Please login to place order')
            return redirect('src:home')
        else:
            return redirect('src:payment')


class CreateOrder(LoginRequiredMixin, CreateView):
    model = Order
    login_url = 'src:home'
    form_class = AddressForm

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        return redirect('src:my-orders')


class PaymentView(View):
    model = Payment
    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.error(self.request, 'Please login to make payment')
            return redirect('src:home')
        return render(self.request, 'payment.html')

    def post(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            messages.error(self.request, 'Please login to make payment')
            return redirect('src:home')
        return redirect('src:my-orders')
