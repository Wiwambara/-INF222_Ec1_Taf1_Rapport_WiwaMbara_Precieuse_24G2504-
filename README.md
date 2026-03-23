# -INF222_Ec1_Taf1_Rapport_WiwaMbara_Precieuse_24G2504-

#API DE GESTION DE BLOG


Ce projet est une API REST developpee avec le framework Flask, permettant de gerer les articles d'un blog. Elle utilise SQLite3 pour le 
stckage des données et Flasgger(Swagger pour la documentation active)

## Installation 
suivez ces etapes pour pouvoir l'installer

###1.Clonner le depot
```bash
git clone https://github.com/Wiwambara/-INF222_Ec1_Taf1_Rapport_WiwaMbara_Precieuse_24G2504-.git
cd code
```
###2.Clonner le depot
Assurer vous d'avoir python ainsi que les bibliothèques necessaires installées
```bash
pip install flask flasgger
```

###3.Lancer l'application

```bash
python api.py
```

##Documentation Swagger
Une fois l'application lancée, vous pouvez tester tous les endpoints via l'interface interactive Swagger à l'adresse suivante : http://127.0.0.1:5000/apidocs/

##Endpoints de l'API

METHODES              |             ENDPOINTS               |                 DESCRIPTION
_____________________________________________________________________________________________________________________________________
POST                  |             /articles               |     Créer un nouvel article (format JSON).
_____________________________________________________________________________________________________________________________________
GET                   |            /api/articles            |     Lister tous les articles (filtres categorie ou auteur possibles).
_____________________________________________________________________________________________________________________________________
GET                   |           /articleSpe/<id>          |     Récupérer un article spécifique via son ID unique.
_____________________________________________________________________________________________________________________________________
PUT                   |           /articles/<id>            |     Modifier un article (via paramètres de requête).
_____________________________________________________________________________________________________________________________________
DELETE_               |            /articles/<id>           |      Supprimer définitivement un article
_____________________________________________________________________________________________________________________________________
GET                   |             /articles               |      Rechercher un article par mot-clé dans le titre ou le contenu.
_____________________________________________________________________________________________________________________________________

##Exemple d'utilisation

####Creer un article : http://127.0.0.1:5000/articles

```
 {
  "titre": "Mon premier article",
  "contenu": "Ceci est le contenu de mon article.",
  "auteur": "Précieuse",
  "date": "2026-03-23",
  "categorie": "Informatique",
  "tags": "python, flask, api"
}
```
####Chercher un article
Pour chercher un article contenant le mot python : http://127.0.0.1:5000/articles?q=python

####Filtrer par catégorie
Pour voir uniquement les articles de la catégorie "Informatique" : http://127.0.0.1:5000/api/articles?categorie=Informatique

####Modifier un article 
Pour changer le titre de l'article n°1 : http://127.0.0.1:5000/articles/1?titre=Nouveau Titre

Developpe par Precieuse -2026
