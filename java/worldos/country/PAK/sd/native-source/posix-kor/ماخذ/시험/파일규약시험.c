#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int حالت, int لڪير) {
    검사항목수++;
    if (!حالت) {
        puts("POSIX CHECK FAILED");
        char ڊجٽ_قدر[12]; int لمبائي_قدر = 0;
        do { ڊجٽ_قدر[لمبائي_قدر++] = '0' + لڪير % 10; لڪير /= 10; } while (لڪير);
        while (لمبائي_قدر) putchar(ڊجٽ_قدر[--لمبائي_قدر]);
        putchar('\n'); _exit(1);
    }
}
#define تصديق_ڪريو(حالت) 검사((حالت), __LINE__)

int main(int 인수개수, char **دليل_فهرست) {
    char ڪوائف[32]; struct stat حالت_قدر;
    تصديق_ڪريو(인수개수 == 2 && strcmp(دليل_فهرست[1], "check") == 0 && دليل_فهرست[2] == 0);
    تصديق_ڪريو(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    تصديق_ڪريو(ٺاھيو_فائل("absent", صرف_مطالعو_قدر) == -1 && 오류번호 == ENOENT);
    int فائل = ٺاھيو_فائل("/posix.txt", پڙهڻ_لکڻ | 새파일만들기, 0640);
    تصديق_ڪريو(فائل == 3);
    تصديق_ڪريو(لکو_فائل_ڪوائف(فائل, "abcd", 4) == 4);
    تصديق_ڪريو(ٺاھيو_فائل("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    تصديق_ڪريو(파일상태읽기(فائل, &حالت_قدر) == 0 && حالت_قدر.st_size == 4 && S_ISREG(حالت_قدر.st_mode));
    تصديق_ڪريو((حالت_قدر.st_mode & 0777) == 0640 && حالت_قدر.st_nlink == 1);
    تصديق_ڪريو(ڳولا_فائل(فائل, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(فائل);
    تصديق_ڪريو(복제 == 4);
    تصديق_ڪريو(파일자료읽기(복제, ڪوائف, 2) == 2 && memcmp(ڪوائف, "ab", 2) == 0);
    تصديق_ڪريو(파일자료읽기(فائل, ڪوائف, 2) == 2 && memcmp(ڪوائف, "cd", 2) == 0);
    تصديق_ڪريو(파일자료읽기(فائل, ڪوائف, 1) == 0);
    تصديق_ڪريو(fcntl(فائل, F_SETFD, FD_CLOEXEC) == 0 && fcntl(فائل, F_GETFD) == 1);
    تصديق_ڪريو(fcntl(복제, F_GETFD) == 0);
    تصديق_ڪريو(dup2(فائل, فائل) == فائل && fcntl(فائل, F_GETFD) == 1);
    تصديق_ڪريو(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    تصديق_ڪريو(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(فائل, F_GETFL) & O_APPEND));
    تصديق_ڪريو(lseek(فائل, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(فائل, 0, SEEK_CUR) == 5);
    تصديق_ڪريو(fcntl(فائل, F_SETFL, 0) == 0);
    تصديق_ڪريو(lseek(فائل, 8, SEEK_SET) == 8 && write(فائل, "Z", 1) == 1);
    تصديق_ڪريو(lseek(복제, 5, SEEK_SET) == 5 && read(فائل, ڪوائف, 4) == 4);
    تصديق_ڪريو(ڪوائف[0] == 0 && ڪوائف[1] == 0 && ڪوائف[2] == 0 && ڪوائف[3] == 'Z');
    تصديق_ڪريو(ftruncate(فائل, 2) == 0 && lseek(فائل, 0, SEEK_CUR) == 9);
    تصديق_ڪريو(ftruncate(فائل, 6) == 0 && lseek(فائل, 2, SEEK_SET) == 2 && read(فائل, ڪوائف, 4) == 4);
    تصديق_ڪريو(!ڪوائف[0] && !ڪوائف[1] && !ڪوائف[2] && !ڪوائف[3]);
    تصديق_ڪريو(lseek(فائل, 2147483647, SEEK_SET) == 2147483647);
    تصديق_ڪريو(lseek(فائل, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    تصديق_ڪريو(lseek(فائل, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    تصديق_ڪريو(write(فائل, "!", 1) == -1 && errno == EFBIG);
    تصديق_ڪريو(lseek(فائل, 0, SEEK_SET) == 0);
    تصديق_ڪريو(read(فائل, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تصديق_ڪريو(read(فائل, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    تصديق_ڪريو(write(فائل, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تصديق_ڪريو(read(فائل, ڪوائف, (size_t)-1) == -1 && errno == EINVAL);
    تصديق_ڪريو(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    تصديق_ڪريو(fstat(فائل, (void *)0x00100000) == -1 && errno == EFAULT);
    تصديق_ڪريو(lseek(فائل, 0, SEEK_CUR) == 0);
    تصديق_ڪريو(read(فائل, NULL, 0) == 0 && write(فائل, NULL, 0) == 0);
    تصديق_ڪريو(هٽايو_فائل_داخلا_نالو("posix.txt") == 0);
    تصديق_ڪريو(fstat(فائل, &حالت_قدر) == 0 && حالت_قدر.st_nlink == 0 && حالت_قدر.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    تصديق_ڪريو(새파일 == 5 && fstat(새파일, &حالت_قدر) == 0 && حالت_قدر.st_size == 0);
    تصديق_ڪريو(read(فائل, ڪوائف, 2) == 2 && memcmp(ڪوائف, "ab", 2) == 0);
    تصديق_ڪريو(close(فائل) == 0 && close(복제) == 0 && close(새파일) == 0);
    تصديق_ڪريو(close(새파일) == -1 && errno == EBADF);
    تصديق_ڪريو(unlink("posix.txt") == 0);
    فائل = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    تصديق_ڪريو(فائل == 3 && fcntl(فائل, F_GETFD) == 1);
    تصديق_ڪريو(read(فائل, ڪوائف, 1) == -1 && errno == EBADF);
    تصديق_ڪريو(write(فائل, "keep", 4) == 4);
    for (int ابتدائي = 4; ابتدائي < 32; ابتدائي++) تصديق_ڪريو(dup(فائل) == ابتدائي);
    تصديق_ڪريو(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    تصديق_ڪريو(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    تصديق_ڪريو(fstat(فائل, &حالت_قدر) == 0 && حالت_قدر.st_size == 4);
    for (int ابتدائي = 3; ابتدائي < 32; ابتدائي++) تصديق_ڪريو(close(ابتدائي) == 0);
    تصديق_ڪريو(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    فائل = open("posix.txt", O_RDONLY);
    تصديق_ڪريو(فائل == 3 && write(فائل, ڪوائف, 1) == -1 && errno == EBADF);
    تصديق_ڪريو(fcntl(فائل, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    تصديق_ڪريو(close(8) == 0 && close(فائل) == 0 && unlink("posix.txt") == 0);
    تصديق_ڪريو(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    تصديق_ڪريو(fstat(1, &حالت_قدر) == 0 && S_ISCHR(حالت_قدر.st_mode));
    تصديق_ڪريو(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    تصديق_ڪريو(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr پتو; char پتو_متن[16];
    تصديق_ڪريو(inet_pton(AF_INET, "10.0.2.2", &پتو) == 1 && ntohl(پتو.s_addr) == 0x0a000202U);
    تصديق_ڪريو(inet_ntop(AF_INET, &پتو, پتو_متن, sizeof پتو_متن) == پتو_متن && strcmp(پتو_متن, "10.0.2.2") == 0);
    تصديق_ڪريو(inet_pton(AF_INET, "256.0.0.1", &پتو) == 0 && ntohl(پتو.s_addr) == 0x0a000202U);
    تصديق_ڪريو(inet_pton(AF_INET, "01.0.0.1", &پتو) == 0);
    تصديق_ڪريو(inet_ntop(AF_INET, &پتو, پتو_متن, 3) == NULL && errno == ENOSPC);
    تصديق_ڪريو(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char نالو[] = "slot0";
    for (int ابتدائي = 0; ابتدائي < 8; ابتدائي++) {
        نالو[4] = '0' + ابتدائي;
        int 열린파일 = open(نالو, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { تصديق_ڪريو(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    تصديق_ڪريو(개수 > 0 && 개수 < 8);
    تصديق_ڪريو(unlink("slot0") == 0);
    تصديق_ڪريو(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    تصديق_ڪريو(close(보관[0]) == 0);
    فائل = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    تصديق_ڪريو(فائل >= 0 && close(فائل) == 0 && unlink("held-slot") == 0);
    for (int ابتدائي = 1; ابتدائي < 개수; ابتدائي++) {
        نالو[4] = '0' + ابتدائي;
        تصديق_ڪريو(close(보관[ابتدائي]) == 0 && unlink(نالو) == 0);
    }
    تصديق_ڪريو(fsync(-1) == -1 && errno == EBADF);
    تصديق_ڪريو(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
