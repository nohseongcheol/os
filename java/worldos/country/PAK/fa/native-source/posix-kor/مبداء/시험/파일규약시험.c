#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int شرط, int خط) {
    검사항목수++;
    if (!شرط) {
        puts("POSIX CHECK FAILED");
        char رقم_مقدار[12]; int طول_مقدار = 0;
        do { رقم_مقدار[طول_مقدار++] = '0' + خط % 10; خط /= 10; } while (خط);
        while (طول_مقدار) putchar(رقم_مقدار[--طول_مقدار]);
        putchar('\n'); _exit(1);
    }
}
#define تأیید_صحت(شرط) 검사((شرط), __LINE__)

int main(int 인수개수, char **آرگومان_لیست) {
    char داده_ها[32]; struct stat وضعیت_مقدار;
    تأیید_صحت(인수개수 == 2 && strcmp(آرگومان_لیست[1], "check") == 0 && آرگومان_لیست[2] == 0);
    تأیید_صحت(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    تأیید_صحت(ایجاد_فایل("absent", فقط_خواندنی_مقدار) == -1 && 오류번호 == ENOENT);
    int پرونده = ایجاد_فایل("/posix.txt", خواندن_نوشتن | 새파일만들기, 0640);
    تأیید_صحت(پرونده == 3);
    تأیید_صحت(نوشتن_فایل_داده_ها(پرونده, "abcd", 4) == 4);
    تأیید_صحت(ایجاد_فایل("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    تأیید_صحت(파일상태읽기(پرونده, &وضعیت_مقدار) == 0 && وضعیت_مقدار.st_size == 4 && S_ISREG(وضعیت_مقدار.st_mode));
    تأیید_صحت((وضعیت_مقدار.st_mode & 0777) == 0640 && وضعیت_مقدار.st_nlink == 1);
    تأیید_صحت(جستجو_کردن_فایل(پرونده, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(پرونده);
    تأیید_صحت(복제 == 4);
    تأیید_صحت(파일자료읽기(복제, داده_ها, 2) == 2 && memcmp(داده_ها, "ab", 2) == 0);
    تأیید_صحت(파일자료읽기(پرونده, داده_ها, 2) == 2 && memcmp(داده_ها, "cd", 2) == 0);
    تأیید_صحت(파일자료읽기(پرونده, داده_ها, 1) == 0);
    تأیید_صحت(fcntl(پرونده, F_SETFD, FD_CLOEXEC) == 0 && fcntl(پرونده, F_GETFD) == 1);
    تأیید_صحت(fcntl(복제, F_GETFD) == 0);
    تأیید_صحت(dup2(پرونده, پرونده) == پرونده && fcntl(پرونده, F_GETFD) == 1);
    تأیید_صحت(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    تأیید_صحت(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(پرونده, F_GETFL) & O_APPEND));
    تأیید_صحت(lseek(پرونده, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(پرونده, 0, SEEK_CUR) == 5);
    تأیید_صحت(fcntl(پرونده, F_SETFL, 0) == 0);
    تأیید_صحت(lseek(پرونده, 8, SEEK_SET) == 8 && write(پرونده, "Z", 1) == 1);
    تأیید_صحت(lseek(복제, 5, SEEK_SET) == 5 && read(پرونده, داده_ها, 4) == 4);
    تأیید_صحت(داده_ها[0] == 0 && داده_ها[1] == 0 && داده_ها[2] == 0 && داده_ها[3] == 'Z');
    تأیید_صحت(ftruncate(پرونده, 2) == 0 && lseek(پرونده, 0, SEEK_CUR) == 9);
    تأیید_صحت(ftruncate(پرونده, 6) == 0 && lseek(پرونده, 2, SEEK_SET) == 2 && read(پرونده, داده_ها, 4) == 4);
    تأیید_صحت(!داده_ها[0] && !داده_ها[1] && !داده_ها[2] && !داده_ها[3]);
    تأیید_صحت(lseek(پرونده, 2147483647, SEEK_SET) == 2147483647);
    تأیید_صحت(lseek(پرونده, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    تأیید_صحت(lseek(پرونده, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    تأیید_صحت(write(پرونده, "!", 1) == -1 && errno == EFBIG);
    تأیید_صحت(lseek(پرونده, 0, SEEK_SET) == 0);
    تأیید_صحت(read(پرونده, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تأیید_صحت(read(پرونده, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    تأیید_صحت(write(پرونده, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تأیید_صحت(read(پرونده, داده_ها, (size_t)-1) == -1 && errno == EINVAL);
    تأیید_صحت(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    تأیید_صحت(fstat(پرونده, (void *)0x00100000) == -1 && errno == EFAULT);
    تأیید_صحت(lseek(پرونده, 0, SEEK_CUR) == 0);
    تأیید_صحت(read(پرونده, NULL, 0) == 0 && write(پرونده, NULL, 0) == 0);
    تأیید_صحت(حذف_فایل_ورودی_نام("posix.txt") == 0);
    تأیید_صحت(fstat(پرونده, &وضعیت_مقدار) == 0 && وضعیت_مقدار.st_nlink == 0 && وضعیت_مقدار.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    تأیید_صحت(새파일 == 5 && fstat(새파일, &وضعیت_مقدار) == 0 && وضعیت_مقدار.st_size == 0);
    تأیید_صحت(read(پرونده, داده_ها, 2) == 2 && memcmp(داده_ها, "ab", 2) == 0);
    تأیید_صحت(close(پرونده) == 0 && close(복제) == 0 && close(새파일) == 0);
    تأیید_صحت(close(새파일) == -1 && errno == EBADF);
    تأیید_صحت(unlink("posix.txt") == 0);
    پرونده = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    تأیید_صحت(پرونده == 3 && fcntl(پرونده, F_GETFD) == 1);
    تأیید_صحت(read(پرونده, داده_ها, 1) == -1 && errno == EBADF);
    تأیید_صحت(write(پرونده, "keep", 4) == 4);
    for (int فهرست = 4; فهرست < 32; فهرست++) تأیید_صحت(dup(پرونده) == فهرست);
    تأیید_صحت(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    تأیید_صحت(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    تأیید_صحت(fstat(پرونده, &وضعیت_مقدار) == 0 && وضعیت_مقدار.st_size == 4);
    for (int فهرست = 3; فهرست < 32; فهرست++) تأیید_صحت(close(فهرست) == 0);
    تأیید_صحت(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    پرونده = open("posix.txt", O_RDONLY);
    تأیید_صحت(پرونده == 3 && write(پرونده, داده_ها, 1) == -1 && errno == EBADF);
    تأیید_صحت(fcntl(پرونده, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    تأیید_صحت(close(8) == 0 && close(پرونده) == 0 && unlink("posix.txt") == 0);
    تأیید_صحت(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    تأیید_صحت(fstat(1, &وضعیت_مقدار) == 0 && S_ISCHR(وضعیت_مقدار.st_mode));
    تأیید_صحت(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    تأیید_صحت(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr آدرس; char آدرس_متن[16];
    تأیید_صحت(inet_pton(AF_INET, "10.0.2.2", &آدرس) == 1 && ntohl(آدرس.s_addr) == 0x0a000202U);
    تأیید_صحت(inet_ntop(AF_INET, &آدرس, آدرس_متن, sizeof آدرس_متن) == آدرس_متن && strcmp(آدرس_متن, "10.0.2.2") == 0);
    تأیید_صحت(inet_pton(AF_INET, "256.0.0.1", &آدرس) == 0 && ntohl(آدرس.s_addr) == 0x0a000202U);
    تأیید_صحت(inet_pton(AF_INET, "01.0.0.1", &آدرس) == 0);
    تأیید_صحت(inet_ntop(AF_INET, &آدرس, آدرس_متن, 3) == NULL && errno == ENOSPC);
    تأیید_صحت(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char نام[] = "slot0";
    for (int فهرست = 0; فهرست < 8; فهرست++) {
        نام[4] = '0' + فهرست;
        int 열린파일 = open(نام, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { تأیید_صحت(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    تأیید_صحت(개수 > 0 && 개수 < 8);
    تأیید_صحت(unlink("slot0") == 0);
    تأیید_صحت(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    تأیید_صحت(close(보관[0]) == 0);
    پرونده = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    تأیید_صحت(پرونده >= 0 && close(پرونده) == 0 && unlink("held-slot") == 0);
    for (int فهرست = 1; فهرست < 개수; فهرست++) {
        نام[4] = '0' + فهرست;
        تأیید_صحت(close(보관[فهرست]) == 0 && unlink(نام) == 0);
    }
    تأیید_صحت(fsync(-1) == -1 && errno == EBADF);
    تأیید_صحت(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
