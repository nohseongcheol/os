#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*inicjator_metoda)(void);
extern inicjator_metoda __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_użytkownik_program(int);
int użytkownik_START(int 전달값) {
    for (inicjator_metoda *dane_stanowisko = __init_array_start; dane_stanowisko < __init_array_end; dane_stanowisko++) (*dane_stanowisko)();
    int WYNIK = START_użytkownik_program(전달값);
    for (inicjator_metoda *dane_stanowisko = __fini_array_end; dane_stanowisko != __fini_array_start;) (*--dane_stanowisko)();
    return WYNIK;
}
void *memset(void *dane_stanowisko, int WARTOŚĆ, size_t wpis_ILE_LICZB) { unsigned char *cel_dane = dane_stanowisko; while (wpis_ILE_LICZB--) *cel_dane++ = WARTOŚĆ; return dane_stanowisko; }
void *memcpy(void *cel_dane, const void *ciąg_dane, size_t wpis_ILE_LICZB) { unsigned char *첫째값 = cel_dane; const unsigned char *SEKUNDA_WARTOŚĆ = ciąg_dane; while (wpis_ILE_LICZB--) *첫째값++ = *SEKUNDA_WARTOŚĆ++; return cel_dane; }
