#include "../명명/기계연결이름.h"
#include "tela_informações.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Quadro_pixel(uintptr_t,uintptr_t,uintptr_t),Quadro_Terminal(uintptr_t);
extern void Terminal_glifo(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int área_VALOR,pai,coordenada_X,Y_coordenada,너비값,solicitado_altura_VALOR,보이는지,manual_Layout,Layout_Policy;unsigned texto[128],duração_VALOR; } Widget_Estado;
static Widget_Estado 요소들[4][32];
static int Destaques[4],Evento_Lista[4][16];static unsigned 첫항목[4],entrada_CONT_NÚM_8f7753a1[4],부호없는결과[4],긴부호없는값[4];
static void Evento(int proprietário_objeto,int VALOR){if(entrada_CONT_NÚM_8f7753a1[proprietário_objeto]<16){Evento_Lista[proprietário_objeto][(첫항목[proprietário_objeto]+entrada_CONT_NÚM_8f7753a1[proprietário_objeto])%16]=VALOR;entrada_CONT_NÚM_8f7753a1[proprietário_objeto]++;}}
static Widget_Estado *elemento_VALOR(int proprietário_objeto,int identificador_VALOR){return proprietário_objeto>=0&&proprietário_objeto<4&&identificador_VALOR>0&&identificador_VALOR<=32&&요소들[proprietário_objeto][identificador_VALOR-1].área_VALOR?&요소들[proprietário_objeto][identificador_VALOR-1]:0;}
static void 사각영역(int coordenada_X,int Y_coordenada,int 너비값,int solicitado_altura_VALOR,unsigned 색상){Quadro_retângulo_preencher(coordenada_X,Y_coordenada,너비값,solicitado_altura_VALOR,색상);}
int 화면보임(int proprietário_objeto){if(proprietário_objeto<0||proprietário_objeto>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[proprietário_objeto][순번].área_VALOR==1&&요소들[proprietário_objeto][순번].보이는지)return 1;return 0;}
void inicializar_tela(int proprietário_objeto){memset(요소들[proprietário_objeto],0,sizeof(요소들[proprietário_objeto]));entrada_CONT_NÚM_8f7753a1[proprietário_objeto]=첫항목[proprietário_objeto]=Destaques[proprietário_objeto]=긴부호없는값[proprietário_objeto]=0;}
static void posição(int proprietário_objeto,Widget_Estado *너비값,int *coordenada_X,int *Y_coordenada){*coordenada_X=너비값->coordenada_X;*Y_coordenada=너비값->Y_coordenada;int dados_cargo=너비값->pai;for(int item_CONT_NÚM=0;dados_cargo&&item_CONT_NÚM<32;item_CONT_NÚM++){Widget_Estado *위쪽=elemento_VALOR(proprietário_objeto,dados_cargo);if(!위쪽)break;*coordenada_X+=위쪽->coordenada_X;*Y_coordenada+=위쪽->Y_coordenada+(위쪽->área_VALOR==1?30:0);dados_cargo=위쪽->pai;}}
static int 표시됨(int proprietário_objeto,Widget_Estado *너비값){for(int item_CONT_NÚM=0;item_CONT_NÚM<32;item_CONT_NÚM++){if(!너비값->보이는지)return 0;if(너비값->área_VALOR==1)return 1;너비값=elemento_VALOR(proprietário_objeto,너비값->pai);if(!너비값)return 0;}return 0;}
static void texto(int coordenada_X,int Y_coordenada,Widget_Estado *너비값,int 최대값,unsigned 색상,unsigned 배경색){int em_dia_cargo=0;for(unsigned 순번=0;순번<너비값->duração_VALOR;순번++){unsigned codificação_de_caracteres=너비값->texto[순번],너비=codificação_de_caracteres>=256?16:8;if(em_dia_cargo+(int)너비>최대값)break;Terminal_glifo(coordenada_X+em_dia_cargo,Y_coordenada,codificação_de_caracteres,색상,배경색);em_dia_cargo+=너비;}}
void 화면다시그림(int proprietário_objeto){
    if(!화면보임(proprietário_objeto))return;
    for(int processamento_ordem=1;processamento_ordem<=5;processamento_ordem++)for(int 순번=0;순번<32;순번++){
        Widget_Estado *너비값=&요소들[proprietário_objeto][순번];if(너비값->área_VALOR!=processamento_ordem||!표시됨(proprietário_objeto,너비값))continue;int coordenada_X,Y_coordenada;posição(proprietário_objeto,너비값,&coordenada_X,&Y_coordenada);
        if(processamento_ordem==1){사각영역(coordenada_X,Y_coordenada,너비값->너비값,너비값->solicitado_altura_VALOR,0xeee9e0);사각영역(coordenada_X,Y_coordenada,너비값->너비값,30,0x905020);texto(coordenada_X+10,Y_coordenada+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(coordenada_X+너비값->너비값-28,Y_coordenada+4,24,22,0x5555b8);Terminal_glifo(coordenada_X+너비값->너비값-20,Y_coordenada+7,'X',0xffffff,0x5555b8);}
        if(processamento_ordem==2)사각영역(coordenada_X,Y_coordenada,너비값->너비값,너비값->solicitado_altura_VALOR,0xeee9e0);
        if(processamento_ordem>=3){unsigned 배경색=processamento_ordem==4?0xc0ab86:processamento_ordem==5?0xffffff:0xeee9e0;if(processamento_ordem!=3)사각영역(coordenada_X,Y_coordenada,너비값->너비값,너비값->solicitado_altura_VALOR,배경색);texto(coordenada_X+4,Y_coordenada+4,너비값,너비값->너비값-8,0x201a15,배경색);if(processamento_ordem==5&&Destaques[proprietário_objeto]==순번+1)사각영역(coordenada_X,Y_coordenada+너비값->solicitado_altura_VALOR-2,너비값->너비값,2,0x905020);}
    }
}
int tela_sobreposição(int proprietário_objeto,int coordenada_X,int Y_coordenada){
    if(!화면보임(proprietário_objeto))return 0;
    for(int 순번=0;순번<32;순번++){
        Widget_Estado *Janela=&요소들[proprietário_objeto][순번];
        if(Janela->área_VALOR==1&&Janela->보이는지&&coordenada_X>=Janela->coordenada_X&&Y_coordenada>=Janela->Y_coordenada&&
           coordenada_X<Janela->coordenada_X+Janela->너비값&&Y_coordenada<Janela->Y_coordenada+Janela->solicitado_altura_VALOR)return 1;
    }return 0;
}
int tela_ponteiro(int proprietário_objeto,unsigned 눌림,int coordenada_X,int Y_coordenada){
    if(!화면보임(proprietário_objeto))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){Widget_Estado *너비값=&요소들[proprietário_objeto][순번];if(!너비값->área_VALOR||!표시됨(proprietário_objeto,너비값))continue;int janela_X,janela_Y;posição(proprietário_objeto,너비값,&janela_X,&janela_Y);
        if(coordenada_X<janela_X||Y_coordenada<janela_Y||coordenada_X>=janela_X+너비값->너비값||Y_coordenada>=janela_Y+너비값->solicitado_altura_VALOR)continue;
        if(너비값->área_VALOR==1&&Y_coordenada<janela_Y+30&&coordenada_X>=janela_X+너비값->너비값-28){if(너비값->Layout_Policy!=0)너비값->보이는지=0;Evento(proprietário_objeto,0x10000+순번+1);Quadro_Terminal(3);return 1;}
        if(너비값->área_VALOR==4){Evento(proprietário_objeto,순번+1);return 1;}if(너비값->área_VALOR==5){Destaques[proprietário_objeto]=순번+1;Quadro_Terminal(3);return 1;}
        if(너비값->área_VALOR==1)return 1;
    }return 0;
}
void 화면누름(int proprietário_objeto,unsigned SEGUNDO_VALOR){
    Widget_Estado *너비값=elemento_VALOR(proprietário_objeto,Destaques[proprietário_objeto]);if(!너비값||너비값->área_VALOR!=5)return;
    if(SEGUNDO_VALOR==13||SEGUNDO_VALOR==10){Evento(proprietário_objeto,Destaques[proprietário_objeto]);return;}
    if(SEGUNDO_VALOR==8||SEGUNDO_VALOR==127){if(너비값->duração_VALOR)너비값->duração_VALOR--;긴부호없는값[proprietário_objeto]=0;}
    else{
        unsigned codificação_de_caracteres=SEGUNDO_VALOR;
        if(긴부호없는값[proprietário_objeto]){if((SEGUNDO_VALOR&192)!=128){긴부호없는값[proprietário_objeto]=0;return;}부호없는결과[proprietário_objeto]=(부호없는결과[proprietário_objeto]<<6)|(SEGUNDO_VALOR&63);if(--긴부호없는값[proprietário_objeto])return;codificação_de_caracteres=부호없는결과[proprietário_objeto];}
        else if(SEGUNDO_VALOR>=0xc2&&SEGUNDO_VALOR<=0xf4){긴부호없는값[proprietário_objeto]=SEGUNDO_VALOR<0xe0?1:SEGUNDO_VALOR<0xf0?2:3;부호없는결과[proprietário_objeto]=SEGUNDO_VALOR&((1u<<(6-긴부호없는값[proprietário_objeto]))-1);return;}
        else if(SEGUNDO_VALOR<32||SEGUNDO_VALOR>=128)return;
        if(codificação_de_caracteres>0x10ffff||(codificação_de_caracteres>=0xd800&&codificação_de_caracteres<=0xdfff))return;if(너비값->duração_VALOR<127)너비값->texto[너비값->duração_VALOR++]=codificação_de_caracteres;
    }
    Quadro_Terminal(3);
}
int 화면호출(int proprietário_objeto,unsigned Acção,int identificador_VALOR,int 첫째값,int SEGUNDO_VALOR,int ponto_de_código,int destino_dados){
    if(proprietário_objeto<0||proprietário_objeto>=4)return -22;Widget_Estado *너비값=elemento_VALOR(proprietário_objeto,identificador_VALOR);
    if(Acção==0){if(identificador_VALOR<1||identificador_VALOR>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[proprietário_objeto][순번].área_VALOR==0){너비값=&요소들[proprietário_objeto][순번];memset(너비값,0,sizeof(*너비값));너비값->área_VALOR=identificador_VALOR;너비값->보이는지=identificador_VALOR!=1;너비값->너비값=identificador_VALOR==1?380:220;너비값->solicitado_altura_VALOR=identificador_VALOR==1?240:28;너비값->Layout_Policy=1;너비값->coordenada_X=identificador_VALOR==1?130:16;너비값->Y_coordenada=identificador_VALOR==1?110:16;return 순번+1;}return -28;}
    if(Acção==5){if(!entrada_CONT_NÚM_8f7753a1[proprietário_objeto])return 0;int 반환값=Evento_Lista[proprietário_objeto][첫항목[proprietário_objeto]];첫항목[proprietário_objeto]=(첫항목[proprietário_objeto]+1)%16;entrada_CONT_NÚM_8f7753a1[proprietário_objeto]--;return 반환값;}
    if(Acção==6)return 화면보임(proprietário_objeto);
    if(!너비값)return -9;
    int 이전표시=표시됨(proprietário_objeto,너비값);
    if(Acção==1){int 바탕너비=보드화면너비(),Tela_de_fundo_altura=Quadro_tela_altura();if(첫째값<0||SEGUNDO_VALOR<0||ponto_de_código<1||destino_dados<1||첫째값>바탕너비||SEGUNDO_VALOR>Tela_de_fundo_altura||ponto_de_código>바탕너비-첫째값||destino_dados>Tela_de_fundo_altura-SEGUNDO_VALOR)return -22;너비값->coordenada_X=첫째값;너비값->Y_coordenada=SEGUNDO_VALOR;너비값->너비값=ponto_de_código;너비값->solicitado_altura_VALOR=destino_dados;너비값->manual_Layout=1;}
    else if(Acção==2){Widget_Estado *filho=elemento_VALOR(proprietário_objeto,첫째값);if(!filho||filho==너비값||filho->área_VALOR==1)return -22;int dados_cargo=identificador_VALOR;for(int 깊이=0;dados_cargo&&깊이<32;깊이++){if(dados_cargo==첫째값)return -22;Widget_Estado *위쪽=elemento_VALOR(proprietário_objeto,dados_cargo);dados_cargo=위쪽?위쪽->pai:0;}filho->pai=identificador_VALOR;if(!filho->manual_Layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[proprietário_objeto][순번]!=filho&&요소들[proprietário_objeto][순번].pai==identificador_VALOR)형제요소++;filho->Y_coordenada=16+형제요소*36;}}
    else if(Acção==3)너비값->보이는지=첫째값!=0;
    else if(Acção==4)너비값->보이는지=0;
    else if(Acção==7)너비값->Layout_Policy=첫째값;
    else if(Acção==8)return 너비값->duração_VALOR;
    else if(Acção==9)return 첫째값>=0&&(unsigned)첫째값<너비값->duração_VALOR?너비값->texto[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(proprietário_objeto,너비값))Quadro_Terminal(3);return 0;
}
int tela_SMS(int proprietário_objeto,int identificador_VALOR,const uint32_t *dados,unsigned item_CONT_NÚM){Widget_Estado *너비값=elemento_VALOR(proprietário_objeto,identificador_VALOR);if(!너비값)return -9;if(item_CONT_NÚM>127)return -22;for(unsigned 순번=0;순번<item_CONT_NÚM;순번++){unsigned codificação_de_caracteres=dados[순번];if(codificação_de_caracteres>0x10ffff||(codificação_de_caracteres>=0xd800&&codificação_de_caracteres<=0xdfff))return -22;}for(unsigned 순번=0;순번<item_CONT_NÚM;순번++)너비값->texto[순번]=dados[순번];너비값->duração_VALOR=item_CONT_NÚM;if(표시됨(proprietário_objeto,너비값))Quadro_Terminal(3);return 0;}
