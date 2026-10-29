#ifndef nativní_uživatel_Nadpis
#define nativní_uživatel_Nadpis
#include <stdint.h>
#include <stddef.h>
#define uživatel_BASE 0x02000000ul
#define uživatel_image_konec 0x02c00000ul
#define uživatel_halda_konec 0x02ed0000ul
#define uživatel_Štos_ODKAZ 0x02f00000ul
#define uživatel_konec 0x03000000ul
#define uživatel_stránka_POČET ((uživatel_konec - uživatel_BASE) / 4096ul)
#define uživatel_spustitelný_chyba (-8)
#define uživatel_data_chyba (-1001)
#define uživatel_spuštění_chyba (-1002)
#define 사용자잘못된명령 (-1003)
#define uživatel_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registr_data[31], příkaz_pozice, Stav_KÓD, Štos_ODKAZ; } uživatel_rámec;
void 사용자체계준비(void);
int výjimka_uživatelského_režimu(uživatel_rámec *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Panel_uživatel_spustit(uintptr_t);
uintptr_t Panel_uživatel_ověřit(void);
uintptr_t Panel_uživatelský_ovládací_prvek(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
