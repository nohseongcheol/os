#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int imo, int umgca) {
    검사항목수++;
    if (!imo) {
        puts("POSIX CHECK FAILED");
        char inani_ixabiso[12]; int ubude_ixabiso = 0;
        do { inani_ixabiso[ubude_ixabiso++] = '0' + umgca % 10; umgca /= 10; } while (umgca);
        while (ubude_ixabiso) putchar(inani_ixabiso[--ubude_ixabiso]);
        putchar('\n'); _exit(1);
    }
}
#define ngqinisisa(imo) 검사((imo), __LINE__)

int main(int 인수개수, char **isiniki_myalelo_uludwe) {
    char iingcombolo[32]; struct stat imo_ixabiso;
    ngqinisisa(인수개수 == 2 && strcmp(isiniki_myalelo_uludwe[1], "check") == 0 && isiniki_myalelo_uludwe[2] == 0);
    ngqinisisa(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ngqinisisa(vula_ifayile("absent", efundwayo_kuphela_ixabiso) == -1 && 오류번호 == ENOENT);
    int iFayili = vula_ifayile("/posix.txt", funda_bhala | 새파일만들기, 0640);
    ngqinisisa(iFayili == 3);
    ngqinisisa(bhala_ifayile_iingcombolo(iFayili, "abcd", 4) == 4);
    ngqinisisa(vula_ifayile("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ngqinisisa(파일상태읽기(iFayili, &imo_ixabiso) == 0 && imo_ixabiso.st_size == 4 && S_ISREG(imo_ixabiso.st_mode));
    ngqinisisa((imo_ixabiso.st_mode & 0777) == 0640 && imo_ixabiso.st_nlink == 1);
    ngqinisisa(khangela_ifayile(iFayili, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(iFayili);
    ngqinisisa(복제 == 4);
    ngqinisisa(파일자료읽기(복제, iingcombolo, 2) == 2 && memcmp(iingcombolo, "ab", 2) == 0);
    ngqinisisa(파일자료읽기(iFayili, iingcombolo, 2) == 2 && memcmp(iingcombolo, "cd", 2) == 0);
    ngqinisisa(파일자료읽기(iFayili, iingcombolo, 1) == 0);
    ngqinisisa(fcntl(iFayili, F_SETFD, FD_CLOEXEC) == 0 && fcntl(iFayili, F_GETFD) == 1);
    ngqinisisa(fcntl(복제, F_GETFD) == 0);
    ngqinisisa(dup2(iFayili, iFayili) == iFayili && fcntl(iFayili, F_GETFD) == 1);
    ngqinisisa(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ngqinisisa(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(iFayili, F_GETFL) & O_APPEND));
    ngqinisisa(lseek(iFayili, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(iFayili, 0, SEEK_CUR) == 5);
    ngqinisisa(fcntl(iFayili, F_SETFL, 0) == 0);
    ngqinisisa(lseek(iFayili, 8, SEEK_SET) == 8 && write(iFayili, "Z", 1) == 1);
    ngqinisisa(lseek(복제, 5, SEEK_SET) == 5 && read(iFayili, iingcombolo, 4) == 4);
    ngqinisisa(iingcombolo[0] == 0 && iingcombolo[1] == 0 && iingcombolo[2] == 0 && iingcombolo[3] == 'Z');
    ngqinisisa(ftruncate(iFayili, 2) == 0 && lseek(iFayili, 0, SEEK_CUR) == 9);
    ngqinisisa(ftruncate(iFayili, 6) == 0 && lseek(iFayili, 2, SEEK_SET) == 2 && read(iFayili, iingcombolo, 4) == 4);
    ngqinisisa(!iingcombolo[0] && !iingcombolo[1] && !iingcombolo[2] && !iingcombolo[3]);
    ngqinisisa(lseek(iFayili, 2147483647, SEEK_SET) == 2147483647);
    ngqinisisa(lseek(iFayili, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ngqinisisa(lseek(iFayili, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ngqinisisa(write(iFayili, "!", 1) == -1 && errno == EFBIG);
    ngqinisisa(lseek(iFayili, 0, SEEK_SET) == 0);
    ngqinisisa(read(iFayili, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ngqinisisa(read(iFayili, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ngqinisisa(write(iFayili, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ngqinisisa(read(iFayili, iingcombolo, (size_t)-1) == -1 && errno == EINVAL);
    ngqinisisa(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ngqinisisa(fstat(iFayili, (void *)0x00100000) == -1 && errno == EFAULT);
    ngqinisisa(lseek(iFayili, 0, SEEK_CUR) == 0);
    ngqinisisa(read(iFayili, NULL, 0) == 0 && write(iFayili, NULL, 0) == 0);
    ngqinisisa(shenxisa_ifayile_ufako_nkcukacha_igama("posix.txt") == 0);
    ngqinisisa(fstat(iFayili, &imo_ixabiso) == 0 && imo_ixabiso.st_nlink == 0 && imo_ixabiso.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ngqinisisa(새파일 == 5 && fstat(새파일, &imo_ixabiso) == 0 && imo_ixabiso.st_size == 0);
    ngqinisisa(read(iFayili, iingcombolo, 2) == 2 && memcmp(iingcombolo, "ab", 2) == 0);
    ngqinisisa(close(iFayili) == 0 && close(복제) == 0 && close(새파일) == 0);
    ngqinisisa(close(새파일) == -1 && errno == EBADF);
    ngqinisisa(unlink("posix.txt") == 0);
    iFayili = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ngqinisisa(iFayili == 3 && fcntl(iFayili, F_GETFD) == 1);
    ngqinisisa(read(iFayili, iingcombolo, 1) == -1 && errno == EBADF);
    ngqinisisa(write(iFayili, "keep", 4) == 4);
    for (int indeksa = 4; indeksa < 32; indeksa++) ngqinisisa(dup(iFayili) == indeksa);
    ngqinisisa(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ngqinisisa(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ngqinisisa(fstat(iFayili, &imo_ixabiso) == 0 && imo_ixabiso.st_size == 4);
    for (int indeksa = 3; indeksa < 32; indeksa++) ngqinisisa(close(indeksa) == 0);
    ngqinisisa(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    iFayili = open("posix.txt", O_RDONLY);
    ngqinisisa(iFayili == 3 && write(iFayili, iingcombolo, 1) == -1 && errno == EBADF);
    ngqinisisa(fcntl(iFayili, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ngqinisisa(close(8) == 0 && close(iFayili) == 0 && unlink("posix.txt") == 0);
    ngqinisisa(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ngqinisisa(fstat(1, &imo_ixabiso) == 0 && S_ISCHR(imo_ixabiso.st_mode));
    ngqinisisa(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ngqinisisa(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr idilesi; char idilesi_I_SMS[16];
    ngqinisisa(inet_pton(AF_INET, "10.0.2.2", &idilesi) == 1 && ntohl(idilesi.s_addr) == 0x0a000202U);
    ngqinisisa(inet_ntop(AF_INET, &idilesi, idilesi_I_SMS, sizeof idilesi_I_SMS) == idilesi_I_SMS && strcmp(idilesi_I_SMS, "10.0.2.2") == 0);
    ngqinisisa(inet_pton(AF_INET, "256.0.0.1", &idilesi) == 0 && ntohl(idilesi.s_addr) == 0x0a000202U);
    ngqinisisa(inet_pton(AF_INET, "01.0.0.1", &idilesi) == 0);
    ngqinisisa(inet_ntop(AF_INET, &idilesi, idilesi_I_SMS, 3) == NULL && errno == ENOSPC);
    ngqinisisa(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Igama[] = "slot0";
    for (int indeksa = 0; indeksa < 8; indeksa++) {
        Igama[4] = '0' + indeksa;
        int 열린파일 = open(Igama, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ngqinisisa(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ngqinisisa(개수 > 0 && 개수 < 8);
    ngqinisisa(unlink("slot0") == 0);
    ngqinisisa(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ngqinisisa(close(보관[0]) == 0);
    iFayili = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ngqinisisa(iFayili >= 0 && close(iFayili) == 0 && unlink("held-slot") == 0);
    for (int indeksa = 1; indeksa < 개수; indeksa++) {
        Igama[4] = '0' + indeksa;
        ngqinisisa(close(보관[indeksa]) == 0 && unlink(Igama) == 0);
    }
    ngqinisisa(fsync(-1) == -1 && errno == EBADF);
    ngqinisisa(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
