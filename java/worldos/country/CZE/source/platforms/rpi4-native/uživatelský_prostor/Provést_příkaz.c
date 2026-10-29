#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*inicializátor_metoda)(void);
extern inicializátor_metoda __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_uživatel_program(int);
int uživatel_START(int 전달값) {
    for (inicializátor_metoda *data_pozice = __init_array_start; data_pozice < __init_array_end; data_pozice++) (*data_pozice)();
    int VÝSLEDEK = START_uživatel_program(전달값);
    for (inicializátor_metoda *data_pozice = __fini_array_end; data_pozice != __fini_array_start;) (*--data_pozice)();
    return VÝSLEDEK;
}
void *memset(void *data_pozice, int HODNOTA, size_t položka_POČET) { unsigned char *cíl_data = data_pozice; while (položka_POČET--) *cíl_data++ = HODNOTA; return data_pozice; }
void *memcpy(void *cíl_data, const void *řetězec_data, size_t položka_POČET) { unsigned char *첫째값 = cíl_data; const unsigned char *SEKUNDA_HODNOTA = řetězec_data; while (položka_POČET--) *첫째값++ = *SEKUNDA_HODNOTA++; return cíl_data; }
