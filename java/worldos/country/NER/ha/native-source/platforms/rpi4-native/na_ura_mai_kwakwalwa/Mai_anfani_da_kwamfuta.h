#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define Mai_anfani_da_kwamfuta_Hoto_Ƙarshe 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define Mai_anfani_da_kwamfuta_tara_imel 0x02f00000ul
#define Mai_anfani_da_kwamfuta_Ƙarshe 0x03000000ul
#define 사용자쪽수 ((Mai_anfani_da_kwamfuta_Ƙarshe - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define Mai_anfani_da_kwamfuta_Tarin_bayani_Kuskure (-1001)
#define 사용자실행오류 (-1002)
#define Mai_anfani_da_kwamfuta_mara_ƙarfi_Sharadi (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t 저장기값[31], 명령위치, Matsayi_lambar_sirri, tara_imel; } Mai_anfani_da_kwamfuta_allo;
void 사용자체계준비(void);
int Mai_anfani_da_kwamfuta_banbanchi(Mai_anfani_da_kwamfuta_allo *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t 보드사용자실행(uintptr_t);
uintptr_t 보드사용자검사(void);
uintptr_t 보드사용자제어(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
