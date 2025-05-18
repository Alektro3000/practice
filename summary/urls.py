from django.urls import path, include
import summary.views as views
import summary.views_pdf as views_pdf
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('export/product/csv', views.CreateProductSummaryCSVView.as_view(), name='export_product_csv'),
    path('export/run_out/csv', views.CreateProductRunOutSummaryCSVView.as_view(), name='export_run_out_csv'),
    path('export/movement/csv', views.CreateMovementSummaryCSVView.as_view(), name='export_movement_csv'),
    path('export/product_movement/csv', views.CreateProductMovementFullSummaryCSVView.as_view(), name='export_product_movement_csv'),

    path('export/product/pdf', views_pdf.CreateProductSummaryPDFView.as_view(), name='export_pdf'),

    path('export/', views.SummaryListView.as_view(), name='export_all'),  
    path('export/<int:id>', views.SummaryLoadView.as_view(), name='export'),  
]
