#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char аргумент_МАССИВ[8][256];
int кулланучы_Start(int 미사용값){
    (void)미사용값;char *аргумент_Исемлек[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)аргумент_МАССИВ[순번],256,0,0,0)<0)return 126;аргумент_Исемлек[순번]=аргумент_МАССИВ[순번];}аргумент_Исемлек[인수개수]=0;
    return main(인수개수,аргумент_Исемлек);
}
void *memset(void*мәгълүмат_урнаштыру,int символ_коды,size_t элемент_COUNT){unsigned char*күчерү_урыны_мәгълүмат=мәгълүмат_урнаштыру;while(элемент_COUNT--)*күчерү_урыны_мәгълүмат++=символ_коды;return мәгълүмат_урнаштыру;}
void *memcpy(void*күчерү_урыны_мәгълүмат,const void*юл_мәгълүмат,size_t элемент_COUNT){unsigned char*첫째값=күчерү_урыны_мәгълүмат;const unsigned char*SECOND_VALUE=юл_мәгълүмат;while(элемент_COUNT--)*첫째값++=*SECOND_VALUE++;return күчерү_урыны_мәгълүмат;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned X_координатасы,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(X_координатасы,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Вертикаль_урнаштыру,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Вертикаль_урнаштыру,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
