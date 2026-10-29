#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int চৰ্ত, int লাইন) {
    검사항목수++;
    if (!চৰ্ত) {
        puts("POSIX CHECK FAILED");
        char অংক_মান[12]; int দৈর্ঘ্য_মান = 0;
        do { অংক_মান[দৈর্ঘ্য_মান++] = '0' + লাইন % 10; লাইন /= 10; } while (লাইন);
        while (দৈর্ঘ্য_মান) putchar(অংক_মান[--দৈর্ঘ্য_মান]);
        putchar('\n'); _exit(1);
    }
}
#define প্ৰমাণিত_কৰক(চৰ্ত) 검사((চৰ্ত), __LINE__)

int main(int 인수개수, char **যুক্তি_সূচী) {
    char ডাটা[32]; struct stat অৱস্থা_মান;
    প্ৰমাণিত_কৰক(인수개수 == 2 && strcmp(যুক্তি_সূচী[1], "check") == 0 && যুক্তি_সূচী[2] == 0);
    প্ৰমাণিত_কৰক(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    প্ৰমাণিত_কৰক(খোলক_ফাইল("absent", ৰিড_অনলি_মান) == -1 && 오류번호 == ENOENT);
    int নথিপত্ৰ = খোলক_ফাইল("/posix.txt", পঢ়িব_লিখিব_পৰা | 새파일만들기, 0640);
    প্ৰমাণিত_কৰক(নথিপত্ৰ == 3);
    প্ৰমাণিত_কৰক(লিখক_ফাইল_ডাটা(নথিপত্ৰ, "abcd", 4) == 4);
    প্ৰমাণিত_কৰক(খোলক_ফাইল("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    প্ৰমাণিত_কৰক(파일상태읽기(নথিপত্ৰ, &অৱস্থা_মান) == 0 && অৱস্থা_মান.st_size == 4 && S_ISREG(অৱস্থা_মান.st_mode));
    প্ৰমাণিত_কৰক((অৱস্থা_মান.st_mode & 0777) == 0640 && অৱস্থা_মান.st_nlink == 1);
    প্ৰমাণিত_কৰক(ছীক_ফাইল(নথিপত্ৰ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(নথিপত্ৰ);
    প্ৰমাণিত_কৰক(복제 == 4);
    প্ৰমাণিত_কৰক(파일자료읽기(복제, ডাটা, 2) == 2 && memcmp(ডাটা, "ab", 2) == 0);
    প্ৰমাণিত_কৰক(파일자료읽기(নথিপত্ৰ, ডাটা, 2) == 2 && memcmp(ডাটা, "cd", 2) == 0);
    প্ৰমাণিত_কৰক(파일자료읽기(নথিপত্ৰ, ডাটা, 1) == 0);
    প্ৰমাণিত_কৰক(fcntl(নথিপত্ৰ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(নথিপত্ৰ, F_GETFD) == 1);
    প্ৰমাণিত_কৰক(fcntl(복제, F_GETFD) == 0);
    প্ৰমাণিত_কৰক(dup2(নথিপত্ৰ, নথিপত্ৰ) == নথিপত্ৰ && fcntl(নথিপত্ৰ, F_GETFD) == 1);
    প্ৰমাণিত_কৰক(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    প্ৰমাণিত_কৰক(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(নথিপত্ৰ, F_GETFL) & O_APPEND));
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(নথিপত্ৰ, 0, SEEK_CUR) == 5);
    প্ৰমাণিত_কৰক(fcntl(নথিপত্ৰ, F_SETFL, 0) == 0);
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, 8, SEEK_SET) == 8 && write(নথিপত্ৰ, "Z", 1) == 1);
    প্ৰমাণিত_কৰক(lseek(복제, 5, SEEK_SET) == 5 && read(নথিপত্ৰ, ডাটা, 4) == 4);
    প্ৰমাণিত_কৰক(ডাটা[0] == 0 && ডাটা[1] == 0 && ডাটা[2] == 0 && ডাটা[3] == 'Z');
    প্ৰমাণিত_কৰক(ftruncate(নথিপত্ৰ, 2) == 0 && lseek(নথিপত্ৰ, 0, SEEK_CUR) == 9);
    প্ৰমাণিত_কৰক(ftruncate(নথিপত্ৰ, 6) == 0 && lseek(নথিপত্ৰ, 2, SEEK_SET) == 2 && read(নথিপত্ৰ, ডাটা, 4) == 4);
    প্ৰমাণিত_কৰক(!ডাটা[0] && !ডাটা[1] && !ডাটা[2] && !ডাটা[3]);
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, 2147483647, SEEK_SET) == 2147483647);
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    প্ৰমাণিত_কৰক(write(নথিপত্ৰ, "!", 1) == -1 && errno == EFBIG);
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, 0, SEEK_SET) == 0);
    প্ৰমাণিত_কৰক(read(নথিপত্ৰ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    প্ৰমাণিত_কৰক(read(নথিপত্ৰ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    প্ৰমাণিত_কৰক(write(নথিপত্ৰ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    প্ৰমাণিত_কৰক(read(নথিপত্ৰ, ডাটা, (size_t)-1) == -1 && errno == EINVAL);
    প্ৰমাণিত_কৰক(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    প্ৰমাণিত_কৰক(fstat(নথিপত্ৰ, (void *)0x00100000) == -1 && errno == EFAULT);
    প্ৰমাণিত_কৰক(lseek(নথিপত্ৰ, 0, SEEK_CUR) == 0);
    প্ৰমাণিত_কৰক(read(নথিপত্ৰ, NULL, 0) == 0 && write(নথিপত্ৰ, NULL, 0) == 0);
    প্ৰমাণিত_কৰক(আঁতৰাওক_ফাইল_প্রবিষ্ট_নাম("posix.txt") == 0);
    প্ৰমাণিত_কৰক(fstat(নথিপত্ৰ, &অৱস্থা_মান) == 0 && অৱস্থা_মান.st_nlink == 0 && অৱস্থা_মান.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    প্ৰমাণিত_কৰক(새파일 == 5 && fstat(새파일, &অৱস্থা_মান) == 0 && অৱস্থা_মান.st_size == 0);
    প্ৰমাণিত_কৰক(read(নথিপত্ৰ, ডাটা, 2) == 2 && memcmp(ডাটা, "ab", 2) == 0);
    প্ৰমাণিত_কৰক(close(নথিপত্ৰ) == 0 && close(복제) == 0 && close(새파일) == 0);
    প্ৰমাণিত_কৰক(close(새파일) == -1 && errno == EBADF);
    প্ৰমাণিত_কৰক(unlink("posix.txt") == 0);
    নথিপত্ৰ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    প্ৰমাণিত_কৰক(নথিপত্ৰ == 3 && fcntl(নথিপত্ৰ, F_GETFD) == 1);
    প্ৰমাণিত_কৰক(read(নথিপত্ৰ, ডাটা, 1) == -1 && errno == EBADF);
    প্ৰমাণিত_কৰক(write(নথিপত্ৰ, "keep", 4) == 4);
    for (int ইনডেক্স = 4; ইনডেক্স < 32; ইনডেক্স++) প্ৰমাণিত_কৰক(dup(নথিপত্ৰ) == ইনডেক্স);
    প্ৰমাণিত_কৰক(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    প্ৰমাণিত_কৰক(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    প্ৰমাণিত_কৰক(fstat(নথিপত্ৰ, &অৱস্থা_মান) == 0 && অৱস্থা_মান.st_size == 4);
    for (int ইনডেক্স = 3; ইনডেক্স < 32; ইনডেক্স++) প্ৰমাণিত_কৰক(close(ইনডেক্স) == 0);
    প্ৰমাণিত_কৰক(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    নথিপত্ৰ = open("posix.txt", O_RDONLY);
    প্ৰমাণিত_কৰক(নথিপত্ৰ == 3 && write(নথিপত্ৰ, ডাটা, 1) == -1 && errno == EBADF);
    প্ৰমাণিত_কৰক(fcntl(নথিপত্ৰ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    প্ৰমাণিত_কৰক(close(8) == 0 && close(নথিপত্ৰ) == 0 && unlink("posix.txt") == 0);
    প্ৰমাণিত_কৰক(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    প্ৰমাণিত_কৰক(fstat(1, &অৱস্থা_মান) == 0 && S_ISCHR(অৱস্থা_মান.st_mode));
    প্ৰমাণিত_কৰক(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    প্ৰমাণিত_কৰক(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ঠিকনা; char ঠিকনা_পাঠ[16];
    প্ৰমাণিত_কৰক(inet_pton(AF_INET, "10.0.2.2", &ঠিকনা) == 1 && ntohl(ঠিকনা.s_addr) == 0x0a000202U);
    প্ৰমাণিত_কৰক(inet_ntop(AF_INET, &ঠিকনা, ঠিকনা_পাঠ, sizeof ঠিকনা_পাঠ) == ঠিকনা_পাঠ && strcmp(ঠিকনা_পাঠ, "10.0.2.2") == 0);
    প্ৰমাণিত_কৰক(inet_pton(AF_INET, "256.0.0.1", &ঠিকনা) == 0 && ntohl(ঠিকনা.s_addr) == 0x0a000202U);
    প্ৰমাণিত_কৰক(inet_pton(AF_INET, "01.0.0.1", &ঠিকনা) == 0);
    প্ৰমাণিত_কৰক(inet_ntop(AF_INET, &ঠিকনা, ঠিকনা_পাঠ, 3) == NULL && errno == ENOSPC);
    প্ৰমাণিত_কৰক(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char নাম[] = "slot0";
    for (int ইনডেক্স = 0; ইনডেক্স < 8; ইনডেক্স++) {
        নাম[4] = '0' + ইনডেক্স;
        int 열린파일 = open(নাম, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { প্ৰমাণিত_কৰক(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    প্ৰমাণিত_কৰক(개수 > 0 && 개수 < 8);
    প্ৰমাণিত_কৰক(unlink("slot0") == 0);
    প্ৰমাণিত_কৰক(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    প্ৰমাণিত_কৰক(close(보관[0]) == 0);
    নথিপত্ৰ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    প্ৰমাণিত_কৰক(নথিপত্ৰ >= 0 && close(নথিপত্ৰ) == 0 && unlink("held-slot") == 0);
    for (int ইনডেক্স = 1; ইনডেক্স < 개수; ইনডেক্স++) {
        নাম[4] = '0' + ইনডেক্স;
        প্ৰমাণিত_কৰক(close(보관[ইনডেক্স]) == 0 && unlink(নাম) == 0);
    }
    প্ৰমাণিত_কৰক(fsync(-1) == -1 && errno == EBADF);
    প্ৰমাণিত_কৰক(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
