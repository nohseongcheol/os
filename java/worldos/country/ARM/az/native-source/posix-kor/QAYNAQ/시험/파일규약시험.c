#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int şərt, int Giriş) {
    검사항목수++;
    if (!şərt) {
        puts("POSIX CHECK FAILED");
        char rəqəm_VALUE[12]; int uzunluq_VALUE = 0;
        do { rəqəm_VALUE[uzunluq_VALUE++] = '0' + Giriş % 10; Giriş /= 10; } while (Giriş);
        while (uzunluq_VALUE) putchar(rəqəm_VALUE[--uzunluq_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define yoxlamaq(şərt) 검사((şərt), __LINE__)

int main(int 인수개수, char **arqument_Siyahı) {
    char verilənlər[32]; struct stat vəziyyət_VALUE;
    yoxlamaq(인수개수 == 2 && strcmp(arqument_Siyahı[1], "check") == 0 && arqument_Siyahı[2] == 0);
    yoxlamaq(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    yoxlamaq(açmaq_fayl("absent", yalnız_oxunan_VALUE) == -1 && 오류번호 == ENOENT);
    int FAYL = açmaq_fayl("/posix.txt", oxunan_yazılan | 새파일만들기, 0640);
    yoxlamaq(FAYL == 3);
    yoxlamaq(yazmaq_fayl_verilənlər(FAYL, "abcd", 4) == 4);
    yoxlamaq(açmaq_fayl("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    yoxlamaq(파일상태읽기(FAYL, &vəziyyət_VALUE) == 0 && vəziyyət_VALUE.st_size == 4 && S_ISREG(vəziyyət_VALUE.st_mode));
    yoxlamaq((vəziyyət_VALUE.st_mode & 0777) == 0640 && vəziyyət_VALUE.st_nlink == 1);
    yoxlamaq(axtarmaq_fayl(FAYL, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(FAYL);
    yoxlamaq(복제 == 4);
    yoxlamaq(파일자료읽기(복제, verilənlər, 2) == 2 && memcmp(verilənlər, "ab", 2) == 0);
    yoxlamaq(파일자료읽기(FAYL, verilənlər, 2) == 2 && memcmp(verilənlər, "cd", 2) == 0);
    yoxlamaq(파일자료읽기(FAYL, verilənlər, 1) == 0);
    yoxlamaq(fcntl(FAYL, F_SETFD, FD_CLOEXEC) == 0 && fcntl(FAYL, F_GETFD) == 1);
    yoxlamaq(fcntl(복제, F_GETFD) == 0);
    yoxlamaq(dup2(FAYL, FAYL) == FAYL && fcntl(FAYL, F_GETFD) == 1);
    yoxlamaq(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    yoxlamaq(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(FAYL, F_GETFL) & O_APPEND));
    yoxlamaq(lseek(FAYL, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(FAYL, 0, SEEK_CUR) == 5);
    yoxlamaq(fcntl(FAYL, F_SETFL, 0) == 0);
    yoxlamaq(lseek(FAYL, 8, SEEK_SET) == 8 && write(FAYL, "Z", 1) == 1);
    yoxlamaq(lseek(복제, 5, SEEK_SET) == 5 && read(FAYL, verilənlər, 4) == 4);
    yoxlamaq(verilənlər[0] == 0 && verilənlər[1] == 0 && verilənlər[2] == 0 && verilənlər[3] == 'Z');
    yoxlamaq(ftruncate(FAYL, 2) == 0 && lseek(FAYL, 0, SEEK_CUR) == 9);
    yoxlamaq(ftruncate(FAYL, 6) == 0 && lseek(FAYL, 2, SEEK_SET) == 2 && read(FAYL, verilənlər, 4) == 4);
    yoxlamaq(!verilənlər[0] && !verilənlər[1] && !verilənlər[2] && !verilənlər[3]);
    yoxlamaq(lseek(FAYL, 2147483647, SEEK_SET) == 2147483647);
    yoxlamaq(lseek(FAYL, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    yoxlamaq(lseek(FAYL, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    yoxlamaq(write(FAYL, "!", 1) == -1 && errno == EFBIG);
    yoxlamaq(lseek(FAYL, 0, SEEK_SET) == 0);
    yoxlamaq(read(FAYL, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    yoxlamaq(read(FAYL, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    yoxlamaq(write(FAYL, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    yoxlamaq(read(FAYL, verilənlər, (size_t)-1) == -1 && errno == EINVAL);
    yoxlamaq(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    yoxlamaq(fstat(FAYL, (void *)0x00100000) == -1 && errno == EFAULT);
    yoxlamaq(lseek(FAYL, 0, SEEK_CUR) == 0);
    yoxlamaq(read(FAYL, NULL, 0) == 0 && write(FAYL, NULL, 0) == 0);
    yoxlamaq(silmək_fayl_daxiletmə_ad("posix.txt") == 0);
    yoxlamaq(fstat(FAYL, &vəziyyət_VALUE) == 0 && vəziyyət_VALUE.st_nlink == 0 && vəziyyət_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    yoxlamaq(새파일 == 5 && fstat(새파일, &vəziyyət_VALUE) == 0 && vəziyyət_VALUE.st_size == 0);
    yoxlamaq(read(FAYL, verilənlər, 2) == 2 && memcmp(verilənlər, "ab", 2) == 0);
    yoxlamaq(close(FAYL) == 0 && close(복제) == 0 && close(새파일) == 0);
    yoxlamaq(close(새파일) == -1 && errno == EBADF);
    yoxlamaq(unlink("posix.txt") == 0);
    FAYL = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    yoxlamaq(FAYL == 3 && fcntl(FAYL, F_GETFD) == 1);
    yoxlamaq(read(FAYL, verilənlər, 1) == -1 && errno == EBADF);
    yoxlamaq(write(FAYL, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) yoxlamaq(dup(FAYL) == INDEX);
    yoxlamaq(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    yoxlamaq(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    yoxlamaq(fstat(FAYL, &vəziyyət_VALUE) == 0 && vəziyyət_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) yoxlamaq(close(INDEX) == 0);
    yoxlamaq(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    FAYL = open("posix.txt", O_RDONLY);
    yoxlamaq(FAYL == 3 && write(FAYL, verilənlər, 1) == -1 && errno == EBADF);
    yoxlamaq(fcntl(FAYL, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    yoxlamaq(close(8) == 0 && close(FAYL) == 0 && unlink("posix.txt") == 0);
    yoxlamaq(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    yoxlamaq(fstat(1, &vəziyyət_VALUE) == 0 && S_ISCHR(vəziyyət_VALUE.st_mode));
    yoxlamaq(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    yoxlamaq(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ünvan; char ünvan_SMS[16];
    yoxlamaq(inet_pton(AF_INET, "10.0.2.2", &ünvan) == 1 && ntohl(ünvan.s_addr) == 0x0a000202U);
    yoxlamaq(inet_ntop(AF_INET, &ünvan, ünvan_SMS, sizeof ünvan_SMS) == ünvan_SMS && strcmp(ünvan_SMS, "10.0.2.2") == 0);
    yoxlamaq(inet_pton(AF_INET, "256.0.0.1", &ünvan) == 0 && ntohl(ünvan.s_addr) == 0x0a000202U);
    yoxlamaq(inet_pton(AF_INET, "01.0.0.1", &ünvan) == 0);
    yoxlamaq(inet_ntop(AF_INET, &ünvan, ünvan_SMS, 3) == NULL && errno == ENOSPC);
    yoxlamaq(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], element_COUNT = 0; char Ad[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Ad[4] = '0' + INDEX;
        int 열린파일 = open(Ad, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { yoxlamaq(errno == ENOSPC); break; }
        보관[element_COUNT++] = 열린파일;
    }
    yoxlamaq(element_COUNT > 0 && element_COUNT < 8);
    yoxlamaq(unlink("slot0") == 0);
    yoxlamaq(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    yoxlamaq(close(보관[0]) == 0);
    FAYL = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    yoxlamaq(FAYL >= 0 && close(FAYL) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < element_COUNT; INDEX++) {
        Ad[4] = '0' + INDEX;
        yoxlamaq(close(보관[INDEX]) == 0 && unlink(Ad) == 0);
    }
    yoxlamaq(fsync(-1) == -1 && errno == EBADF);
    yoxlamaq(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
