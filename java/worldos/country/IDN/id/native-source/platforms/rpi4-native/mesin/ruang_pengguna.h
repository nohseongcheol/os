#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define pengguna_BASE 0x02000000ul
#define pengguna_foto_mengakhiri 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define pengguna_tumpuk_surel 0x02f00000ul
#define pengguna_mengakhiri 0x03000000ul
#define pengguna_halaman_COUNT ((pengguna_mengakhiri - pengguna_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define pengguna_data_kesalahan (-1001)
#define 사용자실행오류 (-1002)
#define pengguna_tidak_sahih_instruksi (-1003)
#define pengguna_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t daftar_data[31], perintah_posisi, Status_CODE, tumpuk_surel; } pengguna_bingkai;
void 사용자체계준비(void);
int pengguna_pengecualian(pengguna_bingkai *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Papan_pengguna_eksekusi(uintptr_t);
uintptr_t Papan_pengguna_validasi(void);
uintptr_t Papan_kontrol_pengguna(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
