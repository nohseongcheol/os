#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ọnọdụ, int ahịrī) {
    검사항목수++;
    if (!ọnọdụ) {
        puts("POSIX CHECK FAILED");
        char ọbula_valuu[12]; int ogologo_valuu = 0;
        do { ọbula_valuu[ogologo_valuu++] = '0' + ahịrī % 10; ahịrī /= 10; } while (ahịrī);
        while (ogologo_valuu) putchar(ọbula_valuu[--ogologo_valuu]);
        putchar('\n'); _exit(1);
    }
}
#define nkwàdo_eziokwū(ọnọdụ) 검사((ọnọdụ), __LINE__)

int main(int 인수개수, char **agụment_ndepụta) {
    char datà[32]; struct stat ọnọdụ_valuu;
    nkwàdo_eziokwū(인수개수 == 2 && strcmp(agụment_ndepụta[1], "check") == 0 && agụment_ndepụta[2] == 0);
    nkwàdo_eziokwū(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    nkwàdo_eziokwū(mepee_ọbọakwụkwọ("absent", ọgụgụ_naanị_valuu) == -1 && 오류번호 == ENOENT);
    int Faịlụ = mepee_ọbọakwụkwọ("/posix.txt", gụọ_dèe | 새파일만들기, 0640);
    nkwàdo_eziokwū(Faịlụ == 3);
    nkwàdo_eziokwū(dee_ọbọakwụkwọ_datà(Faịlụ, "abcd", 4) == 4);
    nkwàdo_eziokwū(mepee_ọbọakwụkwọ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    nkwàdo_eziokwū(파일상태읽기(Faịlụ, &ọnọdụ_valuu) == 0 && ọnọdụ_valuu.st_size == 4 && S_ISREG(ọnọdụ_valuu.st_mode));
    nkwàdo_eziokwū((ọnọdụ_valuu.st_mode & 0777) == 0640 && ọnọdụ_valuu.st_nlink == 1);
    nkwàdo_eziokwū(ọchịchọ_ọbọakwụkwọ(Faịlụ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Faịlụ);
    nkwàdo_eziokwū(복제 == 4);
    nkwàdo_eziokwū(파일자료읽기(복제, datà, 2) == 2 && memcmp(datà, "ab", 2) == 0);
    nkwàdo_eziokwū(파일자료읽기(Faịlụ, datà, 2) == 2 && memcmp(datà, "cd", 2) == 0);
    nkwàdo_eziokwū(파일자료읽기(Faịlụ, datà, 1) == 0);
    nkwàdo_eziokwū(fcntl(Faịlụ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Faịlụ, F_GETFD) == 1);
    nkwàdo_eziokwū(fcntl(복제, F_GETFD) == 0);
    nkwàdo_eziokwū(dup2(Faịlụ, Faịlụ) == Faịlụ && fcntl(Faịlụ, F_GETFD) == 1);
    nkwàdo_eziokwū(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    nkwàdo_eziokwū(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Faịlụ, F_GETFL) & O_APPEND));
    nkwàdo_eziokwū(lseek(Faịlụ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Faịlụ, 0, SEEK_CUR) == 5);
    nkwàdo_eziokwū(fcntl(Faịlụ, F_SETFL, 0) == 0);
    nkwàdo_eziokwū(lseek(Faịlụ, 8, SEEK_SET) == 8 && write(Faịlụ, "Z", 1) == 1);
    nkwàdo_eziokwū(lseek(복제, 5, SEEK_SET) == 5 && read(Faịlụ, datà, 4) == 4);
    nkwàdo_eziokwū(datà[0] == 0 && datà[1] == 0 && datà[2] == 0 && datà[3] == 'Z');
    nkwàdo_eziokwū(ftruncate(Faịlụ, 2) == 0 && lseek(Faịlụ, 0, SEEK_CUR) == 9);
    nkwàdo_eziokwū(ftruncate(Faịlụ, 6) == 0 && lseek(Faịlụ, 2, SEEK_SET) == 2 && read(Faịlụ, datà, 4) == 4);
    nkwàdo_eziokwū(!datà[0] && !datà[1] && !datà[2] && !datà[3]);
    nkwàdo_eziokwū(lseek(Faịlụ, 2147483647, SEEK_SET) == 2147483647);
    nkwàdo_eziokwū(lseek(Faịlụ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    nkwàdo_eziokwū(lseek(Faịlụ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    nkwàdo_eziokwū(write(Faịlụ, "!", 1) == -1 && errno == EFBIG);
    nkwàdo_eziokwū(lseek(Faịlụ, 0, SEEK_SET) == 0);
    nkwàdo_eziokwū(read(Faịlụ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    nkwàdo_eziokwū(read(Faịlụ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    nkwàdo_eziokwū(write(Faịlụ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    nkwàdo_eziokwū(read(Faịlụ, datà, (size_t)-1) == -1 && errno == EINVAL);
    nkwàdo_eziokwū(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    nkwàdo_eziokwū(fstat(Faịlụ, (void *)0x00100000) == -1 && errno == EFAULT);
    nkwàdo_eziokwū(lseek(Faịlụ, 0, SEEK_CUR) == 0);
    nkwàdo_eziokwū(read(Faịlụ, NULL, 0) == 0 && write(Faịlụ, NULL, 0) == 0);
    nkwàdo_eziokwū(wepụ_ọbọakwụkwọ_ndebà_akara_ahà("posix.txt") == 0);
    nkwàdo_eziokwū(fstat(Faịlụ, &ọnọdụ_valuu) == 0 && ọnọdụ_valuu.st_nlink == 0 && ọnọdụ_valuu.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    nkwàdo_eziokwū(새파일 == 5 && fstat(새파일, &ọnọdụ_valuu) == 0 && ọnọdụ_valuu.st_size == 0);
    nkwàdo_eziokwū(read(Faịlụ, datà, 2) == 2 && memcmp(datà, "ab", 2) == 0);
    nkwàdo_eziokwū(close(Faịlụ) == 0 && close(복제) == 0 && close(새파일) == 0);
    nkwàdo_eziokwū(close(새파일) == -1 && errno == EBADF);
    nkwàdo_eziokwū(unlink("posix.txt") == 0);
    Faịlụ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    nkwàdo_eziokwū(Faịlụ == 3 && fcntl(Faịlụ, F_GETFD) == 1);
    nkwàdo_eziokwū(read(Faịlụ, datà, 1) == -1 && errno == EBADF);
    nkwàdo_eziokwū(write(Faịlụ, "keep", 4) == 4);
    for (int indèks = 4; indèks < 32; indèks++) nkwàdo_eziokwū(dup(Faịlụ) == indèks);
    nkwàdo_eziokwū(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    nkwàdo_eziokwū(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    nkwàdo_eziokwū(fstat(Faịlụ, &ọnọdụ_valuu) == 0 && ọnọdụ_valuu.st_size == 4);
    for (int indèks = 3; indèks < 32; indèks++) nkwàdo_eziokwū(close(indèks) == 0);
    nkwàdo_eziokwū(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Faịlụ = open("posix.txt", O_RDONLY);
    nkwàdo_eziokwū(Faịlụ == 3 && write(Faịlụ, datà, 1) == -1 && errno == EBADF);
    nkwàdo_eziokwū(fcntl(Faịlụ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    nkwàdo_eziokwū(close(8) == 0 && close(Faịlụ) == 0 && unlink("posix.txt") == 0);
    nkwàdo_eziokwū(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    nkwàdo_eziokwū(fstat(1, &ọnọdụ_valuu) == 0 && S_ISCHR(ọnọdụ_valuu.st_mode));
    nkwàdo_eziokwū(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    nkwàdo_eziokwū(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr àdreèsì; char àdreèsì_SMS[16];
    nkwàdo_eziokwū(inet_pton(AF_INET, "10.0.2.2", &àdreèsì) == 1 && ntohl(àdreèsì.s_addr) == 0x0a000202U);
    nkwàdo_eziokwū(inet_ntop(AF_INET, &àdreèsì, àdreèsì_SMS, sizeof àdreèsì_SMS) == àdreèsì_SMS && strcmp(àdreèsì_SMS, "10.0.2.2") == 0);
    nkwàdo_eziokwū(inet_pton(AF_INET, "256.0.0.1", &àdreèsì) == 0 && ntohl(àdreèsì.s_addr) == 0x0a000202U);
    nkwàdo_eziokwū(inet_pton(AF_INET, "01.0.0.1", &àdreèsì) == 0);
    nkwàdo_eziokwū(inet_ntop(AF_INET, &àdreèsì, àdreèsì_SMS, 3) == NULL && errno == ENOSPC);
    nkwàdo_eziokwū(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Aha[] = "slot0";
    for (int indèks = 0; indèks < 8; indèks++) {
        Aha[4] = '0' + indèks;
        int 열린파일 = open(Aha, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { nkwàdo_eziokwū(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    nkwàdo_eziokwū(개수 > 0 && 개수 < 8);
    nkwàdo_eziokwū(unlink("slot0") == 0);
    nkwàdo_eziokwū(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    nkwàdo_eziokwū(close(보관[0]) == 0);
    Faịlụ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    nkwàdo_eziokwū(Faịlụ >= 0 && close(Faịlụ) == 0 && unlink("held-slot") == 0);
    for (int indèks = 1; indèks < 개수; indèks++) {
        Aha[4] = '0' + indèks;
        nkwàdo_eziokwū(close(보관[indèks]) == 0 && unlink(Aha) == 0);
    }
    nkwàdo_eziokwū(fsync(-1) == -1 && errno == EBADF);
    nkwàdo_eziokwū(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
