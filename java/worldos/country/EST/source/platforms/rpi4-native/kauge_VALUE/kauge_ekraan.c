/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Ühendu, 제한된 입력 길이, 비동기 saatma_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 andmed 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "kauge_VALUE.h"
#include "krüptograafia_tugi.h"
#include "Profiil.h"
#include "../võrk_Virn/võrk_Virn.h"
#include "../arvuti/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tahvel_terminal(uintptr_t);
void kauge_Võti_tinditõmme(unsigned,int);
void 원격글쇠초기화(void);
void kinnitamine_kauge_Võti(void);
static int Kuulamine_osaleja=-1,partner_VALUE=-1,etapp_VALUE,닫을예정;
static uintptr_t ühendus_Aeg,다시받을때;
static unsigned char 입력[8192],Väljund[4096],küsimus_VALUE[16];
static unsigned 입력수,toodang_COUNT,보낸수;
static unsigned 너비,높이,piksel_suurust_muutma=4,tavabaidijärjestusega_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned paan_COUNT,paan_ametikoht,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *andmed_ametikoht){return(unsigned)andmed_ametikoht[0]*256+andmed_ametikoht[1];}
static uint32_t 읽기32(const unsigned char *andmed_ametikoht){return(uint32_t)andmed_ametikoht[0]<<24|(uint32_t)andmed_ametikoht[1]<<16|(uint32_t)andmed_ametikoht[2]<<8|andmed_ametikoht[3];}
static void kirjutamine_16(unsigned char *andmed_ametikoht,unsigned VALUE){andmed_ametikoht[0]=VALUE>>8;andmed_ametikoht[1]=VALUE;}
static void kirjutamine_32(unsigned char *andmed_ametikoht,uint32_t VALUE){andmed_ametikoht[0]=VALUE>>24;andmed_ametikoht[1]=VALUE>>16;andmed_ametikoht[2]=VALUE>>8;andmed_ametikoht[3]=VALUE;}
static void Suletud(void){if(partner_VALUE>=0)Sule_võrk(partner_VALUE);partner_VALUE=-1;etapp_VALUE=0;입력수=toodang_COUNT=보낸수=0;paan_COUNT=paan_ametikoht=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *andmed,unsigned number){memcpy(Väljund,andmed,number);toodang_COUNT=number;보낸수=0;}
static void tarbima_VALUE(unsigned number){입력수-=number;memmove(입력,입력+number,입력수);}
int meede_kauge_ekraan(unsigned Nimi){
    if(Nimi==0){Suletud();if(Kuulamine_osaleja>=0)Sule_võrk(Kuulamine_osaleja);Kuulamine_osaleja=-1;return 0;}
    if(Nimi!=1)return Kuulamine_osaleja>=0;
    if(Kuulamine_osaleja>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int TULEMUS=NET_BIND(port_VALUE,0,5900);if(!TULEMUS)TULEMUS=NET_jälgima(port_VALUE);
    if(TULEMUS<0){Sule_võrk(port_VALUE);return TULEMUS;}Kuulamine_osaleja=port_VALUE;return 0;
}
static uint32_t paan_kokkuvõte(unsigned 가로,unsigned vertikaal_ametikoht){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=vertikaal_ametikoht;세로좌표<vertikaal_ametikoht+16&&세로좌표<높이;세로좌표++)for(unsigned 가로좌표=가로;가로좌표<가로+32&&가로좌표<너비;가로좌표++)VALUE=(VALUE^보드화면읽기(가로좌표,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *andmed_ametikoht){
    요청가로=읽기16(andmed_ametikoht+2);요청세로=읽기16(andmed_ametikoht+4);요청폭=읽기16(andmed_ametikoht+6);요청높이=읽기16(andmed_ametikoht+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    paan_COUNT=paan_ametikoht=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned 가로좌표=요청가로/32;가로좌표<=(요청가로+요청폭-1)/32;가로좌표++){
        unsigned asukohaindeks=세로좌표*60+가로좌표;uint32_t kokkuvõte_VALUE=paan_kokkuvõte(가로좌표*32,세로좌표*16);
        if(!andmed_ametikoht[1]||지난요약[asukohaindeks]!=kokkuvõte_VALUE)바뀐타일[paan_COUNT++]=asukohaindeks;
    }
    Väljund[0]=Väljund[1]=0;kirjutamine_16(Väljund+2,paan_COUNT);toodang_COUNT=4;보낸수=0;
}
static void saatma_paan(void){
    unsigned asukohaindeks=바뀐타일[paan_ametikoht++],가로=(asukohaindeks%60)*32,vertikaal_ametikoht=(asukohaindeks/60)*16;
    unsigned lõpeta_kõne_X=가로+32,lõpeta_kõne_Y=vertikaal_ametikoht+16;if(lõpeta_kõne_X>너비)lõpeta_kõne_X=너비;if(lõpeta_kõne_Y>높이)lõpeta_kõne_Y=높이;
    /* 부분 타일 päring 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&vertikaal_ametikoht>=요청세로&&lõpeta_kõne_X<=요청가로+요청폭&&lõpeta_kõne_Y<=요청세로+요청높이;
    if(전부)지난요약[asukohaindeks]=paan_kokkuvõte(가로,vertikaal_ametikoht);
    if(가로<요청가로)가로=요청가로;if(vertikaal_ametikoht<요청세로)vertikaal_ametikoht=요청세로;
    if(lõpeta_kõne_X>요청가로+요청폭)lõpeta_kõne_X=요청가로+요청폭;if(lõpeta_kõne_Y>요청세로+요청높이)lõpeta_kõne_Y=요청세로+요청높이;
    kirjutamine_16(Väljund,가로);kirjutamine_16(Väljund+2,vertikaal_ametikoht);kirjutamine_16(Väljund+4,lõpeta_kõne_X-가로);kirjutamine_16(Väljund+6,lõpeta_kõne_Y-vertikaal_ametikoht);kirjutamine_32(Väljund+8,0);
    toodang_COUNT=12;보낸수=0;
    for(unsigned 세로좌표=vertikaal_ametikoht;세로좌표<lõpeta_kõne_Y;세로좌표++)for(unsigned 가로좌표=가로;가로좌표<lõpeta_kõne_X;가로좌표++){
        uint32_t 색=보드화면읽기(가로좌표,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<piksel_suurust_muutma;순번++)Väljund[toodang_COUNT++]=VALUE>>(8*(tavabaidijärjestusega_VALUE?piksel_suurust_muutma-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Kuulamine_osaleja<0)return;
    if(partner_VALUE<0){if(보드밀리초()<다시받을때)return;partner_VALUE=NET_aktsepteerima(Kuulamine_osaleja);if(partner_VALUE<0)return;
        ühendus_Aeg=보드밀리초();etapp_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        piksel_suurust_muutma=4;tavabaidijärjestusega_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(etapp_VALUE<5&&보드밀리초()-ühendus_Aeg>15000){Suletud();return;}
    if(toodang_COUNT){int number=NET_kirjutamine(partner_VALUE,Väljund+보낸수,toodang_COUNT-보낸수);if(number>0){보낸수+=number;if(보낸수==toodang_COUNT)toodang_COUNT=보낸수=0;}else if(number!=-11){Suletud();return;}}
    if(!toodang_COUNT&&닫을예정){Suletud();return;}
    if(!toodang_COUNT&&paan_ametikoht<paan_COUNT)saatma_paan();
    if(입력수==sizeof(입력)){Suletud();return;}
    int RECEIVED_COUNT=통신읽기(partner_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Suletud();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(toodang_COUNT||paan_ametikoht<paan_COUNT)return;
    if(etapp_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Suletud();return;}tarbima_VALUE(12);const unsigned char autentimismeetod[]={1,2};내보내기(autentimismeetod,2);etapp_VALUE=2;return;}
    if(etapp_VALUE==2&&입력수){if(입력[0]!=2||kauge_juhuslik(küsimus_VALUE,16)){Suletud();return;}tarbima_VALUE(1);내보내기(küsimus_VALUE,16);etapp_VALUE=3;return;}
    if(etapp_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys parool_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&parool_VALUE,열쇠,8);memcpy(정답,küsimus_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&parool_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];tarbima_VALUE(16);memset(&parool_VALUE,0,sizeof(parool_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(küsimus_VALUE,0,16);
        kirjutamine_32(Väljund,차이?1:0);toodang_COUNT=4;보낸수=0;
        if(차이){kirjutamine_32(Väljund+4,19);memcpy(Väljund+8,"Authentication fail",19);toodang_COUNT=27;닫을예정=1;}else etapp_VALUE=4;return;}
    if(etapp_VALUE==4&&입력수){tarbima_VALUE(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Suletud();return;}
        if(!Tahvel_terminal(7)){const unsigned char Sündmus[]={30,2,1,0,0,0,0};원격입력넣기(Sündmus,7);}
        memset(Väljund,0,40);kirjutamine_16(Väljund,너비);kirjutamine_16(Väljund+2,높이);Väljund[4]=32;Väljund[5]=24;Väljund[7]=1;
        kirjutamine_16(Väljund+8,255);kirjutamine_16(Väljund+10,255);kirjutamine_16(Väljund+12,255);Väljund[14]=16;Väljund[15]=8;
        const char *Nimi_2="jkoros native";kirjutamine_32(Väljund+20,strlen(Nimi_2));memcpy(Väljund+24,Nimi_2,strlen(Nimi_2));toodang_COUNT=24+strlen(Nimi_2);보낸수=0;etapp_VALUE=5;return;}
    if(etapp_VALUE!=5||!입력수)return;
    unsigned TYPE_ala=입력[0],필요=TYPE_ala==0?20:TYPE_ala==2?4:TYPE_ala==3?10:TYPE_ala==4?8:TYPE_ala==5?6:TYPE_ala==6?8:0;
    if(!필요){Suletud();return;}if(입력수<필요)return;
    if(TYPE_ala==2){unsigned number=읽기16(입력+2);if(number>128){Suletud();return;}필요+=number*4;}
    if(TYPE_ala==6){unsigned number=읽기32(입력+4);if(number>4096){Suletud();return;}필요+=number;}
    if(입력수<필요)return;
    if(TYPE_ala==0){unsigned bitt_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bitt_VALUE!=16&&bitt_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bitt_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bitt_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bitt_VALUE)-1)){Suletud();return;}
        piksel_suurust_muutma=bitt_VALUE/8;tavabaidijärjestusega_VALUE=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_ala==3)화면요청(입력);
    else if(TYPE_ala==4)kauge_Võti_tinditõmme(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_ala==5){unsigned 가로좌표=읽기16(입력+2),세로좌표=읽기16(입력+4);if(가로좌표>=너비)가로좌표=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])kinnitamine_kauge_Võti();
        unsigned char Sündmus[]={30,1,입력[1],가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8};원격입력넣기(Sündmus,sizeof(Sündmus));}
    tarbima_VALUE(필요);
}
