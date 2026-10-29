#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char 인수배열[8][256];
int 사용자진입연결(int 미사용값){
    (void)미사용값;char *인수목록[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)인수배열[순번],256,0,0,0)<0)return 126;인수목록[순번]=인수배열[순번];}인수목록[인수개수]=0;
    return main(인수개수,인수목록);
}
void *memset(void*자료위치,int 문자값,size_t 개수){unsigned char*목적자료=자료위치;while(개수--)*목적자료++=문자값;return 자료위치;}
void *memcpy(void*목적자료,const void*문자열값,size_t 개수){unsigned char*첫째값=목적자료;const unsigned char*둘째값=문자열값;while(개수--)*첫째값++=*둘째값++;return 목적자료;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned 가로좌표,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(가로좌표,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned 세로,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,세로,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
