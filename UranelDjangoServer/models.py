from django.db import models
from django.contrib.auth.models import User



# Create your models here.


#model site
class Site(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    libelleSite=models.CharField(max_length=120)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    archived=models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Site")
        verbose_name_plural = ("Sites")

    def __str__(self):
        return self.libelleSite

    def get_absolute_url(self):
        return reverse("Site_detail", kwargs={"pk": self.pk})




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    
    def __int__(self):
        return self.pk

#model client
class Customer(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.OneToOneField)
    site=models.ForeignKey(Site, on_delete=models.CASCADE)
    
    nomCustomer=models.CharField(max_length=120,null=False)
    numeroCustomer=models.CharField(max_length=20)
    sexe=models.CharField(max_length=20,null=False)
    adresse=models.CharField(max_length=120)
    age=models.FloatField()
    
    archived=models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")

    def __str__(self):
        return self.nomCustomer

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})
    



#model Produit
class Product(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    categorieProduct=models.CharField(max_length=50)
    LibelleProduct=models.TextField(null=False)
    prix=models.FloatField()
    
    archived=models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.LibelleProduct

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


#model Stock
class Stock(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    operation=models.CharField(max_length=20,null=False)
    site=models.ForeignKey(Site,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    facture=models.CharField(max_length=100)
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantite=models.FloatField(null=False)
    prixArticle=models.FloatField(null=False)
    prixConvenu=models.FloatField(null=False)
    remise=models.FloatField(null=False)
    total=models.FloatField(null=False)
    archived=models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Stock")
        verbose_name_plural = ("Stocks")

    def __int__(self):
        return self.pk
    
    def get_absolute_url(self):
        return reverse("Stock_detail", kwargs={"pk": self.pk})
    

# paiement
class Paiement(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    site=models.ForeignKey(Site,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    facture=models.CharField(max_length=100)
    montant=models.FloatField()
    class Meta:
        verbose_name = ("Paiement")
        verbose_name_plural = ("Paiements")

    def __int__(self):
        return self.pk
    
    def get_absolute_url(self):
        return reverse("Paiement_detail", kwargs={"pk": self.pk})
    


class Depense(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    site=models.ForeignKey(Site,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    motif=models.CharField(max_length=100)
    montant=models.FloatField()
    class Meta:
        verbose_name = ("Depense")
        verbose_name_plural = ("Depenses")

    def __int__(self):
        return self.pk
    
    def get_absolute_url(self):
        return reverse("Depense_detail", kwargs={"pk": self.pk})
    

class Consultation(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    site=models.ForeignKey(Site,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    plainte=models.TextField()
    diagnostique=models.TextField()
    traitement=models.TextField()
    class Meta:
        verbose_name = ("Consultation")
        verbose_name_plural = ("Consultations")

    def __int__(self):
        return self.pk
    
    def get_absolute_url(self):
        return reverse("Consultation_detail", kwargs={"pk": self.pk})
    

class Prescription(models.Model):
    dates=models.DateTimeField(auto_now_add=True)
    site=models.ForeignKey(Site,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    prescription=models.TextField()
    class Meta:
        verbose_name = ("Prescription")
        verbose_name_plural = ("Prescriptions")

    def __int__(self):
        return self.pk
    
    def get_absolute_url(self):
        return reverse("Prescription_detail", kwargs={"pk": self.pk})

class Lunette(models.Model):
    dates=models.DateField( auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    site=models.ForeignKey(Site,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    #oeil droit 
    sphere_vl_od=models.CharField(default='(vide)',max_length=30)
    cylindre_vl_od=models.CharField(max_length=30,default='(vide)')
    axe_vl_od=models.CharField(max_length=30,default='(vide)')
    addition_vl_od=models.CharField(max_length=30,default='(vide)')

    sphere_vp_od=models.CharField(max_length=30,default='(vide)')
    cylindre_vp_od=models.CharField(max_length=30,default='(vide)')
    axe_vp_od=models.CharField(max_length=30,default='(vide)')
    addition_vp_od=models.CharField(max_length=30,default='(vide)')
    

    # oeil gauche

    sphere_vl_og=models.CharField(max_length=30,default='(vide)')
    cylindre_vl_og=models.CharField(max_length=30,default='(vide)')
    axe_vl_og=models.CharField(max_length=30,default='(vide)')
    addition_vl_og=models.CharField(max_length=30,default='(vide)')

    sphere_vp_og=models.CharField(max_length=30,default='(vide)')
    cylindre_vp_og=models.CharField(max_length=30,default='(vide)')
    axe_vp_og=models.CharField(max_length=30,default='(vide)')
    addition_vp_og=models.CharField(max_length=30,default='(vide)')
    
    #type verre
    focal=models.CharField(max_length=30,null=True)
    filtre=models.CharField(max_length=30,null=True)
    teinte=models.CharField(max_length=30,null=True)

    class Meta:
        verbose_name = ("lunette")
        verbose_name_plural = ("lunettes")
    # def __str__(self):
    #     return self.pk

    def get_absolute_url(self):
        return reverse("lunette_detail", kwargs={"pk": self.pk})

class Information(models.Model):
    telephone1=models.CharField(max_length=100,null=True)
    telephone2=models.CharField(max_length=100,null=True)
    adresse=models.CharField(max_length=250,null=True)
    mail=models.CharField(max_length=100,null=True)
    class Meta:
        verbose_name = ("information")
        verbose_name_plural = ("informationss")
    def __int__(self):
        return  self.pk
    def get_absolute_url(self):
        return reverse("information_detail", kwargs={"pk": self.pk})
    