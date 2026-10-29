#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define utent_BASE 0x02000000ul
#define utent_IMAGE_ttermina 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define utent_Munzell_ADDRESS 0x02f00000ul
#define utent_ttermina 0x03000000ul
#define utent_paġna_COUNT ((utent_ttermina - utent_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define utent_data_żball (-1001)
#define 사용자실행오류 (-1002)
#define utent_invalidu_istruzzjoni (-1003)
#define utent_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t i_rreġistra_data[31], kmand_pożizzjoni, stat_CODE, Munzell_ADDRESS; } utent_frejm;
void 사용자체계준비(void);
int 사용자예외(utent_frejm *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t bord_utent_serje(uintptr_t);
uintptr_t bord_utent_vvalida(void);
uintptr_t bord_kontroll_tal_utent(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
