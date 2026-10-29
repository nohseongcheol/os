#include "../명명/기계연결이름.h"
#include "tela_informações.h"
/* nativo 네 Janela 합성과 UTF-8 terminal. 바뀐 영역의 concluído_VALOR 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t computador_Word;
extern computador_Word Quadro_pixel(computador_Word,computador_Word,computador_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_fonte[];
#define 최대열수 237
#define Histórico_linha_CONT_NÚM 160
typedef struct {
    uint32_t 글자칸들[Histórico_linha_CONT_NÚM][최대열수]; uint8_t 모양들[Histórico_linha_CONT_NÚM][최대열수];
    unsigned 너비,altura_VALOR,COLS,LIN_CONT_NÚM,크기바뀜;
    unsigned 살아있음,coordenada_X,Y_coordenada,LIN_cargo,COL_cargo,맨위,rolar,전경색,배경색,탈출상태,parâmetro_VALOR[4],parâmetro_ÍNDICE,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,MENOR_VALOR,alternativo,가리개보임;
} Terminal;
static Terminal Windows_Lista[4];
static int Foco=-1,saída,ordem_VALOR[4],entrada_CONT_NÚM_8f7753a1,arrastar_VALOR=-1,arrastar_X,arrastar_Y;
static unsigned TI_Pendente,단추들,desktop_Exibir,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),tela_ponteiro(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_entrada;
static unsigned caractere_largo(unsigned ponto_de_código){return ponto_de_código>=256?2:1;}
static void 사각영역(unsigned coordenada_X,unsigned Y_coordenada,unsigned 너비값,unsigned solicitado_altura_VALOR,unsigned 색상){
    Quadro_retângulo_preencher(coordenada_X,Y_coordenada,너비값,solicitado_altura_VALOR,색상);
}
void Terminal_glifo(unsigned coordenada_X,unsigned Y_coordenada,unsigned ponto_de_código,unsigned 전경색,unsigned 배경색){
    unsigned 너비=caractere_largo(ponto_de_código)*8;if(ponto_de_código==0xffffffffu)return;
    int 왼쪽=coordenada_X,위쪽=Y_coordenada,폭=너비,duração_VALOR=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&duração_VALOR))return;
    if(ponto_de_código==' '){Quadro_retângulo_preencher(왼쪽,위쪽,폭,duração_VALOR,배경색);return;}
    unsigned PROC_ÍNDICE=ponto_de_código<65536?ponto_de_código:ponto_de_código>=0x1f600&&ponto_de_código<0x1f650?65536+ponto_de_código-0x1f600:0xfffd;
    const unsigned char *fonte_VALOR=Terminal_fonte+PROC_ÍNDICE*32;
    for(int linha_de_entrada=위쪽;linha_de_entrada<위쪽+duração_VALOR;linha_de_entrada++){unsigned BITS_Lista=fonte_VALOR[(linha_de_entrada-Y_coordenada)*2]*256+fonte_VALOR[(linha_de_entrada-Y_coordenada)*2+1];for(int slot_entrada=왼쪽;slot_entrada<왼쪽+폭;slot_entrada++)Quadro_pixel(slot_entrada,linha_de_entrada,(BITS_Lista&(0x8000>>(slot_entrada-coordenada_X)))?전경색:배경색);}
}
static void nome_tabela(unsigned coordenada_X,unsigned Y_coordenada,const char *cadeia_dados,unsigned 전경색,unsigned 배경색){while(*cadeia_dados){unsigned ponto_de_código=(unsigned char)*cadeia_dados++, 남은수=0;if(ponto_de_código>=0xc0){남은수=ponto_de_código<0xe0?1:ponto_de_código<0xf0?2:3;ponto_de_código&=(1u<<(6-남은수))-1;while(남은수--&&*cadeia_dados)ponto_de_código=(ponto_de_código<<6)|((unsigned char)*cadeia_dados++&63);}Terminal_glifo(coordenada_X,Y_coordenada,ponto_de_código,전경색,배경색);coordenada_X+=caractere_largo(ponto_de_código)*8;}}
static unsigned 첫항목(void){return Terminal_entrada->맨위;}
static int 보이는지(void){return Terminal_entrada->살아있음&&Foco>=0&&Terminal_entrada==&Windows_Lista[Foco]&&!화면보임(Foco);}
static void Paint_tela(unsigned LIN_cargo,unsigned COL_cargo){
    if(!보이는지()||LIN_cargo<첫항목()-Terminal_entrada->rolar||LIN_cargo>=첫항목()-Terminal_entrada->rolar+Terminal_entrada->LIN_CONT_NÚM||COL_cargo>=Terminal_entrada->COLS)return;
    unsigned ponto_de_código=Terminal_entrada->글자칸들[LIN_cargo%Histórico_linha_CONT_NÚM][COL_cargo],cadeia_dados=Terminal_entrada->모양들[LIN_cargo%Histórico_linha_CONT_NÚM][COL_cargo];
    if(caractere_largo(ponto_de_código)==2&&COL_cargo+1>=Terminal_entrada->COLS)ponto_de_código=' ';
    Terminal_glifo(Terminal_entrada->coordenada_X+12+COL_cargo*8,Terminal_entrada->Y_coordenada+36+(LIN_cargo-첫항목()+Terminal_entrada->rolar)*16,ponto_de_código?ponto_de_código:' ',색상들[cadeia_dados&15],색상들[cadeia_dados>>4]);
}
static void circunflexo_VALOR(int mostrar_janela){if(!보이는지()||Terminal_entrada->rolar||Terminal_entrada->COL_cargo>=Terminal_entrada->COLS||Terminal_entrada->LIN_cargo<Terminal_entrada->맨위||Terminal_entrada->LIN_cargo>=Terminal_entrada->맨위+Terminal_entrada->LIN_CONT_NÚM)return;
    if(!mostrar_janela||!Terminal_entrada->가리개보임)Paint_tela(Terminal_entrada->LIN_cargo,Terminal_entrada->COL_cargo);else 사각영역(Terminal_entrada->coordenada_X+12+Terminal_entrada->COL_cargo*8,Terminal_entrada->Y_coordenada+36+(Terminal_entrada->LIN_cargo-Terminal_entrada->맨위)*16+14,8,2,색상들[Terminal_entrada->전경색]);}
static void Conteúdo_VALOR(void){
    사각영역(Terminal_entrada->coordenada_X+12,Terminal_entrada->Y_coordenada+36,Terminal_entrada->COLS*8,Terminal_entrada->LIN_CONT_NÚM*16,색상들[0]);
    int 가로=Terminal_entrada->coordenada_X+12,Vertical_cargo=Terminal_entrada->Y_coordenada+36,폭=Terminal_entrada->COLS*8,duração_VALOR=Terminal_entrada->LIN_CONT_NÚM*16;
    if(보드그림범위(&가로,&Vertical_cargo,&폭,&duração_VALOR)){
    unsigned 첫줄=(Vertical_cargo-Terminal_entrada->Y_coordenada-36)/16,끝줄=(Vertical_cargo+duração_VALOR-Terminal_entrada->Y_coordenada-36+15)/16;
    unsigned 첫칸=(가로-Terminal_entrada->coordenada_X-12)/8,끝칸=(가로+폭-Terminal_entrada->coordenada_X-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 limite_VALOR 왼쪽에서 시작한 두 slot_entrada 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned ponto_de_código=첫칸;ponto_de_código<끝칸;ponto_de_código++){
        unsigned LIN_cargo=첫항목()-Terminal_entrada->rolar+반환값,caractere_VALOR=Terminal_entrada->글자칸들[LIN_cargo%Histórico_linha_CONT_NÚM][ponto_de_código],cadeia_dados=Terminal_entrada->모양들[LIN_cargo%Histórico_linha_CONT_NÚM][ponto_de_código];
        if(caractere_largo(caractere_VALOR)==2&&ponto_de_código+1>=Terminal_entrada->COLS)caractere_VALOR=' ';
        if((caractere_VALOR==0||caractere_VALOR==' ')&&(cadeia_dados>>4)==0)continue;
        Terminal_glifo(Terminal_entrada->coordenada_X+12+ponto_de_código*8,Terminal_entrada->Y_coordenada+36+반환값*16,caractere_VALOR?caractere_VALOR:' ',색상들[cadeia_dados&15],색상들[cadeia_dados>>4]);
    }}
    nome_tabela(Terminal_entrada->coordenada_X+12,Terminal_entrada->Y_coordenada+Terminal_entrada->altura_VALOR-18,Terminal_entrada->rolar?"PgDn: recent output":Terminal_entrada->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);circunflexo_VALOR(1);
}
static void execução_quadro(int identificador_VALOR){
    Terminal_entrada=&Windows_Lista[identificador_VALOR];
    int 가로=Terminal_entrada->coordenada_X,Vertical_cargo=Terminal_entrada->Y_coordenada,폭=Terminal_entrada->너비,duração_VALOR=Terminal_entrada->altura_VALOR;
    if(!보드그림범위(&가로,&Vertical_cargo,&폭,&duração_VALOR))return;
    사각영역(Terminal_entrada->coordenada_X,Terminal_entrada->Y_coordenada,Terminal_entrada->너비,Terminal_entrada->altura_VALOR,0x403127);
    unsigned 색상=identificador_VALOR==Foco?0x905020:0x604438;사각영역(Terminal_entrada->coordenada_X,Terminal_entrada->Y_coordenada,Terminal_entrada->너비,30,색상);
    nome_tabela(Terminal_entrada->coordenada_X+12,Terminal_entrada->Y_coordenada+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identificador_VALOR),0};nome_tabela(Terminal_entrada->coordenada_X+148,Terminal_entrada->Y_coordenada+7,수치,0xffffff,색상);
    nome_tabela(Terminal_entrada->coordenada_X+240,Terminal_entrada->Y_coordenada+7,Terminal_entrada->너비>=500?(한글입력?"[PT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[PT]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_entrada->coordenada_X+Terminal_entrada->너비-32,Terminal_entrada->Y_coordenada+4,26,22,0x5555b8);nome_tabela(Terminal_entrada->coordenada_X+Terminal_entrada->너비-24,Terminal_entrada->Y_coordenada+7,"X",0xffffff,0x5555b8);
    Conteúdo_VALOR();
}
static void emitir_cena(void){
    if(!desktop_Exibir)return;사각영역(0,0,보드화면너비(),Quadro_tela_altura(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nome_tabela(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lista[순번].살아있음){unsigned ponto_de_código=Foco==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,ponto_de_código);nome_tabela(160+순번*112,8,"Terminal",0xffffff,ponto_de_código);char cadeia_dados[2]={(char)('1'+순번),0};nome_tabela(232+순번*112,8,cadeia_dados,0xffffff,ponto_de_código);}
    if(!entrada_CONT_NÚM_8f7753a1)nome_tabela(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<entrada_CONT_NÚM_8f7753a1;순번++)execução_quadro(ordem_VALOR[순번]);화면다시그림(Foco);Terminal_entrada=&Windows_Lista[saída];
}
static void Paint_região(int 가로,int Vertical_cargo,int 폭,int duração_VALOR){
    if(!desktop_Exibir||!보드그림범위(&가로,&Vertical_cargo,&폭,&duração_VALOR))return;
    for(int linha_de_entrada=Vertical_cargo;linha_de_entrada<Vertical_cargo+duração_VALOR;linha_de_entrada+=32){
        int banda_altura=Vertical_cargo+duração_VALOR-linha_de_entrada;if(banda_altura>32)banda_altura=32;
        if(Quadro_START_desenho(가로,linha_de_entrada,폭,banda_altura)){emitir_cena();Quadro_fim_desenho();}
    }
}
static void 다시그리기(void){Paint_região(0,0,보드화면너비(),Quadro_tela_altura());}
/* 서로 겹치지 않는 새 Janela 영역과 Anterior_item 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertical_cargo,int 폭,int duração_VALOR,Terminal *Janela){
    int 왼쪽=가로>(int)Janela->coordenada_X?가로:(int)Janela->coordenada_X;
    int 위쪽=Vertical_cargo>(int)Janela->Y_coordenada?Vertical_cargo:(int)Janela->Y_coordenada;
    int DIREITA=가로+폭<(int)(Janela->coordenada_X+Janela->너비)?가로+폭:(int)(Janela->coordenada_X+Janela->너비);
    int 아래쪽=Vertical_cargo+duração_VALOR<(int)(Janela->Y_coordenada+Janela->altura_VALOR)?Vertical_cargo+duração_VALOR:(int)(Janela->Y_coordenada+Janela->altura_VALOR);
    Paint_região(Janela->coordenada_X,Janela->Y_coordenada,Janela->너비,Janela->altura_VALOR);
    if(왼쪽>=DIREITA||위쪽>=아래쪽){Paint_região(가로,Vertical_cargo,폭,duração_VALOR);return;}
    Paint_região(가로,Vertical_cargo,폭,위쪽-Vertical_cargo);
    Paint_região(가로,아래쪽,폭,Vertical_cargo+duração_VALOR-아래쪽);
    Paint_região(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_região(DIREITA,위쪽,가로+폭-DIREITA,아래쪽-위쪽);
}
static void sinal_Foco(void){TI_Pendente=(TI_Pendente&~15u)|(unsigned)(Foco+1)|0x10000;}
void Terminal_entrada_MODO(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Foco>=0){
        Terminal *janela_entrada=&Windows_Lista[Foco];
        nome_tabela(janela_entrada->coordenada_X+240,janela_entrada->Y_coordenada+7,janela_entrada->너비>=500?(한글입력?"[PT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[PT]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identificador_VALOR){if(identificador_VALOR<0||identificador_VALOR>=4||!Windows_Lista[identificador_VALOR].살아있음)return;int em_dia_cargo=0;while(em_dia_cargo<entrada_CONT_NÚM_8f7753a1&&ordem_VALOR[em_dia_cargo]!=identificador_VALOR)em_dia_cargo++;for(;em_dia_cargo+1<entrada_CONT_NÚM_8f7753a1;em_dia_cargo++)ordem_VALOR[em_dia_cargo]=ordem_VALOR[em_dia_cargo+1];ordem_VALOR[entrada_CONT_NÚM_8f7753a1-1]=identificador_VALOR;Foco=identificador_VALOR;sinal_Foco();다시그리기();}
static void em_branco(unsigned LIN_cargo){for(unsigned ponto_de_código=0;ponto_de_código<최대열수;ponto_de_código++){Terminal_entrada->글자칸들[LIN_cargo%Histórico_linha_CONT_NÚM][ponto_de_código]=0;Terminal_entrada->모양들[LIN_cargo%Histórico_linha_CONT_NÚM][ponto_de_código]=Terminal_entrada->전경색|(Terminal_entrada->배경색<<4);}}
static void limpar_Sumário(void){Terminal_entrada->LIN_cargo=Terminal_entrada->COL_cargo=Terminal_entrada->맨위=Terminal_entrada->rolar=0;for(unsigned 반환값=0;반환값<Histórico_linha_CONT_NÚM;반환값++)em_branco(반환값);if(보이는지())Conteúdo_VALOR();}
static int Criar_entrada(void){
    if(!보드화면기억공간())return -19;int identificador_VALOR=0;while(identificador_VALOR<4&&Windows_Lista[identificador_VALOR].살아있음)identificador_VALOR++;if(identificador_VALOR==4)return -28;
    desktop_Exibir=1;Terminal_entrada=&Windows_Lista[identificador_VALOR];memset(Terminal_entrada,0,sizeof(*Terminal_entrada));Terminal_entrada->살아있음=1;Terminal_entrada->너비=568;Terminal_entrada->altura_VALOR=360;Terminal_entrada->COLS=68;Terminal_entrada->LIN_CONT_NÚM=19;Terminal_entrada->coordenada_X=12+identificador_VALOR*16;Terminal_entrada->Y_coordenada=48+identificador_VALOR*18;Terminal_entrada->전경색=7;Terminal_entrada->가리개보임=1;
    for(unsigned 반환값=0;반환값<Histórico_linha_CONT_NÚM;반환값++)em_branco(반환값);ordem_VALOR[entrada_CONT_NÚM_8f7753a1++]=identificador_VALOR;Foco=identificador_VALOR;TI_Pendente|=1u<<(4+identificador_VALOR);sinal_Foco();다시그리기();return identificador_VALOR+1;
}
static void Close_janela(int identificador_VALOR){
    if(identificador_VALOR<0||identificador_VALOR>=4||!Windows_Lista[identificador_VALOR].살아있음)return;Windows_Lista[identificador_VALOR].살아있음=0;TI_Pendente|=1u<<(8+identificador_VALOR);
    int em_dia_cargo=0;while(em_dia_cargo<entrada_CONT_NÚM_8f7753a1&&ordem_VALOR[em_dia_cargo]!=identificador_VALOR)em_dia_cargo++;for(;em_dia_cargo+1<entrada_CONT_NÚM_8f7753a1;em_dia_cargo++)ordem_VALOR[em_dia_cargo]=ordem_VALOR[em_dia_cargo+1];entrada_CONT_NÚM_8f7753a1--;
    if(Foco==identificador_VALOR)Foco=entrada_CONT_NÚM_8f7753a1?ordem_VALOR[entrada_CONT_NÚM_8f7753a1-1]:-1;sinal_Foco();다시그리기();
}
static void 줄바꿈(void){Terminal_entrada->COL_cargo=0;Terminal_entrada->LIN_cargo++;if(Terminal_entrada->LIN_cargo>=Terminal_entrada->맨위+Terminal_entrada->LIN_CONT_NÚM){Terminal_entrada->맨위++;em_branco(Terminal_entrada->LIN_cargo);if(보이는지())Conteúdo_VALOR();}}
static void ponto_de_código_451f2815(unsigned ponto_de_código){
    if(ponto_de_código==13){Terminal_entrada->COL_cargo=0;return;}if(ponto_de_código==10){줄바꿈();return;}if(ponto_de_código==8){if(Terminal_entrada->COL_cargo)Terminal_entrada->COL_cargo--;return;}
    if(ponto_de_código==9){unsigned item_CONT_NÚM=8-Terminal_entrada->COL_cargo%8;while(item_CONT_NÚM--)ponto_de_código_451f2815(' ');return;}if(ponto_de_código<32||ponto_de_código==127)return;
    unsigned 너비값=caractere_largo(ponto_de_código);if(Terminal_entrada->COL_cargo+너비값>Terminal_entrada->COLS)줄바꿈();
    if(Terminal_entrada->글자칸들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo]==0xffffffffu&&Terminal_entrada->COL_cargo){Terminal_entrada->글자칸들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo-1]=' ';Paint_tela(Terminal_entrada->LIN_cargo,Terminal_entrada->COL_cargo-1);}
    if(caractere_largo(Terminal_entrada->글자칸들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo])==2&&Terminal_entrada->COL_cargo+1<Terminal_entrada->COLS){Terminal_entrada->글자칸들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo+1]=' ';Paint_tela(Terminal_entrada->LIN_cargo,Terminal_entrada->COL_cargo+1);}
    Terminal_entrada->글자칸들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo]=ponto_de_código;Terminal_entrada->모양들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo]=Terminal_entrada->전경색|(Terminal_entrada->배경색<<4);
    if(너비값==2)Terminal_entrada->글자칸들[Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM][Terminal_entrada->COL_cargo+1]=0xffffffffu;
    Paint_tela(Terminal_entrada->LIN_cargo,Terminal_entrada->COL_cargo);Terminal_entrada->COL_cargo+=너비값;
}
static void alça_código_de_controle(unsigned ponto_de_código){
    unsigned item_CONT_NÚM=Terminal_entrada->parâmetro_VALOR[0]?Terminal_entrada->parâmetro_VALOR[0]:1;
    if(ponto_de_código=='m')for(unsigned 순번=0;순번<=Terminal_entrada->parâmetro_ÍNDICE;순번++){unsigned dados_cargo=Terminal_entrada->parâmetro_VALOR[순번];if(!dados_cargo){Terminal_entrada->전경색=7;Terminal_entrada->배경색=0;}if(dados_cargo==1&&Terminal_entrada->전경색<8)Terminal_entrada->전경색+=8;if(dados_cargo==7){unsigned reter_VALOR=Terminal_entrada->전경색;Terminal_entrada->전경색=Terminal_entrada->배경색;Terminal_entrada->배경색=reter_VALOR;}if(dados_cargo>=30&&dados_cargo<=37)Terminal_entrada->전경색=dados_cargo-30;if(dados_cargo>=90&&dados_cargo<=97)Terminal_entrada->전경색=dados_cargo-90+8;if(dados_cargo>=40&&dados_cargo<=47)Terminal_entrada->배경색=dados_cargo-40;if(dados_cargo>=100&&dados_cargo<=107)Terminal_entrada->배경색=dados_cargo-100+8;if(dados_cargo==39)Terminal_entrada->전경색=7;if(dados_cargo==49)Terminal_entrada->배경색=0;}
    if(ponto_de_código=='J'&&(Terminal_entrada->parâmetro_VALOR[0]==2||Terminal_entrada->parâmetro_VALOR[0]==3))limpar_Sumário();
    if(ponto_de_código=='K'){unsigned 출발위치=Terminal_entrada->parâmetro_VALOR[0]==2?0:Terminal_entrada->COL_cargo,도착위치=Terminal_entrada->parâmetro_VALOR[0]==1?Terminal_entrada->COL_cargo+1:Terminal_entrada->COLS;if(Terminal_entrada->parâmetro_VALOR[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_entrada->COLS;순번++){
        unsigned LIN_VALOR=Terminal_entrada->LIN_cargo%Histórico_linha_CONT_NÚM,caractere_VALOR=Terminal_entrada->글자칸들[LIN_VALOR][순번],forma_VALOR=Terminal_entrada->전경색|(Terminal_entrada->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fonte_VALOR 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(caractere_VALOR!=0&&caractere_VALOR!=' ')||Terminal_entrada->모양들[LIN_VALOR][순번]!=forma_VALOR;
        Terminal_entrada->글자칸들[LIN_VALOR][순번]=' ';Terminal_entrada->모양들[LIN_VALOR][순번]=forma_VALOR;
        if(바뀜)Paint_tela(Terminal_entrada->LIN_cargo,순번);
    }}
    if(ponto_de_código=='D')Terminal_entrada->COL_cargo=item_CONT_NÚM>Terminal_entrada->COL_cargo?0:Terminal_entrada->COL_cargo-item_CONT_NÚM;if(ponto_de_código=='C')Terminal_entrada->COL_cargo=Terminal_entrada->COL_cargo+item_CONT_NÚM>=Terminal_entrada->COLS?Terminal_entrada->COLS-1:Terminal_entrada->COL_cargo+item_CONT_NÚM;
    if(ponto_de_código=='G')Terminal_entrada->COL_cargo=item_CONT_NÚM>Terminal_entrada->COLS?Terminal_entrada->COLS-1:item_CONT_NÚM-1;if(ponto_de_código=='A')Terminal_entrada->LIN_cargo=item_CONT_NÚM>Terminal_entrada->LIN_cargo-Terminal_entrada->맨위?Terminal_entrada->맨위:Terminal_entrada->LIN_cargo-item_CONT_NÚM;
    if(ponto_de_código=='B')Terminal_entrada->LIN_cargo=Terminal_entrada->LIN_cargo+item_CONT_NÚM>=Terminal_entrada->맨위+Terminal_entrada->LIN_CONT_NÚM?Terminal_entrada->맨위+Terminal_entrada->LIN_CONT_NÚM-1:Terminal_entrada->LIN_cargo+item_CONT_NÚM;
    if(ponto_de_código=='H'||ponto_de_código=='f'){Terminal_entrada->LIN_cargo=Terminal_entrada->맨위+(item_CONT_NÚM>Terminal_entrada->LIN_CONT_NÚM?Terminal_entrada->LIN_CONT_NÚM:item_CONT_NÚM)-1;unsigned coordenada_X=Terminal_entrada->parâmetro_VALOR[1]?Terminal_entrada->parâmetro_VALOR[1]:1;Terminal_entrada->COL_cargo=(coordenada_X>Terminal_entrada->COLS?Terminal_entrada->COLS:coordenada_X)-1;}
    if(ponto_de_código=='s'){Terminal_entrada->저장행=Terminal_entrada->LIN_cargo;Terminal_entrada->저장열=Terminal_entrada->COL_cargo;}if(ponto_de_código=='u'){Terminal_entrada->LIN_cargo=Terminal_entrada->저장행;Terminal_entrada->COL_cargo=Terminal_entrada->저장열<Terminal_entrada->COLS?Terminal_entrada->저장열:Terminal_entrada->COLS-1;}
    if((ponto_de_código=='h'||ponto_de_código=='l')&&Terminal_entrada->parâmetro_VALOR[0]==25)Terminal_entrada->가리개보임=ponto_de_código=='h';
}
void Terminal_byte(unsigned SEGUNDO_VALOR){
    Terminal_entrada=&Windows_Lista[saída];if(!Terminal_entrada->살아있음)return;circunflexo_VALOR(0);if(Terminal_entrada->rolar){Terminal_entrada->rolar=0;if(보이는지())Conteúdo_VALOR();}
    if(Terminal_entrada->탈출상태==1){Terminal_entrada->탈출상태=SEGUNDO_VALOR=='['?2:0;Terminal_entrada->parâmetro_ÍNDICE=0;for(unsigned 순번=0;순번<4;순번++)Terminal_entrada->parâmetro_VALOR[순번]=0;}
    else if(Terminal_entrada->탈출상태==2){if(SEGUNDO_VALOR=='?'){}else if(SEGUNDO_VALOR>='0'&&SEGUNDO_VALOR<='9'){if(Terminal_entrada->parâmetro_VALOR[Terminal_entrada->parâmetro_ÍNDICE]<10000)Terminal_entrada->parâmetro_VALOR[Terminal_entrada->parâmetro_ÍNDICE]=Terminal_entrada->parâmetro_VALOR[Terminal_entrada->parâmetro_ÍNDICE]*10+SEGUNDO_VALOR-'0';}else if(SEGUNDO_VALOR==';'&&Terminal_entrada->parâmetro_ÍNDICE<3)Terminal_entrada->parâmetro_ÍNDICE++;else{alça_código_de_controle(SEGUNDO_VALOR);Terminal_entrada->탈출상태=0;}}
    else if(SEGUNDO_VALOR==27){Terminal_entrada->긴부호없는값=0;Terminal_entrada->탈출상태=1;}else{
        if(Terminal_entrada->긴부호없는값&&(SEGUNDO_VALOR&0xc0)!=0x80){Terminal_entrada->긴부호없는값=0;ponto_de_código_451f2815(0xfffd);}
        if(Terminal_entrada->긴부호없는값){Terminal_entrada->부호없는결과=Terminal_entrada->부호없는결과*64+(SEGUNDO_VALOR&63);if(--Terminal_entrada->긴부호없는값==0)ponto_de_código_451f2815(Terminal_entrada->부호없는결과<Terminal_entrada->MENOR_VALOR||Terminal_entrada->부호없는결과>0x10ffff||(Terminal_entrada->부호없는결과>=0xd800&&Terminal_entrada->부호없는결과<=0xdfff)?0xfffd:Terminal_entrada->부호없는결과);}
        else if(SEGUNDO_VALOR<128)ponto_de_código_451f2815(SEGUNDO_VALOR);else if(SEGUNDO_VALOR>=0xc2&&SEGUNDO_VALOR<=0xf4){Terminal_entrada->긴부호없는값=SEGUNDO_VALOR<0xe0?1:SEGUNDO_VALOR<0xf0?2:3;Terminal_entrada->부호없는결과=SEGUNDO_VALOR&((1u<<(6-Terminal_entrada->긴부호없는값))-1);Terminal_entrada->MENOR_VALOR=Terminal_entrada->긴부호없는값==1?128:Terminal_entrada->긴부호없는값==2?2048:65536;}else ponto_de_código_451f2815(0xfffd);
    }circunflexo_VALOR(1);
}
int Terminal_Pendente(void){return TI_Pendente!=0;}
/* 모서리 ÍNDICE: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int redimensionar_arrastar=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertical_cargo) {
    for(int SEQUÊNCIA_VALOR=entrada_CONT_NÚM_8f7753a1-1;SEQUÊNCIA_VALOR>=0;SEQUÊNCIA_VALOR--){
        int identificador_VALOR=ordem_VALOR[SEQUÊNCIA_VALOR];Terminal *Janela=&Windows_Lista[identificador_VALOR];
        if(가로>=(int)Janela->coordenada_X&&Vertical_cargo>=(int)Janela->Y_coordenada&&
           가로<(int)(Janela->coordenada_X+Janela->너비)&&Vertical_cargo<(int)(Janela->Y_coordenada+Janela->altura_VALOR))return identificador_VALOR;
    }return -1;
}
static int 모서리찾기(int identificador_VALOR,int 가로,int Vertical_cargo) {
    if(identificador_VALOR<0)return 0;Terminal *Janela=&Windows_Lista[identificador_VALOR];
    int 왼쪽=가로<(int)Janela->coordenada_X+8,DIREITA=가로>=(int)(Janela->coordenada_X+Janela->너비)-8;
    int 위쪽=Vertical_cargo<(int)Janela->Y_coordenada+8,아래쪽=Vertical_cargo>=(int)(Janela->Y_coordenada+Janela->altura_VALOR)-8;
    return (왼쪽||DIREITA)&&(위쪽||아래쪽)?1+DIREITA+아래쪽*2:0;
}
static int separador_VALOR(int VALOR,int 최소,int 최대){return VALOR<최소?최소:VALOR>최대?최대:VALOR;}
static void mover_redimensionar(int 가로,int Vertical_cargo) {
    Terminal *Janela=&Windows_Lista[redimensionar_arrastar];int 왼쪽=처음가로,위쪽=처음세로,DIREITA=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=separador_VALOR(처음가로+가로-잡은가로,0,DIREITA-360);
    else DIREITA=separador_VALOR(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=separador_VALOR(처음세로+Vertical_cargo-잡은세로,34,아래쪽-216);
    else 아래쪽=separador_VALOR(처음세로+처음높이+Vertical_cargo-잡은세로,위쪽+216,Quadro_tela_altura());
    unsigned COLS=(DIREITA-왼쪽-24)/8,LIN_CONT_NÚM=(아래쪽-위쪽-56)/16;
    if(Janela->COLS!=COLS||Janela->LIN_CONT_NÚM!=LIN_CONT_NÚM){
        Janela->크기바뀜=1;Janela->COLS=COLS;Janela->LIN_CONT_NÚM=LIN_CONT_NÚM;
        if(Janela->COL_cargo>=COLS)Janela->COL_cargo=COLS-1;
        if(Janela->LIN_cargo>=Janela->맨위+LIN_CONT_NÚM)Janela->맨위=Janela->LIN_cargo-LIN_CONT_NÚM+1;
        unsigned 한도=Janela->맨위;if(한도>Histórico_linha_CONT_NÚM-LIN_CONT_NÚM)한도=Histórico_linha_CONT_NÚM-LIN_CONT_NÚM;
        if(Janela->rolar>한도)Janela->rolar=한도;
    }
    int 옛가로=Janela->coordenada_X,옛세로=Janela->Y_coordenada,옛폭=Janela->너비,옛길이=Janela->altura_VALOR;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==DIREITA-왼쪽&&옛길이==아래쪽-위쪽)return;
    Janela->coordenada_X=왼쪽;Janela->Y_coordenada=위쪽;Janela->너비=DIREITA-왼쪽;Janela->altura_VALOR=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Janela);
}
void Terminal_ponteiro(unsigned Avançar_item,int coordenada_X,int Y_coordenada){
    unsigned 눌림=Avançar_item&~단추들;단추들=Avançar_item;
    if(!desktop_Exibir){arrastar_VALOR=-1;redimensionar_arrastar=-1;Quadro_ponteiro(coordenada_X,Y_coordenada,1);return;}
    if(!(Avançar_item&1)){arrastar_VALOR=-1;redimensionar_arrastar=-1;}
    if(redimensionar_arrastar>=0&&!Windows_Lista[redimensionar_arrastar].살아있음)redimensionar_arrastar=-1;
    if(arrastar_VALOR>=0&&!Windows_Lista[arrastar_VALOR].살아있음)arrastar_VALOR=-1;
    if(redimensionar_arrastar>=0){
        mover_redimensionar(coordenada_X,Y_coordenada);Quadro_ponteiro(coordenada_X,Y_coordenada,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Quadro_ponteiro(coordenada_X,Y_coordenada,1);
    if(arrastar_VALOR>=0){
        Terminal *Janela=&Windows_Lista[arrastar_VALOR];
        int 옛가로=Janela->coordenada_X,옛세로=Janela->Y_coordenada;
        Janela->coordenada_X=separador_VALOR(coordenada_X-arrastar_X,0,보드화면너비()-Janela->너비);
        Janela->Y_coordenada=separador_VALOR(Y_coordenada-arrastar_Y,34,Quadro_tela_altura()-Janela->altura_VALOR);
        if(옛가로!=(int)Janela->coordenada_X||옛세로!=(int)Janela->Y_coordenada)창자리그리기(옛가로,옛세로,Janela->너비,Janela->altura_VALOR,Janela);
        return;
    }
    extern int tela_sobreposição(int,int,int);
    if(tela_sobreposição(Foco,coordenada_X,Y_coordenada)){tela_ponteiro(Foco,눌림,coordenada_X,Y_coordenada);return;}
    int identificador_VALOR=가리킨창(coordenada_X,Y_coordenada),모서리=모서리찾기(identificador_VALOR,coordenada_X,Y_coordenada);
    if(모서리)Quadro_ponteiro(coordenada_X,Y_coordenada,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Janela=&Windows_Lista[identificador_VALOR];redimensionar_arrastar=identificador_VALOR;잡은모서리=모서리;잡은가로=coordenada_X;잡은세로=Y_coordenada;
            처음가로=Janela->coordenada_X;처음세로=Janela->Y_coordenada;처음너비=Janela->너비;처음높이=Janela->altura_VALOR;
            if(identificador_VALOR!=Foco)앞으로올리기(identificador_VALOR);return;
        }
        if(Y_coordenada<32&&coordenada_X>=6&&coordenada_X<142){Criar_entrada();return;}
        if(Y_coordenada<32&&coordenada_X>=154&&coordenada_X<602){앞으로올리기((coordenada_X-154)/112);return;}
        if(identificador_VALOR>=0){
            Terminal *Janela=&Windows_Lista[identificador_VALOR];
            if(Y_coordenada<(int)Janela->Y_coordenada+30&&coordenada_X>=(int)(Janela->coordenada_X+Janela->너비)-32){Close_janela(identificador_VALOR);return;}
            if(identificador_VALOR!=Foco)앞으로올리기(identificador_VALOR);
            if(Y_coordenada<(int)Janela->Y_coordenada+30){arrastar_VALOR=identificador_VALOR;arrastar_X=coordenada_X-Janela->coordenada_X;arrastar_Y=Y_coordenada-Janela->Y_coordenada;}return;
        }
    }
    if(Foco>=0&&(눌림&(8|16))){Terminal_entrada=&Windows_Lista[Foco];if(눌림&8){unsigned 한도=Terminal_entrada->맨위;if(한도>Histórico_linha_CONT_NÚM-Terminal_entrada->LIN_CONT_NÚM)한도=Histórico_linha_CONT_NÚM-Terminal_entrada->LIN_CONT_NÚM;Terminal_entrada->rolar=Terminal_entrada->rolar+9>한도?한도:Terminal_entrada->rolar+9;}else Terminal_entrada->rolar=Terminal_entrada->rolar<9?0:Terminal_entrada->rolar-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Criar_entrada();if(누름값==2&&entrada_CONT_NÚM_8f7753a1)앞으로올리기(ordem_VALOR[0]);if(누름값==3)Close_janela(Foco);}
computador_Word Quadro_Terminal(computador_Word Acção){
    if(Acção==300){if(!Windows_Lista[saída].살아있음)return Criar_entrada();desktop_Exibir=1;다시그리기();return 0;}
    if(Acção==0){Close_janela(Foco);return 0;}if(Acção==1)return (uint32_t)Criar_entrada();if(Acção==2)return Foco>=0;
    if(Acção==9){desktop_Exibir=0;return 0;}if(Acção==7)return entrada_CONT_NÚM_8f7753a1;if(Acção==10)return Foco+1;if(Acção==11)return saída;
    if(Acção==13){Terminal *Janela=&Windows_Lista[saída];return Janela->살아있음?(Janela->LIN_CONT_NÚM<<16)|Janela->COLS:(19<<16)|68;}
    if(Acção==14){unsigned VALOR=Windows_Lista[saída].크기바뀜;Windows_Lista[saída].크기바뀜=0;return VALOR;}
    if(Acção==12){unsigned VALOR=TI_Pendente;TI_Pendente=0;return VALOR;}
    if(Acção>=20&&Acção<24)return Windows_Lista[Acção-20].살아있음;
    if(Acção>=100&&Acção<104){saída=Acção-100;Terminal_entrada=&Windows_Lista[saída];return 0;}
    if(Acção>=200&&Acção<204){앞으로올리기(Acção-200);return 0;}
    if(Acção==3){다시그리기();return 0;}Terminal_entrada=&Windows_Lista[saída];if(!Terminal_entrada->살아있음)return 0;
    if(Acção==4)limpar_Sumário();if(Acção==5||Acção==6){unsigned Anterior_item=단추들;Terminal_ponteiro(Acção==5?8:16,0,0);단추들=Anterior_item;}return 1;
}
