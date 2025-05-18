from django.urls import path
import summary.views as views

urlpatterns = [
    
    path('export/product/<str:format>/', views.CreateProductSummaryView.as_view(), name='export_product'),
    path('export/product/', views.CreateProductSummaryView.as_view(), name='export_product'),
    path('export/run_out/<str:format>/', views.CreateRunOutSummaryView.as_view(), name='export_run_out'),
    path('export/movement/<str:format>/', views.CreateMovementSummaryView.as_view(), name='export_movement'),
    path('export/product_movement/<str:format>/', views.CreateMovementFullSummaryView.as_view(), name='export_product_movement'),


    path('export/', views.SummaryListView.as_view(), name='export_all'),  
    path('export/<int:id>/', views.SummaryLoadView.as_view(), name='export'),  
]
