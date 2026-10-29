#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int kondizzjoni, int linja) {
    검사항목수++;
    if (!kondizzjoni) {
        puts("POSIX CHECK FAILED");
        char ċifra_VALUE[12]; int tul_VALUE = 0;
        do { ċifra_VALUE[tul_VALUE++] = '0' + linja % 10; linja /= 10; } while (linja);
        while (tul_VALUE) putchar(ċifra_VALUE[--tul_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define vverifika(kondizzjoni) 검사((kondizzjoni), __LINE__)

int main(int 인수개수, char **argument_Lista) {
    char data[32]; struct stat stat_VALUE;
    vverifika(인수개수 == 2 && strcmp(argument_Lista[1], "check") == 0 && argument_Lista[2] == 0);
    vverifika(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    vverifika(fetaħ_fajl("absent", qari_biss_VALUE) == -1 && 오류번호 == ENOENT);
    int fajl = fetaħ_fajl("/posix.txt", qari_kitba | 새파일만들기, 0640);
    vverifika(fajl == 3);
    vverifika(kiteb_fajl_data(fajl, "abcd", 4) == 4);
    vverifika(fetaħ_fajl("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    vverifika(파일상태읽기(fajl, &stat_VALUE) == 0 && stat_VALUE.st_size == 4 && S_ISREG(stat_VALUE.st_mode));
    vverifika((stat_VALUE.st_mode & 0777) == 0640 && stat_VALUE.st_nlink == 1);
    vverifika(fittex_fajl(fajl, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(fajl);
    vverifika(복제 == 4);
    vverifika(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    vverifika(파일자료읽기(fajl, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    vverifika(파일자료읽기(fajl, data, 1) == 0);
    vverifika(fcntl(fajl, F_SETFD, FD_CLOEXEC) == 0 && fcntl(fajl, F_GETFD) == 1);
    vverifika(fcntl(복제, F_GETFD) == 0);
    vverifika(dup2(fajl, fajl) == fajl && fcntl(fajl, F_GETFD) == 1);
    vverifika(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    vverifika(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(fajl, F_GETFL) & O_APPEND));
    vverifika(lseek(fajl, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(fajl, 0, SEEK_CUR) == 5);
    vverifika(fcntl(fajl, F_SETFL, 0) == 0);
    vverifika(lseek(fajl, 8, SEEK_SET) == 8 && write(fajl, "Z", 1) == 1);
    vverifika(lseek(복제, 5, SEEK_SET) == 5 && read(fajl, data, 4) == 4);
    vverifika(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    vverifika(ftruncate(fajl, 2) == 0 && lseek(fajl, 0, SEEK_CUR) == 9);
    vverifika(ftruncate(fajl, 6) == 0 && lseek(fajl, 2, SEEK_SET) == 2 && read(fajl, data, 4) == 4);
    vverifika(!data[0] && !data[1] && !data[2] && !data[3]);
    vverifika(lseek(fajl, 2147483647, SEEK_SET) == 2147483647);
    vverifika(lseek(fajl, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    vverifika(lseek(fajl, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    vverifika(write(fajl, "!", 1) == -1 && errno == EFBIG);
    vverifika(lseek(fajl, 0, SEEK_SET) == 0);
    vverifika(read(fajl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    vverifika(read(fajl, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    vverifika(write(fajl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    vverifika(read(fajl, data, (size_t)-1) == -1 && errno == EINVAL);
    vverifika(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    vverifika(fstat(fajl, (void *)0x00100000) == -1 && errno == EFAULT);
    vverifika(lseek(fajl, 0, SEEK_CUR) == 0);
    vverifika(read(fajl, NULL, 0) == 0 && write(fajl, NULL, 0) == 0);
    vverifika(neħħa_fajl_entrata_isem("posix.txt") == 0);
    vverifika(fstat(fajl, &stat_VALUE) == 0 && stat_VALUE.st_nlink == 0 && stat_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    vverifika(새파일 == 5 && fstat(새파일, &stat_VALUE) == 0 && stat_VALUE.st_size == 0);
    vverifika(read(fajl, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    vverifika(close(fajl) == 0 && close(복제) == 0 && close(새파일) == 0);
    vverifika(close(새파일) == -1 && errno == EBADF);
    vverifika(unlink("posix.txt") == 0);
    fajl = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    vverifika(fajl == 3 && fcntl(fajl, F_GETFD) == 1);
    vverifika(read(fajl, data, 1) == -1 && errno == EBADF);
    vverifika(write(fajl, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) vverifika(dup(fajl) == INDEX);
    vverifika(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    vverifika(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    vverifika(fstat(fajl, &stat_VALUE) == 0 && stat_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) vverifika(close(INDEX) == 0);
    vverifika(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    fajl = open("posix.txt", O_RDONLY);
    vverifika(fajl == 3 && write(fajl, data, 1) == -1 && errno == EBADF);
    vverifika(fcntl(fajl, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    vverifika(close(8) == 0 && close(fajl) == 0 && unlink("posix.txt") == 0);
    vverifika(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    vverifika(fstat(1, &stat_VALUE) == 0 && S_ISCHR(stat_VALUE.st_mode));
    vverifika(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    vverifika(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    vverifika(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    vverifika(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    vverifika(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    vverifika(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    vverifika(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    vverifika(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], element_COUNT = 0; char isem[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        isem[4] = '0' + INDEX;
        int 열린파일 = open(isem, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { vverifika(errno == ENOSPC); break; }
        보관[element_COUNT++] = 열린파일;
    }
    vverifika(element_COUNT > 0 && element_COUNT < 8);
    vverifika(unlink("slot0") == 0);
    vverifika(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    vverifika(close(보관[0]) == 0);
    fajl = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    vverifika(fajl >= 0 && close(fajl) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < element_COUNT; INDEX++) {
        isem[4] = '0' + INDEX;
        vverifika(close(보관[INDEX]) == 0 && unlink(isem) == 0);
    }
    vverifika(fsync(-1) == -1 && errno == EBADF);
    vverifika(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
