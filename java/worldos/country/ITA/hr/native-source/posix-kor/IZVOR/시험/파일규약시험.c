#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int uvjet, int red) {
    검사항목수++;
    if (!uvjet) {
        puts("POSIX CHECK FAILED");
        char znamenka_VALUE[12]; int 길이 = 0;
        do { znamenka_VALUE[길이++] = '0' + red % 10; red /= 10; } while (red);
        while (길이) putchar(znamenka_VALUE[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define provjeriti(uvjet) 검사((uvjet), __LINE__)

int main(int 인수개수, char **argument_Popis) {
    char podaci[32]; struct stat Stanje_VALUE;
    provjeriti(인수개수 == 2 && strcmp(argument_Popis[1], "check") == 0 && argument_Popis[2] == 0);
    provjeriti(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    provjeriti(otvoreno_Datoteka("absent", samo_za_čitanje_VALUE) == -1 && broj_pogreške == ENOENT);
    int Datoteka = otvoreno_Datoteka("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    provjeriti(Datoteka == 3);
    provjeriti(zapisivanje_Datoteka_podaci(Datoteka, "abcd", 4) == 4);
    provjeriti(otvoreno_Datoteka("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    provjeriti(파일상태읽기(Datoteka, &Stanje_VALUE) == 0 && Stanje_VALUE.st_size == 4 && S_ISREG(Stanje_VALUE.st_mode));
    provjeriti((Stanje_VALUE.st_mode & 0777) == 0640 && Stanje_VALUE.st_nlink == 1);
    provjeriti(tražiti_Datoteka(Datoteka, 0, 처음기준) == 0);
    int klon_VALUE = 파일서술자복제(Datoteka);
    provjeriti(klon_VALUE == 4);
    provjeriti(파일자료읽기(klon_VALUE, podaci, 2) == 2 && memcmp(podaci, "ab", 2) == 0);
    provjeriti(파일자료읽기(Datoteka, podaci, 2) == 2 && memcmp(podaci, "cd", 2) == 0);
    provjeriti(파일자료읽기(Datoteka, podaci, 1) == 0);
    provjeriti(fcntl(Datoteka, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Datoteka, F_GETFD) == 1);
    provjeriti(fcntl(klon_VALUE, F_GETFD) == 0);
    provjeriti(dup2(Datoteka, Datoteka) == Datoteka && fcntl(Datoteka, F_GETFD) == 1);
    provjeriti(dup2(-1, klon_VALUE) == -1 && errno == EBADF && fcntl(klon_VALUE, F_GETFD) == 0);
    provjeriti(fcntl(klon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Datoteka, F_GETFL) & O_APPEND));
    provjeriti(lseek(Datoteka, 0, SEEK_SET) == 0 && write(klon_VALUE, "e", 1) == 1 && lseek(Datoteka, 0, SEEK_CUR) == 5);
    provjeriti(fcntl(Datoteka, F_SETFL, 0) == 0);
    provjeriti(lseek(Datoteka, 8, SEEK_SET) == 8 && write(Datoteka, "Z", 1) == 1);
    provjeriti(lseek(klon_VALUE, 5, SEEK_SET) == 5 && read(Datoteka, podaci, 4) == 4);
    provjeriti(podaci[0] == 0 && podaci[1] == 0 && podaci[2] == 0 && podaci[3] == 'Z');
    provjeriti(ftruncate(Datoteka, 2) == 0 && lseek(Datoteka, 0, SEEK_CUR) == 9);
    provjeriti(ftruncate(Datoteka, 6) == 0 && lseek(Datoteka, 2, SEEK_SET) == 2 && read(Datoteka, podaci, 4) == 4);
    provjeriti(!podaci[0] && !podaci[1] && !podaci[2] && !podaci[3]);
    provjeriti(lseek(Datoteka, 2147483647, SEEK_SET) == 2147483647);
    provjeriti(lseek(Datoteka, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    provjeriti(lseek(Datoteka, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    provjeriti(write(Datoteka, "!", 1) == -1 && errno == EFBIG);
    provjeriti(lseek(Datoteka, 0, SEEK_SET) == 0);
    provjeriti(read(Datoteka, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    provjeriti(read(Datoteka, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    provjeriti(write(Datoteka, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    provjeriti(read(Datoteka, podaci, (size_t)-1) == -1 && errno == EINVAL);
    provjeriti(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    provjeriti(fstat(Datoteka, (void *)0x00100000) == -1 && errno == EFAULT);
    provjeriti(lseek(Datoteka, 0, SEEK_CUR) == 0);
    provjeriti(read(Datoteka, NULL, 0) == 0 && write(Datoteka, NULL, 0) == 0);
    provjeriti(ukloniti_Datoteka_unos_naziv("posix.txt") == 0);
    provjeriti(fstat(Datoteka, &Stanje_VALUE) == 0 && Stanje_VALUE.st_nlink == 0 && Stanje_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    provjeriti(새파일 == 5 && fstat(새파일, &Stanje_VALUE) == 0 && Stanje_VALUE.st_size == 0);
    provjeriti(read(Datoteka, podaci, 2) == 2 && memcmp(podaci, "ab", 2) == 0);
    provjeriti(close(Datoteka) == 0 && close(klon_VALUE) == 0 && close(새파일) == 0);
    provjeriti(close(새파일) == -1 && errno == EBADF);
    provjeriti(unlink("posix.txt") == 0);
    Datoteka = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    provjeriti(Datoteka == 3 && fcntl(Datoteka, F_GETFD) == 1);
    provjeriti(read(Datoteka, podaci, 1) == -1 && errno == EBADF);
    provjeriti(write(Datoteka, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) provjeriti(dup(Datoteka) == INDEX);
    provjeriti(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    provjeriti(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    provjeriti(fstat(Datoteka, &Stanje_VALUE) == 0 && Stanje_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) provjeriti(close(INDEX) == 0);
    provjeriti(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Datoteka = open("posix.txt", O_RDONLY);
    provjeriti(Datoteka == 3 && write(Datoteka, podaci, 1) == -1 && errno == EBADF);
    provjeriti(fcntl(Datoteka, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    provjeriti(close(8) == 0 && close(Datoteka) == 0 && unlink("posix.txt") == 0);
    provjeriti(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    provjeriti(fstat(1, &Stanje_VALUE) == 0 && S_ISCHR(Stanje_VALUE.st_mode));
    provjeriti(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    provjeriti(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresa; char adresa_SMS[16];
    provjeriti(inet_pton(AF_INET, "10.0.2.2", &adresa) == 1 && ntohl(adresa.s_addr) == 0x0a000202U);
    provjeriti(inet_ntop(AF_INET, &adresa, adresa_SMS, sizeof adresa_SMS) == adresa_SMS && strcmp(adresa_SMS, "10.0.2.2") == 0);
    provjeriti(inet_pton(AF_INET, "256.0.0.1", &adresa) == 0 && ntohl(adresa.s_addr) == 0x0a000202U);
    provjeriti(inet_pton(AF_INET, "01.0.0.1", &adresa) == 0);
    provjeriti(inet_ntop(AF_INET, &adresa, adresa_SMS, 3) == NULL && errno == ENOSPC);
    provjeriti(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], artikl_COUNT = 0; char Ime[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Ime[4] = '0' + INDEX;
        int 열린파일 = open(Ime, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { provjeriti(errno == ENOSPC); break; }
        보관[artikl_COUNT++] = 열린파일;
    }
    provjeriti(artikl_COUNT > 0 && artikl_COUNT < 8);
    provjeriti(unlink("slot0") == 0);
    provjeriti(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    provjeriti(close(보관[0]) == 0);
    Datoteka = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    provjeriti(Datoteka >= 0 && close(Datoteka) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < artikl_COUNT; INDEX++) {
        Ime[4] = '0' + INDEX;
        provjeriti(close(보관[INDEX]) == 0 && unlink(Ime) == 0);
    }
    provjeriti(fsync(-1) == -1 && errno == EBADF);
    provjeriti(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
