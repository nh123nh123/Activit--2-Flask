# Import de la classe Flask du module Flask
from flask import Flask, render_template, session, redirect
# On importe le module os = Operating System
import os 
from questions import questions
from resultat import resultats

# Création d'une instance de la classe Flask = notre app
app = Flask("Ma premiere app")
# On définit notre secret_key pour pouvoir créer des cookies de session
app.secret_key = os.urandom(24)

# Route de la page d'accueil
# On crée notre premier page qui sera l'URL racine /, la fonction index sera appelée.
# On renvoie ce que la fonction index renvoie.
@app.route('/')
def index():
    session["nb_question"]=0
    session["score"]={"Pikachu" : 0, "Mew" : 0, "Salamèche" : 0, "Carapuce" : 0, "Evoli" : 0}
    return render_template("index.html")

# Route pour la question
@app.route("/question")
def question():
    # On accède à la variable global questions
    global questions
    nb_question = session["nb_question"]
    # S'il reste des questions à afficher
    if nb_question <len(questions) :
       # On récupère l'énoncé
       enonce = questions[nb_question]["enonce"]
       # On copie le dictionnaire qui stocke la question et les réponses possibles
       question_copy = questions[nb_question].copy()
       question_copy.pop("enonce")
       # On récupère les questions
       reponses = list(question_copy.values())
       # On récupère les clefs associées = pour les scores
       clefs = list(question_copy.keys())
       # Cookie pour stocker l'ordre des réponses -> sert pour le score
       session["clefs"] = clefs
       # On affiche la page question avec les différentes réponses possibles       
       return render_template("question.html", question = enonce, reponses = reponses)
    else :
        global resultats
        # On trie les scores dans l'odre décroissant
        score = sorted(session["score"], key=session["score"].get , reverse = True)
        # On stocke le nom du vainqueur -> Premier de la liste score
        vainqueur = score[0]
        # On récupère la description associé au vainqueur
        description = resultats[vainqueur]
        return render_template("resultat.html", vainqueur = vainqueur, description = description)
   
    

# Route pour la sélection d'une réponse puis redirection vers la prochaine question
@app.route("/reponse/<numero>")
def reponse(numero):
    session["nb_question"] += 1
    resultat = session["clefs"][int(numero)]
    session["score"][resultat] += 1
    print(session["score"])
    return redirect("/question")









# Execution de l'application 
# host='0.0.0.0' = le serveur Flask écoute sur toutes les adresses IP
# port = 81 -> port d'écoute de l'app avec lequel on accède à l'application
app.run(host='0.0.0.0', port = 81)