#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int stanje, int red) {
    검사항목수++;
    if (!stanje) {
        puts("POSIX CHECK FAILED");
        char cifra_VALUE[12]; int 길이 = 0;
        do { cifra_VALUE[길이++] = '0' + red % 10; red /= 10; } while (red);
        while (길이) putchar(cifra_VALUE[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define verifikovati(stanje) 검사((stanje), __LINE__)

int main(int 인수개수, char **argument_Lista) {
    char podaci[32]; struct stat Status_VALUE;
    verifikovati(인수개수 == 2 && strcmp(argument_Lista[1], "check") == 0 && argument_Lista[2] == 0);
    verifikovati(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verifikovati(otvoren_Datoteka("absent", samo_za_čitanje_VALUE) == -1 && broj_greške == ENOENT);
    int Datoteka = otvoren_Datoteka("/posix.txt", za_čitanje_pisanje | 새파일만들기, 0640);
    verifikovati(Datoteka == 3);
    verifikovati(파일자료쓰기(Datoteka, "abcd", 4) == 4);
    verifikovati(otvoren_Datoteka("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verifikovati(파일상태읽기(Datoteka, &Status_VALUE) == 0 && Status_VALUE.st_size == 4 && S_ISREG(Status_VALUE.st_mode));
    verifikovati((Status_VALUE.st_mode & 0777) == 0640 && Status_VALUE.st_nlink == 1);
    verifikovati(tražiti_Datoteka(Datoteka, 0, 처음기준) == 0);
    int klon_VALUE = 파일서술자복제(Datoteka);
    verifikovati(klon_VALUE == 4);
    verifikovati(파일자료읽기(klon_VALUE, podaci, 2) == 2 && memcmp(podaci, "ab", 2) == 0);
    verifikovati(파일자료읽기(Datoteka, podaci, 2) == 2 && memcmp(podaci, "cd", 2) == 0);
    verifikovati(파일자료읽기(Datoteka, podaci, 1) == 0);
    verifikovati(fcntl(Datoteka, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Datoteka, F_GETFD) == 1);
    verifikovati(fcntl(klon_VALUE, F_GETFD) == 0);
    verifikovati(dup2(Datoteka, Datoteka) == Datoteka && fcntl(Datoteka, F_GETFD) == 1);
    verifikovati(dup2(-1, klon_VALUE) == -1 && errno == EBADF && fcntl(klon_VALUE, F_GETFD) == 0);
    verifikovati(fcntl(klon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Datoteka, F_GETFL) & O_APPEND));
    verifikovati(lseek(Datoteka, 0, SEEK_SET) == 0 && write(klon_VALUE, "e", 1) == 1 && lseek(Datoteka, 0, SEEK_CUR) == 5);
    verifikovati(fcntl(Datoteka, F_SETFL, 0) == 0);
    verifikovati(lseek(Datoteka, 8, SEEK_SET) == 8 && write(Datoteka, "Z", 1) == 1);
    verifikovati(lseek(klon_VALUE, 5, SEEK_SET) == 5 && read(Datoteka, podaci, 4) == 4);
    verifikovati(podaci[0] == 0 && podaci[1] == 0 && podaci[2] == 0 && podaci[3] == 'Z');
    verifikovati(ftruncate(Datoteka, 2) == 0 && lseek(Datoteka, 0, SEEK_CUR) == 9);
    verifikovati(ftruncate(Datoteka, 6) == 0 && lseek(Datoteka, 2, SEEK_SET) == 2 && read(Datoteka, podaci, 4) == 4);
    verifikovati(!podaci[0] && !podaci[1] && !podaci[2] && !podaci[3]);
    verifikovati(lseek(Datoteka, 2147483647, SEEK_SET) == 2147483647);
    verifikovati(lseek(Datoteka, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verifikovati(lseek(Datoteka, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verifikovati(write(Datoteka, "!", 1) == -1 && errno == EFBIG);
    verifikovati(lseek(Datoteka, 0, SEEK_SET) == 0);
    verifikovati(read(Datoteka, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifikovati(read(Datoteka, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verifikovati(write(Datoteka, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifikovati(read(Datoteka, podaci, (size_t)-1) == -1 && errno == EINVAL);
    verifikovati(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verifikovati(fstat(Datoteka, (void *)0x00100000) == -1 && errno == EFAULT);
    verifikovati(lseek(Datoteka, 0, SEEK_CUR) == 0);
    verifikovati(read(Datoteka, NULL, 0) == 0 && write(Datoteka, NULL, 0) == 0);
    verifikovati(ukloniti_Datoteka_stavka_ime("posix.txt") == 0);
    verifikovati(fstat(Datoteka, &Status_VALUE) == 0 && Status_VALUE.st_nlink == 0 && Status_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifikovati(새파일 == 5 && fstat(새파일, &Status_VALUE) == 0 && Status_VALUE.st_size == 0);
    verifikovati(read(Datoteka, podaci, 2) == 2 && memcmp(podaci, "ab", 2) == 0);
    verifikovati(close(Datoteka) == 0 && close(klon_VALUE) == 0 && close(새파일) == 0);
    verifikovati(close(새파일) == -1 && errno == EBADF);
    verifikovati(unlink("posix.txt") == 0);
    Datoteka = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verifikovati(Datoteka == 3 && fcntl(Datoteka, F_GETFD) == 1);
    verifikovati(read(Datoteka, podaci, 1) == -1 && errno == EBADF);
    verifikovati(write(Datoteka, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verifikovati(dup(Datoteka) == INDEX);
    verifikovati(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verifikovati(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verifikovati(fstat(Datoteka, &Status_VALUE) == 0 && Status_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verifikovati(close(INDEX) == 0);
    verifikovati(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Datoteka = open("posix.txt", O_RDONLY);
    verifikovati(Datoteka == 3 && write(Datoteka, podaci, 1) == -1 && errno == EBADF);
    verifikovati(fcntl(Datoteka, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verifikovati(close(8) == 0 && close(Datoteka) == 0 && unlink("posix.txt") == 0);
    verifikovati(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verifikovati(fstat(1, &Status_VALUE) == 0 && S_ISCHR(Status_VALUE.st_mode));
    verifikovati(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verifikovati(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adresa; char adresa_SMS[16];
    verifikovati(inet_pton(AF_INET, "10.0.2.2", &adresa) == 1 && ntohl(adresa.s_addr) == 0x0a000202U);
    verifikovati(inet_ntop(AF_INET, &adresa, adresa_SMS, sizeof adresa_SMS) == adresa_SMS && strcmp(adresa_SMS, "10.0.2.2") == 0);
    verifikovati(inet_pton(AF_INET, "256.0.0.1", &adresa) == 0 && ntohl(adresa.s_addr) == 0x0a000202U);
    verifikovati(inet_pton(AF_INET, "01.0.0.1", &adresa) == 0);
    verifikovati(inet_ntop(AF_INET, &adresa, adresa_SMS, 3) == NULL && errno == ENOSPC);
    verifikovati(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], stavka_COUNT = 0; char ime[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        ime[4] = '0' + INDEX;
        int 열린파일 = open(ime, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verifikovati(errno == ENOSPC); break; }
        보관[stavka_COUNT++] = 열린파일;
    }
    verifikovati(stavka_COUNT > 0 && stavka_COUNT < 8);
    verifikovati(unlink("slot0") == 0);
    verifikovati(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verifikovati(close(보관[0]) == 0);
    Datoteka = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifikovati(Datoteka >= 0 && close(Datoteka) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < stavka_COUNT; INDEX++) {
        ime[4] = '0' + INDEX;
        verifikovati(close(보관[INDEX]) == 0 && unlink(ime) == 0);
    }
    verifikovati(fsync(-1) == -1 && errno == EBADF);
    verifikovati(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
