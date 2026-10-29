/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Nasc, 제한된 입력 fad_VALUE, 비동기 seol_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 sonraí 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "cianda_VALUE.h"
#include "암호기반.h"
#include "Próifíl.h"
#include "../Líonra_Cruach/Líonra_Cruach.h"
#include "../meaisín/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t clár_Teirminéal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,piara_VALUE=-1,céim_VALUE,닫을예정;
static uintptr_t nasc_TIME,다시받을때;
static unsigned char 입력[8192],Aschur[4096],dúshlán_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,picteilín_socraigh_méid=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned tíl_COUNT,tíl_suíomh,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *sonraí_suíomh){return(unsigned)sonraí_suíomh[0]*256+sonraí_suíomh[1];}
static uint32_t 읽기32(const unsigned char *sonraí_suíomh){return(uint32_t)sonraí_suíomh[0]<<24|(uint32_t)sonraí_suíomh[1]<<16|(uint32_t)sonraí_suíomh[2]<<8|sonraí_suíomh[3];}
static void scríobh_16(unsigned char *sonraí_suíomh,unsigned VALUE){sonraí_suíomh[0]=VALUE>>8;sonraí_suíomh[1]=VALUE;}
static void scríobh_32(unsigned char *sonraí_suíomh,uint32_t VALUE){sonraí_suíomh[0]=VALUE>>24;sonraí_suíomh[1]=VALUE>>16;sonraí_suíomh[2]=VALUE>>8;sonraí_suíomh[3]=VALUE;}
static void Dún(void){if(piara_VALUE>=0)dún_Líonra(piara_VALUE);piara_VALUE=-1;céim_VALUE=0;입력수=출력수=보낸수=0;tíl_COUNT=tíl_suíomh=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *sonraí,unsigned 수){memcpy(Aschur,sonraí,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int rialú_cianda_taispeáin(unsigned Gníomh){
    if(Gníomh==0){Dún();if(듣는곳>=0)dún_Líonra(듣는곳);듣는곳=-1;return 0;}
    if(Gníomh!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int tomhas=망주소묶기(port_VALUE,0,5900);if(!tomhas)tomhas=연결기다리기(port_VALUE);
    if(tomhas<0){dún_Líonra(port_VALUE);return tomhas;}듣는곳=port_VALUE;return 0;
}
static uint32_t tíl_achoimre(unsigned 가로,unsigned Ingearach_suíomh){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=Ingearach_suíomh;세로좌표<Ingearach_suíomh+16&&세로좌표<높이;세로좌표++)for(unsigned x_chomhordanáid=가로;x_chomhordanáid<가로+32&&x_chomhordanáid<너비;x_chomhordanáid++)VALUE=(VALUE^보드화면읽기(x_chomhordanáid,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *sonraí_suíomh){
    요청가로=읽기16(sonraí_suíomh+2);요청세로=읽기16(sonraí_suíomh+4);요청폭=읽기16(sonraí_suíomh+6);요청높이=읽기16(sonraí_suíomh+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    tíl_COUNT=tíl_suíomh=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned x_chomhordanáid=요청가로/32;x_chomhordanáid<=(요청가로+요청폭-1)/32;x_chomhordanáid++){
        unsigned suíomh_INDEX=세로좌표*60+x_chomhordanáid;uint32_t achoimre_VALUE=tíl_achoimre(x_chomhordanáid*32,세로좌표*16);
        if(!sonraí_suíomh[1]||지난요약[suíomh_INDEX]!=achoimre_VALUE)바뀐타일[tíl_COUNT++]=suíomh_INDEX;
    }
    Aschur[0]=Aschur[1]=0;scríobh_16(Aschur+2,tíl_COUNT);출력수=4;보낸수=0;
}
static void seol_tíl(void){
    unsigned suíomh_INDEX=바뀐타일[tíl_suíomh++],가로=(suíomh_INDEX%60)*32,Ingearach_suíomh=(suíomh_INDEX/60)*16;
    unsigned 끝가로=가로+32,끝세로=Ingearach_suíomh+16;if(끝가로>너비)끝가로=너비;if(끝세로>높이)끝세로=높이;
    /* 부분 타일 iarratas_HTTP 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Ingearach_suíomh>=요청세로&&끝가로<=요청가로+요청폭&&끝세로<=요청세로+요청높이;
    if(전부)지난요약[suíomh_INDEX]=tíl_achoimre(가로,Ingearach_suíomh);
    if(가로<요청가로)가로=요청가로;if(Ingearach_suíomh<요청세로)Ingearach_suíomh=요청세로;
    if(끝가로>요청가로+요청폭)끝가로=요청가로+요청폭;if(끝세로>요청세로+요청높이)끝세로=요청세로+요청높이;
    scríobh_16(Aschur,가로);scríobh_16(Aschur+2,Ingearach_suíomh);scríobh_16(Aschur+4,끝가로-가로);scríobh_16(Aschur+6,끝세로-Ingearach_suíomh);scríobh_32(Aschur+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=Ingearach_suíomh;세로좌표<끝세로;세로좌표++)for(unsigned x_chomhordanáid=가로;x_chomhordanáid<끝가로;x_chomhordanáid++){
        uint32_t 색=보드화면읽기(x_chomhordanáid,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<picteilín_socraigh_méid;순번++)Aschur[출력수++]=VALUE>>(8*(큰끝?picteilín_socraigh_méid-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(piara_VALUE<0){if(보드밀리초()<다시받을때)return;piara_VALUE=망연결받기(듣는곳);if(piara_VALUE<0)return;
        nasc_TIME=보드밀리초();céim_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        picteilín_socraigh_méid=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(céim_VALUE<5&&보드밀리초()-nasc_TIME>15000){Dún();return;}
    if(출력수){int 수=통신쓰기(piara_VALUE,Aschur+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Dún();return;}}
    if(!출력수&&닫을예정){Dún();return;}
    if(!출력수&&tíl_suíomh<tíl_COUNT)seol_tíl();
    if(입력수==sizeof(입력)){Dún();return;}
    int RECEIVED_COUNT=통신읽기(piara_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Dún();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||tíl_suíomh<tíl_COUNT)return;
    if(céim_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Dún();return;}소비(12);const unsigned char modh_fíordheimhnithe[]={1,2};내보내기(modh_fíordheimhnithe,2);céim_VALUE=2;return;}
    if(céim_VALUE==2&&입력수){if(입력[0]!=2||원격난수(dúshlán_VALUE,16)){Dún();return;}소비(1);내보내기(dúshlán_VALUE,16);céim_VALUE=3;return;}
    if(céim_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys pasfhocal_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&pasfhocal_VALUE,열쇠,8);memcpy(정답,dúshlán_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char veicteoir_VALUE[8]={0};br_des_ct_cbcenc_run(&pasfhocal_VALUE,veicteoir_VALUE,정답+순번,8);memset(veicteoir_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&pasfhocal_VALUE,0,sizeof(pasfhocal_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(dúshlán_VALUE,0,16);
        scríobh_32(Aschur,차이?1:0);출력수=4;보낸수=0;
        if(차이){scríobh_32(Aschur+4,19);memcpy(Aschur+8,"Authentication fail",19);출력수=27;닫을예정=1;}else céim_VALUE=4;return;}
    if(céim_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Dún();return;}
        if(!clár_Teirminéal(7)){const unsigned char ócáid[]={30,2,1,0,0,0,0};원격입력넣기(ócáid,7);}
        memset(Aschur,0,40);scríobh_16(Aschur,너비);scríobh_16(Aschur+2,높이);Aschur[4]=32;Aschur[5]=24;Aschur[7]=1;
        scríobh_16(Aschur+8,255);scríobh_16(Aschur+10,255);scríobh_16(Aschur+12,255);Aschur[14]=16;Aschur[15]=8;
        const char *Ainm="jkoros native";scríobh_32(Aschur+20,strlen(Ainm));memcpy(Aschur+24,Ainm,strlen(Ainm));출력수=24+strlen(Ainm);보낸수=0;céim_VALUE=5;return;}
    if(céim_VALUE!=5||!입력수)return;
    unsigned TYPE_catagóir=입력[0],필요=TYPE_catagóir==0?20:TYPE_catagóir==2?4:TYPE_catagóir==3?10:TYPE_catagóir==4?8:TYPE_catagóir==5?6:TYPE_catagóir==6?8:0;
    if(!필요){Dún();return;}if(입력수<필요)return;
    if(TYPE_catagóir==2){unsigned 수=읽기16(입력+2);if(수>128){Dún();return;}필요+=수*4;}
    if(TYPE_catagóir==6){unsigned 수=읽기32(입력+4);if(수>4096){Dún();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_catagóir==0){unsigned giotán_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((giotán_VALUE!=16&&giotán_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<giotán_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<giotán_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<giotán_VALUE)-1)){Dún();return;}
        picteilín_socraigh_méid=giotán_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_catagóir==3)화면요청(입력);
    else if(TYPE_catagóir==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_catagóir==5){unsigned x_chomhordanáid=읽기16(입력+2),세로좌표=읽기16(입력+4);if(x_chomhordanáid>=너비)x_chomhordanáid=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char ócáid[]={30,1,입력[1],x_chomhordanáid&255,x_chomhordanáid>>8,세로좌표&255,세로좌표>>8};원격입력넣기(ócáid,sizeof(ócáid));}
    소비(필요);
}
