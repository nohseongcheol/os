#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int увјет, int редак) {
    검사항목수++;
    if (!увјет) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int дужина_вриједност = 0;
        do { 숫자[дужина_вриједност++] = '0' + редак % 10; редак /= 10; } while (редак);
        while (дужина_вриједност) putchar(숫자[--дужина_вриједност]);
        putchar('\n'); _exit(1);
    }
}
#define потврдити(увјет) 검사((увјет), __LINE__)

int main(int 인수개수, char **аргумент_списак) {
    char подаци[32]; struct stat стање_вриједност;
    потврдити(인수개수 == 2 && strcmp(аргумент_списак[1], "check") == 0 && аргумент_списак[2] == 0);
    потврдити(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    потврдити(отворити_фајл("absent", само_за_читање_вриједност) == -1 && 오류번호 == ENOENT);
    int фајл = отворити_фајл("/posix.txt", и_за_читање_и_за_писање | 새파일만들기, 0640);
    потврдити(фајл == 3);
    потврдити(писати_фајл_подаци(фајл, "abcd", 4) == 4);
    потврдити(отворити_фајл("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    потврдити(파일상태읽기(фајл, &стање_вриједност) == 0 && стање_вриједност.st_size == 4 && S_ISREG(стање_вриједност.st_mode));
    потврдити((стање_вриједност.st_mode & 0777) == 0640 && стање_вриједност.st_nlink == 1);
    потврдити(претражити_фајл(фајл, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(фајл);
    потврдити(복제 == 4);
    потврдити(파일자료읽기(복제, подаци, 2) == 2 && memcmp(подаци, "ab", 2) == 0);
    потврдити(파일자료읽기(фајл, подаци, 2) == 2 && memcmp(подаци, "cd", 2) == 0);
    потврдити(파일자료읽기(фајл, подаци, 1) == 0);
    потврдити(fcntl(фајл, F_SETFD, FD_CLOEXEC) == 0 && fcntl(фајл, F_GETFD) == 1);
    потврдити(fcntl(복제, F_GETFD) == 0);
    потврдити(dup2(фајл, фајл) == фајл && fcntl(фајл, F_GETFD) == 1);
    потврдити(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    потврдити(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(фајл, F_GETFL) & O_APPEND));
    потврдити(lseek(фајл, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(фајл, 0, SEEK_CUR) == 5);
    потврдити(fcntl(фајл, F_SETFL, 0) == 0);
    потврдити(lseek(фајл, 8, SEEK_SET) == 8 && write(фајл, "Z", 1) == 1);
    потврдити(lseek(복제, 5, SEEK_SET) == 5 && read(фајл, подаци, 4) == 4);
    потврдити(подаци[0] == 0 && подаци[1] == 0 && подаци[2] == 0 && подаци[3] == 'Z');
    потврдити(ftruncate(фајл, 2) == 0 && lseek(фајл, 0, SEEK_CUR) == 9);
    потврдити(ftruncate(фајл, 6) == 0 && lseek(фајл, 2, SEEK_SET) == 2 && read(фајл, подаци, 4) == 4);
    потврдити(!подаци[0] && !подаци[1] && !подаци[2] && !подаци[3]);
    потврдити(lseek(фајл, 2147483647, SEEK_SET) == 2147483647);
    потврдити(lseek(фајл, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    потврдити(lseek(фајл, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    потврдити(write(фајл, "!", 1) == -1 && errno == EFBIG);
    потврдити(lseek(фајл, 0, SEEK_SET) == 0);
    потврдити(read(фајл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    потврдити(read(фајл, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    потврдити(write(фајл, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    потврдити(read(фајл, подаци, (size_t)-1) == -1 && errno == EINVAL);
    потврдити(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    потврдити(fstat(фајл, (void *)0x00100000) == -1 && errno == EFAULT);
    потврдити(lseek(фајл, 0, SEEK_CUR) == 0);
    потврдити(read(фајл, NULL, 0) == 0 && write(фајл, NULL, 0) == 0);
    потврдити(уклонити_фајл_унос_назив("posix.txt") == 0);
    потврдити(fstat(фајл, &стање_вриједност) == 0 && стање_вриједност.st_nlink == 0 && стање_вриједност.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    потврдити(새파일 == 5 && fstat(새파일, &стање_вриједност) == 0 && стање_вриједност.st_size == 0);
    потврдити(read(фајл, подаци, 2) == 2 && memcmp(подаци, "ab", 2) == 0);
    потврдити(close(фајл) == 0 && close(복제) == 0 && close(새파일) == 0);
    потврдити(close(새파일) == -1 && errno == EBADF);
    потврдити(unlink("posix.txt") == 0);
    фајл = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    потврдити(фајл == 3 && fcntl(фајл, F_GETFD) == 1);
    потврдити(read(фајл, подаци, 1) == -1 && errno == EBADF);
    потврдити(write(фајл, "keep", 4) == 4);
    for (int индекс = 4; индекс < 32; индекс++) потврдити(dup(фајл) == индекс);
    потврдити(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    потврдити(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    потврдити(fstat(фајл, &стање_вриједност) == 0 && стање_вриједност.st_size == 4);
    for (int индекс = 3; индекс < 32; индекс++) потврдити(close(индекс) == 0);
    потврдити(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    фајл = open("posix.txt", O_RDONLY);
    потврдити(фајл == 3 && write(фајл, подаци, 1) == -1 && errno == EBADF);
    потврдити(fcntl(фајл, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    потврдити(close(8) == 0 && close(фајл) == 0 && unlink("posix.txt") == 0);
    потврдити(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    потврдити(fstat(1, &стање_вриједност) == 0 && S_ISCHR(стање_вриједност.st_mode));
    потврдити(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    потврдити(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr адреса; char адреса_текст[16];
    потврдити(inet_pton(AF_INET, "10.0.2.2", &адреса) == 1 && ntohl(адреса.s_addr) == 0x0a000202U);
    потврдити(inet_ntop(AF_INET, &адреса, адреса_текст, sizeof адреса_текст) == адреса_текст && strcmp(адреса_текст, "10.0.2.2") == 0);
    потврдити(inet_pton(AF_INET, "256.0.0.1", &адреса) == 0 && ntohl(адреса.s_addr) == 0x0a000202U);
    потврдити(inet_pton(AF_INET, "01.0.0.1", &адреса) == 0);
    потврдити(inet_ntop(AF_INET, &адреса, адреса_текст, 3) == NULL && errno == ENOSPC);
    потврдити(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char назив[] = "slot0";
    for (int индекс = 0; индекс < 8; индекс++) {
        назив[4] = '0' + индекс;
        int 열린파일 = open(назив, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { потврдити(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    потврдити(개수 > 0 && 개수 < 8);
    потврдити(unlink("slot0") == 0);
    потврдити(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    потврдити(close(보관[0]) == 0);
    фајл = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    потврдити(фајл >= 0 && close(фајл) == 0 && unlink("held-slot") == 0);
    for (int индекс = 1; индекс < 개수; индекс++) {
        назив[4] = '0' + индекс;
        потврдити(close(보관[индекс]) == 0 && unlink(назив) == 0);
    }
    потврдити(fsync(-1) == -1 && errno == EBADF);
    потврдити(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
