#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int شرط, int اندراج_کی_سطر) {
    검사항목수++;
    if (!شرط) {
        puts("POSIX CHECK FAILED");
        char عدد_قدر[12]; int لمبا_ئی_قدر = 0;
        do { عدد_قدر[لمبا_ئی_قدر++] = '0' + اندراج_کی_سطر % 10; اندراج_کی_سطر /= 10; } while (اندراج_کی_سطر);
        while (لمبا_ئی_قدر) putchar(عدد_قدر[--لمبا_ئی_قدر]);
        putchar('\n'); _exit(1);
    }
}
#define تصدیق_کریں(شرط) 검사((شرط), __LINE__)

int main(int 인수개수, char **دلائل_فہرست) {
    char کوائف[32]; struct stat حالت_قدر;
    تصدیق_کریں(인수개수 == 2 && strcmp(دلائل_فہرست[1], "check") == 0 && دلائل_فہرست[2] == 0);
    تصدیق_کریں(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    تصدیق_کریں(بنائیں_فائل("absent", فقط_مطالعہ_قدر) == -1 && 오류번호 == ENOENT);
    int فائل_کا_نام = بنائیں_فائل("/posix.txt", مطالعہ_تحریری | 새파일만들기, 0640);
    تصدیق_کریں(فائل_کا_نام == 3);
    تصدیق_کریں(لکھیں_فائل_کوائف(فائل_کا_نام, "abcd", 4) == 4);
    تصدیق_کریں(بنائیں_فائل("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    تصدیق_کریں(파일상태읽기(فائل_کا_نام, &حالت_قدر) == 0 && حالت_قدر.st_size == 4 && S_ISREG(حالت_قدر.st_mode));
    تصدیق_کریں((حالت_قدر.st_mode & 0777) == 0640 && حالت_قدر.st_nlink == 1);
    تصدیق_کریں(تلاش_کرنا_فائل(فائل_کا_نام, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(فائل_کا_نام);
    تصدیق_کریں(복제 == 4);
    تصدیق_کریں(파일자료읽기(복제, کوائف, 2) == 2 && memcmp(کوائف, "ab", 2) == 0);
    تصدیق_کریں(파일자료읽기(فائل_کا_نام, کوائف, 2) == 2 && memcmp(کوائف, "cd", 2) == 0);
    تصدیق_کریں(파일자료읽기(فائل_کا_نام, کوائف, 1) == 0);
    تصدیق_کریں(fcntl(فائل_کا_نام, F_SETFD, FD_CLOEXEC) == 0 && fcntl(فائل_کا_نام, F_GETFD) == 1);
    تصدیق_کریں(fcntl(복제, F_GETFD) == 0);
    تصدیق_کریں(dup2(فائل_کا_نام, فائل_کا_نام) == فائل_کا_نام && fcntl(فائل_کا_نام, F_GETFD) == 1);
    تصدیق_کریں(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    تصدیق_کریں(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(فائل_کا_نام, F_GETFL) & O_APPEND));
    تصدیق_کریں(lseek(فائل_کا_نام, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(فائل_کا_نام, 0, SEEK_CUR) == 5);
    تصدیق_کریں(fcntl(فائل_کا_نام, F_SETFL, 0) == 0);
    تصدیق_کریں(lseek(فائل_کا_نام, 8, SEEK_SET) == 8 && write(فائل_کا_نام, "Z", 1) == 1);
    تصدیق_کریں(lseek(복제, 5, SEEK_SET) == 5 && read(فائل_کا_نام, کوائف, 4) == 4);
    تصدیق_کریں(کوائف[0] == 0 && کوائف[1] == 0 && کوائف[2] == 0 && کوائف[3] == 'Z');
    تصدیق_کریں(ftruncate(فائل_کا_نام, 2) == 0 && lseek(فائل_کا_نام, 0, SEEK_CUR) == 9);
    تصدیق_کریں(ftruncate(فائل_کا_نام, 6) == 0 && lseek(فائل_کا_نام, 2, SEEK_SET) == 2 && read(فائل_کا_نام, کوائف, 4) == 4);
    تصدیق_کریں(!کوائف[0] && !کوائف[1] && !کوائف[2] && !کوائف[3]);
    تصدیق_کریں(lseek(فائل_کا_نام, 2147483647, SEEK_SET) == 2147483647);
    تصدیق_کریں(lseek(فائل_کا_نام, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    تصدیق_کریں(lseek(فائل_کا_نام, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    تصدیق_کریں(write(فائل_کا_نام, "!", 1) == -1 && errno == EFBIG);
    تصدیق_کریں(lseek(فائل_کا_نام, 0, SEEK_SET) == 0);
    تصدیق_کریں(read(فائل_کا_نام, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تصدیق_کریں(read(فائل_کا_نام, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    تصدیق_کریں(write(فائل_کا_نام, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    تصدیق_کریں(read(فائل_کا_نام, کوائف, (size_t)-1) == -1 && errno == EINVAL);
    تصدیق_کریں(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    تصدیق_کریں(fstat(فائل_کا_نام, (void *)0x00100000) == -1 && errno == EFAULT);
    تصدیق_کریں(lseek(فائل_کا_نام, 0, SEEK_CUR) == 0);
    تصدیق_کریں(read(فائل_کا_نام, NULL, 0) == 0 && write(فائل_کا_نام, NULL, 0) == 0);
    تصدیق_کریں(ہٹائیں_فائل_اندراج_نام("posix.txt") == 0);
    تصدیق_کریں(fstat(فائل_کا_نام, &حالت_قدر) == 0 && حالت_قدر.st_nlink == 0 && حالت_قدر.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    تصدیق_کریں(새파일 == 5 && fstat(새파일, &حالت_قدر) == 0 && حالت_قدر.st_size == 0);
    تصدیق_کریں(read(فائل_کا_نام, کوائف, 2) == 2 && memcmp(کوائف, "ab", 2) == 0);
    تصدیق_کریں(close(فائل_کا_نام) == 0 && close(복제) == 0 && close(새파일) == 0);
    تصدیق_کریں(close(새파일) == -1 && errno == EBADF);
    تصدیق_کریں(unlink("posix.txt") == 0);
    فائل_کا_نام = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    تصدیق_کریں(فائل_کا_نام == 3 && fcntl(فائل_کا_نام, F_GETFD) == 1);
    تصدیق_کریں(read(فائل_کا_نام, کوائف, 1) == -1 && errno == EBADF);
    تصدیق_کریں(write(فائل_کا_نام, "keep", 4) == 4);
    for (int اشاریہ = 4; اشاریہ < 32; اشاریہ++) تصدیق_کریں(dup(فائل_کا_نام) == اشاریہ);
    تصدیق_کریں(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    تصدیق_کریں(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    تصدیق_کریں(fstat(فائل_کا_نام, &حالت_قدر) == 0 && حالت_قدر.st_size == 4);
    for (int اشاریہ = 3; اشاریہ < 32; اشاریہ++) تصدیق_کریں(close(اشاریہ) == 0);
    تصدیق_کریں(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    فائل_کا_نام = open("posix.txt", O_RDONLY);
    تصدیق_کریں(فائل_کا_نام == 3 && write(فائل_کا_نام, کوائف, 1) == -1 && errno == EBADF);
    تصدیق_کریں(fcntl(فائل_کا_نام, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    تصدیق_کریں(close(8) == 0 && close(فائل_کا_نام) == 0 && unlink("posix.txt") == 0);
    تصدیق_کریں(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    تصدیق_کریں(fstat(1, &حالت_قدر) == 0 && S_ISCHR(حالت_قدر.st_mode));
    تصدیق_کریں(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    تصدیق_کریں(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr پتہ; char پتہ_متن[16];
    تصدیق_کریں(inet_pton(AF_INET, "10.0.2.2", &پتہ) == 1 && ntohl(پتہ.s_addr) == 0x0a000202U);
    تصدیق_کریں(inet_ntop(AF_INET, &پتہ, پتہ_متن, sizeof پتہ_متن) == پتہ_متن && strcmp(پتہ_متن, "10.0.2.2") == 0);
    تصدیق_کریں(inet_pton(AF_INET, "256.0.0.1", &پتہ) == 0 && ntohl(پتہ.s_addr) == 0x0a000202U);
    تصدیق_کریں(inet_pton(AF_INET, "01.0.0.1", &پتہ) == 0);
    تصدیق_کریں(inet_ntop(AF_INET, &پتہ, پتہ_متن, 3) == NULL && errno == ENOSPC);
    تصدیق_کریں(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char نام[] = "slot0";
    for (int اشاریہ = 0; اشاریہ < 8; اشاریہ++) {
        نام[4] = '0' + اشاریہ;
        int 열린파일 = open(نام, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { تصدیق_کریں(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    تصدیق_کریں(개수 > 0 && 개수 < 8);
    تصدیق_کریں(unlink("slot0") == 0);
    تصدیق_کریں(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    تصدیق_کریں(close(보관[0]) == 0);
    فائل_کا_نام = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    تصدیق_کریں(فائل_کا_نام >= 0 && close(فائل_کا_نام) == 0 && unlink("held-slot") == 0);
    for (int اشاریہ = 1; اشاریہ < 개수; اشاریہ++) {
        نام[4] = '0' + اشاریہ;
        تصدیق_کریں(close(보관[اشاریہ]) == 0 && unlink(نام) == 0);
    }
    تصدیق_کریں(fsync(-1) == -1 && errno == EBADF);
    تصدیق_کریں(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
