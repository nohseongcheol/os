#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int cyflwr, int llinell) {
    검사항목수++;
    if (!cyflwr) {
        puts("POSIX CHECK FAILED");
        char digid_VALUE[12]; int hyd_VALUE = 0;
        do { digid_VALUE[hyd_VALUE++] = '0' + llinell % 10; llinell /= 10; } while (llinell);
        while (hyd_VALUE) putchar(digid_VALUE[--hyd_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define dilysu(cyflwr) 검사((cyflwr), __LINE__)

int main(int 인수개수, char **arg_Rhestr) {
    char data[32]; struct stat cyflwr_VALUE;
    dilysu(인수개수 == 2 && strcmp(arg_Rhestr[1], "check") == 0 && arg_Rhestr[2] == 0);
    dilysu(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    dilysu(agor_ffeil("absent", darllen_yn_unig_VALUE) == -1 && 오류번호 == ENOENT);
    int Ffeil = agor_ffeil("/posix.txt", darllen_ysgrifennu | 새파일만들기, 0640);
    dilysu(Ffeil == 3);
    dilysu(ysgrifennu_ffeil_data(Ffeil, "abcd", 4) == 4);
    dilysu(agor_ffeil("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    dilysu(파일상태읽기(Ffeil, &cyflwr_VALUE) == 0 && cyflwr_VALUE.st_size == 4 && S_ISREG(cyflwr_VALUE.st_mode));
    dilysu((cyflwr_VALUE.st_mode & 0777) == 0640 && cyflwr_VALUE.st_nlink == 1);
    dilysu(chwilio_ffeil(Ffeil, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Ffeil);
    dilysu(복제 == 4);
    dilysu(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    dilysu(파일자료읽기(Ffeil, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    dilysu(파일자료읽기(Ffeil, data, 1) == 0);
    dilysu(fcntl(Ffeil, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Ffeil, F_GETFD) == 1);
    dilysu(fcntl(복제, F_GETFD) == 0);
    dilysu(dup2(Ffeil, Ffeil) == Ffeil && fcntl(Ffeil, F_GETFD) == 1);
    dilysu(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    dilysu(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Ffeil, F_GETFL) & O_APPEND));
    dilysu(lseek(Ffeil, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Ffeil, 0, SEEK_CUR) == 5);
    dilysu(fcntl(Ffeil, F_SETFL, 0) == 0);
    dilysu(lseek(Ffeil, 8, SEEK_SET) == 8 && write(Ffeil, "Z", 1) == 1);
    dilysu(lseek(복제, 5, SEEK_SET) == 5 && read(Ffeil, data, 4) == 4);
    dilysu(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    dilysu(ftruncate(Ffeil, 2) == 0 && lseek(Ffeil, 0, SEEK_CUR) == 9);
    dilysu(ftruncate(Ffeil, 6) == 0 && lseek(Ffeil, 2, SEEK_SET) == 2 && read(Ffeil, data, 4) == 4);
    dilysu(!data[0] && !data[1] && !data[2] && !data[3]);
    dilysu(lseek(Ffeil, 2147483647, SEEK_SET) == 2147483647);
    dilysu(lseek(Ffeil, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    dilysu(lseek(Ffeil, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    dilysu(write(Ffeil, "!", 1) == -1 && errno == EFBIG);
    dilysu(lseek(Ffeil, 0, SEEK_SET) == 0);
    dilysu(read(Ffeil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    dilysu(read(Ffeil, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    dilysu(write(Ffeil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    dilysu(read(Ffeil, data, (size_t)-1) == -1 && errno == EINVAL);
    dilysu(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    dilysu(fstat(Ffeil, (void *)0x00100000) == -1 && errno == EFAULT);
    dilysu(lseek(Ffeil, 0, SEEK_CUR) == 0);
    dilysu(read(Ffeil, NULL, 0) == 0 && write(Ffeil, NULL, 0) == 0);
    dilysu(tynnu_ffeil_cofnod_enw("posix.txt") == 0);
    dilysu(fstat(Ffeil, &cyflwr_VALUE) == 0 && cyflwr_VALUE.st_nlink == 0 && cyflwr_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    dilysu(새파일 == 5 && fstat(새파일, &cyflwr_VALUE) == 0 && cyflwr_VALUE.st_size == 0);
    dilysu(read(Ffeil, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    dilysu(close(Ffeil) == 0 && close(복제) == 0 && close(새파일) == 0);
    dilysu(close(새파일) == -1 && errno == EBADF);
    dilysu(unlink("posix.txt") == 0);
    Ffeil = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    dilysu(Ffeil == 3 && fcntl(Ffeil, F_GETFD) == 1);
    dilysu(read(Ffeil, data, 1) == -1 && errno == EBADF);
    dilysu(write(Ffeil, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) dilysu(dup(Ffeil) == INDEX);
    dilysu(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    dilysu(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    dilysu(fstat(Ffeil, &cyflwr_VALUE) == 0 && cyflwr_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) dilysu(close(INDEX) == 0);
    dilysu(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Ffeil = open("posix.txt", O_RDONLY);
    dilysu(Ffeil == 3 && write(Ffeil, data, 1) == -1 && errno == EBADF);
    dilysu(fcntl(Ffeil, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    dilysu(close(8) == 0 && close(Ffeil) == 0 && unlink("posix.txt") == 0);
    dilysu(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    dilysu(fstat(1, &cyflwr_VALUE) == 0 && S_ISCHR(cyflwr_VALUE.st_mode));
    dilysu(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    dilysu(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    dilysu(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    dilysu(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    dilysu(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    dilysu(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    dilysu(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    dilysu(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], eitem_COUNT = 0; char Enw[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Enw[4] = '0' + INDEX;
        int 열린파일 = open(Enw, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { dilysu(errno == ENOSPC); break; }
        보관[eitem_COUNT++] = 열린파일;
    }
    dilysu(eitem_COUNT > 0 && eitem_COUNT < 8);
    dilysu(unlink("slot0") == 0);
    dilysu(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    dilysu(close(보관[0]) == 0);
    Ffeil = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    dilysu(Ffeil >= 0 && close(Ffeil) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < eitem_COUNT; INDEX++) {
        Enw[4] = '0' + INDEX;
        dilysu(close(보관[INDEX]) == 0 && unlink(Enw) == 0);
    }
    dilysu(fsync(-1) == -1 && errno == EBADF);
    dilysu(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
