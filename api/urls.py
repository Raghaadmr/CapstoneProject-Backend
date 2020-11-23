from django.urls import path
from api import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<str:store_uuid>/products/<str:barcode>/',
         views.ProductView.as_view(), name='product-detail'),
    path('stores/', views.StoreListView.as_view(), name='store-list'),
    path('order/', views.OrderView.as_view(), name='order-create'),
    path('orders/', views.OrderListView.as_view(), name='order-List'),


]
