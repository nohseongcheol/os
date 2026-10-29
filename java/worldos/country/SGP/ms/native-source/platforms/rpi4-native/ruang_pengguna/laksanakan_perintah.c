#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Mula_pengguna_aplikasi(int);
int pengguna_Mula(int 전달값) {
    for (초기화함수 *data_jawatan = __init_array_start; data_jawatan < __init_array_end; data_jawatan++) (*data_jawatan)();
    int ukuran = Mula_pengguna_aplikasi(전달값);
    for (초기화함수 *data_jawatan = __fini_array_end; data_jawatan != __fini_array_start;) (*--data_jawatan)();
    return ukuran;
}
void *memset(void *data_jawatan, int VALUE, size_t pemasukan_COUNT) { unsigned char *destinasi_data = data_jawatan; while (pemasukan_COUNT--) *destinasi_data++ = VALUE; return data_jawatan; }
void *memcpy(void *destinasi_data, const void *rentetan_data, size_t pemasukan_COUNT) { unsigned char *첫째값 = destinasi_data; const unsigned char *SECOND_VALUE = rentetan_data; while (pemasukan_COUNT--) *첫째값++ = *SECOND_VALUE++; return destinasi_data; }
