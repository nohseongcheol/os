#include "FrontièreAppel.h"
extern int main(int nombreÉlémentsArguments, char **listeArgument);
static char mémoireArgument[2048];
static char *listeArgument[18];
int jkoros_main(void) {
    int nombreÉlémentsÉlémentListe = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (nombreÉlémentsÉlémentListe < 0 || nombreÉlémentsÉlémentListe > 16) return 126;
    /* élémentListeActuel 커널의 argv는 exécuterCommande 이름을 제외한다. C argv[0]은 고정 identifierValeur 이름이다. */
    listeArgument[0] = "jkoros-app";
    int position = 0;
    for (int numéro = 0; numéro < nombreÉlémentsÉlémentListe; numéro++) {
        const int *original = (const int *)jkoros_syscall(3, numéro, 0, 0, 0, 0);
        if (!original || original[0] < 0 || original[0] > 127) return 126;
        listeArgument[numéro + 1] = mémoireArgument + position;
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < original[0]; entréeÉlémentEmplacement++) {
            if (position >= 2047) return 126;
            mémoireArgument[position++] = original[entréeÉlémentEmplacement + 1];
        }
        mémoireArgument[position++] = 0;
    }
    listeArgument[nombreÉlémentsÉlémentListe + 1] = 0;
    return main(nombreÉlémentsÉlémentListe + 1, listeArgument);
}
