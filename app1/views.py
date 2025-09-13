from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import UserProfile,Product,CartItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



# Create your views here.
def members(request):
    return HttpResponse("Hello World")


def afsal(request):
    return HttpResponse("hello Afsal")


def  index(request):
    return render (request,"index.html")

# def user_login(request):
#     return render (request,"login.html")

# def signup(request):
#     return render (request,"signup.html")

def shop(request):
    return render (request,"shop.html")

def services(request):
    return render (request,"services.html")

def contactus(request):
    return render (request,"contactus.html")

def checkout(request):
    return render (request,"checkout.html")

def cart(request):
    return render (request,"cart.html")

# def singleproduct(request):
#     return render (request,"singleproduct.html")

def thankyou(request):
    return render (request,"thankyou.html")

def about(request):
    return render (request,"about.html")


def userprofile(request):
    return render (request,"userprofile.html")









def signup(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Basic validation
        if password != confirm_password:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

        # Check if username (which is email) already exists
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html', {'error_message': 'Email already exists'})

        try:
            # Create user, setting username to email
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = fullname
            user.save()

            # Create profile linked to user
            UserProfile.objects.create(user=user, mobile=mobile)

            # Log the user in immediately (optional)
            login(request, user)

            # Redirect to login page or home page as you want
            return redirect('user_login')

        except Exception as e:
            # Log the error for debugging and show a friendly message
            print(f"Error creating user or profile: {e}")
            return render(request, 'signup.html', {'error_message': 'An error occurred during registration. Please try again.'})

    # If GET request, just render signup form
    return render(request, 'signup.html')



def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # authenticate expects username, which you set as email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email or password'})

    return render(request, 'login.html')


def home(request):
    return render(request, 'index.html')



def  single1(request):
    return render (request,"single1.html")


def  single2(request):
    return render (request,"single2.html")

def  single3(request):
    return render (request,"single3.html")



def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html',{'products':products})


def singleproduct(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'singleproduct.html', {'product': product})



# def cart(request):
#     cart_items = CartItem.objects.all()
#     cart_total = sum(item.total() for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


def cart(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    cart_items = CartItem.objects.filter(user=request.user)  # ✅ only this user's items
    cart_total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

from django.shortcuts import get_object_or_404, redirect
from .models import Product, CartItem

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     cart_item, created = CartItem.objects.get_or_create(product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('cart')
from django.shortcuts import get_object_or_404, redirect
from .models import Product, CartItem

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        # redirect to login if not logged in
        return redirect("user_login")

    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,  # ✅ assign logged-in user
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")




def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')


def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # if set to 0 → remove item
    return redirect('cart')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

# User profile view
@login_required
def user_profile(request):
    user = request.user  # Get currently logged-in user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Optional: first_name and last_name if you include them
        first_name = request.POST.get('first_name', '')
        # last_name = request.POST.get('last_name', '')

        # Update user details
        user.username = username
        user.email = email
        user.first_name = first_name
        # user.last_name = last_name
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('userprofile')

    context = {
        'user': user
    }
    return render(request, 'userprofile.html', context)


# Logout view
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have successfully logged out!")
        return redirect('user_login')  # Redirect to login page
    return redirect('userprofile')












# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import BillingDetails, Order, OrderItem, CartItem, Product


# def checkout(request):
#     if request.method == "POST":
#         # 1️⃣ Save billing details
#         billing = BillingDetails.objects.create(
#             country=request.POST.get("country"),
#             first_name=request.POST.get("first_name"),
#             last_name=request.POST.get("last_name"),
#             address=request.POST.get("address"),
#             apartment=request.POST.get("apartment"),
#             state_country=request.POST.get("state_country"),
#             postal_zip=request.POST.get("postal_zip"),
#             email=request.POST.get("email"),
#             phone=request.POST.get("phone"),
#             order_notes=request.POST.get("order_notes"),
#         )

#         # 2️⃣ Create order
#         payment_method = request.POST.get("payment_method")
#         order = Order.objects.create(
#             billing=billing,
#             payment_method=payment_method,
#         )

#         # 3️⃣ Add cart items to order
#         cart_items = CartItem.objects.all()   # 👈 adjust if using session/user-based carts
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#             )

#         # 4️⃣ Clear cart
#         cart_items.delete()

#         messages.success(request, "Order placed successfully!")
#         return redirect("order_success", order_id=order.id)

#     # GET request → show checkout page
#     cart_items = CartItem.objects.all()
#     total = sum(item.total() for item in cart_items)

#     return render(request, "checkout.html", {
#         "cart_items": cart_items,
#         "total": total,
#     })





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, BillingDetails, Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem, BillingDetails, Order, OrderItem

# @login_required
# def checkout(request):
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user)






#     if request.method == "POST":
#         # Save billing details
#         billing = BillingDetails.objects.create(
#             user=user,
#             country=request.POST.get("country"),
#             first_name=request.POST.get("first_name"),
#             last_name=request.POST.get("last_name"),
#             address=request.POST.get("address"),
#             state_country=request.POST.get("state_country"),
#             postal_zip=request.POST.get("postal_zip"),
#             email=request.POST.get("email"),
#             phone=request.POST.get("phone"),
#             order_notes=request.POST.get("order_notes"),
#         )

#         # Create order
#         order = Order.objects.create(
#             user=user,
#             billing=billing,
#             payment_method=request.POST.get("payment_method")
#         )

#         # Move cart items into order
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#             )
#         cart_items.delete()  # Empty cart after checkout

#         return redirect("order_summary", order_id=order.id)

#     cart_total = sum(item.total_price for item in cart_items)
#     return render(request, "checkout.html", {"cart_items": cart_items, "cart_total": cart_total})
from django.contrib import messages

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    # Calculate total quantity
    total_quantity = sum(item.quantity for item in cart_items)

    # 🚨 Prevent empty cart checkout
    if total_quantity == 0:
        messages.warning(request, "Your cart is empty!")
        return redirect("cart")

    if request.method == "POST":
        # Save billing details
        billing = BillingDetails.objects.create(
            user=user,
            country=request.POST.get("country"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            address=request.POST.get("address"),
            state_country=request.POST.get("state_country"),
            postal_zip=request.POST.get("postal_zip"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            order_notes=request.POST.get("order_notes"),
        )

        # Create order
        order = Order.objects.create(
            user=user,
            billing=billing,
            payment_method=request.POST.get("payment_method"),
        )

        # Move cart items into order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )

        # Clear the cart
        cart_items.delete()

        return redirect("order_summary", order_id=order.id)

    # Calculate cart total
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(
        request,
        "checkout.html",
        {"cart_items": cart_items, "cart_total": cart_total},
    )


@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_summary.html", {"order": order})


