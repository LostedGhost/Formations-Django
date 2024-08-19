from django.db import models
from api.utils import *

# Create your models here.

class Profil(models.Model):
    code = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Profil.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            'code': self.code,
            'nom': self.nom
        }
    
class Utilisateur(models.Model):
    slug = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    motDePasse = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', null=True)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slugs = Utilisateur.objects.all().values_list('slug', flat=True).distinct()
            while True:
                slug = generate_string(LENGTH_CODE)
                if slug not in slugs:
                    break
            self.slug = slug
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            'slug': self.slug,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'photo': self.photo,
            'profil': self.profil.to_json()
        }

class Publication(models.Model):
    code = models.CharField(max_length=100)
    texte = models.CharField(max_length=100)
    datePublication = models.DateTimeField(auto_now=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Publication.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def images(self):
        return ImagePublication.objects.filter(publication=self)
    
    def to_json(self):
        return {
            'code': self.code,
            'texte': self.texte,
            'datePublication': date_to_text(self.datePublication),
            'utilisateur': self.utilisateur.to_json(),
            'images': [image.to_json() for image in self.images()]
        }

class ImagePublication(models.Model):
    code = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = ImagePublication.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            'code': self.code,
            'image': self.image,
            'publication': self.publication.to_json()
        }

class Commentaire(models.Model):
    code = models.CharField(max_length=100)
    texte = models.CharField(max_length=100)
    dateCommentaire = models.DateTimeField(auto_now=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Commentaire.objects.all().values_list('code', flat=True).distinct()
            while True:
                code = generate_string(LENGTH_CODE)
                if code not in codes:
                    break
            self.code = code
        super().save(*args, **kwargs)
    
    def to_json(self):
        return {
            'code': self.code,
            'texte': self.texte,
            'dateCommentaire': date_to_text(self.dateCommentaire),
            'utilisateur': self.utilisateur.to_json(),
            'publication': self.publication.to_json()
        }