#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ସର୍ତ୍ତ, int ରେଖା) {
    검사항목수++;
    if (!ସର୍ତ୍ତ) {
        puts("POSIX CHECK FAILED");
        char ଅଙ୍କ_ମୂଲ୍ୟ[12]; int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 0;
        do { ଅଙ୍କ_ମୂଲ୍ୟ[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++] = '0' + ରେଖା % 10; ରେଖା /= 10; } while (ରେଖା);
        while (ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) putchar(ଅଙ୍କ_ମୂଲ୍ୟ[--ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ]);
        putchar('\n'); _exit(1);
    }
}
#define ଯାଞ୍ଚ୍_କରିବା(ସର୍ତ୍ତ) 검사((ସର୍ତ୍ତ), __LINE__)

int main(int 인수개수, char **ଯୁକ୍ତି_ତାଲିକା) {
    char ଡାଟା[32]; struct stat ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1;
    ଯାଞ୍ଚ୍_କରିବା(인수개수 == 2 && strcmp(ଯୁକ୍ତି_ତାଲିକା[1], "check") == 0 && ଯୁକ୍ତି_ତାଲିକା[2] == 0);
    ଯାଞ୍ଚ୍_କରିବା(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ଯାଞ୍ଚ୍_କରିବା(ଖୋଲିବା_ଫାଇଲ୍("absent", ରିଡ଼୍_ଓନ୍ଲି_ମୂଲ୍ୟ) == -1 && 오류번호 == ENOENT);
    int ଫାଇଲ = ଖୋଲିବା_ଫାଇଲ୍("/posix.txt", ପଢିବା_ଲେଖିବା | 새파일만들기, 0640);
    ଯାଞ୍ଚ୍_କରିବା(ଫାଇଲ == 3);
    ଯାଞ୍ଚ୍_କରିବା(ଲିଖନ_ଫାଇଲ୍_ଡାଟା(ଫାଇଲ, "abcd", 4) == 4);
    ଯାଞ୍ଚ୍_କରିବା(ଖୋଲିବା_ଫାଇଲ୍("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ଯାଞ୍ଚ୍_କରିବା(파일상태읽기(ଫାଇଲ, &ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1) == 0 && ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_size == 4 && S_ISREG(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_mode));
    ଯାଞ୍ଚ୍_କରିବା((ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_mode & 0777) == 0640 && ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_nlink == 1);
    ଯାଞ୍ଚ୍_କରିବା(ସୀକ୍_ଫାଇଲ୍(ଫାଇଲ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ଫାଇଲ);
    ଯାଞ୍ଚ୍_କରିବା(복제 == 4);
    ଯାଞ୍ଚ୍_କରିବା(파일자료읽기(복제, ଡାଟା, 2) == 2 && memcmp(ଡାଟା, "ab", 2) == 0);
    ଯାଞ୍ଚ୍_କରିବା(파일자료읽기(ଫାଇଲ, ଡାଟା, 2) == 2 && memcmp(ଡାଟା, "cd", 2) == 0);
    ଯାଞ୍ଚ୍_କରିବା(파일자료읽기(ଫାଇଲ, ଡାଟା, 1) == 0);
    ଯାଞ୍ଚ୍_କରିବା(fcntl(ଫାଇଲ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ଫାଇଲ, F_GETFD) == 1);
    ଯାଞ୍ଚ୍_କରିବା(fcntl(복제, F_GETFD) == 0);
    ଯାଞ୍ଚ୍_କରିବା(dup2(ଫାଇଲ, ଫାଇଲ) == ଫାଇଲ && fcntl(ଫାଇଲ, F_GETFD) == 1);
    ଯାଞ୍ଚ୍_କରିବା(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ଯାଞ୍ଚ୍_କରିବା(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ଫାଇଲ, F_GETFL) & O_APPEND));
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ଫାଇଲ, 0, SEEK_CUR) == 5);
    ଯାଞ୍ଚ୍_କରିବା(fcntl(ଫାଇଲ, F_SETFL, 0) == 0);
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, 8, SEEK_SET) == 8 && write(ଫାଇଲ, "Z", 1) == 1);
    ଯାଞ୍ଚ୍_କରିବା(lseek(복제, 5, SEEK_SET) == 5 && read(ଫାଇଲ, ଡାଟା, 4) == 4);
    ଯାଞ୍ଚ୍_କରିବା(ଡାଟା[0] == 0 && ଡାଟା[1] == 0 && ଡାଟା[2] == 0 && ଡାଟା[3] == 'Z');
    ଯାଞ୍ଚ୍_କରିବା(ftruncate(ଫାଇଲ, 2) == 0 && lseek(ଫାଇଲ, 0, SEEK_CUR) == 9);
    ଯାଞ୍ଚ୍_କରିବା(ftruncate(ଫାଇଲ, 6) == 0 && lseek(ଫାଇଲ, 2, SEEK_SET) == 2 && read(ଫାଇଲ, ଡାଟା, 4) == 4);
    ଯାଞ୍ଚ୍_କରିବା(!ଡାଟା[0] && !ଡାଟା[1] && !ଡାଟା[2] && !ଡାଟା[3]);
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, 2147483647, SEEK_SET) == 2147483647);
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ଯାଞ୍ଚ୍_କରିବା(write(ଫାଇଲ, "!", 1) == -1 && errno == EFBIG);
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, 0, SEEK_SET) == 0);
    ଯାଞ୍ଚ୍_କରିବା(read(ଫାଇଲ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ଯାଞ୍ଚ୍_କରିବା(read(ଫାଇଲ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ଯାଞ୍ଚ୍_କରିବା(write(ଫାଇଲ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ଯାଞ୍ଚ୍_କରିବା(read(ଫାଇଲ, ଡାଟା, (size_t)-1) == -1 && errno == EINVAL);
    ଯାଞ୍ଚ୍_କରିବା(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ଯାଞ୍ଚ୍_କରିବା(fstat(ଫାଇଲ, (void *)0x00100000) == -1 && errno == EFAULT);
    ଯାଞ୍ଚ୍_କରିବା(lseek(ଫାଇଲ, 0, SEEK_CUR) == 0);
    ଯାଞ୍ଚ୍_କରିବା(read(ଫାଇଲ, NULL, 0) == 0 && write(ଫାଇଲ, NULL, 0) == 0);
    ଯାଞ୍ଚ୍_କରିବା(ଅପସାରଣ_କରିବା_ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ("posix.txt") == 0);
    ଯାଞ୍ଚ୍_କରିବା(fstat(ଫାଇଲ, &ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1) == 0 && ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_nlink == 0 && ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ଯାଞ୍ଚ୍_କରିବା(새파일 == 5 && fstat(새파일, &ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1) == 0 && ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_size == 0);
    ଯାଞ୍ଚ୍_କରିବା(read(ଫାଇଲ, ଡାଟା, 2) == 2 && memcmp(ଡାଟା, "ab", 2) == 0);
    ଯାଞ୍ଚ୍_କରିବା(close(ଫାଇଲ) == 0 && close(복제) == 0 && close(새파일) == 0);
    ଯାଞ୍ଚ୍_କରିବା(close(새파일) == -1 && errno == EBADF);
    ଯାଞ୍ଚ୍_କରିବା(unlink("posix.txt") == 0);
    ଫାଇଲ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ଯାଞ୍ଚ୍_କରିବା(ଫାଇଲ == 3 && fcntl(ଫାଇଲ, F_GETFD) == 1);
    ଯାଞ୍ଚ୍_କରିବା(read(ଫାଇଲ, ଡାଟା, 1) == -1 && errno == EBADF);
    ଯାଞ୍ଚ୍_କରିବା(write(ଫାଇଲ, "keep", 4) == 4);
    for (int ଅନୁକ୍ରମଣିକା = 4; ଅନୁକ୍ରମଣିକା < 32; ଅନୁକ୍ରମଣିକା++) ଯାଞ୍ଚ୍_କରିବା(dup(ଫାଇଲ) == ଅନୁକ୍ରମଣିକା);
    ଯାଞ୍ଚ୍_କରିବା(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ଯାଞ୍ଚ୍_କରିବା(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ଯାଞ୍ଚ୍_କରିବା(fstat(ଫାଇଲ, &ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1) == 0 && ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_size == 4);
    for (int ଅନୁକ୍ରମଣିକା = 3; ଅନୁକ୍ରମଣିକା < 32; ଅନୁକ୍ରମଣିକା++) ଯାଞ୍ଚ୍_କରିବା(close(ଅନୁକ୍ରମଣିକା) == 0);
    ଯାଞ୍ଚ୍_କରିବା(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ଫାଇଲ = open("posix.txt", O_RDONLY);
    ଯାଞ୍ଚ୍_କରିବା(ଫାଇଲ == 3 && write(ଫାଇଲ, ଡାଟା, 1) == -1 && errno == EBADF);
    ଯାଞ୍ଚ୍_କରିବା(fcntl(ଫାଇଲ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ଯାଞ୍ଚ୍_କରିବା(close(8) == 0 && close(ଫାଇଲ) == 0 && unlink("posix.txt") == 0);
    ଯାଞ୍ଚ୍_କରିବା(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ଯାଞ୍ଚ୍_କରିବା(fstat(1, &ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1) == 0 && S_ISCHR(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.st_mode));
    ଯାଞ୍ଚ୍_କରିବା(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ଯାଞ୍ଚ୍_କରିବା(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ଠିକଣା; char ଠିକଣା_ପାଠ[16];
    ଯାଞ୍ଚ୍_କରିବା(inet_pton(AF_INET, "10.0.2.2", &ଠିକଣା) == 1 && ntohl(ଠିକଣା.s_addr) == 0x0a000202U);
    ଯାଞ୍ଚ୍_କରିବା(inet_ntop(AF_INET, &ଠିକଣା, ଠିକଣା_ପାଠ, sizeof ଠିକଣା_ପାଠ) == ଠିକଣା_ପାଠ && strcmp(ଠିକଣା_ପାଠ, "10.0.2.2") == 0);
    ଯାଞ୍ଚ୍_କରିବା(inet_pton(AF_INET, "256.0.0.1", &ଠିକଣା) == 0 && ntohl(ଠିକଣା.s_addr) == 0x0a000202U);
    ଯାଞ୍ଚ୍_କରିବା(inet_pton(AF_INET, "01.0.0.1", &ଠିକଣା) == 0);
    ଯାଞ୍ଚ୍_କରିବା(inet_ntop(AF_INET, &ଠିକଣା, ଠିକଣା_ପାଠ, 3) == NULL && errno == ENOSPC);
    ଯାଞ୍ଚ୍_କରିବା(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ନାମ[] = "slot0";
    for (int ଅନୁକ୍ରମଣିକା = 0; ଅନୁକ୍ରମଣିକା < 8; ଅନୁକ୍ରମଣିକା++) {
        ନାମ[4] = '0' + ଅନୁକ୍ରମଣିକା;
        int 열린파일 = open(ନାମ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ଯାଞ୍ଚ୍_କରିବା(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ଯାଞ୍ଚ୍_କରିବା(개수 > 0 && 개수 < 8);
    ଯାଞ୍ଚ୍_କରିବା(unlink("slot0") == 0);
    ଯାଞ୍ଚ୍_କରିବା(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ଯାଞ୍ଚ୍_କରିବା(close(보관[0]) == 0);
    ଫାଇଲ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ଯାଞ୍ଚ୍_କରିବା(ଫାଇଲ >= 0 && close(ଫାଇଲ) == 0 && unlink("held-slot") == 0);
    for (int ଅନୁକ୍ରମଣିକା = 1; ଅନୁକ୍ରମଣିକା < 개수; ଅନୁକ୍ରମଣିକା++) {
        ନାମ[4] = '0' + ଅନୁକ୍ରମଣିକା;
        ଯାଞ୍ଚ୍_କରିବା(close(보관[ଅନୁକ୍ରମଣିକା]) == 0 && unlink(ନାମ) == 0);
    }
    ଯାଞ୍ଚ୍_କରିବା(fsync(-1) == -1 && errno == EBADF);
    ଯାଞ୍ଚ୍_କରିବା(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
