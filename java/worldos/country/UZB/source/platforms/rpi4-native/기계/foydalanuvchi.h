#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define foydalanuvchi_BASE 0x02000000ul
#define foydalanuvchi_rasm_to_xtatmoq 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define foydalanuvchi_Stack_manzil 0x02f00000ul
#define foydalanuvchi_to_xtatmoq 0x03000000ul
#define foydalanuvchi_sahifa_COUNT ((foydalanuvchi_to_xtatmoq - foydalanuvchi_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define foydalanuvchi_ma_lumotlar_xato (-1001)
#define 사용자실행오류 (-1002)
#define foydalanuvchi_xato_qo_llanma (-1003)
#define foydalanuvchi_TANAFFUS (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t 저장기값[31], buyruq_holat, holat_kod, Stack_manzil; } foydalanuvchi_kadr;
void 사용자체계준비(void);
int foydalanuvchi_istisno(foydalanuvchi_kadr *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t yozuv_taxtasi_foydalanuvchi_ishlash(uintptr_t);
uintptr_t yozuv_taxtasi_foydalanuvchi_tasdiqlash(void);
uintptr_t yozuv_taxtasi_foydalanuvchi_nazorati(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
