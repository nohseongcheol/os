#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define gebruiker_BASE 0x02000000ul
#define gebruiker_foto_beëindig 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define gebruiker_Stapel_adres 0x02f00000ul
#define gebruiker_beëindig 0x03000000ul
#define gebruiker_bladsy_COUNT ((gebruiker_beëindig - gebruiker_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define gebruiker_data_fout (-1001)
#define 사용자실행오류 (-1002)
#define gebruiker_ongeldig_instruksie (-1003)
#define gebruiker_UITTELLING (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registreer_data[31], bevel_plaas, stand_CODE, Stapel_adres; } gebruiker_raam;
void 사용자체계준비(void);
int gebruiker_uitsondering(gebruiker_raam *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t bord_gebruiker_ry(uintptr_t);
uintptr_t bord_gebruiker_valideer(void);
uintptr_t bord_gebruikersbeheer(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
