#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int kondisi, int baris_masukan) {
    검사항목수++;
    if (!kondisi) {
        puts("POSIX CHECK FAILED");
        char angka_VALUE[12]; int panjang_VALUE = 0;
        do { angka_VALUE[panjang_VALUE++] = '0' + baris_masukan % 10; baris_masukan /= 10; } while (baris_masukan);
        while (panjang_VALUE) putchar(angka_VALUE[--panjang_VALUE]);
        putchar('\n'); _exit(1);
    }
}
#define periksa(kondisi) 검사((kondisi), __LINE__)

int main(int 인수개수, char **argumen_Daftar) {
    char data[32]; struct stat Status_VALUE;
    periksa(인수개수 == 2 && strcmp(argumen_Daftar[1], "check") == 0 && argumen_Daftar[2] == 0);
    periksa(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    periksa(buat_file("absent", baca_saja_VALUE) == -1 && nomor_kesalahan == ENOENT);
    int berkas = buat_file("/posix.txt", baca_tulis | 새파일만들기, 0640);
    periksa(berkas == 3);
    periksa(tulis_file_data(berkas, "abcd", 4) == 4);
    periksa(buat_file("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    periksa(파일상태읽기(berkas, &Status_VALUE) == 0 && Status_VALUE.st_size == 4 && S_ISREG(Status_VALUE.st_mode));
    periksa((Status_VALUE.st_mode & 0777) == 0640 && Status_VALUE.st_nlink == 1);
    periksa(cari_file(berkas, 0, 처음기준) == 0);
    int klon_VALUE = 파일서술자복제(berkas);
    periksa(klon_VALUE == 4);
    periksa(파일자료읽기(klon_VALUE, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    periksa(파일자료읽기(berkas, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    periksa(파일자료읽기(berkas, data, 1) == 0);
    periksa(fcntl(berkas, F_SETFD, FD_CLOEXEC) == 0 && fcntl(berkas, F_GETFD) == 1);
    periksa(fcntl(klon_VALUE, F_GETFD) == 0);
    periksa(dup2(berkas, berkas) == berkas && fcntl(berkas, F_GETFD) == 1);
    periksa(dup2(-1, klon_VALUE) == -1 && errno == EBADF && fcntl(klon_VALUE, F_GETFD) == 0);
    periksa(fcntl(klon_VALUE, F_SETFL, O_APPEND) == 0 && (fcntl(berkas, F_GETFL) & O_APPEND));
    periksa(lseek(berkas, 0, SEEK_SET) == 0 && write(klon_VALUE, "e", 1) == 1 && lseek(berkas, 0, SEEK_CUR) == 5);
    periksa(fcntl(berkas, F_SETFL, 0) == 0);
    periksa(lseek(berkas, 8, SEEK_SET) == 8 && write(berkas, "Z", 1) == 1);
    periksa(lseek(klon_VALUE, 5, SEEK_SET) == 5 && read(berkas, data, 4) == 4);
    periksa(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    periksa(ftruncate(berkas, 2) == 0 && lseek(berkas, 0, SEEK_CUR) == 9);
    periksa(ftruncate(berkas, 6) == 0 && lseek(berkas, 2, SEEK_SET) == 2 && read(berkas, data, 4) == 4);
    periksa(!data[0] && !data[1] && !data[2] && !data[3]);
    periksa(lseek(berkas, 2147483647, SEEK_SET) == 2147483647);
    periksa(lseek(berkas, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    periksa(lseek(berkas, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    periksa(write(berkas, "!", 1) == -1 && errno == EFBIG);
    periksa(lseek(berkas, 0, SEEK_SET) == 0);
    periksa(read(berkas, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    periksa(read(berkas, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    periksa(write(berkas, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    periksa(read(berkas, data, (size_t)-1) == -1 && errno == EINVAL);
    periksa(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    periksa(fstat(berkas, (void *)0x00100000) == -1 && errno == EFAULT);
    periksa(lseek(berkas, 0, SEEK_CUR) == 0);
    periksa(read(berkas, NULL, 0) == 0 && write(berkas, NULL, 0) == 0);
    periksa(hapus_file_entri_nama("posix.txt") == 0);
    periksa(fstat(berkas, &Status_VALUE) == 0 && Status_VALUE.st_nlink == 0 && Status_VALUE.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    periksa(새파일 == 5 && fstat(새파일, &Status_VALUE) == 0 && Status_VALUE.st_size == 0);
    periksa(read(berkas, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    periksa(close(berkas) == 0 && close(klon_VALUE) == 0 && close(새파일) == 0);
    periksa(close(새파일) == -1 && errno == EBADF);
    periksa(unlink("posix.txt") == 0);
    berkas = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    periksa(berkas == 3 && fcntl(berkas, F_GETFD) == 1);
    periksa(read(berkas, data, 1) == -1 && errno == EBADF);
    periksa(write(berkas, "keep", 4) == 4);
    for (int INDEX = 4; INDEX < 32; INDEX++) periksa(dup(berkas) == INDEX);
    periksa(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    periksa(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    periksa(fstat(berkas, &Status_VALUE) == 0 && Status_VALUE.st_size == 4);
    for (int INDEX = 3; INDEX < 32; INDEX++) periksa(close(INDEX) == 0);
    periksa(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    berkas = open("posix.txt", O_RDONLY);
    periksa(berkas == 3 && write(berkas, data, 1) == -1 && errno == EBADF);
    periksa(fcntl(berkas, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    periksa(close(8) == 0 && close(berkas) == 0 && unlink("posix.txt") == 0);
    periksa(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    periksa(fstat(1, &Status_VALUE) == 0 && S_ISCHR(Status_VALUE.st_mode));
    periksa(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    periksa(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr surel; char surel_SMS[16];
    periksa(inet_pton(AF_INET, "10.0.2.2", &surel) == 1 && ntohl(surel.s_addr) == 0x0a000202U);
    periksa(inet_ntop(AF_INET, &surel, surel_SMS, sizeof surel_SMS) == surel_SMS && strcmp(surel_SMS, "10.0.2.2") == 0);
    periksa(inet_pton(AF_INET, "256.0.0.1", &surel) == 0 && ntohl(surel.s_addr) == 0x0a000202U);
    periksa(inet_pton(AF_INET, "01.0.0.1", &surel) == 0);
    periksa(inet_ntop(AF_INET, &surel, surel_SMS, 3) == NULL && errno == ENOSPC);
    periksa(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], item_COUNT = 0; char Nama_2[] = "slot0";
    for (int INDEX = 0; INDEX < 8; INDEX++) {
        Nama_2[4] = '0' + INDEX;
        int 열린파일 = open(Nama_2, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { periksa(errno == ENOSPC); break; }
        보관[item_COUNT++] = 열린파일;
    }
    periksa(item_COUNT > 0 && item_COUNT < 8);
    periksa(unlink("slot0") == 0);
    periksa(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    periksa(close(보관[0]) == 0);
    berkas = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    periksa(berkas >= 0 && close(berkas) == 0 && unlink("held-slot") == 0);
    for (int INDEX = 1; INDEX < item_COUNT; INDEX++) {
        Nama_2[4] = '0' + INDEX;
        periksa(close(보관[INDEX]) == 0 && unlink(Nama_2) == 0);
    }
    periksa(fsync(-1) == -1 && errno == EBADF);
    periksa(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
