#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int kondisyon, int linya) {
    검사항목수++;
    if (!kondisyon) {
        puts("POSIX CHECK FAILED");
        char digit_VALUE[12]; int haba_VALUE = 0;
        do { digit_VALUE[haba_VALUE++] = '0' + linya % 10; linya /= 10; } while (linya);
        while (haba_VALUE) putchar(digit_VALUE[--haba_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define tiyakin_kumpirmahin(kondisyon) 검사((kondisyon), __LINE__)

int main(int 인수개수, char **argumento_list) {
    char data[32]; struct stat katayuan_VALUE;
    tiyakin_kumpirmahin(인수개수 == 2 && strcmp(argumento_list[1], "check") == 0 && argumento_list[2] == 0);
    tiyakin_kumpirmahin(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    tiyakin_kumpirmahin(buksan_file("absent", mababasa_lamang_VALUE) == -1 && 오류번호 == ENOENT);
    int file = buksan_file("/posix.txt", nababasa_nasusulatan | 새파일만들기, 0640);
    tiyakin_kumpirmahin(file == 3);
    tiyakin_kumpirmahin(sumulat_file_data(file, "abcd", 4) == 4);
    tiyakin_kumpirmahin(buksan_file("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    tiyakin_kumpirmahin(파일상태읽기(file, &katayuan_VALUE) == 0 && katayuan_VALUE.st_size == 4 && S_ISREG(katayuan_VALUE.st_mode));
    tiyakin_kumpirmahin((katayuan_VALUE.st_mode & 0777) == 0640 && katayuan_VALUE.st_nlink == 1);
    tiyakin_kumpirmahin(i_seek_file(file, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(file);
    tiyakin_kumpirmahin(복제 == 4);
    tiyakin_kumpirmahin(파일자료읽기(복제, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    tiyakin_kumpirmahin(파일자료읽기(file, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    tiyakin_kumpirmahin(파일자료읽기(file, data, 1) == 0);
    tiyakin_kumpirmahin(fcntl(file, F_SETFD, FD_CLOEXEC) == 0 && fcntl(file, F_GETFD) == 1);
    tiyakin_kumpirmahin(fcntl(복제, F_GETFD) == 0);
    tiyakin_kumpirmahin(dup2(file, file) == file && fcntl(file, F_GETFD) == 1);
    tiyakin_kumpirmahin(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    tiyakin_kumpirmahin(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(file, F_GETFL) & O_APPEND));
    tiyakin_kumpirmahin(lseek(file, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(file, 0, SEEK_CUR) == 5);
    tiyakin_kumpirmahin(fcntl(file, F_SETFL, 0) == 0);
    tiyakin_kumpirmahin(lseek(file, 8, SEEK_SET) == 8 && write(file, "Z", 1) == 1);
    tiyakin_kumpirmahin(lseek(복제, 5, SEEK_SET) == 5 && read(file, data, 4) == 4);
    tiyakin_kumpirmahin(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    tiyakin_kumpirmahin(ftruncate(file, 2) == 0 && lseek(file, 0, SEEK_CUR) == 9);
    tiyakin_kumpirmahin(ftruncate(file, 6) == 0 && lseek(file, 2, SEEK_SET) == 2 && read(file, data, 4) == 4);
    tiyakin_kumpirmahin(!data[0] && !data[1] && !data[2] && !data[3]);
    tiyakin_kumpirmahin(lseek(file, 2147483647, SEEK_SET) == 2147483647);
    tiyakin_kumpirmahin(lseek(file, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    tiyakin_kumpirmahin(lseek(file, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    tiyakin_kumpirmahin(write(file, "!", 1) == -1 && errno == EFBIG);
    tiyakin_kumpirmahin(lseek(file, 0, SEEK_SET) == 0);
    tiyakin_kumpirmahin(read(file, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tiyakin_kumpirmahin(read(file, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    tiyakin_kumpirmahin(write(file, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tiyakin_kumpirmahin(read(file, data, (size_t)-1) == -1 && errno == EINVAL);
    tiyakin_kumpirmahin(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    tiyakin_kumpirmahin(fstat(file, (void *)0x00100000) == -1 && errno == EFAULT);
    tiyakin_kumpirmahin(lseek(file, 0, SEEK_CUR) == 0);
    tiyakin_kumpirmahin(read(file, NULL, 0) == 0 && write(file, NULL, 0) == 0);
    tiyakin_kumpirmahin(tanggalin_file_pagpasok_pangalan("posix.txt") == 0);
    tiyakin_kumpirmahin(fstat(file, &katayuan_VALUE) == 0 && katayuan_VALUE.st_nlink == 0 && katayuan_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    tiyakin_kumpirmahin(새파일 == 5 && fstat(새파일, &katayuan_VALUE) == 0 && katayuan_VALUE.st_size == 0);
    tiyakin_kumpirmahin(read(file, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    tiyakin_kumpirmahin(close(file) == 0 && close(복제) == 0 && close(새파일) == 0);
    tiyakin_kumpirmahin(close(새파일) == -1 && errno == EBADF);
    tiyakin_kumpirmahin(unlink("posix.txt") == 0);
    file = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    tiyakin_kumpirmahin(file == 3 && fcntl(file, F_GETFD) == 1);
    tiyakin_kumpirmahin(read(file, data, 1) == -1 && errno == EBADF);
    tiyakin_kumpirmahin(write(file, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) tiyakin_kumpirmahin(dup(file) == INDEX);
    tiyakin_kumpirmahin(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    tiyakin_kumpirmahin(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    tiyakin_kumpirmahin(fstat(file, &katayuan_VALUE) == 0 && katayuan_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) tiyakin_kumpirmahin(close(INDEX) == 0);
    tiyakin_kumpirmahin(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    file = open("posix.txt", O_RDONLY);
    tiyakin_kumpirmahin(file == 3 && write(file, data, 1) == -1 && errno == EBADF);
    tiyakin_kumpirmahin(fcntl(file, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    tiyakin_kumpirmahin(close(8) == 0 && close(file) == 0 && unlink("posix.txt") == 0);
    tiyakin_kumpirmahin(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    tiyakin_kumpirmahin(fstat(1, &katayuan_VALUE) == 0 && S_ISCHR(katayuan_VALUE.st_mode));
    tiyakin_kumpirmahin(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    tiyakin_kumpirmahin(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr email; char email_SMS[16];
    tiyakin_kumpirmahin(inet_pton(AF_INET, "10.0.2.2", &email) == 1 && ntohl(email.s_addr) == 0x0a000202U);
    tiyakin_kumpirmahin(inet_ntop(AF_INET, &email, email_SMS, sizeof email_SMS) == email_SMS && strcmp(email_SMS, "10.0.2.2") == 0);
    tiyakin_kumpirmahin(inet_pton(AF_INET, "256.0.0.1", &email) == 0 && ntohl(email.s_addr) == 0x0a000202U);
    tiyakin_kumpirmahin(inet_pton(AF_INET, "01.0.0.1", &email) == 0);
    tiyakin_kumpirmahin(inet_ntop(AF_INET, &email, email_SMS, 3) == NULL && errno == ENOSPC);
    tiyakin_kumpirmahin(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], item_COUNT = 0; char pangalan[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        pangalan[4] = '0' + INDEX;
        int 열린파일 = open(pangalan, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { tiyakin_kumpirmahin(errno == ENOSPC); break; }
        보관[item_COUNT++] = 열린파일;
    }
    tiyakin_kumpirmahin(item_COUNT > 0 && item_COUNT < 8);
    tiyakin_kumpirmahin(unlink("slot0") == 0);
    tiyakin_kumpirmahin(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    tiyakin_kumpirmahin(close(보관[0]) == 0);
    file = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    tiyakin_kumpirmahin(file >= 0 && close(file) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < item_COUNT; INDEX++) {
        pangalan[4] = '0' + INDEX;
        tiyakin_kumpirmahin(close(보관[INDEX]) == 0 && unlink(pangalan) == 0);
    }
    tiyakin_kumpirmahin(fsync(-1) == -1 && errno == EBADF);
    tiyakin_kumpirmahin(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
