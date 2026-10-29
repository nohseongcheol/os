#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int શરત, int લાઇન) {
    검사항목수++;
    if (!શરત) {
        puts("POSIX CHECK FAILED");
        char અંક_મૂલ્ય[12]; int લંબાઈ_મૂલ્ય = 0;
        do { અંક_મૂલ્ય[લંબાઈ_મૂલ્ય++] = '0' + લાઇન % 10; લાઇન /= 10; } while (લાઇન);
        while (લંબાઈ_મૂલ્ય) putchar(અંક_મૂલ્ય[--લંબાઈ_મૂલ્ય]);
        putchar('\n'); _exit(1);
    }
}
#define ચકાસવું(શરત) 검사((શરત), __LINE__)

int main(int 인수개수, char **દલીલ_સૂચી) {
    char ડેટા[32]; struct stat સ્થિતિ_મૂલ્ય_e10195a1;
    ચકાસવું(인수개수 == 2 && strcmp(દલીલ_સૂચી[1], "check") == 0 && દલીલ_સૂચી[2] == 0);
    ચકાસવું(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ચકાસવું(બનાવો_ફાઇલ("absent", ફક્ત_વાંચવા_માટે_મૂલ્ય) == -1 && 오류번호 == ENOENT);
    int ફાઈલ = બનાવો_ફાઇલ("/posix.txt", વાંચન_લેખન | 새파일만들기, 0640);
    ચકાસવું(ફાઈલ == 3);
    ચકાસવું(લખો_ફાઇલ_ડેટા(ફાઈલ, "abcd", 4) == 4);
    ચકાસવું(બનાવો_ફાઇલ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ચકાસવું(파일상태읽기(ફાઈલ, &સ્થિતિ_મૂલ્ય_e10195a1) == 0 && સ્થિતિ_મૂલ્ય_e10195a1.st_size == 4 && S_ISREG(સ્થિતિ_મૂલ્ય_e10195a1.st_mode));
    ચકાસવું((સ્થિતિ_મૂલ્ય_e10195a1.st_mode & 0777) == 0640 && સ્થિતિ_મૂલ્ય_e10195a1.st_nlink == 1);
    ચકાસવું(સીક_ફાઇલ(ફાઈલ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ફાઈલ);
    ચકાસવું(복제 == 4);
    ચકાસવું(파일자료읽기(복제, ડેટા, 2) == 2 && memcmp(ડેટા, "ab", 2) == 0);
    ચકાસવું(파일자료읽기(ફાઈલ, ડેટા, 2) == 2 && memcmp(ડેટા, "cd", 2) == 0);
    ચકાસવું(파일자료읽기(ફાઈલ, ડેટા, 1) == 0);
    ચકાસવું(fcntl(ફાઈલ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ફાઈલ, F_GETFD) == 1);
    ચકાસવું(fcntl(복제, F_GETFD) == 0);
    ચકાસવું(dup2(ફાઈલ, ફાઈલ) == ફાઈલ && fcntl(ફાઈલ, F_GETFD) == 1);
    ચકાસવું(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ચકાસવું(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ફાઈલ, F_GETFL) & O_APPEND));
    ચકાસવું(lseek(ફાઈલ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ફાઈલ, 0, SEEK_CUR) == 5);
    ચકાસવું(fcntl(ફાઈલ, F_SETFL, 0) == 0);
    ચકાસવું(lseek(ફાઈલ, 8, SEEK_SET) == 8 && write(ફાઈલ, "Z", 1) == 1);
    ચકાસવું(lseek(복제, 5, SEEK_SET) == 5 && read(ફાઈલ, ડેટા, 4) == 4);
    ચકાસવું(ડેટા[0] == 0 && ડેટા[1] == 0 && ડેટા[2] == 0 && ડેટા[3] == 'Z');
    ચકાસવું(ftruncate(ફાઈલ, 2) == 0 && lseek(ફાઈલ, 0, SEEK_CUR) == 9);
    ચકાસવું(ftruncate(ફાઈલ, 6) == 0 && lseek(ફાઈલ, 2, SEEK_SET) == 2 && read(ફાઈલ, ડેટા, 4) == 4);
    ચકાસવું(!ડેટા[0] && !ડેટા[1] && !ડેટા[2] && !ડેટા[3]);
    ચકાસવું(lseek(ફાઈલ, 2147483647, SEEK_SET) == 2147483647);
    ચકાસવું(lseek(ફાઈલ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ચકાસવું(lseek(ફાઈલ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ચકાસવું(write(ફાઈલ, "!", 1) == -1 && errno == EFBIG);
    ચકાસવું(lseek(ફાઈલ, 0, SEEK_SET) == 0);
    ચકાસવું(read(ફાઈલ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ચકાસવું(read(ફાઈલ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ચકાસવું(write(ફાઈલ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ચકાસવું(read(ફાઈલ, ડેટા, (size_t)-1) == -1 && errno == EINVAL);
    ચકાસવું(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ચકાસવું(fstat(ફાઈલ, (void *)0x00100000) == -1 && errno == EFAULT);
    ચકાસવું(lseek(ફાઈલ, 0, SEEK_CUR) == 0);
    ચકાસવું(read(ફાઈલ, NULL, 0) == 0 && write(ફાઈલ, NULL, 0) == 0);
    ચકાસવું(કાઢી_નાંખો_ફાઇલ_પ્રવેશ_નામ("posix.txt") == 0);
    ચકાસવું(fstat(ફાઈલ, &સ્થિતિ_મૂલ્ય_e10195a1) == 0 && સ્થિતિ_મૂલ્ય_e10195a1.st_nlink == 0 && સ્થિતિ_મૂલ્ય_e10195a1.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ચકાસવું(새파일 == 5 && fstat(새파일, &સ્થિતિ_મૂલ્ય_e10195a1) == 0 && સ્થિતિ_મૂલ્ય_e10195a1.st_size == 0);
    ચકાસવું(read(ફાઈલ, ડેટા, 2) == 2 && memcmp(ડેટા, "ab", 2) == 0);
    ચકાસવું(close(ફાઈલ) == 0 && close(복제) == 0 && close(새파일) == 0);
    ચકાસવું(close(새파일) == -1 && errno == EBADF);
    ચકાસવું(unlink("posix.txt") == 0);
    ફાઈલ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ચકાસવું(ફાઈલ == 3 && fcntl(ફાઈલ, F_GETFD) == 1);
    ચકાસવું(read(ફાઈલ, ડેટા, 1) == -1 && errno == EBADF);
    ચકાસવું(write(ફાઈલ, "keep", 4) == 4);
    for (int અનુક્રમણિકા = 4; અનુક્રમણિકા < 32; અનુક્રમણિકા++) ચકાસવું(dup(ફાઈલ) == અનુક્રમણિકા);
    ચકાસવું(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ચકાસવું(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ચકાસવું(fstat(ફાઈલ, &સ્થિતિ_મૂલ્ય_e10195a1) == 0 && સ્થિતિ_મૂલ્ય_e10195a1.st_size == 4);
    for (int અનુક્રમણિકા = 3; અનુક્રમણિકા < 32; અનુક્રમણિકા++) ચકાસવું(close(અનુક્રમણિકા) == 0);
    ચકાસવું(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ફાઈલ = open("posix.txt", O_RDONLY);
    ચકાસવું(ફાઈલ == 3 && write(ફાઈલ, ડેટા, 1) == -1 && errno == EBADF);
    ચકાસવું(fcntl(ફાઈલ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ચકાસવું(close(8) == 0 && close(ફાઈલ) == 0 && unlink("posix.txt") == 0);
    ચકાસવું(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ચકાસવું(fstat(1, &સ્થિતિ_મૂલ્ય_e10195a1) == 0 && S_ISCHR(સ્થિતિ_મૂલ્ય_e10195a1.st_mode));
    ચકાસવું(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ચકાસવું(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr સરનામું; char સરનામું_પાઠ[16];
    ચકાસવું(inet_pton(AF_INET, "10.0.2.2", &સરનામું) == 1 && ntohl(સરનામું.s_addr) == 0x0a000202U);
    ચકાસવું(inet_ntop(AF_INET, &સરનામું, સરનામું_પાઠ, sizeof સરનામું_પાઠ) == સરનામું_પાઠ && strcmp(સરનામું_પાઠ, "10.0.2.2") == 0);
    ચકાસવું(inet_pton(AF_INET, "256.0.0.1", &સરનામું) == 0 && ntohl(સરનામું.s_addr) == 0x0a000202U);
    ચકાસવું(inet_pton(AF_INET, "01.0.0.1", &સરનામું) == 0);
    ચકાસવું(inet_ntop(AF_INET, &સરનામું, સરનામું_પાઠ, 3) == NULL && errno == ENOSPC);
    ચકાસવું(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char નામ[] = "slot0";
    for (int અનુક્રમણિકા = 0; અનુક્રમણિકા < 8; અનુક્રમણિકા++) {
        નામ[4] = '0' + અનુક્રમણિકા;
        int 열린파일 = open(નામ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ચકાસવું(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ચકાસવું(개수 > 0 && 개수 < 8);
    ચકાસવું(unlink("slot0") == 0);
    ચકાસવું(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ચકાસવું(close(보관[0]) == 0);
    ફાઈલ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ચકાસવું(ફાઈલ >= 0 && close(ફાઈલ) == 0 && unlink("held-slot") == 0);
    for (int અનુક્રમણિકા = 1; અનુક્રમણિકા < 개수; અનુક્રમણિકા++) {
        નામ[4] = '0' + અનુક્રમણિકા;
        ચકાસવું(close(보관[અનુક્રમણિકા]) == 0 && unlink(નામ) == 0);
    }
    ચકાસવું(fsync(-1) == -1 && errno == EBADF);
    ચકાસવું(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
