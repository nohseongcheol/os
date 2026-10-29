#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char arg_ARAE[8][256];
int defnyddiwr_START(int 미사용값){
    (void)미사용값;char *arg_Rhestr[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)arg_ARAE[순번],256,0,0,0)<0)return 126;arg_Rhestr[순번]=arg_ARAE[순번];}arg_Rhestr[인수개수]=0;
    return main(인수개수,arg_Rhestr);
}
void *memset(void*data_safle,int cod_nod,size_t eitem_COUNT){unsigned char*cyrchfan_data=data_safle;while(eitem_COUNT--)*cyrchfan_data++=cod_nod;return data_safle;}
void *memcpy(void*cyrchfan_data,const void*testun_data,size_t eitem_COUNT){unsigned char*첫째값=cyrchfan_data;const unsigned char*SECOND_VALUE=testun_data;while(eitem_COUNT--)*첫째값++=*SECOND_VALUE++;return cyrchfan_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned cyfesuryn_x,unsigned Y_cyfesuryn,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(cyfesuryn_x,Y_cyfesuryn,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Ar_i_fyny_safle,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Ar_i_fyny_safle,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
