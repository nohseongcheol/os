#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ehto, int syöterivi) {
    검사항목수++;
    if (!ehto) {
        puts("POSIX CHECK FAILED");
        char numero_ARVO[12]; int kesto_ARVO = 0;
        do { numero_ARVO[kesto_ARVO++] = '0' + syöterivi % 10; syöterivi /= 10; } while (syöterivi);
        while (kesto_ARVO) putchar(numero_ARVO[--kesto_ARVO]);
        putchar('\n'); _exit(1);
    }
}
#define tarkistaa(ehto) 검사((ehto), __LINE__)

int main(int 인수개수, char **argumentti_luettelo) {
    char data[32]; struct stat Tila_ARVO;
    tarkistaa(인수개수 == 2 && strcmp(argumentti_luettelo[1], "check") == 0 && argumentti_luettelo[2] == 0);
    tarkistaa(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    tarkistaa(avata_Tiedosto("absent", vain_luku_ARVO) == -1 && virhenumero == ENOENT);
    int tiedoston_nimi = avata_Tiedosto("/posix.txt", luku_ja_kirjoitus | 새파일만들기, 0640);
    tarkistaa(tiedoston_nimi == 3);
    tarkistaa(kirjoitus_Tiedosto_data(tiedoston_nimi, "abcd", 4) == 4);
    tarkistaa(avata_Tiedosto("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    tarkistaa(lukea_Tiedosto_tila(tiedoston_nimi, &Tila_ARVO) == 0 && Tila_ARVO.st_size == 4 && S_ISREG(Tila_ARVO.st_mode));
    tarkistaa((Tila_ARVO.st_mode & 0777) == 0640 && Tila_ARVO.st_nlink == 1);
    tarkistaa(hae_Tiedosto(tiedoston_nimi, 0, 처음기준) == 0);
    int klooni_ARVO = 파일서술자복제(tiedoston_nimi);
    tarkistaa(klooni_ARVO == 4);
    tarkistaa(lukea_Tiedosto_data(klooni_ARVO, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    tarkistaa(lukea_Tiedosto_data(tiedoston_nimi, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    tarkistaa(lukea_Tiedosto_data(tiedoston_nimi, data, 1) == 0);
    tarkistaa(fcntl(tiedoston_nimi, F_SETFD, FD_CLOEXEC) == 0 && fcntl(tiedoston_nimi, F_GETFD) == 1);
    tarkistaa(fcntl(klooni_ARVO, F_GETFD) == 0);
    tarkistaa(dup2(tiedoston_nimi, tiedoston_nimi) == tiedoston_nimi && fcntl(tiedoston_nimi, F_GETFD) == 1);
    tarkistaa(dup2(-1, klooni_ARVO) == -1 && errno == EBADF && fcntl(klooni_ARVO, F_GETFD) == 0);
    tarkistaa(fcntl(klooni_ARVO, F_SETFL, O_APPEND) == 0 && (fcntl(tiedoston_nimi, F_GETFL) & O_APPEND));
    tarkistaa(lseek(tiedoston_nimi, 0, SEEK_SET) == 0 && write(klooni_ARVO, "e", 1) == 1 && lseek(tiedoston_nimi, 0, SEEK_CUR) == 5);
    tarkistaa(fcntl(tiedoston_nimi, F_SETFL, 0) == 0);
    tarkistaa(lseek(tiedoston_nimi, 8, SEEK_SET) == 8 && write(tiedoston_nimi, "Z", 1) == 1);
    tarkistaa(lseek(klooni_ARVO, 5, SEEK_SET) == 5 && read(tiedoston_nimi, data, 4) == 4);
    tarkistaa(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    tarkistaa(ftruncate(tiedoston_nimi, 2) == 0 && lseek(tiedoston_nimi, 0, SEEK_CUR) == 9);
    tarkistaa(ftruncate(tiedoston_nimi, 6) == 0 && lseek(tiedoston_nimi, 2, SEEK_SET) == 2 && read(tiedoston_nimi, data, 4) == 4);
    tarkistaa(!data[0] && !data[1] && !data[2] && !data[3]);
    tarkistaa(lseek(tiedoston_nimi, 2147483647, SEEK_SET) == 2147483647);
    tarkistaa(lseek(tiedoston_nimi, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    tarkistaa(lseek(tiedoston_nimi, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    tarkistaa(write(tiedoston_nimi, "!", 1) == -1 && errno == EFBIG);
    tarkistaa(lseek(tiedoston_nimi, 0, SEEK_SET) == 0);
    tarkistaa(read(tiedoston_nimi, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tarkistaa(read(tiedoston_nimi, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    tarkistaa(write(tiedoston_nimi, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tarkistaa(read(tiedoston_nimi, data, (size_t)-1) == -1 && errno == EINVAL);
    tarkistaa(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    tarkistaa(fstat(tiedoston_nimi, (void *)0x00100000) == -1 && errno == EFAULT);
    tarkistaa(lseek(tiedoston_nimi, 0, SEEK_CUR) == 0);
    tarkistaa(read(tiedoston_nimi, NULL, 0) == 0 && write(tiedoston_nimi, NULL, 0) == 0);
    tarkistaa(poistaa_Tiedosto_merkintä_nimi("posix.txt") == 0);
    tarkistaa(fstat(tiedoston_nimi, &Tila_ARVO) == 0 && Tila_ARVO.st_nlink == 0 && Tila_ARVO.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    tarkistaa(새파일 == 5 && fstat(새파일, &Tila_ARVO) == 0 && Tila_ARVO.st_size == 0);
    tarkistaa(read(tiedoston_nimi, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    tarkistaa(close(tiedoston_nimi) == 0 && close(klooni_ARVO) == 0 && close(새파일) == 0);
    tarkistaa(close(새파일) == -1 && errno == EBADF);
    tarkistaa(unlink("posix.txt") == 0);
    tiedoston_nimi = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    tarkistaa(tiedoston_nimi == 3 && fcntl(tiedoston_nimi, F_GETFD) == 1);
    tarkistaa(read(tiedoston_nimi, data, 1) == -1 && errno == EBADF);
    tarkistaa(write(tiedoston_nimi, "keep", 4) == 4);
    for (int INDEKSI = 4; INDEKSI < 32; INDEKSI++) tarkistaa(dup(tiedoston_nimi) == INDEKSI);
    tarkistaa(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    tarkistaa(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    tarkistaa(fstat(tiedoston_nimi, &Tila_ARVO) == 0 && Tila_ARVO.st_size == 4);
    for (int INDEKSI = 3; INDEKSI < 32; INDEKSI++) tarkistaa(close(INDEKSI) == 0);
    tarkistaa(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    tiedoston_nimi = open("posix.txt", O_RDONLY);
    tarkistaa(tiedoston_nimi == 3 && write(tiedoston_nimi, data, 1) == -1 && errno == EBADF);
    tarkistaa(fcntl(tiedoston_nimi, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    tarkistaa(close(8) == 0 && close(tiedoston_nimi) == 0 && unlink("posix.txt") == 0);
    tarkistaa(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    tarkistaa(fstat(1, &Tila_ARVO) == 0 && S_ISCHR(Tila_ARVO.st_mode));
    tarkistaa(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    tarkistaa(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr OSOITE; char OSOITE_SMS[16];
    tarkistaa(inet_pton(AF_INET, "10.0.2.2", &OSOITE) == 1 && ntohl(OSOITE.s_addr) == 0x0a000202U);
    tarkistaa(inet_ntop(AF_INET, &OSOITE, OSOITE_SMS, sizeof OSOITE_SMS) == OSOITE_SMS && strcmp(OSOITE_SMS, "10.0.2.2") == 0);
    tarkistaa(inet_pton(AF_INET, "256.0.0.1", &OSOITE) == 0 && ntohl(OSOITE.s_addr) == 0x0a000202U);
    tarkistaa(inet_pton(AF_INET, "01.0.0.1", &OSOITE) == 0);
    tarkistaa(inet_ntop(AF_INET, &OSOITE, OSOITE_SMS, 3) == NULL && errno == ENOSPC);
    tarkistaa(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], kohde_LASKE = 0; char Nimi[] = "slot0";
    for (int INDEKSI = 0; INDEKSI < 8; INDEKSI++) {
        Nimi[4] = '0' + INDEKSI;
        int 열린파일 = open(Nimi, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { tarkistaa(errno == ENOSPC); break; }
        보관[kohde_LASKE++] = 열린파일;
    }
    tarkistaa(kohde_LASKE > 0 && kohde_LASKE < 8);
    tarkistaa(unlink("slot0") == 0);
    tarkistaa(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    tarkistaa(close(보관[0]) == 0);
    tiedoston_nimi = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    tarkistaa(tiedoston_nimi >= 0 && close(tiedoston_nimi) == 0 && unlink("held-slot") == 0);
    for (int INDEKSI = 1; INDEKSI < kohde_LASKE; INDEKSI++) {
        Nimi[4] = '0' + INDEKSI;
        tarkistaa(close(보관[INDEKSI]) == 0 && unlink(Nimi) == 0);
    }
    tarkistaa(fsync(-1) == -1 && errno == EBADF);
    tarkistaa(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
