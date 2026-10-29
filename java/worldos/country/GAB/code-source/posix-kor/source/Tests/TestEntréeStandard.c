#include <ABIFichier.h>
#include <stdio.h>
#include <string.h>
int main(int nombreÉlémentsÉlémentListe, char **listeEntréeÉlément) {
    (void)nombreÉlémentsÉlémentListe; (void)listeEntréeÉlément;
    char Données[6]; int longueur = 0;
    puts("POSIX INPUT READY");
    while (longueur < 6) {
        int résultat = lireDonnéesFichier(0, Données + longueur, 6 - longueur);
        if (résultat <= 0) return 1;
        longueur += résultat;
    }
    if (memcmp(Données, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
