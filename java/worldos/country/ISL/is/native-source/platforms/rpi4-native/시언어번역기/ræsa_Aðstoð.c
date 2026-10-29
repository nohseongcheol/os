#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char frumbreyta_ARRAY[8][256];
int notandi_Opna(int 미사용값){
    (void)미사용값;char *frumbreyta_Listi[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)frumbreyta_ARRAY[순번],256,0,0,0)<0)return 126;frumbreyta_Listi[순번]=frumbreyta_ARRAY[순번];}frumbreyta_Listi[인수개수]=0;
    return main(인수개수,frumbreyta_Listi);
}
void *memset(void*gögn_staða,int stafkóði,size_t vara_COUNT){unsigned char*endastaður_gögn=gögn_staða;while(vara_COUNT--)*endastaður_gögn++=stafkóði;return gögn_staða;}
void *memcpy(void*endastaður_gögn,const void*strengur_gögn,size_t vara_COUNT){unsigned char*첫째값=endastaður_gögn;const unsigned char*SECOND_VALUE=strengur_gögn;while(vara_COUNT--)*첫째값++=*SECOND_VALUE++;return endastaður_gögn;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_hnit,unsigned Y_hnit,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_hnit,Y_hnit,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Lóðrétt_staða,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Lóðrétt_staða,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
