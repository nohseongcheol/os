#include "ABIFichier.h"
class GestionnaireDocument {
    int numéro;
public:
    GestionnaireDocument(const char *nom) : numéro(ouvrirFichier(nom, ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600)) {}
    ~GestionnaireDocument() { if (numéro >= 0) fermerFichier(numéro); }
    typeRésultatEntréeSortie écrire(const char *Données, typeNombreÉlémentsOctet taille) { return écrireDonnéesFichier(numéro, Données, taille); }
};
extern "C" int démarrerProgrammeUtilisateur(int arguments) {
    (void)arguments;
    const char salutation[] = "C++에서 한글 클래스와 posix-kor invoquer\n";
    GestionnaireDocument Documentation("C++Salutation.txt");
    écrireDonnéesFichier(1, salutation, sizeof(salutation) - 1);
    return Documentation.écrire(salutation, sizeof(salutation) - 1) == sizeof(salutation) - 1 ? 0 : 1;
}
