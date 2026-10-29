#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char tohenga_HUĀNGA[8][256];
int kaiwhakamahi_Start(int 미사용값){
    (void)미사용값;char *tohenga_Rārangi[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)tohenga_HUĀNGA[순번],256,0,0,0)<0)return 126;tohenga_Rārangi[순번]=tohenga_HUĀNGA[순번];}tohenga_Rārangi[인수개수]=0;
    return main(인수개수,tohenga_Rārangi);
}
void *memset(void*raraunga_tūranga,int waehere_pūāhua,size_t tuemi_COUNT){unsigned char*ūnga_raraunga=raraunga_tūranga;while(tuemi_COUNT--)*ūnga_raraunga++=waehere_pūāhua;return raraunga_tūranga;}
void *memcpy(void*ūnga_raraunga,const void*aho_raraunga,size_t tuemi_COUNT){unsigned char*첫째값=ūnga_raraunga;const unsigned char*SECOND_uara=aho_raraunga;while(tuemi_COUNT--)*첫째값++=*SECOND_uara++;return ūnga_raraunga;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned taunga_x,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(taunga_x,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Poutū_tūranga,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Poutū_tūranga,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
