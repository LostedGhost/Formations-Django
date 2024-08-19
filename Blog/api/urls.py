from django.urls import path
from api.views import *

urlpatterns = [
    path('inscription/', inscription, name="inscription"),
    path('connexion/', connexion, name="connexion"),
    path('publication/add/', creer_publication, name="creer_publication"),
    path('publication/image/add/', ajout_image_publication, name="ajout_image_publication"),
    path('publication/image/remove/', supprimer_image_publication, name="supprimer_image_publication"),
    path('publication/delete/', supprimer_publication, name="supprimer_publication"),
    path('publications/', liste_publications_random, name="lister_publication"),
    path('commentaire/add/',commenter_publication, name="commenter_publication"),
    path('commentaire/delete/',supprimer_commentaire, name="supprimer_commentaire"),
    path('commentaire/liste/',liste_commentaires, name="liste_commentaires"),
]
