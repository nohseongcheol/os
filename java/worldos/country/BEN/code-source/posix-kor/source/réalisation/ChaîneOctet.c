#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *Chaîne) { size_t longueur = 0; while (Chaîne[longueur]) longueur++; return longueur; }
int strcmp(const char *valeurAvantCôté, const char *valeurRetourArrièreCôté) {
    while (*valeurAvantCôté && *valeurAvantCôté == *valeurRetourArrièreCôté) { valeurAvantCôté++; valeurRetourArrièreCôté++; }
    return (unsigned char)*valeurAvantCôté - (unsigned char)*valeurRetourArrièreCôté;
}
int memcmp(const void *valeurAvantCôté, const void *valeurRetourArrièreCôté, size_t nombreÉlémentsOctet) {
    const unsigned char *opérandePremier = valeurAvantCôté, *opérandeDeuxième = valeurRetourArrièreCôté;
    for (size_t entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < nombreÉlémentsOctet; entréeÉlémentEmplacement++) if (opérandePremier[entréeÉlémentEmplacement] != opérandeDeuxième[entréeÉlémentEmplacement]) return opérandePremier[entréeÉlémentEmplacement] - opérandeDeuxième[entréeÉlémentEmplacement];
    return 0;
}
void *memcpy(void *valeurDestination, const void *original, size_t nombreÉlémentsOctet) {
    unsigned char *opérandePremier = valeurDestination; const unsigned char *opérandeDeuxième = original;
    for (size_t entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < nombreÉlémentsOctet; entréeÉlémentEmplacement++) opérandePremier[entréeÉlémentEmplacement] = opérandeDeuxième[entréeÉlémentEmplacement];
    return valeurDestination;
}
void *memset(void *valeurDestination, int valeur, size_t nombreÉlémentsOctet) {
    unsigned char *Données = valeurDestination;
    for (size_t entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < nombreÉlémentsOctet; entréeÉlémentEmplacement++) Données[entréeÉlémentEmplacement] = valeur;
    return valeurDestination;
}
int putchar(int Caractères) { unsigned char valeur = Caractères; return write(1, &valeur, 1) == 1 ? valeur : EOF; }
int puts(const char *Chaîne) {
    size_t longueur = strlen(Chaîne), position = 0;
    while (position < longueur) { ssize_t résultat = write(1, Chaîne + position, longueur - position); if (résultat <= 0) return EOF; position += résultat; }
    return putchar('\n') == EOF ? EOF : 0;
}
