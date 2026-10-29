#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argumento_ARRAY[8][256];
int gumagamit_Start(int 미사용값){
    (void)미사용값;char *argumento_list[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argumento_ARRAY[순번],256,0,0,0)<0)return 126;argumento_list[순번]=argumento_ARRAY[순번];}argumento_list[인수개수]=0;
    return main(인수개수,argumento_list);
}
void *memset(void*data_posisyon,int character_code,size_t item_COUNT){unsigned char*patutunguhan_data=data_posisyon;while(item_COUNT--)*patutunguhan_data++=character_code;return data_posisyon;}
void *memcpy(void*patutunguhan_data,const void*string_data,size_t item_COUNT){unsigned char*첫째값=patutunguhan_data;const unsigned char*SECOND_VALUE=string_data;while(item_COUNT--)*첫째값++=*SECOND_VALUE++;return patutunguhan_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_coordinate,unsigned Y_button_coordinate,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(x_coordinate,Y_button_coordinate,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned archive_posisyon,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,archive_posisyon,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
