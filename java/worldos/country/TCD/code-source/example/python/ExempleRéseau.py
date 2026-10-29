from français import Sortie, ouvrirDatagramme, envoyerDatagrammeExtérieur, recevoirDatagramme, fermerRéseau, millisecondes
from français import ErreurSystème, ErreurEncoreEssayer, encoderTexte, argumentsCommande, Entier
extrémité = ouvrirDatagramme(0)
try:
    datagramme = encoderTexte("PYTHON UDP français")
    envoyerDatagrammeExtérieur(extrémité, "10.0.2.2", Entier(argumentsCommande[1]), datagramme)
    lancer = millisecondes()
    while True:
        try:
            réponse, valeurPort = recevoirDatagramme(extrémité)
            break
        except ErreurSystème as erreur:
            if erreur.numéro != ErreurEncoreEssayer or millisecondes() - lancer >= 700:
                raise
    assert réponse == datagramme
    Sortie("PYTHON 네트워크 vérifier: UDP français")
finally:
    fermerRéseau(extrémité)
