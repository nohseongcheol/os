#include <ABIFichier.h>
#include <stdio.h>
int main(int nombreÉlémentsÉlémentListe, char **listeEntréeÉlément) {
    (void)nombreÉlémentsÉlémentListe; (void)listeEntréeÉlément;
    int Fichier = ouvrirFichier("stored.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600);
    if (Fichier < 0 || écrireDonnéesFichier(Fichier, "saved-from-C", 12) != 12) return 1;
    if (stockageFichierConfirmer(Fichier) < 0) return 2;
    if (fermerFichier(Fichier) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
