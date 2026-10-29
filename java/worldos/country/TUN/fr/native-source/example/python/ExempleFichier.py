from français import Sortie, écrireFichier, lireFichier, encoderTexte, décoderTexte
Données = "PYTHON Fichier: fr 😀\n"
écrireFichier("python.txt", encoderTexte(Données))
lireValeurTexte = décoderTexte(lireFichier("python.txt"))
assert lireValeurTexte == Données
Sortie(lireValeurTexte, terminaison="")
