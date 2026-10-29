#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int תנאי, int שורה) {
    검사항목수++;
    if (!תנאי) {
        puts("POSIX CHECK FAILED");
        char ספרה_ערך[12]; int 길이 = 0;
        do { ספרה_ערך[길이++] = '0' + שורה % 10; שורה /= 10; } while (שורה);
        while (길이) putchar(ספרה_ערך[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define ודא_אמת(תנאי) 검사((תנאי), __LINE__)

int main(int 인수개수, char **ארגומנט_רשימה) {
    char נתונים[32]; struct stat מצב_ערך;
    ודא_אמת(인수개수 == 2 && strcmp(ארגומנט_רשימה[1], "check") == 0 && ארגומנט_רשימה[2] == 0);
    ודא_אמת(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ודא_אמת(פתח_קובץ("absent", לקריאה_בלבד_ערך) == -1 && מספר_שגיאה == ENOENT);
    int קובץ = פתח_קובץ("/posix.txt", קריאה_כתיבה | 새파일만들기, 0640);
    ודא_אמת(קובץ == 3);
    ודא_אמת(כתיבה_קובץ_נתונים(קובץ, "abcd", 4) == 4);
    ודא_אמת(פתח_קובץ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ודא_אמת(파일상태읽기(קובץ, &מצב_ערך) == 0 && מצב_ערך.st_size == 4 && S_ISREG(מצב_ערך.st_mode));
    ודא_אמת((מצב_ערך.st_mode & 0777) == 0640 && מצב_ערך.st_nlink == 1);
    ודא_אמת(חפש_קובץ(קובץ, 0, 처음기준) == 0);
    int לשכפל_ערך = 파일서술자복제(קובץ);
    ודא_אמת(לשכפל_ערך == 4);
    ודא_אמת(파일자료읽기(לשכפל_ערך, נתונים, 2) == 2 && memcmp(נתונים, "ab", 2) == 0);
    ודא_אמת(파일자료읽기(קובץ, נתונים, 2) == 2 && memcmp(נתונים, "cd", 2) == 0);
    ודא_אמת(파일자료읽기(קובץ, נתונים, 1) == 0);
    ודא_אמת(fcntl(קובץ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(קובץ, F_GETFD) == 1);
    ודא_אמת(fcntl(לשכפל_ערך, F_GETFD) == 0);
    ודא_אמת(dup2(קובץ, קובץ) == קובץ && fcntl(קובץ, F_GETFD) == 1);
    ודא_אמת(dup2(-1, לשכפל_ערך) == -1 && errno == EBADF && fcntl(לשכפל_ערך, F_GETFD) == 0);
    ודא_אמת(fcntl(לשכפל_ערך, F_SETFL, O_APPEND) == 0 && (fcntl(קובץ, F_GETFL) & O_APPEND));
    ודא_אמת(lseek(קובץ, 0, SEEK_SET) == 0 && write(לשכפל_ערך, "e", 1) == 1 && lseek(קובץ, 0, SEEK_CUR) == 5);
    ודא_אמת(fcntl(קובץ, F_SETFL, 0) == 0);
    ודא_אמת(lseek(קובץ, 8, SEEK_SET) == 8 && write(קובץ, "Z", 1) == 1);
    ודא_אמת(lseek(לשכפל_ערך, 5, SEEK_SET) == 5 && read(קובץ, נתונים, 4) == 4);
    ודא_אמת(נתונים[0] == 0 && נתונים[1] == 0 && נתונים[2] == 0 && נתונים[3] == 'Z');
    ודא_אמת(ftruncate(קובץ, 2) == 0 && lseek(קובץ, 0, SEEK_CUR) == 9);
    ודא_אמת(ftruncate(קובץ, 6) == 0 && lseek(קובץ, 2, SEEK_SET) == 2 && read(קובץ, נתונים, 4) == 4);
    ודא_אמת(!נתונים[0] && !נתונים[1] && !נתונים[2] && !נתונים[3]);
    ודא_אמת(lseek(קובץ, 2147483647, SEEK_SET) == 2147483647);
    ודא_אמת(lseek(קובץ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ודא_אמת(lseek(קובץ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ודא_אמת(write(קובץ, "!", 1) == -1 && errno == EFBIG);
    ודא_אמת(lseek(קובץ, 0, SEEK_SET) == 0);
    ודא_אמת(read(קובץ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ודא_אמת(read(קובץ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ודא_אמת(write(קובץ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ודא_אמת(read(קובץ, נתונים, (size_t)-1) == -1 && errno == EINVAL);
    ודא_אמת(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ודא_אמת(fstat(קובץ, (void *)0x00100000) == -1 && errno == EFAULT);
    ודא_אמת(lseek(קובץ, 0, SEEK_CUR) == 0);
    ודא_אמת(read(קובץ, NULL, 0) == 0 && write(קובץ, NULL, 0) == 0);
    ודא_אמת(הסר_קובץ_ערך_שם("posix.txt") == 0);
    ודא_אמת(fstat(קובץ, &מצב_ערך) == 0 && מצב_ערך.st_nlink == 0 && מצב_ערך.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ודא_אמת(새파일 == 5 && fstat(새파일, &מצב_ערך) == 0 && מצב_ערך.st_size == 0);
    ודא_אמת(read(קובץ, נתונים, 2) == 2 && memcmp(נתונים, "ab", 2) == 0);
    ודא_אמת(close(קובץ) == 0 && close(לשכפל_ערך) == 0 && close(새파일) == 0);
    ודא_אמת(close(새파일) == -1 && errno == EBADF);
    ודא_אמת(unlink("posix.txt") == 0);
    קובץ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ודא_אמת(קובץ == 3 && fcntl(קובץ, F_GETFD) == 1);
    ודא_אמת(read(קובץ, נתונים, 1) == -1 && errno == EBADF);
    ודא_אמת(write(קובץ, "keep", 4) == 4);
    for (int מדד = 4; מדד < 32; מדד++) ודא_אמת(dup(קובץ) == מדד);
    ודא_אמת(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ודא_אמת(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ודא_אמת(fstat(קובץ, &מצב_ערך) == 0 && מצב_ערך.st_size == 4);
    for (int מדד = 3; מדד < 32; מדד++) ודא_אמת(close(מדד) == 0);
    ודא_אמת(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    קובץ = open("posix.txt", O_RDONLY);
    ודא_אמת(קובץ == 3 && write(קובץ, נתונים, 1) == -1 && errno == EBADF);
    ודא_אמת(fcntl(קובץ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ודא_אמת(close(8) == 0 && close(קובץ) == 0 && unlink("posix.txt") == 0);
    ודא_אמת(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ודא_אמת(fstat(1, &מצב_ערך) == 0 && S_ISCHR(מצב_ערך.st_mode));
    ודא_אמת(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ודא_אמת(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr למען; char למען_טקסט[16];
    ודא_אמת(inet_pton(AF_INET, "10.0.2.2", &למען) == 1 && ntohl(למען.s_addr) == 0x0a000202U);
    ודא_אמת(inet_ntop(AF_INET, &למען, למען_טקסט, sizeof למען_טקסט) == למען_טקסט && strcmp(למען_טקסט, "10.0.2.2") == 0);
    ודא_אמת(inet_pton(AF_INET, "256.0.0.1", &למען) == 0 && ntohl(למען.s_addr) == 0x0a000202U);
    ודא_אמת(inet_pton(AF_INET, "01.0.0.1", &למען) == 0);
    ודא_אמת(inet_ntop(AF_INET, &למען, למען_טקסט, 3) == NULL && errno == ENOSPC);
    ודא_אמת(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char שם[] = "slot0";
    for (int מדד = 0; מדד < 8; מדד++) {
        שם[4] = '0' + מדד;
        int 열린파일 = open(שם, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ודא_אמת(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ודא_אמת(개수 > 0 && 개수 < 8);
    ודא_אמת(unlink("slot0") == 0);
    ודא_אמת(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ודא_אמת(close(보관[0]) == 0);
    קובץ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ודא_אמת(קובץ >= 0 && close(קובץ) == 0 && unlink("held-slot") == 0);
    for (int מדד = 1; מדד < 개수; מדד++) {
        שם[4] = '0' + מדד;
        ודא_אמת(close(보관[מדד]) == 0 && unlink(שם) == 0);
    }
    ודא_אמת(fsync(-1) == -1 && errno == EBADF);
    ודא_אמת(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
