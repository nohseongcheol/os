#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char hoja_ARRAY[8][256];
int mtumiaji_Anza(int 미사용값){
    (void)미사용값;char *hoja_Orodha[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)hoja_ARRAY[순번],256,0,0,0)<0)return 126;hoja_Orodha[순번]=hoja_ARRAY[순번];}hoja_Orodha[인수개수]=0;
    return main(인수개수,hoja_Orodha);
}
void *memset(void*자료위치,int msimbo_wa_kibambo,size_t 개수){unsigned char*fikio_data=자료위치;while(개수--)*fikio_data++=msimbo_wa_kibambo;return 자료위치;}
void *memcpy(void*fikio_data,const void*tungo_data,size_t 개수){unsigned char*첫째값=fikio_data;const unsigned char*둘째값=tungo_data;while(개수--)*첫째값++=*둘째값++;return fikio_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned jira_x,unsigned Kitufe_cha_Y_kiratibu,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(jira_x,Kitufe_cha_Y_kiratibu,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned 세로,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,세로,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
