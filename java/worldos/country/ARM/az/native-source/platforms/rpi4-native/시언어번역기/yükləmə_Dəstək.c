#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char arqument_ARRAY[8][256];
int istifadəçi_Başla(int 미사용값){
    (void)미사용값;char *arqument_Siyahı[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)arqument_ARRAY[순번],256,0,0,0)<0)return 126;arqument_Siyahı[순번]=arqument_ARRAY[순번];}arqument_Siyahı[인수개수]=0;
    return main(인수개수,arqument_Siyahı);
}
void *memset(void*verilənlər_yerinə_qoymaq,int simvol_kodu,size_t element_COUNT){unsigned char*təyinat_verilənlər=verilənlər_yerinə_qoymaq;while(element_COUNT--)*təyinat_verilənlər++=simvol_kodu;return verilənlər_yerinə_qoymaq;}
void *memcpy(void*təyinat_verilənlər,const void*sətir_verilənlər,size_t element_COUNT){unsigned char*첫째값=təyinat_verilənlər;const unsigned char*SECOND_VALUE=sətir_verilənlər;while(element_COUNT--)*첫째값++=*SECOND_VALUE++;return təyinat_verilənlər;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koordinatı,unsigned Y_koordinat,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koordinatı,Y_koordinat,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Şaquli_yerinə_qoymaq,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Şaquli_yerinə_qoymaq,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
