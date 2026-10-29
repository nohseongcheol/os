#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int 조건, int 줄) {
    검사항목수++;
    if (!조건) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int 길이 = 0;
        do { 숫자[길이++] = '0' + 줄 % 10; 줄 /= 10; } while (줄);
        while (길이) putchar(숫자[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define 확인(조건) 검사((조건), __LINE__)

int main(int 인수개수, char **인수목록) {
    char 자료[32]; struct stat 상태;
    확인(인수개수 == 2 && strcmp(인수목록[1], "check") == 0 && 인수목록[2] == 0);
    확인(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    확인(파일열기("absent", 읽기전용) == -1 && 오류번호 == ENOENT);
    int טעקע = 파일열기("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    확인(טעקע == 3);
    확인(파일자료쓰기(טעקע, "abcd", 4) == 4);
    확인(파일열기("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    확인(파일상태읽기(טעקע, &상태) == 0 && 상태.st_size == 4 && S_ISREG(상태.st_mode));
    확인((상태.st_mode & 0777) == 0640 && 상태.st_nlink == 1);
    확인(파일위치옮기기(טעקע, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(טעקע);
    확인(복제 == 4);
    확인(파일자료읽기(복제, 자료, 2) == 2 && memcmp(자료, "ab", 2) == 0);
    확인(파일자료읽기(טעקע, 자료, 2) == 2 && memcmp(자료, "cd", 2) == 0);
    확인(파일자료읽기(טעקע, 자료, 1) == 0);
    확인(fcntl(טעקע, F_SETFD, FD_CLOEXEC) == 0 && fcntl(טעקע, F_GETFD) == 1);
    확인(fcntl(복제, F_GETFD) == 0);
    확인(dup2(טעקע, טעקע) == טעקע && fcntl(טעקע, F_GETFD) == 1);
    확인(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    확인(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(טעקע, F_GETFL) & O_APPEND));
    확인(lseek(טעקע, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(טעקע, 0, SEEK_CUR) == 5);
    확인(fcntl(טעקע, F_SETFL, 0) == 0);
    확인(lseek(טעקע, 8, SEEK_SET) == 8 && write(טעקע, "Z", 1) == 1);
    확인(lseek(복제, 5, SEEK_SET) == 5 && read(טעקע, 자료, 4) == 4);
    확인(자료[0] == 0 && 자료[1] == 0 && 자료[2] == 0 && 자료[3] == 'Z');
    확인(ftruncate(טעקע, 2) == 0 && lseek(טעקע, 0, SEEK_CUR) == 9);
    확인(ftruncate(טעקע, 6) == 0 && lseek(טעקע, 2, SEEK_SET) == 2 && read(טעקע, 자료, 4) == 4);
    확인(!자료[0] && !자료[1] && !자료[2] && !자료[3]);
    확인(lseek(טעקע, 2147483647, SEEK_SET) == 2147483647);
    확인(lseek(טעקע, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    확인(lseek(טעקע, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    확인(write(טעקע, "!", 1) == -1 && errno == EFBIG);
    확인(lseek(טעקע, 0, SEEK_SET) == 0);
    확인(read(טעקע, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(טעקע, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    확인(write(טעקע, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(טעקע, 자료, (size_t)-1) == -1 && errno == EINVAL);
    확인(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    확인(fstat(טעקע, (void *)0x00100000) == -1 && errno == EFAULT);
    확인(lseek(טעקע, 0, SEEK_CUR) == 0);
    확인(read(טעקע, NULL, 0) == 0 && write(טעקע, NULL, 0) == 0);
    확인(파일이름지우기("posix.txt") == 0);
    확인(fstat(טעקע, &상태) == 0 && 상태.st_nlink == 0 && 상태.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(새파일 == 5 && fstat(새파일, &상태) == 0 && 상태.st_size == 0);
    확인(read(טעקע, 자료, 2) == 2 && memcmp(자료, "ab", 2) == 0);
    확인(close(טעקע) == 0 && close(복제) == 0 && close(새파일) == 0);
    확인(close(새파일) == -1 && errno == EBADF);
    확인(unlink("posix.txt") == 0);
    טעקע = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    확인(טעקע == 3 && fcntl(טעקע, F_GETFD) == 1);
    확인(read(טעקע, 자료, 1) == -1 && errno == EBADF);
    확인(write(טעקע, "keep", 4) == 4);
    for (int 번호 = 4; 번호 < 32; 번호++) 확인(dup(טעקע) == 번호);
    확인(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    확인(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    확인(fstat(טעקע, &상태) == 0 && 상태.st_size == 4);
    for (int 번호 = 3; 번호 < 32; 번호++) 확인(close(번호) == 0);
    확인(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    טעקע = open("posix.txt", O_RDONLY);
    확인(טעקע == 3 && write(טעקע, 자료, 1) == -1 && errno == EBADF);
    확인(fcntl(טעקע, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    확인(close(8) == 0 && close(טעקע) == 0 && unlink("posix.txt") == 0);
    확인(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    확인(fstat(1, &상태) == 0 && S_ISCHR(상태.st_mode));
    확인(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    확인(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr 주소; char 주소글[16];
    확인(inet_pton(AF_INET, "10.0.2.2", &주소) == 1 && ntohl(주소.s_addr) == 0x0a000202U);
    확인(inet_ntop(AF_INET, &주소, 주소글, sizeof 주소글) == 주소글 && strcmp(주소글, "10.0.2.2") == 0);
    확인(inet_pton(AF_INET, "256.0.0.1", &주소) == 0 && ntohl(주소.s_addr) == 0x0a000202U);
    확인(inet_pton(AF_INET, "01.0.0.1", &주소) == 0);
    확인(inet_ntop(AF_INET, &주소, 주소글, 3) == NULL && errno == ENOSPC);
    확인(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char נאָמען[] = "slot0";
    for (int 번호 = 0; 번호 < 8; 번호++) {
        נאָמען[4] = '0' + 번호;
        int 열린파일 = open(נאָמען, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { 확인(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    확인(개수 > 0 && 개수 < 8);
    확인(unlink("slot0") == 0);
    확인(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    확인(close(보관[0]) == 0);
    טעקע = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(טעקע >= 0 && close(טעקע) == 0 && unlink("held-slot") == 0);
    for (int 번호 = 1; 번호 < 개수; 번호++) {
        נאָמען[4] = '0' + 번호;
        확인(close(보관[번호]) == 0 && unlink(נאָמען) == 0);
    }
    확인(fsync(-1) == -1 && errno == EBADF);
    확인(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
