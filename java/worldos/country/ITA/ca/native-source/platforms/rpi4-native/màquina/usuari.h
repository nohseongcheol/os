#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define usuari_BASE 0x02000000ul
#define usuari_IMATGE_finalitzar 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define usuari_Pila_ADREÇA 0x02f00000ul
#define usuari_finalitzar 0x03000000ul
#define usuari_pàgina_COMPT ((usuari_finalitzar - usuari_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define usuari_dades_error (-1001)
#define 사용자실행오류 (-1002)
#define usuari_invàlid_instrucció (-1003)
#define usuari_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registrar_se_dades[31], ordre_càrrec, Estat_CODI, Pila_ADREÇA; } usuari_marc;
void 사용자체계준비(void);
int usuari_excepció(usuari_marc *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tauler_usuari_execució(uintptr_t);
uintptr_t Tauler_usuari_validar(void);
uintptr_t Tauler_control_d_usuari(uintptr_t);
uint32_t tancar_usuari_Estat(unsigned, unsigned);
#endif
