#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int toestand, int lyn) {
    검사항목수++;
    if (!toestand) {
        puts("POSIX CHECK FAILED");
        char syfer_VALUE[12]; int lengte_VALUE = 0;
        do { syfer_VALUE[lengte_VALUE++] = '0' + lyn % 10; lyn /= 10; } while (lyn);
        while (lengte_VALUE) putchar(syfer_VALUE[--lengte_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define verifieer(toestand) 검사((toestand), __LINE__)

int main(int 인수개수, char **argument_Lys) {
    char data[32]; struct stat stand_VALUE;
    verifieer(인수개수 == 2 && strcmp(argument_Lys[1], "check") == 0 && argument_Lys[2] == 0);
    verifieer(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verifieer(skep_lêer("absent", leesalleen_VALUE) == -1 && 오류번호 == ENOENT);
    int Lêer = skep_lêer("/posix.txt", lees_skryf | 새파일만들기, 0640);
    verifieer(Lêer == 3);
    verifieer(skryf_lêer_data(Lêer, "abcd", 4) == 4);
    verifieer(skep_lêer("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verifieer(파일상태읽기(Lêer, &stand_VALUE) == 0 && stand_VALUE.st_size == 4 && S_ISREG(stand_VALUE.st_mode));
    verifieer((stand_VALUE.st_mode & 0777) == 0640 && stand_VALUE.st_nlink == 1);
    verifieer(soek_lêer(Lêer, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Lêer);
    verifieer(복제 == 4);
    verifieer(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    verifieer(파일자료읽기(Lêer, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    verifieer(파일자료읽기(Lêer, data, 1) == 0);
    verifieer(fcntl(Lêer, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Lêer, F_GETFD) == 1);
    verifieer(fcntl(복제, F_GETFD) == 0);
    verifieer(dup2(Lêer, Lêer) == Lêer && fcntl(Lêer, F_GETFD) == 1);
    verifieer(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    verifieer(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Lêer, F_GETFL) & O_APPEND));
    verifieer(lseek(Lêer, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Lêer, 0, SEEK_CUR) == 5);
    verifieer(fcntl(Lêer, F_SETFL, 0) == 0);
    verifieer(lseek(Lêer, 8, SEEK_SET) == 8 && write(Lêer, "Z", 1) == 1);
    verifieer(lseek(복제, 5, SEEK_SET) == 5 && read(Lêer, data, 4) == 4);
    verifieer(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    verifieer(ftruncate(Lêer, 2) == 0 && lseek(Lêer, 0, SEEK_CUR) == 9);
    verifieer(ftruncate(Lêer, 6) == 0 && lseek(Lêer, 2, SEEK_SET) == 2 && read(Lêer, data, 4) == 4);
    verifieer(!data[0] && !data[1] && !data[2] && !data[3]);
    verifieer(lseek(Lêer, 2147483647, SEEK_SET) == 2147483647);
    verifieer(lseek(Lêer, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verifieer(lseek(Lêer, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verifieer(write(Lêer, "!", 1) == -1 && errno == EFBIG);
    verifieer(lseek(Lêer, 0, SEEK_SET) == 0);
    verifieer(read(Lêer, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifieer(read(Lêer, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verifieer(write(Lêer, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifieer(read(Lêer, data, (size_t)-1) == -1 && errno == EINVAL);
    verifieer(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verifieer(fstat(Lêer, (void *)0x00100000) == -1 && errno == EFAULT);
    verifieer(lseek(Lêer, 0, SEEK_CUR) == 0);
    verifieer(read(Lêer, NULL, 0) == 0 && write(Lêer, NULL, 0) == 0);
    verifieer(verwyder_lêer_inskrywing_naam("posix.txt") == 0);
    verifieer(fstat(Lêer, &stand_VALUE) == 0 && stand_VALUE.st_nlink == 0 && stand_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifieer(새파일 == 5 && fstat(새파일, &stand_VALUE) == 0 && stand_VALUE.st_size == 0);
    verifieer(read(Lêer, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    verifieer(close(Lêer) == 0 && close(복제) == 0 && close(새파일) == 0);
    verifieer(close(새파일) == -1 && errno == EBADF);
    verifieer(unlink("posix.txt") == 0);
    Lêer = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verifieer(Lêer == 3 && fcntl(Lêer, F_GETFD) == 1);
    verifieer(read(Lêer, data, 1) == -1 && errno == EBADF);
    verifieer(write(Lêer, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verifieer(dup(Lêer) == INDEX);
    verifieer(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verifieer(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verifieer(fstat(Lêer, &stand_VALUE) == 0 && stand_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verifieer(close(INDEX) == 0);
    verifieer(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Lêer = open("posix.txt", O_RDONLY);
    verifieer(Lêer == 3 && write(Lêer, data, 1) == -1 && errno == EBADF);
    verifieer(fcntl(Lêer, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verifieer(close(8) == 0 && close(Lêer) == 0 && unlink("posix.txt") == 0);
    verifieer(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verifieer(fstat(1, &stand_VALUE) == 0 && S_ISCHR(stand_VALUE.st_mode));
    verifieer(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verifieer(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr adres; char adres_SMS[16];
    verifieer(inet_pton(AF_INET, "10.0.2.2", &adres) == 1 && ntohl(adres.s_addr) == 0x0a000202U);
    verifieer(inet_ntop(AF_INET, &adres, adres_SMS, sizeof adres_SMS) == adres_SMS && strcmp(adres_SMS, "10.0.2.2") == 0);
    verifieer(inet_pton(AF_INET, "256.0.0.1", &adres) == 0 && ntohl(adres.s_addr) == 0x0a000202U);
    verifieer(inet_pton(AF_INET, "01.0.0.1", &adres) == 0);
    verifieer(inet_ntop(AF_INET, &adres, adres_SMS, 3) == NULL && errno == ENOSPC);
    verifieer(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], item_COUNT = 0; char Naam[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Naam[4] = '0' + INDEX;
        int 열린파일 = open(Naam, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verifieer(errno == ENOSPC); break; }
        보관[item_COUNT++] = 열린파일;
    }
    verifieer(item_COUNT > 0 && item_COUNT < 8);
    verifieer(unlink("slot0") == 0);
    verifieer(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verifieer(close(보관[0]) == 0);
    Lêer = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifieer(Lêer >= 0 && close(Lêer) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < item_COUNT; INDEX++) {
        Naam[4] = '0' + INDEX;
        verifieer(close(보관[INDEX]) == 0 && unlink(Naam) == 0);
    }
    verifieer(fsync(-1) == -1 && errno == EBADF);
    verifieer(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
