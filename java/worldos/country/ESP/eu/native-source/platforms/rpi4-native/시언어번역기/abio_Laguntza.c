#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char arg_matrize[8][256];
int erabiltzaile_HASI(int 미사용값){
    (void)미사용값;char *arg_Zerrenda[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)arg_matrize[순번],256,0,0,0)<0)return 126;arg_Zerrenda[순번]=arg_matrize[순번];}arg_Zerrenda[인수개수]=0;
    return main(인수개수,arg_Zerrenda);
}
void *memset(void*datuak_kargu,int karaktere_kode,size_t elementu_ZENBATU){unsigned char*helburu_datuak=datuak_kargu;while(elementu_ZENBATU--)*helburu_datuak++=karaktere_kode;return datuak_kargu;}
void *memcpy(void*helburu_datuak,const void*kate_datuak,size_t elementu_ZENBATU){unsigned char*첫째값=helburu_datuak;const unsigned char*SEGUNDOA_balio=kate_datuak;while(elementu_ZENBATU--)*첫째값++=*SEGUNDOA_balio++;return helburu_datuak;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned X_koordenatu,unsigned Y_koordenatu,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(X_koordenatu,Y_koordenatu,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned Bertikala_kargu,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Bertikala_kargu,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
