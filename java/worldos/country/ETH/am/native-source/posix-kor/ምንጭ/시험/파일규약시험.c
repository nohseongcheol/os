#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ሁኔታ, int መስመር) {
    검사항목수++;
    if (!ሁኔታ) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int ርዝመት_እሴት = 0;
        do { 숫자[ርዝመት_እሴት++] = '0' + መስመር % 10; መስመር /= 10; } while (መስመር);
        while (ርዝመት_እሴት) putchar(숫자[--ርዝመት_እሴት]);
        putchar('\n'); _exit(1);
    }
}
#define አረጋግጥ(ሁኔታ) 검사((ሁኔታ), __LINE__)

int main(int 인수개수, char **ነጋሪ_እሴት_ዝርዝር) {
    char ውሂብ[32]; struct stat ዞን_እሴት;
    አረጋግጥ(인수개수 == 2 && strcmp(ነጋሪ_እሴት_ዝርዝር[1], "check") == 0 && ነጋሪ_እሴት_ዝርዝር[2] == 0);
    አረጋግጥ(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    አረጋግጥ(ክፈት_ፋይል("absent", ተነባቢ_ብቻ_እሴት) == -1 && 오류번호 == ENOENT);
    int ፋይል = ክፈት_ፋይል("/posix.txt", ተነባቢ_የሚጻፍበት | 새파일만들기, 0640);
    አረጋግጥ(ፋይል == 3);
    አረጋግጥ(ጻፍ_ፋይል_ውሂብ(ፋይል, "abcd", 4) == 4);
    አረጋግጥ(ክፈት_ፋይል("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    አረጋግጥ(파일상태읽기(ፋይል, &ዞን_እሴት) == 0 && ዞን_እሴት.st_size == 4 && S_ISREG(ዞን_እሴት.st_mode));
    አረጋግጥ((ዞን_እሴት.st_mode & 0777) == 0640 && ዞን_እሴት.st_nlink == 1);
    አረጋግጥ(ፈልግ_ፋይል(ፋይል, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ፋይል);
    አረጋግጥ(복제 == 4);
    አረጋግጥ(파일자료읽기(복제, ውሂብ, 2) == 2 && memcmp(ውሂብ, "ab", 2) == 0);
    አረጋግጥ(파일자료읽기(ፋይል, ውሂብ, 2) == 2 && memcmp(ውሂብ, "cd", 2) == 0);
    አረጋግጥ(파일자료읽기(ፋይል, ውሂብ, 1) == 0);
    አረጋግጥ(fcntl(ፋይል, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ፋይል, F_GETFD) == 1);
    አረጋግጥ(fcntl(복제, F_GETFD) == 0);
    አረጋግጥ(dup2(ፋይል, ፋይል) == ፋይል && fcntl(ፋይል, F_GETFD) == 1);
    አረጋግጥ(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    አረጋግጥ(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ፋይል, F_GETFL) & O_APPEND));
    አረጋግጥ(lseek(ፋይል, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ፋይል, 0, SEEK_CUR) == 5);
    አረጋግጥ(fcntl(ፋይል, F_SETFL, 0) == 0);
    አረጋግጥ(lseek(ፋይል, 8, SEEK_SET) == 8 && write(ፋይል, "Z", 1) == 1);
    አረጋግጥ(lseek(복제, 5, SEEK_SET) == 5 && read(ፋይል, ውሂብ, 4) == 4);
    አረጋግጥ(ውሂብ[0] == 0 && ውሂብ[1] == 0 && ውሂብ[2] == 0 && ውሂብ[3] == 'Z');
    አረጋግጥ(ftruncate(ፋይል, 2) == 0 && lseek(ፋይል, 0, SEEK_CUR) == 9);
    አረጋግጥ(ftruncate(ፋይል, 6) == 0 && lseek(ፋይል, 2, SEEK_SET) == 2 && read(ፋይል, ውሂብ, 4) == 4);
    አረጋግጥ(!ውሂብ[0] && !ውሂብ[1] && !ውሂብ[2] && !ውሂብ[3]);
    አረጋግጥ(lseek(ፋይል, 2147483647, SEEK_SET) == 2147483647);
    አረጋግጥ(lseek(ፋይል, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    አረጋግጥ(lseek(ፋይል, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    አረጋግጥ(write(ፋይል, "!", 1) == -1 && errno == EFBIG);
    አረጋግጥ(lseek(ፋይል, 0, SEEK_SET) == 0);
    አረጋግጥ(read(ፋይል, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    አረጋግጥ(read(ፋይል, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    አረጋግጥ(write(ፋይል, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    አረጋግጥ(read(ፋይል, ውሂብ, (size_t)-1) == -1 && errno == EINVAL);
    አረጋግጥ(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    አረጋግጥ(fstat(ፋይል, (void *)0x00100000) == -1 && errno == EFAULT);
    አረጋግጥ(lseek(ፋይል, 0, SEEK_CUR) == 0);
    አረጋግጥ(read(ፋይል, NULL, 0) == 0 && write(ፋይል, NULL, 0) == 0);
    አረጋግጥ(አስወግድ_ፋይል_ምዝግብ_ስም("posix.txt") == 0);
    አረጋግጥ(fstat(ፋይል, &ዞን_እሴት) == 0 && ዞን_እሴት.st_nlink == 0 && ዞን_እሴት.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    አረጋግጥ(새파일 == 5 && fstat(새파일, &ዞን_እሴት) == 0 && ዞን_እሴት.st_size == 0);
    አረጋግጥ(read(ፋይል, ውሂብ, 2) == 2 && memcmp(ውሂብ, "ab", 2) == 0);
    አረጋግጥ(close(ፋይል) == 0 && close(복제) == 0 && close(새파일) == 0);
    አረጋግጥ(close(새파일) == -1 && errno == EBADF);
    አረጋግጥ(unlink("posix.txt") == 0);
    ፋይል = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    አረጋግጥ(ፋይል == 3 && fcntl(ፋይል, F_GETFD) == 1);
    አረጋግጥ(read(ፋይል, ውሂብ, 1) == -1 && errno == EBADF);
    አረጋግጥ(write(ፋይል, "keep", 4) == 4);
    for (int መረጃ_ጠቆመ = 4; መረጃ_ጠቆመ < 32; መረጃ_ጠቆመ++) አረጋግጥ(dup(ፋይል) == መረጃ_ጠቆመ);
    አረጋግጥ(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    አረጋግጥ(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    አረጋግጥ(fstat(ፋይል, &ዞን_እሴት) == 0 && ዞን_እሴት.st_size == 4);
    for (int መረጃ_ጠቆመ = 3; መረጃ_ጠቆመ < 32; መረጃ_ጠቆመ++) አረጋግጥ(close(መረጃ_ጠቆመ) == 0);
    አረጋግጥ(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ፋይል = open("posix.txt", O_RDONLY);
    አረጋግጥ(ፋይል == 3 && write(ፋይል, ውሂብ, 1) == -1 && errno == EBADF);
    አረጋግጥ(fcntl(ፋይል, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    አረጋግጥ(close(8) == 0 && close(ፋይል) == 0 && unlink("posix.txt") == 0);
    አረጋግጥ(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    አረጋግጥ(fstat(1, &ዞን_እሴት) == 0 && S_ISCHR(ዞን_እሴት.st_mode));
    አረጋግጥ(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    አረጋግጥ(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr አድራሻ; char አድራሻ_ጽሁፍ[16];
    አረጋግጥ(inet_pton(AF_INET, "10.0.2.2", &አድራሻ) == 1 && ntohl(አድራሻ.s_addr) == 0x0a000202U);
    አረጋግጥ(inet_ntop(AF_INET, &አድራሻ, አድራሻ_ጽሁፍ, sizeof አድራሻ_ጽሁፍ) == አድራሻ_ጽሁፍ && strcmp(አድራሻ_ጽሁፍ, "10.0.2.2") == 0);
    አረጋግጥ(inet_pton(AF_INET, "256.0.0.1", &አድራሻ) == 0 && ntohl(አድራሻ.s_addr) == 0x0a000202U);
    አረጋግጥ(inet_pton(AF_INET, "01.0.0.1", &አድራሻ) == 0);
    አረጋግጥ(inet_ntop(AF_INET, &አድራሻ, አድራሻ_ጽሁፍ, 3) == NULL && errno == ENOSPC);
    አረጋግጥ(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ስም[] = "slot0";
    for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < 8; መረጃ_ጠቆመ++) {
        ስም[4] = '0' + መረጃ_ጠቆመ;
        int 열린파일 = open(ስም, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { አረጋግጥ(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    አረጋግጥ(개수 > 0 && 개수 < 8);
    አረጋግጥ(unlink("slot0") == 0);
    አረጋግጥ(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    አረጋግጥ(close(보관[0]) == 0);
    ፋይል = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    አረጋግጥ(ፋይል >= 0 && close(ፋይል) == 0 && unlink("held-slot") == 0);
    for (int መረጃ_ጠቆመ = 1; መረጃ_ጠቆመ < 개수; መረጃ_ጠቆመ++) {
        ስም[4] = '0' + መረጃ_ጠቆመ;
        አረጋግጥ(close(보관[መረጃ_ጠቆመ]) == 0 && unlink(ስም) == 0);
    }
    አረጋግጥ(fsync(-1) == -1 && errno == EBADF);
    አረጋግጥ(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
