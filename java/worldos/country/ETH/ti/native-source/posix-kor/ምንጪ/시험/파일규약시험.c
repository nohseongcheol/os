#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ኩነታት, int መስመር) {
    검사항목수++;
    if (!ኩነታት) {
        puts("POSIX CHECK FAILED");
        char ኣሃዝ_ዋጋ[12]; int ንውሓት_ዋጋ = 0;
        do { ኣሃዝ_ዋጋ[ንውሓት_ዋጋ++] = '0' + መስመር % 10; መስመር /= 10; } while (መስመር);
        while (ንውሓት_ዋጋ) putchar(ኣሃዝ_ዋጋ[--ንውሓት_ዋጋ]);
        putchar('\n'); _exit(1);
    }
}
#define ኣረጋግጽ(ኩነታት) 검사((ኩነታት), __LINE__)

int main(int 인수개수, char **ሓባሪ_ቁጽሪ_ዝርዝር) {
    char ሓበሬታ[32]; struct stat ደረጃ_ዋጋ;
    ኣረጋግጽ(인수개수 == 2 && strcmp(ሓባሪ_ቁጽሪ_ዝርዝር[1], "check") == 0 && ሓባሪ_ቁጽሪ_ዝርዝር[2] == 0);
    ኣረጋግጽ(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ኣረጋግጽ(ክፈት_ፋይል("absent", ንምንባብ_ጥራይ_ዋጋ) == -1 && 오류번호 == ENOENT);
    int ፋይል = ክፈት_ፋይል("/posix.txt", ኣንብብ_ጽሓፍ | 새파일만들기, 0640);
    ኣረጋግጽ(ፋይል == 3);
    ኣረጋግጽ(ጸሓፍ_ፋይል_ሓበሬታ(ፋይል, "abcd", 4) == 4);
    ኣረጋግጽ(ክፈት_ፋይል("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ኣረጋግጽ(파일상태읽기(ፋይል, &ደረጃ_ዋጋ) == 0 && ደረጃ_ዋጋ.st_size == 4 && S_ISREG(ደረጃ_ዋጋ.st_mode));
    ኣረጋግጽ((ደረጃ_ዋጋ.st_mode & 0777) == 0640 && ደረጃ_ዋጋ.st_nlink == 1);
    ኣረጋግጽ(መድለዪ_ፋይል(ፋይል, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ፋይል);
    ኣረጋግጽ(복제 == 4);
    ኣረጋግጽ(파일자료읽기(복제, ሓበሬታ, 2) == 2 && memcmp(ሓበሬታ, "ab", 2) == 0);
    ኣረጋግጽ(파일자료읽기(ፋይል, ሓበሬታ, 2) == 2 && memcmp(ሓበሬታ, "cd", 2) == 0);
    ኣረጋግጽ(파일자료읽기(ፋይል, ሓበሬታ, 1) == 0);
    ኣረጋግጽ(fcntl(ፋይል, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ፋይል, F_GETFD) == 1);
    ኣረጋግጽ(fcntl(복제, F_GETFD) == 0);
    ኣረጋግጽ(dup2(ፋይል, ፋይል) == ፋይል && fcntl(ፋይል, F_GETFD) == 1);
    ኣረጋግጽ(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ኣረጋግጽ(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ፋይል, F_GETFL) & O_APPEND));
    ኣረጋግጽ(lseek(ፋይል, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ፋይል, 0, SEEK_CUR) == 5);
    ኣረጋግጽ(fcntl(ፋይል, F_SETFL, 0) == 0);
    ኣረጋግጽ(lseek(ፋይል, 8, SEEK_SET) == 8 && write(ፋይል, "Z", 1) == 1);
    ኣረጋግጽ(lseek(복제, 5, SEEK_SET) == 5 && read(ፋይል, ሓበሬታ, 4) == 4);
    ኣረጋግጽ(ሓበሬታ[0] == 0 && ሓበሬታ[1] == 0 && ሓበሬታ[2] == 0 && ሓበሬታ[3] == 'Z');
    ኣረጋግጽ(ftruncate(ፋይል, 2) == 0 && lseek(ፋይል, 0, SEEK_CUR) == 9);
    ኣረጋግጽ(ftruncate(ፋይል, 6) == 0 && lseek(ፋይል, 2, SEEK_SET) == 2 && read(ፋይል, ሓበሬታ, 4) == 4);
    ኣረጋግጽ(!ሓበሬታ[0] && !ሓበሬታ[1] && !ሓበሬታ[2] && !ሓበሬታ[3]);
    ኣረጋግጽ(lseek(ፋይል, 2147483647, SEEK_SET) == 2147483647);
    ኣረጋግጽ(lseek(ፋይል, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ኣረጋግጽ(lseek(ፋይል, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ኣረጋግጽ(write(ፋይል, "!", 1) == -1 && errno == EFBIG);
    ኣረጋግጽ(lseek(ፋይል, 0, SEEK_SET) == 0);
    ኣረጋግጽ(read(ፋይል, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ኣረጋግጽ(read(ፋይል, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ኣረጋግጽ(write(ፋይል, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ኣረጋግጽ(read(ፋይል, ሓበሬታ, (size_t)-1) == -1 && errno == EINVAL);
    ኣረጋግጽ(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ኣረጋግጽ(fstat(ፋይል, (void *)0x00100000) == -1 && errno == EFAULT);
    ኣረጋግጽ(lseek(ፋይል, 0, SEEK_CUR) == 0);
    ኣረጋግጽ(read(ፋይል, NULL, 0) == 0 && write(ፋይል, NULL, 0) == 0);
    ኣረጋግጽ(ኣልግስ_ፋይል_ምእታው_ሽም("posix.txt") == 0);
    ኣረጋግጽ(fstat(ፋይል, &ደረጃ_ዋጋ) == 0 && ደረጃ_ዋጋ.st_nlink == 0 && ደረጃ_ዋጋ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ኣረጋግጽ(새파일 == 5 && fstat(새파일, &ደረጃ_ዋጋ) == 0 && ደረጃ_ዋጋ.st_size == 0);
    ኣረጋግጽ(read(ፋይል, ሓበሬታ, 2) == 2 && memcmp(ሓበሬታ, "ab", 2) == 0);
    ኣረጋግጽ(close(ፋይል) == 0 && close(복제) == 0 && close(새파일) == 0);
    ኣረጋግጽ(close(새파일) == -1 && errno == EBADF);
    ኣረጋግጽ(unlink("posix.txt") == 0);
    ፋይል = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ኣረጋግጽ(ፋይል == 3 && fcntl(ፋይል, F_GETFD) == 1);
    ኣረጋግጽ(read(ፋይል, ሓበሬታ, 1) == -1 && errno == EBADF);
    ኣረጋግጽ(write(ፋይል, "keep", 4) == 4);
    for (int መሐበሪ = 4; መሐበሪ < 32; መሐበሪ++) ኣረጋግጽ(dup(ፋይል) == መሐበሪ);
    ኣረጋግጽ(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ኣረጋግጽ(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ኣረጋግጽ(fstat(ፋይል, &ደረጃ_ዋጋ) == 0 && ደረጃ_ዋጋ.st_size == 4);
    for (int መሐበሪ = 3; መሐበሪ < 32; መሐበሪ++) ኣረጋግጽ(close(መሐበሪ) == 0);
    ኣረጋግጽ(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ፋይል = open("posix.txt", O_RDONLY);
    ኣረጋግጽ(ፋይል == 3 && write(ፋይል, ሓበሬታ, 1) == -1 && errno == EBADF);
    ኣረጋግጽ(fcntl(ፋይል, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ኣረጋግጽ(close(8) == 0 && close(ፋይል) == 0 && unlink("posix.txt") == 0);
    ኣረጋግጽ(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ኣረጋግጽ(fstat(1, &ደረጃ_ዋጋ) == 0 && S_ISCHR(ደረጃ_ዋጋ.st_mode));
    ኣረጋግጽ(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ኣረጋግጽ(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ኣድራሻ; char ኣድራሻ_ጽሑፍ[16];
    ኣረጋግጽ(inet_pton(AF_INET, "10.0.2.2", &ኣድራሻ) == 1 && ntohl(ኣድራሻ.s_addr) == 0x0a000202U);
    ኣረጋግጽ(inet_ntop(AF_INET, &ኣድራሻ, ኣድራሻ_ጽሑፍ, sizeof ኣድራሻ_ጽሑፍ) == ኣድራሻ_ጽሑፍ && strcmp(ኣድራሻ_ጽሑፍ, "10.0.2.2") == 0);
    ኣረጋግጽ(inet_pton(AF_INET, "256.0.0.1", &ኣድራሻ) == 0 && ntohl(ኣድራሻ.s_addr) == 0x0a000202U);
    ኣረጋግጽ(inet_pton(AF_INET, "01.0.0.1", &ኣድራሻ) == 0);
    ኣረጋግጽ(inet_ntop(AF_INET, &ኣድራሻ, ኣድራሻ_ጽሑፍ, 3) == NULL && errno == ENOSPC);
    ኣረጋግጽ(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ሽም[] = "slot0";
    for (int መሐበሪ = 0; መሐበሪ < 8; መሐበሪ++) {
        ሽም[4] = '0' + መሐበሪ;
        int 열린파일 = open(ሽም, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ኣረጋግጽ(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ኣረጋግጽ(개수 > 0 && 개수 < 8);
    ኣረጋግጽ(unlink("slot0") == 0);
    ኣረጋግጽ(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ኣረጋግጽ(close(보관[0]) == 0);
    ፋይል = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ኣረጋግጽ(ፋይል >= 0 && close(ፋይል) == 0 && unlink("held-slot") == 0);
    for (int መሐበሪ = 1; መሐበሪ < 개수; መሐበሪ++) {
        ሽም[4] = '0' + መሐበሪ;
        ኣረጋግጽ(close(보관[መሐበሪ]) == 0 && unlink(ሽም) == 0);
    }
    ኣረጋግጽ(fsync(-1) == -1 && errno == EBADF);
    ኣረጋግጽ(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
