#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char dalil_ARRAY[8][256];
int foydalanuvchi_Start(int 미사용값){
    (void)미사용값;char *dalil_Ro_yxat[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)dalil_ARRAY[순번],256,0,0,0)<0)return 126;dalil_Ro_yxat[순번]=dalil_ARRAY[순번];}dalil_Ro_yxat[인수개수]=0;
    return main(인수개수,dalil_Ro_yxat);
}
void *memset(void*ma_lumotlar_holat,int belgi_kodi,size_t element_COUNT){unsigned char*ko_chirish_joyi_ma_lumotlar=ma_lumotlar_holat;while(element_COUNT--)*ko_chirish_joyi_ma_lumotlar++=belgi_kodi;return ma_lumotlar_holat;}
void *memcpy(void*ko_chirish_joyi_ma_lumotlar,const void*satr_ma_lumotlar,size_t element_COUNT){unsigned char*첫째값=ko_chirish_joyi_ma_lumotlar;const unsigned char*SECOND_VALUE=satr_ma_lumotlar;while(element_COUNT--)*첫째값++=*SECOND_VALUE++;return ko_chirish_joyi_ma_lumotlar;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koordinata,unsigned Y_tugmasi_koordinat,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koordinata,Y_tugmasi_koordinat,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Vertikal_holat,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Vertikal_holat,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
