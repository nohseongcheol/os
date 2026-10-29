#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int pogoj, int Črtni) {
    검사항목수++;
    if (!pogoj) {
        puts("POSIX CHECK FAILED");
        char številka_VALUE[12]; int 길이 = 0;
        do { številka_VALUE[길이++] = '0' + Črtni % 10; Črtni /= 10; } while (Črtni);
        while (길이) putchar(številka_VALUE[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define 확인(pogoj) 검사((pogoj), __LINE__)

int main(int 인수개수, char **argument_Seznam) {
    char podatki[32]; struct stat stanje_VALUE;
    확인(인수개수 == 2 && strcmp(argument_Seznam[1], "check") == 0 && argument_Seznam[2] == 0);
    확인(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    확인(odprto_Datoteka("absent", samo_za_branje_VALUE) == -1 && številka_napake == ENOENT);
    int Datoteka = odprto_Datoteka("/posix.txt", branje_pisanje | 새파일만들기, 0640);
    확인(Datoteka == 3);
    확인(pisati_Datoteka_podatki(Datoteka, "abcd", 4) == 4);
    확인(odprto_Datoteka("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    확인(파일상태읽기(Datoteka, &stanje_VALUE) == 0 && stanje_VALUE.st_size == 4 && S_ISREG(stanje_VALUE.st_mode));
    확인((stanje_VALUE.st_mode & 0777) == 0640 && stanje_VALUE.st_nlink == 1);
    확인(iskati_Datoteka(Datoteka, 0, 처음기준) == 0);
    int klon_VALUE = 파일서술자복제(Datoteka);
    확인(klon_VALUE == 4);
    확인(파일자료읽기(klon_VALUE, podatki, 2) == 2 && memcmp(podatki, "ab", 2) == 0);
    확인(파일자료읽기(Datoteka, podatki, 2) == 2 && memcmp(podatki, "cd", 2) == 0);
    확인(파일자료읽기(Datoteka, podatki, 1) == 0);
    확인(fcntl(Datoteka, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Datoteka, F_GETFD) == 1);
    확인(fcntl(klon_VALUE, F_GETFD) == 0);
    확인(dup2(Datoteka, Datoteka) == Datoteka && fcntl(Datoteka, F_GETFD) == 1);
    확인(dup2(-1, klon_VALUE) == -1 && errno == EBADF && fcntl(klon_VALUE, F_GETFD) == 0);
    확인(fcntl(klon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Datoteka, F_GETFL) & O_APPEND));
    확인(lseek(Datoteka, 0, SEEK_SET) == 0 && write(klon_VALUE, "e", 1) == 1 && lseek(Datoteka, 0, SEEK_CUR) == 5);
    확인(fcntl(Datoteka, F_SETFL, 0) == 0);
    확인(lseek(Datoteka, 8, SEEK_SET) == 8 && write(Datoteka, "Z", 1) == 1);
    확인(lseek(klon_VALUE, 5, SEEK_SET) == 5 && read(Datoteka, podatki, 4) == 4);
    확인(podatki[0] == 0 && podatki[1] == 0 && podatki[2] == 0 && podatki[3] == 'Z');
    확인(ftruncate(Datoteka, 2) == 0 && lseek(Datoteka, 0, SEEK_CUR) == 9);
    확인(ftruncate(Datoteka, 6) == 0 && lseek(Datoteka, 2, SEEK_SET) == 2 && read(Datoteka, podatki, 4) == 4);
    확인(!podatki[0] && !podatki[1] && !podatki[2] && !podatki[3]);
    확인(lseek(Datoteka, 2147483647, SEEK_SET) == 2147483647);
    확인(lseek(Datoteka, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    확인(lseek(Datoteka, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    확인(write(Datoteka, "!", 1) == -1 && errno == EFBIG);
    확인(lseek(Datoteka, 0, SEEK_SET) == 0);
    확인(read(Datoteka, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(Datoteka, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    확인(write(Datoteka, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(Datoteka, podatki, (size_t)-1) == -1 && errno == EINVAL);
    확인(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    확인(fstat(Datoteka, (void *)0x00100000) == -1 && errno == EFAULT);
    확인(lseek(Datoteka, 0, SEEK_CUR) == 0);
    확인(read(Datoteka, NULL, 0) == 0 && write(Datoteka, NULL, 0) == 0);
    확인(odstraniti_Datoteka_vnos_ime("posix.txt") == 0);
    확인(fstat(Datoteka, &stanje_VALUE) == 0 && stanje_VALUE.st_nlink == 0 && stanje_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(새파일 == 5 && fstat(새파일, &stanje_VALUE) == 0 && stanje_VALUE.st_size == 0);
    확인(read(Datoteka, podatki, 2) == 2 && memcmp(podatki, "ab", 2) == 0);
    확인(close(Datoteka) == 0 && close(klon_VALUE) == 0 && close(새파일) == 0);
    확인(close(새파일) == -1 && errno == EBADF);
    확인(unlink("posix.txt") == 0);
    Datoteka = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    확인(Datoteka == 3 && fcntl(Datoteka, F_GETFD) == 1);
    확인(read(Datoteka, podatki, 1) == -1 && errno == EBADF);
    확인(write(Datoteka, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) 확인(dup(Datoteka) == INDEX);
    확인(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    확인(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    확인(fstat(Datoteka, &stanje_VALUE) == 0 && stanje_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) 확인(close(INDEX) == 0);
    확인(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Datoteka = open("posix.txt", O_RDONLY);
    확인(Datoteka == 3 && write(Datoteka, podatki, 1) == -1 && errno == EBADF);
    확인(fcntl(Datoteka, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    확인(close(8) == 0 && close(Datoteka) == 0 && unlink("posix.txt") == 0);
    확인(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    확인(fstat(1, &stanje_VALUE) == 0 && S_ISCHR(stanje_VALUE.st_mode));
    확인(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    확인(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr naslov; char naslov_SMS[16];
    확인(inet_pton(AF_INET, "10.0.2.2", &naslov) == 1 && ntohl(naslov.s_addr) == 0x0a000202U);
    확인(inet_ntop(AF_INET, &naslov, naslov_SMS, sizeof naslov_SMS) == naslov_SMS && strcmp(naslov_SMS, "10.0.2.2") == 0);
    확인(inet_pton(AF_INET, "256.0.0.1", &naslov) == 0 && ntohl(naslov.s_addr) == 0x0a000202U);
    확인(inet_pton(AF_INET, "01.0.0.1", &naslov) == 0);
    확인(inet_ntop(AF_INET, &naslov, naslov_SMS, 3) == NULL && errno == ENOSPC);
    확인(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], element_COUNT = 0; char Ime[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Ime[4] = '0' + INDEX;
        int 열린파일 = open(Ime, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { 확인(errno == ENOSPC); break; }
        보관[element_COUNT++] = 열린파일;
    }
    확인(element_COUNT > 0 && element_COUNT < 8);
    확인(unlink("slot0") == 0);
    확인(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    확인(close(보관[0]) == 0);
    Datoteka = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(Datoteka >= 0 && close(Datoteka) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < element_COUNT; INDEX++) {
        Ime[4] = '0' + INDEX;
        확인(close(보관[INDEX]) == 0 && unlink(Ime) == 0);
    }
    확인(fsync(-1) == -1 && errno == EBADF);
    확인(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
