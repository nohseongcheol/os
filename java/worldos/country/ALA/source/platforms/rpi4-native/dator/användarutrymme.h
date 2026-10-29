#ifndef ursprunglig_användare_huvud
#define ursprunglig_användare_huvud
#include <stdint.h>
#include <stddef.h>
#define användare_BAS 0x02000000ul
#define användare_BILD_avsluta 0x02c00000ul
#define användare_heap_avsluta 0x02ed0000ul
#define användare_Stack_ADRESS 0x02f00000ul
#define användare_avsluta 0x03000000ul
#define användare_page_ANTAL ((användare_avsluta - användare_BAS) / 4096ul)
#define användare_körbar_fil_fel (-8)
#define användare_data_fel (-1001)
#define användare_körning_fel (-1002)
#define användare_ogiltig_instruktion (-1003)
#define användare_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_data[31], kommando_placera, kod_för_tillstånd, Stack_ADRESS; } användare_ram;
void 사용자체계준비(void);
int undantagsfel_för_användare(användare_ram *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tavla_användare_köra(uintptr_t);
uintptr_t Tavla_användare_validera(void);
uintptr_t Tavla_användarkontroll(uintptr_t);
uint32_t läsa_användare_status(unsigned, unsigned);
#endif
