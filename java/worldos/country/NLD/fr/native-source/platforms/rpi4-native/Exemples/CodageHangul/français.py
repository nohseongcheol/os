"""interne valeurNoyau MicroPython에서 사용하는 한글 Fonction nom."""
import jkoros as SystèmeExploitation
Sortie = print
lireFichier = SystèmeExploitation.read
écrireFichier = SystèmeExploitation.write
supprimerFichier = SystèmeExploitation.remove
lireEntrée = SystèmeExploitation.stdin
dessinerRectangle = SystèmeExploitation.rect
attendreDessinPour = SystèmeExploitation.wait_key
millisecondes = SystèmeExploitation.ticks_ms
ouvrirDatagramme = SystèmeExploitation.udp_open
envoyerDatagramme = SystèmeExploitation.udp_send
envoyerDatagrammeExtérieur = SystèmeExploitation.udp_sendto
recevoirDatagramme = SystèmeExploitation.udp_recv
fermerRéseau = SystèmeExploitation.udp_close

def décoderTexte(Données):
    return Données.decode("utf-8")
