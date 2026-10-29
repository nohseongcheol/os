#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int kusht, int linjë) {
    검사항목수++;
    if (!kusht) {
        puts("POSIX CHECK FAILED");
        char shifër_VALUE[12]; int gjatësi_VALUE = 0;
        do { shifër_VALUE[gjatësi_VALUE++] = '0' + linjë % 10; linjë /= 10; } while (linjë);
        while (gjatësi_VALUE) putchar(shifër_VALUE[--gjatësi_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define verifikoj(kusht) 검사((kusht), __LINE__)

int main(int 인수개수, char **argument_Listë) {
    char të_dhëna[32]; struct stat status_VALUE;
    verifikoj(인수개수 == 2 && strcmp(argument_Listë[1], "check") == 0 && argument_Listë[2] == 0);
    verifikoj(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verifikoj(hap_skedar("absent", vetëm_për_lexim_VALUE) == -1 && 오류번호 == ENOENT);
    int Kartelë = hap_skedar("/posix.txt", lexoj_shkruaj | 새파일만들기, 0640);
    verifikoj(Kartelë == 3);
    verifikoj(shkruaj_skedar_të_dhëna(Kartelë, "abcd", 4) == 4);
    verifikoj(hap_skedar("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verifikoj(파일상태읽기(Kartelë, &status_VALUE) == 0 && status_VALUE.st_size == 4 && S_ISREG(status_VALUE.st_mode));
    verifikoj((status_VALUE.st_mode & 0777) == 0640 && status_VALUE.st_nlink == 1);
    verifikoj(kërko_skedar(Kartelë, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Kartelë);
    verifikoj(복제 == 4);
    verifikoj(파일자료읽기(복제, të_dhëna, 2) == 2 && memcmp(të_dhëna, "ab", 2) == 0);
    verifikoj(파일자료읽기(Kartelë, të_dhëna, 2) == 2 && memcmp(të_dhëna, "cd", 2) == 0);
    verifikoj(파일자료읽기(Kartelë, të_dhëna, 1) == 0);
    verifikoj(fcntl(Kartelë, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Kartelë, F_GETFD) == 1);
    verifikoj(fcntl(복제, F_GETFD) == 0);
    verifikoj(dup2(Kartelë, Kartelë) == Kartelë && fcntl(Kartelë, F_GETFD) == 1);
    verifikoj(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    verifikoj(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Kartelë, F_GETFL) & O_APPEND));
    verifikoj(lseek(Kartelë, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Kartelë, 0, SEEK_CUR) == 5);
    verifikoj(fcntl(Kartelë, F_SETFL, 0) == 0);
    verifikoj(lseek(Kartelë, 8, SEEK_SET) == 8 && write(Kartelë, "Z", 1) == 1);
    verifikoj(lseek(복제, 5, SEEK_SET) == 5 && read(Kartelë, të_dhëna, 4) == 4);
    verifikoj(të_dhëna[0] == 0 && të_dhëna[1] == 0 && të_dhëna[2] == 0 && të_dhëna[3] == 'Z');
    verifikoj(ftruncate(Kartelë, 2) == 0 && lseek(Kartelë, 0, SEEK_CUR) == 9);
    verifikoj(ftruncate(Kartelë, 6) == 0 && lseek(Kartelë, 2, SEEK_SET) == 2 && read(Kartelë, të_dhëna, 4) == 4);
    verifikoj(!të_dhëna[0] && !të_dhëna[1] && !të_dhëna[2] && !të_dhëna[3]);
    verifikoj(lseek(Kartelë, 2147483647, SEEK_SET) == 2147483647);
    verifikoj(lseek(Kartelë, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verifikoj(lseek(Kartelë, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verifikoj(write(Kartelë, "!", 1) == -1 && errno == EFBIG);
    verifikoj(lseek(Kartelë, 0, SEEK_SET) == 0);
    verifikoj(read(Kartelë, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifikoj(read(Kartelë, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verifikoj(write(Kartelë, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verifikoj(read(Kartelë, të_dhëna, (size_t)-1) == -1 && errno == EINVAL);
    verifikoj(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verifikoj(fstat(Kartelë, (void *)0x00100000) == -1 && errno == EFAULT);
    verifikoj(lseek(Kartelë, 0, SEEK_CUR) == 0);
    verifikoj(read(Kartelë, NULL, 0) == 0 && write(Kartelë, NULL, 0) == 0);
    verifikoj(heq_skedar_futje_emër("posix.txt") == 0);
    verifikoj(fstat(Kartelë, &status_VALUE) == 0 && status_VALUE.st_nlink == 0 && status_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifikoj(새파일 == 5 && fstat(새파일, &status_VALUE) == 0 && status_VALUE.st_size == 0);
    verifikoj(read(Kartelë, të_dhëna, 2) == 2 && memcmp(të_dhëna, "ab", 2) == 0);
    verifikoj(close(Kartelë) == 0 && close(복제) == 0 && close(새파일) == 0);
    verifikoj(close(새파일) == -1 && errno == EBADF);
    verifikoj(unlink("posix.txt") == 0);
    Kartelë = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verifikoj(Kartelë == 3 && fcntl(Kartelë, F_GETFD) == 1);
    verifikoj(read(Kartelë, të_dhëna, 1) == -1 && errno == EBADF);
    verifikoj(write(Kartelë, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) verifikoj(dup(Kartelë) == INDEX);
    verifikoj(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verifikoj(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verifikoj(fstat(Kartelë, &status_VALUE) == 0 && status_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) verifikoj(close(INDEX) == 0);
    verifikoj(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Kartelë = open("posix.txt", O_RDONLY);
    verifikoj(Kartelë == 3 && write(Kartelë, të_dhëna, 1) == -1 && errno == EBADF);
    verifikoj(fcntl(Kartelë, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verifikoj(close(8) == 0 && close(Kartelë) == 0 && unlink("posix.txt") == 0);
    verifikoj(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verifikoj(fstat(1, &status_VALUE) == 0 && S_ISCHR(status_VALUE.st_mode));
    verifikoj(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verifikoj(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr email; char email_SMS[16];
    verifikoj(inet_pton(AF_INET, "10.0.2.2", &email) == 1 && ntohl(email.s_addr) == 0x0a000202U);
    verifikoj(inet_ntop(AF_INET, &email, email_SMS, sizeof email_SMS) == email_SMS && strcmp(email_SMS, "10.0.2.2") == 0);
    verifikoj(inet_pton(AF_INET, "256.0.0.1", &email) == 0 && ntohl(email.s_addr) == 0x0a000202U);
    verifikoj(inet_pton(AF_INET, "01.0.0.1", &email) == 0);
    verifikoj(inet_ntop(AF_INET, &email, email_SMS, 3) == NULL && errno == ENOSPC);
    verifikoj(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], njësi_COUNT = 0; char Emër[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Emër[4] = '0' + INDEX;
        int 열린파일 = open(Emër, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { verifikoj(errno == ENOSPC); break; }
        보관[njësi_COUNT++] = 열린파일;
    }
    verifikoj(njësi_COUNT > 0 && njësi_COUNT < 8);
    verifikoj(unlink("slot0") == 0);
    verifikoj(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verifikoj(close(보관[0]) == 0);
    Kartelë = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verifikoj(Kartelë >= 0 && close(Kartelë) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < njësi_COUNT; INDEX++) {
        Emër[4] = '0' + INDEX;
        verifikoj(close(보관[INDEX]) == 0 && unlink(Emër) == 0);
    }
    verifikoj(fsync(-1) == -1 && errno == EBADF);
    verifikoj(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
