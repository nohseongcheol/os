#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int állapot, int Vonal) {
    검사항목수++;
    if (!állapot) {
        puts("POSIX CHECK FAILED");
        char számjegy_ÉRTÉK[12]; int hossz_ÉRTÉK = 0;
        do { számjegy_ÉRTÉK[hossz_ÉRTÉK++] = '0' + Vonal % 10; Vonal /= 10; } while (Vonal);
        while (hossz_ÉRTÉK) putchar(számjegy_ÉRTÉK[--hossz_ÉRTÉK]);
        putchar('\n'); _exit(1);
    }
}
#define igazol(állapot) 검사((állapot), __LINE__)

int main(int 인수개수, char **argumentum_Lista) {
    char adat[32]; struct stat Állapot_ÉRTÉK;
    igazol(인수개수 == 2 && strcmp(argumentum_Lista[1], "check") == 0 && argumentum_Lista[2] == 0);
    igazol(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    igazol(készít_Fájl("absent", írásvédett_ÉRTÉK) == -1 && hibaszám == ENOENT);
    int Fájl = készít_Fájl("/posix.txt", 읽고쓰기 | 새파일만들기, 0640);
    igazol(Fájl == 3);
    igazol(ír_Fájl_adat(Fájl, "abcd", 4) == 4);
    igazol(készít_Fájl("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    igazol(파일상태읽기(Fájl, &Állapot_ÉRTÉK) == 0 && Állapot_ÉRTÉK.st_size == 4 && S_ISREG(Állapot_ÉRTÉK.st_mode));
    igazol((Állapot_ÉRTÉK.st_mode & 0777) == 0640 && Állapot_ÉRTÉK.st_nlink == 1);
    igazol(keres_Fájl(Fájl, 0, 처음기준) == 0);
    int klón_ÉRTÉK = 파일서술자복제(Fájl);
    igazol(klón_ÉRTÉK == 4);
    igazol(파일자료읽기(klón_ÉRTÉK, adat, 2) == 2 && memcmp(adat, "ab", 2) == 0);
    igazol(파일자료읽기(Fájl, adat, 2) == 2 && memcmp(adat, "cd", 2) == 0);
    igazol(파일자료읽기(Fájl, adat, 1) == 0);
    igazol(fcntl(Fájl, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fájl, F_GETFD) == 1);
    igazol(fcntl(klón_ÉRTÉK, F_GETFD) == 0);
    igazol(dup2(Fájl, Fájl) == Fájl && fcntl(Fájl, F_GETFD) == 1);
    igazol(dup2(-1, klón_ÉRTÉK) == -1 && errno == EBADF && fcntl(klón_ÉRTÉK, F_GETFD) == 0);
    igazol(fcntl(klón_ÉRTÉK, F_SETFL, O_APPEND) == 0 && (fcntl(Fájl, F_GETFL) & O_APPEND));
    igazol(lseek(Fájl, 0, SEEK_SET) == 0 && write(klón_ÉRTÉK, "e", 1) == 1 && lseek(Fájl, 0, SEEK_CUR) == 5);
    igazol(fcntl(Fájl, F_SETFL, 0) == 0);
    igazol(lseek(Fájl, 8, SEEK_SET) == 8 && write(Fájl, "Z", 1) == 1);
    igazol(lseek(klón_ÉRTÉK, 5, SEEK_SET) == 5 && read(Fájl, adat, 4) == 4);
    igazol(adat[0] == 0 && adat[1] == 0 && adat[2] == 0 && adat[3] == 'Z');
    igazol(ftruncate(Fájl, 2) == 0 && lseek(Fájl, 0, SEEK_CUR) == 9);
    igazol(ftruncate(Fájl, 6) == 0 && lseek(Fájl, 2, SEEK_SET) == 2 && read(Fájl, adat, 4) == 4);
    igazol(!adat[0] && !adat[1] && !adat[2] && !adat[3]);
    igazol(lseek(Fájl, 2147483647, SEEK_SET) == 2147483647);
    igazol(lseek(Fájl, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    igazol(lseek(Fájl, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    igazol(write(Fájl, "!", 1) == -1 && errno == EFBIG);
    igazol(lseek(Fájl, 0, SEEK_SET) == 0);
    igazol(read(Fájl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    igazol(read(Fájl, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    igazol(write(Fájl, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    igazol(read(Fájl, adat, (size_t)-1) == -1 && errno == EINVAL);
    igazol(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    igazol(fstat(Fájl, (void *)0x00100000) == -1 && errno == EFAULT);
    igazol(lseek(Fájl, 0, SEEK_CUR) == 0);
    igazol(read(Fájl, NULL, 0) == 0 && write(Fájl, NULL, 0) == 0);
    igazol(eltávolít_Fájl_bejegyzés_név("posix.txt") == 0);
    igazol(fstat(Fájl, &Állapot_ÉRTÉK) == 0 && Állapot_ÉRTÉK.st_nlink == 0 && Állapot_ÉRTÉK.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    igazol(새파일 == 5 && fstat(새파일, &Állapot_ÉRTÉK) == 0 && Állapot_ÉRTÉK.st_size == 0);
    igazol(read(Fájl, adat, 2) == 2 && memcmp(adat, "ab", 2) == 0);
    igazol(close(Fájl) == 0 && close(klón_ÉRTÉK) == 0 && close(새파일) == 0);
    igazol(close(새파일) == -1 && errno == EBADF);
    igazol(unlink("posix.txt") == 0);
    Fájl = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    igazol(Fájl == 3 && fcntl(Fájl, F_GETFD) == 1);
    igazol(read(Fájl, adat, 1) == -1 && errno == EBADF);
    igazol(write(Fájl, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) igazol(dup(Fájl) == INDEX);
    igazol(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    igazol(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    igazol(fstat(Fájl, &Állapot_ÉRTÉK) == 0 && Állapot_ÉRTÉK.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) igazol(close(INDEX) == 0);
    igazol(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fájl = open("posix.txt", O_RDONLY);
    igazol(Fájl == 3 && write(Fájl, adat, 1) == -1 && errno == EBADF);
    igazol(fcntl(Fájl, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    igazol(close(8) == 0 && close(Fájl) == 0 && unlink("posix.txt") == 0);
    igazol(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    igazol(fstat(1, &Állapot_ÉRTÉK) == 0 && S_ISCHR(Állapot_ÉRTÉK.st_mode));
    igazol(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    igazol(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr CÍM; char CÍM_SMS[16];
    igazol(inet_pton(AF_INET, "10.0.2.2", &CÍM) == 1 && ntohl(CÍM.s_addr) == 0x0a000202U);
    igazol(inet_ntop(AF_INET, &CÍM, CÍM_SMS, sizeof CÍM_SMS) == CÍM_SMS && strcmp(CÍM_SMS, "10.0.2.2") == 0);
    igazol(inet_pton(AF_INET, "256.0.0.1", &CÍM) == 0 && ntohl(CÍM.s_addr) == 0x0a000202U);
    igazol(inet_pton(AF_INET, "01.0.0.1", &CÍM) == 0);
    igazol(inet_ntop(AF_INET, &CÍM, CÍM_SMS, 3) == NULL && errno == ENOSPC);
    igazol(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], cikk_DARAB = 0; char Név[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Név[4] = '0' + INDEX;
        int 열린파일 = open(Név, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { igazol(errno == ENOSPC); break; }
        보관[cikk_DARAB++] = 열린파일;
    }
    igazol(cikk_DARAB > 0 && cikk_DARAB < 8);
    igazol(unlink("slot0") == 0);
    igazol(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    igazol(close(보관[0]) == 0);
    Fájl = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    igazol(Fájl >= 0 && close(Fájl) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < cikk_DARAB; INDEX++) {
        Név[4] = '0' + INDEX;
        igazol(close(보관[INDEX]) == 0 && unlink(Név) == 0);
    }
    igazol(fsync(-1) == -1 && errno == EBADF);
    igazol(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
