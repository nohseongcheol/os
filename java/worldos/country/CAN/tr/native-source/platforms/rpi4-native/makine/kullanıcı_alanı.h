#ifndef yerel_kullanıcı_Başlık
#define yerel_kullanıcı_Başlık
#include <stdint.h>
#include <stddef.h>
#define kullanıcı_TABAN 0x02000000ul
#define kullanıcı_RESİM_Bitiş 0x02c00000ul
#define kullanıcı_yığın_Bitiş 0x02ed0000ul
#define kullanıcı_Yığın_ADRES 0x02f00000ul
#define kullanıcı_Bitiş 0x03000000ul
#define kullanıcı_sayfa_BAĞ_DEĞ_SAY ((kullanıcı_Bitiş - kullanıcı_TABAN) / 4096ul)
#define kullanıcı_yürütülebilir_hata (-8)
#define kullanıcı_veri_hata (-1001)
#define kullanıcı_yürütme_hata (-1002)
#define 사용자잘못된명령 (-1003)
#define kullanıcı_ZAMANAŞIMI (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t yazmaç_veri[31], komut_konum, Durum_KOD, Yığın_ADRES; } kullanıcı_kare;
void 사용자체계준비(void);
int kullanıcı_özel_durumu(kullanıcı_kare *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Pano_kullanıcı_çalıştırma(uintptr_t);
uintptr_t Pano_kullanıcı_doğrulamak(void);
uintptr_t Pano_kullanıcı_kontrolü(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
