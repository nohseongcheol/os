#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int podmienka, int riadok) {
    검사항목수++;
    if (!podmienka) {
        puts("POSIX CHECK FAILED");
        char číslica_VALUE[12]; int dĺžka_VALUE = 0;
        do { číslica_VALUE[dĺžka_VALUE++] = '0' + riadok % 10; riadok /= 10; } while (riadok);
        while (dĺžka_VALUE) putchar(číslica_VALUE[--dĺžka_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define overiť(podmienka) 검사((podmienka), __LINE__)

int main(int 인수개수, char **argument_Zoznam) {
    char údaje[32]; struct stat Stav_VALUE;
    overiť(인수개수 == 2 && strcmp(argument_Zoznam[1], "check") == 0 && argument_Zoznam[2] == 0);
    overiť(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    overiť(otvoriť_Súbor("absent", iba_na_čítanie_VALUE) == -1 && chybové_číslo == ENOENT);
    int Súbor = otvoriť_Súbor("/posix.txt", na_čítanie_a_zapisovanie | 새파일만들기, 0640);
    overiť(Súbor == 3);
    overiť(zapísať_Súbor_údaje(Súbor, "abcd", 4) == 4);
    overiť(otvoriť_Súbor("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    overiť(파일상태읽기(Súbor, &Stav_VALUE) == 0 && Stav_VALUE.st_size == 4 && S_ISREG(Stav_VALUE.st_mode));
    overiť((Stav_VALUE.st_mode & 0777) == 0640 && Stav_VALUE.st_nlink == 1);
    overiť(hľadať_Súbor(Súbor, 0, 처음기준) == 0);
    int klon_VALUE = 파일서술자복제(Súbor);
    overiť(klon_VALUE == 4);
    overiť(파일자료읽기(klon_VALUE, údaje, 2) == 2 && memcmp(údaje, "ab", 2) == 0);
    overiť(파일자료읽기(Súbor, údaje, 2) == 2 && memcmp(údaje, "cd", 2) == 0);
    overiť(파일자료읽기(Súbor, údaje, 1) == 0);
    overiť(fcntl(Súbor, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Súbor, F_GETFD) == 1);
    overiť(fcntl(klon_VALUE, F_GETFD) == 0);
    overiť(dup2(Súbor, Súbor) == Súbor && fcntl(Súbor, F_GETFD) == 1);
    overiť(dup2(-1, klon_VALUE) == -1 && errno == EBADF && fcntl(klon_VALUE, F_GETFD) == 0);
    overiť(fcntl(klon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Súbor, F_GETFL) & O_APPEND));
    overiť(lseek(Súbor, 0, SEEK_SET) == 0 && write(klon_VALUE, "e", 1) == 1 && lseek(Súbor, 0, SEEK_CUR) == 5);
    overiť(fcntl(Súbor, F_SETFL, 0) == 0);
    overiť(lseek(Súbor, 8, SEEK_SET) == 8 && write(Súbor, "Z", 1) == 1);
    overiť(lseek(klon_VALUE, 5, SEEK_SET) == 5 && read(Súbor, údaje, 4) == 4);
    overiť(údaje[0] == 0 && údaje[1] == 0 && údaje[2] == 0 && údaje[3] == 'Z');
    overiť(ftruncate(Súbor, 2) == 0 && lseek(Súbor, 0, SEEK_CUR) == 9);
    overiť(ftruncate(Súbor, 6) == 0 && lseek(Súbor, 2, SEEK_SET) == 2 && read(Súbor, údaje, 4) == 4);
    overiť(!údaje[0] && !údaje[1] && !údaje[2] && !údaje[3]);
    overiť(lseek(Súbor, 2147483647, SEEK_SET) == 2147483647);
    overiť(lseek(Súbor, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    overiť(lseek(Súbor, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    overiť(write(Súbor, "!", 1) == -1 && errno == EFBIG);
    overiť(lseek(Súbor, 0, SEEK_SET) == 0);
    overiť(read(Súbor, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    overiť(read(Súbor, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    overiť(write(Súbor, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    overiť(read(Súbor, údaje, (size_t)-1) == -1 && errno == EINVAL);
    overiť(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    overiť(fstat(Súbor, (void *)0x00100000) == -1 && errno == EFAULT);
    overiť(lseek(Súbor, 0, SEEK_CUR) == 0);
    overiť(read(Súbor, NULL, 0) == 0 && write(Súbor, NULL, 0) == 0);
    overiť(odobrať_Súbor_položka_názov("posix.txt") == 0);
    overiť(fstat(Súbor, &Stav_VALUE) == 0 && Stav_VALUE.st_nlink == 0 && Stav_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    overiť(새파일 == 5 && fstat(새파일, &Stav_VALUE) == 0 && Stav_VALUE.st_size == 0);
    overiť(read(Súbor, údaje, 2) == 2 && memcmp(údaje, "ab", 2) == 0);
    overiť(close(Súbor) == 0 && close(klon_VALUE) == 0 && close(새파일) == 0);
    overiť(close(새파일) == -1 && errno == EBADF);
    overiť(unlink("posix.txt") == 0);
    Súbor = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    overiť(Súbor == 3 && fcntl(Súbor, F_GETFD) == 1);
    overiť(read(Súbor, údaje, 1) == -1 && errno == EBADF);
    overiť(write(Súbor, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) overiť(dup(Súbor) == INDEX);
    overiť(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    overiť(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    overiť(fstat(Súbor, &Stav_VALUE) == 0 && Stav_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) overiť(close(INDEX) == 0);
    overiť(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Súbor = open("posix.txt", O_RDONLY);
    overiť(Súbor == 3 && write(Súbor, údaje, 1) == -1 && errno == EBADF);
    overiť(fcntl(Súbor, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    overiť(close(8) == 0 && close(Súbor) == 0 && unlink("posix.txt") == 0);
    overiť(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    overiť(fstat(1, &Stav_VALUE) == 0 && S_ISCHR(Stav_VALUE.st_mode));
    overiť(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    overiť(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresa; char adresa_SMS[16];
    overiť(inet_pton(AF_INET, "10.0.2.2", &adresa) == 1 && ntohl(adresa.s_addr) == 0x0a000202U);
    overiť(inet_ntop(AF_INET, &adresa, adresa_SMS, sizeof adresa_SMS) == adresa_SMS && strcmp(adresa_SMS, "10.0.2.2") == 0);
    overiť(inet_pton(AF_INET, "256.0.0.1", &adresa) == 0 && ntohl(adresa.s_addr) == 0x0a000202U);
    overiť(inet_pton(AF_INET, "01.0.0.1", &adresa) == 0);
    overiť(inet_ntop(AF_INET, &adresa, adresa_SMS, 3) == NULL && errno == ENOSPC);
    overiť(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], položka_COUNT = 0; char Názov[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Názov[4] = '0' + INDEX;
        int 열린파일 = open(Názov, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { overiť(errno == ENOSPC); break; }
        보관[položka_COUNT++] = 열린파일;
    }
    overiť(položka_COUNT > 0 && položka_COUNT < 8);
    overiť(unlink("slot0") == 0);
    overiť(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    overiť(close(보관[0]) == 0);
    Súbor = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    overiť(Súbor >= 0 && close(Súbor) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < položka_COUNT; INDEX++) {
        Názov[4] = '0' + INDEX;
        overiť(close(보관[INDEX]) == 0 && unlink(Názov) == 0);
    }
    overiť(fsync(-1) == -1 && errno == EBADF);
    overiť(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
