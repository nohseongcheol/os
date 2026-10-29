#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char isiniki_myalelo_ULUHLU[8][256];
int umsebenzisi_qala(int 미사용값){
    (void)미사용값;char *isiniki_myalelo_uludwe[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)isiniki_myalelo_ULUHLU[순번],256,0,0,0)<0)return 126;isiniki_myalelo_uludwe[순번]=isiniki_myalelo_ULUHLU[순번];}isiniki_myalelo_uludwe[인수개수]=0;
    return main(인수개수,isiniki_myalelo_uludwe);
}
void *memset(void*자료위치,int ikhowudi_yekharakhtha,size_t 개수){unsigned char*indawo_ekuyiwa_kuyo_iingcombolo=자료위치;while(개수--)*indawo_ekuyiwa_kuyo_iingcombolo++=ikhowudi_yekharakhtha;return 자료위치;}
void *memcpy(void*indawo_ekuyiwa_kuyo_iingcombolo,const void*uluhlu_lweekharektha_iingcombolo,size_t 개수){unsigned char*첫째값=indawo_ekuyiwa_kuyo_iingcombolo;const unsigned char*둘째값=uluhlu_lweekharektha_iingcombolo;while(개수--)*첫째값++=*둘째값++;return indawo_ekuyiwa_kuyo_iingcombolo;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned isilungelelanisi_x,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(isilungelelanisi_x,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned 세로,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,세로,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
