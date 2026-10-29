#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_MATRIX[8][256];
int gebruiker_START(int 미사용값){
    (void)미사용값;char *argument_Lijst[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_MATRIX[순번],256,0,0,0)<0)return 126;argument_Lijst[순번]=argument_MATRIX[순번];}argument_Lijst[인수개수]=0;
    return main(인수개수,argument_Lijst);
}
void *memset(void*gegevens_functie,int codepoint,size_t item_AANTAL){unsigned char*doel_gegevens=gegevens_functie;while(item_AANTAL--)*doel_gegevens++=codepoint;return gegevens_functie;}
void *memcpy(void*doel_gegevens,const void*tekenreeks_gegevens,size_t item_AANTAL){unsigned char*첫째값=doel_gegevens;const unsigned char*SECONDE_WAARDE=tekenreeks_gegevens;while(item_AANTAL--)*첫째값++=*SECONDE_WAARDE++;return doel_gegevens;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned x_coördinaat,unsigned Y_coördinaat,unsigned 너비,unsigned hoogte_WAARDE,unsigned 색상){return scherm_rechthoek(x_coördinaat,Y_coördinaat,너비,hoogte_WAARDE,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Tekenen_rechthoek(unsigned 가로,unsigned Verticaal_functie,unsigned 너비,unsigned hoogte_WAARDE,unsigned 색상){return pk_rectangle(가로,Verticaal_functie,너비,hoogte_WAARDE,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int scherm_hoogte(void){return 화면높이읽기();}
