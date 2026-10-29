#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char аргумент_масив[8][256];
int потребител_Старт(int 미사용값){
    (void)미사용값;char *аргумент_Списък[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)аргумент_масив[순번],256,0,0,0)<0)return 126;аргумент_Списък[순번]=аргумент_масив[순번];}аргумент_Списък[인수개수]=0;
    return main(인수개수,аргумент_Списък);
}
void *memset(void*данни_позиция,int знаков_код,size_t 개수){unsigned char*местоназначение_данни=данни_позиция;while(개수--)*местоназначение_данни++=знаков_код;return данни_позиция;}
void *memcpy(void*местоназначение_данни,const void*низ_данни,size_t 개수){unsigned char*첫째값=местоназначение_данни;const unsigned char*둘째값=низ_данни;while(개수--)*첫째값++=*둘째값++;return местоназначение_данни;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_координата,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_координата,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int рисувам_правоъгълник(unsigned 가로,unsigned вертикал_позиция,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,вертикал_позиция,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
