/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Prisijungti, 제한된 입력 길이, 비동기 siųsti_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 duomenys 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "nuotolinis_VALUE.h"
#include "kriptografija_pagalba.h"
#include "Profilis.h"
#include "../tinklas_eilė/tinklas_eilė.h"
#include "../mašina/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Lenta_Terminalas(uintptr_t);
void nuotolinis_Raktas_brūkštelėjimas_stiliumi(unsigned,int);
void 원격글쇠초기화(void);
void vykdymas_nuotolinis_Raktas(void);
static int Klausausi_dalyvis=-1,lygiavertis_mazgas_VALUE=-1,etapas_VALUE,닫을예정;
static uintptr_t ryšys_TIME,다시받을때;
static unsigned char 입력[8192],Išvestis[4096],iššūkis_VALUE[16];
static unsigned 입력수,išeiga_COUNT,보낸수;
static unsigned 너비,높이,pikselis_dydis=4,mažėjantys_baitai_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned iškloti_COUNT,iškloti_padėtis,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *duomenys_padėtis){return(unsigned)duomenys_padėtis[0]*256+duomenys_padėtis[1];}
static uint32_t 읽기32(const unsigned char *duomenys_padėtis){return(uint32_t)duomenys_padėtis[0]<<24|(uint32_t)duomenys_padėtis[1]<<16|(uint32_t)duomenys_padėtis[2]<<8|duomenys_padėtis[3];}
static void rašymas_16(unsigned char *duomenys_padėtis,unsigned VALUE){duomenys_padėtis[0]=VALUE>>8;duomenys_padėtis[1]=VALUE;}
static void rašymas_32(unsigned char *duomenys_padėtis,uint32_t VALUE){duomenys_padėtis[0]=VALUE>>24;duomenys_padėtis[1]=VALUE>>16;duomenys_padėtis[2]=VALUE>>8;duomenys_padėtis[3]=VALUE;}
static void Užverti(void){if(lygiavertis_mazgas_VALUE>=0)Uždaryti_tinklas(lygiavertis_mazgas_VALUE);lygiavertis_mazgas_VALUE=-1;etapas_VALUE=0;입력수=išeiga_COUNT=보낸수=0;iškloti_COUNT=iškloti_padėtis=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *duomenys,unsigned numeris){memcpy(Išvestis,duomenys,numeris);išeiga_COUNT=numeris;보낸수=0;}
static void vartoti_VALUE(unsigned numeris){입력수-=numeris;memmove(입력,입력+numeris,입력수);}
int valdymas_nuotolinis_rodyti(unsigned Veiksmas){
    if(Veiksmas==0){Užverti();if(Klausausi_dalyvis>=0)Uždaryti_tinklas(Klausausi_dalyvis);Klausausi_dalyvis=-1;return 0;}
    if(Veiksmas!=1)return Klausausi_dalyvis>=0;
    if(Klausausi_dalyvis>=0)return 0;
    int jungtis_VALUE=통신끝점만들기(1);if(jungtis_VALUE<0)return jungtis_VALUE;통신주소재사용(jungtis_VALUE);
    int REZULTATAS=NET_BIND(jungtis_VALUE,0,5900);if(!REZULTATAS)REZULTATAS=NET_laukti(jungtis_VALUE);
    if(REZULTATAS<0){Uždaryti_tinklas(jungtis_VALUE);return REZULTATAS;}Klausausi_dalyvis=jungtis_VALUE;return 0;
}
static uint32_t iškloti_suvestinė(unsigned 가로,unsigned segmentas_padėtis){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=segmentas_padėtis;세로좌표<segmentas_padėtis+16&&세로좌표<높이;세로좌표++)for(unsigned x_koordinatė=가로;x_koordinatė<가로+32&&x_koordinatė<너비;x_koordinatė++)VALUE=(VALUE^보드화면읽기(x_koordinatė,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *duomenys_padėtis){
    요청가로=읽기16(duomenys_padėtis+2);요청세로=읽기16(duomenys_padėtis+4);요청폭=읽기16(duomenys_padėtis+6);요청높이=읽기16(duomenys_padėtis+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    iškloti_COUNT=iškloti_padėtis=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned x_koordinatė=요청가로/32;x_koordinatė<=(요청가로+요청폭-1)/32;x_koordinatė++){
        unsigned vietos_rodyklė=세로좌표*60+x_koordinatė;uint32_t suvestinė_VALUE=iškloti_suvestinė(x_koordinatė*32,세로좌표*16);
        if(!duomenys_padėtis[1]||지난요약[vietos_rodyklė]!=suvestinė_VALUE)바뀐타일[iškloti_COUNT++]=vietos_rodyklė;
    }
    Išvestis[0]=Išvestis[1]=0;rašymas_16(Išvestis+2,iškloti_COUNT);išeiga_COUNT=4;보낸수=0;
}
static void siųsti_iškloti(void){
    unsigned vietos_rodyklė=바뀐타일[iškloti_padėtis++],가로=(vietos_rodyklė%60)*32,segmentas_padėtis=(vietos_rodyklė/60)*16;
    unsigned baigti_pokalbį_X=가로+32,baigti_pokalbį_Y=segmentas_padėtis+16;if(baigti_pokalbį_X>너비)baigti_pokalbį_X=너비;if(baigti_pokalbį_Y>높이)baigti_pokalbį_Y=높이;
    /* 부분 타일 užklausa 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&segmentas_padėtis>=요청세로&&baigti_pokalbį_X<=요청가로+요청폭&&baigti_pokalbį_Y<=요청세로+요청높이;
    if(전부)지난요약[vietos_rodyklė]=iškloti_suvestinė(가로,segmentas_padėtis);
    if(가로<요청가로)가로=요청가로;if(segmentas_padėtis<요청세로)segmentas_padėtis=요청세로;
    if(baigti_pokalbį_X>요청가로+요청폭)baigti_pokalbį_X=요청가로+요청폭;if(baigti_pokalbį_Y>요청세로+요청높이)baigti_pokalbį_Y=요청세로+요청높이;
    rašymas_16(Išvestis,가로);rašymas_16(Išvestis+2,segmentas_padėtis);rašymas_16(Išvestis+4,baigti_pokalbį_X-가로);rašymas_16(Išvestis+6,baigti_pokalbį_Y-segmentas_padėtis);rašymas_32(Išvestis+8,0);
    išeiga_COUNT=12;보낸수=0;
    for(unsigned 세로좌표=segmentas_padėtis;세로좌표<baigti_pokalbį_Y;세로좌표++)for(unsigned x_koordinatė=가로;x_koordinatė<baigti_pokalbį_X;x_koordinatė++){
        uint32_t 색=보드화면읽기(x_koordinatė,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pikselis_dydis;순번++)Išvestis[išeiga_COUNT++]=VALUE>>(8*(mažėjantys_baitai_VALUE?pikselis_dydis-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Klausausi_dalyvis<0)return;
    if(lygiavertis_mazgas_VALUE<0){if(보드밀리초()<다시받을때)return;lygiavertis_mazgas_VALUE=NET_priimti(Klausausi_dalyvis);if(lygiavertis_mazgas_VALUE<0)return;
        ryšys_TIME=보드밀리초();etapas_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pikselis_dydis=4;mažėjantys_baitai_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(etapas_VALUE<5&&보드밀리초()-ryšys_TIME>15000){Užverti();return;}
    if(išeiga_COUNT){int numeris=NET_rašymas(lygiavertis_mazgas_VALUE,Išvestis+보낸수,išeiga_COUNT-보낸수);if(numeris>0){보낸수+=numeris;if(보낸수==išeiga_COUNT)išeiga_COUNT=보낸수=0;}else if(numeris!=-11){Užverti();return;}}
    if(!išeiga_COUNT&&닫을예정){Užverti();return;}
    if(!išeiga_COUNT&&iškloti_padėtis<iškloti_COUNT)siųsti_iškloti();
    if(입력수==sizeof(입력)){Užverti();return;}
    int RECEIVED_COUNT=통신읽기(lygiavertis_mazgas_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Užverti();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(išeiga_COUNT||iškloti_padėtis<iškloti_COUNT)return;
    if(etapas_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Užverti();return;}vartoti_VALUE(12);const unsigned char autentifikavimo_metodas[]={1,2};내보내기(autentifikavimo_metodas,2);etapas_VALUE=2;return;}
    if(etapas_VALUE==2&&입력수){if(입력[0]!=2||nuotolinis_atsitiktinis(iššūkis_VALUE,16)){Užverti();return;}vartoti_VALUE(1);내보내기(iššūkis_VALUE,16);etapas_VALUE=3;return;}
    if(etapas_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys slaptažodis_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&slaptažodis_VALUE,열쇠,8);memcpy(정답,iššūkis_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektorius_VALUE[8]={0};br_des_ct_cbcenc_run(&slaptažodis_VALUE,vektorius_VALUE,정답+순번,8);memset(vektorius_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];vartoti_VALUE(16);memset(&slaptažodis_VALUE,0,sizeof(slaptažodis_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(iššūkis_VALUE,0,16);
        rašymas_32(Išvestis,차이?1:0);išeiga_COUNT=4;보낸수=0;
        if(차이){rašymas_32(Išvestis+4,19);memcpy(Išvestis+8,"Authentication fail",19);išeiga_COUNT=27;닫을예정=1;}else etapas_VALUE=4;return;}
    if(etapas_VALUE==4&&입력수){vartoti_VALUE(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Užverti();return;}
        if(!Lenta_Terminalas(7)){const unsigned char Įvykis[]={30,2,1,0,0,0,0};원격입력넣기(Įvykis,7);}
        memset(Išvestis,0,40);rašymas_16(Išvestis,너비);rašymas_16(Išvestis+2,높이);Išvestis[4]=32;Išvestis[5]=24;Išvestis[7]=1;
        rašymas_16(Išvestis+8,255);rašymas_16(Išvestis+10,255);rašymas_16(Išvestis+12,255);Išvestis[14]=16;Išvestis[15]=8;
        const char *Pavadinimas_2="jkoros native";rašymas_32(Išvestis+20,strlen(Pavadinimas_2));memcpy(Išvestis+24,Pavadinimas_2,strlen(Pavadinimas_2));išeiga_COUNT=24+strlen(Pavadinimas_2);보낸수=0;etapas_VALUE=5;return;}
    if(etapas_VALUE!=5||!입력수)return;
    unsigned TYPE_sritis=입력[0],필요=TYPE_sritis==0?20:TYPE_sritis==2?4:TYPE_sritis==3?10:TYPE_sritis==4?8:TYPE_sritis==5?6:TYPE_sritis==6?8:0;
    if(!필요){Užverti();return;}if(입력수<필요)return;
    if(TYPE_sritis==2){unsigned numeris=읽기16(입력+2);if(numeris>128){Užverti();return;}필요+=numeris*4;}
    if(TYPE_sritis==6){unsigned numeris=읽기32(입력+4);if(numeris>4096){Užverti();return;}필요+=numeris;}
    if(입력수<필요)return;
    if(TYPE_sritis==0){unsigned bitas_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bitas_VALUE!=16&&bitas_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bitas_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bitas_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bitas_VALUE)-1)){Užverti();return;}
        pikselis_dydis=bitas_VALUE/8;mažėjantys_baitai_VALUE=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_sritis==3)화면요청(입력);
    else if(TYPE_sritis==4)nuotolinis_Raktas_brūkštelėjimas_stiliumi(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_sritis==5){unsigned x_koordinatė=읽기16(입력+2),세로좌표=읽기16(입력+4);if(x_koordinatė>=너비)x_koordinatė=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])vykdymas_nuotolinis_Raktas();
        unsigned char Įvykis[]={30,1,입력[1],x_koordinatė&255,x_koordinatė>>8,세로좌표&255,세로좌표>>8};원격입력넣기(Įvykis,sizeof(Įvykis));}
    vartoti_VALUE(필요);
}
