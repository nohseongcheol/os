#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int ᎤᏍᏗᏓᏅ, int ᏚᏓᏅᏅᎢ) {
    검사항목수++;
    if (!ᎤᏍᏗᏓᏅ) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 0;
        do { 숫자[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++] = '0' + ᏚᏓᏅᏅᎢ % 10; ᏚᏓᏅᏅᎢ /= 10; } while (ᏚᏓᏅᏅᎢ);
        while (ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) putchar(숫자[--ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ]);
        putchar('\n'); _exit(1);
    }
}
#define ᎰᎯᏳᏓ(ᎤᏍᏗᏓᏅ) 검사((ᎤᏍᏗᏓᏅ), __LINE__)

int main(int 인수개수, char **ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ) {
    char ᎦᏟᏌᏅᎯ[32]; struct stat ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ;
    ᎰᎯᏳᏓ(인수개수 == 2 && strcmp(ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[1], "check") == 0 && ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[2] == 0);
    ᎰᎯᏳᏓ(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ᎰᎯᏳᏓ(ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ("absent", ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ) == -1 && 오류번호 == ENOENT);
    int ᎠᏍᏆᏂᎪᏙᏗ = ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ("/posix.txt", ᎠᎪᎵᏰᏗᏊ_ᎪᏪᎶᏗ | 새파일만들기, 0640);
    ᎰᎯᏳᏓ(ᎠᏍᏆᏂᎪᏙᏗ == 3);
    ᎰᎯᏳᏓ(ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(ᎠᏍᏆᏂᎪᏙᏗ, "abcd", 4) == 4);
    ᎰᎯᏳᏓ(ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ᎰᎯᏳᏓ(파일상태읽기(ᎠᏍᏆᏂᎪᏙᏗ, &ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ) == 0 && ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_size == 4 && S_ISREG(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_mode));
    ᎰᎯᏳᏓ((ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_mode & 0777) == 0640 && ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_nlink == 1);
    ᎰᎯᏳᏓ(파일위치옮기기(ᎠᏍᏆᏂᎪᏙᏗ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ᎠᏍᏆᏂᎪᏙᏗ);
    ᎰᎯᏳᏓ(복제 == 4);
    ᎰᎯᏳᏓ(파일자료읽기(복제, ᎦᏟᏌᏅᎯ, 2) == 2 && memcmp(ᎦᏟᏌᏅᎯ, "ab", 2) == 0);
    ᎰᎯᏳᏓ(파일자료읽기(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 2) == 2 && memcmp(ᎦᏟᏌᏅᎯ, "cd", 2) == 0);
    ᎰᎯᏳᏓ(파일자료읽기(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 1) == 0);
    ᎰᎯᏳᏓ(fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_GETFD) == 1);
    ᎰᎯᏳᏓ(fcntl(복제, F_GETFD) == 0);
    ᎰᎯᏳᏓ(dup2(ᎠᏍᏆᏂᎪᏙᏗ, ᎠᏍᏆᏂᎪᏙᏗ) == ᎠᏍᏆᏂᎪᏙᏗ && fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_GETFD) == 1);
    ᎰᎯᏳᏓ(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ᎰᎯᏳᏓ(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_GETFL) & O_APPEND));
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ᎠᏍᏆᏂᎪᏙᏗ, 0, SEEK_CUR) == 5);
    ᎰᎯᏳᏓ(fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_SETFL, 0) == 0);
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, 8, SEEK_SET) == 8 && write(ᎠᏍᏆᏂᎪᏙᏗ, "Z", 1) == 1);
    ᎰᎯᏳᏓ(lseek(복제, 5, SEEK_SET) == 5 && read(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 4) == 4);
    ᎰᎯᏳᏓ(ᎦᏟᏌᏅᎯ[0] == 0 && ᎦᏟᏌᏅᎯ[1] == 0 && ᎦᏟᏌᏅᎯ[2] == 0 && ᎦᏟᏌᏅᎯ[3] == 'Z');
    ᎰᎯᏳᏓ(ftruncate(ᎠᏍᏆᏂᎪᏙᏗ, 2) == 0 && lseek(ᎠᏍᏆᏂᎪᏙᏗ, 0, SEEK_CUR) == 9);
    ᎰᎯᏳᏓ(ftruncate(ᎠᏍᏆᏂᎪᏙᏗ, 6) == 0 && lseek(ᎠᏍᏆᏂᎪᏙᏗ, 2, SEEK_SET) == 2 && read(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 4) == 4);
    ᎰᎯᏳᏓ(!ᎦᏟᏌᏅᎯ[0] && !ᎦᏟᏌᏅᎯ[1] && !ᎦᏟᏌᏅᎯ[2] && !ᎦᏟᏌᏅᎯ[3]);
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, 2147483647, SEEK_SET) == 2147483647);
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ᎰᎯᏳᏓ(write(ᎠᏍᏆᏂᎪᏙᏗ, "!", 1) == -1 && errno == EFBIG);
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, 0, SEEK_SET) == 0);
    ᎰᎯᏳᏓ(read(ᎠᏍᏆᏂᎪᏙᏗ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ᎰᎯᏳᏓ(read(ᎠᏍᏆᏂᎪᏙᏗ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ᎰᎯᏳᏓ(write(ᎠᏍᏆᏂᎪᏙᏗ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ᎰᎯᏳᏓ(read(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, (size_t)-1) == -1 && errno == EINVAL);
    ᎰᎯᏳᏓ(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ᎰᎯᏳᏓ(fstat(ᎠᏍᏆᏂᎪᏙᏗ, (void *)0x00100000) == -1 && errno == EFAULT);
    ᎰᎯᏳᏓ(lseek(ᎠᏍᏆᏂᎪᏙᏗ, 0, SEEK_CUR) == 0);
    ᎰᎯᏳᏓ(read(ᎠᏍᏆᏂᎪᏙᏗ, NULL, 0) == 0 && write(ᎠᏍᏆᏂᎪᏙᏗ, NULL, 0) == 0);
    ᎰᎯᏳᏓ(ᎯᎲᎾ_ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ("posix.txt") == 0);
    ᎰᎯᏳᏓ(fstat(ᎠᏍᏆᏂᎪᏙᏗ, &ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ) == 0 && ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_nlink == 0 && ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ᎰᎯᏳᏓ(새파일 == 5 && fstat(새파일, &ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ) == 0 && ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_size == 0);
    ᎰᎯᏳᏓ(read(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 2) == 2 && memcmp(ᎦᏟᏌᏅᎯ, "ab", 2) == 0);
    ᎰᎯᏳᏓ(close(ᎠᏍᏆᏂᎪᏙᏗ) == 0 && close(복제) == 0 && close(새파일) == 0);
    ᎰᎯᏳᏓ(close(새파일) == -1 && errno == EBADF);
    ᎰᎯᏳᏓ(unlink("posix.txt") == 0);
    ᎠᏍᏆᏂᎪᏙᏗ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ᎰᎯᏳᏓ(ᎠᏍᏆᏂᎪᏙᏗ == 3 && fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_GETFD) == 1);
    ᎰᎯᏳᏓ(read(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 1) == -1 && errno == EBADF);
    ᎰᎯᏳᏓ(write(ᎠᏍᏆᏂᎪᏙᏗ, "keep", 4) == 4);
    for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 4; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 32; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) ᎰᎯᏳᏓ(dup(ᎠᏍᏆᏂᎪᏙᏗ) == ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
    ᎰᎯᏳᏓ(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ᎰᎯᏳᏓ(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ᎰᎯᏳᏓ(fstat(ᎠᏍᏆᏂᎪᏙᏗ, &ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ) == 0 && ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_size == 4);
    for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 3; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 32; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) ᎰᎯᏳᏓ(close(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) == 0);
    ᎰᎯᏳᏓ(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ᎠᏍᏆᏂᎪᏙᏗ = open("posix.txt", O_RDONLY);
    ᎰᎯᏳᏓ(ᎠᏍᏆᏂᎪᏙᏗ == 3 && write(ᎠᏍᏆᏂᎪᏙᏗ, ᎦᏟᏌᏅᎯ, 1) == -1 && errno == EBADF);
    ᎰᎯᏳᏓ(fcntl(ᎠᏍᏆᏂᎪᏙᏗ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ᎰᎯᏳᏓ(close(8) == 0 && close(ᎠᏍᏆᏂᎪᏙᏗ) == 0 && unlink("posix.txt") == 0);
    ᎰᎯᏳᏓ(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ᎰᎯᏳᏓ(fstat(1, &ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ) == 0 && S_ISCHR(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.st_mode));
    ᎰᎯᏳᏓ(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ᎰᎯᏳᏓ(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ᎪᏪᎵ_ᏫᏗᎦᏅᏗ; char ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ[16];
    ᎰᎯᏳᏓ(inet_pton(AF_INET, "10.0.2.2", &ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) == 1 && ntohl(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.s_addr) == 0x0a000202U);
    ᎰᎯᏳᏓ(inet_ntop(AF_INET, &ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ, sizeof ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ) == ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ && strcmp(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ, "10.0.2.2") == 0);
    ᎰᎯᏳᏓ(inet_pton(AF_INET, "256.0.0.1", &ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) == 0 && ntohl(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.s_addr) == 0x0a000202U);
    ᎰᎯᏳᏓ(inet_pton(AF_INET, "01.0.0.1", &ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) == 0);
    ᎰᎯᏳᏓ(inet_ntop(AF_INET, &ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᎠᎪᎵᏰᏗ, 3) == NULL && errno == ENOSPC);
    ᎰᎯᏳᏓ(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ᏚᏙᎥᎢ[] = "slot0";
    for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 8; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
        ᏚᏙᎥᎢ[4] = '0' + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ;
        int 열린파일 = open(ᏚᏙᎥᎢ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ᎰᎯᏳᏓ(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ᎰᎯᏳᏓ(개수 > 0 && 개수 < 8);
    ᎰᎯᏳᏓ(unlink("slot0") == 0);
    ᎰᎯᏳᏓ(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ᎰᎯᏳᏓ(close(보관[0]) == 0);
    ᎠᏍᏆᏂᎪᏙᏗ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ᎰᎯᏳᏓ(ᎠᏍᏆᏂᎪᏙᏗ >= 0 && close(ᎠᏍᏆᏂᎪᏙᏗ) == 0 && unlink("held-slot") == 0);
    for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 1; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 개수; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
        ᏚᏙᎥᎢ[4] = '0' + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ;
        ᎰᎯᏳᏓ(close(보관[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ]) == 0 && unlink(ᏚᏙᎥᎢ) == 0);
    }
    ᎰᎯᏳᏓ(fsync(-1) == -1 && errno == EBADF);
    ᎰᎯᏳᏓ(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
