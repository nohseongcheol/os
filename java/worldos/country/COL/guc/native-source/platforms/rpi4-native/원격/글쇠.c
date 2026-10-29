#include "원격.h"
#include <string.h>
#include "두벌식표.h"
static unsigned aa_inmajia_ajutuu,ajüttia_MAYÚS,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,aa_innachikimaajatü_aparatsee[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){aa_inmajia_ajutuu=ajüttia_MAYÚS=한글=0;원격글쇠확정();}
static void 글넣기(unsigned ajutuu){
    unsigned char 글[4];unsigned 수;
    if(ajutuu<128){글[0]=ajutuu;수=1;}else if(ajutuu<2048){글[0]=0xc0|(ajutuu>>6);글[1]=0x80|(ajutuu&63);수=2;}
    else if(ajutuu<65536){글[0]=0xe0|(ajutuu>>12);글[1]=0x80|((ajutuu>>6)&63);글[2]=0x80|(ajutuu&63);수=3;}
    else{글[0]=0xf0|(ajutuu>>18);글[1]=0x80|((ajutuu>>12)&63);글[2]=0x80|((ajutuu>>6)&63);글[3]=0x80|(ajutuu&63);수=4;}
    원격입력넣기(글,수);
}
static int 찾기(const unsigned *목록,unsigned 수,unsigned ajutuu){for(unsigned 순번=0;순번<수;순번++)if(목록[순번]==ajutuu)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(찾기(첫소리목록,19,조합.첫)*21+찾기(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?찾기(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(ajüttia_akumajiakuai_pa)/sizeof(ajüttia_akumajiakuai_pa[0]);순번++)if(ajüttia_akumajiakuai_pa[순번][0]==글쇠)자모=ajüttia_akumajiakuai_pa[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)aa_innachikimaajatü_aparatsee[기록수++]=전;
    if(찾기(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&찾기(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned 겹=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&겹)조합.끝=겹;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(aa_innachikimaajatü_aparatsee,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(aa_innachikimaajatü_aparatsee,0,2*sizeof(조합상태));aa_innachikimaajatü_aparatsee[1].첫=오른쪽;
    }else if(조합.가운데){unsigned 겹=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(겹)조합.가운데=겹;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(aa_innachikimaajatü_aparatsee,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned 기호,int 누름){
    if(기호==0xffe3||기호==0xffe4){aa_inmajia_ajutuu=누름;return;}
    if(기호==0xffe1||기호==0xffe2){ajüttia_MAYÚS=누름;return;}
    if(!누름)return;
    if(기호==0xffc6||기호==0xff31||(기호==32&&ajüttia_MAYÚS&&!aa_inmajia_ajutuu)){
        원격글쇠확정();한글=!한글;unsigned char kasachiki[]={30,3,한글,0,0,0,0};원격입력넣기(kasachiki,7);return;
    }
    if(기호==0xff08&&한글&&!aa_inmajia_ajutuu&&기록수){조합=aa_innachikimaajatü_aparatsee[--기록수];글넣기(127);unsigned 글=조합글();if(글)글넣기(글);return;}
    if(한글&&!aa_inmajia_ajutuu&&기호<128&&한글넣기(기호))return;
    원격글쇠확정();
    if((aa_inmajia_ajutuu&&ajüttia_MAYÚS&&(기호=='t'||기호=='T'))||기호==0xffc3||기호==0xffc9){unsigned char kasachiki[]={30,2,기호==0xffc3?2:기호==0xffc9?3:1,0,0,0,0};원격입력넣기(kasachiki,7);return;}
    const char *특수=기호==0xff08?"\177":기호==0xff09?"\t":기호==0xff0d?"\r":기호==0xff1b?"\033":
        기호==0xffff?"\033[3~":기호==0xff50?"\033[H":기호==0xff57?"\033[F":기호==0xff51?"\033[D":
        기호==0xff52?"\033[A":기호==0xff53?"\033[C":기호==0xff54?"\033[B":기호==0xff55?"\033[5~":기호==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned ajutuu=(기호&0xff000000)==0x01000000?기호&0xffffff:기호;
    if(ajutuu>0x10ffff||(ajutuu>=0xd800&&ajutuu<=0xdfff)||(기호>=0xff00&&기호<0x1000000))return;
    if(aa_inmajia_ajutuu){if(ajutuu>='a'&&ajutuu<='z')ajutuu-=96;else if(ajutuu>='A'&&ajutuu<='Z')ajutuu-=64;}
    글넣기(ajutuu);
}
