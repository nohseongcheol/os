#include <ABIFichier.h>
#include <ABIRéseau.h>
#include <string.h>
#include <stdio.h>

static int nombreÉlémentsÉlémentListeContrôlé;
static void Contrôles(int condition, int ligne) {
    nombreÉlémentsÉlémentListeContrôlé++;
    if (!condition) {
        puts("POSIX CHECK FAILED");
        char valeurChiffre[12]; int longueur = 0;
        do { valeurChiffre[longueur++] = '0' + ligne % 10; ligne /= 10; } while (ligne);
        while (longueur) putchar(valeurChiffre[--longueur]);
        putchar('\n'); _exit(1);
    }
}
#define vérifier(condition) Contrôles((condition), __LINE__)

int main(int nombreÉlémentsArguments, char **listeArgument) {
    char Données[32]; struct stat valeurÉtatValeur;
    vérifier(nombreÉlémentsArguments == 2 && strcmp(listeArgument[1], "check") == 0 && listeArgument[2] == 0);
    vérifier(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    vérifier(ouvrirFichier("absent", lireValeurSeulement) == -1 && numéroErreur == ENOENT);
    int Fichier = ouvrirFichier("/posix.txt", ÉcrireLire | créerFichierNouveau, 0640);
    vérifier(Fichier == 3);
    vérifier(écrireDonnéesFichier(Fichier, "abcd", 4) == 4);
    vérifier(ouvrirFichier("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    vérifier(lireÉtatFichier(Fichier, &valeurÉtatValeur) == 0 && valeurÉtatValeur.st_size == 4 && S_ISREG(valeurÉtatValeur.st_mode));
    vérifier((valeurÉtatValeur.st_mode & 0777) == 0640 && valeurÉtatValeur.st_nlink == 1);
    vérifier(positionnerFichier(Fichier, 0, DébutDepuis) == 0);
    int valeurCloner = descripteurFichierDuplicata(Fichier);
    vérifier(valeurCloner == 4);
    vérifier(lireDonnéesFichier(valeurCloner, Données, 2) == 2 && memcmp(Données, "ab", 2) == 0);
    vérifier(lireDonnéesFichier(Fichier, Données, 2) == 2 && memcmp(Données, "cd", 2) == 0);
    vérifier(lireDonnéesFichier(Fichier, Données, 1) == 0);
    vérifier(fcntl(Fichier, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fichier, F_GETFD) == 1);
    vérifier(fcntl(valeurCloner, F_GETFD) == 0);
    vérifier(dup2(Fichier, Fichier) == Fichier && fcntl(Fichier, F_GETFD) == 1);
    vérifier(dup2(-1, valeurCloner) == -1 && errno == EBADF && fcntl(valeurCloner, F_GETFD) == 0);
    vérifier(fcntl(valeurCloner, F_SETFL, O_APPEND) == 0 && (fcntl(Fichier, F_GETFL) & O_APPEND));
    vérifier(lseek(Fichier, 0, SEEK_SET) == 0 && write(valeurCloner, "e", 1) == 1 && lseek(Fichier, 0, SEEK_CUR) == 5);
    vérifier(fcntl(Fichier, F_SETFL, 0) == 0);
    vérifier(lseek(Fichier, 8, SEEK_SET) == 8 && write(Fichier, "Z", 1) == 1);
    vérifier(lseek(valeurCloner, 5, SEEK_SET) == 5 && read(Fichier, Données, 4) == 4);
    vérifier(Données[0] == 0 && Données[1] == 0 && Données[2] == 0 && Données[3] == 'Z');
    vérifier(ftruncate(Fichier, 2) == 0 && lseek(Fichier, 0, SEEK_CUR) == 9);
    vérifier(ftruncate(Fichier, 6) == 0 && lseek(Fichier, 2, SEEK_SET) == 2 && read(Fichier, Données, 4) == 4);
    vérifier(!Données[0] && !Données[1] && !Données[2] && !Données[3]);
    vérifier(lseek(Fichier, 2147483647, SEEK_SET) == 2147483647);
    vérifier(lseek(Fichier, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    vérifier(lseek(Fichier, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    vérifier(write(Fichier, "!", 1) == -1 && errno == EFBIG);
    vérifier(lseek(Fichier, 0, SEEK_SET) == 0);
    vérifier(read(Fichier, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    vérifier(read(Fichier, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    vérifier(write(Fichier, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    vérifier(read(Fichier, Données, (size_t)-1) == -1 && errno == EINVAL);
    vérifier(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    vérifier(fstat(Fichier, (void *)0x00100000) == -1 && errno == EFAULT);
    vérifier(lseek(Fichier, 0, SEEK_CUR) == 0);
    vérifier(read(Fichier, NULL, 0) == 0 && write(Fichier, NULL, 0) == 0);
    vérifier(supprimerNomEntréeÉlémentFichier("posix.txt") == 0);
    vérifier(fstat(Fichier, &valeurÉtatValeur) == 0 && valeurÉtatValeur.st_nlink == 0 && valeurÉtatValeur.st_size == 6);
    int fichierNouveau = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    vérifier(fichierNouveau == 5 && fstat(fichierNouveau, &valeurÉtatValeur) == 0 && valeurÉtatValeur.st_size == 0);
    vérifier(read(Fichier, Données, 2) == 2 && memcmp(Données, "ab", 2) == 0);
    vérifier(close(Fichier) == 0 && close(valeurCloner) == 0 && close(fichierNouveau) == 0);
    vérifier(close(fichierNouveau) == -1 && errno == EBADF);
    vérifier(unlink("posix.txt") == 0);
    Fichier = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    vérifier(Fichier == 3 && fcntl(Fichier, F_GETFD) == 1);
    vérifier(read(Fichier, Données, 1) == -1 && errno == EBADF);
    vérifier(write(Fichier, "keep", 4) == 4);
    for (int numéro = 4; numéro < 32; numéro++) vérifier(dup(Fichier) == numéro);
    vérifier(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    vérifier(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    vérifier(fstat(Fichier, &valeurÉtatValeur) == 0 && valeurÉtatValeur.st_size == 4);
    for (int numéro = 3; numéro < 32; numéro++) vérifier(close(numéro) == 0);
    vérifier(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fichier = open("posix.txt", O_RDONLY);
    vérifier(Fichier == 3 && write(Fichier, Données, 1) == -1 && errno == EBADF);
    vérifier(fcntl(Fichier, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    vérifier(close(8) == 0 && close(Fichier) == 0 && unlink("posix.txt") == 0);
    vérifier(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    vérifier(fstat(1, &valeurÉtatValeur) == 0 && S_ISCHR(valeurÉtatValeur.st_mode));
    vérifier(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    vérifier(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresse; char texteAdresse[16];
    vérifier(inet_pton(AF_INET, "10.0.2.2", &adresse) == 1 && ntohl(adresse.s_addr) == 0x0a000202U);
    vérifier(inet_ntop(AF_INET, &adresse, texteAdresse, sizeof texteAdresse) == texteAdresse && strcmp(texteAdresse, "10.0.2.2") == 0);
    vérifier(inet_pton(AF_INET, "256.0.0.1", &adresse) == 0 && ntohl(adresse.s_addr) == 0x0a000202U);
    vérifier(inet_pton(AF_INET, "01.0.0.1", &adresse) == 0);
    vérifier(inet_ntop(AF_INET, &adresse, texteAdresse, 3) == NULL && errno == ENOSPC);
    vérifier(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int préserverValeur[8], nombreÉlémentsÉlémentListe = 0; char nom[] = "slot0";
    for (int numéro = 0; numéro < 8; numéro++) {
        nom[4] = '0' + numéro;
        int fichierOuvert = open(nom, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (fichierOuvert < 0) { vérifier(errno == ENOSPC); break; }
        préserverValeur[nombreÉlémentsÉlémentListe++] = fichierOuvert;
    }
    vérifier(nombreÉlémentsÉlémentListe > 0 && nombreÉlémentsÉlémentListe < 8);
    vérifier(unlink("slot0") == 0);
    vérifier(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    vérifier(close(préserverValeur[0]) == 0);
    Fichier = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    vérifier(Fichier >= 0 && close(Fichier) == 0 && unlink("held-slot") == 0);
    for (int numéro = 1; numéro < nombreÉlémentsÉlémentListe; numéro++) {
        nom[4] = '0' + numéro;
        vérifier(close(préserverValeur[numéro]) == 0 && unlink(nom) == 0);
    }
    vérifier(fsync(-1) == -1 && errno == EBADF);
    vérifier(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
