#include "remoto_VALOR.h"
#include <string.h>
#include "두벌식표.h"
static unsigned visual_VALOR,tecla_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} composição_Estado;
static composição_Estado composição_VALOR,LOG_linha[16];
static unsigned LOG_CONT_NÚM;
void commit_remoto_Chave(void){memset(&composição_VALOR,0,sizeof(composição_VALOR));LOG_CONT_NÚM=0;}
void inicializar_remoto_Chave_traço(void){visual_VALOR=tecla_SHIFT=한글=0;commit_remoto_Chave();}
static void 글넣기(unsigned VALOR){
    unsigned char texto[4];unsigned número;
    if(VALOR<128){texto[0]=VALOR;número=1;}else if(VALOR<2048){texto[0]=0xc0|(VALOR>>6);texto[1]=0x80|(VALOR&63);número=2;}
    else if(VALOR<65536){texto[0]=0xe0|(VALOR>>12);texto[1]=0x80|((VALOR>>6)&63);texto[2]=0x80|(VALOR&63);número=3;}
    else{texto[0]=0xf0|(VALOR>>18);texto[1]=0x80|((VALOR>>12)&63);texto[2]=0x80|((VALOR>>6)&63);texto[3]=0x80|(VALOR&63);número=4;}
    feed_remoto_entrada(texto,número);
}
static int PROCURAR_entrada(const unsigned *entrada_Lista_f07b3200,unsigned número,unsigned VALOR){for(unsigned 순번=0;순번<número;순번++)if(entrada_Lista_f07b3200[순번]==VALOR)return 순번;return -1;}
static unsigned PROCURAR_Duplicar(const unsigned tabela_de_pesquisa[][3],unsigned número,unsigned 가,unsigned SEGUNDO_operando){for(unsigned 순번=0;순번<número;순번++)if(tabela_de_pesquisa[순번][0]==가&&tabela_de_pesquisa[순번][1]==SEGUNDO_operando)return tabela_de_pesquisa[순번][2];return 0;}
static unsigned 조합글(void){
    if(composição_VALOR.첫&&composição_VALOR.가운데)return 0xac00+(PROCURAR_entrada(첫소리목록,19,composição_VALOR.첫)*21+PROCURAR_entrada(가운뎃소리목록,21,composição_VALOR.가운데))*28+(composição_VALOR.끝?PROCURAR_entrada(끝소리목록,28,composição_VALOR.끝):0);
    return composição_VALOR.첫?composição_VALOR.첫:composição_VALOR.가운데;
}
static int 한글넣기(unsigned Chave_traço){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Chave_Layout)/sizeof(Chave_Layout[0]);순번++)if(Chave_Layout[순번][0]==Chave_traço)자모=Chave_Layout[순번][1];
    if(!자모&&Chave_traço>='A'&&Chave_traço<='Z')return 한글넣기(Chave_traço+32);if(!자모)return 0;
    unsigned Anterior_item=조합글(),commit_VALOR=0;composição_Estado 전=composição_VALOR;
    if(LOG_CONT_NÚM<16)LOG_linha[LOG_CONT_NÚM++]=전;
    if(PROCURAR_entrada(첫소리목록,19,자모)>=0){
        if(composição_VALOR.첫&&composição_VALOR.가운데&&!composição_VALOR.끝&&PROCURAR_entrada(끝소리목록,28,자모)>=0)composição_VALOR.끝=자모;
        else{unsigned sobreposição_VALOR=PROCURAR_Duplicar(겹끝소리,11,composição_VALOR.끝,자모);if(composição_VALOR.끝&&sobreposição_VALOR)composição_VALOR.끝=sobreposição_VALOR;
            else{commit_VALOR=Anterior_item;commit_remoto_Chave();composição_VALOR.첫=자모;LOG_CONT_NÚM=1;memset(LOG_linha,0,sizeof(composição_Estado));}}
    }else if(composição_VALOR.끝){
        unsigned 왼쪽=0,DIREITA=composição_VALOR.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==composição_VALOR.끝){왼쪽=겹끝소리[순번][0];DIREITA=겹끝소리[순번][1];break;}
        composição_VALOR.끝=왼쪽;commit_VALOR=조합글();commit_remoto_Chave();composição_VALOR.첫=DIREITA;composição_VALOR.가운데=자모;LOG_CONT_NÚM=2;
        memset(LOG_linha,0,2*sizeof(composição_Estado));LOG_linha[1].첫=DIREITA;
    }else if(composição_VALOR.가운데){unsigned sobreposição_VALOR=PROCURAR_Duplicar(겹가운뎃소리,7,composição_VALOR.가운데,자모);
        if(sobreposição_VALOR)composição_VALOR.가운데=sobreposição_VALOR;else{commit_VALOR=Anterior_item;commit_remoto_Chave();composição_VALOR.가운데=자모;LOG_CONT_NÚM=1;memset(LOG_linha,0,sizeof(composição_Estado));}
    }else composição_VALOR.가운데=자모;
    if(Anterior_item)글넣기(127);if(commit_VALOR)글넣기(commit_VALOR);unsigned AGORA_VALOR=조합글();if(AGORA_VALOR)글넣기(AGORA_VALOR);return 1;
}
void remoto_Chave_traço(unsigned símbolo,int 누름){
    if(símbolo==0xffe3||símbolo==0xffe4){visual_VALOR=누름;return;}
    if(símbolo==0xffe1||símbolo==0xffe2){tecla_SHIFT=누름;return;}
    if(!누름)return;
    if(símbolo==0xffc6||símbolo==0xff31||(símbolo==32&&tecla_SHIFT&&!visual_VALOR)){
        commit_remoto_Chave();한글=!한글;unsigned char Evento[]={30,3,한글,0,0,0,0};feed_remoto_entrada(Evento,7);return;
    }
    if(símbolo==0xff08&&한글&&!visual_VALOR&&LOG_CONT_NÚM){composição_VALOR=LOG_linha[--LOG_CONT_NÚM];글넣기(127);unsigned texto=조합글();if(texto)글넣기(texto);return;}
    if(한글&&!visual_VALOR&&símbolo<128&&한글넣기(símbolo))return;
    commit_remoto_Chave();
    if((visual_VALOR&&tecla_SHIFT&&(símbolo=='t'||símbolo=='T'))||símbolo==0xffc3||símbolo==0xffc9){unsigned char Evento[]={30,2,símbolo==0xffc3?2:símbolo==0xffc9?3:1,0,0,0,0};feed_remoto_entrada(Evento,7);return;}
    const char *특수=símbolo==0xff08?"\177":símbolo==0xff09?"\t":símbolo==0xff0d?"\r":símbolo==0xff1b?"\033":
        símbolo==0xffff?"\033[3~":símbolo==0xff50?"\033[H":símbolo==0xff57?"\033[F":símbolo==0xff51?"\033[D":
        símbolo==0xff52?"\033[A":símbolo==0xff53?"\033[C":símbolo==0xff54?"\033[B":símbolo==0xff55?"\033[5~":símbolo==0xff56?"\033[6~":0;
    if(특수){feed_remoto_entrada((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALOR=(símbolo&0xff000000)==0x01000000?símbolo&0xffffff:símbolo;
    if(VALOR>0x10ffff||(VALOR>=0xd800&&VALOR<=0xdfff)||(símbolo>=0xff00&&símbolo<0x1000000))return;
    if(visual_VALOR){if(VALOR>='a'&&VALOR<='z')VALOR-=96;else if(VALOR>='A'&&VALOR<='Z')VALOR-=64;}
    글넣기(VALOR);
}
