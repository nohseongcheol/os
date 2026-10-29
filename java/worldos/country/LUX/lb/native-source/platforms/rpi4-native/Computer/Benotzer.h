#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define Benotzer_BASE 0x02000000ul
#define Benotzer_Bild_bëennegen 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define Benotzer_Stapel_Adress 0x02f00000ul
#define Benotzer_bëennegen 0x03000000ul
#define Benotzer_Säit_COUNT ((Benotzer_bëennegen - Benotzer_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define Benotzer_Daten_Feeler (-1001)
#define 사용자실행오류 (-1002)
#define Benotzer_ongëlteg_Instruktioun (-1003)
#define Benotzer_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registréieren_Daten[31], Befeel_positionéieren, Status_CODE, Stapel_Adress; } Benotzer_Rumm;
void 사용자체계준비(void);
int 사용자예외(Benotzer_Rumm *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Board_Benotzer_Laf(uintptr_t);
uintptr_t Board_Benotzer_validéieren(void);
uintptr_t Board_Benotzersteierelement(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
