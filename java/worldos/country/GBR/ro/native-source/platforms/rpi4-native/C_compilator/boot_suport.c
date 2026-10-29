#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argument_ARRAY[8][256];
int utilizator_buta(int 미사용값){
    (void)미사용값;char *argument_Listă[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argument_ARRAY[순번],256,0,0,0)<0)return 126;argument_Listă[순번]=argument_ARRAY[순번];}argument_Listă[인수개수]=0;
    return main(인수개수,argument_Listă);
}
void *memset(void*date_poziție,int cod_caracter,size_t element_COUNT){unsigned char*destinație_date=date_poziție;while(element_COUNT--)*destinație_date++=cod_caracter;return date_poziție;}
void *memcpy(void*destinație_date,const void*șir_date,size_t element_COUNT){unsigned char*첫째값=destinație_date;const unsigned char*SECOND_VALUE=șir_date;while(element_COUNT--)*첫째값++=*SECOND_VALUE++;return destinație_date;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned coordonata_X,unsigned 세로좌표,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(coordonata_X,세로좌표,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int Desen_dreptunghi(unsigned 가로,unsigned Verticală_poziție,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,Verticală_poziție,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
