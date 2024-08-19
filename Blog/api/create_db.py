from api.models import *

p=Profil(nom="Administrateur")
p.save()

p=Profil(nom="Publicateur")
p.save()

u=Utilisateur(
    nom="TOPANOU",
    prenom="Ludel",
    email="topanoulucio@gmail.com",
    motDePasse=chiffrement("Lucio@7410"),
    profil_id=1
)
u.save()