#ifndef entêteAppelUtilisateurNatif
#define entêteAppelUtilisateurNatif
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=invoquer numéro, x0..x5=arguments, x0=résultat/valeurNégatif erreur. Linux ABI 아님.
static inline intptr_t invoquerUtilisateur(uintptr_t numéro, uintptr_t opérandePremier, uintptr_t opérandeDeuxième, uintptr_t opérandeTroisième,
                                uintptr_t opérandeQuatrième, uintptr_t opérandeCinquième, uintptr_t opérandeSixième) {
    register uintptr_t registreZéro __asm__("x0") = opérandePremier;
    register uintptr_t registreUn __asm__("x1") = opérandeDeuxième;
    register uintptr_t registreDeux __asm__("x2") = opérandeTroisième;
    register uintptr_t registreTrois __asm__("x3") = opérandeQuatrième;
    register uintptr_t registreQuatre __asm__("x4") = opérandeCinquième;
    register uintptr_t registreCinq __asm__("x5") = opérandeSixième;
    register uintptr_t registreHuit __asm__("x8") = numéro;
    __asm__ volatile("svc #0" : "+r"(registreZéro) : "r"(registreUn), "r"(registreDeux), "r"(registreTrois), "r"(registreQuatre), "r"(registreCinq), "r"(registreHuit) : "memory", "cc");
    return (intptr_t)registreZéro;
}
static inline intptr_t rectangleÉcran(unsigned coordonnéeCoordonnéeHorizontale, unsigned coordonnéeCoordonnéeVerticale, unsigned valeurLargeurDemandé, unsigned valeurHauteurDemandé, unsigned couleurRGB) {
    return invoquerUtilisateur(13, coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale, couleurRGB, valeurLargeurDemandé, valeurHauteurDemandé, 0);
}
static inline intptr_t finMémoireUtilisateur(uintptr_t terminaison) { return invoquerUtilisateur(8, terminaison, 0, 0, 0, 0, 0); }
static inline intptr_t lireLargeurÉcran(void) { return invoquerUtilisateur(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t lireHauteurÉcran(void) { return invoquerUtilisateur(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t attendreToucheÉcranPour(void) {
    intptr_t résultat = invoquerUtilisateur(16, 0, 0, 0, 0, 0, 0);
    if (résultat < 0) return résultat;
    do { résultat = invoquerUtilisateur(16, 1, 0, 0, 0, 0, 0); } while (résultat == -11);
    invoquerUtilisateur(16, 2, 0, 0, 0, 0, 0);
    return résultat;
}
static inline intptr_t nombreÉlémentsArgumentUtilisateur(void) { return invoquerUtilisateur(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t argumentUtilisateur(unsigned numéro, char *valeurContenuValeur, size_t taille) {
    return invoquerUtilisateur(15, numéro, (uintptr_t)valeurContenuValeur, taille, 0, 0, 0);
}
#endif
