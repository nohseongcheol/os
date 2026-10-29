#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_ARRAY[8][256];
int ulanyjy_başlat(int 미사용값){
    (void)미사용값;char *argument_Sanaw[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_ARRAY[순번],256,0,0,0)<0)return 126;argument_Sanaw[순번]=argument_ARRAY[순번];}argument_Sanaw[인수개수]=0;
    return main(인수개수,argument_Sanaw);
}
void *memset(void*자료위치,int nyşanyň_kody,size_t 개수){unsigned char*barylmaly_ýer_maglumat=자료위치;while(개수--)*barylmaly_ýer_maglumat++=nyşanyň_kody;return 자료위치;}
void *memcpy(void*barylmaly_ýer_maglumat,const void*setir_maglumat,size_t 개수){unsigned char*첫째값=barylmaly_ýer_maglumat;const unsigned char*둘째값=setir_maglumat;while(개수--)*첫째값++=*둘째값++;return barylmaly_ýer_maglumat;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koordinatasy,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koordinatasy,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned 세로,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,세로,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
