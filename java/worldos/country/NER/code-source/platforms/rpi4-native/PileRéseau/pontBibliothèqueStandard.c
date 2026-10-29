#include "string.h"
size_t strlen(const char *donnéesChaîne) { const char *positionDonnées = donnéesChaîne; while (*positionDonnées) positionDonnées++; return positionDonnées - donnéesChaîne; }
int memcmp(const void *valeurPremier, const void *valeurDeuxième, size_t nombreÉlémentsÉlémentListe) { const unsigned char *coordonnéeCoordonnéeHorizontale = valeurPremier, *coordonnéeCoordonnéeVerticale = valeurDeuxième; while (nombreÉlémentsÉlémentListe--) { if (*coordonnéeCoordonnéeHorizontale != *coordonnéeCoordonnéeVerticale) return (int)*coordonnéeCoordonnéeHorizontale - *coordonnéeCoordonnéeVerticale; coordonnéeCoordonnéeHorizontale++; coordonnéeCoordonnéeVerticale++; } return 0; }
void *memmove(void *donnéesDestination, const void *donnéesChaîne, size_t nombreÉlémentsÉlémentListe) { unsigned char *coordonnéeCoordonnéeHorizontale = donnéesDestination; const unsigned char *coordonnéeCoordonnéeVerticale = donnéesChaîne; if (coordonnéeCoordonnéeHorizontale < coordonnéeCoordonnéeVerticale) { for (size_t indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) coordonnéeCoordonnéeHorizontale[indiceOrdinal] = coordonnéeCoordonnéeVerticale[indiceOrdinal]; } else { while (nombreÉlémentsÉlémentListe) { nombreÉlémentsÉlémentListe--; coordonnéeCoordonnéeHorizontale[nombreÉlémentsÉlémentListe] = coordonnéeCoordonnéeVerticale[nombreÉlémentsÉlémentListe]; } } return donnéesDestination; }
int strncmp(const char *valeurPremier, const char *valeurDeuxième, size_t nombreÉlémentsÉlémentListe) { while (nombreÉlémentsÉlémentListe--) { unsigned char coordonnéeCoordonnéeHorizontale = *valeurPremier++, coordonnéeCoordonnéeVerticale = *valeurDeuxième++; if (coordonnéeCoordonnéeHorizontale != coordonnéeCoordonnéeVerticale) return (int)coordonnéeCoordonnéeHorizontale-coordonnéeCoordonnéeVerticale; if (!coordonnéeCoordonnéeHorizontale) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *donnéesChaîne, char **décalageFin, int valeurArrièrePlan) {
    const char *démarrerDécalage = donnéesChaîne; unsigned long valeur = 0; int valeurEncodage = 1, valeurQuelconque = 0;
    while (*donnéesChaîne == ' ' || (*donnéesChaîne >= 9 && *donnéesChaîne <= 13)) donnéesChaîne++;
    if (*donnéesChaîne == '-' || *donnéesChaîne == '+') { if (*donnéesChaîne == '-') valeurEncodage = -1; donnéesChaîne++; }
    if (valeurArrièrePlan == 0) valeurArrièrePlan = 10;
    while (*donnéesChaîne >= '0' && *donnéesChaîne <= '9' && *donnéesChaîne - '0' < valeurArrièrePlan) {
        unsigned valeurChiffre = *donnéesChaîne++ - '0'; valeurQuelconque = 1;
        if (valeur > (0x7ffffffffffffffful - valeurChiffre) / (unsigned)valeurArrièrePlan) valeur = 0x7ffffffffffffffful;
        else valeur = valeur * valeurArrièrePlan + valeurChiffre;
    }
    if (décalageFin) *décalageFin = (char *)(valeurQuelconque ? donnéesChaîne : démarrerDécalage); return valeurEncodage > 0 ? (long)valeur : -(long)valeur;
}
int atoi(const char *donnéesChaîne) { return (int)strtol(donnéesChaîne, 0, 10); }
