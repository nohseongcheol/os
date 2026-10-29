#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argumen_ARRAY[8][256];
int pengguna_Mula(int 미사용값){
    (void)미사용값;char *argumen_Senarai[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argumen_ARRAY[순번],256,0,0,0)<0)return 126;argumen_Senarai[순번]=argumen_ARRAY[순번];}argumen_Senarai[인수개수]=0;
    return main(인수개수,argumen_Senarai);
}
void *memset(void*data_jawatan,int titik_kod,size_t item_COUNT){unsigned char*destinasi_data=data_jawatan;while(item_COUNT--)*destinasi_data++=titik_kod;return data_jawatan;}
void *memcpy(void*destinasi_data,const void*rentetan_data,size_t item_COUNT){unsigned char*첫째값=destinasi_data;const unsigned char*SECOND_VALUE=rentetan_data;while(item_COUNT--)*첫째값++=*SECOND_VALUE++;return destinasi_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned koordinat_x,unsigned Y_koordinat,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(koordinat_x,Y_koordinat,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Lukis_segi_empat_tepat(unsigned 가로,unsigned Menegak_jawatan,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Menegak_jawatan,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
