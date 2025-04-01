from django.urls import path 
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('mobile', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login', LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('changepassword', views.password_change, name='changepassword'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('address', views.address, name='address'),
    path('add-to-cart', views.AddToCart, name='add-to-cart'),
    path('cart', views.ShowCart, name='show-cart'),
    path('checkout', views.CheckOut, name='checkout'),
    path('paymentdone', views.PaymentDone, name='paymentdone'),
    path('orders', views.Orders, name='orders'),
    
    path('pluscart', views.plus_cart), 
    path('minuscart', views.minus_cart),
    path('removecart', views.remove_cart),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)