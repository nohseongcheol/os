#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int حالت, int لائن) {
    검사항목수++;
    if (!حالت) {
        puts("POSIX CHECK FAILED");
        char عدد_قدر[12]; int لمبائی_قدر = 0;
        do { عدد_قدر[لمبائی_قدر++] = '0' + لائن % 10; لائن /= 10; } while (لائن);
        while (لمبائی_قدر) putchar(عدد_قدر[--لمبائی_قدر]);
        putchar('\n'); _exit(1);
    }
}
#define تصدیق_کرو(حالت) 검사((حالت), __LINE__)

int main(int 인수개수, char **دلیل_فرست) {
    char کوائف[32]; struct stat حالت_قدر;
    تصدیق_کرو(인수개수 == 2 && strcmp(دلیل_فرست[1], "check") == 0 && دلیل_فرست[2] == 0);
    تصدیق_کرو(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    تصدیق_کرو(بنڑاؤ_فائل("absent", صرف_مطالعہ_قدر) == -1 && 오류번호 == ENOENT);
    int فائل = بنڑاؤ_فائل("/posix.txt", پڑھو_لکھو | 새파일만들기, 0640);
    تصدیق_کرو(فائل == 3);
    تصدیق_کرو(لکھو_فائل_کوائف(فائل, "abcd", 4) == 4);
    تصدیق_کرو(بنڑاؤ_فائل("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    تصدیق_کرو(파일상태읽기(فائل, &حالت_قدر) == 0 && حالت_قدر.st_size == 4 && S_ISREG(حالت_قدر.st_mode));
    تصدیق_کرو((حالت_قدر.st_mode & 0777) == 0640 && حالت_قدر.st_nlink == 1);
    تصدیق_کرو(تلاش_کرو_فائل(فائل, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(فائل);
    تصدیق_کرو(복제 == 4);
    تصدیق_کرو(파일자료읽기(복제, کوائف, 2) == 2 && memcmp(کوائف, "ab", 2) == 0);
    تصدیق_کرو(파일자료읽기(فائل, کوائف, 2) == 2 && memcmp(کوائف, "cd", 2) == 0);
    تصدیق_کرو(파일자료읽기(فائل, کوائف, 1) == 0);
    تصدیق_کرو(fcntl(فائل, F_SETFD, FD_CLOEXEC) == 0 && fcntl(فائل, F_GETFD) == 1);
    تصدیق_کرو(fcntl(복제, F_GETFD) == 0);
    تصدیق_کرو(dup2(فائل, فائل) == فائل && fcntl(فائل, F_GETFD) == 1);
    تصدیق_کرو(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    تصدیق_کرو(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(فائل, F_GETFL) & O_APPEND));
    تصدیق_کرو(lseek(فائل, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(فائل, 0, SEEK_CUR) == 5);
    تصدیق_کرو(fcntl(فائل, F_SETFL, 0) == 0);
    تصدیق_کرو(lseek(فائل, 8, SEEK_SET) == 8 && write(فائل, "Z", 1) == 1);
    تصدیق_کرو(lseek(복제, 5, SEEK_SET) == 5 && read(فائل, کوائف, 4) == 4);
    تصدیق_کرو(کوائف[0] == 0 && کوائف[1] == 0 && کوائف[2] == 0 && کوائف[3] == 'Z');
    تصدیق_کرو(ftruncate(فائل, 2) == 0 && lseek(فائل, 0, SEEK_CUR) == 9);
    تصدیق_کرو(ftruncate(فائل, 6) == 0 && lseek(فائل, 2, SEEK_SET) == 2 && read(فائل, کوائف, 4) == 4);
    تصدیق_کرو(!کوائف[0] && !کوائف[1] && !کوائف[2] && !کوائف[3]);
    تصدیق_کرو(lseek(فائل, 2147483647, SEEK_SET) == 2147483647);
    تصدیق_کرو(lseek(فائل, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    تصدیق_کرو(lseek(فائل, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    تصدیق_کرو(write(فائل, "!", 1) == -1 && errno == EFBIG);
    تصدیق_کرو(lseek(فائل, 0, SEEK_SET) == 0);
    تصدیق_کرو(read(فائل, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تصدیق_کرو(read(فائل, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    تصدیق_کرو(write(فائل, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تصدیق_کرو(read(فائل, کوائف, (size_t)-1) == -1 && errno == EINVAL);
    تصدیق_کرو(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    تصدیق_کرو(fstat(فائل, (void *)0x00100000) == -1 && errno == EFAULT);
    تصدیق_کرو(lseek(فائل, 0, SEEK_CUR) == 0);
    تصدیق_کرو(read(فائل, NULL, 0) == 0 && write(فائل, NULL, 0) == 0);
    تصدیق_کرو(ہٹاؤ_فائل_داخلہ_ناں("posix.txt") == 0);
    تصدیق_کرو(fstat(فائل, &حالت_قدر) == 0 && حالت_قدر.st_nlink == 0 && حالت_قدر.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    تصدیق_کرو(새파일 == 5 && fstat(새파일, &حالت_قدر) == 0 && حالت_قدر.st_size == 0);
    تصدیق_کرو(read(فائل, کوائف, 2) == 2 && memcmp(کوائف, "ab", 2) == 0);
    تصدیق_کرو(close(فائل) == 0 && close(복제) == 0 && close(새파일) == 0);
    تصدیق_کرو(close(새파일) == -1 && errno == EBADF);
    تصدیق_کرو(unlink("posix.txt") == 0);
    فائل = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    تصدیق_کرو(فائل == 3 && fcntl(فائل, F_GETFD) == 1);
    تصدیق_کرو(read(فائل, کوائف, 1) == -1 && errno == EBADF);
    تصدیق_کرو(write(فائل, "keep", 4) == 4);
    for (int اشاریہ = 4; اشاریہ < 32; اشاریہ++) تصدیق_کرو(dup(فائل) == اشاریہ);
    تصدیق_کرو(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    تصدیق_کرو(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    تصدیق_کرو(fstat(فائل, &حالت_قدر) == 0 && حالت_قدر.st_size == 4);
    for (int اشاریہ = 3; اشاریہ < 32; اشاریہ++) تصدیق_کرو(close(اشاریہ) == 0);
    تصدیق_کرو(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    فائل = open("posix.txt", O_RDONLY);
    تصدیق_کرو(فائل == 3 && write(فائل, کوائف, 1) == -1 && errno == EBADF);
    تصدیق_کرو(fcntl(فائل, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    تصدیق_کرو(close(8) == 0 && close(فائل) == 0 && unlink("posix.txt") == 0);
    تصدیق_کرو(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    تصدیق_کرو(fstat(1, &حالت_قدر) == 0 && S_ISCHR(حالت_قدر.st_mode));
    تصدیق_کرو(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    تصدیق_کرو(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr پتا; char پتا_متن[16];
    تصدیق_کرو(inet_pton(AF_INET, "10.0.2.2", &پتا) == 1 && ntohl(پتا.s_addr) == 0x0a000202U);
    تصدیق_کرو(inet_ntop(AF_INET, &پتا, پتا_متن, sizeof پتا_متن) == پتا_متن && strcmp(پتا_متن, "10.0.2.2") == 0);
    تصدیق_کرو(inet_pton(AF_INET, "256.0.0.1", &پتا) == 0 && ntohl(پتا.s_addr) == 0x0a000202U);
    تصدیق_کرو(inet_pton(AF_INET, "01.0.0.1", &پتا) == 0);
    تصدیق_کرو(inet_ntop(AF_INET, &پتا, پتا_متن, 3) == NULL && errno == ENOSPC);
    تصدیق_کرو(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ناں[] = "slot0";
    for (int اشاریہ = 0; اشاریہ < 8; اشاریہ++) {
        ناں[4] = '0' + اشاریہ;
        int 열린파일 = open(ناں, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { تصدیق_کرو(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    تصدیق_کرو(개수 > 0 && 개수 < 8);
    تصدیق_کرو(unlink("slot0") == 0);
    تصدیق_کرو(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    تصدیق_کرو(close(보관[0]) == 0);
    فائل = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    تصدیق_کرو(فائل >= 0 && close(فائل) == 0 && unlink("held-slot") == 0);
    for (int اشاریہ = 1; اشاریہ < 개수; اشاریہ++) {
        ناں[4] = '0' + اشاریہ;
        تصدیق_کرو(close(보관[اشاریہ]) == 0 && unlink(ناں) == 0);
    }
    تصدیق_کرو(fsync(-1) == -1 && errno == EBADF);
    تصدیق_کرو(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
