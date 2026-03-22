from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger


myApp = Flask(__name__)
swagger = Swagger(myApp)

#fonction permettant la connexion entre mon API et ma base de donnee sqlite3
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialisation_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, titre TEXT, contenu TEXT, auteur TEXT, date DATE, categorie TEXT, tags TEXT)')
    conn.commit()
    conn.close()
initialisation_db()



#______________________________________DEFINITION DES ROUTES______________________________________________

#route pour la creation d'article pour le blog
@myApp.route('/articles',methods=['POST'])
def ajouter_articles() :
    """
    Creer un nouvel article
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema: 
          id: Article
          required: 
            - titre
            - contenu
            - auteur
            - date
            - categorie
            - tags 
          properties: 
            titre: 
              type: string
              description: le titre de l'article
            contenu: 
              type: string
              description: le contenu de l'article
            auteur: 
              type: string
              description: l'auteur de l'article
            date: 
              type: string
              format: date
              description: la date de publication de l'article  sous le format  "2026-03-22"
            categorie: 
              type: string
              description: la categorie de l'article
            tags: 
              type: string
              description: les tags  de l'article
            
    responses:
      201:
        description: Succès, une liste d'articles filtrée
    """

    requete = request.get_json(silent=True)

    # On vérifie d'abord si on a bien reçu un JSON
    if not requete:
        return "erreur", 400

    n_titre = requete.get('titre')
    n_contenu = requete.get('contenu')
    n_auteur = requete.get('auteur')
    n_date = requete.get('date')
    n_categorie = requete.get('categorie')
    n_tags = requete.get('tags')

    conn = get_db_connection()
    curseur = conn.execute('INSERT INTO articles (titre, contenu, auteur, date, categorie, tags) VALUES(?,?,?,?,?,?)',(n_titre, n_contenu, n_auteur,n_date, n_categorie,n_tags))
    n_id = curseur.lastrowid
    conn.commit()
    conn.close()
    #comment retourner l'id de l'article qui vient d'etre creer
    return jsonify({'message':'cree avec succes','id':n_id}),201

#route pour la lecture tous les articles du blog
@myApp.route('/api/articles' ,methods=['GET'])
def lire_articles():
    """
    Récupérer la liste complète ou filtrée par catégorie, auteur ou date
    ---
    parameters:
      - name: categorie
        in: query
        type: string
        description: filtrer par categorie
      - name: auteur
        in: query
        type: string
        description : filtrer par auteur
    responses:
      200:
        description: Succès, une liste d'articles filtrée
    """

    filtre_cat = request.args.get('categorie')
    filtre_aut = request.args.get('auteur')
    conn = get_db_connection()
    lArt = conn.execute('SELECT * FROM articles').fetchall()
    conn.close()
    dict_res = [dict(ligne)for ligne in lArt]

    if filtre_cat : 
        result = [i for i in dict_res if i['categorie'] == filtre_cat]

    elif filtre_aut :
        result = [j for j in dict_res if j['auteur'] == filtre_aut]
    else :
        result = dict_res
    
    return jsonify(result),200

#route pour la lecture d'un article specifique du blog
@myApp.route('/articleSpe/<int:id>',methods=['GET'])
def lire_article_unique(id):
    """
    Recuperer un article avec un id specifique
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required : true
        description: L'identifiant unique de l'article
    responses:
      200:
        description: article trouve
      404:
        description: article non trouve
    """
    
    conn = get_db_connection()
    requete = 'SELECT * FROM articles WHERE id =? '
    artSpe= conn.execute(requete,(id,)).fetchone()
    conn.close()
    
    resultat = dict(artSpe)
    return jsonify(resultat),200

#route pour la modification d'un article specifique du blog
@myApp.route('/articles/<int:id>',methods= ['PUT'])
def modifier_article(id):
    
    """
    Modifier un article qui existe deja
    ---
    parameters:
      - name : id
        in: path
        type: integer
        required: true
      - name : titre
        in: query
        type: string
      - name : auteur
        in: query
        type: string
      - name : contenu
        in: query
        type: string
      - name : date
        in: query
        type: string
        format : date
      - name : tags
        in: query
        type: string
      - name : categorie
        in: query
        type: string
    responses:
      200:
        description: Article modifie
      404:
        description: article non trouve

    """

    n_titre = request.args.get('titre')
    n_contenu = request.args.get('contenu')
    n_auteur = request.args.get('auteur')
    n_categorie = request.args.get('categorie')
    n_date = request.args.get('date')
    n_tags = request.args.get('tags')

    conn = get_db_connection()
    if n_titre : 
        requete = 'UPDATE articles SET titre = ? WHERE id= ?'
        conn.execute(requete,(n_titre,id))
        conn.commit()
        
    elif n_auteur : 
        requete = 'UPDATE articles SET auteur = ? WHERE id= ?'
        conn.execute(requete,(n_auteur,id))
        conn.commit()
    elif n_contenu : 
        requete = 'UPDATE articles SET contenu = ? WHERE id= ?'
        conn.execute(requete,(n_contenu,id))
        conn.commit()
    elif n_categorie : 
        requete = 'UPDATE articles SET categorie = ? WHERE id= ?'
        conn.execute(requete,(n_categorie,id))
        conn.commit()
    elif n_date : 
        requete = 'UPDATE articles SET date = ? WHERE id= ?'
        conn.execute(requete,(n_date,id))
        conn.commit()
    elif n_tags : 
        requete = 'UPDATE articles SET tags = ? WHERE id= ?'
        conn.execute(requete,(n_tags,id))
        conn.commit()
    
    conn.close()
    return jsonify({'message':'modifie avec succes'}), 200

#route pour la suppression d'un article specifique du blog
@myApp.route('/articles/<int:id>',methods= ['DELETE'])
def supprimer_articles(id):
  """
    Supprimer un article avec un id specifique
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required : true
        description: L'identifiant unique de l'article
    responses:
      200:
        description: article supprime
      404:
        description: article non trouve
    """
 
  conn =get_db_connection()
  conn.execute('DELETE FROM articles WHERE id =?',(id,))
  conn.commit()
  conn.close()
  return jsonify({'message':'suppression reussie'}),200

#route pour la recherche d'un article en fonction d'une portion de texte
@myApp.route('/articles',methods= ['GET'])
def rechercher_texte():
    """
    Rechercher des articles dont le titre ou le contenu contient un texte donné
    ---
    parameters:
      - name: q
        in: query
        type: string
        required : true
        description: mot cle ou titre
    responses:
      200:
        description: liste des article trouvee
     
    """
  
    key_word= request.args.get('q')
    if not key_word:
        return 'erreur, entrez le mot cle'
    conn = get_db_connection()
    requete = 'SELECT *FROM articles WHERE titre LIKE ? OR contenu LIKE ?'
    recherche = str(key_word)

    article = conn.execute(requete,(recherche,recherche)).fetchall()
    conn.close()
    resultat = [dict(a) for a in article]

    return jsonify(resultat), 200


if __name__ == '__main__':
    myApp.run(debug=True)