#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_pole[8][256];
int používateľ_START(int 미사용값){
    (void)미사용값;char *argument_Zoznam[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_pole[순번],256,0,0,0)<0)return 126;argument_Zoznam[순번]=argument_pole[순번];}argument_Zoznam[인수개수]=0;
    return main(인수개수,argument_Zoznam);
}
void *memset(void*údaje_pozícia,int bod_kódu,size_t položka_COUNT){unsigned char*cieľ_údaje=údaje_pozícia;while(položka_COUNT--)*cieľ_údaje++=bod_kódu;return údaje_pozícia;}
void *memcpy(void*cieľ_údaje,const void*reťazec_údaje,size_t položka_COUNT){unsigned char*첫째값=cieľ_údaje;const unsigned char*SECOND_VALUE=reťazec_údaje;while(položka_COUNT--)*첫째값++=*SECOND_VALUE++;return cieľ_údaje;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned X_súradnica,unsigned Y_súradnica,unsigned 너비,unsigned výška_VALUE,unsigned 색상){return 화면사각형(X_súradnica,Y_súradnica,너비,výška_VALUE,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int kresliť_obdĺžnik(unsigned 가로,unsigned vertikála_pozícia,unsigned 너비,unsigned výška_VALUE,unsigned 색상){return pk_rectangle(가로,vertikála_pozícia,너비,výška_VALUE,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
