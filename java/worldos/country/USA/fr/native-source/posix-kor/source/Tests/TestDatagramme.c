#include <ABIFichier.h>
#include <ABIRéseau.h>
#include <string.h>
#include <stdio.h>

#define vérifier(condition) do { if (!(condition)) { puts("POSIX UDP CHECK FAILED: " #condition); return 1; } } while (0)
int main(int nombreÉlémentsArguments, char **listeArgument) {
    vérifier(nombreÉlémentsArguments == 2);
    int numéroPort = 0;
    for (int entréeÉlémentEmplacement = 0; listeArgument[1][entréeÉlémentEmplacement]; entréeÉlémentEmplacement++) {
        vérifier(listeArgument[1][entréeÉlémentEmplacement] >= '0' && listeArgument[1][entréeÉlémentEmplacement] <= '9');
        numéroPort = numéroPort * 10 + listeArgument[1][entréeÉlémentEmplacement] - '0';
        vérifier(numéroPort <= 65535);
    }
    int valeurExtrémité = créerExtrémité(AF_INET, SOCK_DGRAM, 0);
    vérifier(valeurExtrémité == 3);
    struct sockaddr_in portéeLocal = {0}, valeurPairRéseau = {0}, adresseReçu = {0};
    portéeLocal.sin_family = AF_INET;
    socklen_t longueur = sizeof portéeLocal;
    vérifier(lireAdressePriseRéseau(valeurExtrémité, (struct sockaddr *)&portéeLocal, &longueur) == 0 && portéeLocal.sin_port == 0);
    vérifier(associerAdresse(valeurExtrémité, (struct sockaddr *)&portéeLocal, sizeof portéeLocal) == 0);
    vérifier(lireAdressePriseRéseau(valeurExtrémité, (struct sockaddr *)&portéeLocal, &longueur) == 0 && ntohs(portéeLocal.sin_port) >= 49152);
    vérifier(associerAdresse(valeurExtrémité, (struct sockaddr *)&portéeLocal, sizeof portéeLocal) == -1 && errno == EINVAL);
    int ordinalDeuxième = socket(AF_INET, SOCK_DGRAM, 0);
    vérifier(bind(ordinalDeuxième, (struct sockaddr *)&portéeLocal, sizeof portéeLocal) == -1 && errno == EADDRINUSE);
    vérifier(close(ordinalDeuxième) == 0);
    ordinalDeuxième = dup(valeurExtrémité);
    vérifier(close(valeurExtrémité) == 0); valeurExtrémité = ordinalDeuxième;
    valeurPairRéseau.sin_family = AF_INET; valeurPairRéseau.sin_port = courtRéseau(numéroPort);
    vérifier(analyserAdresseRéseau(AF_INET, "10.0.2.2", &valeurPairRéseau.sin_addr) == 1);
    struct timeval attendreValeur = {0, 200000};
    vérifier(changerRéglagesRéseau(valeurExtrémité, SOL_SOCKET, SO_RCVTIMEO, &attendreValeur, sizeof attendreValeur) == 0);
    char Données[32];
    vérifier(recevoirDonnéesDatagramme(valeurExtrémité, Données, sizeof Données, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    vérifier(envoyerDonnéesDatagramme(valeurExtrémité, "posix-udp", 9, 0, (struct sockaddr *)&valeurPairRéseau, sizeof valeurPairRéseau) == 9);
    longueur = sizeof adresseReçu;
    vérifier(recvfrom(valeurExtrémité, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    vérifier(recevoirDonnéesDatagramme(valeurExtrémité, Données, sizeof Données, 0, (struct sockaddr *)&adresseReçu, &longueur) == 9);
    vérifier(memcmp(Données, "posix-udp", 9) == 0 && longueur == 16);
    vérifier(adresseReçu.sin_port == valeurPairRéseau.sin_port && adresseReçu.sin_addr.s_addr == valeurPairRéseau.sin_addr.s_addr);
    vérifier(sendto(valeurExtrémité, "truncate", 8, 0, (struct sockaddr *)&valeurPairRéseau, sizeof valeurPairRéseau) == 8);
    vérifier(recvfrom(valeurExtrémité, Données, 3, 0, NULL, NULL) == 3 && memcmp(Données, "tru", 3) == 0);
    vérifier(recvfrom(valeurExtrémité, Données, sizeof Données, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    vérifier(sendto(valeurExtrémité, NULL, 0, 0, (struct sockaddr *)&valeurPairRéseau, sizeof valeurPairRéseau) == 0);
    vérifier(recvfrom(valeurExtrémité, NULL, 0, 0, NULL, NULL) == 0);
    vérifier(recvfrom(valeurExtrémité, Données, sizeof Données, 0, NULL, NULL) == -1 && errno == EAGAIN);
    vérifier(close(valeurExtrémité) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
