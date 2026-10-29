#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argumentum_TÖMB[8][256];
int felhasználó_START(int 미사용값){
    (void)미사용값;char *argumentum_Lista[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argumentum_TÖMB[순번],256,0,0,0)<0)return 126;argumentum_Lista[순번]=argumentum_TÖMB[순번];}argumentum_Lista[인수개수]=0;
    return main(인수개수,argumentum_Lista);
}
void *memset(void*adat_pozíció,int kódpont,size_t cikk_DARAB){unsigned char*cél_adat=adat_pozíció;while(cikk_DARAB--)*cél_adat++=kódpont;return adat_pozíció;}
void *memcpy(void*cél_adat,const void*sztring_adat,size_t cikk_DARAB){unsigned char*첫째값=cél_adat;const unsigned char*MPERC_ÉRTÉK=sztring_adat;while(cikk_DARAB--)*첫째값++=*MPERC_ÉRTÉK++;return cél_adat;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koordináta,unsigned Y_koordináta,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koordináta,Y_koordináta,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Rajz_téglalap(unsigned 가로,unsigned szektor_pozíció,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,szektor_pozíció,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
