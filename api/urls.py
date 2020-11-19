from django.urls import path
from api import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<str:store_uuid>/products/',
         views.ProductView.as_view(), name='products'),
    path('products/', views.ProductListView.as_view(), name='list-products'),
    path('stores/', views.StoreListView.as_view(), name='stores'),
]
