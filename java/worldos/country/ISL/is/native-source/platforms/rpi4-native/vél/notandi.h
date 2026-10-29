#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define notandi_BASE 0x02000000ul
#define notandi_mynd_ljúka 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define notandi_bunki_slóð 0x02f00000ul
#define notandi_ljúka 0x03000000ul
#define notandi_síða_COUNT ((notandi_ljúka - notandi_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define notandi_gögn_villa (-1001)
#define 사용자실행오류 (-1002)
#define notandi_ógilt_skipun (-1003)
#define notandi_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t skrá_gögn[31], skipun_staða, staða_CODE, bunki_slóð; } notandi_ramma;
void 사용자체계준비(void);
int notandi_undantekning(notandi_ramma *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t bretti_notandi_runa(uintptr_t);
uintptr_t bretti_notandi_staðfesta(void);
uintptr_t bretti_notandastjórn(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
