from django.db import transaction
from django.db.models import Sum,F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.contrib.auth.models import Group
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from datetime import date
import os
from django.conf import settings
import shutil
from django.http import FileResponse
from django.views import View
from datetime import datetime


class InformationViewSet(APIView):
    def get(self,request, *args, **kwargs):
        pk=request.GET.get('pk')
        if pk is not None:
            info=Information.objects.values("id",
                                            "telephone1",
                                            "telephone2",
                                            "mail",
                                            "adresse",
                                            ).filter(pk=pk)
        else:
            info=Information.objects.values("id",
                                            "telephone1",
                                            "telephone2",
                                            "mail",
                                            "adresse",
                                            )
        return Response(info)
    def patch(self,request):
        pk=request.GET.get("pk")
        try:
            info=Information.objects.get(pk=pk)
        except Exception as e:
            return Response({"detail":e},status=status.HTTP_404_NO_FOUND)
        
        serializer=InformationSerializer(info,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




# Create your views here.
class UserViewSet(APIView):
    def get(self,request, *args, **kwargs):
        pk=request.GET.get('pk')
        if pk is not None:
            Users=Profile.objects.annotate(Id=F('user'),
                                           username=F('user__username'),
                                           first_name=F('user__first_name'),
                                           last_name=F('user__last_name'),
                                           is_active=F('user__is_active'),
                                           groups=F('user__groups'),
                                           groups__name=F('user__groups__name'),
                                           libelleSites=F('site__libelleSite'),
                                           sites=F('site')
                                           ).values("user","user__username",
                                      "user__first_name","user__last_name","user__password","user__is_active",
                                      "user__groups","user__groups__name","site__libelleSite").filter(user=pk)
        else:
            Users=Profile.objects.annotate(Id=F('user'),
                                           username=F('user__username'),
                                           first_name=F('user__first_name'),
                                           last_name=F('user__last_name'),
                                           is_active=F('user__is_active'),
                                           groups=F('user__groups'),
                                           groups__name=F('user__groups__name'),
                                           libelleSitess=F('site__libelleSite'),
                                           sites=F('site')
                                           ).values("user","user__username",
                                      "user__first_name","user__last_name","user__password","user__is_active",
                                      "user__groups","user__groups__name","site","site__libelleSite")
        return Response(Users)
    def post(self, request):
        try:
            data = request.data
            password = data['password']
            user = User(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_active=True,
                is_staff=False,
                is_superuser=False,
                )
            user.set_password(password)  # Cette méthode hache le mot de passe avant de le sauvegarder
            user.save()

            profile = Profile(user=user, fonction=data['fonction'])  # Correction ici
            profile.save()

            if 'groups' in data:
                groups = data['groups']  # Assumes 'groups' is a list of group IDs or names
                user.groups.set(groups)
            serializer = UserSerializer(user)

                

            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e :
            return Response( { "detail":f"une erreur  s'est produit produit {e} "  }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        try:
            # Récupérer l'ID de l'utilisateur depuis les paramètres de l'URL
            pk = request.GET.get('pk')
            if not pk:
                return Response(
                    {"detail": "Le paramètre 'pk' est requis."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Récupérer l'utilisateur et le profil
            user = User.objects.get(pk=pk)
            profile = Profile.objects.get(user=pk)

        except User.DoesNotExist:
            return Response(
                {"detail": "Utilisateur non trouvé."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profil non trouvé."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Une erreur s'est produite lors de la récupération des données."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Sérialiser et valider les données
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        profile_data = {"site": request.data.get("site")}  # Extraire le champ 'site' pour le profil
        profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            errors = {}
            if user_serializer.errors:
                errors["user"] = user_serializer.errors
            if profile_serializer.errors:
                errors["profile"] = profile_serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


            

class GroupsViewSet(APIView):
    def get(self,request,*args,**kwargs):
        fonction=Group.objects.values("id","name")
        site=Site.objects.values("id","libelleSite")
        return Response({"fonction":fonction,"site":site}) 

# client    
class CustomerViewSet(APIView):
    def get(self,request,*args, **kwargs):
        pk=request.GET.get('pk')
        if pk is None:
            Customers=Customer.objects.values("id",
                                              "site__libelleSite",
                                              "dates",
                                              "user__username",
                                              "nomCustomer",
                                              "numeroCustomer",
                                              "sexe",
                                              "adresse",
                                              "age").order_by("-id")
            return Response(Customers)
        else:
            Customers=Customer.objects.values("id",
                                              "site__libelleSite",
                                              "dates",
                                              "user__username",
                                              "nomCustomer",
                                              "numeroCustomer",
                                              "sexe",
                                              "adresse",
                                              "age").filter(pk=pk)
            consultation=Consultation.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "plainte",'diagnostique',"traitement").filter(customer=pk).order_by("-id")
            
            facture=Stock.objects.values("facture").filter(customer=pk).distinct()
            lunette=Lunette.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "user","user__username","customer__sexe","customer__age",
                                               "sphere_vl_od",'cylindre_vl_od',"axe_vl_od","addition_vl_od",
                                               "sphere_vp_od","cylindre_vp_od","axe_vp_od","addition_vp_od",
                                               "sphere_vl_og","cylindre_vl_og","axe_vl_og","addition_vl_og",
                                               "sphere_vp_og","cylindre_vp_og","axe_vp_og","addition_vp_og",
                                               "focal","filtre","teinte").filter(customer=pk).order_by("-id")
            

            return Response({"info":Customers, "facture":facture,"consultation":consultation,"lunette":lunette})

    def post(self,request):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    



class ProductViewSet(APIView):

    def get(self,request, *args, **kwargs):
        product=Product.objects.values("id",
                                       "categorieProduct",
                                       "LibelleProduct",
                                       "prix")
        return Response(product)
    def post(self,request,*args,**kwargs):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
class StockViewSet(APIView):
    def get(self,request,site=None,operation=None,*args,**kwargs):
        site=request.GET.get('site')
        if(len(site)<=0):
            site=None
        operation=request.GET.get('operation')
        if site is  None and operation is None :
            stock=Stock.objects.values("id","dates","operation",
                                       "user","user__username",
                                       "site","site__libelleSite",
                                       "customer__nomCustomer","facture",
                                       "Product","Product__LibelleProduct","Product__categorieProduct",
                                       "Quantite","prixArticle","prixConvenu","remise","total").filter(operation="vente").order_by("-id")
                                       
        elif site is not None and operation is not None :
                stock=Stock.objects.values("id","dates","operation",
                                           "user","user__username",
                                           "site","site__libelleSite",
                                           "customer__nomCustomer","facture",
                                           "Product","Product__LibelleProduct","Product__categorieProduct",
                                           "Quantite","prixArticle","prixConvenu","remise","total").order_by("-id").filter(site=site,operation=operation)
        elif site is not None and operation is None:
                stock=Stock.objects.values("id","dates","operation",
                                           "user","user__username",
                                           "site","site__libelleSite",
                                           "customer__nomCustomer","facture",
                                           "Product","Product__LibelleProduct","Product__categorieProduct",
                                           "Quantite","prixArticle","prixConvenu","remise","total").order_by("-id").filter(site=site,operation="vente")
        elif site is None and operation is not None:
                stock=Stock.objects.values("id","dates","operation",
                                           "user","user__username",
                                           "site","site__libelleSite",
                                           "customer__nomCustomer","facture",
                                           "Product","Product__LibelleProduct","Product__categorieProduct",
                                           "Quantite","prixArticle","prixConvenu","remise","total").order_by("-id").filter(operation=operation)   
        
        return Response(stock)
    def post(self, request, *args, **kwargs):
        try:
            # Démarrer une transaction
            with transaction.atomic():
                # Récupérer les données de la requête
                stocks_data = request.data

                # Valider et enregistrer chaque instance
                created_stocks = []
                for stock_data in stocks_data:
                    serializer = StockSerializer(data=stock_data)
                    serializer.is_valid(raise_exception=True)
                    stock = serializer.save()
                    created_stocks.append(stock)
                # Retourner la réponse avec les objets créés
                response_serializer = StockSerializer(created_stocks, many=True)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # En cas d'erreur, la transaction est annulée
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self,request,*args,**kwargs):
        try:
            pk=request.GET.get("pk")
            stock=Stock.objects.get(pk=pk)
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Stock.DoesNotExist:
            return Response({"detail":"Aucune correspondance n'a été trouvée"},status=status.HTTP_404_NOT_FOUND)
        

class EtatStockViewSet(APIView):
    def get(self,request,*args,**kwargs):
            site=request.GET.get("site")
            if(len(site)<=0):
                site=None
            if site is not None:
                entree_stock=Stock.objects.values("Product","Product__categorieProduct","Product__LibelleProduct","Product__prix").filter(site=site,operation="entrée").annotate(quantite_entree=models.Sum("Quantite"))
                sortie_stock=Stock.objects.values("Product","Product__categorieProduct","Product__LibelleProduct","Product__prix").filter(site=site).exclude(operation="entrée").annotate(quantite_sortie=models.Sum("Quantite"))
                stock=Stock.objects.values("id","dates","operation",
                                           "user","user__username",
                                           "site","site__libelleSite",
                                           "Product","Product__LibelleProduct",
                                           "Quantite","prixArticle","prixConvenu","remise","total").exclude(operation="vente").order_by("-id").filter(site=site)
                return Response({ "entree_stock":entree_stock,"sortie_stock":sortie_stock,"stock":stock })
            else:
                entree_stock=Stock.objects.values("Product","Product__LibelleProduct","Product__prix").filter(operation="entrée").annotate(quantite_entree=models.Sum("Quantite"))
                sortie_stock=Stock.objects.values("Product","Product__LibelleProduct","Product__prix").exclude(operation="entrée").annotate(quantite_sortie=models.Sum("Quantite"))
                stock=Stock.objects.values("id","dates","operation",
                                           "user","user__username",
                                           "site","site__libelleSite",
                                           "Product","Product__LibelleProduct",
                                           "Quantite","prixArticle","prixConvenu","remise","total").exclude(operation="vente").order_by("-id")
                return Response({ "entrée":entree_stock,"sortie":sortie_stock,"stock":stock })

    
class PaiementViewSet(APIView):
    def get(self,request,*args,**kwargs):
        pk=request.GET.get('pk')
        facture=request.GET.get('facture')
        site=request.GET.get('site')
        if(len(site)<=0):
            site=None
        if pk is None and facture is None and site is None :
            paiement=Paiement.objects.values("id","dates",
                                             "site","site__libelleSite",
                                             "user","user__username",
                                             "customer","customer__nomCustomer",
                                             "facture","montant")
            return Response(paiement)
        elif pk is not None:
            paiement=Paiement.objects.values("id","dates",
                                             "site","site__libelleSite",
                                             "user","user__username",
                                             "customer","customer__nomCustomer",
                                             "facture","montant").filter(pk=pk)
            return Response(paiement)
        elif site is not None: 
            paiement=Paiement.objects.values("id","dates",
                                             "site","site__libelleSite",
                                             "user","user__username",
                                             "customer","customer__nomCustomer",
                                             "facture","montant").filter(site=site)
            return Response(paiement)
        elif facture is not None:
            stock=Stock.objects.values("id",
                                       "dates","operation",
                                       "user","user__username",
                                       "site","site__libelleSite",
                                       "customer__nomCustomer",
                                       "facture",
                                       "Product","Product__LibelleProduct","Product__categorieProduct",
                                       "Quantite","prixArticle","prixConvenu","remise","total").filter(facture=facture).order_by("-id")
            TotalPaiement=Paiement.objects.filter(facture=facture).aggregate(total_sum=Sum('montant'))
            return Response({'stock':stock,'TotalPaiement':TotalPaiement})
    def post(self,request):
        serializer=PaiementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        try:
            pk=request.GET.get("pk")
            paiement=Paiement.objects.get(pk=pk)
            paiement.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Paiement.DoesNotExist:
            return Response({"detail":"Aucune correspondance n'a été trouvée"},status=status.HTTP_404_NOT_FOUND)

class DepenseViewSet(APIView):
    def get(self,request,*args,**kwargs):
        site=request.GET.get("site")
        if(len(site)<=0):
            site=None
        listmotif=Depense.objects.values("motif").distinct()
        if site is not None:
            listDepense=Depense.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "motif",'montant').filter(site=site).order_by("-id")
            return Response({ 'listDepense':listDepense,"listmotif":listmotif })
        else:
            listDepense=Depense.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "motif",'montant').order_by("-id")
            return Response({ 'listDepense':listDepense,"listmotif":listmotif })
    def post(self,request):
        serializer=DepenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        try:
            pk=request.GET.get("pk")
            depense=Depense.objects.get(pk=pk)
            depense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Depense.DoesNotExist:
            return Response({"detail":"Aucune correspondance n'a été trouvée"},status=status.HTTP_404_NOT_FOUND)


class PrescriptionViewSet(APIView):
    def get(self,request,*args,**kwargs):
        site=request.GET.get("site")
        pk=request.GET.get("pk")
        if(len(site)<=0):
            site=None
        
        if site is not None:
            prescription=Prescription.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "customer","customer__nomCustomer",
                                               "user","user__username",
                                               "prescription").filter(site=site).order_by("-id")
            return Response(prescription)
        elif pk is not None :
            prescription=Prescription.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "customer","customer__nomCustomer","customer__sexe","customer__age",
                                               "user","user__username",
                                               "prescription").filter(pk=pk).order_by("-id")
            return Response(prescription)
        else:
            prescription=Prescription.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "customer","customer__nomCustomer",
                                               "prescription").order_by("-id")
            return Response(prescription)
    def post(self,request):
        serializer=PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        try:
            pk=request.GET.get("pk")
            prescription=Prescription.objects.get(pk=pk)
            prescription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Prescription.DoesNotExist:
            return Response({"detail":"Aucune correspondance n'a été trouvée"},status=status.HTTP_404_NOT_FOUND)

class ConsultationViewSet(APIView):
    def get(self,request,*args,**kwargs):
        site=request.GET.get("site")
        if(len(site)<=0):
            site=None
        if site is not None:
            consultation=Consultation.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "customer","customer__nomCustomer",
                                               "user","user__username",
                                               "plainte",'diagnostique',"traitement").filter(site=site).order_by("-id")
            return Response(consultation)
        else:
            consultation=Consultation.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "customer","customer__nomCustomer",
                                               "plainte",'diagnostique',"traitement").order_by("-id")
            return Response(consultation)
    def post(self,request):
        serializer=ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        try:
            pk=request.GET.get("pk")
            consultation=Consultation.objects.get(pk=pk)
            consultation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Consultation.DoesNotExist:
            return Response({"detail":"Aucune correspondance n'a été trouvée"},status=status.HTTP_404_NOT_FOUND)



class LunetteViewSet(APIView):
    def get(self,request,*args,**kwargs):
        site=request.GET.get("site")
        pk=request.GET.get("pk")

        if(len(site)<=0):
            site=None

        if site is not None:
            lunette=Lunette.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username","customer__sexe","customer__age",
                                               "customer","customer__nomCustomer",
                                               "sphere_vl_od",'cylindre_vl_od',"axe_vl_od","addition_vl_od",
                                               "sphere_vp_od","cylindre_vp_od","axe_vp_od","addition_vp_od",
                                               "sphere_vl_og","cylindre_vl_og","axe_vl_og","addition_vl_og",
                                               "sphere_vp_og","cylindre_vp_og","axe_vp_og","addition_vp_og",
                                               "focal","filtre","teinte").filter(site=site).order_by("-id")
            return Response(lunette)
        
        elif pk is not None:
            lunette=Lunette.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "customer__sexe","customer__age",
                                               "customer","customer__nomCustomer",
                                               "sphere_vl_od",'cylindre_vl_od',"axe_vl_od","addition_vl_od",
                                               "sphere_vp_od","cylindre_vp_od","axe_vp_od","addition_vp_od",
                                               "sphere_vl_og","cylindre_vl_og","axe_vl_og","addition_vl_og",
                                               "sphere_vp_og","cylindre_vp_og","axe_vp_og","addition_vp_og",
                                               "focal","filtre","teinte").filter(pk=pk).order_by("-id")
            return Response(lunette)
        
        
        else:
            lunette=Lunette.objects.values("id","dates",
                                               "site","site__libelleSite",
                                               "user","user__username",
                                               "user","user__username","customer__sexe","customer__age",
                                               "sphere_vl_od",'cylindre_vl_od',"axe_vl_od","addition_vl_od",
                                               "sphere_vp_od","cylindre_vp_od","axe_vp_od","addition_vp_od",
                                               "sphere_vl_og","cylindre_vl_og","axe_vl_og","addition_vl_og",
                                               "sphere_vp_og","cylindre_vp_og","axe_vp_og","addition_vp_og",
                                               "focal","filtre","teinte").order_by("-id")
            return Response(lunette)
    def post(self,request,*args,**kwargs):
        serializer=LunetteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        try:
            pk=request.GET.get("pk")
            lunette=Lunette.objects.get(pk=pk)
            lunette.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Lunette.DoesNotExist:
            return Response({"detail":"Aucune correspondance n'a été trouvée"},status=status.HTTP_404_NOT_FOUND)



class CustomAuthToken(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        
        # Authentifier l'utilisateur
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=400)

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            userinfo=User.objects.values("id","first_name","last_name","groups__name").filter(username=username)
            site=Profile.objects.values("site","site__libelleSite").filter(user__username=username)
            return Response({"token": token.key,"userInfo":userinfo,"site":site})

        return Response({"error": "Identifiants invalides"}, status=400)
    

class ManagementViewSet(APIView):
    def get(self,request,*args,**kwargs):
        date_debut_str = request.GET.get('date_debut')
        date_fin_str = request.GET.get('date_fin')
        site=request.GET.get("site")
        if(len(site)<=0):
            site=None
        if date_debut_str is not None and date_fin_str is not None :
            # Convertir les chaînes de caractères en objets date
            try:
                date_debut = date.fromisoformat(date_debut_str)
                date_fin = date.fromisoformat(date_fin_str) 
            except Exception as e:
                return Response({"detail": e}, status=400)
            
            if site is not None :
                vente=Stock.objects.values("Product__categorieProduct","Product__LibelleProduct").filter(dates__range=[date_debut,date_fin],operation="vente",site=site).annotate(total_montant=models.Sum("total"),total_quantite=models.Sum("Quantite"))
                depense=Depense.objects.values("motif").filter(dates__range=[date_debut,date_fin],site=site).annotate(total_montant=models.Sum("montant"))
                dette=Stock.objects.values("customer","customer__site__libelleSite","customer__nomCustomer","customer__numeroCustomer").filter(operation="vente").annotate(total_montant=models.Sum("total"))
                paiement=Paiement.objects.values("customer","customer__site__libelleSite","customer__nomCustomer","customer__numeroCustomer").annotate(total_montant=models.Sum("montant"))
                entree=Paiement.objects.values("montant").filter(dates__range=[date_debut,date_fin],site=site).aggregate(total_montant=models.Sum("montant"))
                
            else :
                vente=Stock.objects.values("Product__categorieProduct","Product__LibelleProduct").filter(dates__range=[date_debut,date_fin],operation="vente").annotate(total_montant=models.Sum("total"))
                depense=Depense.objects.values("motif").filter(dates__range=[date_debut,date_fin]).annotate(total_montant=models.Sum("montant"))
                dette=Stock.objects.values("customer","customer__site__libelleSite","customer__nomCustomer","customer__numeroCustomer").filter(operation="vente").annotate(total_montant=models.Sum("total"))
                paiement=Paiement.objects.values("customer","customer__site__libelleSite","customer__nomCustomer","customer__numeroCustomer").annotate(total_montant=models.Sum("montant"))
                entree=Paiement.objects.values("montant").filter(dates__range=[date_debut,date_fin]).aggregate(total_montant=models.Sum("montant"))
                
             
            data={
                'vente':vente,
                "dette":dette,
                "paiement":paiement,
                "depense":depense,
                "entree":entree
            }
            return Response(data,status=status.HTTP_200_OK)
        else :
            return Response({"detail":"les dates n'ont pas été envoyé"})    

class BackupDatabaseView(View):
    def get(self, request, *args, **kwargs):
        # Chemin de la base de données SQLite
        db_path = settings.DATABASES['default']['NAME']
        
        # Créer un nom de fichier de sauvegarde avec la date et l'heure
        backup_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sqlite3"
        backup_path = os.path.join(settings.MEDIA_ROOT, backup_filename)
        
        # Copier la base de données dans le dossier de sauvegarde
        shutil.copy2(db_path, backup_path)
        
        # Renvoyer le fichier en tant que réponse téléchargeable
        response = FileResponse(open(backup_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
        return response