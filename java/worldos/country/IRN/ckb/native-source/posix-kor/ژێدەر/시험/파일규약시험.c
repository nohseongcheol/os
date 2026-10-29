#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int دۆخ, int دێڕ) {
    검사항목수++;
    if (!دۆخ) {
        puts("POSIX CHECK FAILED");
        char ڕه_نووس_نرخ[12]; int درێژی_نرخ = 0;
        do { ڕه_نووس_نرخ[درێژی_نرخ++] = '0' + دێڕ % 10; دێڕ /= 10; } while (دێڕ);
        while (درێژی_نرخ) putchar(ڕه_نووس_نرخ[--درێژی_نرخ]);
        putchar('\n'); _exit(1);
    }
}
#define سەلماندن(دۆخ) 검사((دۆخ), __LINE__)

int main(int 인수개수, char **ئارگیومێنت_لیست) {
    char دەیتا[32]; struct stat دۆخ_نرخ;
    سەلماندن(인수개수 == 2 && strcmp(ئارگیومێنت_لیست[1], "check") == 0 && ئارگیومێنت_لیست[2] == 0);
    سەلماندن(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    سەلماندن(کردنەوە_فایل("absent", تەنیا_دەخوێنرێتەوە_نرخ) == -1 && 오류번호 == ENOENT);
    int فایل = کردنەوە_فایل("/posix.txt", خوێندن_نووسین | 새파일만들기, 0640);
    سەلماندن(فایل == 3);
    سەلماندن(ڕایت_کردن_فایل_دەیتا(فایل, "abcd", 4) == 4);
    سەلماندن(کردنەوە_فایل("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    سەلماندن(파일상태읽기(فایل, &دۆخ_نرخ) == 0 && دۆخ_نرخ.st_size == 4 && S_ISREG(دۆخ_نرخ.st_mode));
    سەلماندن((دۆخ_نرخ.st_mode & 0777) == 0640 && دۆخ_نرخ.st_nlink == 1);
    سەلماندن(گەڕان_فایل(فایل, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(فایل);
    سەلماندن(복제 == 4);
    سەلماندن(파일자료읽기(복제, دەیتا, 2) == 2 && memcmp(دەیتا, "ab", 2) == 0);
    سەلماندن(파일자료읽기(فایل, دەیتا, 2) == 2 && memcmp(دەیتا, "cd", 2) == 0);
    سەلماندن(파일자료읽기(فایل, دەیتا, 1) == 0);
    سەلماندن(fcntl(فایل, F_SETFD, FD_CLOEXEC) == 0 && fcntl(فایل, F_GETFD) == 1);
    سەلماندن(fcntl(복제, F_GETFD) == 0);
    سەلماندن(dup2(فایل, فایل) == فایل && fcntl(فایل, F_GETFD) == 1);
    سەلماندن(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    سەلماندن(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(فایل, F_GETFL) & O_APPEND));
    سەلماندن(lseek(فایل, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(فایل, 0, SEEK_CUR) == 5);
    سەلماندن(fcntl(فایل, F_SETFL, 0) == 0);
    سەلماندن(lseek(فایل, 8, SEEK_SET) == 8 && write(فایل, "Z", 1) == 1);
    سەلماندن(lseek(복제, 5, SEEK_SET) == 5 && read(فایل, دەیتا, 4) == 4);
    سەلماندن(دەیتا[0] == 0 && دەیتا[1] == 0 && دەیتا[2] == 0 && دەیتا[3] == 'Z');
    سەلماندن(ftruncate(فایل, 2) == 0 && lseek(فایل, 0, SEEK_CUR) == 9);
    سەلماندن(ftruncate(فایل, 6) == 0 && lseek(فایل, 2, SEEK_SET) == 2 && read(فایل, دەیتا, 4) == 4);
    سەلماندن(!دەیتا[0] && !دەیتا[1] && !دەیتا[2] && !دەیتا[3]);
    سەلماندن(lseek(فایل, 2147483647, SEEK_SET) == 2147483647);
    سەلماندن(lseek(فایل, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    سەلماندن(lseek(فایل, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    سەلماندن(write(فایل, "!", 1) == -1 && errno == EFBIG);
    سەلماندن(lseek(فایل, 0, SEEK_SET) == 0);
    سەلماندن(read(فایل, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    سەلماندن(read(فایل, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    سەلماندن(write(فایل, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    سەلماندن(read(فایل, دەیتا, (size_t)-1) == -1 && errno == EINVAL);
    سەلماندن(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    سەلماندن(fstat(فایل, (void *)0x00100000) == -1 && errno == EFAULT);
    سەلماندن(lseek(فایل, 0, SEEK_CUR) == 0);
    سەلماندن(read(فایل, NULL, 0) == 0 && write(فایل, NULL, 0) == 0);
    سەلماندن(لابردن_فایل_تێنووسین_ناو("posix.txt") == 0);
    سەلماندن(fstat(فایل, &دۆخ_نرخ) == 0 && دۆخ_نرخ.st_nlink == 0 && دۆخ_نرخ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    سەلماندن(새파일 == 5 && fstat(새파일, &دۆخ_نرخ) == 0 && دۆخ_نرخ.st_size == 0);
    سەلماندن(read(فایل, دەیتا, 2) == 2 && memcmp(دەیتا, "ab", 2) == 0);
    سەلماندن(close(فایل) == 0 && close(복제) == 0 && close(새파일) == 0);
    سەلماندن(close(새파일) == -1 && errno == EBADF);
    سەلماندن(unlink("posix.txt") == 0);
    فایل = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    سەلماندن(فایل == 3 && fcntl(فایل, F_GETFD) == 1);
    سەلماندن(read(فایل, دەیتا, 1) == -1 && errno == EBADF);
    سەلماندن(write(فایل, "keep", 4) == 4);
    for (int پێرست = 4; پێرست < 32; پێرست++) سەلماندن(dup(فایل) == پێرست);
    سەلماندن(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    سەلماندن(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    سەلماندن(fstat(فایل, &دۆخ_نرخ) == 0 && دۆخ_نرخ.st_size == 4);
    for (int پێرست = 3; پێرست < 32; پێرست++) سەلماندن(close(پێرست) == 0);
    سەلماندن(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    فایل = open("posix.txt", O_RDONLY);
    سەلماندن(فایل == 3 && write(فایل, دەیتا, 1) == -1 && errno == EBADF);
    سەلماندن(fcntl(فایل, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    سەلماندن(close(8) == 0 && close(فایل) == 0 && unlink("posix.txt") == 0);
    سەلماندن(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    سەلماندن(fstat(1, &دۆخ_نرخ) == 0 && S_ISCHR(دۆخ_نرخ.st_mode));
    سەلماندن(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    سەلماندن(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ناونیشان; char ناونیشان_دەق[16];
    سەلماندن(inet_pton(AF_INET, "10.0.2.2", &ناونیشان) == 1 && ntohl(ناونیشان.s_addr) == 0x0a000202U);
    سەلماندن(inet_ntop(AF_INET, &ناونیشان, ناونیشان_دەق, sizeof ناونیشان_دەق) == ناونیشان_دەق && strcmp(ناونیشان_دەق, "10.0.2.2") == 0);
    سەلماندن(inet_pton(AF_INET, "256.0.0.1", &ناونیشان) == 0 && ntohl(ناونیشان.s_addr) == 0x0a000202U);
    سەلماندن(inet_pton(AF_INET, "01.0.0.1", &ناونیشان) == 0);
    سەلماندن(inet_ntop(AF_INET, &ناونیشان, ناونیشان_دەق, 3) == NULL && errno == ENOSPC);
    سەلماندن(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ناو[] = "slot0";
    for (int پێرست = 0; پێرست < 8; پێرست++) {
        ناو[4] = '0' + پێرست;
        int 열린파일 = open(ناو, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { سەلماندن(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    سەلماندن(개수 > 0 && 개수 < 8);
    سەلماندن(unlink("slot0") == 0);
    سەلماندن(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    سەلماندن(close(보관[0]) == 0);
    فایل = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    سەلماندن(فایل >= 0 && close(فایل) == 0 && unlink("held-slot") == 0);
    for (int پێرست = 1; پێرست < 개수; پێرست++) {
        ناو[4] = '0' + پێرست;
        سەلماندن(close(보관[پێرست]) == 0 && unlink(ناو) == 0);
    }
    سەلماندن(fsync(-1) == -1 && errno == EBADF);
    سەلماندن(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
