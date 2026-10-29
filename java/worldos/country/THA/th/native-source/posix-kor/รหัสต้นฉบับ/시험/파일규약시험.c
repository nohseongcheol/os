#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int โรค, int บรรทัด) {
    검사항목수++;
    if (!โรค) {
        puts("POSIX CHECK FAILED");
        char ตัวเลข_ค่า[12]; int 길이 = 0;
        do { ตัวเลข_ค่า[길이++] = '0' + บรรทัด % 10; บรรทัด /= 10; } while (บรรทัด);
        while (길이) putchar(ตัวเลข_ค่า[--길이]);
        putchar('\n'); _exit(1);
    }
}
#define ยืนยัน(โรค) 검사((โรค), __LINE__)

int main(int 인수개수, char **อาร์กิวเมนต์_รายการ) {
    char ข้อมูล[32]; struct stat สถานะ_ค่า;
    ยืนยัน(인수개수 == 2 && strcmp(อาร์กิวเมนต์_รายการ[1], "check") == 0 && อาร์กิวเมนต์_รายการ[2] == 0);
    ยืนยัน(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ยืนยัน(เปิด_แฟ้ม("absent", อ่านอย่างเดียว_ค่า) == -1 && หมายเลขข้อผิดพลาด == ENOENT);
    int แฟ้ม = เปิด_แฟ้ม("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    ยืนยัน(แฟ้ม == 3);
    ยืนยัน(파일자료쓰기(แฟ้ม, "abcd", 4) == 4);
    ยืนยัน(เปิด_แฟ้ม("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ยืนยัน(파일상태읽기(แฟ้ม, &สถานะ_ค่า) == 0 && สถานะ_ค่า.st_size == 4 && S_ISREG(สถานะ_ค่า.st_mode));
    ยืนยัน((สถานะ_ค่า.st_mode & 0777) == 0640 && สถานะ_ค่า.st_nlink == 1);
    ยืนยัน(กรอ_แฟ้ม(แฟ้ม, 0, 처음기준) == 0);
    int ลอกแบบ_ค่า = 파일서술자복제(แฟ้ม);
    ยืนยัน(ลอกแบบ_ค่า == 4);
    ยืนยัน(파일자료읽기(ลอกแบบ_ค่า, ข้อมูล, 2) == 2 && memcmp(ข้อมูล, "ab", 2) == 0);
    ยืนยัน(파일자료읽기(แฟ้ม, ข้อมูล, 2) == 2 && memcmp(ข้อมูล, "cd", 2) == 0);
    ยืนยัน(파일자료읽기(แฟ้ม, ข้อมูล, 1) == 0);
    ยืนยัน(fcntl(แฟ้ม, F_SETFD, FD_CLOEXEC) == 0 && fcntl(แฟ้ม, F_GETFD) == 1);
    ยืนยัน(fcntl(ลอกแบบ_ค่า, F_GETFD) == 0);
    ยืนยัน(dup2(แฟ้ม, แฟ้ม) == แฟ้ม && fcntl(แฟ้ม, F_GETFD) == 1);
    ยืนยัน(dup2(-1, ลอกแบบ_ค่า) == -1 && errno == EBADF && fcntl(ลอกแบบ_ค่า, F_GETFD) == 0);
    ยืนยัน(fcntl(ลอกแบบ_ค่า, F_SETFL, O_APPEND) == 0 && (fcntl(แฟ้ม, F_GETFL) & O_APPEND));
    ยืนยัน(lseek(แฟ้ม, 0, SEEK_SET) == 0 && write(ลอกแบบ_ค่า, "e", 1) == 1 && lseek(แฟ้ม, 0, SEEK_CUR) == 5);
    ยืนยัน(fcntl(แฟ้ม, F_SETFL, 0) == 0);
    ยืนยัน(lseek(แฟ้ม, 8, SEEK_SET) == 8 && write(แฟ้ม, "Z", 1) == 1);
    ยืนยัน(lseek(ลอกแบบ_ค่า, 5, SEEK_SET) == 5 && read(แฟ้ม, ข้อมูล, 4) == 4);
    ยืนยัน(ข้อมูล[0] == 0 && ข้อมูล[1] == 0 && ข้อมูล[2] == 0 && ข้อมูล[3] == 'Z');
    ยืนยัน(ftruncate(แฟ้ม, 2) == 0 && lseek(แฟ้ม, 0, SEEK_CUR) == 9);
    ยืนยัน(ftruncate(แฟ้ม, 6) == 0 && lseek(แฟ้ม, 2, SEEK_SET) == 2 && read(แฟ้ม, ข้อมูล, 4) == 4);
    ยืนยัน(!ข้อมูล[0] && !ข้อมูล[1] && !ข้อมูล[2] && !ข้อมูล[3]);
    ยืนยัน(lseek(แฟ้ม, 2147483647, SEEK_SET) == 2147483647);
    ยืนยัน(lseek(แฟ้ม, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ยืนยัน(lseek(แฟ้ม, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ยืนยัน(write(แฟ้ม, "!", 1) == -1 && errno == EFBIG);
    ยืนยัน(lseek(แฟ้ม, 0, SEEK_SET) == 0);
    ยืนยัน(read(แฟ้ม, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ยืนยัน(read(แฟ้ม, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ยืนยัน(write(แฟ้ม, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ยืนยัน(read(แฟ้ม, ข้อมูล, (size_t)-1) == -1 && errno == EINVAL);
    ยืนยัน(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ยืนยัน(fstat(แฟ้ม, (void *)0x00100000) == -1 && errno == EFAULT);
    ยืนยัน(lseek(แฟ้ม, 0, SEEK_CUR) == 0);
    ยืนยัน(read(แฟ้ม, NULL, 0) == 0 && write(แฟ้ม, NULL, 0) == 0);
    ยืนยัน(นําออก_แฟ้ม_รายการ_ชื่อ("posix.txt") == 0);
    ยืนยัน(fstat(แฟ้ม, &สถานะ_ค่า) == 0 && สถานะ_ค่า.st_nlink == 0 && สถานะ_ค่า.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ยืนยัน(새파일 == 5 && fstat(새파일, &สถานะ_ค่า) == 0 && สถานะ_ค่า.st_size == 0);
    ยืนยัน(read(แฟ้ม, ข้อมูล, 2) == 2 && memcmp(ข้อมูล, "ab", 2) == 0);
    ยืนยัน(close(แฟ้ม) == 0 && close(ลอกแบบ_ค่า) == 0 && close(새파일) == 0);
    ยืนยัน(close(새파일) == -1 && errno == EBADF);
    ยืนยัน(unlink("posix.txt") == 0);
    แฟ้ม = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ยืนยัน(แฟ้ม == 3 && fcntl(แฟ้ม, F_GETFD) == 1);
    ยืนยัน(read(แฟ้ม, ข้อมูล, 1) == -1 && errno == EBADF);
    ยืนยัน(write(แฟ้ม, "keep", 4) == 4);
    for (int ดัชนี = 4; ดัชนี < 32; ดัชนี++) ยืนยัน(dup(แฟ้ม) == ดัชนี);
    ยืนยัน(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ยืนยัน(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ยืนยัน(fstat(แฟ้ม, &สถานะ_ค่า) == 0 && สถานะ_ค่า.st_size == 4);
    for (int ดัชนี = 3; ดัชนี < 32; ดัชนี++) ยืนยัน(close(ดัชนี) == 0);
    ยืนยัน(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    แฟ้ม = open("posix.txt", O_RDONLY);
    ยืนยัน(แฟ้ม == 3 && write(แฟ้ม, ข้อมูล, 1) == -1 && errno == EBADF);
    ยืนยัน(fcntl(แฟ้ม, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ยืนยัน(close(8) == 0 && close(แฟ้ม) == 0 && unlink("posix.txt") == 0);
    ยืนยัน(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ยืนยัน(fstat(1, &สถานะ_ค่า) == 0 && S_ISCHR(สถานะ_ค่า.st_mode));
    ยืนยัน(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ยืนยัน(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr อีเมล; char อีเมล_ข้อความ[16];
    ยืนยัน(inet_pton(AF_INET, "10.0.2.2", &อีเมล) == 1 && ntohl(อีเมล.s_addr) == 0x0a000202U);
    ยืนยัน(inet_ntop(AF_INET, &อีเมล, อีเมล_ข้อความ, sizeof อีเมล_ข้อความ) == อีเมล_ข้อความ && strcmp(อีเมล_ข้อความ, "10.0.2.2") == 0);
    ยืนยัน(inet_pton(AF_INET, "256.0.0.1", &อีเมล) == 0 && ntohl(อีเมล.s_addr) == 0x0a000202U);
    ยืนยัน(inet_pton(AF_INET, "01.0.0.1", &อีเมล) == 0);
    ยืนยัน(inet_ntop(AF_INET, &อีเมล, อีเมล_ข้อความ, 3) == NULL && errno == ENOSPC);
    ยืนยัน(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ชื่อ[] = "slot0";
    for (int ดัชนี = 0; ดัชนี < 8; ดัชนี++) {
        ชื่อ[4] = '0' + ดัชนี;
        int 열린파일 = open(ชื่อ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ยืนยัน(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ยืนยัน(개수 > 0 && 개수 < 8);
    ยืนยัน(unlink("slot0") == 0);
    ยืนยัน(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ยืนยัน(close(보관[0]) == 0);
    แฟ้ม = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ยืนยัน(แฟ้ม >= 0 && close(แฟ้ม) == 0 && unlink("held-slot") == 0);
    for (int ดัชนี = 1; ดัชนี < 개수; ดัชนี++) {
        ชื่อ[4] = '0' + ดัชนี;
        ยืนยัน(close(보관[ดัชนี]) == 0 && unlink(ชื่อ) == 0);
    }
    ยืนยัน(fsync(-1) == -1 && errno == EBADF);
    ยืนยัน(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
