#include <ABIRéseau.h>
#include <errno.h>
#include "FrontièreAppel.h"

int socket(int schémaAdresse, int genreRéseau, int numéroContrat) {
    return résultatInvocation(jkoros_syscall(41, schémaAdresse, genreRéseau, numéroContrat, 0, 0));
}
int bind(int descripteurFichier, const struct sockaddr *adresse, socklen_t longueurAdresse) {
    return résultatInvocation(jkoros_syscall(42, descripteurFichier, (int)adresse, longueurAdresse, 0, 0));
}
ssize_t sendto(int descripteurFichier, const void *Données, size_t nombreÉlémentsOctet, int réglages,
               const struct sockaddr *adresse, socklen_t longueurAdresse) {
    int requête[2] = {(int)adresse, longueurAdresse};
    return résultatInvocation(jkoros_syscall(43, descripteurFichier, (int)Données, nombreÉlémentsOctet, réglages, (int)requête));
}
ssize_t recvfrom(int descripteurFichier, void *Données, size_t nombreÉlémentsOctet, int réglages,
                 struct sockaddr *adresse, socklen_t *longueurAdresse) {
    int requête[2] = {(int)adresse, (int)longueurAdresse};
    return résultatInvocation(jkoros_syscall(44, descripteurFichier, (int)Données, nombreÉlémentsOctet, réglages, (int)requête));
}
int getsockname(int descripteurFichier, struct sockaddr *adresse, socklen_t *longueurAdresse) {
    return résultatInvocation(jkoros_syscall(45, descripteurFichier, (int)adresse, (int)longueurAdresse, 0, 0));
}
int setsockopt(int descripteurFichier, int valeurCouche, int nomRéglages, const void *valeur, socklen_t longueurValeur) {
    if (valeurCouche != SOL_SOCKET || nomRéglages != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!valeur) { errno = EFAULT; return -1; }
    if (longueurValeur != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *valeurTemps = valeur;
    if (valeurTemps->tv_sec < 0 || valeurTemps->tv_sec > 2 || valeurTemps->tv_usec < 0 || valeurTemps->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int millisecondes = valeurTemps->tv_sec * 1000 + (valeurTemps->tv_usec + 999) / 1000;
    return résultatInvocation(jkoros_syscall(46, descripteurFichier, millisecondes, 0, 0, 0));
}
uint16_t htons(uint16_t valeur) { return (valeur << 8) | (valeur >> 8); }
uint16_t ntohs(uint16_t valeur) { return htons(valeur); }
uint32_t htonl(uint32_t valeur) {
    return (valeur << 24) | ((valeur << 8) & 0xff0000U) | ((valeur >> 8) & 0xff00U) | (valeur >> 24);
}
uint32_t ntohl(uint32_t valeur) { return htonl(valeur); }
int inet_pton(int schémaAdresse, const char *Chaîne, void *adresse) {
    if (schémaAdresse != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!Chaîne || !adresse) { errno = EFAULT; return -1; }
    unsigned char valeurTemporaire[4];
    for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 4; entréeÉlémentEmplacement++) {
        int valeur = 0, chiffres = 0;
        const char *lancer = Chaîne;
        while (*Chaîne >= '0' && *Chaîne <= '9') {
            if (++chiffres > 3) return 0;
            valeur = valeur * 10 + *Chaîne++ - '0';
        }
        if (!chiffres || valeur > 255 || (chiffres > 1 && *lancer == '0')) return 0;
        valeurTemporaire[entréeÉlémentEmplacement] = valeur;
        if (entréeÉlémentEmplacement < 3) { if (*Chaîne++ != '.') return 0; }
        else if (*Chaîne) return 0;
    }
    for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 4; entréeÉlémentEmplacement++) ((unsigned char *)adresse)[entréeÉlémentEmplacement] = valeurTemporaire[entréeÉlémentEmplacement];
    return 1;
}
const char *inet_ntop(int schémaAdresse, const void *adresse, char *Chaîne, socklen_t valeurCapacité) {
    if (schémaAdresse != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!adresse || !Chaîne) { errno = EFAULT; return 0; }
    const unsigned char *nombre = adresse;
    char valeurTemporaire[16]; unsigned int longueur = 0;
    for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 4; entréeÉlémentEmplacement++) {
        unsigned int valeur = nombre[entréeÉlémentEmplacement];
        if (valeur >= 100) valeurTemporaire[longueur++] = '0' + valeur / 100;
        if (valeur >= 10) valeurTemporaire[longueur++] = '0' + valeur / 10 % 10;
        valeurTemporaire[longueur++] = '0' + valeur % 10;
        if (entréeÉlémentEmplacement < 3) valeurTemporaire[longueur++] = '.';
    }
    valeurTemporaire[longueur++] = 0;
    if (valeurCapacité < longueur) { errno = ENOSPC; return 0; }
    for (unsigned int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueur; entréeÉlémentEmplacement++) Chaîne[entréeÉlémentEmplacement] = valeurTemporaire[entréeÉlémentEmplacement];
    return Chaîne;
}
