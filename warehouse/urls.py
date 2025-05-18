from django.urls import path
import warehouse.views as views


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'), 
    path('categories/<int:id>/', views.CategoryView.as_view(), name='category'), 
    
    path('products/', views.ProductListView.as_view(), name='products'), 
    path('products/<int:id>/', views.ProductView.as_view(), name='product'), 

    path('movements/', views.MovementListView.as_view(), name='movements'), 
    path('movements/<int:id>/', views.MovementView.as_view(), name='movement'), 

    path('operations/', views.OperationListView.as_view(), name='operations'), 
    path('operations/<int:id>/', views.OperationView.as_view(), name='operation'),
]
