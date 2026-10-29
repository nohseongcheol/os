#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ເງື່ອນໄຂ, int ສາຍ) {
    검사항목수++;
    if (!ເງື່ອນໄຂ) {
        puts("POSIX CHECK FAILED");
        char ຕົວເລກ_ຄ່າ[12]; int ຄວາມຍາວ_ຄ່າ = 0;
        do { ຕົວເລກ_ຄ່າ[ຄວາມຍາວ_ຄ່າ++] = '0' + ສາຍ % 10; ສາຍ /= 10; } while (ສາຍ);
        while (ຄວາມຍາວ_ຄ່າ) putchar(ຕົວເລກ_ຄ່າ[--ຄວາມຍາວ_ຄ່າ]);
        putchar('\n'); _exit(1);
    }
}
#define 확인(ເງື່ອນໄຂ) 검사((ເງື່ອນໄຂ), __LINE__)

int main(int 인수개수, char **ຂໍ້ພິສູດ_ລາຍຊື່) {
    char ຂໍ້ມູນ[32]; struct stat ສະຖານະ_ຄ່າ;
    확인(인수개수 == 2 && strcmp(ຂໍ້ພິສູດ_ລາຍຊື່[1], "check") == 0 && ຂໍ້ພິສູດ_ລາຍຊື່[2] == 0);
    확인(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    확인(ສ້າງ_ຟາຍ("absent", ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ) == -1 && 오류번호 == ENOENT);
    int ຟາຍ = ສ້າງ_ຟາຍ("/posix.txt", ອ່ານ_ຂຽນ | 새파일만들기, 0640);
    확인(ຟາຍ == 3);
    확인(ຂຽນ_ຟາຍ_ຂໍ້ມູນ(ຟາຍ, "abcd", 4) == 4);
    확인(ສ້າງ_ຟາຍ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    확인(파일상태읽기(ຟາຍ, &ສະຖານະ_ຄ່າ) == 0 && ສະຖານະ_ຄ່າ.st_size == 4 && S_ISREG(ສະຖານະ_ຄ່າ.st_mode));
    확인((ສະຖານະ_ຄ່າ.st_mode & 0777) == 0640 && ສະຖານະ_ຄ່າ.st_nlink == 1);
    확인(ຊອກຫາ_ຟາຍ(ຟາຍ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ຟາຍ);
    확인(복제 == 4);
    확인(파일자료읽기(복제, ຂໍ້ມູນ, 2) == 2 && memcmp(ຂໍ້ມູນ, "ab", 2) == 0);
    확인(파일자료읽기(ຟາຍ, ຂໍ້ມູນ, 2) == 2 && memcmp(ຂໍ້ມູນ, "cd", 2) == 0);
    확인(파일자료읽기(ຟາຍ, ຂໍ້ມູນ, 1) == 0);
    확인(fcntl(ຟາຍ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ຟາຍ, F_GETFD) == 1);
    확인(fcntl(복제, F_GETFD) == 0);
    확인(dup2(ຟາຍ, ຟາຍ) == ຟາຍ && fcntl(ຟາຍ, F_GETFD) == 1);
    확인(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    확인(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ຟາຍ, F_GETFL) & O_APPEND));
    확인(lseek(ຟາຍ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ຟາຍ, 0, SEEK_CUR) == 5);
    확인(fcntl(ຟາຍ, F_SETFL, 0) == 0);
    확인(lseek(ຟາຍ, 8, SEEK_SET) == 8 && write(ຟາຍ, "Z", 1) == 1);
    확인(lseek(복제, 5, SEEK_SET) == 5 && read(ຟາຍ, ຂໍ້ມູນ, 4) == 4);
    확인(ຂໍ້ມູນ[0] == 0 && ຂໍ້ມູນ[1] == 0 && ຂໍ້ມູນ[2] == 0 && ຂໍ້ມູນ[3] == 'Z');
    확인(ftruncate(ຟາຍ, 2) == 0 && lseek(ຟາຍ, 0, SEEK_CUR) == 9);
    확인(ftruncate(ຟາຍ, 6) == 0 && lseek(ຟາຍ, 2, SEEK_SET) == 2 && read(ຟາຍ, ຂໍ້ມູນ, 4) == 4);
    확인(!ຂໍ້ມູນ[0] && !ຂໍ້ມູນ[1] && !ຂໍ້ມູນ[2] && !ຂໍ້ມູນ[3]);
    확인(lseek(ຟາຍ, 2147483647, SEEK_SET) == 2147483647);
    확인(lseek(ຟາຍ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    확인(lseek(ຟາຍ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    확인(write(ຟາຍ, "!", 1) == -1 && errno == EFBIG);
    확인(lseek(ຟາຍ, 0, SEEK_SET) == 0);
    확인(read(ຟາຍ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(ຟາຍ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    확인(write(ຟາຍ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(ຟາຍ, ຂໍ້ມູນ, (size_t)-1) == -1 && errno == EINVAL);
    확인(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    확인(fstat(ຟາຍ, (void *)0x00100000) == -1 && errno == EFAULT);
    확인(lseek(ຟາຍ, 0, SEEK_CUR) == 0);
    확인(read(ຟາຍ, NULL, 0) == 0 && write(ຟາຍ, NULL, 0) == 0);
    확인(파일이름지우기("posix.txt") == 0);
    확인(fstat(ຟາຍ, &ສະຖານະ_ຄ່າ) == 0 && ສະຖານະ_ຄ່າ.st_nlink == 0 && ສະຖານະ_ຄ່າ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(새파일 == 5 && fstat(새파일, &ສະຖານະ_ຄ່າ) == 0 && ສະຖານະ_ຄ່າ.st_size == 0);
    확인(read(ຟາຍ, ຂໍ້ມູນ, 2) == 2 && memcmp(ຂໍ້ມູນ, "ab", 2) == 0);
    확인(close(ຟາຍ) == 0 && close(복제) == 0 && close(새파일) == 0);
    확인(close(새파일) == -1 && errno == EBADF);
    확인(unlink("posix.txt") == 0);
    ຟາຍ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    확인(ຟາຍ == 3 && fcntl(ຟາຍ, F_GETFD) == 1);
    확인(read(ຟາຍ, ຂໍ້ມູນ, 1) == -1 && errno == EBADF);
    확인(write(ຟາຍ, "keep", 4) == 4);
    for (int ດັດຊະນີ = 4; ດັດຊະນີ < 32; ດັດຊະນີ++) 확인(dup(ຟາຍ) == ດັດຊະນີ);
    확인(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    확인(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    확인(fstat(ຟາຍ, &ສະຖານະ_ຄ່າ) == 0 && ສະຖານະ_ຄ່າ.st_size == 4);
    for (int ດັດຊະນີ = 3; ດັດຊະນີ < 32; ດັດຊະນີ++) 확인(close(ດັດຊະນີ) == 0);
    확인(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ຟາຍ = open("posix.txt", O_RDONLY);
    확인(ຟາຍ == 3 && write(ຟາຍ, ຂໍ້ມູນ, 1) == -1 && errno == EBADF);
    확인(fcntl(ຟາຍ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    확인(close(8) == 0 && close(ຟາຍ) == 0 && unlink("posix.txt") == 0);
    확인(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    확인(fstat(1, &ສະຖານະ_ຄ່າ) == 0 && S_ISCHR(ສະຖານະ_ຄ່າ.st_mode));
    확인(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    확인(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ອີເມວ; char ອີເມວ_ຂໍ້ຄວາມ[16];
    확인(inet_pton(AF_INET, "10.0.2.2", &ອີເມວ) == 1 && ntohl(ອີເມວ.s_addr) == 0x0a000202U);
    확인(inet_ntop(AF_INET, &ອີເມວ, ອີເມວ_ຂໍ້ຄວາມ, sizeof ອີເມວ_ຂໍ້ຄວາມ) == ອີເມວ_ຂໍ້ຄວາມ && strcmp(ອີເມວ_ຂໍ້ຄວາມ, "10.0.2.2") == 0);
    확인(inet_pton(AF_INET, "256.0.0.1", &ອີເມວ) == 0 && ntohl(ອີເມວ.s_addr) == 0x0a000202U);
    확인(inet_pton(AF_INET, "01.0.0.1", &ອີເມວ) == 0);
    확인(inet_ntop(AF_INET, &ອີເມວ, ອີເມວ_ຂໍ້ຄວາມ, 3) == NULL && errno == ENOSPC);
    확인(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ຊື່[] = "slot0";
    for (int ດັດຊະນີ = 0; ດັດຊະນີ < 8; ດັດຊະນີ++) {
        ຊື່[4] = '0' + ດັດຊະນີ;
        int 열린파일 = open(ຊື່, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { 확인(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    확인(개수 > 0 && 개수 < 8);
    확인(unlink("slot0") == 0);
    확인(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    확인(close(보관[0]) == 0);
    ຟາຍ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(ຟາຍ >= 0 && close(ຟາຍ) == 0 && unlink("held-slot") == 0);
    for (int ດັດຊະນີ = 1; ດັດຊະນີ < 개수; ດັດຊະນີ++) {
        ຊື່[4] = '0' + ດັດຊະນີ;
        확인(close(보관[ດັດຊະນີ]) == 0 && unlink(ຊື່) == 0);
    }
    확인(fsync(-1) == -1 && errno == EBADF);
    확인(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
