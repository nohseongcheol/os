#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int cumha, int loidhne) {
    검사항목수++;
    if (!cumha) {
        puts("POSIX CHECK FAILED");
        char figear_VALUE[12]; int faid_VALUE = 0;
        do { figear_VALUE[faid_VALUE++] = '0' + loidhne % 10; loidhne /= 10; } while (loidhne);
        while (faid_VALUE) putchar(figear_VALUE[--faid_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define dearbh(cumha) 검사((cumha), __LINE__)

int main(int 인수개수, char **argamaid_Liosta) {
    char dàta[32]; struct stat cor_VALUE;
    dearbh(인수개수 == 2 && strcmp(argamaid_Liosta[1], "check") == 0 && argamaid_Liosta[2] == 0);
    dearbh(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    dearbh(fosgail_faidhle("absent", ri_leughadh_a_mhàin_VALUE) == -1 && 오류번호 == ENOENT);
    int faidhle = fosgail_faidhle("/posix.txt", so_leughte_so_sgrìobhte | 새파일만들기, 0640);
    dearbh(faidhle == 3);
    dearbh(sgrìobh_faidhle_dàta(faidhle, "abcd", 4) == 4);
    dearbh(fosgail_faidhle("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    dearbh(파일상태읽기(faidhle, &cor_VALUE) == 0 && cor_VALUE.st_size == 4 && S_ISREG(cor_VALUE.st_mode));
    dearbh((cor_VALUE.st_mode & 0777) == 0640 && cor_VALUE.st_nlink == 1);
    dearbh(sir_faidhle(faidhle, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(faidhle);
    dearbh(복제 == 4);
    dearbh(파일자료읽기(복제, dàta, 2) == 2 && memcmp(dàta, "ab", 2) == 0);
    dearbh(파일자료읽기(faidhle, dàta, 2) == 2 && memcmp(dàta, "cd", 2) == 0);
    dearbh(파일자료읽기(faidhle, dàta, 1) == 0);
    dearbh(fcntl(faidhle, F_SETFD, FD_CLOEXEC) == 0 && fcntl(faidhle, F_GETFD) == 1);
    dearbh(fcntl(복제, F_GETFD) == 0);
    dearbh(dup2(faidhle, faidhle) == faidhle && fcntl(faidhle, F_GETFD) == 1);
    dearbh(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    dearbh(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(faidhle, F_GETFL) & O_APPEND));
    dearbh(lseek(faidhle, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(faidhle, 0, SEEK_CUR) == 5);
    dearbh(fcntl(faidhle, F_SETFL, 0) == 0);
    dearbh(lseek(faidhle, 8, SEEK_SET) == 8 && write(faidhle, "Z", 1) == 1);
    dearbh(lseek(복제, 5, SEEK_SET) == 5 && read(faidhle, dàta, 4) == 4);
    dearbh(dàta[0] == 0 && dàta[1] == 0 && dàta[2] == 0 && dàta[3] == 'Z');
    dearbh(ftruncate(faidhle, 2) == 0 && lseek(faidhle, 0, SEEK_CUR) == 9);
    dearbh(ftruncate(faidhle, 6) == 0 && lseek(faidhle, 2, SEEK_SET) == 2 && read(faidhle, dàta, 4) == 4);
    dearbh(!dàta[0] && !dàta[1] && !dàta[2] && !dàta[3]);
    dearbh(lseek(faidhle, 2147483647, SEEK_SET) == 2147483647);
    dearbh(lseek(faidhle, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    dearbh(lseek(faidhle, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    dearbh(write(faidhle, "!", 1) == -1 && errno == EFBIG);
    dearbh(lseek(faidhle, 0, SEEK_SET) == 0);
    dearbh(read(faidhle, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    dearbh(read(faidhle, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    dearbh(write(faidhle, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    dearbh(read(faidhle, dàta, (size_t)-1) == -1 && errno == EINVAL);
    dearbh(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    dearbh(fstat(faidhle, (void *)0x00100000) == -1 && errno == EFAULT);
    dearbh(lseek(faidhle, 0, SEEK_CUR) == 0);
    dearbh(read(faidhle, NULL, 0) == 0 && write(faidhle, NULL, 0) == 0);
    dearbh(thoir_air_falbh_faidhle_cur_a_steach_ainm("posix.txt") == 0);
    dearbh(fstat(faidhle, &cor_VALUE) == 0 && cor_VALUE.st_nlink == 0 && cor_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    dearbh(새파일 == 5 && fstat(새파일, &cor_VALUE) == 0 && cor_VALUE.st_size == 0);
    dearbh(read(faidhle, dàta, 2) == 2 && memcmp(dàta, "ab", 2) == 0);
    dearbh(close(faidhle) == 0 && close(복제) == 0 && close(새파일) == 0);
    dearbh(close(새파일) == -1 && errno == EBADF);
    dearbh(unlink("posix.txt") == 0);
    faidhle = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    dearbh(faidhle == 3 && fcntl(faidhle, F_GETFD) == 1);
    dearbh(read(faidhle, dàta, 1) == -1 && errno == EBADF);
    dearbh(write(faidhle, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) dearbh(dup(faidhle) == INDEX);
    dearbh(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    dearbh(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    dearbh(fstat(faidhle, &cor_VALUE) == 0 && cor_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) dearbh(close(INDEX) == 0);
    dearbh(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    faidhle = open("posix.txt", O_RDONLY);
    dearbh(faidhle == 3 && write(faidhle, dàta, 1) == -1 && errno == EBADF);
    dearbh(fcntl(faidhle, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    dearbh(close(8) == 0 && close(faidhle) == 0 && unlink("posix.txt") == 0);
    dearbh(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    dearbh(fstat(1, &cor_VALUE) == 0 && S_ISCHR(cor_VALUE.st_mode));
    dearbh(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    dearbh(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADDRESS; char ADDRESS_SMS[16];
    dearbh(inet_pton(AF_INET, "10.0.2.2", &ADDRESS) == 1 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    dearbh(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, sizeof ADDRESS_SMS) == ADDRESS_SMS && strcmp(ADDRESS_SMS, "10.0.2.2") == 0);
    dearbh(inet_pton(AF_INET, "256.0.0.1", &ADDRESS) == 0 && ntohl(ADDRESS.s_addr) == 0x0a000202U);
    dearbh(inet_pton(AF_INET, "01.0.0.1", &ADDRESS) == 0);
    dearbh(inet_ntop(AF_INET, &ADDRESS, ADDRESS_SMS, 3) == NULL && errno == ENOSPC);
    dearbh(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], nì_COUNT = 0; char Ainm[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Ainm[4] = '0' + INDEX;
        int 열린파일 = open(Ainm, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { dearbh(errno == ENOSPC); break; }
        보관[nì_COUNT++] = 열린파일;
    }
    dearbh(nì_COUNT > 0 && nì_COUNT < 8);
    dearbh(unlink("slot0") == 0);
    dearbh(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    dearbh(close(보관[0]) == 0);
    faidhle = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    dearbh(faidhle >= 0 && close(faidhle) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < nì_COUNT; INDEX++) {
        Ainm[4] = '0' + INDEX;
        dearbh(close(보관[INDEX]) == 0 && unlink(Ainm) == 0);
    }
    dearbh(fsync(-1) == -1 && errno == EBADF);
    dearbh(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
