from rest_framework import serializers
from .models import* 
from django.contrib.auth.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
        extra_kwargs = {
            'password': {'write_only': True}  # Le mot de passe doit être masqué dans les réponses
        }
        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        # Ajouter l'utilisateur au groupe "Admins" ou lui accorder les permissions d'admin
            user.is_staff = True  
            user.is_superuser=False
            user.save()
            return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields='__all__'

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paiement
        fields='__all__'
class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Depense
        fields='__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Consultation
        fields='__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Prescription
        fields='__all__'

class LunetteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lunette
        fields='__all__'

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Information
        fields='__all__'