from django.urls import path
from . import views

urlpatterns=[
    path('members/', views.members, name='members' ),
    path('afsal',views.afsal, name='afsal'),
    path('',views.index, name="index"),
    path('user_login/',views.user_login, name="user_login"),
    path('signup/',views.signup,name="signup"),
    path('shop/',views.shop,name="shop"),
    path('services/',views.services,name="services"),
    path('contactus/',views.contactus,name="contactus"),
    path('checkout/',views.checkout,name="checkout"),
    path('cart/',views.cart,name="cart"),
    path('singleproduct/<int:id>/',views.singleproduct,name="singleproduct"),
    path('thankyou/',views.thankyou,name="thankyou"),
    path('about/',views.about,name="about"),
    path('single1/',views.single1,name="single1"),
    path('single2/',views.single2,name="single2"),
    path('single3/',views.single3,name="single3"),
    path('add-to-cart/<int:product_id>/',views.add_to_cart,name="add_to_cart"),
    path('remove_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),  # Update quantity
    path('userprofile/',views.userprofile,name="userprofile"),
    path('logout/', views.user_logout, name='user_logout'),
    path("order-summary/<int:order_id>/", views.order_summary, name="order_summary"),

    

    
    

]