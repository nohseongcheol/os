#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int شرط, int سطر) {
    검사항목수++;
    if (!شرط) {
        puts("POSIX CHECK FAILED");
        char رقم_قيمة[12]; int 길이 = 0;
        do { رقم_قيمة[길이++] = '0' + سطر % 10; سطر /= 10; } while (سطر);
        while (길이) putchar(رقم_قيمة[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define يتحقق(شرط) 검사((شرط), __LINE__)

int main(int 인수개수, char **وسيطة_قائمة) {
    char بيانات[32]; struct stat حالة_قيمة;
    يتحقق(인수개수 == 2 && strcmp(وسيطة_قائمة[1], "check") == 0 && وسيطة_قائمة[2] == 0);
    يتحقق(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    يتحقق(فتح_ملف("absent", للقراءة_فقط_قيمة) == -1 && رقم_الخطأ == ENOENT);
    int ملف = فتح_ملف("/posix.txt", مقروء_مكتوب | 새파일만들기, 0640);
    يتحقق(ملف == 3);
    يتحقق(كتابة_ملف_بيانات(ملف, "abcd", 4) == 4);
    يتحقق(فتح_ملف("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    يتحقق(يقرأ_ملف_توفر(ملف, &حالة_قيمة) == 0 && حالة_قيمة.st_size == 4 && S_ISREG(حالة_قيمة.st_mode));
    يتحقق((حالة_قيمة.st_mode & 0777) == 0640 && حالة_قيمة.st_nlink == 1);
    يتحقق(يبحث_ملف(ملف, 0, 처음기준) == 0);
    int نسخة_قيمة = 파일서술자복제(ملف);
    يتحقق(نسخة_قيمة == 4);
    يتحقق(يقرأ_ملف_بيانات(نسخة_قيمة, بيانات, 2) == 2 && memcmp(بيانات, "ab", 2) == 0);
    يتحقق(يقرأ_ملف_بيانات(ملف, بيانات, 2) == 2 && memcmp(بيانات, "cd", 2) == 0);
    يتحقق(يقرأ_ملف_بيانات(ملف, بيانات, 1) == 0);
    يتحقق(fcntl(ملف, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ملف, F_GETFD) == 1);
    يتحقق(fcntl(نسخة_قيمة, F_GETFD) == 0);
    يتحقق(dup2(ملف, ملف) == ملف && fcntl(ملف, F_GETFD) == 1);
    يتحقق(dup2(-1, نسخة_قيمة) == -1 && errno == EBADF && fcntl(نسخة_قيمة, F_GETFD) == 0);
    يتحقق(fcntl(نسخة_قيمة, F_SETFL, O_APPEND) == 0 && (fcntl(ملف, F_GETFL) & O_APPEND));
    يتحقق(lseek(ملف, 0, SEEK_SET) == 0 && write(نسخة_قيمة, "e", 1) == 1 && lseek(ملف, 0, SEEK_CUR) == 5);
    يتحقق(fcntl(ملف, F_SETFL, 0) == 0);
    يتحقق(lseek(ملف, 8, SEEK_SET) == 8 && write(ملف, "Z", 1) == 1);
    يتحقق(lseek(نسخة_قيمة, 5, SEEK_SET) == 5 && read(ملف, بيانات, 4) == 4);
    يتحقق(بيانات[0] == 0 && بيانات[1] == 0 && بيانات[2] == 0 && بيانات[3] == 'Z');
    يتحقق(ftruncate(ملف, 2) == 0 && lseek(ملف, 0, SEEK_CUR) == 9);
    يتحقق(ftruncate(ملف, 6) == 0 && lseek(ملف, 2, SEEK_SET) == 2 && read(ملف, بيانات, 4) == 4);
    يتحقق(!بيانات[0] && !بيانات[1] && !بيانات[2] && !بيانات[3]);
    يتحقق(lseek(ملف, 2147483647, SEEK_SET) == 2147483647);
    يتحقق(lseek(ملف, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    يتحقق(lseek(ملف, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    يتحقق(write(ملف, "!", 1) == -1 && errno == EFBIG);
    يتحقق(lseek(ملف, 0, SEEK_SET) == 0);
    يتحقق(read(ملف, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    يتحقق(read(ملف, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    يتحقق(write(ملف, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    يتحقق(read(ملف, بيانات, (size_t)-1) == -1 && errno == EINVAL);
    يتحقق(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    يتحقق(fstat(ملف, (void *)0x00100000) == -1 && errno == EFAULT);
    يتحقق(lseek(ملف, 0, SEEK_CUR) == 0);
    يتحقق(read(ملف, NULL, 0) == 0 && write(ملف, NULL, 0) == 0);
    يتحقق(يزيل_ملف_إدخال_اسم("posix.txt") == 0);
    يتحقق(fstat(ملف, &حالة_قيمة) == 0 && حالة_قيمة.st_nlink == 0 && حالة_قيمة.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    يتحقق(새파일 == 5 && fstat(새파일, &حالة_قيمة) == 0 && حالة_قيمة.st_size == 0);
    يتحقق(read(ملف, بيانات, 2) == 2 && memcmp(بيانات, "ab", 2) == 0);
    يتحقق(close(ملف) == 0 && close(نسخة_قيمة) == 0 && close(새파일) == 0);
    يتحقق(close(새파일) == -1 && errno == EBADF);
    يتحقق(unlink("posix.txt") == 0);
    ملف = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    يتحقق(ملف == 3 && fcntl(ملف, F_GETFD) == 1);
    يتحقق(read(ملف, بيانات, 1) == -1 && errno == EBADF);
    يتحقق(write(ملف, "keep", 4) == 4);
    for (int فهرس = 4; فهرس < 32; فهرس++) يتحقق(dup(ملف) == فهرس);
    يتحقق(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    يتحقق(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    يتحقق(fstat(ملف, &حالة_قيمة) == 0 && حالة_قيمة.st_size == 4);
    for (int فهرس = 3; فهرس < 32; فهرس++) يتحقق(close(فهرس) == 0);
    يتحقق(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ملف = open("posix.txt", O_RDONLY);
    يتحقق(ملف == 3 && write(ملف, بيانات, 1) == -1 && errno == EBADF);
    يتحقق(fcntl(ملف, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    يتحقق(close(8) == 0 && close(ملف) == 0 && unlink("posix.txt") == 0);
    يتحقق(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    يتحقق(fstat(1, &حالة_قيمة) == 0 && S_ISCHR(حالة_قيمة.st_mode));
    يتحقق(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    يتحقق(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr عنوان; char عنوان_نص[16];
    يتحقق(inet_pton(AF_INET, "10.0.2.2", &عنوان) == 1 && ntohl(عنوان.s_addr) == 0x0a000202U);
    يتحقق(inet_ntop(AF_INET, &عنوان, عنوان_نص, sizeof عنوان_نص) == عنوان_نص && strcmp(عنوان_نص, "10.0.2.2") == 0);
    يتحقق(inet_pton(AF_INET, "256.0.0.1", &عنوان) == 0 && ntohl(عنوان.s_addr) == 0x0a000202U);
    يتحقق(inet_pton(AF_INET, "01.0.0.1", &عنوان) == 0);
    يتحقق(inet_ntop(AF_INET, &عنوان, عنوان_نص, 3) == NULL && errno == ENOSPC);
    يتحقق(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char اسم[] = "slot0";
    for (int فهرس = 0; فهرس < 8; فهرس++) {
        اسم[4] = '0' + فهرس;
        int 열린파일 = open(اسم, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { يتحقق(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    يتحقق(개수 > 0 && 개수 < 8);
    يتحقق(unlink("slot0") == 0);
    يتحقق(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    يتحقق(close(보관[0]) == 0);
    ملف = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    يتحقق(ملف >= 0 && close(ملف) == 0 && unlink("held-slot") == 0);
    for (int فهرس = 1; فهرس < 개수; فهرس++) {
        اسم[4] = '0' + فهرس;
        يتحقق(close(보관[فهرس]) == 0 && unlink(اسم) == 0);
    }
    يتحقق(fsync(-1) == -1 && errno == EBADF);
    يتحقق(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
