#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define кулланучы_BASE 0x02000000ul
#define кулланучы_IMAGE_тәмамлау 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define кулланучы_Стәк_адрес 0x02f00000ul
#define кулланучы_тәмамлау 0x03000000ul
#define кулланучы_бит_COUNT ((кулланучы_тәмамлау - кулланучы_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define кулланучы_мәгълүмат_хата (-1001)
#define 사용자실행오류 (-1002)
#define кулланучы_дөрес_булмаган_инструкция (-1003)
#define кулланучы_КӨТҮВАКЫТЫЧЫГУ (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t теркәлү_мәгълүмат[31], команда_урнаштыру, халәт_CODE, Стәк_адрес; } кулланучы_кадр;
void 사용자체계준비(void);
int 사용자예외(кулланучы_кадр *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t такта_кулланучы_эшләтү(uintptr_t);
uintptr_t такта_кулланучы_тикшерү(void);
uintptr_t такта_кулланучының_идарә_элементы(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
