/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Koppel, 제한된 입력 lengte_VALUE, 비동기 e_pos_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "afstands_VALUE.h"
#include "암호기반.h"
#include "Profiel.h"
#include "../Netwerk_Stapel/Netwerk_Stapel.h"
#include "../masjien/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t bord_Terminaal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,portuur_VALUE=-1,toneel_VALUE,닫을예정;
static uintptr_t verbinding_tyd,다시받을때;
static unsigned char 입력[8192],Afvoer[4096],uitdaging_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pieksel_verstel=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned teël_COUNT,teël_plaas,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_plaas){return(unsigned)data_plaas[0]*256+data_plaas[1];}
static uint32_t 읽기32(const unsigned char *data_plaas){return(uint32_t)data_plaas[0]<<24|(uint32_t)data_plaas[1]<<16|(uint32_t)data_plaas[2]<<8|data_plaas[3];}
static void skryf_16(unsigned char *data_plaas,unsigned VALUE){data_plaas[0]=VALUE>>8;data_plaas[1]=VALUE;}
static void skryf_32(unsigned char *data_plaas,uint32_t VALUE){data_plaas[0]=VALUE>>24;data_plaas[1]=VALUE>>16;data_plaas[2]=VALUE>>8;data_plaas[3]=VALUE;}
static void Sluit(void){if(portuur_VALUE>=0)sluit_Netwerk(portuur_VALUE);portuur_VALUE=-1;toneel_VALUE=0;입력수=출력수=보낸수=0;teël_COUNT=teël_plaas=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned 수){memcpy(Afvoer,data,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int kontrole_afstands_wys(unsigned Aksie){
    if(Aksie==0){Sluit();if(듣는곳>=0)sluit_Netwerk(듣는곳);듣는곳=-1;return 0;}
    if(Aksie!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int ombou_VALUE=통신끝점만들기(1);if(ombou_VALUE<0)return ombou_VALUE;통신주소재사용(ombou_VALUE);
    int maatreël=망주소묶기(ombou_VALUE,0,5900);if(!maatreël)maatreël=연결기다리기(ombou_VALUE);
    if(maatreël<0){sluit_Netwerk(ombou_VALUE);return maatreël;}듣는곳=ombou_VALUE;return 0;
}
static uint32_t 타일요약(unsigned 가로,unsigned Vertikaal_plaas){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_koördinaat=Vertikaal_plaas;Y_koördinaat<Vertikaal_plaas+16&&Y_koördinaat<높이;Y_koördinaat++)for(unsigned x_koördinaat=가로;x_koördinaat<가로+32&&x_koördinaat<너비;x_koördinaat++)VALUE=(VALUE^보드화면읽기(x_koördinaat,Y_koördinaat))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *data_plaas){
    요청가로=읽기16(data_plaas+2);요청세로=읽기16(data_plaas+4);요청폭=읽기16(data_plaas+6);요청높이=읽기16(data_plaas+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    teël_COUNT=teël_plaas=0;
    if(요청폭&&요청높이)for(unsigned Y_koördinaat=요청세로/16;Y_koördinaat<=(요청세로+요청높이-1)/16;Y_koördinaat++)for(unsigned x_koördinaat=요청가로/32;x_koördinaat<=(요청가로+요청폭-1)/32;x_koördinaat++){
        unsigned plaas_INDEX=Y_koördinaat*60+x_koördinaat;uint32_t 요약=타일요약(x_koördinaat*32,Y_koördinaat*16);
        if(!data_plaas[1]||지난요약[plaas_INDEX]!=요약)바뀐타일[teël_COUNT++]=plaas_INDEX;
    }
    Afvoer[0]=Afvoer[1]=0;skryf_16(Afvoer+2,teël_COUNT);출력수=4;보낸수=0;
}
static void e_pos_teël(void){
    unsigned plaas_INDEX=바뀐타일[teël_plaas++],가로=(plaas_INDEX%60)*32,Vertikaal_plaas=(plaas_INDEX/60)*16;
    unsigned beëindig_X=가로+32,beëindig_Y=Vertikaal_plaas+16;if(beëindig_X>너비)beëindig_X=너비;if(beëindig_Y>높이)beëindig_Y=높이;
    /* 부분 타일 요청 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Vertikaal_plaas>=요청세로&&beëindig_X<=요청가로+요청폭&&beëindig_Y<=요청세로+요청높이;
    if(전부)지난요약[plaas_INDEX]=타일요약(가로,Vertikaal_plaas);
    if(가로<요청가로)가로=요청가로;if(Vertikaal_plaas<요청세로)Vertikaal_plaas=요청세로;
    if(beëindig_X>요청가로+요청폭)beëindig_X=요청가로+요청폭;if(beëindig_Y>요청세로+요청높이)beëindig_Y=요청세로+요청높이;
    skryf_16(Afvoer,가로);skryf_16(Afvoer+2,Vertikaal_plaas);skryf_16(Afvoer+4,beëindig_X-가로);skryf_16(Afvoer+6,beëindig_Y-Vertikaal_plaas);skryf_32(Afvoer+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_koördinaat=Vertikaal_plaas;Y_koördinaat<beëindig_Y;Y_koördinaat++)for(unsigned x_koördinaat=가로;x_koördinaat<beëindig_X;x_koördinaat++){
        uint32_t 색=보드화면읽기(x_koördinaat,Y_koördinaat),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pieksel_verstel;순번++)Afvoer[출력수++]=VALUE>>(8*(큰끝?pieksel_verstel-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(portuur_VALUE<0){if(보드밀리초()<다시받을때)return;portuur_VALUE=망연결받기(듣는곳);if(portuur_VALUE<0)return;
        verbinding_tyd=보드밀리초();toneel_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pieksel_verstel=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(toneel_VALUE<5&&보드밀리초()-verbinding_tyd>15000){Sluit();return;}
    if(출력수){int 수=통신쓰기(portuur_VALUE,Afvoer+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Sluit();return;}}
    if(!출력수&&닫을예정){Sluit();return;}
    if(!출력수&&teël_plaas<teël_COUNT)e_pos_teël();
    if(입력수==sizeof(입력)){Sluit();return;}
    int RECEIVED_COUNT=통신읽기(portuur_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Sluit();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||teël_plaas<teël_COUNT)return;
    if(toneel_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Sluit();return;}소비(12);const unsigned char waarmerkmetode[]={1,2};내보내기(waarmerkmetode,2);toneel_VALUE=2;return;}
    if(toneel_VALUE==2&&입력수){if(입력[0]!=2||원격난수(uitdaging_VALUE,16)){Sluit();return;}소비(1);내보내기(uitdaging_VALUE,16);toneel_VALUE=3;return;}
    if(toneel_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys wagwoord_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&wagwoord_VALUE,열쇠,8);memcpy(정답,uitdaging_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&wagwoord_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&wagwoord_VALUE,0,sizeof(wagwoord_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(uitdaging_VALUE,0,16);
        skryf_32(Afvoer,차이?1:0);출력수=4;보낸수=0;
        if(차이){skryf_32(Afvoer+4,19);memcpy(Afvoer+8,"Authentication fail",19);출력수=27;닫을예정=1;}else toneel_VALUE=4;return;}
    if(toneel_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Sluit();return;}
        if(!bord_Terminaal(7)){const unsigned char gebeurtenis[]={30,2,1,0,0,0,0};원격입력넣기(gebeurtenis,7);}
        memset(Afvoer,0,40);skryf_16(Afvoer,너비);skryf_16(Afvoer+2,높이);Afvoer[4]=32;Afvoer[5]=24;Afvoer[7]=1;
        skryf_16(Afvoer+8,255);skryf_16(Afvoer+10,255);skryf_16(Afvoer+12,255);Afvoer[14]=16;Afvoer[15]=8;
        const char *Naam="jkoros native";skryf_32(Afvoer+20,strlen(Naam));memcpy(Afvoer+24,Naam,strlen(Naam));출력수=24+strlen(Naam);보낸수=0;toneel_VALUE=5;return;}
    if(toneel_VALUE!=5||!입력수)return;
    unsigned TYPE_kategorie=입력[0],필요=TYPE_kategorie==0?20:TYPE_kategorie==2?4:TYPE_kategorie==3?10:TYPE_kategorie==4?8:TYPE_kategorie==5?6:TYPE_kategorie==6?8:0;
    if(!필요){Sluit();return;}if(입력수<필요)return;
    if(TYPE_kategorie==2){unsigned 수=읽기16(입력+2);if(수>128){Sluit();return;}필요+=수*4;}
    if(TYPE_kategorie==6){unsigned 수=읽기32(입력+4);if(수>4096){Sluit();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_kategorie==0){unsigned bis_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bis_VALUE!=16&&bis_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bis_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bis_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bis_VALUE)-1)){Sluit();return;}
        pieksel_verstel=bis_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_kategorie==3)화면요청(입력);
    else if(TYPE_kategorie==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_kategorie==5){unsigned x_koördinaat=읽기16(입력+2),Y_koördinaat=읽기16(입력+4);if(x_koördinaat>=너비)x_koördinaat=너비-1;if(Y_koördinaat>=높이)Y_koördinaat=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char gebeurtenis[]={30,1,입력[1],x_koördinaat&255,x_koördinaat>>8,Y_koördinaat&255,Y_koördinaat>>8};원격입력넣기(gebeurtenis,sizeof(gebeurtenis));}
    소비(필요);
}
