#include "kgakala_Boleng.h"
#include <string.h>
#include "두벌식표.h"
static unsigned taolo_Boleng,taetsi_ya_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,rekota_mola[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){taolo_Boleng=taetsi_ya_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned Boleng){
    unsigned char SMS[4];unsigned 수;
    if(Boleng<128){SMS[0]=Boleng;수=1;}else if(Boleng<2048){SMS[0]=0xc0|(Boleng>>6);SMS[1]=0x80|(Boleng&63);수=2;}
    else if(Boleng<65536){SMS[0]=0xe0|(Boleng>>12);SMS[1]=0x80|((Boleng>>6)&63);SMS[2]=0x80|(Boleng&63);수=3;}
    else{SMS[0]=0xf0|(Boleng>>18);SMS[1]=0x80|((Boleng>>12)&63);SMS[2]=0x80|((Boleng>>6)&63);SMS[3]=0x80|(Boleng&63);수=4;}
    원격입력넣기(SMS,수);
}
static int batla_tsenyo(const unsigned *tsenyo_lenaane,unsigned 수,unsigned Boleng){for(unsigned 순번=0;순번<수;순번++)if(tsenyo_lenaane[순번]==Boleng)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(batla_tsenyo(첫소리목록,19,조합.첫)*21+batla_tsenyo(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?batla_tsenyo(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(taetsi_Boalo)/sizeof(taetsi_Boalo[0]);순번++)if(taetsi_Boalo[순번][0]==글쇠)자모=taetsi_Boalo[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)rekota_mola[기록수++]=전;
    if(batla_tsenyo(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&batla_tsenyo(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned tsenyoditshwantsho_Boleng=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&tsenyoditshwantsho_Boleng)조합.끝=tsenyoditshwantsho_Boleng;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(rekota_mola,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(rekota_mola,0,2*sizeof(조합상태));rekota_mola[1].첫=오른쪽;
    }else if(조합.가운데){unsigned tsenyoditshwantsho_Boleng=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(tsenyoditshwantsho_Boleng)조합.가운데=tsenyoditshwantsho_Boleng;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(rekota_mola,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned letshwao,int 누름){
    if(letshwao==0xffe3||letshwao==0xffe4){taolo_Boleng=누름;return;}
    if(letshwao==0xffe1||letshwao==0xffe2){taetsi_ya_SHIFT=누름;return;}
    if(!누름)return;
    if(letshwao==0xffc6||letshwao==0xff31||(letshwao==32&&taetsi_ya_SHIFT&&!taolo_Boleng)){
        원격글쇠확정();한글=!한글;unsigned char tiragalo[]={30,3,한글,0,0,0,0};원격입력넣기(tiragalo,7);return;
    }
    if(letshwao==0xff08&&한글&&!taolo_Boleng&&기록수){조합=rekota_mola[--기록수];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!taolo_Boleng&&letshwao<128&&한글넣기(letshwao))return;
    원격글쇠확정();
    if((taolo_Boleng&&taetsi_ya_SHIFT&&(letshwao=='t'||letshwao=='T'))||letshwao==0xffc3||letshwao==0xffc9){unsigned char tiragalo[]={30,2,letshwao==0xffc3?2:letshwao==0xffc9?3:1,0,0,0,0};원격입력넣기(tiragalo,7);return;}
    const char *특수=letshwao==0xff08?"\177":letshwao==0xff09?"\t":letshwao==0xff0d?"\r":letshwao==0xff1b?"\033":
        letshwao==0xffff?"\033[3~":letshwao==0xff50?"\033[H":letshwao==0xff57?"\033[F":letshwao==0xff51?"\033[D":
        letshwao==0xff52?"\033[A":letshwao==0xff53?"\033[C":letshwao==0xff54?"\033[B":letshwao==0xff55?"\033[5~":letshwao==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned Boleng=(letshwao&0xff000000)==0x01000000?letshwao&0xffffff:letshwao;
    if(Boleng>0x10ffff||(Boleng>=0xd800&&Boleng<=0xdfff)||(letshwao>=0xff00&&letshwao<0x1000000))return;
    if(taolo_Boleng){if(Boleng>='a'&&Boleng<='z')Boleng-=96;else if(Boleng>='A'&&Boleng<='Z')Boleng-=64;}
    글넣기(Boleng);
}
