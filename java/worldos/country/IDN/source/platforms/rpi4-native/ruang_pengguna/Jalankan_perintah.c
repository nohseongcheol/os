#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Mulai_pengguna_apl(int);
int pengguna_Mulai(int 전달값) {
    for (초기화함수 *data_posisi = __init_array_start; data_posisi < __init_array_end; data_posisi++) (*data_posisi)();
    int hasil = Mulai_pengguna_apl(전달값);
    for (초기화함수 *data_posisi = __fini_array_end; data_posisi != __fini_array_start;) (*--data_posisi)();
    return hasil;
}
void *memset(void *data_posisi, int VALUE, size_t entri_COUNT) { unsigned char *tujuan_data = data_posisi; while (entri_COUNT--) *tujuan_data++ = VALUE; return data_posisi; }
void *memcpy(void *tujuan_data, const void *string_data, size_t entri_COUNT) { unsigned char *첫째값 = tujuan_data; const unsigned char *SECOND_VALUE = string_data; while (entri_COUNT--) *첫째값++ = *SECOND_VALUE++; return tujuan_data; }
