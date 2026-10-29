#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argomento_array[8][256];
int USER_START(int 미사용값){
    (void)미사용값;char *argomento_elenco[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argomento_array[순번],256,0,0,0)<0)return 126;argomento_elenco[순번]=argomento_array[순번];}argomento_elenco[인수개수]=0;
    return main(인수개수,argomento_elenco);
}
void *memset(void*dati_funzione,int punto_di_codice,size_t articolo_CONTA_NUMERI){unsigned char*meta_dati=dati_funzione;while(articolo_CONTA_NUMERI--)*meta_dati++=punto_di_codice;return dati_funzione;}
void *memcpy(void*meta_dati,const void*stringa_dati,size_t articolo_CONTA_NUMERI){unsigned char*첫째값=meta_dati;const unsigned char*SECONDO_VALORE=stringa_dati;while(articolo_CONTA_NUMERI--)*첫째값++=*SECONDO_VALORE++;return meta_dati;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned coordinata_x,unsigned Y_coordinata,unsigned 너비,unsigned altezza_VALORE,unsigned 색상){return schermata_rettangolo(coordinata_x,Y_coordinata,너비,altezza_VALORE,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Disegno_rettangolo(unsigned 가로,unsigned Verticale_funzione,unsigned 너비,unsigned altezza_VALORE,unsigned 색상){return pk_rectangle(가로,Verticale_funzione,너비,altezza_VALORE,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int schermata_altezza(void){return 화면높이읽기();}
