#include <Plik_ABI.h>
#include <stdio.h>
#include <string.h>
int main(int towar_ILE_LICZB, char **wpis_Lista) {
    (void)towar_ILE_LICZB; (void)wpis_Lista;
    char dane[6]; int długość_WARTOŚĆ = 0;
    puts("POSIX INPUT READY");
    while (długość_WARTOŚĆ < 6) {
        int WYNIK = 파일자료읽기(0, dane + długość_WARTOŚĆ, 6 - długość_WARTOŚĆ);
        if (WYNIK <= 0) return 1;
        długość_WARTOŚĆ += WYNIK;
    }
    if (memcmp(dane, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
