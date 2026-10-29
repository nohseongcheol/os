#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define карыстальнік_выява_скончыць 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define карыстальнік_Стэк_адрас 0x02f00000ul
#define карыстальнік_скончыць 0x03000000ul
#define 사용자쪽수 ((карыстальнік_скончыць - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define карыстальнік_дадзеныя_памылка (-1001)
#define 사용자실행오류 (-1002)
#define карыстальнік_памылковы_інструкцыя (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t рэгістраваць_дадзеныя[31], 명령위치, стан_код, Стэк_адрас; } карыстальнік_кадр;
void 사용자체계준비(void);
int карыстальнік_выключэнне(карыстальнік_кадр *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t 보드사용자실행(uintptr_t);
uintptr_t 보드사용자검사(void);
uintptr_t 보드사용자제어(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
