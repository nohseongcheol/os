#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int सर्त, int रेखा) {
    검사항목수++;
    if (!सर्त) {
        puts("POSIX CHECK FAILED");
        char अङ्क_मान[12]; int लम्बाइ_मान = 0;
        do { अङ्क_मान[लम्बाइ_मान++] = '0' + रेखा % 10; रेखा /= 10; } while (रेखा);
        while (लम्बाइ_मान) putchar(अङ्क_मान[--लम्बाइ_मान]);
        putchar('\n'); _exit(1);
    }
}
#define रुजू_गर्नुहोस्(सर्त) 검사((सर्त), __LINE__)

int main(int 인수개수, char **तर्क_सूची) {
    char लगत[32]; struct stat स्थिति_मान;
    रुजू_गर्नुहोस्(인수개수 == 2 && strcmp(तर्क_सूची[1], "check") == 0 && तर्क_सूची[2] == 0);
    रुजू_गर्नुहोस्(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    रुजू_गर्नुहोस्(सिर्जना_फाइल("absent", पढ्न_मात्र_मान) == -1 && 오류번호 == ENOENT);
    int फाइल = सिर्जना_फाइल("/posix.txt", पढ्न_लेख्_न | 새파일만들기, 0640);
    रुजू_गर्नुहोस्(फाइल == 3);
    रुजू_गर्नुहोस्(लेख्नुहोस्_फाइल_लगत(फाइल, "abcd", 4) == 4);
    रुजू_गर्नुहोस्(सिर्जना_फाइल("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    रुजू_गर्नुहोस्(파일상태읽기(फाइल, &स्थिति_मान) == 0 && स्थिति_मान.st_size == 4 && S_ISREG(स्थिति_मान.st_mode));
    रुजू_गर्नुहोस्((स्थिति_मान.st_mode & 0777) == 0640 && स्थिति_मान.st_nlink == 1);
    रुजू_गर्नुहोस्(खोज्नुहोस्_फाइल(फाइल, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(फाइल);
    रुजू_गर्नुहोस्(복제 == 4);
    रुजू_गर्नुहोस्(파일자료읽기(복제, लगत, 2) == 2 && memcmp(लगत, "ab", 2) == 0);
    रुजू_गर्नुहोस्(파일자료읽기(फाइल, लगत, 2) == 2 && memcmp(लगत, "cd", 2) == 0);
    रुजू_गर्नुहोस्(파일자료읽기(फाइल, लगत, 1) == 0);
    रुजू_गर्नुहोस्(fcntl(फाइल, F_SETFD, FD_CLOEXEC) == 0 && fcntl(फाइल, F_GETFD) == 1);
    रुजू_गर्नुहोस्(fcntl(복제, F_GETFD) == 0);
    रुजू_गर्नुहोस्(dup2(फाइल, फाइल) == फाइल && fcntl(फाइल, F_GETFD) == 1);
    रुजू_गर्नुहोस्(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    रुजू_गर्नुहोस्(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(फाइल, F_GETFL) & O_APPEND));
    रुजू_गर्नुहोस्(lseek(फाइल, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(फाइल, 0, SEEK_CUR) == 5);
    रुजू_गर्नुहोस्(fcntl(फाइल, F_SETFL, 0) == 0);
    रुजू_गर्नुहोस्(lseek(फाइल, 8, SEEK_SET) == 8 && write(फाइल, "Z", 1) == 1);
    रुजू_गर्नुहोस्(lseek(복제, 5, SEEK_SET) == 5 && read(फाइल, लगत, 4) == 4);
    रुजू_गर्नुहोस्(लगत[0] == 0 && लगत[1] == 0 && लगत[2] == 0 && लगत[3] == 'Z');
    रुजू_गर्नुहोस्(ftruncate(फाइल, 2) == 0 && lseek(फाइल, 0, SEEK_CUR) == 9);
    रुजू_गर्नुहोस्(ftruncate(फाइल, 6) == 0 && lseek(फाइल, 2, SEEK_SET) == 2 && read(फाइल, लगत, 4) == 4);
    रुजू_गर्नुहोस्(!लगत[0] && !लगत[1] && !लगत[2] && !लगत[3]);
    रुजू_गर्नुहोस्(lseek(फाइल, 2147483647, SEEK_SET) == 2147483647);
    रुजू_गर्नुहोस्(lseek(फाइल, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    रुजू_गर्नुहोस्(lseek(फाइल, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    रुजू_गर्नुहोस्(write(फाइल, "!", 1) == -1 && errno == EFBIG);
    रुजू_गर्नुहोस्(lseek(फाइल, 0, SEEK_SET) == 0);
    रुजू_गर्नुहोस्(read(फाइल, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    रुजू_गर्नुहोस्(read(फाइल, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    रुजू_गर्नुहोस्(write(फाइल, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    रुजू_गर्नुहोस्(read(फाइल, लगत, (size_t)-1) == -1 && errno == EINVAL);
    रुजू_गर्नुहोस्(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    रुजू_गर्नुहोस्(fstat(फाइल, (void *)0x00100000) == -1 && errno == EFAULT);
    रुजू_गर्नुहोस्(lseek(फाइल, 0, SEEK_CUR) == 0);
    रुजू_गर्नुहोस्(read(फाइल, NULL, 0) == 0 && write(फाइल, NULL, 0) == 0);
    रुजू_गर्नुहोस्(हटाउनुहोस्_फाइल_प्रविष्टि_नाम("posix.txt") == 0);
    रुजू_गर्नुहोस्(fstat(फाइल, &स्थिति_मान) == 0 && स्थिति_मान.st_nlink == 0 && स्थिति_मान.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    रुजू_गर्नुहोस्(새파일 == 5 && fstat(새파일, &स्थिति_मान) == 0 && स्थिति_मान.st_size == 0);
    रुजू_गर्नुहोस्(read(फाइल, लगत, 2) == 2 && memcmp(लगत, "ab", 2) == 0);
    रुजू_गर्नुहोस्(close(फाइल) == 0 && close(복제) == 0 && close(새파일) == 0);
    रुजू_गर्नुहोस्(close(새파일) == -1 && errno == EBADF);
    रुजू_गर्नुहोस्(unlink("posix.txt") == 0);
    फाइल = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    रुजू_गर्नुहोस्(फाइल == 3 && fcntl(फाइल, F_GETFD) == 1);
    रुजू_गर्नुहोस्(read(फाइल, लगत, 1) == -1 && errno == EBADF);
    रुजू_गर्नुहोस्(write(फाइल, "keep", 4) == 4);
    for (int अनुक्रमणिका = 4; अनुक्रमणिका < 32; अनुक्रमणिका++) रुजू_गर्नुहोस्(dup(फाइल) == अनुक्रमणिका);
    रुजू_गर्नुहोस्(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    रुजू_गर्नुहोस्(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    रुजू_गर्नुहोस्(fstat(फाइल, &स्थिति_मान) == 0 && स्थिति_मान.st_size == 4);
    for (int अनुक्रमणिका = 3; अनुक्रमणिका < 32; अनुक्रमणिका++) रुजू_गर्नुहोस्(close(अनुक्रमणिका) == 0);
    रुजू_गर्नुहोस्(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    फाइल = open("posix.txt", O_RDONLY);
    रुजू_गर्नुहोस्(फाइल == 3 && write(फाइल, लगत, 1) == -1 && errno == EBADF);
    रुजू_गर्नुहोस्(fcntl(फाइल, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    रुजू_गर्नुहोस्(close(8) == 0 && close(फाइल) == 0 && unlink("posix.txt") == 0);
    रुजू_गर्नुहोस्(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    रुजू_गर्नुहोस्(fstat(1, &स्थिति_मान) == 0 && S_ISCHR(स्थिति_मान.st_mode));
    रुजू_गर्नुहोस्(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    रुजू_गर्नुहोस्(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ठेगाना; char ठेगाना_पाठ[16];
    रुजू_गर्नुहोस्(inet_pton(AF_INET, "10.0.2.2", &ठेगाना) == 1 && ntohl(ठेगाना.s_addr) == 0x0a000202U);
    रुजू_गर्नुहोस्(inet_ntop(AF_INET, &ठेगाना, ठेगाना_पाठ, sizeof ठेगाना_पाठ) == ठेगाना_पाठ && strcmp(ठेगाना_पाठ, "10.0.2.2") == 0);
    रुजू_गर्नुहोस्(inet_pton(AF_INET, "256.0.0.1", &ठेगाना) == 0 && ntohl(ठेगाना.s_addr) == 0x0a000202U);
    रुजू_गर्नुहोस्(inet_pton(AF_INET, "01.0.0.1", &ठेगाना) == 0);
    रुजू_गर्नुहोस्(inet_ntop(AF_INET, &ठेगाना, ठेगाना_पाठ, 3) == NULL && errno == ENOSPC);
    रुजू_गर्नुहोस्(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char नाम[] = "slot0";
    for (int अनुक्रमणिका = 0; अनुक्रमणिका < 8; अनुक्रमणिका++) {
        नाम[4] = '0' + अनुक्रमणिका;
        int 열린파일 = open(नाम, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { रुजू_गर्नुहोस्(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    रुजू_गर्नुहोस्(개수 > 0 && 개수 < 8);
    रुजू_गर्नुहोस्(unlink("slot0") == 0);
    रुजू_गर्नुहोस्(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    रुजू_गर्नुहोस्(close(보관[0]) == 0);
    फाइल = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    रुजू_गर्नुहोस्(फाइल >= 0 && close(फाइल) == 0 && unlink("held-slot") == 0);
    for (int अनुक्रमणिका = 1; अनुक्रमणिका < 개수; अनुक्रमणिका++) {
        नाम[4] = '0' + अनुक्रमणिका;
        रुजू_गर्नुहोस्(close(보관[अनुक्रमणिका]) == 0 && unlink(नाम) == 0);
    }
    रुजू_गर्नुहोस्(fsync(-1) == -1 && errno == EBADF);
    रुजू_गर्नुहोस्(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
