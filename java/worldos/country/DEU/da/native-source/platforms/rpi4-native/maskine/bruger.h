#ifndef oprindelig_bruger_Header
#define oprindelig_bruger_Header
#include <stdint.h>
#include <stddef.h>
#define bruger_BASIS 0x02000000ul
#define bruger_Image_afslutte_et_opkald 0x02c00000ul
#define bruger_heap_afslutte_et_opkald 0x02ed0000ul
#define bruger_Stak_mail 0x02f00000ul
#define bruger_afslutte_et_opkald 0x03000000ul
#define bruger_side_TÆL ((bruger_afslutte_et_opkald - bruger_BASIS) / 4096ul)
#define bruger_eksekverbar_fil_fejl (-8)
#define bruger_data_fejl (-1001)
#define bruger_udførelse_fejl (-1002)
#define 사용자잘못된명령 (-1003)
#define bruger_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_data[31], kommando_placere, status_KODE, Stak_mail; } bruger_ramme;
void 사용자체계준비(void);
int brugerundtagelse(bruger_ramme *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tavle_bruger_køre(uintptr_t);
uintptr_t Tavle_bruger_bekræfte(void);
uintptr_t Tavle_brugerkontrolelement(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
