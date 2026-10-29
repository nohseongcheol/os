#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define корисник_слика_завршити 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define корисник_комплет_адреса 0x02f00000ul
#define корисник_завршити 0x03000000ul
#define 사용자쪽수 ((корисник_завршити - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define корисник_подаци_грешка (-1001)
#define 사용자실행오류 (-1002)
#define корисник_неважеће_програмска_наредба (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t регистровати_подаци[31], команда_позиција, стање_шифра, комплет_адреса; } корисник_кадар;
void 사용자체계준비(void);
int корисник_изузетак(корисник_кадар *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Табла_корисник_низ(uintptr_t);
uintptr_t Табла_корисник_потврдити(void);
uintptr_t Табла_корисничка_контрола(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
