#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int qanuinniq, int titikutaak) {
    검사항목수++;
    if (!qanuinniq) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int takininga_atuutilik = 0;
        do { 숫자[takininga_atuutilik++] = '0' + titikutaak % 10; titikutaak /= 10; } while (titikutaak);
        while (takininga_atuutilik) putchar(숫자[--takininga_atuutilik]);
        putchar('\n'); _exit(1);
    }
}
#define nalunairli_1aacb54c(qanuinniq) 검사((qanuinniq), __LINE__)

int main(int 인수개수, char **aturniqarnirainiq_Titiqpalliagaq) {
    char titiqqat[32]; struct stat qanuilinganiq_atuutilik;
    nalunairli_1aacb54c(인수개수 == 2 && strcmp(aturniqarnirainiq_Titiqpalliagaq[1], "check") == 0 && aturniqarnirainiq_Titiqpalliagaq[2] == 0);
    nalunairli_1aacb54c(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    nalunairli_1aacb54c(matuirli_ini("absent", takugatuinnaq_atuutilik) == -1 && 오류번호 == ENOENT);
    int ini = matuirli_ini("/posix.txt", uqalimaarli_titirarli | 새파일만들기, 0640);
    nalunairli_1aacb54c(ini == 3);
    nalunairli_1aacb54c(titiraq_ini_titiqqat(ini, "abcd", 4) == 4);
    nalunairli_1aacb54c(matuirli_ini("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    nalunairli_1aacb54c(파일상태읽기(ini, &qanuilinganiq_atuutilik) == 0 && qanuilinganiq_atuutilik.st_size == 4 && S_ISREG(qanuilinganiq_atuutilik.st_mode));
    nalunairli_1aacb54c((qanuilinganiq_atuutilik.st_mode & 0777) == 0640 && qanuilinganiq_atuutilik.st_nlink == 1);
    nalunairli_1aacb54c(qinirli_ini(ini, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ini);
    nalunairli_1aacb54c(복제 == 4);
    nalunairli_1aacb54c(파일자료읽기(복제, titiqqat, 2) == 2 && memcmp(titiqqat, "ab", 2) == 0);
    nalunairli_1aacb54c(파일자료읽기(ini, titiqqat, 2) == 2 && memcmp(titiqqat, "cd", 2) == 0);
    nalunairli_1aacb54c(파일자료읽기(ini, titiqqat, 1) == 0);
    nalunairli_1aacb54c(fcntl(ini, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ini, F_GETFD) == 1);
    nalunairli_1aacb54c(fcntl(복제, F_GETFD) == 0);
    nalunairli_1aacb54c(dup2(ini, ini) == ini && fcntl(ini, F_GETFD) == 1);
    nalunairli_1aacb54c(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    nalunairli_1aacb54c(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ini, F_GETFL) & O_APPEND));
    nalunairli_1aacb54c(lseek(ini, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ini, 0, SEEK_CUR) == 5);
    nalunairli_1aacb54c(fcntl(ini, F_SETFL, 0) == 0);
    nalunairli_1aacb54c(lseek(ini, 8, SEEK_SET) == 8 && write(ini, "Z", 1) == 1);
    nalunairli_1aacb54c(lseek(복제, 5, SEEK_SET) == 5 && read(ini, titiqqat, 4) == 4);
    nalunairli_1aacb54c(titiqqat[0] == 0 && titiqqat[1] == 0 && titiqqat[2] == 0 && titiqqat[3] == 'Z');
    nalunairli_1aacb54c(ftruncate(ini, 2) == 0 && lseek(ini, 0, SEEK_CUR) == 9);
    nalunairli_1aacb54c(ftruncate(ini, 6) == 0 && lseek(ini, 2, SEEK_SET) == 2 && read(ini, titiqqat, 4) == 4);
    nalunairli_1aacb54c(!titiqqat[0] && !titiqqat[1] && !titiqqat[2] && !titiqqat[3]);
    nalunairli_1aacb54c(lseek(ini, 2147483647, SEEK_SET) == 2147483647);
    nalunairli_1aacb54c(lseek(ini, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    nalunairli_1aacb54c(lseek(ini, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    nalunairli_1aacb54c(write(ini, "!", 1) == -1 && errno == EFBIG);
    nalunairli_1aacb54c(lseek(ini, 0, SEEK_SET) == 0);
    nalunairli_1aacb54c(read(ini, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    nalunairli_1aacb54c(read(ini, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    nalunairli_1aacb54c(write(ini, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    nalunairli_1aacb54c(read(ini, titiqqat, (size_t)-1) == -1 && errno == EINVAL);
    nalunairli_1aacb54c(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    nalunairli_1aacb54c(fstat(ini, (void *)0x00100000) == -1 && errno == EFAULT);
    nalunairli_1aacb54c(lseek(ini, 0, SEEK_CUR) == 0);
    nalunairli_1aacb54c(read(ini, NULL, 0) == 0 && write(ini, NULL, 0) == 0);
    nalunairli_1aacb54c(sanirvalli_ini_Iliniku_atiq("posix.txt") == 0);
    nalunairli_1aacb54c(fstat(ini, &qanuilinganiq_atuutilik) == 0 && qanuilinganiq_atuutilik.st_nlink == 0 && qanuilinganiq_atuutilik.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    nalunairli_1aacb54c(새파일 == 5 && fstat(새파일, &qanuilinganiq_atuutilik) == 0 && qanuilinganiq_atuutilik.st_size == 0);
    nalunairli_1aacb54c(read(ini, titiqqat, 2) == 2 && memcmp(titiqqat, "ab", 2) == 0);
    nalunairli_1aacb54c(close(ini) == 0 && close(복제) == 0 && close(새파일) == 0);
    nalunairli_1aacb54c(close(새파일) == -1 && errno == EBADF);
    nalunairli_1aacb54c(unlink("posix.txt") == 0);
    ini = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    nalunairli_1aacb54c(ini == 3 && fcntl(ini, F_GETFD) == 1);
    nalunairli_1aacb54c(read(ini, titiqqat, 1) == -1 && errno == EBADF);
    nalunairli_1aacb54c(write(ini, "keep", 4) == 4);
    for (int nalunaiqsimavik = 4; nalunaiqsimavik < 32; nalunaiqsimavik++) nalunairli_1aacb54c(dup(ini) == nalunaiqsimavik);
    nalunairli_1aacb54c(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    nalunairli_1aacb54c(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    nalunairli_1aacb54c(fstat(ini, &qanuilinganiq_atuutilik) == 0 && qanuilinganiq_atuutilik.st_size == 4);
    for (int nalunaiqsimavik = 3; nalunaiqsimavik < 32; nalunaiqsimavik++) nalunairli_1aacb54c(close(nalunaiqsimavik) == 0);
    nalunairli_1aacb54c(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ini = open("posix.txt", O_RDONLY);
    nalunairli_1aacb54c(ini == 3 && write(ini, titiqqat, 1) == -1 && errno == EBADF);
    nalunairli_1aacb54c(fcntl(ini, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    nalunairli_1aacb54c(close(8) == 0 && close(ini) == 0 && unlink("posix.txt") == 0);
    nalunairli_1aacb54c(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    nalunairli_1aacb54c(fstat(1, &qanuilinganiq_atuutilik) == 0 && S_ISCHR(qanuilinganiq_atuutilik.st_mode));
    nalunairli_1aacb54c(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    nalunairli_1aacb54c(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr turaarut; char turaarut_titiqqaq[16];
    nalunairli_1aacb54c(inet_pton(AF_INET, "10.0.2.2", &turaarut) == 1 && ntohl(turaarut.s_addr) == 0x0a000202U);
    nalunairli_1aacb54c(inet_ntop(AF_INET, &turaarut, turaarut_titiqqaq, sizeof turaarut_titiqqaq) == turaarut_titiqqaq && strcmp(turaarut_titiqqaq, "10.0.2.2") == 0);
    nalunairli_1aacb54c(inet_pton(AF_INET, "256.0.0.1", &turaarut) == 0 && ntohl(turaarut.s_addr) == 0x0a000202U);
    nalunairli_1aacb54c(inet_pton(AF_INET, "01.0.0.1", &turaarut) == 0);
    nalunairli_1aacb54c(inet_ntop(AF_INET, &turaarut, turaarut_titiqqaq, 3) == NULL && errno == ENOSPC);
    nalunairli_1aacb54c(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char atiq[] = "slot0";
    for (int nalunaiqsimavik = 0; nalunaiqsimavik < 8; nalunaiqsimavik++) {
        atiq[4] = '0' + nalunaiqsimavik;
        int 열린파일 = open(atiq, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { nalunairli_1aacb54c(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    nalunairli_1aacb54c(개수 > 0 && 개수 < 8);
    nalunairli_1aacb54c(unlink("slot0") == 0);
    nalunairli_1aacb54c(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    nalunairli_1aacb54c(close(보관[0]) == 0);
    ini = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    nalunairli_1aacb54c(ini >= 0 && close(ini) == 0 && unlink("held-slot") == 0);
    for (int nalunaiqsimavik = 1; nalunaiqsimavik < 개수; nalunaiqsimavik++) {
        atiq[4] = '0' + nalunaiqsimavik;
        nalunairli_1aacb54c(close(보관[nalunaiqsimavik]) == 0 && unlink(atiq) == 0);
    }
    nalunairli_1aacb54c(fsync(-1) == -1 && errno == EBADF);
    nalunairli_1aacb54c(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
