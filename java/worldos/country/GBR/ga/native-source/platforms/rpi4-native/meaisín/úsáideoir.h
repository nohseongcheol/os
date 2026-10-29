#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define úsáideoir_BASE 0x02000000ul
#define úsáideoir_IMAGE_cuir_deireadh_le 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define úsáideoir_Cruach_ADDRESS 0x02f00000ul
#define úsáideoir_cuir_deireadh_le 0x03000000ul
#define úsáideoir_leathanach_COUNT ((úsáideoir_cuir_deireadh_le - úsáideoir_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define úsáideoir_sonraí_earráid (-1001)
#define 사용자실행오류 (-1002)
#define úsáideoir_neamhbhailí_treoir (-1003)
#define úsáideoir_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t cláraigh_sonraí[31], ordú_suíomh, staid_CODE, Cruach_ADDRESS; } úsáideoir_fráma;
void 사용자체계준비(void);
int úsáideoir_eisceacht(úsáideoir_fráma *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t clár_úsáideoir_rith(uintptr_t);
uintptr_t clár_úsáideoir_bailíochtaigh(void);
uintptr_t clár_rialtán_úsáideora(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
