#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int លក្ខខណ្ឌ, int បន្ទាត់) {
    검사항목수++;
    if (!លក្ខខណ្ឌ) {
        puts("POSIX CHECK FAILED");
        char 숫자[12]; int ប្រវែង_តំលៃ = 0;
        do { 숫자[ប្រវែង_តំលៃ++] = '0' + បន្ទាត់ % 10; បន្ទាត់ /= 10; } while (បន្ទាត់);
        while (ប្រវែង_តំលៃ) putchar(숫자[--ប្រវែង_តំលៃ]);
        putchar('\n'); _exit(1);
    }
}
#define ផ្ទៀងផ្ទាត់(លក្ខខណ្ឌ) 검사((លក្ខខណ្ឌ), __LINE__)

int main(int 인수개수, char **អាគុយម៉ង់_បញ្ជី) {
    char ទិន្នន័យ[32]; struct stat ភាព_តំលៃ;
    ផ្ទៀងផ្ទាត់(인수개수 == 2 && strcmp(អាគុយម៉ង់_បញ្ជី[1], "check") == 0 && អាគុយម៉ង់_បញ្ជី[2] == 0);
    ផ្ទៀងផ្ទាត់(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    ផ្ទៀងផ្ទាត់(បើក_ឯកសារ("absent", ដែលបានត្រឹមតែអាន_តំលៃ) == -1 && 오류번호 == ENOENT);
    int ឯកសារ = បើក_ឯកសារ("/posix.txt", អាន_សរសេរ | 새파일만들기, 0640);
    ផ្ទៀងផ្ទាត់(ឯកសារ == 3);
    ផ្ទៀងផ្ទាត់(សរសេរ_ឯកសារ_ទិន្នន័យ(ឯកសារ, "abcd", 4) == 4);
    ផ្ទៀងផ្ទាត់(បើក_ឯកសារ("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    ផ្ទៀងផ្ទាត់(파일상태읽기(ឯកសារ, &ភាព_តំលៃ) == 0 && ភាព_តំលៃ.st_size == 4 && S_ISREG(ភាព_តំលៃ.st_mode));
    ផ្ទៀងផ្ទាត់((ភាព_តំលៃ.st_mode & 0777) == 0640 && ភាព_តំលៃ.st_nlink == 1);
    ផ្ទៀងផ្ទាត់(ស្វែងរក_ឯកសារ(ឯកសារ, 0, 처음기준) == 0);
    int 복제 = 파일서술자복제(ឯកសារ);
    ផ្ទៀងផ្ទាត់(복제 == 4);
    ផ្ទៀងផ្ទាត់(파일자료읽기(복제, ទិន្នន័យ, 2) == 2 && memcmp(ទិន្នន័យ, "ab", 2) == 0);
    ផ្ទៀងផ្ទាត់(파일자료읽기(ឯកសារ, ទិន្នន័យ, 2) == 2 && memcmp(ទិន្នន័យ, "cd", 2) == 0);
    ផ្ទៀងផ្ទាត់(파일자료읽기(ឯកសារ, ទិន្នន័យ, 1) == 0);
    ផ្ទៀងផ្ទាត់(fcntl(ឯកសារ, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ឯកសារ, F_GETFD) == 1);
    ផ្ទៀងផ្ទាត់(fcntl(복제, F_GETFD) == 0);
    ផ្ទៀងផ្ទាត់(dup2(ឯកសារ, ឯកសារ) == ឯកសារ && fcntl(ឯកសារ, F_GETFD) == 1);
    ផ្ទៀងផ្ទាត់(dup2(-1, 복제) == -1 && errno == EBADF && fcntl(복제, F_GETFD) == 0);
    ផ្ទៀងផ្ទាត់(fcntl(복제, F_SETFL, O_APPEND) == 0 && (fcntl(ឯកសារ, F_GETFL) & O_APPEND));
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, 0, SEEK_SET) == 0 && write(복제, "e", 1) == 1 && lseek(ឯកសារ, 0, SEEK_CUR) == 5);
    ផ្ទៀងផ្ទាត់(fcntl(ឯកសារ, F_SETFL, 0) == 0);
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, 8, SEEK_SET) == 8 && write(ឯកសារ, "Z", 1) == 1);
    ផ្ទៀងផ្ទាត់(lseek(복제, 5, SEEK_SET) == 5 && read(ឯកសារ, ទិន្នន័យ, 4) == 4);
    ផ្ទៀងផ្ទាត់(ទិន្នន័យ[0] == 0 && ទិន្នន័យ[1] == 0 && ទិន្នន័យ[2] == 0 && ទិន្នន័យ[3] == 'Z');
    ផ្ទៀងផ្ទាត់(ftruncate(ឯកសារ, 2) == 0 && lseek(ឯកសារ, 0, SEEK_CUR) == 9);
    ផ្ទៀងផ្ទាត់(ftruncate(ឯកសារ, 6) == 0 && lseek(ឯកសារ, 2, SEEK_SET) == 2 && read(ឯកសារ, ទិន្នន័យ, 4) == 4);
    ផ្ទៀងផ្ទាត់(!ទិន្នន័យ[0] && !ទិន្នន័យ[1] && !ទិន្នន័យ[2] && !ទិន្នន័យ[3]);
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, 2147483647, SEEK_SET) == 2147483647);
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    ផ្ទៀងផ្ទាត់(write(ឯកសារ, "!", 1) == -1 && errno == EFBIG);
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, 0, SEEK_SET) == 0);
    ផ្ទៀងផ្ទាត់(read(ឯកសារ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ផ្ទៀងផ្ទាត់(read(ឯកសារ, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    ផ្ទៀងផ្ទាត់(write(ឯកសារ, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    ផ្ទៀងផ្ទាត់(read(ឯកសារ, ទិន្នន័យ, (size_t)-1) == -1 && errno == EINVAL);
    ផ្ទៀងផ្ទាត់(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    ផ្ទៀងផ្ទាត់(fstat(ឯកសារ, (void *)0x00100000) == -1 && errno == EFAULT);
    ផ្ទៀងផ្ទាត់(lseek(ឯកសារ, 0, SEEK_CUR) == 0);
    ផ្ទៀងផ្ទាត់(read(ឯកសារ, NULL, 0) == 0 && write(ឯកសារ, NULL, 0) == 0);
    ផ្ទៀងផ្ទាត់(យកចេញ_ឯកសារ_ការបញ្ចូល_ឈ្មោះ("posix.txt") == 0);
    ផ្ទៀងផ្ទាត់(fstat(ឯកសារ, &ភាព_តំលៃ) == 0 && ភាព_តំលៃ.st_nlink == 0 && ភាព_តំលៃ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    ផ្ទៀងផ្ទាត់(새파일 == 5 && fstat(새파일, &ភាព_តំលៃ) == 0 && ភាព_តំលៃ.st_size == 0);
    ផ្ទៀងផ្ទាត់(read(ឯកសារ, ទិន្នន័យ, 2) == 2 && memcmp(ទិន្នន័យ, "ab", 2) == 0);
    ផ្ទៀងផ្ទាត់(close(ឯកសារ) == 0 && close(복제) == 0 && close(새파일) == 0);
    ផ្ទៀងផ្ទាត់(close(새파일) == -1 && errno == EBADF);
    ផ្ទៀងផ្ទាត់(unlink("posix.txt") == 0);
    ឯកសារ = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    ផ្ទៀងផ្ទាត់(ឯកសារ == 3 && fcntl(ឯកសារ, F_GETFD) == 1);
    ផ្ទៀងផ្ទាត់(read(ឯកសារ, ទិន្នន័យ, 1) == -1 && errno == EBADF);
    ផ្ទៀងផ្ទាត់(write(ឯកសារ, "keep", 4) == 4);
    for (int សន្ទស្សន៏ = 4; សន្ទស្សន៏ < 32; សន្ទស្សន៏++) ផ្ទៀងផ្ទាត់(dup(ឯកសារ) == សន្ទស្សន៏);
    ផ្ទៀងផ្ទាត់(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    ផ្ទៀងផ្ទាត់(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    ផ្ទៀងផ្ទាត់(fstat(ឯកសារ, &ភាព_តំលៃ) == 0 && ភាព_តំលៃ.st_size == 4);
    for (int សន្ទស្សន៏ = 3; សន្ទស្សន៏ < 32; សន្ទស្សន៏++) ផ្ទៀងផ្ទាត់(close(សន្ទស្សន៏) == 0);
    ផ្ទៀងផ្ទាត់(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ឯកសារ = open("posix.txt", O_RDONLY);
    ផ្ទៀងផ្ទាត់(ឯកសារ == 3 && write(ឯកសារ, ទិន្នន័យ, 1) == -1 && errno == EBADF);
    ផ្ទៀងផ្ទាត់(fcntl(ឯកសារ, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    ផ្ទៀងផ្ទាត់(close(8) == 0 && close(ឯកសារ) == 0 && unlink("posix.txt") == 0);
    ផ្ទៀងផ្ទាត់(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    ផ្ទៀងផ្ទាត់(fstat(1, &ភាព_តំលៃ) == 0 && S_ISCHR(ភាព_តំលៃ.st_mode));
    ផ្ទៀងផ្ទាត់(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    ផ្ទៀងផ្ទាត់(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr អ៊ីម៉ែល; char អ៊ីម៉ែល_អត្ថបទ[16];
    ផ្ទៀងផ្ទាត់(inet_pton(AF_INET, "10.0.2.2", &អ៊ីម៉ែល) == 1 && ntohl(អ៊ីម៉ែល.s_addr) == 0x0a000202U);
    ផ្ទៀងផ្ទាត់(inet_ntop(AF_INET, &អ៊ីម៉ែល, អ៊ីម៉ែល_អត្ថបទ, sizeof អ៊ីម៉ែល_អត្ថបទ) == អ៊ីម៉ែល_អត្ថបទ && strcmp(អ៊ីម៉ែល_អត្ថបទ, "10.0.2.2") == 0);
    ផ្ទៀងផ្ទាត់(inet_pton(AF_INET, "256.0.0.1", &អ៊ីម៉ែល) == 0 && ntohl(អ៊ីម៉ែល.s_addr) == 0x0a000202U);
    ផ្ទៀងផ្ទាត់(inet_pton(AF_INET, "01.0.0.1", &អ៊ីម៉ែល) == 0);
    ផ្ទៀងផ្ទាត់(inet_ntop(AF_INET, &អ៊ីម៉ែល, អ៊ីម៉ែល_អត្ថបទ, 3) == NULL && errno == ENOSPC);
    ផ្ទៀងផ្ទាត់(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], 개수 = 0; char ឈ្មោះ[] = "slot0";
    for (int សន្ទស្សន៏ = 0; សន្ទស្សន៏ < 8; សន្ទស្សន៏++) {
        ឈ្មោះ[4] = '0' + សន្ទស្សន៏;
        int 열린파일 = open(ឈ្មោះ, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { ផ្ទៀងផ្ទាត់(errno == ENOSPC); break; }
        보관[개수++] = 열린파일;
    }
    ផ្ទៀងផ្ទាត់(개수 > 0 && 개수 < 8);
    ផ្ទៀងផ្ទាត់(unlink("slot0") == 0);
    ផ្ទៀងផ្ទាត់(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    ផ្ទៀងផ្ទាត់(close(보관[0]) == 0);
    ឯកសារ = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    ផ្ទៀងផ្ទាត់(ឯកសារ >= 0 && close(ឯកសារ) == 0 && unlink("held-slot") == 0);
    for (int សន្ទស្សន៏ = 1; សន្ទស្សន៏ < 개수; សន្ទស្សន៏++) {
        ឈ្មោះ[4] = '0' + សន្ទស្សន៏;
        ផ្ទៀងផ្ទាត់(close(보관[សន្ទស្សន៏]) == 0 && unlink(ឈ្មោះ) == 0);
    }
    ផ្ទៀងផ្ទាត់(fsync(-1) == -1 && errno == EBADF);
    ផ្ទៀងផ្ទាត់(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
