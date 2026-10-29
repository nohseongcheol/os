#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ਸ਼ਰਤ, int ਲਾਈਨ) {
    검사항목수++;
    if (!ਸ਼ਰਤ) {
        puts("POSIX CHECK FAILED");
        char ਅੰਕ_ਕੀਮਤ[12]; int ਲੰਬਾਈ_ਕੀਮਤ = 0;
        do { ਅੰਕ_ਕੀਮਤ[ਲੰਬਾਈ_ਕੀਮਤ++] = '0' + ਲਾਈਨ % 10; ਲਾਈਨ /= 10; } while (ਲਾਈਨ);
        while (ਲੰਬਾਈ_ਕੀਮਤ) putchar(ਅੰਕ_ਕੀਮਤ[--ਲੰਬਾਈ_ਕੀਮਤ]);
        putchar('\n'); _exit(1);
    }
}
#define ਤਸਦੀਕ(ਸ਼ਰਤ) 검사((ਸ਼ਰਤ), __LINE__)

int main(int 인수개수, char **ਦਲੀਲ_ਸੂਚੀ) {
    char ਸਮੱਗਰੀ[32]; struct stat ਸਥਿਤੀ_ਕੀਮਤ;
    ਤਸਦੀਕ(인수개수 == 2 && strcmp(ਦਲੀਲ_ਸੂਚੀ[1], "check") == 0 && ਦਲੀਲ_ਸੂਚੀ[2] == 0);
    ਤਸਦੀਕ(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ਤਸਦੀਕ(ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ("absent", ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ) == -1 && 오류번호 == ENOENT);
    int ਫਾਇਲ = ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ("/posix.txt", ਪੜ੍ਹਨ_ਲਿਖਣ | 새파일만들기, 0640);
    ਤਸਦੀਕ(ਫਾਇਲ == 3);
    ਤਸਦੀਕ(ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(ਫਾਇਲ, "abcd", 4) == 4);
    ਤਸਦੀਕ(ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ਤਸਦੀਕ(파일상태읽기(ਫਾਇਲ, &ਸਥਿਤੀ_ਕੀਮਤ) == 0 && ਸਥਿਤੀ_ਕੀਮਤ.st_size == 4 && S_ISREG(ਸਥਿਤੀ_ਕੀਮਤ.st_mode));
    ਤਸਦੀਕ((ਸਥਿਤੀ_ਕੀਮਤ.st_mode & 0777) == 0640 && ਸਥਿਤੀ_ਕੀਮਤ.st_nlink == 1);
    ਤਸਦੀਕ(ਸੀਕ_ਲਿਖਤ_ਪੱਤਰ(ਫਾਇਲ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ਫਾਇਲ);
    ਤਸਦੀਕ(복제 == 4);
    ਤਸਦੀਕ(파일자료읽기(복제, ਸਮੱਗਰੀ, 2) == 2 && memcmp(ਸਮੱਗਰੀ, "ab", 2) == 0);
    ਤਸਦੀਕ(파일자료읽기(ਫਾਇਲ, ਸਮੱਗਰੀ, 2) == 2 && memcmp(ਸਮੱਗਰੀ, "cd", 2) == 0);
    ਤਸਦੀਕ(파일자료읽기(ਫਾਇਲ, ਸਮੱਗਰੀ, 1) == 0);
    ਤਸਦੀਕ(fcntl(ਫਾਇਲ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ਫਾਇਲ, F_GETFD) == 1);
    ਤਸਦੀਕ(fcntl(복제, F_GETFD) == 0);
    ਤਸਦੀਕ(dup2(ਫਾਇਲ, ਫਾਇਲ) == ਫਾਇਲ && fcntl(ਫਾਇਲ, F_GETFD) == 1);
    ਤਸਦੀਕ(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ਤਸਦੀਕ(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ਫਾਇਲ, F_GETFL) & O_APPEND));
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ਫਾਇਲ, 0, SEEK_CUR) == 5);
    ਤਸਦੀਕ(fcntl(ਫਾਇਲ, F_SETFL, 0) == 0);
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, 8, SEEK_SET) == 8 && write(ਫਾਇਲ, "Z", 1) == 1);
    ਤਸਦੀਕ(lseek(복제, 5, SEEK_SET) == 5 && read(ਫਾਇਲ, ਸਮੱਗਰੀ, 4) == 4);
    ਤਸਦੀਕ(ਸਮੱਗਰੀ[0] == 0 && ਸਮੱਗਰੀ[1] == 0 && ਸਮੱਗਰੀ[2] == 0 && ਸਮੱਗਰੀ[3] == 'Z');
    ਤਸਦੀਕ(ftruncate(ਫਾਇਲ, 2) == 0 && lseek(ਫਾਇਲ, 0, SEEK_CUR) == 9);
    ਤਸਦੀਕ(ftruncate(ਫਾਇਲ, 6) == 0 && lseek(ਫਾਇਲ, 2, SEEK_SET) == 2 && read(ਫਾਇਲ, ਸਮੱਗਰੀ, 4) == 4);
    ਤਸਦੀਕ(!ਸਮੱਗਰੀ[0] && !ਸਮੱਗਰੀ[1] && !ਸਮੱਗਰੀ[2] && !ਸਮੱਗਰੀ[3]);
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, 2147483647, SEEK_SET) == 2147483647);
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ਤਸਦੀਕ(write(ਫਾਇਲ, "!", 1) == -1 && errno == EFBIG);
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, 0, SEEK_SET) == 0);
    ਤਸਦੀਕ(read(ਫਾਇਲ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ਤਸਦੀਕ(read(ਫਾਇਲ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ਤਸਦੀਕ(write(ਫਾਇਲ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ਤਸਦੀਕ(read(ਫਾਇਲ, ਸਮੱਗਰੀ, (size_t)-1) == -1 && errno == EINVAL);
    ਤਸਦੀਕ(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ਤਸਦੀਕ(fstat(ਫਾਇਲ, (void *)0x00100000) == -1 && errno == EFAULT);
    ਤਸਦੀਕ(lseek(ਫਾਇਲ, 0, SEEK_CUR) == 0);
    ਤਸਦੀਕ(read(ਫਾਇਲ, NULL, 0) == 0 && write(ਫਾਇਲ, NULL, 0) == 0);
    ਤਸਦੀਕ(ਹਟਾਉਣਾ_ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ("posix.txt") == 0);
    ਤਸਦੀਕ(fstat(ਫਾਇਲ, &ਸਥਿਤੀ_ਕੀਮਤ) == 0 && ਸਥਿਤੀ_ਕੀਮਤ.st_nlink == 0 && ਸਥਿਤੀ_ਕੀਮਤ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ਤਸਦੀਕ(새파일 == 5 && fstat(새파일, &ਸਥਿਤੀ_ਕੀਮਤ) == 0 && ਸਥਿਤੀ_ਕੀਮਤ.st_size == 0);
    ਤਸਦੀਕ(read(ਫਾਇਲ, ਸਮੱਗਰੀ, 2) == 2 && memcmp(ਸਮੱਗਰੀ, "ab", 2) == 0);
    ਤਸਦੀਕ(close(ਫਾਇਲ) == 0 && close(복제) == 0 && close(새파일) == 0);
    ਤਸਦੀਕ(close(새파일) == -1 && errno == EBADF);
    ਤਸਦੀਕ(unlink("posix.txt") == 0);
    ਫਾਇਲ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ਤਸਦੀਕ(ਫਾਇਲ == 3 && fcntl(ਫਾਇਲ, F_GETFD) == 1);
    ਤਸਦੀਕ(read(ਫਾਇਲ, ਸਮੱਗਰੀ, 1) == -1 && errno == EBADF);
    ਤਸਦੀਕ(write(ਫਾਇਲ, "keep", 4) == 4);
    for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 4; ਅਨੁਕ੍ਰਮਣਿਕਾ < 32; ਅਨੁਕ੍ਰਮਣਿਕਾ++) ਤਸਦੀਕ(dup(ਫਾਇਲ) == ਅਨੁਕ੍ਰਮਣਿਕਾ);
    ਤਸਦੀਕ(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ਤਸਦੀਕ(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ਤਸਦੀਕ(fstat(ਫਾਇਲ, &ਸਥਿਤੀ_ਕੀਮਤ) == 0 && ਸਥਿਤੀ_ਕੀਮਤ.st_size == 4);
    for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 3; ਅਨੁਕ੍ਰਮਣਿਕਾ < 32; ਅਨੁਕ੍ਰਮਣਿਕਾ++) ਤਸਦੀਕ(close(ਅਨੁਕ੍ਰਮਣਿਕਾ) == 0);
    ਤਸਦੀਕ(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ਫਾਇਲ = open("posix.txt", O_RDONLY);
    ਤਸਦੀਕ(ਫਾਇਲ == 3 && write(ਫਾਇਲ, ਸਮੱਗਰੀ, 1) == -1 && errno == EBADF);
    ਤਸਦੀਕ(fcntl(ਫਾਇਲ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ਤਸਦੀਕ(close(8) == 0 && close(ਫਾਇਲ) == 0 && unlink("posix.txt") == 0);
    ਤਸਦੀਕ(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ਤਸਦੀਕ(fstat(1, &ਸਥਿਤੀ_ਕੀਮਤ) == 0 && S_ISCHR(ਸਥਿਤੀ_ਕੀਮਤ.st_mode));
    ਤਸਦੀਕ(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ਤਸਦੀਕ(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ਪਤਾ; char ਪਤਾ_ਪਾਠ[16];
    ਤਸਦੀਕ(inet_pton(AF_INET, "10.0.2.2", &ਪਤਾ) == 1 && ntohl(ਪਤਾ.s_addr) == 0x0a000202U);
    ਤਸਦੀਕ(inet_ntop(AF_INET, &ਪਤਾ, ਪਤਾ_ਪਾਠ, sizeof ਪਤਾ_ਪਾਠ) == ਪਤਾ_ਪਾਠ && strcmp(ਪਤਾ_ਪਾਠ, "10.0.2.2") == 0);
    ਤਸਦੀਕ(inet_pton(AF_INET, "256.0.0.1", &ਪਤਾ) == 0 && ntohl(ਪਤਾ.s_addr) == 0x0a000202U);
    ਤਸਦੀਕ(inet_pton(AF_INET, "01.0.0.1", &ਪਤਾ) == 0);
    ਤਸਦੀਕ(inet_ntop(AF_INET, &ਪਤਾ, ਪਤਾ_ਪਾਠ, 3) == NULL && errno == ENOSPC);
    ਤਸਦੀਕ(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ਨਾਂ[] = "slot0";
    for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਅਨੁਕ੍ਰਮਣਿਕਾ < 8; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
        ਨਾਂ[4] = '0' + ਅਨੁਕ੍ਰਮਣਿਕਾ;
        int 열린파일 = open(ਨਾਂ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ਤਸਦੀਕ(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ਤਸਦੀਕ(개수 > 0 && 개수 < 8);
    ਤਸਦੀਕ(unlink("slot0") == 0);
    ਤਸਦੀਕ(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ਤਸਦੀਕ(close(보관[0]) == 0);
    ਫਾਇਲ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ਤਸਦੀਕ(ਫਾਇਲ >= 0 && close(ਫਾਇਲ) == 0 && unlink("held-slot") == 0);
    for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 1; ਅਨੁਕ੍ਰਮਣਿਕਾ < 개수; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
        ਨਾਂ[4] = '0' + ਅਨੁਕ੍ਰਮਣਿਕਾ;
        ਤਸਦੀਕ(close(보관[ਅਨੁਕ੍ਰਮਣਿਕਾ]) == 0 && unlink(ਨਾਂ) == 0);
    }
    ਤਸਦੀਕ(fsync(-1) == -1 && errno == EBADF);
    ਤਸਦੀਕ(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
