from django.shortcuts import HttpResponse
from api.models import *

# Create your views here.
def inscription(request):
    nom = request.GET.get('nom', None)
    prenom = request.GET.get('prenom', None)
    email = request.GET.get('email', None)
    motDePasse = request.GET.get('motDePasse', None)
    profil_id = 2
    photo = request.FILES.get('photo', None)
    if nom and prenom and email and motDePasse and profil_id:
        u = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            motDePasse=chiffrement(motDePasse),
            profil_id=profil_id,
            photo=photo
        )
        u.save()
        return HttpResponse({
            'status': 200,
            'message': 'Inscription effectuée avec succès'
        })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })
    
def connexion(request):
    email = request.GET.get('email', None)
    motDePasse = request.GET.get('motDePasse', None)
    if email and motDePasse:
        u = Utilisateur.objects.filter(email=email, motDePasse=chiffrement(motDePasse))
        if u.exists():
            return HttpResponse({
                'status': 200,
                'message': 'Connexion effectuée avec succès',
                'utilisateur': u.first().to_json()
            })
        else:
            return HttpResponse({
                'status': 400,
                'message': 'Email ou mot de passe incorrect'
            })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })

def creer_publication(request):
    texte = request.GET.get('texte', None)
    slug = request.GET.get('slug', None)
    utilisateur_id = Utilisateur.objects.get(slug=slug).id
    if texte and utilisateur_id:
        p = Publication(
            texte=texte,
            utilisateur_id=utilisateur_id
        )
        p.save()
        return HttpResponse({
            'status': 200,
            'message': 'Publication effectuée avec succès',
            'publication': p.to_json()
        })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })

def ajout_image_publication(request):
    image=request.FILES.get('image')
    code=request.FILES.get('code')
    if image and code:
        p = Publication.objects.get(code=code)
        i = ImagePublication(
            image=image,
            publication=p
        )
        i.save()
        return HttpResponse({
            'status': 200,
            'message': 'Image ajoutée avec succès',
            'image': i.to_json(),
        })
    else:
            return HttpResponse({
                'status': 400,
                'message': 'Veuillez renseigner tous les champs'
            })

def supprimer_image_publication(request):
    code = request.GET.get('code', None)
    slug = request.GET.get('slug', None)
    if code and slug:
        utilisateur = Utilisateur.objects.get(slug=slug)
        p = Publication.objects.get(code=code)
        if p.utilisateur == utilisateur or utilisateur.profil.id == 1:
            i = ImagePublication.objects.get(publication=p)
            i.delete()
            return HttpResponse({
                'status': 200,
                'message': 'Image supprimée avec succès'
            })
        else:
            return HttpResponse({
                'status': 400,
                'message': 'Vous n\'avez pas le droit de supprimer cette image'
            })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })

def supprimer_publication(request):
    code = request.GET.get('code', None)
    slug = request.GET.get('slug', None)
    if code and slug:
        utilisateur = Utilisateur.objects.get(slug=slug)
        p = Publication.objects.get(code=code)
        if p.utilisateur == utilisateur or utilisateur.profil.id == 1:
            p.delete()
            return HttpResponse({
                'status': 200,
                'message': 'Publication supprimée avec succès'
            })
        else:
            return HttpResponse({
                'status': 400,
                'message': 'Vous n\'avez pas le droit de supprimer cette publication'
            })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })

def commenter_publication(request):
    texte = request.GET.get('texte', None)
    code = request.GET.get('code', None)
    slug = request.GET.get('slug', None)
    if texte and code and slug:
        utilisateur = Utilisateur.objects.get(slug=slug)
        p = Publication.objects.get(code=code)
        if True:
            c = Commentaire(
                texte=texte,
                publication=p,
                utilisateur=utilisateur
            )
            c.save()
            return HttpResponse({
                'status': 200,
                'message': 'Commentaire effectué avec succès',
                'commentaire': c.to_json()
            })
        
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
            })

def supprimer_commentaire(request):
    code = request.GET.get('code', None)
    slug = request.GET.get('slug', None)
    if code and slug:
        utilisateur = Utilisateur.objects.get(slug=slug)
        c = Commentaire.objects.get(code=code)
        if c.utilisateur == utilisateur or utilisateur.profil.id == 1 or c.publication.utilisateur == utilisateur:
            c.delete()
            return HttpResponse({
                'status': 200,
                'message': 'Commentaire supprimé avec succès'
            })
        else:
            return HttpResponse({
                'status': 400,
                'message': 'Vous n\'avez pas le droit de supprimer ce commentaire'
            })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })

def liste_commentaires(request):
    code = request.GET.get('code', None)
    if code:
        p = Publication.objects.get(code=code)
        c = Commentaire.objects.filter(publication=p).order_by('-id')
        return HttpResponse({
            'status': 200,
            'message': 'Liste des commentaires récupérée avec succès',
            'commentaires': [c.to_json() for c in c]
        })
    else:
        return HttpResponse({
            'status': 400,
            'message': 'Veuillez renseigner tous les champs'
        })

def liste_publications_random(request):
    if True:
        p = Publication.objects.all().order_by('?')
        return HttpResponse({
            'status': 200,
            'message': 'Liste des publications récupérée avec succès',
            'publications': [p.to_json() for p in p]
        })