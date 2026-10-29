#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define kasutaja_BASE 0x02000000ul
#define kasutaja_pilt_lõpeta_kõne 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define kasutaja_Virn_ADDRESS 0x02f00000ul
#define kasutaja_lõpeta_kõne 0x03000000ul
#define kasutaja_leht_COUNT ((kasutaja_lõpeta_kõne - kasutaja_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define kasutaja_andmed_tõrge (-1001)
#define 사용자실행오류 (-1002)
#define 사용자잘못된명령 (-1003)
#define kasutaja_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_andmed[31], käsk_ametikoht, Olek_CODE, Virn_ADDRESS; } kasutaja_raam;
void 사용자체계준비(void);
int kasutajaerand(kasutaja_raam *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tahvel_kasutaja_sari(uintptr_t);
uintptr_t Tahvel_kasutaja_valideerima(void);
uintptr_t Tahvel_kasutusjuhtelement(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
