#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int isimo, int umugqa) {
    검사항목수++;
    if (!isimo) {
        puts("POSIX CHECK FAILED");
        char idijithi_inani[12]; int ubude_inani = 0;
        do { idijithi_inani[ubude_inani++] = '0' + umugqa % 10; umugqa /= 10; } while (umugqa);
        while (ubude_inani) putchar(idijithi_inani[--ubude_inani]);
        putchar('\n'); _exit(1);
    }
}
#define qiniseka(isimo) 검사((isimo), __LINE__)

int main(int 인수개수, char **i_agumenti_Uhlu) {
    char imininingwane[32]; struct stat isimo_inani;
    qiniseka(인수개수 == 2 && strcmp(i_agumenti_Uhlu[1], "check") == 0 && i_agumenti_Uhlu[2] == 0);
    qiniseka(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    qiniseka(vula_ifayela("absent", fundwayo_kuphela_inani) == -1 && 오류번호 == ENOENT);
    int Ihele = vula_ifayela("/posix.txt", fundeka_bhaleka | 새파일만들기, 0640);
    qiniseka(Ihele == 3);
    qiniseka(bhala_ifayela_imininingwane(Ihele, "abcd", 4) == 4);
    qiniseka(vula_ifayela("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    qiniseka(파일상태읽기(Ihele, &isimo_inani) == 0 && isimo_inani.st_size == 4 && S_ISREG(isimo_inani.st_mode));
    qiniseka((isimo_inani.st_mode & 0777) == 0640 && isimo_inani.st_nlink == 1);
    qiniseka(cinga_ifayela(Ihele, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Ihele);
    qiniseka(복제 == 4);
    qiniseka(파일자료읽기(복제, imininingwane, 2) == 2 && memcmp(imininingwane, "ab", 2) == 0);
    qiniseka(파일자료읽기(Ihele, imininingwane, 2) == 2 && memcmp(imininingwane, "cd", 2) == 0);
    qiniseka(파일자료읽기(Ihele, imininingwane, 1) == 0);
    qiniseka(fcntl(Ihele, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Ihele, F_GETFD) == 1);
    qiniseka(fcntl(복제, F_GETFD) == 0);
    qiniseka(dup2(Ihele, Ihele) == Ihele && fcntl(Ihele, F_GETFD) == 1);
    qiniseka(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    qiniseka(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Ihele, F_GETFL) & O_APPEND));
    qiniseka(lseek(Ihele, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Ihele, 0, SEEK_CUR) == 5);
    qiniseka(fcntl(Ihele, F_SETFL, 0) == 0);
    qiniseka(lseek(Ihele, 8, SEEK_SET) == 8 && write(Ihele, "Z", 1) == 1);
    qiniseka(lseek(복제, 5, SEEK_SET) == 5 && read(Ihele, imininingwane, 4) == 4);
    qiniseka(imininingwane[0] == 0 && imininingwane[1] == 0 && imininingwane[2] == 0 && imininingwane[3] == 'Z');
    qiniseka(ftruncate(Ihele, 2) == 0 && lseek(Ihele, 0, SEEK_CUR) == 9);
    qiniseka(ftruncate(Ihele, 6) == 0 && lseek(Ihele, 2, SEEK_SET) == 2 && read(Ihele, imininingwane, 4) == 4);
    qiniseka(!imininingwane[0] && !imininingwane[1] && !imininingwane[2] && !imininingwane[3]);
    qiniseka(lseek(Ihele, 2147483647, SEEK_SET) == 2147483647);
    qiniseka(lseek(Ihele, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    qiniseka(lseek(Ihele, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    qiniseka(write(Ihele, "!", 1) == -1 && errno == EFBIG);
    qiniseka(lseek(Ihele, 0, SEEK_SET) == 0);
    qiniseka(read(Ihele, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    qiniseka(read(Ihele, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    qiniseka(write(Ihele, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    qiniseka(read(Ihele, imininingwane, (size_t)-1) == -1 && errno == EINVAL);
    qiniseka(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    qiniseka(fstat(Ihele, (void *)0x00100000) == -1 && errno == EFAULT);
    qiniseka(lseek(Ihele, 0, SEEK_CUR) == 0);
    qiniseka(read(Ihele, NULL, 0) == 0 && write(Ihele, NULL, 0) == 0);
    qiniseka(khipha_ifayela_okufakwayo_igama("posix.txt") == 0);
    qiniseka(fstat(Ihele, &isimo_inani) == 0 && isimo_inani.st_nlink == 0 && isimo_inani.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    qiniseka(새파일 == 5 && fstat(새파일, &isimo_inani) == 0 && isimo_inani.st_size == 0);
    qiniseka(read(Ihele, imininingwane, 2) == 2 && memcmp(imininingwane, "ab", 2) == 0);
    qiniseka(close(Ihele) == 0 && close(복제) == 0 && close(새파일) == 0);
    qiniseka(close(새파일) == -1 && errno == EBADF);
    qiniseka(unlink("posix.txt") == 0);
    Ihele = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    qiniseka(Ihele == 3 && fcntl(Ihele, F_GETFD) == 1);
    qiniseka(read(Ihele, imininingwane, 1) == -1 && errno == EBADF);
    qiniseka(write(Ihele, "keep", 4) == 4);
    for (int thola_inkomba = 4; thola_inkomba < 32; thola_inkomba++) qiniseka(dup(Ihele) == thola_inkomba);
    qiniseka(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    qiniseka(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    qiniseka(fstat(Ihele, &isimo_inani) == 0 && isimo_inani.st_size == 4);
    for (int thola_inkomba = 3; thola_inkomba < 32; thola_inkomba++) qiniseka(close(thola_inkomba) == 0);
    qiniseka(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Ihele = open("posix.txt", O_RDONLY);
    qiniseka(Ihele == 3 && write(Ihele, imininingwane, 1) == -1 && errno == EBADF);
    qiniseka(fcntl(Ihele, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    qiniseka(close(8) == 0 && close(Ihele) == 0 && unlink("posix.txt") == 0);
    qiniseka(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    qiniseka(fstat(1, &isimo_inani) == 0 && S_ISCHR(isimo_inani.st_mode));
    qiniseka(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    qiniseka(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ikheli; char ikheli_I_SMS[16];
    qiniseka(inet_pton(AF_INET, "10.0.2.2", &ikheli) == 1 && ntohl(ikheli.s_addr) == 0x0a000202U);
    qiniseka(inet_ntop(AF_INET, &ikheli, ikheli_I_SMS, sizeof ikheli_I_SMS) == ikheli_I_SMS && strcmp(ikheli_I_SMS, "10.0.2.2") == 0);
    qiniseka(inet_pton(AF_INET, "256.0.0.1", &ikheli) == 0 && ntohl(ikheli.s_addr) == 0x0a000202U);
    qiniseka(inet_pton(AF_INET, "01.0.0.1", &ikheli) == 0);
    qiniseka(inet_ntop(AF_INET, &ikheli, ikheli_I_SMS, 3) == NULL && errno == ENOSPC);
    qiniseka(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Igama[] = "slot0";
    for (int thola_inkomba = 0; thola_inkomba < 8; thola_inkomba++) {
        Igama[4] = '0' + thola_inkomba;
        int 열린파일 = open(Igama, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { qiniseka(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    qiniseka(개수 > 0 && 개수 < 8);
    qiniseka(unlink("slot0") == 0);
    qiniseka(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    qiniseka(close(보관[0]) == 0);
    Ihele = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    qiniseka(Ihele >= 0 && close(Ihele) == 0 && unlink("held-slot") == 0);
    for (int thola_inkomba = 1; thola_inkomba < 개수; thola_inkomba++) {
        Igama[4] = '0' + thola_inkomba;
        qiniseka(close(보관[thola_inkomba]) == 0 && unlink(Igama) == 0);
    }
    qiniseka(fsync(-1) == -1 && errno == EBADF);
    qiniseka(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
