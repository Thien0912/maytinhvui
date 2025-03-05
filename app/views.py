import imp
from itertools import product
from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, Value, IntegerField

# Create your views here.

def success(request):
    context = {}
    return render(request, 'app/success.html', context)

def review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "visible"
        
        # Kiểm tra người dùng đã bình luận hay chưa
        user_review = Review.objects.filter(product=product, user=request.user).first()

        # Nếu đã đăng nhập, thêm annotation
        reviews = Review.objects.filter(product=product).annotate(
            is_user_review=Case(
                When(user=request.user, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-is_user_review', '-created_at')  # Sắp xếp theo is_user_review và created_at
    else:
        user_not_login = "visible"
        user_login = "hidden"
        user_review = None

        # Nếu chưa đăng nhập, chỉ sắp xếp theo created_at
        reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Đặt giá trị display cho form
    form_display = "none" if user_review else "block"

    context = {
        'categories': categories,
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'form_display': form_display,
        'user_not_login': user_not_login, 
        'user_login': user_login
    }
    return render(request, 'app/review.html', context)

@login_required
def add_or_update_review(request, product_id):
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review_id = request.POST.get('review_id')  # Lấy ID nếu là cập nhật
        product = get_object_or_404(Product, id=product_id)

        if review_id:  # Nếu có review_id thì cập nhật
            review = get_object_or_404(Review, id=review_id, user=request.user)
            review.rating = rating
            review.comment = comment
            review.save()  # Cập nhật nội dung đánh giá
            return JsonResponse({"status": "updated"})
        else:  # Nếu không có review_id thì tạo mới
            Review.objects.create(
                product=product, user=request.user, rating=rating, comment=comment
            )
            return JsonResponse({"status": "created"})

    return JsonResponse({"status": "error"})

@login_required
def delete_review(request, product_id):
    if request.method == "POST":
        review_id = request.POST.get('review_id')  # Lấy ID của review cần xóa
        review = Review.objects.filter(id=review_id, product_id=product_id, user=request.user)
        if review.exists():
            review.delete()  # Xóa review
            return JsonResponse({"status": "deleted"})
    return JsonResponse({"status": "error"})

from django.utils.timezone import now

def detail(request):
    categories = Category.objects.all()
    active_category = request.GET.get('category', '')

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "visible"
    else:
        user_not_login = "visible"
        user_login = "hidden"

    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)

    if active_category:
        products = Product.objects.filter(category__slug=active_category)

    # Xử lý giá giảm cho từng sản phẩm trong danh sách
    for product in products:
        offer = Offer.objects.filter(product=product, start__lte=now(), end__gte=now()).first()
        product.discount_price = product.price  # Giá mặc định là giá gốc
        product.discount_percent = 0  # Mặc định không giảm giá

        if offer:
            product.discount_price = product.price * (1 - offer.discount / 100)
            product.discount_percent = offer.discount

    context = {
        'categories': categories,
        'active_category': active_category,
        'products': products,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/detail.html', context)

def search(request):
    categories= Category.objects.all()
    active_category= request.GET.get('category','')
    if request.method == "POST":
        searched= request.POST["searched"]
        keys= Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer= request.user
        order, created= Order.objects.get_or_create(customer =customer)
        items= order.orderdetail_set.all()
        user_not_login = "hidden"
        user_login = "visible"
    else:
        order= {'get_cart_items': 0, 'get_cart_total': 0}
        items= []
        user_not_login = "visible"
        user_login = "hidden"
    products= Product.objects.all()
    if active_category:
        products= Product.objects.filter(category__slug = active_category)
    return render(request,'app/search.html',{'categories':categories, 
                                             'active_category': active_category, 
                                             'searched': searched, 'keys': keys, 
                                             'products': products, 'items': items, 
                                             'user_not_login': user_not_login, 
                                             'user_login': user_login})

def category(request):
    categories= Category.objects.all()
    active_category= request.GET.get('category','')
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "visible"
    else:
        user_not_login = "visible"
        user_login = "hidden"
    if active_category:
        products= Product.objects.filter(category__slug = active_category)
    context= {'categories':categories, 
              'active_category': active_category,  
              'products': products, 
              'user_not_login': user_not_login, 
              'user_login': user_login}
    return render(request,'app/category.html',context)

def register(request):
    form= CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            start_date = timezone.now()
            end_date = start_date + timezone.timedelta(days = 3)
            if not Offer.objects.filter(user=user).exists():
                products = Product.objects.all()
                for product in products:
                    Offer.objects.create(
                        discount = 10,
                        product = product,
                        user=user,
                        start=start_date,
                        end=end_date
                    )
        return redirect('login')
    context= {'form':form}
    return render(request,'app/register.html',context)

def loginForm(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user= authenticate(request,username= username, password= password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Tài khoản hoặc mật khẩu không đúng')
    context= {}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer= request.user
        order, created= Order.objects.get_or_create(customer =customer)
        items= order.orderdetail_set.all()
        user_not_login = "hidden"
        user_login = "visible"
        user_offer = Offer.objects.filter(user=customer, start__lte=timezone.now(), end__gte=timezone.now()).first()
    else:
        order= {'get_cart_items': 0, 'get_cart_total': 0}
        items= []
        user_not_login = "visible"
        user_login = "hidden"
        user_offer = None
    categories= Category.objects.all()
    products= Product.objects.all()
    context={'categories':categories, 
             'products': products, 
             'user_not_login': user_not_login,
             'user_offer': user_offer,
             'user_login': user_login}
    return render(request,'app/home.html',context)

def cart(request):
    categories = Category.objects.all()
    active_category = request.GET.get('category', '')

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        
        # Xóa tất cả các bản ghi CheckoutInfo cũ trước khi tạo mới
        CheckoutInfo.objects.filter(order=order).delete()
        checkout_info = CheckoutInfo.objects.create(order=order)

        items = order.orderdetail_set.all()

        for item in items:
            offer = Offer.objects.filter(product=item.product, start__lte=now(), end__gte=now()).first()
            if offer:
                item.discount = offer.discount
                item.discount_price = round(item.product.price * (1 - offer.discount / 100), -3)  # Làm tròn hàng nghìn
            else:
                item.discount = 0
                item.discount_price = item.product.price

            item.total_price = item.discount_price * item.quantity

        user_not_login = "hidden"
        user_login = "visible"
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        items = []
        user_not_login = "visible"
        user_login = "hidden"

    context = {
        'categories': categories,
        'active_category': active_category,
        'items': items,
        'order': order,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/cart.html', context)

def checkout(request):
    categories = Category.objects.all()
    active_category = request.GET.get('category', '')
    c_form = CheckoutInfoForm()

    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(customer=customer).first()  # Lấy đơn hàng chưa thanh toán

        if request.method == 'POST':
            selected_items = request.POST.getlist('selected_items')  # Lấy danh sách sản phẩm được chọn
            if order:
                items = order.orderdetail_set.filter(product__id__in=selected_items)  # Lọc sản phẩm đã chọn
            else:
                items = []

            c_form = CheckoutInfoForm(request.POST)
            if c_form.is_valid():
                checkout_info = c_form.save(commit=False)
                checkout_info.order = order
                checkout_info.save()

                # Giảm số lượng sản phẩm trong kho
                for item in items:
                    product = item.product
                    if product.quantity is not None and product.quantity >= item.quantity:
                        product.quantity -= item.quantity
                        product.save()
                    else:
                        messages.error(request, f"Sản phẩm {product.name} không đủ hàng!")

                # Nếu tất cả sản phẩm hợp lệ, đánh dấu đơn hàng đã hoàn tất
                if all(item.product.quantity >= 0 for item in items):
                    order.save()
                    messages.success(request, "Thanh toán thành công!")
                    return redirect('success')
        else:
            items = order.orderdetail_set.all() if order else []
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        items = []

    for item in items:
        offer = Offer.objects.filter(product=item.product, start__lte=now(), end__gte=now()).first()
        item.discount_price = item.product.get_discounted_price()
        item.discount_percent = offer.discount if offer else 0

    context = {
        'c_form': c_form,
        'categories': categories,
        'active_category': active_category,
        'items': items,
        'order': order,
        'user_not_login': "visible" if not request.user.is_authenticated else "hidden",
        'user_login': "hidden" if not request.user.is_authenticated else "visible"
    }
    return render(request, 'app/checkout.html', context)

def updateOrder(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created= Order.objects.get_or_create(customer =customer)
    orderDetail, created= OrderDetail.objects.get_or_create(order =order, product =product)
    if action == 'add':
        orderDetail.quantity += 1
    elif action == 'remove':
        orderDetail.quantity -= 1
    orderDetail.save()
    if orderDetail.quantity <= 0:
        orderDetail.delete()
    order.total = order.get_cart_total()
    order.save()
    return JsonResponse('added', safe= False)

def delete_order_detail(request, detail_id):
    if request.user.is_authenticated:
        order_detail = get_object_or_404(OrderDetail, id=detail_id, order__customer=request.user)
        order_detail.delete()
    return redirect('cart')