"""interne 커널의 Fichier·Communication·Écran 호출과 français exception. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as SystèmeExploitation
import sys as EnvironnementExécution

def Sortie(*valeur, séparateur=" ", terminaison="\n", **argumentsAncienSystème):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in argumentsAncienSystème: argumentsAncienSystème["sep"] = séparateur
    if "end" not in argumentsAncienSystème: argumentsAncienSystème["end"] = terminaison
    print(*valeur, **argumentsAncienSystème)

Entier = int
argumentsCommande = EnvironnementExécution.argv
ErreurEncoreEssayer = 11

class ErreurSystème(OSError):
    def __init__(valeurSoi, numéro, description="SystèmeExploitation 작업에 실패했습니다."):
        super().__init__(numéro, description)
        valeurSoi.numéro = numéro
        valeurSoi.description = description

def invoquerSystème(Fonction, *arguments):
    try:
        return Fonction(*arguments)
    except OSError as erreur:
        numéro = erreur.args[0] if erreur.args else 0
        raise ErreurSystème(numéro)

def encoderTexte(texte):
    return texte.encode("utf-8")

def décoderTexte(Données):
    return Données.decode("utf-8")

def lireFichier(nom):
    return invoquerSystème(SystèmeExploitation.read, nom)

def écrireFichier(nom, Données):
    return invoquerSystème(SystèmeExploitation.write, nom, Données)

def supprimerFichier(nom):
    return invoquerSystème(SystèmeExploitation.remove, nom)

def ouvrirDatagramme(numéroPort):
    return invoquerSystème(SystèmeExploitation.udp_open, numéroPort)

def envoyerDatagramme(extrémité, numéroPort, Données):
    return invoquerSystème(SystèmeExploitation.udp_send, extrémité, numéroPort, Données)

def envoyerDatagrammeExtérieur(extrémité, adresse, numéroPort, Données):
    return invoquerSystème(SystèmeExploitation.udp_sendto, extrémité, adresse, numéroPort, Données)

def recevoirDatagramme(extrémité):
    return invoquerSystème(SystèmeExploitation.udp_recv, extrémité)

def fermerRéseau(extrémité):
    return invoquerSystème(SystèmeExploitation.udp_close, extrémité)

def dessinerRectangle(*arguments):
    return invoquerSystème(SystèmeExploitation.rect, *arguments)

def tailleÉcran():
    return invoquerSystème(SystèmeExploitation.screen_size)

def attendreDessinPour():
    return invoquerSystème(SystèmeExploitation.wait_key)

millisecondes = SystèmeExploitation.ticks_ms
