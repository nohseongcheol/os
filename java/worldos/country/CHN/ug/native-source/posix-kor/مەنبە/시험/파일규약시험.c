#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int شەرت, int قۇر) {
    검사항목수++;
    if (!شەرت) {
        puts("POSIX CHECK FAILED");
        char خانا_قىممىتى[12]; int ئۇزۇنلۇق_قىممىتى = 0;
        do { خانا_قىممىتى[ئۇزۇنلۇق_قىممىتى++] = '0' + قۇر % 10; قۇر /= 10; } while (قۇر);
        while (ئۇزۇنلۇق_قىممىتى) putchar(خانا_قىممىتى[--ئۇزۇنلۇق_قىممىتى]);
        putchar('\n'); _exit(1);
    }
}
#define دەلىللىمەك(شەرت) 검사((شەرت), __LINE__)

int main(int 인수개수, char **دەلىل_تىزىم) {
    char مەلۇمات[32]; struct stat ھالەت_قىممىتى;
    دەلىللىمەك(인수개수 == 2 && strcmp(دەلىل_تىزىم[1], "check") == 0 && دەلىل_تىزىم[2] == 0);
    دەلىللىمەك(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    دەلىللىمەك(قۇرۇش_ھۆججەت("absent", ئوقۇشقىلا_بولىدىغان_قىممىتى) == -1 && 오류번호 == ENOENT);
    int ھۆججەت = قۇرۇش_ھۆججەت("/posix.txt", ئوقۇش_يېزىش | 새파일만들기, 0640);
    دەلىللىمەك(ھۆججەت == 3);
    دەلىللىمەك(يازماق_ھۆججەت_مەلۇمات(ھۆججەت, "abcd", 4) == 4);
    دەلىللىمەك(قۇرۇش_ھۆججەت("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    دەلىللىمەك(파일상태읽기(ھۆججەت, &ھالەت_قىممىتى) == 0 && ھالەت_قىممىتى.st_size == 4 && S_ISREG(ھالەت_قىممىتى.st_mode));
    دەلىللىمەك((ھالەت_قىممىتى.st_mode & 0777) == 0640 && ھالەت_قىممىتى.st_nlink == 1);
    دەلىللىمەك(ئىزدەش_ھۆججەت(ھۆججەت, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ھۆججەت);
    دەلىللىمەك(복제 == 4);
    دەلىللىمەك(파일자료읽기(복제, مەلۇمات, 2) == 2 && memcmp(مەلۇمات, "ab", 2) == 0);
    دەلىللىمەك(파일자료읽기(ھۆججەت, مەلۇمات, 2) == 2 && memcmp(مەلۇمات, "cd", 2) == 0);
    دەلىللىمەك(파일자료읽기(ھۆججەت, مەلۇمات, 1) == 0);
    دەلىللىمەك(fcntl(ھۆججەت, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ھۆججەت, F_GETFD) == 1);
    دەلىللىمەك(fcntl(복제, F_GETFD) == 0);
    دەلىللىمەك(dup2(ھۆججەت, ھۆججەت) == ھۆججەت && fcntl(ھۆججەت, F_GETFD) == 1);
    دەلىللىمەك(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    دەلىللىمەك(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ھۆججەت, F_GETFL) & O_APPEND));
    دەلىللىمەك(lseek(ھۆججەت, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ھۆججەت, 0, SEEK_CUR) == 5);
    دەلىللىمەك(fcntl(ھۆججەت, F_SETFL, 0) == 0);
    دەلىللىمەك(lseek(ھۆججەت, 8, SEEK_SET) == 8 && write(ھۆججەت, "Z", 1) == 1);
    دەلىللىمەك(lseek(복제, 5, SEEK_SET) == 5 && read(ھۆججەت, مەلۇمات, 4) == 4);
    دەلىللىمەك(مەلۇمات[0] == 0 && مەلۇمات[1] == 0 && مەلۇمات[2] == 0 && مەلۇمات[3] == 'Z');
    دەلىللىمەك(ftruncate(ھۆججەت, 2) == 0 && lseek(ھۆججەت, 0, SEEK_CUR) == 9);
    دەلىللىمەك(ftruncate(ھۆججەت, 6) == 0 && lseek(ھۆججەت, 2, SEEK_SET) == 2 && read(ھۆججەت, مەلۇمات, 4) == 4);
    دەلىللىمەك(!مەلۇمات[0] && !مەلۇمات[1] && !مەلۇمات[2] && !مەلۇمات[3]);
    دەلىللىمەك(lseek(ھۆججەت, 2147483647, SEEK_SET) == 2147483647);
    دەلىللىمەك(lseek(ھۆججەت, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    دەلىللىمەك(lseek(ھۆججەت, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    دەلىللىمەك(write(ھۆججەت, "!", 1) == -1 && errno == EFBIG);
    دەلىللىمەك(lseek(ھۆججەت, 0, SEEK_SET) == 0);
    دەلىللىمەك(read(ھۆججەت, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    دەلىللىمەك(read(ھۆججەت, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    دەلىللىمەك(write(ھۆججەت, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    دەلىللىمەك(read(ھۆججەت, مەلۇمات, (size_t)-1) == -1 && errno == EINVAL);
    دەلىللىمەك(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    دەلىللىمەك(fstat(ھۆججەت, (void *)0x00100000) == -1 && errno == EFAULT);
    دەلىللىمەك(lseek(ھۆججەت, 0, SEEK_CUR) == 0);
    دەلىللىمەك(read(ھۆججەت, NULL, 0) == 0 && write(ھۆججەت, NULL, 0) == 0);
    دەلىللىمەك(چىقىرىۋەتمەك_ھۆججەت_كىرگۈزۈش_نامى("posix.txt") == 0);
    دەلىللىمەك(fstat(ھۆججەت, &ھالەت_قىممىتى) == 0 && ھالەت_قىممىتى.st_nlink == 0 && ھالەت_قىممىتى.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    دەلىللىمەك(새파일 == 5 && fstat(새파일, &ھالەت_قىممىتى) == 0 && ھالەت_قىممىتى.st_size == 0);
    دەلىللىمەك(read(ھۆججەت, مەلۇمات, 2) == 2 && memcmp(مەلۇمات, "ab", 2) == 0);
    دەلىللىمەك(close(ھۆججەت) == 0 && close(복제) == 0 && close(새파일) == 0);
    دەلىللىمەك(close(새파일) == -1 && errno == EBADF);
    دەلىللىمەك(unlink("posix.txt") == 0);
    ھۆججەت = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    دەلىللىمەك(ھۆججەت == 3 && fcntl(ھۆججەت, F_GETFD) == 1);
    دەلىللىمەك(read(ھۆججەت, مەلۇمات, 1) == -1 && errno == EBADF);
    دەلىللىمەك(write(ھۆججەت, "keep", 4) == 4);
    for (int ئىندېكس = 4; ئىندېكس < 32; ئىندېكس++) دەلىللىمەك(dup(ھۆججەت) == ئىندېكس);
    دەلىللىمەك(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    دەلىللىمەك(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    دەلىللىمەك(fstat(ھۆججەت, &ھالەت_قىممىتى) == 0 && ھالەت_قىممىتى.st_size == 4);
    for (int ئىندېكس = 3; ئىندېكس < 32; ئىندېكس++) دەلىللىمەك(close(ئىندېكس) == 0);
    دەلىللىمەك(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ھۆججەت = open("posix.txt", O_RDONLY);
    دەلىللىمەك(ھۆججەت == 3 && write(ھۆججەت, مەلۇمات, 1) == -1 && errno == EBADF);
    دەلىللىمەك(fcntl(ھۆججەت, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    دەلىللىمەك(close(8) == 0 && close(ھۆججەت) == 0 && unlink("posix.txt") == 0);
    دەلىللىمەك(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    دەلىللىمەك(fstat(1, &ھالەت_قىممىتى) == 0 && S_ISCHR(ھالەت_قىممىتى.st_mode));
    دەلىللىمەك(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    دەلىللىمەك(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ئادرېس; char ئادرېس_تېكست[16];
    دەلىللىمەك(inet_pton(AF_INET, "10.0.2.2", &ئادرېس) == 1 && ntohl(ئادرېس.s_addr) == 0x0a000202U);
    دەلىللىمەك(inet_ntop(AF_INET, &ئادرېس, ئادرېس_تېكست, sizeof ئادرېس_تېكست) == ئادرېس_تېكست && strcmp(ئادرېس_تېكست, "10.0.2.2") == 0);
    دەلىللىمەك(inet_pton(AF_INET, "256.0.0.1", &ئادرېس) == 0 && ntohl(ئادرېس.s_addr) == 0x0a000202U);
    دەلىللىمەك(inet_pton(AF_INET, "01.0.0.1", &ئادرېس) == 0);
    دەلىللىمەك(inet_ntop(AF_INET, &ئادرېس, ئادرېس_تېكست, 3) == NULL && errno == ENOSPC);
    دەلىللىمەك(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ئاتى[] = "slot0";
    for (int ئىندېكس = 0; ئىندېكس < 8; ئىندېكس++) {
        ئاتى[4] = '0' + ئىندېكس;
        int 열린파일 = open(ئاتى, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { دەلىللىمەك(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    دەلىللىمەك(개수 > 0 && 개수 < 8);
    دەلىللىمەك(unlink("slot0") == 0);
    دەلىللىمەك(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    دەلىللىمەك(close(보관[0]) == 0);
    ھۆججەت = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    دەلىللىمەك(ھۆججەت >= 0 && close(ھۆججەت) == 0 && unlink("held-slot") == 0);
    for (int ئىندېكس = 1; ئىندېكس < 개수; ئىندېكس++) {
        ئاتى[4] = '0' + ئىندېكس;
        دەلىللىمەك(close(보관[ئىندېكس]) == 0 && unlink(ئاتى) == 0);
    }
    دەلىللىمەك(fsync(-1) == -1 && errno == EBADF);
    دەلىللىمەك(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
