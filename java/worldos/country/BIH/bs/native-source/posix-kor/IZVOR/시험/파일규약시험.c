#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int uvjet, int Linija) {
    검사항목수++;
    if (!uvjet) {
        puts("POSIX CHECK FAILED");
        char cifra_VALUE[12]; int dužina_VALUE = 0;
        do { cifra_VALUE[dužina_VALUE++] = '0' + Linija % 10; Linija /= 10; } while (Linija);
        while (dužina_VALUE) putchar(cifra_VALUE[--dužina_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define potvrditi(uvjet) 검사((uvjet), __LINE__)

int main(int 인수개수, char **argument_spisak) {
    char podaci[32]; struct stat stanje_VALUE;
    potvrditi(인수개수 == 2 && strcmp(argument_spisak[1], "check") == 0 && argument_spisak[2] == 0);
    potvrditi(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    potvrditi(kreirati_fajl("absent", samo_za_čitanje_VALUE) == -1 && broj_greške == ENOENT);
    int Fajl = kreirati_fajl("/posix.txt", i_za_čitanje_i_za_pisanje | 새파일만들기, 0640);
    potvrditi(Fajl == 3);
    potvrditi(pisati_fajl_podaci(Fajl, "abcd", 4) == 4);
    potvrditi(kreirati_fajl("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    potvrditi(파일상태읽기(Fajl, &stanje_VALUE) == 0 && stanje_VALUE.st_size == 4 && S_ISREG(stanje_VALUE.st_mode));
    potvrditi((stanje_VALUE.st_mode & 0777) == 0640 && stanje_VALUE.st_nlink == 1);
    potvrditi(tražiti_fajl(Fajl, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Fajl);
    potvrditi(복제 == 4);
    potvrditi(파일자료읽기(복제, podaci, 2) == 2 && memcmp(podaci, "ab", 2) == 0);
    potvrditi(파일자료읽기(Fajl, podaci, 2) == 2 && memcmp(podaci, "cd", 2) == 0);
    potvrditi(파일자료읽기(Fajl, podaci, 1) == 0);
    potvrditi(fcntl(Fajl, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fajl, F_GETFD) == 1);
    potvrditi(fcntl(복제, F_GETFD) == 0);
    potvrditi(dup2(Fajl, Fajl) == Fajl && fcntl(Fajl, F_GETFD) == 1);
    potvrditi(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    potvrditi(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Fajl, F_GETFL) & O_APPEND));
    potvrditi(lseek(Fajl, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Fajl, 0, SEEK_CUR) == 5);
    potvrditi(fcntl(Fajl, F_SETFL, 0) == 0);
    potvrditi(lseek(Fajl, 8, SEEK_SET) == 8 && write(Fajl, "Z", 1) == 1);
    potvrditi(lseek(복제, 5, SEEK_SET) == 5 && read(Fajl, podaci, 4) == 4);
    potvrditi(podaci[0] == 0 && podaci[1] == 0 && podaci[2] == 0 && podaci[3] == 'Z');
    potvrditi(ftruncate(Fajl, 2) == 0 && lseek(Fajl, 0, SEEK_CUR) == 9);
    potvrditi(ftruncate(Fajl, 6) == 0 && lseek(Fajl, 2, SEEK_SET) == 2 && read(Fajl, podaci, 4) == 4);
    potvrditi(!podaci[0] && !podaci[1] && !podaci[2] && !podaci[3]);
    potvrditi(lseek(Fajl, 2147483647, SEEK_SET) == 2147483647);
    potvrditi(lseek(Fajl, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    potvrditi(lseek(Fajl, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    potvrditi(write(Fajl, "!", 1) == -1 && errno == EFBIG);
    potvrditi(lseek(Fajl, 0, SEEK_SET) == 0);
    potvrditi(read(Fajl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    potvrditi(read(Fajl, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    potvrditi(write(Fajl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    potvrditi(read(Fajl, podaci, (size_t)-1) == -1 && errno == EINVAL);
    potvrditi(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    potvrditi(fstat(Fajl, (void *)0x00100000) == -1 && errno == EFAULT);
    potvrditi(lseek(Fajl, 0, SEEK_CUR) == 0);
    potvrditi(read(Fajl, NULL, 0) == 0 && write(Fajl, NULL, 0) == 0);
    potvrditi(ukloniti_fajl_unos_naziv("posix.txt") == 0);
    potvrditi(fstat(Fajl, &stanje_VALUE) == 0 && stanje_VALUE.st_nlink == 0 && stanje_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    potvrditi(새파일 == 5 && fstat(새파일, &stanje_VALUE) == 0 && stanje_VALUE.st_size == 0);
    potvrditi(read(Fajl, podaci, 2) == 2 && memcmp(podaci, "ab", 2) == 0);
    potvrditi(close(Fajl) == 0 && close(복제) == 0 && close(새파일) == 0);
    potvrditi(close(새파일) == -1 && errno == EBADF);
    potvrditi(unlink("posix.txt") == 0);
    Fajl = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    potvrditi(Fajl == 3 && fcntl(Fajl, F_GETFD) == 1);
    potvrditi(read(Fajl, podaci, 1) == -1 && errno == EBADF);
    potvrditi(write(Fajl, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) potvrditi(dup(Fajl) == INDEX);
    potvrditi(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    potvrditi(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    potvrditi(fstat(Fajl, &stanje_VALUE) == 0 && stanje_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) potvrditi(close(INDEX) == 0);
    potvrditi(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fajl = open("posix.txt", O_RDONLY);
    potvrditi(Fajl == 3 && write(Fajl, podaci, 1) == -1 && errno == EBADF);
    potvrditi(fcntl(Fajl, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    potvrditi(close(8) == 0 && close(Fajl) == 0 && unlink("posix.txt") == 0);
    potvrditi(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    potvrditi(fstat(1, &stanje_VALUE) == 0 && S_ISCHR(stanje_VALUE.st_mode));
    potvrditi(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    potvrditi(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresa; char adresa_SMS[16];
    potvrditi(inet_pton(AF_INET, "10.0.2.2", &adresa) == 1 && ntohl(adresa.s_addr) == 0x0a000202U);
    potvrditi(inet_ntop(AF_INET, &adresa, adresa_SMS, sizeof adresa_SMS) == adresa_SMS && strcmp(adresa_SMS, "10.0.2.2") == 0);
    potvrditi(inet_pton(AF_INET, "256.0.0.1", &adresa) == 0 && ntohl(adresa.s_addr) == 0x0a000202U);
    potvrditi(inet_pton(AF_INET, "01.0.0.1", &adresa) == 0);
    potvrditi(inet_ntop(AF_INET, &adresa, adresa_SMS, 3) == NULL && errno == ENOSPC);
    potvrditi(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], stavka_COUNT = 0; char Naziv[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Naziv[4] = '0' + INDEX;
        int 열린파일 = open(Naziv, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { potvrditi(errno == ENOSPC); break; }
        보관[stavka_COUNT++] = 열린파일;
    }
    potvrditi(stavka_COUNT > 0 && stavka_COUNT < 8);
    potvrditi(unlink("slot0") == 0);
    potvrditi(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    potvrditi(close(보관[0]) == 0);
    Fajl = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    potvrditi(Fajl >= 0 && close(Fajl) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < stavka_COUNT; INDEX++) {
        Naziv[4] = '0' + INDEX;
        potvrditi(close(보관[INDEX]) == 0 && unlink(Naziv) == 0);
    }
    potvrditi(fsync(-1) == -1 && errno == EBADF);
    potvrditi(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
