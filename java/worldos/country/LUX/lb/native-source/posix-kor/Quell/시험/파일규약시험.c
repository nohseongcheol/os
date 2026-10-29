#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int Bedéngung, int Zeil) {
    검사항목수++;
    if (!Bedéngung) {
        puts("POSIX CHECK FAILED");
        char Ziffer_VALUE[12]; int Längt_VALUE = 0;
        do { Ziffer_VALUE[Längt_VALUE++] = '0' + Zeil % 10; Zeil /= 10; } while (Zeil);
        while (Längt_VALUE) putchar(Ziffer_VALUE[--Längt_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define verifizéieren(Bedéngung) 검사((Bedéngung), __LINE__)

int main(int 인수개수, char **Argument_Lëscht) {
    char Daten[32]; struct stat Status_VALUE;
    verifizéieren(인수개수 == 2 && strcmp(Argument_Lëscht[1], "check") == 0 && Argument_Lëscht[2] == 0);
    verifizéieren(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verifizéieren(ariichten_Fichier("absent", schreifgeschützt_VALUE) == -1 && 오류번호 == ENOENT);
    int Fichier = ariichten_Fichier("/posix.txt", lies_schreiffäeg | 새파일만들기, 0640);
    verifizéieren(Fichier == 3);
    verifizéieren(schreiwen_Fichier_Daten(Fichier, "abcd", 4) == 4);
    verifizéieren(ariichten_Fichier("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verifizéieren(파일상태읽기(Fichier, &Status_VALUE) == 0 && Status_VALUE.st_size == 4 && S_ISREG(Status_VALUE.st_mode));
    verifizéieren((Status_VALUE.st_mode & 0777) == 0640 && Status_VALUE.st_nlink == 1);
    verifizéieren(sichen_Fichier(Fichier, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Fichier);
    verifizéieren(복제 == 4);
    verifizéieren(파일자료읽기(복제, Daten, 2) == 2 && memcmp(Daten, "ab", 2) == 0);
    verifizéieren(파일자료읽기(Fichier, Daten, 2) == 2 && memcmp(Daten, "cd", 2) == 0);
    verifizéieren(파일자료읽기(Fichier, Daten, 1) == 0);
    verifizéieren(fcntl(Fichier, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fichier, F_GETFD) == 1);
    verifizéieren(fcntl(복제, F_GETFD) == 0);
    verifizéieren(dup2(Fichier, Fichier) == Fichier && fcntl(Fichier, F_GETFD) == 1);
    verifizéieren(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    verifizéieren(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Fichier, F_GETFL) & O_APPEND));
    verifizéieren(lseek(Fichier, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Fichier, 0, SEEK_CUR) == 5);
    verifizéieren(fcntl(Fichier, F_SETFL, 0) == 0);
    verifizéieren(lseek(Fichier, 8, SEEK_SET) == 8 && write(Fichier, "Z", 1) == 1);
    verifizéieren(lseek(복제, 5, SEEK_SET) == 5 && read(Fichier, Daten, 4) == 4);
    verifizéieren(Daten[0] == 0 && Daten[1] == 0 && Daten[2] == 0 && Daten[3] == 'Z');
    verifizéieren(ftruncate(Fichier, 2) == 0 && lseek(Fichier, 0, SEEK_CUR) == 9);
    verifizéieren(ftruncate(Fichier, 6) == 0 && lseek(Fichier, 2, SEEK_SET) == 2 && read(Fichier, Daten, 4) == 4);
    verifizéieren(!Daten[0] && !Daten[1] && !Daten[2] && !Daten[3]);
    verifizéieren(lseek(Fichier, 2147483647, SEEK_SET) == 2147483647);
    verifizéieren(lseek(Fichier, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verifizéieren(lseek(Fichier, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verifizéieren(write(Fichier, "!", 1) == -1 && errno == EFBIG);
    verifizéieren(lseek(Fichier, 0, SEEK_SET) == 0);
    verifizéieren(read(Fichier, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifizéieren(read(Fichier, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verifizéieren(write(Fichier, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifizéieren(read(Fichier, Daten, (size_t)-1) == -1 && errno == EINVAL);
    verifizéieren(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verifizéieren(fstat(Fichier, (void *)0x00100000) == -1 && errno == EFAULT);
    verifizéieren(lseek(Fichier, 0, SEEK_CUR) == 0);
    verifizéieren(read(Fichier, NULL, 0) == 0 && write(Fichier, NULL, 0) == 0);
    verifizéieren(ewechhuelen_Fichier_Agab_Numm("posix.txt") == 0);
    verifizéieren(fstat(Fichier, &Status_VALUE) == 0 && Status_VALUE.st_nlink == 0 && Status_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifizéieren(새파일 == 5 && fstat(새파일, &Status_VALUE) == 0 && Status_VALUE.st_size == 0);
    verifizéieren(read(Fichier, Daten, 2) == 2 && memcmp(Daten, "ab", 2) == 0);
    verifizéieren(close(Fichier) == 0 && close(복제) == 0 && close(새파일) == 0);
    verifizéieren(close(새파일) == -1 && errno == EBADF);
    verifizéieren(unlink("posix.txt") == 0);
    Fichier = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verifizéieren(Fichier == 3 && fcntl(Fichier, F_GETFD) == 1);
    verifizéieren(read(Fichier, Daten, 1) == -1 && errno == EBADF);
    verifizéieren(write(Fichier, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verifizéieren(dup(Fichier) == INDEX);
    verifizéieren(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verifizéieren(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verifizéieren(fstat(Fichier, &Status_VALUE) == 0 && Status_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verifizéieren(close(INDEX) == 0);
    verifizéieren(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fichier = open("posix.txt", O_RDONLY);
    verifizéieren(Fichier == 3 && write(Fichier, Daten, 1) == -1 && errno == EBADF);
    verifizéieren(fcntl(Fichier, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verifizéieren(close(8) == 0 && close(Fichier) == 0 && unlink("posix.txt") == 0);
    verifizéieren(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verifizéieren(fstat(1, &Status_VALUE) == 0 && S_ISCHR(Status_VALUE.st_mode));
    verifizéieren(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verifizéieren(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Adress; char Adress_SMS[16];
    verifizéieren(inet_pton(AF_INET, "10.0.2.2", &Adress) == 1 && ntohl(Adress.s_addr) == 0x0a000202U);
    verifizéieren(inet_ntop(AF_INET, &Adress, Adress_SMS, sizeof Adress_SMS) == Adress_SMS && strcmp(Adress_SMS, "10.0.2.2") == 0);
    verifizéieren(inet_pton(AF_INET, "256.0.0.1", &Adress) == 0 && ntohl(Adress.s_addr) == 0x0a000202U);
    verifizéieren(inet_pton(AF_INET, "01.0.0.1", &Adress) == 0);
    verifizéieren(inet_ntop(AF_INET, &Adress, Adress_SMS, 3) == NULL && errno == ENOSPC);
    verifizéieren(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], Element_COUNT = 0; char Numm[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Numm[4] = '0' + INDEX;
        int 열린파일 = open(Numm, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verifizéieren(errno == ENOSPC); break; }
        보관[Element_COUNT++] = 열린파일;
    }
    verifizéieren(Element_COUNT > 0 && Element_COUNT < 8);
    verifizéieren(unlink("slot0") == 0);
    verifizéieren(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verifizéieren(close(보관[0]) == 0);
    Fichier = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifizéieren(Fichier >= 0 && close(Fichier) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < Element_COUNT; INDEX++) {
        Numm[4] = '0' + INDEX;
        verifizéieren(close(보관[INDEX]) == 0 && unlink(Numm) == 0);
    }
    verifizéieren(fsync(-1) == -1 && errno == EBADF);
    verifizéieren(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
