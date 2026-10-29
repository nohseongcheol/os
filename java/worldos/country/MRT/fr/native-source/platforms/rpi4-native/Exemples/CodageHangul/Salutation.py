import français

def saluer(nom):
    salutation = "안녕하세요 " + nom
    français.écrireFichier("Salutation.txt", salutation)
    français.Sortie(français.décoderTexte(français.lireFichier("Salutation.txt")))

saluer("누리")
