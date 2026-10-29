#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int syarat, int baris) {
    검사항목수++;
    if (!syarat) {
        puts("POSIX CHECK FAILED");
        char digit_VALUE[12]; int kepanjangan_VALUE = 0;
        do { digit_VALUE[kepanjangan_VALUE++] = '0' + baris % 10; baris /= 10; } while (baris);
        while (kepanjangan_VALUE) putchar(digit_VALUE[--kepanjangan_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define tentu_sahkan(syarat) 검사((syarat), __LINE__)

int main(int 인수개수, char **argumen_Senarai) {
    char data[32]; struct stat status_VALUE;
    tentu_sahkan(인수개수 == 2 && strcmp(argumen_Senarai[1], "check") == 0 && argumen_Senarai[2] == 0);
    tentu_sahkan(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    tentu_sahkan(buka_fail("absent", baca_sahaja_VALUE) == -1 && 오류번호 == ENOENT);
    int Fail = buka_fail("/posix.txt", baca_tulis | 새파일만들기, 0640);
    tentu_sahkan(Fail == 3);
    tentu_sahkan(tulis_fail_data(Fail, "abcd", 4) == 4);
    tentu_sahkan(buka_fail("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    tentu_sahkan(파일상태읽기(Fail, &status_VALUE) == 0 && status_VALUE.st_size == 4 && S_ISREG(status_VALUE.st_mode));
    tentu_sahkan((status_VALUE.st_mode & 0777) == 0640 && status_VALUE.st_nlink == 1);
    tentu_sahkan(cari_fail(Fail, 0, 처음기준) == 0);
    int klon_VALUE = 파일서술자복제(Fail);
    tentu_sahkan(klon_VALUE == 4);
    tentu_sahkan(파일자료읽기(klon_VALUE, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    tentu_sahkan(파일자료읽기(Fail, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    tentu_sahkan(파일자료읽기(Fail, data, 1) == 0);
    tentu_sahkan(fcntl(Fail, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fail, F_GETFD) == 1);
    tentu_sahkan(fcntl(klon_VALUE, F_GETFD) == 0);
    tentu_sahkan(dup2(Fail, Fail) == Fail && fcntl(Fail, F_GETFD) == 1);
    tentu_sahkan(dup2(-1, klon_VALUE) == -1 && errno == EBADF && fcntl(klon_VALUE, F_GETFD) == 0);
    tentu_sahkan(fcntl(klon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(Fail, F_GETFL) & O_APPEND));
    tentu_sahkan(lseek(Fail, 0, SEEK_SET) == 0 && write(klon_VALUE, "e", 1) == 1 && lseek(Fail, 0, SEEK_CUR) == 5);
    tentu_sahkan(fcntl(Fail, F_SETFL, 0) == 0);
    tentu_sahkan(lseek(Fail, 8, SEEK_SET) == 8 && write(Fail, "Z", 1) == 1);
    tentu_sahkan(lseek(klon_VALUE, 5, SEEK_SET) == 5 && read(Fail, data, 4) == 4);
    tentu_sahkan(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    tentu_sahkan(ftruncate(Fail, 2) == 0 && lseek(Fail, 0, SEEK_CUR) == 9);
    tentu_sahkan(ftruncate(Fail, 6) == 0 && lseek(Fail, 2, SEEK_SET) == 2 && read(Fail, data, 4) == 4);
    tentu_sahkan(!data[0] && !data[1] && !data[2] && !data[3]);
    tentu_sahkan(lseek(Fail, 2147483647, SEEK_SET) == 2147483647);
    tentu_sahkan(lseek(Fail, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    tentu_sahkan(lseek(Fail, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    tentu_sahkan(write(Fail, "!", 1) == -1 && errno == EFBIG);
    tentu_sahkan(lseek(Fail, 0, SEEK_SET) == 0);
    tentu_sahkan(read(Fail, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tentu_sahkan(read(Fail, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    tentu_sahkan(write(Fail, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tentu_sahkan(read(Fail, data, (size_t)-1) == -1 && errno == EINVAL);
    tentu_sahkan(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    tentu_sahkan(fstat(Fail, (void *)0x00100000) == -1 && errno == EFAULT);
    tentu_sahkan(lseek(Fail, 0, SEEK_CUR) == 0);
    tentu_sahkan(read(Fail, NULL, 0) == 0 && write(Fail, NULL, 0) == 0);
    tentu_sahkan(alih_keluar_fail_pemasukan_nama("posix.txt") == 0);
    tentu_sahkan(fstat(Fail, &status_VALUE) == 0 && status_VALUE.st_nlink == 0 && status_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    tentu_sahkan(새파일 == 5 && fstat(새파일, &status_VALUE) == 0 && status_VALUE.st_size == 0);
    tentu_sahkan(read(Fail, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    tentu_sahkan(close(Fail) == 0 && close(klon_VALUE) == 0 && close(새파일) == 0);
    tentu_sahkan(close(새파일) == -1 && errno == EBADF);
    tentu_sahkan(unlink("posix.txt") == 0);
    Fail = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    tentu_sahkan(Fail == 3 && fcntl(Fail, F_GETFD) == 1);
    tentu_sahkan(read(Fail, data, 1) == -1 && errno == EBADF);
    tentu_sahkan(write(Fail, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) tentu_sahkan(dup(Fail) == INDEX);
    tentu_sahkan(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    tentu_sahkan(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    tentu_sahkan(fstat(Fail, &status_VALUE) == 0 && status_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) tentu_sahkan(close(INDEX) == 0);
    tentu_sahkan(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fail = open("posix.txt", O_RDONLY);
    tentu_sahkan(Fail == 3 && write(Fail, data, 1) == -1 && errno == EBADF);
    tentu_sahkan(fcntl(Fail, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    tentu_sahkan(close(8) == 0 && close(Fail) == 0 && unlink("posix.txt") == 0);
    tentu_sahkan(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    tentu_sahkan(fstat(1, &status_VALUE) == 0 && S_ISCHR(status_VALUE.st_mode));
    tentu_sahkan(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    tentu_sahkan(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr e_mel; char e_mel_SMS[16];
    tentu_sahkan(inet_pton(AF_INET, "10.0.2.2", &e_mel) == 1 && ntohl(e_mel.s_addr) == 0x0a000202U);
    tentu_sahkan(inet_ntop(AF_INET, &e_mel, e_mel_SMS, sizeof e_mel_SMS) == e_mel_SMS && strcmp(e_mel_SMS, "10.0.2.2") == 0);
    tentu_sahkan(inet_pton(AF_INET, "256.0.0.1", &e_mel) == 0 && ntohl(e_mel.s_addr) == 0x0a000202U);
    tentu_sahkan(inet_pton(AF_INET, "01.0.0.1", &e_mel) == 0);
    tentu_sahkan(inet_ntop(AF_INET, &e_mel, e_mel_SMS, 3) == NULL && errno == ENOSPC);
    tentu_sahkan(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], item_COUNT = 0; char Nama[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nama[4] = '0' + INDEX;
        int 열린파일 = open(Nama, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { tentu_sahkan(errno == ENOSPC); break; }
        보관[item_COUNT++] = 열린파일;
    }
    tentu_sahkan(item_COUNT > 0 && item_COUNT < 8);
    tentu_sahkan(unlink("slot0") == 0);
    tentu_sahkan(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    tentu_sahkan(close(보관[0]) == 0);
    Fail = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    tentu_sahkan(Fail >= 0 && close(Fail) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < item_COUNT; INDEX++) {
        Nama[4] = '0' + INDEX;
        tentu_sahkan(close(보관[INDEX]) == 0 && unlink(Nama) == 0);
    }
    tentu_sahkan(fsync(-1) == -1 && errno == EBADF);
    tentu_sahkan(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
