#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_ARRAY[8][256];
int gebruiker_BEGIN(int 미사용값){
    (void)미사용값;char *argument_Lys[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_ARRAY[순번],256,0,0,0)<0)return 126;argument_Lys[순번]=argument_ARRAY[순번];}argument_Lys[인수개수]=0;
    return main(인수개수,argument_Lys);
}
void *memset(void*data_plaas,int karakterkode,size_t item_COUNT){unsigned char*bestemming_data=data_plaas;while(item_COUNT--)*bestemming_data++=karakterkode;return data_plaas;}
void *memcpy(void*bestemming_data,const void*string_data,size_t item_COUNT){unsigned char*첫째값=bestemming_data;const unsigned char*SECOND_VALUE=string_data;while(item_COUNT--)*첫째값++=*SECOND_VALUE++;return bestemming_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_koördinaat,unsigned Y_koördinaat,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_koördinaat,Y_koördinaat,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Vertikaal_plaas,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Vertikaal_plaas,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
