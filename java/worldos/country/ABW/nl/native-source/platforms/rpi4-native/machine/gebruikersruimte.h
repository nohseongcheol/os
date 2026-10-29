#ifndef systeemeigen_gebruiker_header
#define systeemeigen_gebruiker_header
#include <stdint.h>
#include <stddef.h>
#define gebruiker_BASIS 0x02000000ul
#define gebruiker_kopie_beëindigen 0x02c00000ul
#define gebruiker_heap_beëindigen 0x02ed0000ul
#define gebruiker_stack_ADRES 0x02f00000ul
#define gebruiker_beëindigen 0x03000000ul
#define gebruiker_page_AANTAL ((gebruiker_beëindigen - gebruiker_BASIS) / 4096ul)
#define gebruiker_uitvoerbaar_fout (-8)
#define gebruiker_gegevens_fout (-1001)
#define gebruiker_uitvoerbewerking_fout (-1002)
#define gebruiker_nietig_instructie (-1003)
#define gebruiker_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_gegevens[31], opdracht_functie, Status_CODE, stack_ADRES; } gebruiker_frame;
void 사용자체계준비(void);
int gebruikersuitzondering(gebruiker_frame *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Bord_gebruiker_uitvoeren(uintptr_t);
uintptr_t Bord_gebruiker_valideren(void);
uintptr_t Bord_gebruikersbesturingselement(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
