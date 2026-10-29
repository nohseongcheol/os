#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argumentas_ARRAY[8][256];
int naudotojas_Start(int 미사용값){
    (void)미사용값;char *argumentas_Sąrašas[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argumentas_ARRAY[순번],256,0,0,0)<0)return 126;argumentas_Sąrašas[순번]=argumentas_ARRAY[순번];}argumentas_Sąrašas[인수개수]=0;
    return main(인수개수,argumentas_Sąrašas);
}
void *memset(void*duomenys_padėtis,int simbolio_kodas,size_t prekė_COUNT){unsigned char*vieta_duomenys=duomenys_padėtis;while(prekė_COUNT--)*vieta_duomenys++=simbolio_kodas;return duomenys_padėtis;}
void *memcpy(void*vieta_duomenys,const void*eilutė_duomenys,size_t prekė_COUNT){unsigned char*첫째값=vieta_duomenys;const unsigned char*SECOND_VALUE=eilutė_duomenys;while(prekė_COUNT--)*첫째값++=*SECOND_VALUE++;return vieta_duomenys;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koordinatė,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koordinatė,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int piešti_stačiakampis(unsigned 가로,unsigned segmentas_padėtis,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,segmentas_padėtis,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
