#include <Plik_ABI.h>
#include <sieć_ABI.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void 검사(int choroba, int wiersz_wejścia) {
    검사항목수++;
    if (!choroba) {
        puts("POSIX CHECK FAILED");
        char cyfra_WARTOŚĆ[12]; int długość_WARTOŚĆ = 0;
        do { cyfra_WARTOŚĆ[długość_WARTOŚĆ++] = '0' + wiersz_wejścia % 10; wiersz_wejścia /= 10; } while (wiersz_wejścia);
        while (długość_WARTOŚĆ) putchar(cyfra_WARTOŚĆ[--długość_WARTOŚĆ]);
        putchar('\n'); _exit(1);
    }
}
#define 확인(choroba) 검사((choroba), __LINE__)

int main(int 인수개수, char **argument_Lista) {
    char dane[32]; struct stat Stan_WARTOŚĆ;
    확인(인수개수 == 2 && strcmp(argument_Lista[1], "check") == 0 && argument_Lista[2] == 0);
    확인(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    확인(otwarty_Plik("absent", tylko_do_odczytu_WARTOŚĆ) == -1 && numer_błędu == ENOENT);
    int nazwa_pliku = otwarty_Plik("/posix.txt", R_W | 새파일만들기, 0640);
    확인(nazwa_pliku == 3);
    확인(zapis_Plik_dane(nazwa_pliku, "abcd", 4) == 4);
    확인(otwarty_Plik("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    확인(파일상태읽기(nazwa_pliku, &Stan_WARTOŚĆ) == 0 && Stan_WARTOŚĆ.st_size == 4 && S_ISREG(Stan_WARTOŚĆ.st_mode));
    확인((Stan_WARTOŚĆ.st_mode & 0777) == 0640 && Stan_WARTOŚĆ.st_nlink == 1);
    확인(szukać_Plik(nazwa_pliku, 0, 처음기준) == 0);
    int klon_WARTOŚĆ = Duplikuj_Plik_deskryptor(nazwa_pliku);
    확인(klon_WARTOŚĆ == 4);
    확인(파일자료읽기(klon_WARTOŚĆ, dane, 2) == 2 && memcmp(dane, "ab", 2) == 0);
    확인(파일자료읽기(nazwa_pliku, dane, 2) == 2 && memcmp(dane, "cd", 2) == 0);
    확인(파일자료읽기(nazwa_pliku, dane, 1) == 0);
    확인(fcntl(nazwa_pliku, F_SETFD, FD_CLOEXEC) == 0 && fcntl(nazwa_pliku, F_GETFD) == 1);
    확인(fcntl(klon_WARTOŚĆ, F_GETFD) == 0);
    확인(dup2(nazwa_pliku, nazwa_pliku) == nazwa_pliku && fcntl(nazwa_pliku, F_GETFD) == 1);
    확인(dup2(-1, klon_WARTOŚĆ) == -1 && errno == EBADF && fcntl(klon_WARTOŚĆ, F_GETFD) == 0);
    확인(fcntl(klon_WARTOŚĆ, F_SETFL, O_APPEND) == 0 && (fcntl(nazwa_pliku, F_GETFL) & O_APPEND));
    확인(lseek(nazwa_pliku, 0, SEEK_SET) == 0 && write(klon_WARTOŚĆ, "e", 1) == 1 && lseek(nazwa_pliku, 0, SEEK_CUR) == 5);
    확인(fcntl(nazwa_pliku, F_SETFL, 0) == 0);
    확인(lseek(nazwa_pliku, 8, SEEK_SET) == 8 && write(nazwa_pliku, "Z", 1) == 1);
    확인(lseek(klon_WARTOŚĆ, 5, SEEK_SET) == 5 && read(nazwa_pliku, dane, 4) == 4);
    확인(dane[0] == 0 && dane[1] == 0 && dane[2] == 0 && dane[3] == 'Z');
    확인(ftruncate(nazwa_pliku, 2) == 0 && lseek(nazwa_pliku, 0, SEEK_CUR) == 9);
    확인(ftruncate(nazwa_pliku, 6) == 0 && lseek(nazwa_pliku, 2, SEEK_SET) == 2 && read(nazwa_pliku, dane, 4) == 4);
    확인(!dane[0] && !dane[1] && !dane[2] && !dane[3]);
    확인(lseek(nazwa_pliku, 2147483647, SEEK_SET) == 2147483647);
    확인(lseek(nazwa_pliku, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    확인(lseek(nazwa_pliku, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    확인(write(nazwa_pliku, "!", 1) == -1 && errno == EFBIG);
    확인(lseek(nazwa_pliku, 0, SEEK_SET) == 0);
    확인(read(nazwa_pliku, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(nazwa_pliku, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    확인(write(nazwa_pliku, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    확인(read(nazwa_pliku, dane, (size_t)-1) == -1 && errno == EINVAL);
    확인(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    확인(fstat(nazwa_pliku, (void *)0x00100000) == -1 && errno == EFAULT);
    확인(lseek(nazwa_pliku, 0, SEEK_CUR) == 0);
    확인(read(nazwa_pliku, NULL, 0) == 0 && write(nazwa_pliku, NULL, 0) == 0);
    확인(usuń_Plik_wpis_nazwa("posix.txt") == 0);
    확인(fstat(nazwa_pliku, &Stan_WARTOŚĆ) == 0 && Stan_WARTOŚĆ.st_nlink == 0 && Stan_WARTOŚĆ.st_size == 6);
    int 새파일 = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(새파일 == 5 && fstat(새파일, &Stan_WARTOŚĆ) == 0 && Stan_WARTOŚĆ.st_size == 0);
    확인(read(nazwa_pliku, dane, 2) == 2 && memcmp(dane, "ab", 2) == 0);
    확인(close(nazwa_pliku) == 0 && close(klon_WARTOŚĆ) == 0 && close(새파일) == 0);
    확인(close(새파일) == -1 && errno == EBADF);
    확인(unlink("posix.txt") == 0);
    nazwa_pliku = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    확인(nazwa_pliku == 3 && fcntl(nazwa_pliku, F_GETFD) == 1);
    확인(read(nazwa_pliku, dane, 1) == -1 && errno == EBADF);
    확인(write(nazwa_pliku, "keep", 4) == 4);
    for (int INDEKS = 4; INDEKS < 32; INDEKS++) 확인(dup(nazwa_pliku) == INDEKS);
    확인(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    확인(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    확인(fstat(nazwa_pliku, &Stan_WARTOŚĆ) == 0 && Stan_WARTOŚĆ.st_size == 4);
    for (int INDEKS = 3; INDEKS < 32; INDEKS++) 확인(close(INDEKS) == 0);
    확인(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    nazwa_pliku = open("posix.txt", O_RDONLY);
    확인(nazwa_pliku == 3 && write(nazwa_pliku, dane, 1) == -1 && errno == EBADF);
    확인(fcntl(nazwa_pliku, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    확인(close(8) == 0 && close(nazwa_pliku) == 0 && unlink("posix.txt") == 0);
    확인(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    확인(fstat(1, &Stan_WARTOŚĆ) == 0 && S_ISCHR(Stan_WARTOŚĆ.st_mode));
    확인(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    확인(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr Adres; char ADRES_SMS[16];
    확인(inet_pton(AF_INET, "10.0.2.2", &Adres) == 1 && ntohl(Adres.s_addr) == 0x0a000202U);
    확인(inet_ntop(AF_INET, &Adres, ADRES_SMS, sizeof ADRES_SMS) == ADRES_SMS && strcmp(ADRES_SMS, "10.0.2.2") == 0);
    확인(inet_pton(AF_INET, "256.0.0.1", &Adres) == 0 && ntohl(Adres.s_addr) == 0x0a000202U);
    확인(inet_pton(AF_INET, "01.0.0.1", &Adres) == 0);
    확인(inet_ntop(AF_INET, &Adres, ADRES_SMS, 3) == NULL && errno == ENOSPC);
    확인(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int 보관[8], towar_ILE_LICZB = 0; char Nazwa[] = "slot0";
    for (int INDEKS = 0; INDEKS < 8; INDEKS++) {
        Nazwa[4] = '0' + INDEKS;
        int 열린파일 = open(Nazwa, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (열린파일 < 0) { 확인(errno == ENOSPC); break; }
        보관[towar_ILE_LICZB++] = 열린파일;
    }
    확인(towar_ILE_LICZB > 0 && towar_ILE_LICZB < 8);
    확인(unlink("slot0") == 0);
    확인(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    확인(close(보관[0]) == 0);
    nazwa_pliku = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    확인(nazwa_pliku >= 0 && close(nazwa_pliku) == 0 && unlink("held-slot") == 0);
    for (int INDEKS = 1; INDEKS < towar_ILE_LICZB; INDEKS++) {
        Nazwa[4] = '0' + INDEKS;
        확인(close(보관[INDEKS]) == 0 && unlink(Nazwa) == 0);
    }
    확인(fsync(-1) == -1 && errno == EBADF);
    확인(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
