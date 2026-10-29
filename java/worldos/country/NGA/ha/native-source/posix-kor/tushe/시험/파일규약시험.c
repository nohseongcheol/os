#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int Yanayi, int Layi) {
    검사항목수++;
    if (!Yanayi) {
        puts("POSIX CHECK FAILED");
        char lamba_Daraja[12]; int Tsawo_Daraja = 0;
        do { lamba_Daraja[Tsawo_Daraja++] = '0' + Layi % 10; Layi /= 10; } while (Layi);
        while (Tsawo_Daraja) putchar(lamba_Daraja[--Tsawo_Daraja]);
        putchar('\n'); _exit(1);
    }
}
#define Tabbatar_da(Yanayi) 검사((Yanayi), __LINE__)

int main(int 인수개수, char **Tubalin_aiki_Jeri) {
    char Tarin_bayani[32]; struct stat Matsayi_Daraja;
    Tabbatar_da(인수개수 == 2 && strcmp(Tubalin_aiki_Jeri[1], "check") == 0 && Tubalin_aiki_Jeri[2] == 0);
    Tabbatar_da(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    Tabbatar_da(buɗe_Fayil("absent", karanta_kawai_Daraja) == -1 && 오류번호 == ENOENT);
    int Fayil = buɗe_Fayil("/posix.txt", Rubutuwa_karantuwa | 새파일만들기, 0640);
    Tabbatar_da(Fayil == 3);
    Tabbatar_da(Rubuta_Fayil_Tarin_bayani(Fayil, "abcd", 4) == 4);
    Tabbatar_da(buɗe_Fayil("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    Tabbatar_da(파일상태읽기(Fayil, &Matsayi_Daraja) == 0 && Matsayi_Daraja.st_size == 4 && S_ISREG(Matsayi_Daraja.st_mode));
    Tabbatar_da((Matsayi_Daraja.st_mode & 0777) == 0640 && Matsayi_Daraja.st_nlink == 1);
    Tabbatar_da(binciko_Fayil(Fayil, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Fayil);
    Tabbatar_da(복제 == 4);
    Tabbatar_da(파일자료읽기(복제, Tarin_bayani, 2) == 2 && memcmp(Tarin_bayani, "ab", 2) == 0);
    Tabbatar_da(파일자료읽기(Fayil, Tarin_bayani, 2) == 2 && memcmp(Tarin_bayani, "cd", 2) == 0);
    Tabbatar_da(파일자료읽기(Fayil, Tarin_bayani, 1) == 0);
    Tabbatar_da(fcntl(Fayil, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fayil, F_GETFD) == 1);
    Tabbatar_da(fcntl(복제, F_GETFD) == 0);
    Tabbatar_da(dup2(Fayil, Fayil) == Fayil && fcntl(Fayil, F_GETFD) == 1);
    Tabbatar_da(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    Tabbatar_da(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Fayil, F_GETFL) & O_APPEND));
    Tabbatar_da(lseek(Fayil, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Fayil, 0, SEEK_CUR) == 5);
    Tabbatar_da(fcntl(Fayil, F_SETFL, 0) == 0);
    Tabbatar_da(lseek(Fayil, 8, SEEK_SET) == 8 && write(Fayil, "Z", 1) == 1);
    Tabbatar_da(lseek(복제, 5, SEEK_SET) == 5 && read(Fayil, Tarin_bayani, 4) == 4);
    Tabbatar_da(Tarin_bayani[0] == 0 && Tarin_bayani[1] == 0 && Tarin_bayani[2] == 0 && Tarin_bayani[3] == 'Z');
    Tabbatar_da(ftruncate(Fayil, 2) == 0 && lseek(Fayil, 0, SEEK_CUR) == 9);
    Tabbatar_da(ftruncate(Fayil, 6) == 0 && lseek(Fayil, 2, SEEK_SET) == 2 && read(Fayil, Tarin_bayani, 4) == 4);
    Tabbatar_da(!Tarin_bayani[0] && !Tarin_bayani[1] && !Tarin_bayani[2] && !Tarin_bayani[3]);
    Tabbatar_da(lseek(Fayil, 2147483647, SEEK_SET) == 2147483647);
    Tabbatar_da(lseek(Fayil, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    Tabbatar_da(lseek(Fayil, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    Tabbatar_da(write(Fayil, "!", 1) == -1 && errno == EFBIG);
    Tabbatar_da(lseek(Fayil, 0, SEEK_SET) == 0);
    Tabbatar_da(read(Fayil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    Tabbatar_da(read(Fayil, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    Tabbatar_da(write(Fayil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    Tabbatar_da(read(Fayil, Tarin_bayani, (size_t)-1) == -1 && errno == EINVAL);
    Tabbatar_da(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    Tabbatar_da(fstat(Fayil, (void *)0x00100000) == -1 && errno == EFAULT);
    Tabbatar_da(lseek(Fayil, 0, SEEK_CUR) == 0);
    Tabbatar_da(read(Fayil, NULL, 0) == 0 && write(Fayil, NULL, 0) == 0);
    Tabbatar_da(Cire_Fayil_Mashigar_bayanai_Suna("posix.txt") == 0);
    Tabbatar_da(fstat(Fayil, &Matsayi_Daraja) == 0 && Matsayi_Daraja.st_nlink == 0 && Matsayi_Daraja.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    Tabbatar_da(새파일 == 5 && fstat(새파일, &Matsayi_Daraja) == 0 && Matsayi_Daraja.st_size == 0);
    Tabbatar_da(read(Fayil, Tarin_bayani, 2) == 2 && memcmp(Tarin_bayani, "ab", 2) == 0);
    Tabbatar_da(close(Fayil) == 0 && close(복제) == 0 && close(새파일) == 0);
    Tabbatar_da(close(새파일) == -1 && errno == EBADF);
    Tabbatar_da(unlink("posix.txt") == 0);
    Fayil = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    Tabbatar_da(Fayil == 3 && fcntl(Fayil, F_GETFD) == 1);
    Tabbatar_da(read(Fayil, Tarin_bayani, 1) == -1 && errno == EBADF);
    Tabbatar_da(write(Fayil, "keep", 4) == 4);
    for (int Indes = 4; Indes < 32; Indes++) Tabbatar_da(dup(Fayil) == Indes);
    Tabbatar_da(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    Tabbatar_da(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    Tabbatar_da(fstat(Fayil, &Matsayi_Daraja) == 0 && Matsayi_Daraja.st_size == 4);
    for (int Indes = 3; Indes < 32; Indes++) Tabbatar_da(close(Indes) == 0);
    Tabbatar_da(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fayil = open("posix.txt", O_RDONLY);
    Tabbatar_da(Fayil == 3 && write(Fayil, Tarin_bayani, 1) == -1 && errno == EBADF);
    Tabbatar_da(fcntl(Fayil, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    Tabbatar_da(close(8) == 0 && close(Fayil) == 0 && unlink("posix.txt") == 0);
    Tabbatar_da(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    Tabbatar_da(fstat(1, &Matsayi_Daraja) == 0 && S_ISCHR(Matsayi_Daraja.st_mode));
    Tabbatar_da(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    Tabbatar_da(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr imel; char imel_SMS[16];
    Tabbatar_da(inet_pton(AF_INET, "10.0.2.2", &imel) == 1 && ntohl(imel.s_addr) == 0x0a000202U);
    Tabbatar_da(inet_ntop(AF_INET, &imel, imel_SMS, sizeof imel_SMS) == imel_SMS && strcmp(imel_SMS, "10.0.2.2") == 0);
    Tabbatar_da(inet_pton(AF_INET, "256.0.0.1", &imel) == 0 && ntohl(imel.s_addr) == 0x0a000202U);
    Tabbatar_da(inet_pton(AF_INET, "01.0.0.1", &imel) == 0);
    Tabbatar_da(inet_ntop(AF_INET, &imel, imel_SMS, 3) == NULL && errno == ENOSPC);
    Tabbatar_da(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Suna[] = "slot0";
    for (int Indes = 0; Indes < 8; Indes++) {
        Suna[4] = '0' + Indes;
        int 열린파일 = open(Suna, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { Tabbatar_da(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    Tabbatar_da(개수 > 0 && 개수 < 8);
    Tabbatar_da(unlink("slot0") == 0);
    Tabbatar_da(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    Tabbatar_da(close(보관[0]) == 0);
    Fayil = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    Tabbatar_da(Fayil >= 0 && close(Fayil) == 0 && unlink("held-slot") == 0);
    for (int Indes = 1; Indes < 개수; Indes++) {
        Suna[4] = '0' + Indes;
        Tabbatar_da(close(보관[Indes]) == 0 && unlink(Suna) == 0);
    }
    Tabbatar_da(fsync(-1) == -1 && errno == EBADF);
    Tabbatar_da(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
