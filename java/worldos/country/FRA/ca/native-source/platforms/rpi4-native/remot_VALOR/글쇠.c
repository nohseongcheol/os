#include "remot_VALOR.h"
#include <string.h>
#include "두벌식표.h"
static unsigned control_VALOR,tecla_Maj,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_fila[16];
static unsigned LOG_COMPT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COMPT=0;}
void 원격글쇠초기화(void){control_VALOR=tecla_Maj=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALOR){
    unsigned char SMS[4];unsigned 수;
    if(VALOR<128){SMS[0]=VALOR;수=1;}else if(VALOR<2048){SMS[0]=0xc0|(VALOR>>6);SMS[1]=0x80|(VALOR&63);수=2;}
    else if(VALOR<65536){SMS[0]=0xe0|(VALOR>>12);SMS[1]=0x80|((VALOR>>6)&63);SMS[2]=0x80|(VALOR&63);수=3;}
    else{SMS[0]=0xf0|(VALOR>>18);SMS[1]=0x80|((VALOR>>12)&63);SMS[2]=0x80|((VALOR>>6)&63);SMS[3]=0x80|(VALOR&63);수=4;}
    원격입력넣기(SMS,수);
}
static int BUSCA_introducció(const unsigned *introducció_Llista,unsigned 수,unsigned VALOR){for(unsigned 순번=0;순번<수;순번++)if(introducció_Llista[순번]==VALOR)return 순번;return -1;}
static unsigned BUSCA_dupl(const unsigned Cerca_taula[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(Cerca_taula[순번][0]==가&&Cerca_taula[순번][1]==나)return Cerca_taula[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(BUSCA_introducció(첫소리목록,19,조합.첫)*21+BUSCA_introducció(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?BUSCA_introducció(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Clau_disseny)/sizeof(Clau_disseny[0]);순번++)if(Clau_disseny[순번][0]==글쇠)자모=Clau_disseny[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COMPT<16)LOG_fila[LOG_COMPT++]=전;
    if(BUSCA_introducció(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&BUSCA_introducció(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned superposició_VALOR=BUSCA_dupl(겹끝소리,11,조합.끝,자모);if(조합.끝&&superposició_VALOR)조합.끝=superposició_VALOR;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COMPT=1;memset(LOG_fila,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,DRETA=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];DRETA=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=DRETA;조합.가운데=자모;LOG_COMPT=2;
        memset(LOG_fila,0,2*sizeof(조합상태));LOG_fila[1].첫=DRETA;
    }else if(조합.가운데){unsigned superposició_VALOR=BUSCA_dupl(겹가운뎃소리,7,조합.가운데,자모);
        if(superposició_VALOR)조합.가운데=superposició_VALOR;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COMPT=1;memset(LOG_fila,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned ARA_VALOR=조합글();if(ARA_VALOR)글넣기(ARA_VALOR);return 1;
}
void 원격글쇠(unsigned símbol,int prémer_VALOR){
    if(símbol==0xffe3||símbol==0xffe4){control_VALOR=prémer_VALOR;return;}
    if(símbol==0xffe1||símbol==0xffe2){tecla_Maj=prémer_VALOR;return;}
    if(!prémer_VALOR)return;
    if(símbol==0xffc6||símbol==0xff31||(símbol==32&&tecla_Maj&&!control_VALOR)){
        원격글쇠확정();한글=!한글;unsigned char Esdeveniment[]={30,3,한글,0,0,0,0};원격입력넣기(Esdeveniment,7);return;
    }
    if(símbol==0xff08&&한글&&!control_VALOR&&LOG_COMPT){조합=LOG_fila[--LOG_COMPT];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!control_VALOR&&símbol<128&&한글넣기(símbol))return;
    원격글쇠확정();
    if((control_VALOR&&tecla_Maj&&(símbol=='t'||símbol=='T'))||símbol==0xffc3||símbol==0xffc9){unsigned char Esdeveniment[]={30,2,símbol==0xffc3?2:símbol==0xffc9?3:1,0,0,0,0};원격입력넣기(Esdeveniment,7);return;}
    const char *특수=símbol==0xff08?"\177":símbol==0xff09?"\t":símbol==0xff0d?"\r":símbol==0xff1b?"\033":
        símbol==0xffff?"\033[3~":símbol==0xff50?"\033[H":símbol==0xff57?"\033[F":símbol==0xff51?"\033[D":
        símbol==0xff52?"\033[A":símbol==0xff53?"\033[C":símbol==0xff54?"\033[B":símbol==0xff55?"\033[5~":símbol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALOR=(símbol&0xff000000)==0x01000000?símbol&0xffffff:símbol;
    if(VALOR>0x10ffff||(VALOR>=0xd800&&VALOR<=0xdfff)||(símbol>=0xff00&&símbol<0x1000000))return;
    if(control_VALOR){if(VALOR>='a'&&VALOR<='z')VALOR-=96;else if(VALOR>='A'&&VALOR<='Z')VALOR-=64;}
    글넣기(VALOR);
}
