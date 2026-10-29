#include "nuotolinis_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned valdymas_VALUE,윗글쇠,한글;
typedef struct {unsigned 첫,가운데,끝;} struktūra_Būsena;
static struktūra_Būsena struktūra_VALUE,LOG_RECORD[16];
static unsigned LOG_COUNT;
void vykdymas_nuotolinis_Raktas(void){memset(&struktūra_VALUE,0,sizeof(struktūra_VALUE));LOG_COUNT=0;}
void 원격글쇠초기화(void){valdymas_VALUE=윗글쇠=한글=0;vykdymas_nuotolinis_Raktas();}
static void 글넣기(unsigned VALUE){
    unsigned char Tekstas[4];unsigned numeris;
    if(VALUE<128){Tekstas[0]=VALUE;numeris=1;}else if(VALUE<2048){Tekstas[0]=0xc0|(VALUE>>6);Tekstas[1]=0x80|(VALUE&63);numeris=2;}
    else if(VALUE<65536){Tekstas[0]=0xe0|(VALUE>>12);Tekstas[1]=0x80|((VALUE>>6)&63);Tekstas[2]=0x80|(VALUE&63);numeris=3;}
    else{Tekstas[0]=0xf0|(VALUE>>18);Tekstas[1]=0x80|((VALUE>>12)&63);Tekstas[2]=0x80|((VALUE>>6)&63);Tekstas[3]=0x80|(VALUE&63);numeris=4;}
    원격입력넣기(Tekstas,numeris);
}
static int FIND_įrašas(const unsigned *įrašas_Sąrašas,unsigned numeris,unsigned VALUE){for(unsigned 순번=0;순번<numeris;순번++)if(įrašas_Sąrašas[순번]==VALUE)return 순번;return -1;}
static unsigned FIND_dublikatas(const unsigned LOOKUP_lentelė[][3],unsigned numeris,unsigned 가,unsigned SECOND_operandas){for(unsigned 순번=0;순번<numeris;순번++)if(LOOKUP_lentelė[순번][0]==가&&LOOKUP_lentelė[순번][1]==SECOND_operandas)return LOOKUP_lentelė[순번][2];return 0;}
static unsigned 조합글(void){
    if(struktūra_VALUE.첫&&struktūra_VALUE.가운데)return 0xac00+(FIND_įrašas(첫소리목록,19,struktūra_VALUE.첫)*21+FIND_įrašas(가운뎃소리목록,21,struktūra_VALUE.가운데))*28+(struktūra_VALUE.끝?FIND_įrašas(끝소리목록,28,struktūra_VALUE.끝):0);
    return struktūra_VALUE.첫?struktūra_VALUE.첫:struktūra_VALUE.가운데;
}
static int 한글넣기(unsigned Raktas_brūkštelėjimas_stiliumi){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Raktas_schema)/sizeof(Raktas_schema[0]);순번++)if(Raktas_schema[순번][0]==Raktas_brūkštelėjimas_stiliumi)자모=Raktas_schema[순번][1];
    if(!자모&&Raktas_brūkštelėjimas_stiliumi>='A'&&Raktas_brūkštelėjimas_stiliumi<='Z')return 한글넣기(Raktas_brūkštelėjimas_stiliumi+32);if(!자모)return 0;
    unsigned 이전=조합글(),vykdymas_VALUE=0;struktūra_Būsena 전=struktūra_VALUE;
    if(LOG_COUNT<16)LOG_RECORD[LOG_COUNT++]=전;
    if(FIND_įrašas(첫소리목록,19,자모)>=0){
        if(struktūra_VALUE.첫&&struktūra_VALUE.가운데&&!struktūra_VALUE.끝&&FIND_įrašas(끝소리목록,28,자모)>=0)struktūra_VALUE.끝=자모;
        else{unsigned perdanga_VALUE=FIND_dublikatas(겹끝소리,11,struktūra_VALUE.끝,자모);if(struktūra_VALUE.끝&&perdanga_VALUE)struktūra_VALUE.끝=perdanga_VALUE;
            else{vykdymas_VALUE=이전;vykdymas_nuotolinis_Raktas();struktūra_VALUE.첫=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(struktūra_Būsena));}}
    }else if(struktūra_VALUE.끝){
        unsigned 왼쪽=0,RIGHT=struktūra_VALUE.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==struktūra_VALUE.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        struktūra_VALUE.끝=왼쪽;vykdymas_VALUE=조합글();vykdymas_nuotolinis_Raktas();struktūra_VALUE.첫=RIGHT;struktūra_VALUE.가운데=자모;LOG_COUNT=2;
        memset(LOG_RECORD,0,2*sizeof(struktūra_Būsena));LOG_RECORD[1].첫=RIGHT;
    }else if(struktūra_VALUE.가운데){unsigned perdanga_VALUE=FIND_dublikatas(겹가운뎃소리,7,struktūra_VALUE.가운데,자모);
        if(perdanga_VALUE)struktūra_VALUE.가운데=perdanga_VALUE;else{vykdymas_VALUE=이전;vykdymas_nuotolinis_Raktas();struktūra_VALUE.가운데=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(struktūra_Būsena));}
    }else struktūra_VALUE.가운데=자모;
    if(이전)글넣기(127);if(vykdymas_VALUE)글넣기(vykdymas_VALUE);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void nuotolinis_Raktas_brūkštelėjimas_stiliumi(unsigned simbolis,int paspausti_VALUE){
    if(simbolis==0xffe3||simbolis==0xffe4){valdymas_VALUE=paspausti_VALUE;return;}
    if(simbolis==0xffe1||simbolis==0xffe2){윗글쇠=paspausti_VALUE;return;}
    if(!paspausti_VALUE)return;
    if(simbolis==0xffc6||simbolis==0xff31||(simbolis==32&&윗글쇠&&!valdymas_VALUE)){
        vykdymas_nuotolinis_Raktas();한글=!한글;unsigned char Įvykis[]={30,3,한글,0,0,0,0};원격입력넣기(Įvykis,7);return;
    }
    if(simbolis==0xff08&&한글&&!valdymas_VALUE&&LOG_COUNT){struktūra_VALUE=LOG_RECORD[--LOG_COUNT];글넣기(127);unsigned Tekstas=조합글();if(Tekstas)글넣기(Tekstas);return;}
    if(한글&&!valdymas_VALUE&&simbolis<128&&한글넣기(simbolis))return;
    vykdymas_nuotolinis_Raktas();
    if((valdymas_VALUE&&윗글쇠&&(simbolis=='t'||simbolis=='T'))||simbolis==0xffc3||simbolis==0xffc9){unsigned char Įvykis[]={30,2,simbolis==0xffc3?2:simbolis==0xffc9?3:1,0,0,0,0};원격입력넣기(Įvykis,7);return;}
    const char *특수=simbolis==0xff08?"\177":simbolis==0xff09?"\t":simbolis==0xff0d?"\r":simbolis==0xff1b?"\033":
        simbolis==0xffff?"\033[3~":simbolis==0xff50?"\033[H":simbolis==0xff57?"\033[F":simbolis==0xff51?"\033[D":
        simbolis==0xff52?"\033[A":simbolis==0xff53?"\033[C":simbolis==0xff54?"\033[B":simbolis==0xff55?"\033[5~":simbolis==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simbolis&0xff000000)==0x01000000?simbolis&0xffffff:simbolis;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simbolis>=0xff00&&simbolis<0x1000000))return;
    if(valdymas_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
