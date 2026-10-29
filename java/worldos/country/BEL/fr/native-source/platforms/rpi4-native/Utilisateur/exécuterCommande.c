#include "../nommage/nomsLierMachine.h"
#include "invoquer.h"
typedef void (*méthodeInitialiseur)(void);
extern méthodeInitialiseur __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int démarrerProgrammeUtilisateur(int);
int démarrerUtilisateur(int valeurTransféré) {
    for (méthodeInitialiseur *positionDonnées = __init_array_start; positionDonnées < __init_array_end; positionDonnées++) (*positionDonnées)();
    int résultat = démarrerProgrammeUtilisateur(valeurTransféré);
    for (méthodeInitialiseur *positionDonnées = __fini_array_end; positionDonnées != __fini_array_start;) (*--positionDonnées)();
    return résultat;
}
void *memset(void *positionDonnées, int valeur, size_t nombreÉlémentsEntréeÉlément) { unsigned char *donnéesDestination = positionDonnées; while (nombreÉlémentsEntréeÉlément--) *donnéesDestination++ = valeur; return positionDonnées; }
void *memcpy(void *donnéesDestination, const void *donnéesChaîne, size_t nombreÉlémentsEntréeÉlément) { unsigned char *valeurPremier = donnéesDestination; const unsigned char *valeurDeuxième = donnéesChaîne; while (nombreÉlémentsEntréeÉlément--) *valeurPremier++ = *valeurDeuxième++; return donnéesDestination; }
