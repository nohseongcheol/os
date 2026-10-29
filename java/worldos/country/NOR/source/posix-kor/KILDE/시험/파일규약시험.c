#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int vilkår, int Linje) {
    검사항목수++;
    if (!vilkår) {
        puts("POSIX CHECK FAILED");
        char siffer_VERDI[12]; int lengde_VERDI = 0;
        do { siffer_VERDI[lengde_VERDI++] = '0' + Linje % 10; Linje /= 10; } while (Linje);
        while (lengde_VERDI) putchar(siffer_VERDI[--lengde_VERDI]);
        putchar('\n'); _exit(1);
    }
}
#define bekrefte(vilkår) 검사((vilkår), __LINE__)

int main(int 인수개수, char **argument_Liste) {
    char data[32]; struct stat status_VERDI;
    bekrefte(인수개수 == 2 && strcmp(argument_Liste[1], "check") == 0 && argument_Liste[2] == 0);
    bekrefte(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    bekrefte(åpen_Fil("absent", skrivebeskyttet_VERDI) == -1 && feilnummer == ENOENT);
    int Fil = åpen_Fil("/posix.txt", lese_og_skrive | 새파일만들기, 0640);
    bekrefte(Fil == 3);
    bekrefte(skrive_Fil_data(Fil, "abcd", 4) == 4);
    bekrefte(åpen_Fil("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    bekrefte(파일상태읽기(Fil, &status_VERDI) == 0 && status_VERDI.st_size == 4 && S_ISREG(status_VERDI.st_mode));
    bekrefte((status_VERDI.st_mode & 0777) == 0640 && status_VERDI.st_nlink == 1);
    bekrefte(søk_Fil(Fil, 0, 처음기준) == 0);
    int klon_VERDI = 파일서술자복제(Fil);
    bekrefte(klon_VERDI == 4);
    bekrefte(파일자료읽기(klon_VERDI, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    bekrefte(파일자료읽기(Fil, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    bekrefte(파일자료읽기(Fil, data, 1) == 0);
    bekrefte(fcntl(Fil, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fil, F_GETFD) == 1);
    bekrefte(fcntl(klon_VERDI, F_GETFD) == 0);
    bekrefte(dup2(Fil, Fil) == Fil && fcntl(Fil, F_GETFD) == 1);
    bekrefte(dup2(-1, klon_VERDI) == -1 && errno == EBADF && fcntl(klon_VERDI, F_GETFD) == 0);
    bekrefte(fcntl(klon_VERDI, F_SETFL, O_APPEND) == 0 && (fcntl(Fil, F_GETFL) & O_APPEND));
    bekrefte(lseek(Fil, 0, SEEK_SET) == 0 && write(klon_VERDI, "e", 1) == 1 && lseek(Fil, 0, SEEK_CUR) == 5);
    bekrefte(fcntl(Fil, F_SETFL, 0) == 0);
    bekrefte(lseek(Fil, 8, SEEK_SET) == 8 && write(Fil, "Z", 1) == 1);
    bekrefte(lseek(klon_VERDI, 5, SEEK_SET) == 5 && read(Fil, data, 4) == 4);
    bekrefte(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    bekrefte(ftruncate(Fil, 2) == 0 && lseek(Fil, 0, SEEK_CUR) == 9);
    bekrefte(ftruncate(Fil, 6) == 0 && lseek(Fil, 2, SEEK_SET) == 2 && read(Fil, data, 4) == 4);
    bekrefte(!data[0] && !data[1] && !data[2] && !data[3]);
    bekrefte(lseek(Fil, 2147483647, SEEK_SET) == 2147483647);
    bekrefte(lseek(Fil, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    bekrefte(lseek(Fil, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    bekrefte(write(Fil, "!", 1) == -1 && errno == EFBIG);
    bekrefte(lseek(Fil, 0, SEEK_SET) == 0);
    bekrefte(read(Fil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    bekrefte(read(Fil, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    bekrefte(write(Fil, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    bekrefte(read(Fil, data, (size_t)-1) == -1 && errno == EINVAL);
    bekrefte(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    bekrefte(fstat(Fil, (void *)0x00100000) == -1 && errno == EFAULT);
    bekrefte(lseek(Fil, 0, SEEK_CUR) == 0);
    bekrefte(read(Fil, NULL, 0) == 0 && write(Fil, NULL, 0) == 0);
    bekrefte(fjerne_Fil_oppføring_navn("posix.txt") == 0);
    bekrefte(fstat(Fil, &status_VERDI) == 0 && status_VERDI.st_nlink == 0 && status_VERDI.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    bekrefte(새파일 == 5 && fstat(새파일, &status_VERDI) == 0 && status_VERDI.st_size == 0);
    bekrefte(read(Fil, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    bekrefte(close(Fil) == 0 && close(klon_VERDI) == 0 && close(새파일) == 0);
    bekrefte(close(새파일) == -1 && errno == EBADF);
    bekrefte(unlink("posix.txt") == 0);
    Fil = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    bekrefte(Fil == 3 && fcntl(Fil, F_GETFD) == 1);
    bekrefte(read(Fil, data, 1) == -1 && errno == EBADF);
    bekrefte(write(Fil, "keep", 4) == 4);
    for (int INDEKS = 4; INDEKS < 32; INDEKS++) bekrefte(dup(Fil) == INDEKS);
    bekrefte(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    bekrefte(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    bekrefte(fstat(Fil, &status_VERDI) == 0 && status_VERDI.st_size == 4);
    for (int INDEKS = 3; INDEKS < 32; INDEKS++) bekrefte(close(INDEKS) == 0);
    bekrefte(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fil = open("posix.txt", O_RDONLY);
    bekrefte(Fil == 3 && write(Fil, data, 1) == -1 && errno == EBADF);
    bekrefte(fcntl(Fil, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    bekrefte(close(8) == 0 && close(Fil) == 0 && unlink("posix.txt") == 0);
    bekrefte(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    bekrefte(fstat(1, &status_VERDI) == 0 && S_ISCHR(status_VERDI.st_mode));
    bekrefte(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    bekrefte(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr e_post; char e_post_SMS[16];
    bekrefte(inet_pton(AF_INET, "10.0.2.2", &e_post) == 1 && ntohl(e_post.s_addr) == 0x0a000202U);
    bekrefte(inet_ntop(AF_INET, &e_post, e_post_SMS, sizeof e_post_SMS) == e_post_SMS && strcmp(e_post_SMS, "10.0.2.2") == 0);
    bekrefte(inet_pton(AF_INET, "256.0.0.1", &e_post) == 0 && ntohl(e_post.s_addr) == 0x0a000202U);
    bekrefte(inet_pton(AF_INET, "01.0.0.1", &e_post) == 0);
    bekrefte(inet_ntop(AF_INET, &e_post, e_post_SMS, 3) == NULL && errno == ENOSPC);
    bekrefte(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], vare_ANTALL = 0; char Navn[] = "slot0";
    for (int INDEKS = 0; INDEKS < 8; INDEKS++) {
        Navn[4] = '0' + INDEKS;
        int 열린파일 = open(Navn, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { bekrefte(errno == ENOSPC); break; }
        보관[vare_ANTALL++] = 열린파일;
    }
    bekrefte(vare_ANTALL > 0 && vare_ANTALL < 8);
    bekrefte(unlink("slot0") == 0);
    bekrefte(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    bekrefte(close(보관[0]) == 0);
    Fil = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    bekrefte(Fil >= 0 && close(Fil) == 0 && unlink("held-slot") == 0);
    for (int INDEKS = 1; INDEKS < vare_ANTALL; INDEKS++) {
        Navn[4] = '0' + INDEKS;
        bekrefte(close(보관[INDEKS]) == 0 && unlink(Navn) == 0);
    }
    bekrefte(fsync(-1) == -1 && errno == EBADF);
    bekrefte(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
