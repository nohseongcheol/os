#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int स्थिती_291ac971, int रेग) {
    검사항목수++;
    if (!स्थिती_291ac971) {
        puts("POSIX CHECK FAILED");
        char अंक_मोल[12]; int लांबाय_मोल = 0;
        do { अंक_मोल[लांबाय_मोल++] = '0' + रेग % 10; रेग /= 10; } while (रेग);
        while (लांबाय_मोल) putchar(अंक_मोल[--लांबाय_मोल]);
        putchar('\n'); _exit(1);
    }
}
#define पुनर्तपासणी_करची(स्थिती_291ac971) 검사((स्थिती_291ac971), __LINE__)

int main(int 인수개수, char **युक्तीवाद_सुची) {
    char डेटा[32]; struct stat स्थिती_मोल_e10195a1;
    पुनर्तपासणी_करची(인수개수 == 2 && strcmp(युक्तीवाद_सुची[1], "check") == 0 && युक्तीवाद_सुची[2] == 0);
    पुनर्तपासणी_करची(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    पुनर्तपासणी_करची(उगडचें_फायल("absent", फकत_वाचचें_मोल) == -1 && 오류번호 == ENOENT);
    int फायल = उगडचें_फायल("/posix.txt", वाचन_बरप | 새파일만들기, 0640);
    पुनर्तपासणी_करची(फायल == 3);
    पुनर्तपासणी_करची(बरोवचें_फायल_डेटा(फायल, "abcd", 4) == 4);
    पुनर्तपासणी_करची(उगडचें_फायल("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    पुनर्तपासणी_करची(파일상태읽기(फायल, &स्थिती_मोल_e10195a1) == 0 && स्थिती_मोल_e10195a1.st_size == 4 && S_ISREG(स्थिती_मोल_e10195a1.st_mode));
    पुनर्तपासणी_करची((स्थिती_मोल_e10195a1.st_mode & 0777) == 0640 && स्थिती_मोल_e10195a1.st_nlink == 1);
    पुनर्तपासणी_करची(सोद_फायल(फायल, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(फायल);
    पुनर्तपासणी_करची(복제 == 4);
    पुनर्तपासणी_करची(파일자료읽기(복제, डेटा, 2) == 2 && memcmp(डेटा, "ab", 2) == 0);
    पुनर्तपासणी_करची(파일자료읽기(फायल, डेटा, 2) == 2 && memcmp(डेटा, "cd", 2) == 0);
    पुनर्तपासणी_करची(파일자료읽기(फायल, डेटा, 1) == 0);
    पुनर्तपासणी_करची(fcntl(फायल, F_SETFD, FD_CLOEXEC) == 0 && fcntl(फायल, F_GETFD) == 1);
    पुनर्तपासणी_करची(fcntl(복제, F_GETFD) == 0);
    पुनर्तपासणी_करची(dup2(फायल, फायल) == फायल && fcntl(फायल, F_GETFD) == 1);
    पुनर्तपासणी_करची(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    पुनर्तपासणी_करची(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(फायल, F_GETFL) & O_APPEND));
    पुनर्तपासणी_करची(lseek(फायल, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(फायल, 0, SEEK_CUR) == 5);
    पुनर्तपासणी_करची(fcntl(फायल, F_SETFL, 0) == 0);
    पुनर्तपासणी_करची(lseek(फायल, 8, SEEK_SET) == 8 && write(फायल, "Z", 1) == 1);
    पुनर्तपासणी_करची(lseek(복제, 5, SEEK_SET) == 5 && read(फायल, डेटा, 4) == 4);
    पुनर्तपासणी_करची(डेटा[0] == 0 && डेटा[1] == 0 && डेटा[2] == 0 && डेटा[3] == 'Z');
    पुनर्तपासणी_करची(ftruncate(फायल, 2) == 0 && lseek(फायल, 0, SEEK_CUR) == 9);
    पुनर्तपासणी_करची(ftruncate(फायल, 6) == 0 && lseek(फायल, 2, SEEK_SET) == 2 && read(फायल, डेटा, 4) == 4);
    पुनर्तपासणी_करची(!डेटा[0] && !डेटा[1] && !डेटा[2] && !डेटा[3]);
    पुनर्तपासणी_करची(lseek(फायल, 2147483647, SEEK_SET) == 2147483647);
    पुनर्तपासणी_करची(lseek(फायल, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    पुनर्तपासणी_करची(lseek(फायल, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    पुनर्तपासणी_करची(write(फायल, "!", 1) == -1 && errno == EFBIG);
    पुनर्तपासणी_करची(lseek(फायल, 0, SEEK_SET) == 0);
    पुनर्तपासणी_करची(read(फायल, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    पुनर्तपासणी_करची(read(फायल, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    पुनर्तपासणी_करची(write(फायल, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    पुनर्तपासणी_करची(read(फायल, डेटा, (size_t)-1) == -1 && errno == EINVAL);
    पुनर्तपासणी_करची(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    पुनर्तपासणी_करची(fstat(फायल, (void *)0x00100000) == -1 && errno == EFAULT);
    पुनर्तपासणी_करची(lseek(फायल, 0, SEEK_CUR) == 0);
    पुनर्तपासणी_करची(read(फायल, NULL, 0) == 0 && write(फायल, NULL, 0) == 0);
    पुनर्तपासणी_करची(काडचें_फायल_प्रवेश_नांव("posix.txt") == 0);
    पुनर्तपासणी_करची(fstat(फायल, &स्थिती_मोल_e10195a1) == 0 && स्थिती_मोल_e10195a1.st_nlink == 0 && स्थिती_मोल_e10195a1.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    पुनर्तपासणी_करची(새파일 == 5 && fstat(새파일, &स्थिती_मोल_e10195a1) == 0 && स्थिती_मोल_e10195a1.st_size == 0);
    पुनर्तपासणी_करची(read(फायल, डेटा, 2) == 2 && memcmp(डेटा, "ab", 2) == 0);
    पुनर्तपासणी_करची(close(फायल) == 0 && close(복제) == 0 && close(새파일) == 0);
    पुनर्तपासणी_करची(close(새파일) == -1 && errno == EBADF);
    पुनर्तपासणी_करची(unlink("posix.txt") == 0);
    फायल = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    पुनर्तपासणी_करची(फायल == 3 && fcntl(फायल, F_GETFD) == 1);
    पुनर्तपासणी_करची(read(फायल, डेटा, 1) == -1 && errno == EBADF);
    पुनर्तपासणी_करची(write(फायल, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) पुनर्तपासणी_करची(dup(फायल) == INDEX);
    पुनर्तपासणी_करची(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    पुनर्तपासणी_करची(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    पुनर्तपासणी_करची(fstat(फायल, &स्थिती_मोल_e10195a1) == 0 && स्थिती_मोल_e10195a1.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) पुनर्तपासणी_करची(close(INDEX) == 0);
    पुनर्तपासणी_करची(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    फायल = open("posix.txt", O_RDONLY);
    पुनर्तपासणी_करची(फायल == 3 && write(फायल, डेटा, 1) == -1 && errno == EBADF);
    पुनर्तपासणी_करची(fcntl(फायल, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    पुनर्तपासणी_करची(close(8) == 0 && close(फायल) == 0 && unlink("posix.txt") == 0);
    पुनर्तपासणी_करची(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    पुनर्तपासणी_करची(fstat(1, &स्थिती_मोल_e10195a1) == 0 && S_ISCHR(स्थिती_मोल_e10195a1.st_mode));
    पुनर्तपासणी_करची(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    पुनर्तपासणी_करची(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr नामो; char नामो_SMS[16];
    पुनर्तपासणी_करची(inet_pton(AF_INET, "10.0.2.2", &नामो) == 1 && ntohl(नामो.s_addr) == 0x0a000202U);
    पुनर्तपासणी_करची(inet_ntop(AF_INET, &नामो, नामो_SMS, sizeof नामो_SMS) == नामो_SMS && strcmp(नामो_SMS, "10.0.2.2") == 0);
    पुनर्तपासणी_करची(inet_pton(AF_INET, "256.0.0.1", &नामो) == 0 && ntohl(नामो.s_addr) == 0x0a000202U);
    पुनर्तपासणी_करची(inet_pton(AF_INET, "01.0.0.1", &नामो) == 0);
    पुनर्तपासणी_करची(inet_ntop(AF_INET, &नामो, नामो_SMS, 3) == NULL && errno == ENOSPC);
    पुनर्तपासणी_करची(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], आयटम_COUNT = 0; char नांव[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        नांव[4] = '0' + INDEX;
        int 열린파일 = open(नांव, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { पुनर्तपासणी_करची(errno == ENOSPC); break; }
        보관[आयटम_COUNT++] = 열린파일;
    }
    पुनर्तपासणी_करची(आयटम_COUNT > 0 && आयटम_COUNT < 8);
    पुनर्तपासणी_करची(unlink("slot0") == 0);
    पुनर्तपासणी_करची(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    पुनर्तपासणी_करची(close(보관[0]) == 0);
    फायल = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    पुनर्तपासणी_करची(फायल >= 0 && close(फायल) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < आयटम_COUNT; INDEX++) {
        नांव[4] = '0' + INDEX;
        पुनर्तपासणी_करची(close(보관[INDEX]) == 0 && unlink(नांव) == 0);
    }
    पुनर्तपासणी_करची(fsync(-1) == -1 && errno == EBADF);
    पुनर्तपासणी_करची(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
