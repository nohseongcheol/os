/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Ligar, 제한된 entrada_VALOR duração_VALOR, 비동기 enviar_VALOR, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 tela dados 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "remoto_VALOR.h"
#include "criptografia_Suporte.h"
#include "Perfil.h"
#include "../rede_pilha/rede_pilha.h"
#include "../computador/tela_informações.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(tela_senha)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Quadro_Terminal(uintptr_t);
void remoto_Chave_traço(unsigned,int);
void inicializar_remoto_Chave_traço(void);
void commit_remoto_Chave(void);
static int Estou_ouvindo_empresa=-1,par_VALOR=-1,fase_VALOR,닫을예정;
static uintptr_t conexão_time,다시받을때;
static unsigned char entrada_VALOR[8192],saídaTexto[4096],desafio_VALOR[16];
static unsigned entrada_CONT_NÚM,saída_CONT_NÚM,보낸수;
static unsigned 너비,altura_VALOR,pixel_dimensionar=4,big_endian_VALOR,빨강최대=255,초록최대=255,파랑최대=255,vermelho_deslocar=16,verde_deslocar=8,azul_deslocar;
static uint32_t Anterior_resumo[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned peça_CONT_NÚM,peça_cargo,solicitado_X,solicitado_Y,요청폭,solicitado_altura;
static unsigned leitura_16(const unsigned char *dados_cargo){return(unsigned)dados_cargo[0]*256+dados_cargo[1];}
static uint32_t leitura_32(const unsigned char *dados_cargo){return(uint32_t)dados_cargo[0]<<24|(uint32_t)dados_cargo[1]<<16|(uint32_t)dados_cargo[2]<<8|dados_cargo[3];}
static void gravar_16(unsigned char *dados_cargo,unsigned VALOR){dados_cargo[0]=VALOR>>8;dados_cargo[1]=VALOR;}
static void gravar_32(unsigned char *dados_cargo,uint32_t VALOR){dados_cargo[0]=VALOR>>24;dados_cargo[1]=VALOR>>16;dados_cargo[2]=VALOR>>8;dados_cargo[3]=VALOR;}
static void Fechar(void){if(par_VALOR>=0)Close_rede(par_VALOR);par_VALOR=-1;fase_VALOR=0;entrada_CONT_NÚM=saída_CONT_NÚM=보낸수=0;peça_CONT_NÚM=peça_cargo=0;닫을예정=0;inicializar_remoto_Chave_traço();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *dados,unsigned número){memcpy(saídaTexto,dados,número);saída_CONT_NÚM=número;보낸수=0;}
static void consumir_VALOR(unsigned número){entrada_CONT_NÚM-=número;memmove(entrada_VALOR,entrada_VALOR+número,entrada_CONT_NÚM);}
int visual_remoto_visor(unsigned Acção){
    if(Acção==0){Fechar();if(Estou_ouvindo_empresa>=0)Close_rede(Estou_ouvindo_empresa);Estou_ouvindo_empresa=-1;return 0;}
    if(Acção!=1)return Estou_ouvindo_empresa>=0;
    if(Estou_ouvindo_empresa>=0)return 0;
    int porta_VALOR=Criar_soquete_empresa(1);if(porta_VALOR<0)return porta_VALOR;통신주소재사용(porta_VALOR);
    int resultado=NET_BIND(porta_VALOR,0,5900);if(!resultado)resultado=NET_escutar(porta_VALOR);
    if(resultado<0){Close_rede(porta_VALOR);return resultado;}Estou_ouvindo_empresa=porta_VALOR;return 0;
}
static uint32_t peça_resumo(unsigned 가로,unsigned Vertical_cargo){
    uint32_t VALOR=2166136261u;
    for(unsigned Y_coordenada=Vertical_cargo;Y_coordenada<Vertical_cargo+16&&Y_coordenada<altura_VALOR;Y_coordenada++)for(unsigned coordenada_X=가로;coordenada_X<가로+32&&coordenada_X<너비;coordenada_X++)VALOR=(VALOR^Quadro_leitura_tela(coordenada_X,Y_coordenada))*16777619u;
    return VALOR;
}
static void tela_solicitação(const unsigned char *dados_cargo){
    solicitado_X=leitura_16(dados_cargo+2);solicitado_Y=leitura_16(dados_cargo+4);요청폭=leitura_16(dados_cargo+6);solicitado_altura=leitura_16(dados_cargo+8);
    if(solicitado_X>=너비||solicitado_Y>=altura_VALOR)요청폭=solicitado_altura=0;
    if(요청폭>너비-solicitado_X&&solicitado_X<너비)요청폭=너비-solicitado_X;
    if(solicitado_altura>altura_VALOR-solicitado_Y&&solicitado_Y<altura_VALOR)solicitado_altura=altura_VALOR-solicitado_Y;
    peça_CONT_NÚM=peça_cargo=0;
    if(요청폭&&solicitado_altura)for(unsigned Y_coordenada=solicitado_Y/16;Y_coordenada<=(solicitado_Y+solicitado_altura-1)/16;Y_coordenada++)for(unsigned coordenada_X=solicitado_X/32;coordenada_X<=(solicitado_X+요청폭-1)/32;coordenada_X++){
        unsigned cargo_ÍNDICE=Y_coordenada*60+coordenada_X;uint32_t resumo_VALOR=peça_resumo(coordenada_X*32,Y_coordenada*16);
        if(!dados_cargo[1]||Anterior_resumo[cargo_ÍNDICE]!=resumo_VALOR)바뀐타일[peça_CONT_NÚM++]=cargo_ÍNDICE;
    }
    saídaTexto[0]=saídaTexto[1]=0;gravar_16(saídaTexto+2,peça_CONT_NÚM);saída_CONT_NÚM=4;보낸수=0;
}
static void enviar_peça(void){
    unsigned cargo_ÍNDICE=바뀐타일[peça_cargo++],가로=(cargo_ÍNDICE%60)*32,Vertical_cargo=(cargo_ÍNDICE/60)*16;
    unsigned encerrar_X=가로+32,encerrar_Y=Vertical_cargo+16;if(encerrar_X>너비)encerrar_X=너비;if(encerrar_Y>altura_VALOR)encerrar_Y=altura_VALOR;
    /* 부분 타일 solicitação 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=solicitado_X&&Vertical_cargo>=solicitado_Y&&encerrar_X<=solicitado_X+요청폭&&encerrar_Y<=solicitado_Y+solicitado_altura;
    if(전부)Anterior_resumo[cargo_ÍNDICE]=peça_resumo(가로,Vertical_cargo);
    if(가로<solicitado_X)가로=solicitado_X;if(Vertical_cargo<solicitado_Y)Vertical_cargo=solicitado_Y;
    if(encerrar_X>solicitado_X+요청폭)encerrar_X=solicitado_X+요청폭;if(encerrar_Y>solicitado_Y+solicitado_altura)encerrar_Y=solicitado_Y+solicitado_altura;
    gravar_16(saídaTexto,가로);gravar_16(saídaTexto+2,Vertical_cargo);gravar_16(saídaTexto+4,encerrar_X-가로);gravar_16(saídaTexto+6,encerrar_Y-Vertical_cargo);gravar_32(saídaTexto+8,0);
    saída_CONT_NÚM=12;보낸수=0;
    for(unsigned Y_coordenada=Vertical_cargo;Y_coordenada<encerrar_Y;Y_coordenada++)for(unsigned coordenada_X=가로;coordenada_X<encerrar_X;coordenada_X++){
        uint32_t 색=Quadro_leitura_tela(coordenada_X,Y_coordenada),VALOR=(((색>>16)&255)*빨강최대/255)<<vermelho_deslocar|
            (((색>>8)&255)*초록최대/255)<<verde_deslocar|((색&255)*파랑최대/255)<<azul_deslocar;
        for(unsigned 순번=0;순번<pixel_dimensionar;순번++)saídaTexto[saída_CONT_NÚM++]=VALOR>>(8*(big_endian_VALOR?pixel_dimensionar-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Estou_ouvindo_empresa<0)return;
    if(par_VALOR<0){if(보드밀리초()<다시받을때)return;par_VALOR=NET_aceitar(Estou_ouvindo_empresa);if(par_VALOR<0)return;
        conexão_time=보드밀리초();fase_VALOR=1;내보내기("RFB 003.008\n",12);memset(Anterior_resumo,0,sizeof(Anterior_resumo));
        pixel_dimensionar=4;big_endian_VALOR=0;빨강최대=초록최대=파랑최대=255;vermelho_deslocar=16;verde_deslocar=8;azul_deslocar=0;}
    if(fase_VALOR<5&&보드밀리초()-conexão_time>15000){Fechar();return;}
    if(saída_CONT_NÚM){int número=NET_gravar(par_VALOR,saídaTexto+보낸수,saída_CONT_NÚM-보낸수);if(número>0){보낸수+=número;if(보낸수==saída_CONT_NÚM)saída_CONT_NÚM=보낸수=0;}else if(número!=-11){Fechar();return;}}
    if(!saída_CONT_NÚM&&닫을예정){Fechar();return;}
    if(!saída_CONT_NÚM&&peça_cargo<peça_CONT_NÚM)enviar_peça();
    if(entrada_CONT_NÚM==sizeof(entrada_VALOR)){Fechar();return;}
    int RECEBER_CONT_NÚM=NET_leitura(par_VALOR,entrada_VALOR+entrada_CONT_NÚM,sizeof(entrada_VALOR)-entrada_CONT_NÚM);
    if(RECEBER_CONT_NÚM==0||(RECEBER_CONT_NÚM<0&&RECEBER_CONT_NÚM!=-11)){Fechar();return;}if(RECEBER_CONT_NÚM>0)entrada_CONT_NÚM+=RECEBER_CONT_NÚM;
    if(saída_CONT_NÚM||peça_cargo<peça_CONT_NÚM)return;
    if(fase_VALOR==1&&entrada_CONT_NÚM>=12){if(memcmp(entrada_VALOR,"RFB 003.008\n",12)){Fechar();return;}consumir_VALOR(12);const unsigned char método_de_autenticação[]={1,2};내보내기(método_de_autenticação,2);fase_VALOR=2;return;}
    if(fase_VALOR==2&&entrada_CONT_NÚM){if(entrada_VALOR[0]!=2||remoto_aleatório(desafio_VALOR,16)){Fechar();return;}consumir_VALOR(1);내보내기(desafio_VALOR,16);fase_VALOR=3;return;}
    if(fase_VALOR==3&&entrada_CONT_NÚM>=16){unsigned char Chave_material[8],정답[16];br_des_ct_cbcenc_keys senha_VALOR;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALOR=tela_senha[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALOR&1);VALOR>>=1;}Chave_material[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&senha_VALOR,Chave_material,8);memcpy(정답,desafio_VALOR,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vetor_VALOR[8]={0};br_des_ct_cbcenc_run(&senha_VALOR,vetor_VALOR,정답+순번,8);memset(vetor_VALOR,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^entrada_VALOR[순번];consumir_VALOR(16);memset(&senha_VALOR,0,sizeof(senha_VALOR));memset(Chave_material,0,8);memset(정답,0,16);memset(desafio_VALOR,0,16);
        gravar_32(saídaTexto,차이?1:0);saída_CONT_NÚM=4;보낸수=0;
        if(차이){gravar_32(saídaTexto+4,19);memcpy(saídaTexto+8,"Authentication fail",19);saída_CONT_NÚM=27;닫을예정=1;}else fase_VALOR=4;return;}
    if(fase_VALOR==4&&entrada_CONT_NÚM){consumir_VALOR(1);너비=보드화면너비();altura_VALOR=Quadro_tela_altura();if(!너비||!altura_VALOR||너비>1920||altura_VALOR>1080){Fechar();return;}
        if(!Quadro_Terminal(7)){const unsigned char Evento[]={30,2,1,0,0,0,0};feed_remoto_entrada(Evento,7);}
        memset(saídaTexto,0,40);gravar_16(saídaTexto,너비);gravar_16(saídaTexto+2,altura_VALOR);saídaTexto[4]=32;saídaTexto[5]=24;saídaTexto[7]=1;
        gravar_16(saídaTexto+8,255);gravar_16(saídaTexto+10,255);gravar_16(saídaTexto+12,255);saídaTexto[14]=16;saídaTexto[15]=8;
        const char *Nome="jkoros native";gravar_32(saídaTexto+20,strlen(Nome));memcpy(saídaTexto+24,Nome,strlen(Nome));saída_CONT_NÚM=24+strlen(Nome);보낸수=0;fase_VALOR=5;return;}
    if(fase_VALOR!=5||!entrada_CONT_NÚM)return;
    unsigned TIPO_área=entrada_VALOR[0],필요=TIPO_área==0?20:TIPO_área==2?4:TIPO_área==3?10:TIPO_área==4?8:TIPO_área==5?6:TIPO_área==6?8:0;
    if(!필요){Fechar();return;}if(entrada_CONT_NÚM<필요)return;
    if(TIPO_área==2){unsigned número=leitura_16(entrada_VALOR+2);if(número>128){Fechar();return;}필요+=número*4;}
    if(TIPO_área==6){unsigned número=leitura_32(entrada_VALOR+4);if(número>4096){Fechar();return;}필요+=número;}
    if(entrada_CONT_NÚM<필요)return;
    if(TIPO_área==0){unsigned bit_VALOR=entrada_VALOR[4],빨=leitura_16(entrada_VALOR+8),초=leitura_16(entrada_VALOR+10),파=leitura_16(entrada_VALOR+12),vermelho_Canal_deslocar=entrada_VALOR[14],verde_Canal_deslocar=entrada_VALOR[15],azul_Canal_deslocar=entrada_VALOR[16];
        if((bit_VALOR!=16&&bit_VALOR!=32)||!entrada_VALOR[7]||entrada_VALOR[6]>1||!빨||!초||!파||빨>255||초>255||파>255||vermelho_Canal_deslocar>24||verde_Canal_deslocar>24||azul_Canal_deslocar>24||
           ((uint64_t)빨<<vermelho_Canal_deslocar)>((1ull<<bit_VALOR)-1)||((uint64_t)초<<verde_Canal_deslocar)>((1ull<<bit_VALOR)-1)||((uint64_t)파<<azul_Canal_deslocar)>((1ull<<bit_VALOR)-1)){Fechar();return;}
        pixel_dimensionar=bit_VALOR/8;big_endian_VALOR=entrada_VALOR[6];빨강최대=빨;초록최대=초;파랑최대=파;vermelho_deslocar=vermelho_Canal_deslocar;verde_deslocar=verde_Canal_deslocar;azul_deslocar=azul_Canal_deslocar;memset(Anterior_resumo,0,sizeof(Anterior_resumo));
    }else if(TIPO_área==3)tela_solicitação(entrada_VALOR);
    else if(TIPO_área==4)remoto_Chave_traço(leitura_32(entrada_VALOR+4),entrada_VALOR[1]!=0);
    else if(TIPO_área==5){unsigned coordenada_X=leitura_16(entrada_VALOR+2),Y_coordenada=leitura_16(entrada_VALOR+4);if(coordenada_X>=너비)coordenada_X=너비-1;if(Y_coordenada>=altura_VALOR)Y_coordenada=altura_VALOR-1;
        if(entrada_VALOR[1])commit_remoto_Chave();
        unsigned char Evento[]={30,1,entrada_VALOR[1],coordenada_X&255,coordenada_X>>8,Y_coordenada&255,Y_coordenada>>8};feed_remoto_entrada(Evento,sizeof(Evento));}
    consumir_VALOR(필요);
}
