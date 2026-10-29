#include "remoto_VALOR.h"
#include <string.h>
#include "두벌식표.h"
static unsigned control_VALOR,tecla_MAIÚS,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_fila[16];
static unsigned LOG_CONTAR;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_CONTAR=0;}
void 원격글쇠초기화(void){control_VALOR=tecla_MAIÚS=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALOR){
    unsigned char Texto[4];unsigned 수;
    if(VALOR<128){Texto[0]=VALOR;수=1;}else if(VALOR<2048){Texto[0]=0xc0|(VALOR>>6);Texto[1]=0x80|(VALOR&63);수=2;}
    else if(VALOR<65536){Texto[0]=0xe0|(VALOR>>12);Texto[1]=0x80|((VALOR>>6)&63);Texto[2]=0x80|(VALOR&63);수=3;}
    else{Texto[0]=0xf0|(VALOR>>18);Texto[1]=0x80|((VALOR>>12)&63);Texto[2]=0x80|((VALOR>>6)&63);Texto[3]=0x80|(VALOR&63);수=4;}
    원격입력넣기(Texto,수);
}
static int Busca_introdución(const unsigned *introdución_Lista,unsigned 수,unsigned VALOR){for(unsigned 순번=0;순번<수;순번++)if(introdución_Lista[순번]==VALOR)return 순번;return -1;}
static unsigned Busca_copia(const unsigned Busca_táboa[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(Busca_táboa[순번][0]==가&&Busca_táboa[순번][1]==나)return Busca_táboa[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(Busca_introdución(첫소리목록,19,조합.첫)*21+Busca_introdución(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?Busca_introdución(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Chave_deseño)/sizeof(Chave_deseño[0]);순번++)if(Chave_deseño[순번][0]==글쇠)자모=Chave_deseño[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_CONTAR<16)LOG_fila[LOG_CONTAR++]=전;
    if(Busca_introdución(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&Busca_introdución(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned superposición_VALOR=Busca_copia(겹끝소리,11,조합.끝,자모);if(조합.끝&&superposición_VALOR)조합.끝=superposición_VALOR;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_CONTAR=1;memset(LOG_fila,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,DEREITA=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];DEREITA=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=DEREITA;조합.가운데=자모;LOG_CONTAR=2;
        memset(LOG_fila,0,2*sizeof(조합상태));LOG_fila[1].첫=DEREITA;
    }else if(조합.가운데){unsigned superposición_VALOR=Busca_copia(겹가운뎃소리,7,조합.가운데,자모);
        if(superposición_VALOR)조합.가운데=superposición_VALOR;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_CONTAR=1;memset(LOG_fila,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned AGORA_VALOR=조합글();if(AGORA_VALOR)글넣기(AGORA_VALOR);return 1;
}
void 원격글쇠(unsigned símbolo,int pulsar_VALOR){
    if(símbolo==0xffe3||símbolo==0xffe4){control_VALOR=pulsar_VALOR;return;}
    if(símbolo==0xffe1||símbolo==0xffe2){tecla_MAIÚS=pulsar_VALOR;return;}
    if(!pulsar_VALOR)return;
    if(símbolo==0xffc6||símbolo==0xff31||(símbolo==32&&tecla_MAIÚS&&!control_VALOR)){
        원격글쇠확정();한글=!한글;unsigned char Evento[]={30,3,한글,0,0,0,0};원격입력넣기(Evento,7);return;
    }
    if(símbolo==0xff08&&한글&&!control_VALOR&&LOG_CONTAR){조합=LOG_fila[--LOG_CONTAR];글넣기(127);unsigned Texto=조합글();if(Texto)글넣기(Texto);return;}
    if(한글&&!control_VALOR&&símbolo<128&&한글넣기(símbolo))return;
    원격글쇠확정();
    if((control_VALOR&&tecla_MAIÚS&&(símbolo=='t'||símbolo=='T'))||símbolo==0xffc3||símbolo==0xffc9){unsigned char Evento[]={30,2,símbolo==0xffc3?2:símbolo==0xffc9?3:1,0,0,0,0};원격입력넣기(Evento,7);return;}
    const char *특수=símbolo==0xff08?"\177":símbolo==0xff09?"\t":símbolo==0xff0d?"\r":símbolo==0xff1b?"\033":
        símbolo==0xffff?"\033[3~":símbolo==0xff50?"\033[H":símbolo==0xff57?"\033[F":símbolo==0xff51?"\033[D":
        símbolo==0xff52?"\033[A":símbolo==0xff53?"\033[C":símbolo==0xff54?"\033[B":símbolo==0xff55?"\033[5~":símbolo==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALOR=(símbolo&0xff000000)==0x01000000?símbolo&0xffffff:símbolo;
    if(VALOR>0x10ffff||(VALOR>=0xd800&&VALOR<=0xdfff)||(símbolo>=0xff00&&símbolo<0x1000000))return;
    if(control_VALOR){if(VALOR>='a'&&VALOR<='z')VALOR-=96;else if(VALOR>='A'&&VALOR<='Z')VALOR-=64;}
    글넣기(VALOR);
}
