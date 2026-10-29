#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int holat, int satr) {
    검사항목수++;
    if (!holat) {
        puts("POSIX CHECK FAILED");
        char raqam_VALUE[12]; int uzunlik_VALUE = 0;
        do { raqam_VALUE[uzunlik_VALUE++] = '0' + satr % 10; satr /= 10; } while (satr);
        while (uzunlik_VALUE) putchar(raqam_VALUE[--uzunlik_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define tasdiqlamoq(holat) 검사((holat), __LINE__)

int main(int 인수개수, char **dalil_Ro_yxat) {
    char ma_lumotlar[32]; struct stat holat_VALUE_e10195a1;
    tasdiqlamoq(인수개수 == 2 && strcmp(dalil_Ro_yxat[1], "check") == 0 && dalil_Ro_yxat[2] == 0);
    tasdiqlamoq(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    tasdiqlamoq(ochmoq_fayl("absent", faqat_o_qish_uchun_VALUE) == -1 && 오류번호 == ENOENT);
    int Fayl = ochmoq_fayl("/posix.txt", o_qish_yozish_mumkin | 새파일만들기, 0640);
    tasdiqlamoq(Fayl == 3);
    tasdiqlamoq(yozmoq_fayl_ma_lumotlar(Fayl, "abcd", 4) == 4);
    tasdiqlamoq(ochmoq_fayl("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    tasdiqlamoq(파일상태읽기(Fayl, &holat_VALUE_e10195a1) == 0 && holat_VALUE_e10195a1.st_size == 4 && S_ISREG(holat_VALUE_e10195a1.st_mode));
    tasdiqlamoq((holat_VALUE_e10195a1.st_mode & 0777) == 0640 && holat_VALUE_e10195a1.st_nlink == 1);
    tasdiqlamoq(izlamoq_fayl(Fayl, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Fayl);
    tasdiqlamoq(복제 == 4);
    tasdiqlamoq(파일자료읽기(복제, ma_lumotlar, 2) == 2 && memcmp(ma_lumotlar, "ab", 2) == 0);
    tasdiqlamoq(파일자료읽기(Fayl, ma_lumotlar, 2) == 2 && memcmp(ma_lumotlar, "cd", 2) == 0);
    tasdiqlamoq(파일자료읽기(Fayl, ma_lumotlar, 1) == 0);
    tasdiqlamoq(fcntl(Fayl, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fayl, F_GETFD) == 1);
    tasdiqlamoq(fcntl(복제, F_GETFD) == 0);
    tasdiqlamoq(dup2(Fayl, Fayl) == Fayl && fcntl(Fayl, F_GETFD) == 1);
    tasdiqlamoq(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    tasdiqlamoq(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Fayl, F_GETFL) & O_APPEND));
    tasdiqlamoq(lseek(Fayl, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Fayl, 0, SEEK_CUR) == 5);
    tasdiqlamoq(fcntl(Fayl, F_SETFL, 0) == 0);
    tasdiqlamoq(lseek(Fayl, 8, SEEK_SET) == 8 && write(Fayl, "Z", 1) == 1);
    tasdiqlamoq(lseek(복제, 5, SEEK_SET) == 5 && read(Fayl, ma_lumotlar, 4) == 4);
    tasdiqlamoq(ma_lumotlar[0] == 0 && ma_lumotlar[1] == 0 && ma_lumotlar[2] == 0 && ma_lumotlar[3] == 'Z');
    tasdiqlamoq(ftruncate(Fayl, 2) == 0 && lseek(Fayl, 0, SEEK_CUR) == 9);
    tasdiqlamoq(ftruncate(Fayl, 6) == 0 && lseek(Fayl, 2, SEEK_SET) == 2 && read(Fayl, ma_lumotlar, 4) == 4);
    tasdiqlamoq(!ma_lumotlar[0] && !ma_lumotlar[1] && !ma_lumotlar[2] && !ma_lumotlar[3]);
    tasdiqlamoq(lseek(Fayl, 2147483647, SEEK_SET) == 2147483647);
    tasdiqlamoq(lseek(Fayl, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    tasdiqlamoq(lseek(Fayl, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    tasdiqlamoq(write(Fayl, "!", 1) == -1 && errno == EFBIG);
    tasdiqlamoq(lseek(Fayl, 0, SEEK_SET) == 0);
    tasdiqlamoq(read(Fayl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tasdiqlamoq(read(Fayl, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    tasdiqlamoq(write(Fayl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    tasdiqlamoq(read(Fayl, ma_lumotlar, (size_t)-1) == -1 && errno == EINVAL);
    tasdiqlamoq(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    tasdiqlamoq(fstat(Fayl, (void *)0x00100000) == -1 && errno == EFAULT);
    tasdiqlamoq(lseek(Fayl, 0, SEEK_CUR) == 0);
    tasdiqlamoq(read(Fayl, NULL, 0) == 0 && write(Fayl, NULL, 0) == 0);
    tasdiqlamoq(olib_tashlamoq_fayl_kiritish_nom("posix.txt") == 0);
    tasdiqlamoq(fstat(Fayl, &holat_VALUE_e10195a1) == 0 && holat_VALUE_e10195a1.st_nlink == 0 && holat_VALUE_e10195a1.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    tasdiqlamoq(새파일 == 5 && fstat(새파일, &holat_VALUE_e10195a1) == 0 && holat_VALUE_e10195a1.st_size == 0);
    tasdiqlamoq(read(Fayl, ma_lumotlar, 2) == 2 && memcmp(ma_lumotlar, "ab", 2) == 0);
    tasdiqlamoq(close(Fayl) == 0 && close(복제) == 0 && close(새파일) == 0);
    tasdiqlamoq(close(새파일) == -1 && errno == EBADF);
    tasdiqlamoq(unlink("posix.txt") == 0);
    Fayl = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    tasdiqlamoq(Fayl == 3 && fcntl(Fayl, F_GETFD) == 1);
    tasdiqlamoq(read(Fayl, ma_lumotlar, 1) == -1 && errno == EBADF);
    tasdiqlamoq(write(Fayl, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) tasdiqlamoq(dup(Fayl) == INDEX);
    tasdiqlamoq(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    tasdiqlamoq(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    tasdiqlamoq(fstat(Fayl, &holat_VALUE_e10195a1) == 0 && holat_VALUE_e10195a1.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) tasdiqlamoq(close(INDEX) == 0);
    tasdiqlamoq(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fayl = open("posix.txt", O_RDONLY);
    tasdiqlamoq(Fayl == 3 && write(Fayl, ma_lumotlar, 1) == -1 && errno == EBADF);
    tasdiqlamoq(fcntl(Fayl, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    tasdiqlamoq(close(8) == 0 && close(Fayl) == 0 && unlink("posix.txt") == 0);
    tasdiqlamoq(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    tasdiqlamoq(fstat(1, &holat_VALUE_e10195a1) == 0 && S_ISCHR(holat_VALUE_e10195a1.st_mode));
    tasdiqlamoq(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    tasdiqlamoq(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr manzil; char manzil_SMS[16];
    tasdiqlamoq(inet_pton(AF_INET, "10.0.2.2", &manzil) == 1 && ntohl(manzil.s_addr) == 0x0a000202U);
    tasdiqlamoq(inet_ntop(AF_INET, &manzil, manzil_SMS, sizeof manzil_SMS) == manzil_SMS && strcmp(manzil_SMS, "10.0.2.2") == 0);
    tasdiqlamoq(inet_pton(AF_INET, "256.0.0.1", &manzil) == 0 && ntohl(manzil.s_addr) == 0x0a000202U);
    tasdiqlamoq(inet_pton(AF_INET, "01.0.0.1", &manzil) == 0);
    tasdiqlamoq(inet_ntop(AF_INET, &manzil, manzil_SMS, 3) == NULL && errno == ENOSPC);
    tasdiqlamoq(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], element_COUNT = 0; char Nomi[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nomi[4] = '0' + INDEX;
        int 열린파일 = open(Nomi, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { tasdiqlamoq(errno == ENOSPC); break; }
        보관[element_COUNT++] = 열린파일;
    }
    tasdiqlamoq(element_COUNT > 0 && element_COUNT < 8);
    tasdiqlamoq(unlink("slot0") == 0);
    tasdiqlamoq(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    tasdiqlamoq(close(보관[0]) == 0);
    Fayl = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    tasdiqlamoq(Fayl >= 0 && close(Fayl) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < element_COUNT; INDEX++) {
        Nomi[4] = '0' + INDEX;
        tasdiqlamoq(close(보관[INDEX]) == 0 && unlink(Nomi) == 0);
    }
    tasdiqlamoq(fsync(-1) == -1 && errno == EBADF);
    tasdiqlamoq(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
