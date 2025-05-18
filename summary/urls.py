from django.urls import path
import summary.views as views

urlpatterns = [
    
    path('export/product/csv/', views.ProductSummaryCSVView.as_view(), name='export_product'),
    path('export/product/pdf/', views.ProductSummaryPDFView.as_view(), name='export_product'),
    
    path('export/run_out/csv/', views.RunOutSummaryCSVView.as_view(), name='export_run_out'),
    path('export/run_out/pdf/', views.RunOutSummaryPDFView.as_view(), name='export_run_out'),

    
    path('export/movement/csv/', views.MovementSummaryCSVView.as_view(), name='export_movement'),
    path('export/movement/pdf/', views.MovementSummaryPDFView.as_view(), name='export_movement'),

    path('export/movement_full/csv/', views.MovementFullSummaryCSVView.as_view(), name='export_movement_full'),
    path('export/movement_full/pdf/', views.MovementFullSummaryPDFView.as_view(), name='export_movement_full'),

    path('export/', views.SummaryListView.as_view(), name='export_all'),  
    path('export/<int:id>/', views.SummaryLoadView.as_view(), name='export'),  
]
