#ifndef asal_pengguna_Pengepala
#define asal_pengguna_Pengepala
#include <stdint.h>
#include <stddef.h>
#define pengguna_BASE 0x02000000ul
#define pengguna_imej_tamat 0x02c00000ul
#define pengguna_timbunan_tamat 0x02ed0000ul
#define pengguna_tindan_e_mel 0x02f00000ul
#define pengguna_tamat 0x03000000ul
#define pengguna_halaman_COUNT ((pengguna_tamat - pengguna_BASE) / 4096ul)
#define pengguna_fail_boleh_laku_ralat (-8)
#define pengguna_data_ralat (-1001)
#define 사용자실행오류 (-1002)
#define pengguna_tak_sah_suruhan (-1003)
#define pengguna_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t daftar_data[31], perintah_jawatan, status_kod, tindan_e_mel; } pengguna_bingkai;
void 사용자체계준비(void);
int pengguna_pengecualian(pengguna_bingkai *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Papan_pengguna_jalankan(uintptr_t);
uintptr_t Papan_pengguna_sahkan(void);
uintptr_t Papan_kawalan_pengguna(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
