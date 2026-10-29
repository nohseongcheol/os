#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int lidelse, int Linje) {
    검사항목수++;
    if (!lidelse) {
        puts("POSIX CHECK FAILED");
        char ciffer_VÆRDI[12]; int varighed_VÆRDI = 0;
        do { ciffer_VÆRDI[varighed_VÆRDI++] = '0' + Linje % 10; Linje /= 10; } while (Linje);
        while (varighed_VÆRDI) putchar(ciffer_VÆRDI[--varighed_VÆRDI]);
        putchar('\n'); _exit(1);
    }
}
#define bekræfte(lidelse) 검사((lidelse), __LINE__)

int main(int 인수개수, char **argument_Liste) {
    char data[32]; struct stat status_VÆRDI;
    bekræfte(인수개수 == 2 && strcmp(argument_Liste[1], "check") == 0 && argument_Liste[2] == 0);
    bekræfte(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    bekræfte(åben_fil("absent", skrivebeskyttet_VÆRDI) == -1 && fejlnummer == ENOENT);
    int Fil = åben_fil("/posix.txt", læse_skrive | 새파일만들기, 0640);
    bekræfte(Fil == 3);
    bekræfte(skrive_fil_data(Fil, "abcd", 4) == 4);
    bekræfte(åben_fil("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    bekræfte(파일상태읽기(Fil, &status_VÆRDI) == 0 && status_VÆRDI.st_size == 4 && S_ISREG(status_VÆRDI.st_mode));
    bekræfte((status_VÆRDI.st_mode & 0777) == 0640 && status_VÆRDI.st_nlink == 1);
    bekræfte(søge_fil(Fil, 0, 처음기준) == 0);
    int klon_VÆRDI = 파일서술자복제(Fil);
    bekræfte(klon_VÆRDI == 4);
    bekræfte(파일자료읽기(klon_VÆRDI, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    bekræfte(파일자료읽기(Fil, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    bekræfte(파일자료읽기(Fil, data, 1) == 0);
    bekræfte(fcntl(Fil, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fil, F_GETFD) == 1);
    bekræfte(fcntl(klon_VÆRDI, F_GETFD) == 0);
    bekræfte(dup2(Fil, Fil) == Fil && fcntl(Fil, F_GETFD) == 1);
    bekræfte(dup2(-1, klon_VÆRDI) == -1 && errno == EBADF && fcntl(klon_VÆRDI, F_GETFD) == 0);
    bekræfte(fcntl(klon_VÆRDI, F_SETFL, O_APPEND) == 0 && (fcntl(Fil, F_GETFL) & O_APPEND));
    bekræfte(lseek(Fil, 0, SEEK_SET) == 0 && write(klon_VÆRDI, "e", 1) == 1 && lseek(Fil, 0, SEEK_CUR) == 5);
    bekræfte(fcntl(Fil, F_SETFL, 0) == 0);
    bekræfte(lseek(Fil, 8, SEEK_SET) == 8 && write(Fil, "Z", 1) == 1);
    bekræfte(lseek(klon_VÆRDI, 5, SEEK_SET) == 5 && read(Fil, data, 4) == 4);
    bekræfte(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    bekræfte(ftruncate(Fil, 2) == 0 && lseek(Fil, 0, SEEK_CUR) == 9);
    bekræfte(ftruncate(Fil, 6) == 0 && lseek(Fil, 2, SEEK_SET) == 2 && read(Fil, data, 4) == 4);
    bekræfte(!data[0] && !data[1] && !data[2] && !data[3]);
    bekræfte(lseek(Fil, 2147483647, SEEK_SET) == 2147483647);
    bekræfte(lseek(Fil, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    bekræfte(lseek(Fil, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    bekræfte(write(Fil, "!", 1) == -1 && errno == EFBIG);
    bekræfte(lseek(Fil, 0, SEEK_SET) == 0);
    bekræfte(read(Fil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    bekræfte(read(Fil, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    bekræfte(write(Fil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    bekræfte(read(Fil, data, (size_t)-1) == -1 && errno == EINVAL);
    bekræfte(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    bekræfte(fstat(Fil, (void *)0x00100000) == -1 && errno == EFAULT);
    bekræfte(lseek(Fil, 0, SEEK_CUR) == 0);
    bekræfte(read(Fil, NULL, 0) == 0 && write(Fil, NULL, 0) == 0);
    bekræfte(fjerne_fil_post_navn("posix.txt") == 0);
    bekræfte(fstat(Fil, &status_VÆRDI) == 0 && status_VÆRDI.st_nlink == 0 && status_VÆRDI.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    bekræfte(새파일 == 5 && fstat(새파일, &status_VÆRDI) == 0 && status_VÆRDI.st_size == 0);
    bekræfte(read(Fil, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    bekræfte(close(Fil) == 0 && close(klon_VÆRDI) == 0 && close(새파일) == 0);
    bekræfte(close(새파일) == -1 && errno == EBADF);
    bekræfte(unlink("posix.txt") == 0);
    Fil = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    bekræfte(Fil == 3 && fcntl(Fil, F_GETFD) == 1);
    bekræfte(read(Fil, data, 1) == -1 && errno == EBADF);
    bekræfte(write(Fil, "keep", 4) == 4);
    for (int INDEKS = 4; INDEKS < 32; INDEKS++) bekræfte(dup(Fil) == INDEKS);
    bekræfte(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    bekræfte(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    bekræfte(fstat(Fil, &status_VÆRDI) == 0 && status_VÆRDI.st_size == 4);
    for (int INDEKS = 3; INDEKS < 32; INDEKS++) bekræfte(close(INDEKS) == 0);
    bekræfte(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fil = open("posix.txt", O_RDONLY);
    bekræfte(Fil == 3 && write(Fil, data, 1) == -1 && errno == EBADF);
    bekræfte(fcntl(Fil, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    bekræfte(close(8) == 0 && close(Fil) == 0 && unlink("posix.txt") == 0);
    bekræfte(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    bekræfte(fstat(1, &status_VÆRDI) == 0 && S_ISCHR(status_VÆRDI.st_mode));
    bekræfte(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    bekræfte(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr mail; char mail_sms[16];
    bekræfte(inet_pton(AF_INET, "10.0.2.2", &mail) == 1 && ntohl(mail.s_addr) == 0x0a000202U);
    bekræfte(inet_ntop(AF_INET, &mail, mail_sms, sizeof mail_sms) == mail_sms && strcmp(mail_sms, "10.0.2.2") == 0);
    bekræfte(inet_pton(AF_INET, "256.0.0.1", &mail) == 0 && ntohl(mail.s_addr) == 0x0a000202U);
    bekræfte(inet_pton(AF_INET, "01.0.0.1", &mail) == 0);
    bekræfte(inet_ntop(AF_INET, &mail, mail_sms, 3) == NULL && errno == ENOSPC);
    bekræfte(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], vare_TÆL = 0; char Navn[] = "slot0";
    for (int INDEKS = 0; INDEKS < 8; INDEKS++) {
        Navn[4] = '0' + INDEKS;
        int 열린파일 = open(Navn, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { bekræfte(errno == ENOSPC); break; }
        보관[vare_TÆL++] = 열린파일;
    }
    bekræfte(vare_TÆL > 0 && vare_TÆL < 8);
    bekræfte(unlink("slot0") == 0);
    bekræfte(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    bekræfte(close(보관[0]) == 0);
    Fil = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    bekræfte(Fil >= 0 && close(Fil) == 0 && unlink("held-slot") == 0);
    for (int INDEKS = 1; INDEKS < vare_TÆL; INDEKS++) {
        Navn[4] = '0' + INDEKS;
        bekræfte(close(보관[INDEKS]) == 0 && unlink(Navn) == 0);
    }
    bekræfte(fsync(-1) == -1 && errno == EBADF);
    bekræfte(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
