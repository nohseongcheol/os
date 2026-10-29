#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int kání, int ìlà) {
    검사항목수++;
    if (!kání) {
        puts("POSIX CHECK FAILED");
        char díjììtì_iye[12]; int gígùn_iye = 0;
        do { díjììtì_iye[gígùn_iye++] = '0' + ìlà % 10; ìlà /= 10; } while (ìlà);
        while (gígùn_iye) putchar(díjììtì_iye[--gígùn_iye]);
        putchar('\n'); _exit(1);
    }
}
#define ridájú(kání) 검사((kání), __LINE__)

int main(int 인수개수, char **ágúmẹ́ntì_Àtòkọ) {
    char détà[32]; struct stat ipò_iye;
    ridájú(인수개수 == 2 && strcmp(ágúmẹ́ntì_Àtòkọ[1], "check") == 0 && ágúmẹ́ntì_Àtòkọ[2] == 0);
    ridájú(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ridájú(ṣí_fáìlì("absent", kàn_kàá_iye) == -1 && 오류번호 == ENOENT);
    int Fáìlì = ṣí_fáìlì("/posix.txt", tí_a_lè_kà_tí_a_lè_kọ | 새파일만들기, 0640);
    ridájú(Fáìlì == 3);
    ridájú(kọ_fáìlì_détà(Fáìlì, "abcd", 4) == 4);
    ridájú(ṣí_fáìlì("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ridájú(파일상태읽기(Fáìlì, &ipò_iye) == 0 && ipò_iye.st_size == 4 && S_ISREG(ipò_iye.st_mode));
    ridájú((ipò_iye.st_mode & 0777) == 0640 && ipò_iye.st_nlink == 1);
    ridájú(ṣàwárí_fáìlì(Fáìlì, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(Fáìlì);
    ridájú(복제 == 4);
    ridájú(파일자료읽기(복제, détà, 2) == 2 && memcmp(détà, "ab", 2) == 0);
    ridájú(파일자료읽기(Fáìlì, détà, 2) == 2 && memcmp(détà, "cd", 2) == 0);
    ridájú(파일자료읽기(Fáìlì, détà, 1) == 0);
    ridájú(fcntl(Fáìlì, F_SETFD, FD_CLOEXEC) == 0 && fcntl(Fáìlì, F_GETFD) == 1);
    ridájú(fcntl(복제, F_GETFD) == 0);
    ridájú(dup2(Fáìlì, Fáìlì) == Fáìlì && fcntl(Fáìlì, F_GETFD) == 1);
    ridájú(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ridájú(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(Fáìlì, F_GETFL) & O_APPEND));
    ridájú(lseek(Fáìlì, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(Fáìlì, 0, SEEK_CUR) == 5);
    ridájú(fcntl(Fáìlì, F_SETFL, 0) == 0);
    ridájú(lseek(Fáìlì, 8, SEEK_SET) == 8 && write(Fáìlì, "Z", 1) == 1);
    ridájú(lseek(복제, 5, SEEK_SET) == 5 && read(Fáìlì, détà, 4) == 4);
    ridájú(détà[0] == 0 && détà[1] == 0 && détà[2] == 0 && détà[3] == 'Z');
    ridájú(ftruncate(Fáìlì, 2) == 0 && lseek(Fáìlì, 0, SEEK_CUR) == 9);
    ridájú(ftruncate(Fáìlì, 6) == 0 && lseek(Fáìlì, 2, SEEK_SET) == 2 && read(Fáìlì, détà, 4) == 4);
    ridájú(!détà[0] && !détà[1] && !détà[2] && !détà[3]);
    ridájú(lseek(Fáìlì, 2147483647, SEEK_SET) == 2147483647);
    ridájú(lseek(Fáìlì, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ridájú(lseek(Fáìlì, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ridájú(write(Fáìlì, "!", 1) == -1 && errno == EFBIG);
    ridájú(lseek(Fáìlì, 0, SEEK_SET) == 0);
    ridájú(read(Fáìlì, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ridájú(read(Fáìlì, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ridájú(write(Fáìlì, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ridájú(read(Fáìlì, détà, (size_t)-1) == -1 && errno == EINVAL);
    ridájú(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ridájú(fstat(Fáìlì, (void *)0x00100000) == -1 && errno == EFAULT);
    ridájú(lseek(Fáìlì, 0, SEEK_CUR) == 0);
    ridájú(read(Fáìlì, NULL, 0) == 0 && write(Fáìlì, NULL, 0) == 0);
    ridájú(ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ("posix.txt") == 0);
    ridájú(fstat(Fáìlì, &ipò_iye) == 0 && ipò_iye.st_nlink == 0 && ipò_iye.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ridájú(새파일 == 5 && fstat(새파일, &ipò_iye) == 0 && ipò_iye.st_size == 0);
    ridájú(read(Fáìlì, détà, 2) == 2 && memcmp(détà, "ab", 2) == 0);
    ridájú(close(Fáìlì) == 0 && close(복제) == 0 && close(새파일) == 0);
    ridájú(close(새파일) == -1 && errno == EBADF);
    ridájú(unlink("posix.txt") == 0);
    Fáìlì = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ridájú(Fáìlì == 3 && fcntl(Fáìlì, F_GETFD) == 1);
    ridájú(read(Fáìlì, détà, 1) == -1 && errno == EBADF);
    ridájú(write(Fáìlì, "keep", 4) == 4);
    for (int wá_atọ̀ka_àkóónú = 4; wá_atọ̀ka_àkóónú < 32; wá_atọ̀ka_àkóónú++) ridájú(dup(Fáìlì) == wá_atọ̀ka_àkóónú);
    ridájú(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ridájú(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ridájú(fstat(Fáìlì, &ipò_iye) == 0 && ipò_iye.st_size == 4);
    for (int wá_atọ̀ka_àkóónú = 3; wá_atọ̀ka_àkóónú < 32; wá_atọ̀ka_àkóónú++) ridájú(close(wá_atọ̀ka_àkóónú) == 0);
    ridájú(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    Fáìlì = open("posix.txt", O_RDONLY);
    ridájú(Fáìlì == 3 && write(Fáìlì, détà, 1) == -1 && errno == EBADF);
    ridájú(fcntl(Fáìlì, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ridájú(close(8) == 0 && close(Fáìlì) == 0 && unlink("posix.txt") == 0);
    ridájú(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ridájú(fstat(1, &ipò_iye) == 0 && S_ISCHR(ipò_iye.st_mode));
    ridájú(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ridájú(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr àdírẹ́ẹ̀sì; char àdírẹ́ẹ̀sì_SMS[16];
    ridájú(inet_pton(AF_INET, "10.0.2.2", &àdírẹ́ẹ̀sì) == 1 && ntohl(àdírẹ́ẹ̀sì.s_addr) == 0x0a000202U);
    ridájú(inet_ntop(AF_INET, &àdírẹ́ẹ̀sì, àdírẹ́ẹ̀sì_SMS, sizeof àdírẹ́ẹ̀sì_SMS) == àdírẹ́ẹ̀sì_SMS && strcmp(àdírẹ́ẹ̀sì_SMS, "10.0.2.2") == 0);
    ridájú(inet_pton(AF_INET, "256.0.0.1", &àdírẹ́ẹ̀sì) == 0 && ntohl(àdírẹ́ẹ̀sì.s_addr) == 0x0a000202U);
    ridájú(inet_pton(AF_INET, "01.0.0.1", &àdírẹ́ẹ̀sì) == 0);
    ridájú(inet_ntop(AF_INET, &àdírẹ́ẹ̀sì, àdírẹ́ẹ̀sì_SMS, 3) == NULL && errno == ENOSPC);
    ridájú(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char Orúkọ[] = "slot0";
    for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 8; wá_atọ̀ka_àkóónú++) {
        Orúkọ[4] = '0' + wá_atọ̀ka_àkóónú;
        int 열린파일 = open(Orúkọ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ridájú(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ridájú(개수 > 0 && 개수 < 8);
    ridájú(unlink("slot0") == 0);
    ridájú(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ridájú(close(보관[0]) == 0);
    Fáìlì = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ridájú(Fáìlì >= 0 && close(Fáìlì) == 0 && unlink("held-slot") == 0);
    for (int wá_atọ̀ka_àkóónú = 1; wá_atọ̀ka_àkóónú < 개수; wá_atọ̀ka_àkóónú++) {
        Orúkọ[4] = '0' + wá_atọ̀ka_àkóónú;
        ridájú(close(보관[wá_atọ̀ka_àkóónú]) == 0 && unlink(Orúkọ) == 0);
    }
    ridájú(fsync(-1) == -1 && errno == EBADF);
    ridájú(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
