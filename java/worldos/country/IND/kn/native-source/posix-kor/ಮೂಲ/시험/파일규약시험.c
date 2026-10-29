#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ಸ್ಥಿತಿ, int ಸಾಲು) {
    검사항목수++;
    if (!ಸ್ಥಿತಿ) {
        puts("POSIX CHECK FAILED");
        char ಅಂಕೆ_ಮೌಲ್ಯ[12]; int ಉದ್ದ_ಮೌಲ್ಯ = 0;
        do { ಅಂಕೆ_ಮೌಲ್ಯ[ಉದ್ದ_ಮೌಲ್ಯ++] = '0' + ಸಾಲು % 10; ಸಾಲು /= 10; } while (ಸಾಲು);
        while (ಉದ್ದ_ಮೌಲ್ಯ) putchar(ಅಂಕೆ_ಮೌಲ್ಯ[--ಉದ್ದ_ಮೌಲ್ಯ]);
        putchar('\n'); _exit(1);
    }
}
#define ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಸ್ಥಿತಿ) 검사((ಸ್ಥಿತಿ), __LINE__)

int main(int 인수개수, char **ವಾದ_ಪಟ್ಟಿ) {
    char ಡೇಟಾ[32]; struct stat ಸ್ಥಿತಿ_ಮೌಲ್ಯ;
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(인수개수 == 2 && strcmp(ವಾದ_ಪಟ್ಟಿ[1], "check") == 0 && ವಾದ_ಪಟ್ಟಿ[2] == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ರಚಿಸು_ಫೈಲ್("absent", ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ) == -1 && 오류번호 == ENOENT);
    int ಕಡತ = ರಚಿಸು_ಫೈಲ್("/posix.txt", ಓದು_ಬರೆ | 새파일만들기, 0640);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಕಡತ == 3);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಬರೆ_ಫೈಲ್_ಡೇಟಾ(ಕಡತ, "abcd", 4) == 4);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ರಚಿಸು_ಫೈಲ್("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(파일상태읽기(ಕಡತ, &ಸ್ಥಿತಿ_ಮೌಲ್ಯ) == 0 && ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_size == 4 && S_ISREG(ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_mode));
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು((ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_mode & 0777) == 0640 && ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_nlink == 1);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಸೀಕ್_ಫೈಲ್(ಕಡತ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ಕಡತ);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(복제 == 4);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(파일자료읽기(복제, ಡೇಟಾ, 2) == 2 && memcmp(ಡೇಟಾ, "ab", 2) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(파일자료읽기(ಕಡತ, ಡೇಟಾ, 2) == 2 && memcmp(ಡೇಟಾ, "cd", 2) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(파일자료읽기(ಕಡತ, ಡೇಟಾ, 1) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fcntl(ಕಡತ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ಕಡತ, F_GETFD) == 1);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fcntl(복제, F_GETFD) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(dup2(ಕಡತ, ಕಡತ) == ಕಡತ && fcntl(ಕಡತ, F_GETFD) == 1);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ಕಡತ, F_GETFL) & O_APPEND));
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ಕಡತ, 0, SEEK_CUR) == 5);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fcntl(ಕಡತ, F_SETFL, 0) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, 8, SEEK_SET) == 8 && write(ಕಡತ, "Z", 1) == 1);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(복제, 5, SEEK_SET) == 5 && read(ಕಡತ, ಡೇಟಾ, 4) == 4);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಡೇಟಾ[0] == 0 && ಡೇಟಾ[1] == 0 && ಡೇಟಾ[2] == 0 && ಡೇಟಾ[3] == 'Z');
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ftruncate(ಕಡತ, 2) == 0 && lseek(ಕಡತ, 0, SEEK_CUR) == 9);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ftruncate(ಕಡತ, 6) == 0 && lseek(ಕಡತ, 2, SEEK_SET) == 2 && read(ಕಡತ, ಡೇಟಾ, 4) == 4);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(!ಡೇಟಾ[0] && !ಡೇಟಾ[1] && !ಡೇಟಾ[2] && !ಡೇಟಾ[3]);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, 2147483647, SEEK_SET) == 2147483647);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(write(ಕಡತ, "!", 1) == -1 && errno == EFBIG);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, 0, SEEK_SET) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(read(ಕಡತ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(read(ಕಡತ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(write(ಕಡತ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(read(ಕಡತ, ಡೇಟಾ, (size_t)-1) == -1 && errno == EINVAL);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fstat(ಕಡತ, (void *)0x00100000) == -1 && errno == EFAULT);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(ಕಡತ, 0, SEEK_CUR) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(read(ಕಡತ, NULL, 0) == 0 && write(ಕಡತ, NULL, 0) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ತೆಗೆ_ಫೈಲ್_ನಮೂದು_ಹೆಸರು("posix.txt") == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fstat(ಕಡತ, &ಸ್ಥಿತಿ_ಮೌಲ್ಯ) == 0 && ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_nlink == 0 && ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(새파일 == 5 && fstat(새파일, &ಸ್ಥಿತಿ_ಮೌಲ್ಯ) == 0 && ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_size == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(read(ಕಡತ, ಡೇಟಾ, 2) == 2 && memcmp(ಡೇಟಾ, "ab", 2) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(close(ಕಡತ) == 0 && close(복제) == 0 && close(새파일) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(close(새파일) == -1 && errno == EBADF);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(unlink("posix.txt") == 0);
    ಕಡತ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಕಡತ == 3 && fcntl(ಕಡತ, F_GETFD) == 1);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(read(ಕಡತ, ಡೇಟಾ, 1) == -1 && errno == EBADF);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(write(ಕಡತ, "keep", 4) == 4);
    for (int ಪದಸೂಚಿ = 4; ಪದಸೂಚಿ < 32; ಪದಸೂಚಿ++) ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(dup(ಕಡತ) == ಪದಸೂಚಿ);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fstat(ಕಡತ, &ಸ್ಥಿತಿ_ಮೌಲ್ಯ) == 0 && ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_size == 4);
    for (int ಪದಸೂಚಿ = 3; ಪದಸೂಚಿ < 32; ಪದಸೂಚಿ++) ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(close(ಪದಸೂಚಿ) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ಕಡತ = open("posix.txt", O_RDONLY);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಕಡತ == 3 && write(ಕಡತ, ಡೇಟಾ, 1) == -1 && errno == EBADF);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fcntl(ಕಡತ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(close(8) == 0 && close(ಕಡತ) == 0 && unlink("posix.txt") == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fstat(1, &ಸ್ಥಿತಿ_ಮೌಲ್ಯ) == 0 && S_ISCHR(ಸ್ಥಿತಿ_ಮೌಲ್ಯ.st_mode));
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ಇಮೇಲ್; char ಇಮೇಲ್_ಪಠ್ಯ[16];
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(inet_pton(AF_INET, "10.0.2.2", &ಇಮೇಲ್) == 1 && ntohl(ಇಮೇಲ್.s_addr) == 0x0a000202U);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(inet_ntop(AF_INET, &ಇಮೇಲ್, ಇಮೇಲ್_ಪಠ್ಯ, sizeof ಇಮೇಲ್_ಪಠ್ಯ) == ಇಮೇಲ್_ಪಠ್ಯ && strcmp(ಇಮೇಲ್_ಪಠ್ಯ, "10.0.2.2") == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(inet_pton(AF_INET, "256.0.0.1", &ಇಮೇಲ್) == 0 && ntohl(ಇಮೇಲ್.s_addr) == 0x0a000202U);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(inet_pton(AF_INET, "01.0.0.1", &ಇಮೇಲ್) == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(inet_ntop(AF_INET, &ಇಮೇಲ್, ಇಮೇಲ್_ಪಠ್ಯ, 3) == NULL && errno == ENOSPC);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ಹೆಸರು[] = "slot0";
    for (int ಪದಸೂಚಿ = 0; ಪದಸೂಚಿ < 8; ಪದಸೂಚಿ++) {
        ಹೆಸರು[4] = '0' + ಪದಸೂಚಿ;
        int 열린파일 = open(ಹೆಸರು, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(개수 > 0 && 개수 < 8);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(unlink("slot0") == 0);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(close(보관[0]) == 0);
    ಕಡತ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(ಕಡತ >= 0 && close(ಕಡತ) == 0 && unlink("held-slot") == 0);
    for (int ಪದಸೂಚಿ = 1; ಪದಸೂಚಿ < 개수; ಪದಸೂಚಿ++) {
        ಹೆಸರು[4] = '0' + ಪದಸೂಚಿ;
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(close(보관[ಪದಸೂಚಿ]) == 0 && unlink(ಹೆಸರು) == 0);
    }
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fsync(-1) == -1 && errno == EBADF);
    ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
