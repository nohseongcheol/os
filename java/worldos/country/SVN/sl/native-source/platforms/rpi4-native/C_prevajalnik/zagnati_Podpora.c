#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_ARRAY[8][256];
int uporabnik_Start(int 미사용값){
    (void)미사용값;char *argument_Seznam[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_ARRAY[순번],256,0,0,0)<0)return 126;argument_Seznam[순번]=argument_ARRAY[순번];}argument_Seznam[인수개수]=0;
    return main(인수개수,argument_Seznam);
}
void *memset(void*podatki_položaj,int koda_znaka,size_t element_COUNT){unsigned char*cilj_podatki=podatki_položaj;while(element_COUNT--)*cilj_podatki++=koda_znaka;return podatki_položaj;}
void *memcpy(void*cilj_podatki,const void*niz_podatki,size_t element_COUNT){unsigned char*첫째값=cilj_podatki;const unsigned char*SECOND_VALUE=niz_podatki;while(element_COUNT--)*첫째값++=*SECOND_VALUE++;return cilj_podatki;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned koordinata_x,unsigned 세로좌표,unsigned 너비,unsigned višina_VALUE,unsigned 색상){return 화면사각형(koordinata_x,세로좌표,너비,višina_VALUE,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int risati_pravokotnik(unsigned 가로,unsigned Navpično_položaj,unsigned 너비,unsigned višina_VALUE,unsigned 색상){return pk_rectangle(가로,Navpično_položaj,너비,višina_VALUE,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
