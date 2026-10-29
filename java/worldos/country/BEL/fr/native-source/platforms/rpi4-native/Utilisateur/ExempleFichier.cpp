#include "ABIFichier.h"
#include "invoquer.h"
static int valeurInitialiseur;
static volatile int graineInitialiseur = 72;
static volatile double grainePointFlottant = 1.25;
static int nombreÉlémentsDestruction;
struct testInitialisation { testInitialisation() { valeurInitialiseur = graineInitialiseur + 1; } } initialiserZoneStatique;
class fichierAutomatique {
    int numéro;
public:
    explicit fichierAutomatique(const char *nom) : numéro(ouvrirFichier(nom, ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600)) {}
    ~fichierAutomatique() { if (numéro >= 0) fermerFichier(numéro); nombreÉlémentsDestruction++; }
    int entréeÉlémentDescripteur() const { return numéro; }
};
extern "C" int démarrerProgrammeUtilisateur(int) {
    if (valeurInitialiseur != 73 || invoquerUtilisateur(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double valeurPointFlottant = grainePointFlottant * 2.0 + 0.5;
    if (invoquerUtilisateur(0, 0, 0, 0, 0, 0, 0) != 1 || valeurPointFlottant != 3.0) return 16;
    static const char valeurContenuValeur[] = "EL0 C++ → posix-kor → Java Fichier · 안녕하세요 😀\n";
    char lireValeur[sizeof(valeurContenuValeur)] = {};
    {
        fichierAutomatique Fichier("Utilisateur.txt");
        int numéro = Fichier.entréeÉlémentDescripteur();
        if (numéro < 0 || écrireDonnéesFichier(numéro, valeurContenuValeur, sizeof(valeurContenuValeur)) != sizeof(valeurContenuValeur)) return 2;
        if (positionnerFichier(numéro, 0, DébutDepuis) || lireDonnéesFichier(numéro, lireValeur, sizeof(lireValeur)) != sizeof(lireValeur)) return 3;
        for (unsigned indiceOrdinal = 0; indiceOrdinal < sizeof(valeurContenuValeur); indiceOrdinal++) if (lireValeur[indiceOrdinal] != valeurContenuValeur[indiceOrdinal]) return 4;
    }
    if (nombreÉlémentsDestruction != 1) return 5;
    if (écrireDonnéesFichier(1, valeurContenuValeur, sizeof(valeurContenuValeur) - 1) != sizeof(valeurContenuValeur) - 1) return 6;
    uintptr_t entréeÉlémentBasExtrémité = finMémoireUtilisateur(0);
    if (entréeÉlémentBasExtrémité != 0x02c00000 || finMémoireUtilisateur(entréeÉlémentBasExtrémité + 8192) != (intptr_t)(entréeÉlémentBasExtrémité + 8192)) return 7;
    volatile unsigned char *Mémoire = (volatile unsigned char *)entréeÉlémentBasExtrémité;
    if (Mémoire[0] || Mémoire[8191]) return 8;
    Mémoire[8191] = 137;
    if (finMémoireUtilisateur(entréeÉlémentBasExtrémité) != (intptr_t)entréeÉlémentBasExtrémité || finMémoireUtilisateur(entréeÉlémentBasExtrémité + 8192) != (intptr_t)(entréeÉlémentBasExtrémité + 8192) || Mémoire[8191]) return 9;
    // 잘못된 Utilisateur pointeur/번호는 오류이며 커널을 중단하지 않는다.
    if (écrireDonnéesFichier(1, (const void *)0x80000, 8) != -1 || numéroErreur != 14) return 10;
    if (lireDonnéesFichier(0, (void *)valeurContenuValeur, 1) != -1 || numéroErreur != 14) return 11;
    if (invoquerUtilisateur(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t étendueÉcran = lireLargeurÉcran(), longueurÉcran = lireHauteurÉcran();
    if (étendueÉcran <= 0 || longueurÉcran <= 0 || invoquerUtilisateur(13, étendueÉcran-1, longueurÉcran-1, 0, 2, 2, 0) != -22) return 13;
    if (rectangleÉcran(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 programmeQuitter 시 열린 서술자가 자동 정리되어야 한다.
    if (ouvrirFichier("Utilisateur.txt", lireValeurSeulement) < 0) return 15;
    return 0;
}
