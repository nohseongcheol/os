#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int آړ, int ليکه) {
    검사항목수++;
    if (!آړ) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int اوږدوالى_ارزښت = 0;
        do { 숫자[اوږدوالى_ارزښت++] = '0' + ليکه % 10; ليکه /= 10; } while (ليکه);
        while (اوږدوالى_ارزښت) putchar(숫자[--اوږدوالى_ارزښت]);
        putchar('\n'); _exit(1);
    }
}
#define 확인(آړ) 검사((آړ), __LINE__)

int main(int 인수개수, char **인수목록) {
    char اومتوک[32]; struct stat انکړ_ارزښت;
    확인(인수개수 == 2 && strcmp(인수목록[1], "check") == 0 && 인수목록[2] == 0);
    확인(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    확인(파일열기("absent", 읽기전용) == -1 && 오류번호 == ENOENT);
    int دوتنه = 파일열기("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    확인(دوتنه == 3);
    확인(ليکل_دوتنه_اومتوک(دوتنه, "abcd", 4) == 4);
    확인(파일열기("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    확인(파일상태읽기(دوتنه, &انکړ_ارزښت) == 0 && انکړ_ارزښت.st_size == 4 && S_ISREG(انکړ_ارزښت.st_mode));
    확인((انکړ_ارزښت.st_mode & 0777) == 0640 && انکړ_ارزښت.st_nlink == 1);
    확인(파일위치옮기기(دوتنه, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(دوتنه);
    확인(복제 == 4);
    확인(파일자료읽기(복제, اومتوک, 2) == 2 && memcmp(اومتوک, "ab", 2) == 0);
    확인(파일자료읽기(دوتنه, اومتوک, 2) == 2 && memcmp(اومتوک, "cd", 2) == 0);
    확인(파일자료읽기(دوتنه, اومتوک, 1) == 0);
    확인(fcntl(دوتنه, F_SETFD, FD_CLOEXEC) == 0 && fcntl(دوتنه, F_GETFD) == 1);
    확인(fcntl(복제, F_GETFD) == 0);
    확인(dup2(دوتنه, دوتنه) == دوتنه && fcntl(دوتنه, F_GETFD) == 1);
    확인(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    확인(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(دوتنه, F_GETFL) & O_APPEND));
    확인(lseek(دوتنه, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(دوتنه, 0, SEEK_CUR) == 5);
    확인(fcntl(دوتنه, F_SETFL, 0) == 0);
    확인(lseek(دوتنه, 8, SEEK_SET) == 8 && write(دوتنه, "Z", 1) == 1);
    확인(lseek(복제, 5, SEEK_SET) == 5 && read(دوتنه, اومتوک, 4) == 4);
    확인(اومتوک[0] == 0 && اومتوک[1] == 0 && اومتوک[2] == 0 && اومتوک[3] == 'Z');
    확인(ftruncate(دوتنه, 2) == 0 && lseek(دوتنه, 0, SEEK_CUR) == 9);
    확인(ftruncate(دوتنه, 6) == 0 && lseek(دوتنه, 2, SEEK_SET) == 2 && read(دوتنه, اومتوک, 4) == 4);
    확인(!اومتوک[0] && !اومتوک[1] && !اومتوک[2] && !اومتوک[3]);
    확인(lseek(دوتنه, 2147483647, SEEK_SET) == 2147483647);
    확인(lseek(دوتنه, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    확인(lseek(دوتنه, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    확인(write(دوتنه, "!", 1) == -1 && errno == EFBIG);
    확인(lseek(دوتنه, 0, SEEK_SET) == 0);
    확인(read(دوتنه, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(دوتنه, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    확인(write(دوتنه, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(دوتنه, اومتوک, (size_t)-1) == -1 && errno == EINVAL);
    확인(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    확인(fstat(دوتنه, (void *)0x00100000) == -1 && errno == EFAULT);
    확인(lseek(دوتنه, 0, SEEK_CUR) == 0);
    확인(read(دوتنه, NULL, 0) == 0 && write(دوتنه, NULL, 0) == 0);
    확인(파일이름지우기("posix.txt") == 0);
    확인(fstat(دوتنه, &انکړ_ارزښت) == 0 && انکړ_ارزښت.st_nlink == 0 && انکړ_ارزښت.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(새파일 == 5 && fstat(새파일, &انکړ_ارزښت) == 0 && انکړ_ارزښت.st_size == 0);
    확인(read(دوتنه, اومتوک, 2) == 2 && memcmp(اومتوک, "ab", 2) == 0);
    확인(close(دوتنه) == 0 && close(복제) == 0 && close(새파일) == 0);
    확인(close(새파일) == -1 && errno == EBADF);
    확인(unlink("posix.txt") == 0);
    دوتنه = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    확인(دوتنه == 3 && fcntl(دوتنه, F_GETFD) == 1);
    확인(read(دوتنه, اومتوک, 1) == -1 && errno == EBADF);
    확인(write(دوتنه, "keep", 4) == 4);
    for (int لړیال = 4; لړیال < 32; لړیال++) 확인(dup(دوتنه) == لړیال);
    확인(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    확인(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    확인(fstat(دوتنه, &انکړ_ارزښت) == 0 && انکړ_ارزښت.st_size == 4);
    for (int لړیال = 3; لړیال < 32; لړیال++) 확인(close(لړیال) == 0);
    확인(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    دوتنه = open("posix.txt", O_RDONLY);
    확인(دوتنه == 3 && write(دوتنه, اومتوک, 1) == -1 && errno == EBADF);
    확인(fcntl(دوتنه, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    확인(close(8) == 0 && close(دوتنه) == 0 && unlink("posix.txt") == 0);
    확인(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    확인(fstat(1, &انکړ_ارزښت) == 0 && S_ISCHR(انکړ_ارزښت.st_mode));
    확인(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    확인(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr پته; char 주소글[16];
    확인(inet_pton(AF_INET, "10.0.2.2", &پته) == 1 && ntohl(پته.s_addr) == 0x0a000202U);
    확인(inet_ntop(AF_INET, &پته, 주소글, sizeof 주소글) == 주소글 && strcmp(주소글, "10.0.2.2") == 0);
    확인(inet_pton(AF_INET, "256.0.0.1", &پته) == 0 && ntohl(پته.s_addr) == 0x0a000202U);
    확인(inet_pton(AF_INET, "01.0.0.1", &پته) == 0);
    확인(inet_ntop(AF_INET, &پته, 주소글, 3) == NULL && errno == ENOSPC);
    확인(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char نوم[] = "slot0";
    for (int لړیال = 0; لړیال < 8; لړیال++) {
        نوم[4] = '0' + لړیال;
        int 열린파일 = open(نوم, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { 확인(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    확인(개수 > 0 && 개수 < 8);
    확인(unlink("slot0") == 0);
    확인(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    확인(close(보관[0]) == 0);
    دوتنه = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(دوتنه >= 0 && close(دوتنه) == 0 && unlink("held-slot") == 0);
    for (int لړیال = 1; لړیال < 개수; لړیال++) {
        نوم[4] = '0' + لړیال;
        확인(close(보관[لړیال]) == 0 && unlink(نوم) == 0);
    }
    확인(fsync(-1) == -1 && errno == EBADF);
    확인(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
