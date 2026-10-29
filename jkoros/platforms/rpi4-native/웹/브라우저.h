#ifndef 웹브라우저머리
#define 웹브라우저머리
#include <stdint.h>
#include <stddef.h>
uintptr_t 웹제어(uintptr_t,uintptr_t,uintptr_t);
void 웹살피기(void);
int 웹포인터입력(unsigned,int,int);
void 웹입력살피기(void);
void 웹가리개옮기기(int,int);
int 웹범위(int*,int*,int*,int*);
int 웹사용(int);
int 웹덮음(int,int,int);
int 웹가리킴(int,unsigned,int,int);
void 웹그리기(int);
int 웹글쇠(int,unsigned);
void 웹창닫기(int);
/* 각 커널의 단말·그림·시각 경계. C 내부에서 Go/Java로 재진입하지 않는다. */
int 웹현재창(void);
void 웹화면준비(void);
void 웹화면새로(void);
unsigned 웹화면너비(void);
unsigned 웹화면높이(void);
void 웹사각(int,int,int,int,uint32_t);
void 웹글자(int,int,unsigned,uint32_t,uint32_t);
void 웹출력(unsigned);
uintptr_t 웹밀리초(void);
#endif
