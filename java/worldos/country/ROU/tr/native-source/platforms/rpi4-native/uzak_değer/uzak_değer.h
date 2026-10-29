#ifndef yerel_uzak_bağlantı_Başlık
#define yerel_uzak_bağlantı_Başlık
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Hazırlan_uzak(void);
void 원격살피기(void);
void uzak_çıktı(unsigned char);
int uzak_artış(void);
int akış_uzak_artış(const unsigned char *,unsigned);
uintptr_t Pano_gölge_kullanım(uintptr_t,uintptr_t);
uintptr_t Pano_Bitiş_uzak_komut(uintptr_t);
uintptr_t Pano_uzak_bekle(uintptr_t);
void 원격화면살피기(void);
int denetim_uzak_monitör(unsigned);
#endif
