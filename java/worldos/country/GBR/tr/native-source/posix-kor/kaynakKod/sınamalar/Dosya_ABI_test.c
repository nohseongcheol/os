#include <Dosya_ABI.h>
#include <ağ_ABI.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int koşul, int girdi_satırı) {
    검사항목수++;
    if (!koşul) {
        puts("POSIX CHECK FAILED");
        char rakam_değer[12]; int süre_değer = 0;
        do { rakam_değer[süre_değer++] = '0' + girdi_satırı % 10; girdi_satırı /= 10; } while (girdi_satırı);
        while (süre_değer) putchar(rakam_değer[--süre_değer]);
        putchar('\n'); _exit(1);
    }
}
#define doğrulamak(koşul) 검사((koşul), __LINE__)

int main(int 인수개수, char **bağımsız_değişken_Liste) {
    char veri[32]; struct stat Durum_değer;
    doğrulamak(인수개수 == 2 && strcmp(bağımsız_değişken_Liste[1], "check") == 0 && bağımsız_değişken_Liste[2] == 0);
    doğrulamak(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    doğrulamak(açık_Dosya("absent", salt_okunur_değer) == -1 && hata_numarası == ENOENT);
    int dosya = açık_Dosya("/posix.txt", R_W | 새파일만들기, 0640);
    doğrulamak(dosya == 3);
    doğrulamak(yazma_Dosya_veri(dosya, "abcd", 4) == 4);
    doğrulamak(açık_Dosya("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    doğrulamak(파일상태읽기(dosya, &Durum_değer) == 0 && Durum_değer.st_size == 4 && S_ISREG(Durum_değer.st_mode));
    doğrulamak((Durum_değer.st_mode & 0777) == 0640 && Durum_değer.st_nlink == 1);
    doğrulamak(arama_Dosya(dosya, 0, 처음기준) == 0);
    int kopya_değer = kopya_Dosya_tanımlayıcı(dosya);
    doğrulamak(kopya_değer == 4);
    doğrulamak(파일자료읽기(kopya_değer, veri, 2) == 2 && memcmp(veri, "ab", 2) == 0);
    doğrulamak(파일자료읽기(dosya, veri, 2) == 2 && memcmp(veri, "cd", 2) == 0);
    doğrulamak(파일자료읽기(dosya, veri, 1) == 0);
    doğrulamak(fcntl(dosya, F_SETFD, FD_CLOEXEC) == 0 && fcntl(dosya, F_GETFD) == 1);
    doğrulamak(fcntl(kopya_değer, F_GETFD) == 0);
    doğrulamak(dup2(dosya, dosya) == dosya && fcntl(dosya, F_GETFD) == 1);
    doğrulamak(dup2(-1, kopya_değer) == -1 && errno == EBADF && fcntl(kopya_değer, F_GETFD) == 0);
    doğrulamak(fcntl(kopya_değer, F_SETFL, O_APPEND) == 0 && (fcntl(dosya, F_GETFL) & O_APPEND));
    doğrulamak(lseek(dosya, 0, SEEK_SET) == 0 && write(kopya_değer, "e", 1) == 1 && lseek(dosya, 0, SEEK_CUR) == 5);
    doğrulamak(fcntl(dosya, F_SETFL, 0) == 0);
    doğrulamak(lseek(dosya, 8, SEEK_SET) == 8 && write(dosya, "Z", 1) == 1);
    doğrulamak(lseek(kopya_değer, 5, SEEK_SET) == 5 && read(dosya, veri, 4) == 4);
    doğrulamak(veri[0] == 0 && veri[1] == 0 && veri[2] == 0 && veri[3] == 'Z');
    doğrulamak(ftruncate(dosya, 2) == 0 && lseek(dosya, 0, SEEK_CUR) == 9);
    doğrulamak(ftruncate(dosya, 6) == 0 && lseek(dosya, 2, SEEK_SET) == 2 && read(dosya, veri, 4) == 4);
    doğrulamak(!veri[0] && !veri[1] && !veri[2] && !veri[3]);
    doğrulamak(lseek(dosya, 2147483647, SEEK_SET) == 2147483647);
    doğrulamak(lseek(dosya, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    doğrulamak(lseek(dosya, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    doğrulamak(write(dosya, "!", 1) == -1 && errno == EFBIG);
    doğrulamak(lseek(dosya, 0, SEEK_SET) == 0);
    doğrulamak(read(dosya, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    doğrulamak(read(dosya, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    doğrulamak(write(dosya, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    doğrulamak(read(dosya, veri, (size_t)-1) == -1 && errno == EINVAL);
    doğrulamak(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    doğrulamak(fstat(dosya, (void *)0x00100000) == -1 && errno == EFAULT);
    doğrulamak(lseek(dosya, 0, SEEK_CUR) == 0);
    doğrulamak(read(dosya, NULL, 0) == 0 && write(dosya, NULL, 0) == 0);
    doğrulamak(kaldırmak_Dosya_girdi_ad("posix.txt") == 0);
    doğrulamak(fstat(dosya, &Durum_değer) == 0 && Durum_değer.st_nlink == 0 && Durum_değer.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    doğrulamak(새파일 == 5 && fstat(새파일, &Durum_değer) == 0 && Durum_değer.st_size == 0);
    doğrulamak(read(dosya, veri, 2) == 2 && memcmp(veri, "ab", 2) == 0);
    doğrulamak(close(dosya) == 0 && close(kopya_değer) == 0 && close(새파일) == 0);
    doğrulamak(close(새파일) == -1 && errno == EBADF);
    doğrulamak(unlink("posix.txt") == 0);
    dosya = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    doğrulamak(dosya == 3 && fcntl(dosya, F_GETFD) == 1);
    doğrulamak(read(dosya, veri, 1) == -1 && errno == EBADF);
    doğrulamak(write(dosya, "keep", 4) == 4);
    for (int Dizin = 4; Dizin < 32; Dizin++) doğrulamak(dup(dosya) == Dizin);
    doğrulamak(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    doğrulamak(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    doğrulamak(fstat(dosya, &Durum_değer) == 0 && Durum_değer.st_size == 4);
    for (int Dizin = 3; Dizin < 32; Dizin++) doğrulamak(close(Dizin) == 0);
    doğrulamak(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    dosya = open("posix.txt", O_RDONLY);
    doğrulamak(dosya == 3 && write(dosya, veri, 1) == -1 && errno == EBADF);
    doğrulamak(fcntl(dosya, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    doğrulamak(close(8) == 0 && close(dosya) == 0 && unlink("posix.txt") == 0);
    doğrulamak(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    doğrulamak(fstat(1, &Durum_değer) == 0 && S_ISCHR(Durum_değer.st_mode));
    doğrulamak(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    doğrulamak(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr ADRES; char ADRES_SMS[16];
    doğrulamak(inet_pton(AF_INET, "10.0.2.2", &ADRES) == 1 && ntohl(ADRES.s_addr) == 0x0a000202U);
    doğrulamak(inet_ntop(AF_INET, &ADRES, ADRES_SMS, sizeof ADRES_SMS) == ADRES_SMS && strcmp(ADRES_SMS, "10.0.2.2") == 0);
    doğrulamak(inet_pton(AF_INET, "256.0.0.1", &ADRES) == 0 && ntohl(ADRES.s_addr) == 0x0a000202U);
    doğrulamak(inet_pton(AF_INET, "01.0.0.1", &ADRES) == 0);
    doğrulamak(inet_ntop(AF_INET, &ADRES, ADRES_SMS, 3) == NULL && errno == ENOSPC);
    doğrulamak(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], öğe_BAĞ_DEĞ_SAY = 0; char İsim[] = "slot0";
    for (int Dizin = 0; Dizin < 8; Dizin++) {
        İsim[4] = '0' + Dizin;
        int 열린파일 = open(İsim, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { doğrulamak(errno == ENOSPC); break; }
        보관[öğe_BAĞ_DEĞ_SAY++] = 열린파일;
    }
    doğrulamak(öğe_BAĞ_DEĞ_SAY > 0 && öğe_BAĞ_DEĞ_SAY < 8);
    doğrulamak(unlink("slot0") == 0);
    doğrulamak(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    doğrulamak(close(보관[0]) == 0);
    dosya = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    doğrulamak(dosya >= 0 && close(dosya) == 0 && unlink("held-slot") == 0);
    for (int Dizin = 1; Dizin < öğe_BAĞ_DEĞ_SAY; Dizin++) {
        İsim[4] = '0' + Dizin;
        doğrulamak(close(보관[Dizin]) == 0 && unlink(İsim) == 0);
    }
    doğrulamak(fsync(-1) == -1 && errno == EBADF);
    doğrulamak(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
