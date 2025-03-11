from django.urls import path
from .views import *

urlpatterns = [
    path('user/', UserViewSet.as_view(), name="UserList"),
    path('client/', CustomerViewSet.as_view(), name="client"),
    path('produit/',ProductViewSet.as_view(),name="ProduitList"),
    path('stock/',StockViewSet.as_view(),name="StockList"),
    path('paiement/',PaiementViewSet.as_view(),name='paiement'),
    path('depense/',DepenseViewSet.as_view(),name='depense'),
    path('consultation/',ConsultationViewSet.as_view(),name='consultation'),
    path('prescription/',PrescriptionViewSet.as_view(),name='prescription'),
    path('lunette/',LunetteViewSet.as_view(),name='lunette'),
    path('EtatStock/',EtatStockViewSet.as_view(),name="EtatStock"),
    path('Group/',GroupsViewSet.as_view(),name="Group"),
    path('login/',CustomAuthToken.as_view(),name="login"),
    path('management/',ManagementViewSet.as_view(),name="management"),
    path('information/',InformationViewSet.as_view(),name="information"),
    path('backup/', BackupDatabaseView.as_view(), name='backup-database'),
]