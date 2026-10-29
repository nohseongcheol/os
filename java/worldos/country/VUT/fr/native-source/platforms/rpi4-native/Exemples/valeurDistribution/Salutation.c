#include <ABIFichier.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int nombreÉlémentsArguments, char **listeArgument) {
    if (nombreÉlémentsArguments < 1 || !listeArgument[0]) return 2;
    const char salutation[] = "interne 커널의 C와 français POSIX\n";
    int Documentation = ouvrirFichier("Salutation.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Documentation < 0) return 1;
    typeRésultatEntréeSortie longueur = écrireDonnéesFichier(Documentation, salutation, sizeof(salutation) - 1);
    fermerFichier(Documentation);
    écrireDonnéesFichier(1, salutation, sizeof(salutation) - 1);
    return longueur == sizeof(salutation) - 1 ? 0 : 3;
}
