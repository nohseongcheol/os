#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ئارگیومێنت_ڕیزی_داتا[8][256];
int بەکارهێنەر_دەستپێك(int 미사용값){
    (void)미사용값;char *ئارگیومێنت_لیست[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ئارگیومێنت_ڕیزی_داتا[순번],256,0,0,0)<0)return 126;ئارگیومێنت_لیست[순번]=ئارگیومێنت_ڕیزی_داتا[순번];}ئارگیومێنت_لیست[인수개수]=0;
    return main(인수개수,ئارگیومێنت_لیست);
}
void *memset(void*자료위치,int کۆدی_نووسە,size_t 개수){unsigned char*جێمەبەست_دەیتا=자료위치;while(개수--)*جێمەبەست_دەیتا++=کۆدی_نووسە;return 자료위치;}
void *memcpy(void*جێمەبەست_دەیتا,const void*رست_دەیتا,size_t 개수){unsigned char*첫째값=جێمەبەست_دەیتا;const unsigned char*둘째값=رست_دەیتا;while(개수--)*첫째값++=*둘째값++;return جێمەبەست_دەیتا;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned پۆوتانی_x,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(پۆوتانی_x,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned 세로,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,세로,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
