#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int услов, int ред) {
    검사항목수++;
    if (!услов) {
        puts("POSIX CHECK FAILED");
        char цифра_VALUE[12]; int должина_VALUE = 0;
        do { цифра_VALUE[должина_VALUE++] = '0' + ред % 10; ред /= 10; } while (ред);
        while (должина_VALUE) putchar(цифра_VALUE[--должина_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define провери(услов) 검사((услов), __LINE__)

int main(int 인수개수, char **аргумент_Список) {
    char податоци[32]; struct stat статус_VALUE;
    провери(인수개수 == 2 && strcmp(аргумент_Список[1], "check") == 0 && аргумент_Список[2] == 0);
    провери(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    провери(отвори_датотека("absent", само_за_читање_VALUE) == -1 && 오류번호 == ENOENT);
    int Датотека = отвори_датотека("/posix.txt", чита_пишува | 새파일만들기, 0640);
    провери(Датотека == 3);
    провери(запиши_датотека_податоци(Датотека, "abcd", 4) == 4);
    провери(отвори_датотека("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    провери(파일상태읽기(Датотека, &статус_VALUE) == 0 && статус_VALUE.st_size == 4 && S_ISREG(статус_VALUE.st_mode));
    провери((статус_VALUE.st_mode & 0777) == 0640 && статус_VALUE.st_nlink == 1);
    провери(пребарај_датотека(Датотека, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Датотека);
    провери(복제 == 4);
    провери(파일자료읽기(복제, податоци, 2) == 2 && memcmp(податоци, "ab", 2) == 0);
    провери(파일자료읽기(Датотека, податоци, 2) == 2 && memcmp(податоци, "cd", 2) == 0);
    провери(파일자료읽기(Датотека, податоци, 1) == 0);
    провери(fcntl(Датотека, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Датотека, F_GETFD) == 1);
    провери(fcntl(복제, F_GETFD) == 0);
    провери(dup2(Датотека, Датотека) == Датотека && fcntl(Датотека, F_GETFD) == 1);
    провери(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    провери(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Датотека, F_GETFL) & O_APPEND));
    провери(lseek(Датотека, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Датотека, 0, SEEK_CUR) == 5);
    провери(fcntl(Датотека, F_SETFL, 0) == 0);
    провери(lseek(Датотека, 8, SEEK_SET) == 8 && write(Датотека, "Z", 1) == 1);
    провери(lseek(복제, 5, SEEK_SET) == 5 && read(Датотека, податоци, 4) == 4);
    провери(податоци[0] == 0 && податоци[1] == 0 && податоци[2] == 0 && податоци[3] == 'Z');
    провери(ftruncate(Датотека, 2) == 0 && lseek(Датотека, 0, SEEK_CUR) == 9);
    провери(ftruncate(Датотека, 6) == 0 && lseek(Датотека, 2, SEEK_SET) == 2 && read(Датотека, податоци, 4) == 4);
    провери(!податоци[0] && !податоци[1] && !податоци[2] && !податоци[3]);
    провери(lseek(Датотека, 2147483647, SEEK_SET) == 2147483647);
    провери(lseek(Датотека, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    провери(lseek(Датотека, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    провери(write(Датотека, "!", 1) == -1 && errno == EFBIG);
    провери(lseek(Датотека, 0, SEEK_SET) == 0);
    провери(read(Датотека, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    провери(read(Датотека, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    провери(write(Датотека, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    провери(read(Датотека, податоци, (size_t)-1) == -1 && errno == EINVAL);
    провери(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    провери(fstat(Датотека, (void *)0x00100000) == -1 && errno == EFAULT);
    провери(lseek(Датотека, 0, SEEK_CUR) == 0);
    провери(read(Датотека, NULL, 0) == 0 && write(Датотека, NULL, 0) == 0);
    провери(отстрани_датотека_внес_име("posix.txt") == 0);
    провери(fstat(Датотека, &статус_VALUE) == 0 && статус_VALUE.st_nlink == 0 && статус_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    провери(새파일 == 5 && fstat(새파일, &статус_VALUE) == 0 && статус_VALUE.st_size == 0);
    провери(read(Датотека, податоци, 2) == 2 && memcmp(податоци, "ab", 2) == 0);
    провери(close(Датотека) == 0 && close(복제) == 0 && close(새파일) == 0);
    провери(close(새파일) == -1 && errno == EBADF);
    провери(unlink("posix.txt") == 0);
    Датотека = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    провери(Датотека == 3 && fcntl(Датотека, F_GETFD) == 1);
    провери(read(Датотека, податоци, 1) == -1 && errno == EBADF);
    провери(write(Датотека, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) провери(dup(Датотека) == INDEX);
    провери(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    провери(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    провери(fstat(Датотека, &статус_VALUE) == 0 && статус_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) провери(close(INDEX) == 0);
    провери(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Датотека = open("posix.txt", O_RDONLY);
    провери(Датотека == 3 && write(Датотека, податоци, 1) == -1 && errno == EBADF);
    провери(fcntl(Датотека, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    провери(close(8) == 0 && close(Датотека) == 0 && unlink("posix.txt") == 0);
    провери(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    провери(fstat(1, &статус_VALUE) == 0 && S_ISCHR(статус_VALUE.st_mode));
    провери(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    провери(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr адреса; char адреса_СМС[16];
    провери(inet_pton(AF_INET, "10.0.2.2", &адреса) == 1 && ntohl(адреса.s_addr) == 0x0a000202U);
    провери(inet_ntop(AF_INET, &адреса, адреса_СМС, sizeof адреса_СМС) == адреса_СМС && strcmp(адреса_СМС, "10.0.2.2") == 0);
    провери(inet_pton(AF_INET, "256.0.0.1", &адреса) == 0 && ntohl(адреса.s_addr) == 0x0a000202U);
    провери(inet_pton(AF_INET, "01.0.0.1", &адреса) == 0);
    провери(inet_ntop(AF_INET, &адреса, адреса_СМС, 3) == NULL && errno == ENOSPC);
    провери(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], ставка_COUNT = 0; char Име[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Име[4] = '0' + INDEX;
        int 열린파일 = open(Име, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { провери(errno == ENOSPC); break; }
        보관[ставка_COUNT++] = 열린파일;
    }
    провери(ставка_COUNT > 0 && ставка_COUNT < 8);
    провери(unlink("slot0") == 0);
    провери(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    провери(close(보관[0]) == 0);
    Датотека = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    провери(Датотека >= 0 && close(Датотека) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < ставка_COUNT; INDEX++) {
        Име[4] = '0' + INDEX;
        провери(close(보관[INDEX]) == 0 && unlink(Име) == 0);
    }
    провери(fsync(-1) == -1 && errno == EBADF);
    провери(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
