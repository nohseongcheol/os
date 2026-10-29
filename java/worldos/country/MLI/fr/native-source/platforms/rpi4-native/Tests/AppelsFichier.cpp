#include "../nommage/nomsLierMachine.h"
#include "ABIFichier.h"
// 표준 C++ bibliothèque 없는 freestanding C++11 Programme. 커널에 valeurStatique 링크한다.
extern "C" uintptr_t testProgrammesCpp(void) {
    const char valeurContenuValeur[] = "C++ → Java valeurNoyau · 한글 😀";
    unsigned char lireValeur[sizeof(valeurContenuValeur)] = {};
    int Fichier = ouvrirFichier("Tests.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Fichier < 0) return 1;
    if (écrireDonnéesFichier(Fichier, valeurContenuValeur, sizeof(valeurContenuValeur)) != sizeof(valeurContenuValeur)) return 2;
    if (positionnerFichier(Fichier, 0, DébutDepuis) != 0) return 3;
    if (lireDonnéesFichier(Fichier, lireValeur, sizeof(lireValeur)) != sizeof(lireValeur)) return 4;
    for (size_t indiceOrdinal = 0; indiceOrdinal < sizeof(valeurContenuValeur); indiceOrdinal++) if (lireValeur[indiceOrdinal] != (unsigned char)valeurContenuValeur[indiceOrdinal]) return 5;
    if (lireDonnéesFichier(Fichier, lireValeur, 1) != 0) return 6;
    if (stockageFichierConfirmer(Fichier) != -1 || numéroErreur != 38) return 7;
    if (fermerFichier(Fichier) || fermerFichier(Fichier) != -1 || numéroErreur != 9) return 8;
    Fichier = ouvrirFichier("Tests.txt", lireValeurSeulement);
    if (Fichier < 0 || écrireDonnéesFichier(Fichier, valeurContenuValeur, 1) != -1 || numéroErreur != 9) return 9;
    if (fermerFichier(Fichier)) return 10;
    Fichier = ouvrirFichier("Tests.txt", ÉcrireLire | ajouterFinFinÀPosition);
    if (Fichier < 0 || positionnerFichier(Fichier, 0, DébutDepuis) != 0 || écrireDonnéesFichier(Fichier, "!", 1) != 1 || tailleFichier(Fichier) != sizeof(valeurContenuValeur) + 1) return 11;
    if (définirLongueurFichier(Fichier, 2) || positionnerFichier(Fichier, 4, DébutDepuis) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (écrireDonnéesFichier(Fichier, "x", 1) != 1 || tailleFichier(Fichier) != 3 || fermerFichier(Fichier)) return 13;
    Fichier = ouvrirFichier("구멍.bin", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Fichier < 0 || positionnerFichier(Fichier, 3, DébutDepuis) != 3 || écrireDonnéesFichier(Fichier, "z", 1) != 1) return 14;
    if (positionnerFichier(Fichier, 0, DébutDepuis) != 0 || lireDonnéesFichier(Fichier, lireValeur, 4) != 4 || lireValeur[0] || lireValeur[1] || lireValeur[2] || lireValeur[3] != 'z') return 15;
    if (supprimerNomEntréeÉlémentFichier("구멍.bin") || tailleFichier(Fichier) != 4 || fermerFichier(Fichier)) return 16;
    if (ouvrirFichier("구멍.bin", lireValeurSeulement) != -1 || numéroErreur != 2) return 17;
    if (ouvrirFichier("Tests.txt", ÉcrireLire | créerFichierNouveau, 0600) != -1 || numéroErreur != 17) return 18;
    if (ouvrirFichier("../valeurProhibé", lireValeurSeulement) != -1) return 19;
    return 0;
}
