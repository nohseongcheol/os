#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_pole[8][256];
int uživatel_START(int 미사용값){
    (void)미사용값;char *argument_Seznam[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_pole[순번],256,0,0,0)<0)return 126;argument_Seznam[순번]=argument_pole[순번];}argument_Seznam[인수개수]=0;
    return main(인수개수,argument_Seznam);
}
void *memset(void*data_pozice,int bod_kódu,size_t zboží_POČET){unsigned char*cíl_data=data_pozice;while(zboží_POČET--)*cíl_data++=bod_kódu;return data_pozice;}
void *memcpy(void*cíl_data,const void*řetězec_data,size_t zboží_POČET){unsigned char*첫째값=cíl_data;const unsigned char*SEKUNDA_HODNOTA=řetězec_data;while(zboží_POČET--)*첫째값++=*SEKUNDA_HODNOTA++;return cíl_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned souřadnice_x,unsigned Y_souřadnice,unsigned 너비,unsigned výška_HODNOTA,unsigned 색상){return 화면사각형(souřadnice_x,Y_souřadnice,너비,výška_HODNOTA,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int kreslit_obdélník(unsigned 가로,unsigned Svislá_pozice,unsigned 너비,unsigned výška_HODNOTA,unsigned 색상){return pk_rectangle(가로,Svislá_pozice,너비,výška_HODNOTA,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
