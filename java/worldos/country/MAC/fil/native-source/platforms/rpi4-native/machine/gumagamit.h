#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define gumagamit_BASE 0x02000000ul
#define gumagamit_IMAGE_tapusin 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define gumagamit_Stack_email 0x02f00000ul
#define gumagamit_tapusin 0x03000000ul
#define gumagamit_page_COUNT ((gumagamit_tapusin - gumagamit_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define gumagamit_data_error (-1001)
#define 사용자실행오류 (-1002)
#define gumagamit_hindi_tama_instruksiyon (-1003)
#define gumagamit_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t magrehistro_data[31], utos_posisyon, katayuan_CODE, Stack_email; } gumagamit_frame;
void 사용자체계준비(void);
int gumagamit_pagbubukod(gumagamit_frame *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t board_gumagamit_run(uintptr_t);
uintptr_t board_gumagamit_patunayan(void);
uintptr_t board_user_control(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
