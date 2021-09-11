from django.contrib.auth import login, authenticate
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from .models import *
from .forms import *
from .mixins import CartMixin
from .forms import OrderForm
from .utils import recalc_cart


class MainView(CartMixin, View):

    template_name = 'main.html'

    def get(self, request, brand=''):
        if brand:
            brand = Brand.objects.filter(slug=brand).first()
            works = Work.objects.filter(brand=brand)
        else:
            works = Work.objects.all()
        brands = Brand.objects.all()
        context = {'works': works, 'brands': brands, 'cart': self.cart, 'user': request.user}
        return render(request, self.template_name, context)


class LKView(CartMixin, View):

    template_name = 'lk.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        user = request.user
        customer = Customer.objects.get(user=user)
        form = LKForm(request.POST or None)
        form.fields['phone'].initial = customer.phone
        form.fields['first_name'].initial = user.first_name
        form.fields['city'].initial = customer.city
        form.fields['address'].initial = customer.address
        form.fields['index'].initial = customer.index
        form.fields['email'].initial = user.email
        context = {
            'user': user,
            'form': form,
            'cart': self.cart
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = LKForm(request.POST or None)
        user = request.user
        if form.is_valid() and user.is_authenticated:
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
            if form.cleaned_data['first_name']:
                user.first_name = form.cleaned_data['first_name']
            user.save()
            customer = Customer.objects.get(user=user)
            if form.cleaned_data['phone']:
                customer.phone = form.cleaned_data['phone']
            if form.cleaned_data['city']:
                customer.city = form.cleaned_data['city']
            if form.cleaned_data['index']:
                customer.index = form.cleaned_data['index']
            if form.cleaned_data['address']:
                customer.address = form.cleaned_data['address']
            customer.save()
            return HttpResponseRedirect('/')
        context = {'form': form, 'user': user, 'cart': self.cart}
        return render(request, 'main.html', context)


class ProjectDetailView(CartMixin, View):

    template_name = 'project_detail.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        work = Work.objects.get(slug=slug)
        description = work.description.split('\n')
        print(description)
        context = {
            'user': request.user,
            'work': work,
            'cart': self.cart,
            'description': description
        }
        return render(request, self.template_name, context)


class ShopMainView(CartMixin, View):

    template_name = 'shop.html'

    def get(self, request, category=''):
        categories = Category.objects.all()
        if category:
            self.template_name = 'category_detail.html'
            category = Category.objects.filter(slug=category).first()
            products = Product.objects.filter(category=category)
            context = {'categories': categories, 'products': products, 'cart': self.cart, 'user': request.user}
            return render(request, self.template_name, context)
        else:
            products = Product.objects.all()
            context = {'categories': categories, 'products': products, 'cart': self.cart, 'user': request.user}
            return render(request, self.template_name, context)


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.get(user=user)
        form = OrderForm(request.POST or None)
        print(form.fields['delivery_type'])
        form.fields['first_name'].initial = user.first_name
        form.fields['phone'].initial = customer.phone
        form.fields['city'].initial = customer.city
        form.fields['address'].initial = customer.address
        context = {
            'cart': self.cart,
            'form': form,
            'user': user
        }
        return render(request, 'cart.html', context)


class ProductDetailView(CartMixin, View):

    template_name = 'product_detail.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('slug'))
        categories = Category.objects.all()
        subcategories = product.subcategory
        current_category = product.category
        characteristics = product.characteristics.split(';')
        context = {
            'product': product,
            'cart': self.cart,
            'categories': categories,
            'subcategories': subcategories,
            'current_category': current_category,
            'characteristics': characteristics
        }
        return render(request, self.template_name, context)


class CategoryView(CartMixin, View):

    template_name = 'category_detail.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        current_category = Category.objects.get(slug=kwargs.get('slug'))
        subcategories = Subcategory.objects.filter(category=current_category)
        products = Product.objects.filter(category=current_category)
        context = {
            'current_category': current_category,
            'categories': categories,
            'subcategories': subcategories,
            'products': products,
            'cart': self.cart,
            'user': request.user
        }
        return render(request, self.template_name, context)


class SubcategoryView(CartMixin, View):
    template_name = 'subcategory_detail.html'

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('category_slug'))
        subcategory = Subcategory.objects.get(category=category, slug=kwargs.get('subcategory_slug'))
        products = Product.objects.filter(subcategory=subcategory)
        context = {
            'category': category,
            'subcategory': subcategory,
            'products': products,
            'cart': self.cart,
            'user': request.user
        }
        return render(request, self.template_name, context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        print(self.cart.products.all())
        print(self.cart.final_price)
        return HttpResponseRedirect('/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/cart/')


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            context = {'form': form, 'cart': self.cart}
            return render(request, 'login.html', context)
        context = {'form': form, 'cart': self.cart}
        return render(request, 'login.html', context)


class SignUpView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'signup.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'signup.html', context)