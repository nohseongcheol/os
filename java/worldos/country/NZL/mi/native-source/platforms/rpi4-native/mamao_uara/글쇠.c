#include "mamao_uara.h"
#include <string.h>
#include "두벌식표.h"
static unsigned mana_uara,pātuhi_NEKE,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_RECORD[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){mana_uara=pātuhi_NEKE=한글=0;원격글쇠확정();}
static void 글넣기(unsigned uara){
    unsigned char Ngā_kupu[4];unsigned 수;
    if(uara<128){Ngā_kupu[0]=uara;수=1;}else if(uara<2048){Ngā_kupu[0]=0xc0|(uara>>6);Ngā_kupu[1]=0x80|(uara&63);수=2;}
    else if(uara<65536){Ngā_kupu[0]=0xe0|(uara>>12);Ngā_kupu[1]=0x80|((uara>>6)&63);Ngā_kupu[2]=0x80|(uara&63);수=3;}
    else{Ngā_kupu[0]=0xf0|(uara>>18);Ngā_kupu[1]=0x80|((uara>>12)&63);Ngā_kupu[2]=0x80|((uara>>6)&63);Ngā_kupu[3]=0x80|(uara&63);수=4;}
    원격입력넣기(Ngā_kupu,수);
}
static int FIND_tāurunga(const unsigned *tāurunga_Rārangi,unsigned 수,unsigned uara){for(unsigned 순번=0;순번<수;순번++)if(tāurunga_Rārangi[순번]==uara)return 순번;return -1;}
static unsigned 겹찾기(const unsigned Rapu_ripanga[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(Rapu_ripanga[순번][0]==가&&Rapu_ripanga[순번][1]==나)return Rapu_ripanga[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_tāurunga(첫소리목록,19,조합.첫)*21+FIND_tāurunga(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_tāurunga(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(kī_Tahora)/sizeof(kī_Tahora[0]);순번++)if(kī_Tahora[순번][0]==글쇠)자모=kī_Tahora[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_RECORD[LOG_COUNT++]=전;
    if(FIND_tāurunga(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_tāurunga(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned paparua_uara=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&paparua_uara)조합.끝=paparua_uara;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_RECORD,0,2*sizeof(조합상태));LOG_RECORD[1].첫=RIGHT;
    }else if(조합.가운데){unsigned paparua_uara=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(paparua_uara)조합.가운데=paparua_uara;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_uara=조합글();if(NOW_uara)글넣기(NOW_uara);return 1;
}
void 원격글쇠(unsigned tohu,int 누름){
    if(tohu==0xffe3||tohu==0xffe4){mana_uara=누름;return;}
    if(tohu==0xffe1||tohu==0xffe2){pātuhi_NEKE=누름;return;}
    if(!누름)return;
    if(tohu==0xffc6||tohu==0xff31||(tohu==32&&pātuhi_NEKE&&!mana_uara)){
        원격글쇠확정();한글=!한글;unsigned char hui[]={30,3,한글,0,0,0,0};원격입력넣기(hui,7);return;
    }
    if(tohu==0xff08&&한글&&!mana_uara&&LOG_COUNT){조합=LOG_RECORD[--LOG_COUNT];글넣기(127);unsigned Ngā_kupu=조합글();if(Ngā_kupu)글넣기(Ngā_kupu);return;}
    if(한글&&!mana_uara&&tohu<128&&한글넣기(tohu))return;
    원격글쇠확정();
    if((mana_uara&&pātuhi_NEKE&&(tohu=='t'||tohu=='T'))||tohu==0xffc3||tohu==0xffc9){unsigned char hui[]={30,2,tohu==0xffc3?2:tohu==0xffc9?3:1,0,0,0,0};원격입력넣기(hui,7);return;}
    const char *특수=tohu==0xff08?"\177":tohu==0xff09?"\t":tohu==0xff0d?"\r":tohu==0xff1b?"\033":
        tohu==0xffff?"\033[3~":tohu==0xff50?"\033[H":tohu==0xff57?"\033[F":tohu==0xff51?"\033[D":
        tohu==0xff52?"\033[A":tohu==0xff53?"\033[C":tohu==0xff54?"\033[B":tohu==0xff55?"\033[5~":tohu==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned uara=(tohu&0xff000000)==0x01000000?tohu&0xffffff:tohu;
    if(uara>0x10ffff||(uara>=0xd800&&uara<=0xdfff)||(tohu>=0xff00&&tohu<0x1000000))return;
    if(mana_uara){if(uara>='a'&&uara<='z')uara-=96;else if(uara>='A'&&uara<='Z')uara-=64;}
    글넣기(uara);
}
