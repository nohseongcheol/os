#include <DateiABI.h>
#include <NetzwerkABI.h>
#include <string.h>
#include <stdio.h>

static int geprüftElementeintragAnzahl;
static void Prüfpunkte(int bedingung, int zeile) {
    geprüftElementeintragAnzahl++;
    if (!bedingung) {
        puts("POSIX CHECK FAILED");
        char zifferWert[12]; int Länge = 0;
        do { zifferWert[Länge++] = '0' + zeile % 10; zeile /= 10; } while (zeile);
        while (Länge) putchar(zifferWert[--Länge]);
        putchar('\n'); _exit(1);
    }
}
#define überprüfen(bedingung) Prüfpunkte((bedingung), __LINE__)

int main(int argumenteAnzahl, char **argumentListe) {
    char Daten[32]; struct stat statuswertWert;
    überprüfen(argumenteAnzahl == 2 && strcmp(argumentListe[1], "check") == 0 && argumentListe[2] == 0);
    überprüfen(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    überprüfen(dateiÖffnen("absent", ausschließlichWertLesen) == -1 && fehlerNummer == ENOENT);
    int Datei = dateiÖffnen("/posix.txt", LesenSchreiben | neuDateiErstellen, 0640);
    überprüfen(Datei == 3);
    überprüfen(dateiDatenSchreiben(Datei, "abcd", 4) == 4);
    überprüfen(dateiÖffnen("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    überprüfen(dateiZustandLesen(Datei, &statuswertWert) == 0 && statuswertWert.st_size == 4 && S_ISREG(statuswertWert.st_mode));
    überprüfen((statuswertWert.st_mode & 0777) == 0640 && statuswertWert.st_nlink == 1);
    überprüfen(dateiPositionieren(Datei, 0, VonAnfang) == 0);
    int klonenWert = duplikatDateiDeskriptor(Datei);
    überprüfen(klonenWert == 4);
    überprüfen(dateiDatenLesen(klonenWert, Daten, 2) == 2 && memcmp(Daten, "ab", 2) == 0);
    überprüfen(dateiDatenLesen(Datei, Daten, 2) == 2 && memcmp(Daten, "cd", 2) == 0);
    überprüfen(dateiDatenLesen(Datei, Daten, 1) == 0);
    überprüfen(fcntl(Datei, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Datei, F_GETFD) == 1);
    überprüfen(fcntl(klonenWert, F_GETFD) == 0);
    überprüfen(dup2(Datei, Datei) == Datei && fcntl(Datei, F_GETFD) == 1);
    überprüfen(dup2(-1, klonenWert) == -1 && errno == EBADF && fcntl(klonenWert, F_GETFD) == 0);
    überprüfen(fcntl(klonenWert, F_SETFL, O_APPEND) == 0 && (fcntl(Datei, F_GETFL) & O_APPEND));
    überprüfen(lseek(Datei, 0, SEEK_SET) == 0 && write(klonenWert, "e", 1) == 1 && lseek(Datei, 0, SEEK_CUR) == 5);
    überprüfen(fcntl(Datei, F_SETFL, 0) == 0);
    überprüfen(lseek(Datei, 8, SEEK_SET) == 8 && write(Datei, "Z", 1) == 1);
    überprüfen(lseek(klonenWert, 5, SEEK_SET) == 5 && read(Datei, Daten, 4) == 4);
    überprüfen(Daten[0] == 0 && Daten[1] == 0 && Daten[2] == 0 && Daten[3] == 'Z');
    überprüfen(ftruncate(Datei, 2) == 0 && lseek(Datei, 0, SEEK_CUR) == 9);
    überprüfen(ftruncate(Datei, 6) == 0 && lseek(Datei, 2, SEEK_SET) == 2 && read(Datei, Daten, 4) == 4);
    überprüfen(!Daten[0] && !Daten[1] && !Daten[2] && !Daten[3]);
    überprüfen(lseek(Datei, 2147483647, SEEK_SET) == 2147483647);
    überprüfen(lseek(Datei, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    überprüfen(lseek(Datei, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    überprüfen(write(Datei, "!", 1) == -1 && errno == EFBIG);
    überprüfen(lseek(Datei, 0, SEEK_SET) == 0);
    überprüfen(read(Datei, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    überprüfen(read(Datei, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    überprüfen(write(Datei, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    überprüfen(read(Datei, Daten, (size_t)-1) == -1 && errno == EINVAL);
    überprüfen(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    überprüfen(fstat(Datei, (void *)0x00100000) == -1 && errno == EFAULT);
    überprüfen(lseek(Datei, 0, SEEK_CUR) == 0);
    überprüfen(read(Datei, NULL, 0) == 0 && write(Datei, NULL, 0) == 0);
    überprüfen(dateiEintragNameEntfernen("posix.txt") == 0);
    überprüfen(fstat(Datei, &statuswertWert) == 0 && statuswertWert.st_nlink == 0 && statuswertWert.st_size == 6);
    int neuDatei = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    überprüfen(neuDatei == 5 && fstat(neuDatei, &statuswertWert) == 0 && statuswertWert.st_size == 0);
    überprüfen(read(Datei, Daten, 2) == 2 && memcmp(Daten, "ab", 2) == 0);
    überprüfen(close(Datei) == 0 && close(klonenWert) == 0 && close(neuDatei) == 0);
    überprüfen(close(neuDatei) == -1 && errno == EBADF);
    überprüfen(unlink("posix.txt") == 0);
    Datei = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    überprüfen(Datei == 3 && fcntl(Datei, F_GETFD) == 1);
    überprüfen(read(Datei, Daten, 1) == -1 && errno == EBADF);
    überprüfen(write(Datei, "keep", 4) == 4);
    for (int Nummer = 4; Nummer < 32; Nummer++) überprüfen(dup(Datei) == Nummer);
    überprüfen(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    überprüfen(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    überprüfen(fstat(Datei, &statuswertWert) == 0 && statuswertWert.st_size == 4);
    for (int Nummer = 3; Nummer < 32; Nummer++) überprüfen(close(Nummer) == 0);
    überprüfen(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Datei = open("posix.txt", O_RDONLY);
    überprüfen(Datei == 3 && write(Datei, Daten, 1) == -1 && errno == EBADF);
    überprüfen(fcntl(Datei, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    überprüfen(close(8) == 0 && close(Datei) == 0 && unlink("posix.txt") == 0);
    überprüfen(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    überprüfen(fstat(1, &statuswertWert) == 0 && S_ISCHR(statuswertWert.st_mode));
    überprüfen(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    überprüfen(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresse; char adresseText[16];
    überprüfen(inet_pton(AF_INET, "10.0.2.2", &adresse) == 1 && ntohl(adresse.s_addr) == 0x0a000202U);
    überprüfen(inet_ntop(AF_INET, &adresse, adresseText, sizeof adresseText) == adresseText && strcmp(adresseText, "10.0.2.2") == 0);
    überprüfen(inet_pton(AF_INET, "256.0.0.1", &adresse) == 0 && ntohl(adresse.s_addr) == 0x0a000202U);
    überprüfen(inet_pton(AF_INET, "01.0.0.1", &adresse) == 0);
    überprüfen(inet_ntop(AF_INET, &adresse, adresseText, 3) == NULL && errno == ENOSPC);
    überprüfen(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int wertBewahren[8], elementeintragAnzahl = 0; char Name[] = "slot0";
    for (int Nummer = 0; Nummer < 8; Nummer++) {
        Name[4] = '0' + Nummer;
        int geöffnetDatei = open(Name, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (geöffnetDatei < 0) { überprüfen(errno == ENOSPC); break; }
        wertBewahren[elementeintragAnzahl++] = geöffnetDatei;
    }
    überprüfen(elementeintragAnzahl > 0 && elementeintragAnzahl < 8);
    überprüfen(unlink("slot0") == 0);
    überprüfen(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    überprüfen(close(wertBewahren[0]) == 0);
    Datei = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    überprüfen(Datei >= 0 && close(Datei) == 0 && unlink("held-slot") == 0);
    for (int Nummer = 1; Nummer < elementeintragAnzahl; Nummer++) {
        Name[4] = '0' + Nummer;
        überprüfen(close(wertBewahren[Nummer]) == 0 && unlink(Name) == 0);
    }
    überprüfen(fsync(-1) == -1 && errno == EBADF);
    überprüfen(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
