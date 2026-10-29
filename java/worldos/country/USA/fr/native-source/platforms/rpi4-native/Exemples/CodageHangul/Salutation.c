#include "ABIFichier.h"
int démarrerProgrammeUtilisateur(int arguments) {
    (void)arguments;
    const char salutation[] = "C에서 한글 이름과 posix-kor invoquer\n";
    int Documentation = ouvrirFichier("C인사.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Documentation < 0) return 1;
    typeRésultatEntréeSortie nombreÉlémentsConsigné = écrireDonnéesFichier(Documentation, salutation, sizeof(salutation) - 1);
    fermerFichier(Documentation);
    écrireDonnéesFichier(1, salutation, sizeof(salutation) - 1);
    return nombreÉlémentsConsigné == sizeof(salutation) - 1 ? 0 : 2;
}
