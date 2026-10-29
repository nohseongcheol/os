#include <Plik_ABI.h>
#include "Połącz_granica.h"

int numer_błędu;
int 호출결과(int WYNIK) {
    if (WYNIK < 0) { numer_błędu = -WYNIK; return -1; }
    return WYNIK;
}
int open(const char *Plik_wpis_nazwa, int otwarty_Ustawienia, ...) {
    mode_t udzielenie_pozwolenie = 0;
    if (otwarty_Ustawienia & O_CREAT) {
        __builtin_va_list argumenty;
        __builtin_va_start(argumenty, otwarty_Ustawienia);
        udzielenie_pozwolenie = __builtin_va_arg(argumenty, mode_t);
        __builtin_va_end(argumenty);
    }
    return 호출결과(jkoros_syscall(30, (int)Plik_wpis_nazwa, otwarty_Ustawienia, udzielenie_pozwolenie, 0, 0));
}
int creat(const char *Plik_wpis_nazwa, mode_t udzielenie_pozwolenie) { return open(Plik_wpis_nazwa, O_WRONLY | O_CREAT | O_TRUNC, udzielenie_pozwolenie); }
ssize_t read(int Plik_deskryptor, void *dane, size_t bajt_ILE_LICZB) {
    return 호출결과(jkoros_syscall(31, Plik_deskryptor, (int)dane, bajt_ILE_LICZB, 0, 0));
}
ssize_t write(int Plik_deskryptor, const void *dane, size_t bajt_ILE_LICZB) {
    return 호출결과(jkoros_syscall(32, Plik_deskryptor, (int)dane, bajt_ILE_LICZB, 0, 0));
}
int close(int Plik_deskryptor) { return 호출결과(jkoros_syscall(33, Plik_deskryptor, 0, 0, 0, 0)); }
off_t lseek(int Plik_deskryptor, off_t przesunąć_WARTOŚĆ_450fc799, int Project_korzeń) {
    return 호출결과(jkoros_syscall(34, Plik_deskryptor, przesunąć_WARTOŚĆ_450fc799, Project_korzeń, 0, 0));
}
int dup(int Plik_deskryptor) { return 호출결과(jkoros_syscall(35, Plik_deskryptor, 0, 0, 0, 0)); }
int dup2(int Plik_deskryptor, int 새서술자) { return 호출결과(jkoros_syscall(36, Plik_deskryptor, 새서술자, 0, 0, 0)); }
int fstat(int Plik_deskryptor, struct stat *Stan_WARTOŚĆ) { return 호출결과(jkoros_syscall(37, Plik_deskryptor, (int)Stan_WARTOŚĆ, 0, 0, 0)); }
int unlink(const char *Plik_wpis_nazwa) { return 호출결과(jkoros_syscall(38, (int)Plik_wpis_nazwa, 0, 0, 0, 0)); }
int ftruncate(int Plik_deskryptor, off_t bajt_ILE_LICZB) { return 호출결과(jkoros_syscall(39, Plik_deskryptor, bajt_ILE_LICZB, 0, 0, 0)); }
int fsync(int Plik_deskryptor) { return 호출결과(jkoros_syscall(47, Plik_deskryptor, 0, 0, 0, 0)); }
int fcntl(int Plik_deskryptor, int polecenie, ...) {
    int WARTOŚĆ = 0;
    if (polecenie == F_DUPFD || polecenie == F_DUPFD_CLOEXEC || polecenie == F_SETFD || polecenie == F_SETFL) {
        __builtin_va_list argumenty;
        __builtin_va_start(argumenty, polecenie); WARTOŚĆ = __builtin_va_arg(argumenty, int); __builtin_va_end(argumenty);
    }
    return 호출결과(jkoros_syscall(40, Plik_deskryptor, polecenie, WARTOŚĆ, 0, 0));
}
