#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argumen_ARRAY[8][256];
int pengguna_Mulai(int 미사용값){
    (void)미사용값;char *argumen_Daftar[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argumen_ARRAY[순번],256,0,0,0)<0)return 126;argumen_Daftar[순번]=argumen_ARRAY[순번];}argumen_Daftar[인수개수]=0;
    return main(인수개수,argumen_Daftar);
}
void *memset(void*data_posisi,int kode_karakter,size_t item_COUNT){unsigned char*tujuan_data=data_posisi;while(item_COUNT--)*tujuan_data++=kode_karakter;return data_posisi;}
void *memcpy(void*tujuan_data,const void*string_data,size_t item_COUNT){unsigned char*첫째값=tujuan_data;const unsigned char*SECOND_VALUE=string_data;while(item_COUNT--)*첫째값++=*SECOND_VALUE++;return tujuan_data;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned koordinat_x,unsigned Y_koordinat,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(koordinat_x,Y_koordinat,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Gambar_persegi(unsigned 가로,unsigned Vertikal_posisi,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Vertikal_posisi,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
