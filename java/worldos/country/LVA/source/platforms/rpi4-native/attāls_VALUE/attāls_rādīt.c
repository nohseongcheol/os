/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Savienoties, 제한된 입력 길이, 비동기 sūtīt_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 dati 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "attāls_VALUE.h"
#include "kriptogrāfija_Atbalsts.h"
#include "Profils.h"
#include "../tīkls_kopa/tīkls_kopa.h"
#include "../mašīna/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Panelis_Terminālis(uintptr_t);
void attāls_Atslēga_ciparrokraksta_vilkums(unsigned,int);
void 원격글쇠초기화(void);
void izpilde_attāls_Atslēga(void);
static int Klausīšanās_dalībnieks=-1,vienranga_VALUE=-1,posms_VALUE,닫을예정;
static uintptr_t paziņa_TIME,다시받을때;
static unsigned char 입력[8192],Izvade[4096],izaicinājums_VALUE[16];
static unsigned 입력수,ražojums_COUNT,보낸수;
static unsigned 너비,높이,attēla_elements_mainīt_izmērus=4,resngala_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned elements_COUNT,elements_amats,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *dati_amats){return(unsigned)dati_amats[0]*256+dati_amats[1];}
static uint32_t 읽기32(const unsigned char *dati_amats){return(uint32_t)dati_amats[0]<<24|(uint32_t)dati_amats[1]<<16|(uint32_t)dati_amats[2]<<8|dati_amats[3];}
static void rakstīšana_16(unsigned char *dati_amats,unsigned VALUE){dati_amats[0]=VALUE>>8;dati_amats[1]=VALUE;}
static void rakstīšana_32(unsigned char *dati_amats,uint32_t VALUE){dati_amats[0]=VALUE>>24;dati_amats[1]=VALUE>>16;dati_amats[2]=VALUE>>8;dati_amats[3]=VALUE;}
static void Aizvērt(void){if(vienranga_VALUE>=0)Aizvērt_tīkls(vienranga_VALUE);vienranga_VALUE=-1;posms_VALUE=0;입력수=ražojums_COUNT=보낸수=0;elements_COUNT=elements_amats=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *dati,unsigned numurs){memcpy(Izvade,dati,numurs);ražojums_COUNT=numurs;보낸수=0;}
static void patērēt_VALUE(unsigned numurs){입력수-=numurs;memmove(입력,입력+numurs,입력수);}
int vadība_attāls_rādīt(unsigned Darbība){
    if(Darbība==0){Aizvērt();if(Klausīšanās_dalībnieks>=0)Aizvērt_tīkls(Klausīšanās_dalībnieks);Klausīšanās_dalībnieks=-1;return 0;}
    if(Darbība!=1)return Klausīšanās_dalībnieks>=0;
    if(Klausīšanās_dalībnieks>=0)return 0;
    int ports_VALUE=통신끝점만들기(1);if(ports_VALUE<0)return ports_VALUE;통신주소재사용(ports_VALUE);
    int mērs=NET_BIND(ports_VALUE,0,5900);if(!mērs)mērs=NET_klausīties(ports_VALUE);
    if(mērs<0){Aizvērt_tīkls(ports_VALUE);return mērs;}Klausīšanās_dalībnieks=ports_VALUE;return 0;
}
static uint32_t elements_kopsavilkums(unsigned 가로,unsigned vertikāle_amats){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=vertikāle_amats;세로좌표<vertikāle_amats+16&&세로좌표<높이;세로좌표++)for(unsigned x_koordināta=가로;x_koordināta<가로+32&&x_koordināta<너비;x_koordināta++)VALUE=(VALUE^보드화면읽기(x_koordināta,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *dati_amats){
    요청가로=읽기16(dati_amats+2);요청세로=읽기16(dati_amats+4);요청폭=읽기16(dati_amats+6);요청높이=읽기16(dati_amats+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    elements_COUNT=elements_amats=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned x_koordināta=요청가로/32;x_koordināta<=(요청가로+요청폭-1)/32;x_koordināta++){
        unsigned pozīcijas_indekss=세로좌표*60+x_koordināta;uint32_t kopsavilkums_VALUE=elements_kopsavilkums(x_koordināta*32,세로좌표*16);
        if(!dati_amats[1]||지난요약[pozīcijas_indekss]!=kopsavilkums_VALUE)바뀐타일[elements_COUNT++]=pozīcijas_indekss;
    }
    Izvade[0]=Izvade[1]=0;rakstīšana_16(Izvade+2,elements_COUNT);ražojums_COUNT=4;보낸수=0;
}
static void sūtīt_elements(void){
    unsigned pozīcijas_indekss=바뀐타일[elements_amats++],가로=(pozīcijas_indekss%60)*32,vertikāle_amats=(pozīcijas_indekss/60)*16;
    unsigned beigt_zvanu_X=가로+32,beigt_zvanu_Y=vertikāle_amats+16;if(beigt_zvanu_X>너비)beigt_zvanu_X=너비;if(beigt_zvanu_Y>높이)beigt_zvanu_Y=높이;
    /* 부분 타일 pieprasījums 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&vertikāle_amats>=요청세로&&beigt_zvanu_X<=요청가로+요청폭&&beigt_zvanu_Y<=요청세로+요청높이;
    if(전부)지난요약[pozīcijas_indekss]=elements_kopsavilkums(가로,vertikāle_amats);
    if(가로<요청가로)가로=요청가로;if(vertikāle_amats<요청세로)vertikāle_amats=요청세로;
    if(beigt_zvanu_X>요청가로+요청폭)beigt_zvanu_X=요청가로+요청폭;if(beigt_zvanu_Y>요청세로+요청높이)beigt_zvanu_Y=요청세로+요청높이;
    rakstīšana_16(Izvade,가로);rakstīšana_16(Izvade+2,vertikāle_amats);rakstīšana_16(Izvade+4,beigt_zvanu_X-가로);rakstīšana_16(Izvade+6,beigt_zvanu_Y-vertikāle_amats);rakstīšana_32(Izvade+8,0);
    ražojums_COUNT=12;보낸수=0;
    for(unsigned 세로좌표=vertikāle_amats;세로좌표<beigt_zvanu_Y;세로좌표++)for(unsigned x_koordināta=가로;x_koordināta<beigt_zvanu_X;x_koordināta++){
        uint32_t 색=보드화면읽기(x_koordināta,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<attēla_elements_mainīt_izmērus;순번++)Izvade[ražojums_COUNT++]=VALUE>>(8*(resngala_VALUE?attēla_elements_mainīt_izmērus-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Klausīšanās_dalībnieks<0)return;
    if(vienranga_VALUE<0){if(보드밀리초()<다시받을때)return;vienranga_VALUE=NET_akceptēt(Klausīšanās_dalībnieks);if(vienranga_VALUE<0)return;
        paziņa_TIME=보드밀리초();posms_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        attēla_elements_mainīt_izmērus=4;resngala_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(posms_VALUE<5&&보드밀리초()-paziņa_TIME>15000){Aizvērt();return;}
    if(ražojums_COUNT){int numurs=NET_rakstīšana(vienranga_VALUE,Izvade+보낸수,ražojums_COUNT-보낸수);if(numurs>0){보낸수+=numurs;if(보낸수==ražojums_COUNT)ražojums_COUNT=보낸수=0;}else if(numurs!=-11){Aizvērt();return;}}
    if(!ražojums_COUNT&&닫을예정){Aizvērt();return;}
    if(!ražojums_COUNT&&elements_amats<elements_COUNT)sūtīt_elements();
    if(입력수==sizeof(입력)){Aizvērt();return;}
    int RECEIVED_COUNT=통신읽기(vienranga_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Aizvērt();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(ražojums_COUNT||elements_amats<elements_COUNT)return;
    if(posms_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Aizvērt();return;}patērēt_VALUE(12);const unsigned char autentifikācijas_metode[]={1,2};내보내기(autentifikācijas_metode,2);posms_VALUE=2;return;}
    if(posms_VALUE==2&&입력수){if(입력[0]!=2||attāls_nejaušs(izaicinājums_VALUE,16)){Aizvērt();return;}patērēt_VALUE(1);내보내기(izaicinājums_VALUE,16);posms_VALUE=3;return;}
    if(posms_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys parole_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&parole_VALUE,열쇠,8);memcpy(정답,izaicinājums_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektors_VALUE[8]={0};br_des_ct_cbcenc_run(&parole_VALUE,vektors_VALUE,정답+순번,8);memset(vektors_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];patērēt_VALUE(16);memset(&parole_VALUE,0,sizeof(parole_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(izaicinājums_VALUE,0,16);
        rakstīšana_32(Izvade,차이?1:0);ražojums_COUNT=4;보낸수=0;
        if(차이){rakstīšana_32(Izvade+4,19);memcpy(Izvade+8,"Authentication fail",19);ražojums_COUNT=27;닫을예정=1;}else posms_VALUE=4;return;}
    if(posms_VALUE==4&&입력수){patērēt_VALUE(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Aizvērt();return;}
        if(!Panelis_Terminālis(7)){const unsigned char Notikums[]={30,2,1,0,0,0,0};원격입력넣기(Notikums,7);}
        memset(Izvade,0,40);rakstīšana_16(Izvade,너비);rakstīšana_16(Izvade+2,높이);Izvade[4]=32;Izvade[5]=24;Izvade[7]=1;
        rakstīšana_16(Izvade+8,255);rakstīšana_16(Izvade+10,255);rakstīšana_16(Izvade+12,255);Izvade[14]=16;Izvade[15]=8;
        const char *Nosaukums="jkoros native";rakstīšana_32(Izvade+20,strlen(Nosaukums));memcpy(Izvade+24,Nosaukums,strlen(Nosaukums));ražojums_COUNT=24+strlen(Nosaukums);보낸수=0;posms_VALUE=5;return;}
    if(posms_VALUE!=5||!입력수)return;
    unsigned TYPE_joma=입력[0],필요=TYPE_joma==0?20:TYPE_joma==2?4:TYPE_joma==3?10:TYPE_joma==4?8:TYPE_joma==5?6:TYPE_joma==6?8:0;
    if(!필요){Aizvērt();return;}if(입력수<필요)return;
    if(TYPE_joma==2){unsigned numurs=읽기16(입력+2);if(numurs>128){Aizvērt();return;}필요+=numurs*4;}
    if(TYPE_joma==6){unsigned numurs=읽기32(입력+4);if(numurs>4096){Aizvērt();return;}필요+=numurs;}
    if(입력수<필요)return;
    if(TYPE_joma==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Aizvērt();return;}
        attēla_elements_mainīt_izmērus=bit_VALUE/8;resngala_VALUE=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_joma==3)화면요청(입력);
    else if(TYPE_joma==4)attāls_Atslēga_ciparrokraksta_vilkums(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_joma==5){unsigned x_koordināta=읽기16(입력+2),세로좌표=읽기16(입력+4);if(x_koordināta>=너비)x_koordināta=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])izpilde_attāls_Atslēga();
        unsigned char Notikums[]={30,1,입력[1],x_koordināta&255,x_koordināta>>8,세로좌표&255,세로좌표>>8};원격입력넣기(Notikums,sizeof(Notikums));}
    patērēt_VALUE(필요);
}
