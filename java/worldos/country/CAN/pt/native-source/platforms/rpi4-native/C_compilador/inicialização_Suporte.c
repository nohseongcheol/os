#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char argumento_MATRIZ[8][256];
int usuário_START(int 미사용값){
    (void)미사용값;char *argumento_Lista[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)argumento_MATRIZ[순번],256,0,0,0)<0)return 126;argumento_Lista[순번]=argumento_MATRIZ[순번];}argumento_Lista[인수개수]=0;
    return main(인수개수,argumento_Lista);
}
void *memset(void*dados_cargo,int ponto_de_código,size_t item_CONT_NÚM){unsigned char*destino_dados=dados_cargo;while(item_CONT_NÚM--)*destino_dados++=ponto_de_código;return dados_cargo;}
void *memcpy(void*destino_dados,const void*cadeia_dados,size_t item_CONT_NÚM){unsigned char*첫째값=destino_dados;const unsigned char*SEGUNDO_VALOR=cadeia_dados;while(item_CONT_NÚM--)*첫째값++=*SEGUNDO_VALOR++;return destino_dados;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned coordenada_X,unsigned Y_coordenada,unsigned 너비,unsigned altura_VALOR,unsigned 색상){return tela_retângulo(coordenada_X,Y_coordenada,너비,altura_VALOR,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int emitir_retângulo(unsigned 가로,unsigned Vertical_cargo,unsigned 너비,unsigned altura_VALOR,unsigned 색상){return pk_rectangle(가로,Vertical_cargo,너비,altura_VALOR,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int tela_altura(void){return leitura_tela_altura();}
