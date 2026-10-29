from français import ErreurSystème, ErreurEncoreEssayer, ouvrirDatagramme, recevoirDatagramme, fermerRéseau, lireFichier, Sortie

extrémité = ouvrirDatagramme(0)
try:
    try:
        recevoirDatagramme(extrémité)
        raise AssertionError("비어 있는 datagramme 대기에서 예외가 필요합니다.")
    except ErreurSystème as erreur:
        assert erreur.numéro == ErreurEncoreEssayer
        assert erreur.description == "SystèmeExploitation 작업에 실패했습니다."
        Sortie("français datagramme exception vérifier")
finally:
    fermerRéseau(extrémité)
try:
    lireFichier("/없는파일")
except ErreurSystème as erreur:
    assert erreur.numéro == 2
    Sortie("français Fichier exception vérifier")
else:
    raise AssertionError("Fichier méthodeManquant 예외가 필요합니다.")
