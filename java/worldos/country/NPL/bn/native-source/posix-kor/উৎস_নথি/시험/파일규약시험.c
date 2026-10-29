#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int শর্ত, int নিবেশের_পঙ্_ক্তি) {
    검사항목수++;
    if (!শর্ত) {
        puts("POSIX CHECK FAILED");
        char সংখ্যা_মান[12]; int দৈর্ঘ্য_মান = 0;
        do { সংখ্যা_মান[দৈর্ঘ্য_মান++] = '0' + নিবেশের_পঙ্_ক্তি % 10; নিবেশের_পঙ্_ক্তি /= 10; } while (নিবেশের_পঙ্_ক্তি);
        while (দৈর্ঘ্য_মান) putchar(সংখ্যা_মান[--দৈর্ঘ্য_মান]);
        putchar('\n'); _exit(1);
    }
}
#define যাচাই_করা(শর্ত) 검사((শর্ত), __LINE__)

int main(int 인수개수, char **যুক্তি_তালিকা) {
    char ডাটা[32]; struct stat অবস্হা_মান;
    যাচাই_করা(인수개수 == 2 && strcmp(যুক্তি_তালিকা[1], "check") == 0 && যুক্তি_তালিকা[2] == 0);
    যাচাই_করা(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    যাচাই_করা(খোলা_ফাইল("absent", কেবল_পাঠযোগ্য_মান) == -1 && 오류번호 == ENOENT);
    int নথির_নাম = খোলা_ফাইল("/posix.txt", পঠন_লিখন | 새파일만들기, 0640);
    যাচাই_করা(নথির_নাম == 3);
    যাচাই_করা(লেখা_ফাইল_ডাটা(নথির_নাম, "abcd", 4) == 4);
    যাচাই_করা(খোলা_ফাইল("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    যাচাই_করা(파일상태읽기(নথির_নাম, &অবস্হা_মান) == 0 && অবস্হা_মান.st_size == 4 && S_ISREG(অবস্হা_মান.st_mode));
    যাচাই_করা((অবস্হা_মান.st_mode & 0777) == 0640 && অবস্হা_মান.st_nlink == 1);
    যাচাই_করা(সিক_ফাইল(নথির_নাম, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(নথির_নাম);
    যাচাই_করা(복제 == 4);
    যাচাই_করা(파일자료읽기(복제, ডাটা, 2) == 2 && memcmp(ডাটা, "ab", 2) == 0);
    যাচাই_করা(파일자료읽기(নথির_নাম, ডাটা, 2) == 2 && memcmp(ডাটা, "cd", 2) == 0);
    যাচাই_করা(파일자료읽기(নথির_নাম, ডাটা, 1) == 0);
    যাচাই_করা(fcntl(নথির_নাম, F_SETFD, FD_CLOEXEC) == 0 && fcntl(নথির_নাম, F_GETFD) == 1);
    যাচাই_করা(fcntl(복제, F_GETFD) == 0);
    যাচাই_করা(dup2(নথির_নাম, নথির_নাম) == নথির_নাম && fcntl(নথির_নাম, F_GETFD) == 1);
    যাচাই_করা(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    যাচাই_করা(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(নথির_নাম, F_GETFL) & O_APPEND));
    যাচাই_করা(lseek(নথির_নাম, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(নথির_নাম, 0, SEEK_CUR) == 5);
    যাচাই_করা(fcntl(নথির_নাম, F_SETFL, 0) == 0);
    যাচাই_করা(lseek(নথির_নাম, 8, SEEK_SET) == 8 && write(নথির_নাম, "Z", 1) == 1);
    যাচাই_করা(lseek(복제, 5, SEEK_SET) == 5 && read(নথির_নাম, ডাটা, 4) == 4);
    যাচাই_করা(ডাটা[0] == 0 && ডাটা[1] == 0 && ডাটা[2] == 0 && ডাটা[3] == 'Z');
    যাচাই_করা(ftruncate(নথির_নাম, 2) == 0 && lseek(নথির_নাম, 0, SEEK_CUR) == 9);
    যাচাই_করা(ftruncate(নথির_নাম, 6) == 0 && lseek(নথির_নাম, 2, SEEK_SET) == 2 && read(নথির_নাম, ডাটা, 4) == 4);
    যাচাই_করা(!ডাটা[0] && !ডাটা[1] && !ডাটা[2] && !ডাটা[3]);
    যাচাই_করা(lseek(নথির_নাম, 2147483647, SEEK_SET) == 2147483647);
    যাচাই_করা(lseek(নথির_নাম, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    যাচাই_করা(lseek(নথির_নাম, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    যাচাই_করা(write(নথির_নাম, "!", 1) == -1 && errno == EFBIG);
    যাচাই_করা(lseek(নথির_নাম, 0, SEEK_SET) == 0);
    যাচাই_করা(read(নথির_নাম, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    যাচাই_করা(read(নথির_নাম, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    যাচাই_করা(write(নথির_নাম, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    যাচাই_করা(read(নথির_নাম, ডাটা, (size_t)-1) == -1 && errno == EINVAL);
    যাচাই_করা(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    যাচাই_করা(fstat(নথির_নাম, (void *)0x00100000) == -1 && errno == EFAULT);
    যাচাই_করা(lseek(নথির_নাম, 0, SEEK_CUR) == 0);
    যাচাই_করা(read(নথির_নাম, NULL, 0) == 0 && write(নথির_নাম, NULL, 0) == 0);
    যাচাই_করা(সরানো_ফাইল_ভুক্তি_নাম("posix.txt") == 0);
    যাচাই_করা(fstat(নথির_নাম, &অবস্হা_মান) == 0 && অবস্হা_মান.st_nlink == 0 && অবস্হা_মান.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    যাচাই_করা(새파일 == 5 && fstat(새파일, &অবস্হা_মান) == 0 && অবস্হা_মান.st_size == 0);
    যাচাই_করা(read(নথির_নাম, ডাটা, 2) == 2 && memcmp(ডাটা, "ab", 2) == 0);
    যাচাই_করা(close(নথির_নাম) == 0 && close(복제) == 0 && close(새파일) == 0);
    যাচাই_করা(close(새파일) == -1 && errno == EBADF);
    যাচাই_করা(unlink("posix.txt") == 0);
    নথির_নাম = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    যাচাই_করা(নথির_নাম == 3 && fcntl(নথির_নাম, F_GETFD) == 1);
    যাচাই_করা(read(নথির_নাম, ডাটা, 1) == -1 && errno == EBADF);
    যাচাই_করা(write(নথির_নাম, "keep", 4) == 4);
    for (int সূচি = 4; সূচি < 32; সূচি++) যাচাই_করা(dup(নথির_নাম) == সূচি);
    যাচাই_করা(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    যাচাই_করা(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    যাচাই_করা(fstat(নথির_নাম, &অবস্হা_মান) == 0 && অবস্হা_মান.st_size == 4);
    for (int সূচি = 3; সূচি < 32; সূচি++) যাচাই_করা(close(সূচি) == 0);
    যাচাই_করা(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    নথির_নাম = open("posix.txt", O_RDONLY);
    যাচাই_করা(নথির_নাম == 3 && write(নথির_নাম, ডাটা, 1) == -1 && errno == EBADF);
    যাচাই_করা(fcntl(নথির_নাম, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    যাচাই_করা(close(8) == 0 && close(নথির_নাম) == 0 && unlink("posix.txt") == 0);
    যাচাই_করা(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    যাচাই_করা(fstat(1, &অবস্হা_মান) == 0 && S_ISCHR(অবস্হা_মান.st_mode));
    যাচাই_করা(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    যাচাই_করা(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ইমেইল; char ইমেইল_পাঠ[16];
    যাচাই_করা(inet_pton(AF_INET, "10.0.2.2", &ইমেইল) == 1 && ntohl(ইমেইল.s_addr) == 0x0a000202U);
    যাচাই_করা(inet_ntop(AF_INET, &ইমেইল, ইমেইল_পাঠ, sizeof ইমেইল_পাঠ) == ইমেইল_পাঠ && strcmp(ইমেইল_পাঠ, "10.0.2.2") == 0);
    যাচাই_করা(inet_pton(AF_INET, "256.0.0.1", &ইমেইল) == 0 && ntohl(ইমেইল.s_addr) == 0x0a000202U);
    যাচাই_করা(inet_pton(AF_INET, "01.0.0.1", &ইমেইল) == 0);
    যাচাই_করা(inet_ntop(AF_INET, &ইমেইল, ইমেইল_পাঠ, 3) == NULL && errno == ENOSPC);
    যাচাই_করা(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char নাম[] = "slot0";
    for (int সূচি = 0; সূচি < 8; সূচি++) {
        নাম[4] = '0' + সূচি;
        int 열린파일 = open(নাম, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { যাচাই_করা(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    যাচাই_করা(개수 > 0 && 개수 < 8);
    যাচাই_করা(unlink("slot0") == 0);
    যাচাই_করা(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    যাচাই_করা(close(보관[0]) == 0);
    নথির_নাম = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    যাচাই_করা(নথির_নাম >= 0 && close(নথির_নাম) == 0 && unlink("held-slot") == 0);
    for (int সূচি = 1; সূচি < 개수; সূচি++) {
        নাম[4] = '0' + সূচি;
        যাচাই_করা(close(보관[সূচি]) == 0 && unlink(নাম) == 0);
    }
    যাচাই_করা(fsync(-1) == -1 && errno == EBADF);
    যাচাই_করা(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
