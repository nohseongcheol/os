/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Pripojiť, 제한된 vstup_VALUE dĺžka_VALUE, 비동기 odoslať_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 údaje 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "vzdialený_VALUE.h"
#include "kryptografia_Podpora.h"
#include "Profil.h"
#include "../sieť_Vrstvy/sieť_Vrstvy.h"
#include "../počítač_5eb260fa/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Panel_Terminál(uintptr_t);
void vzdialený_Kľúč_ťah_perom(unsigned,int);
void incializovať_vzdialený_Kľúč_ťah_perom(void);
void potvrdenie_vzdialený_Kľúč(void);
static int Počúvanie_účastník=-1,partnerský_uzol_VALUE=-1,etapa_VALUE,닫을예정;
static uintptr_t kontakt_čas,다시받을때;
static unsigned char vstup_VALUE[8192],Výstup[4096],výzva_VALUE[16];
static unsigned vstup_COUNT,출력수,보낸수;
static unsigned 너비,výška_VALUE,pixel_zmeniť_veľkosť=4,vo_formáte_Big_Endian_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned dlaždica_COUNT,dlaždica_pozícia,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *údaje_pozícia){return(unsigned)údaje_pozícia[0]*256+údaje_pozícia[1];}
static uint32_t 읽기32(const unsigned char *údaje_pozícia){return(uint32_t)údaje_pozícia[0]<<24|(uint32_t)údaje_pozícia[1]<<16|(uint32_t)údaje_pozícia[2]<<8|údaje_pozícia[3];}
static void zapísať_16(unsigned char *údaje_pozícia,unsigned VALUE){údaje_pozícia[0]=VALUE>>8;údaje_pozícia[1]=VALUE;}
static void zapísať_32(unsigned char *údaje_pozícia,uint32_t VALUE){údaje_pozícia[0]=VALUE>>24;údaje_pozícia[1]=VALUE>>16;údaje_pozícia[2]=VALUE>>8;údaje_pozícia[3]=VALUE;}
static void Zatvoriť(void){if(partnerský_uzol_VALUE>=0)Zavrieť_sieť(partnerský_uzol_VALUE);partnerský_uzol_VALUE=-1;etapa_VALUE=0;vstup_COUNT=출력수=보낸수=0;dlaždica_COUNT=dlaždica_pozícia=0;닫을예정=0;incializovať_vzdialený_Kľúč_ťah_perom();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *údaje,unsigned 수){memcpy(Výstup,údaje,수);출력수=수;보낸수=0;}
static void použiť_VALUE(unsigned 수){vstup_COUNT-=수;memmove(vstup_VALUE,vstup_VALUE+수,vstup_COUNT);}
int riadenie_vzdialený_displej(unsigned Akcia){
    if(Akcia==0){Zatvoriť();if(Počúvanie_účastník>=0)Zavrieť_sieť(Počúvanie_účastník);Počúvanie_účastník=-1;return 0;}
    if(Akcia!=1)return Počúvanie_účastník>=0;
    if(Počúvanie_účastník>=0)return 0;
    int port_VALUE=Create_soket_účastník(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int KR=NET_BIND(port_VALUE,0,5900);if(!KR)KR=NET_načúvať(port_VALUE);
    if(KR<0){Zavrieť_sieť(port_VALUE);return KR;}Počúvanie_účastník=port_VALUE;return 0;
}
static uint32_t dlaždica_súhrn(unsigned 가로,unsigned vertikála_pozícia){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_súradnica=vertikála_pozícia;Y_súradnica<vertikála_pozícia+16&&Y_súradnica<výška_VALUE;Y_súradnica++)for(unsigned X_súradnica=가로;X_súradnica<가로+32&&X_súradnica<너비;X_súradnica++)VALUE=(VALUE^보드화면읽기(X_súradnica,Y_súradnica))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *údaje_pozícia){
    요청가로=읽기16(údaje_pozícia+2);요청세로=읽기16(údaje_pozícia+4);요청폭=읽기16(údaje_pozícia+6);요청높이=읽기16(údaje_pozícia+8);
    if(요청가로>=너비||요청세로>=výška_VALUE)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>výška_VALUE-요청세로&&요청세로<výška_VALUE)요청높이=výška_VALUE-요청세로;
    dlaždica_COUNT=dlaždica_pozícia=0;
    if(요청폭&&요청높이)for(unsigned Y_súradnica=요청세로/16;Y_súradnica<=(요청세로+요청높이-1)/16;Y_súradnica++)for(unsigned X_súradnica=요청가로/32;X_súradnica<=(요청가로+요청폭-1)/32;X_súradnica++){
        unsigned pozičný_index=Y_súradnica*60+X_súradnica;uint32_t súhrn_VALUE=dlaždica_súhrn(X_súradnica*32,Y_súradnica*16);
        if(!údaje_pozícia[1]||지난요약[pozičný_index]!=súhrn_VALUE)바뀐타일[dlaždica_COUNT++]=pozičný_index;
    }
    Výstup[0]=Výstup[1]=0;zapísať_16(Výstup+2,dlaždica_COUNT);출력수=4;보낸수=0;
}
static void odoslať_dlaždica(void){
    unsigned pozičný_index=바뀐타일[dlaždica_pozícia++],가로=(pozičný_index%60)*32,vertikála_pozícia=(pozičný_index/60)*16;
    unsigned ukončiť_hovor_X=가로+32,ukončiť_hovor_Y=vertikála_pozícia+16;if(ukončiť_hovor_X>너비)ukončiť_hovor_X=너비;if(ukončiť_hovor_Y>výška_VALUE)ukončiť_hovor_Y=výška_VALUE;
    /* 부분 타일 požiadavka 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&vertikála_pozícia>=요청세로&&ukončiť_hovor_X<=요청가로+요청폭&&ukončiť_hovor_Y<=요청세로+요청높이;
    if(전부)지난요약[pozičný_index]=dlaždica_súhrn(가로,vertikála_pozícia);
    if(가로<요청가로)가로=요청가로;if(vertikála_pozícia<요청세로)vertikála_pozícia=요청세로;
    if(ukončiť_hovor_X>요청가로+요청폭)ukončiť_hovor_X=요청가로+요청폭;if(ukončiť_hovor_Y>요청세로+요청높이)ukončiť_hovor_Y=요청세로+요청높이;
    zapísať_16(Výstup,가로);zapísať_16(Výstup+2,vertikála_pozícia);zapísať_16(Výstup+4,ukončiť_hovor_X-가로);zapísať_16(Výstup+6,ukončiť_hovor_Y-vertikála_pozícia);zapísať_32(Výstup+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_súradnica=vertikála_pozícia;Y_súradnica<ukončiť_hovor_Y;Y_súradnica++)for(unsigned X_súradnica=가로;X_súradnica<ukončiť_hovor_X;X_súradnica++){
        uint32_t 색=보드화면읽기(X_súradnica,Y_súradnica),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pixel_zmeniť_veľkosť;순번++)Výstup[출력수++]=VALUE>>(8*(vo_formáte_Big_Endian_VALUE?pixel_zmeniť_veľkosť-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Počúvanie_účastník<0)return;
    if(partnerský_uzol_VALUE<0){if(보드밀리초()<다시받을때)return;partnerský_uzol_VALUE=NET_prijať(Počúvanie_účastník);if(partnerský_uzol_VALUE<0)return;
        kontakt_čas=보드밀리초();etapa_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pixel_zmeniť_veľkosť=4;vo_formáte_Big_Endian_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(etapa_VALUE<5&&보드밀리초()-kontakt_čas>15000){Zatvoriť();return;}
    if(출력수){int 수=NET_zapísať(partnerský_uzol_VALUE,Výstup+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Zatvoriť();return;}}
    if(!출력수&&닫을예정){Zatvoriť();return;}
    if(!출력수&&dlaždica_pozícia<dlaždica_COUNT)odoslať_dlaždica();
    if(vstup_COUNT==sizeof(vstup_VALUE)){Zatvoriť();return;}
    int RECEIVED_COUNT=통신읽기(partnerský_uzol_VALUE,vstup_VALUE+vstup_COUNT,sizeof(vstup_VALUE)-vstup_COUNT);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Zatvoriť();return;}if(RECEIVED_COUNT>0)vstup_COUNT+=RECEIVED_COUNT;
    if(출력수||dlaždica_pozícia<dlaždica_COUNT)return;
    if(etapa_VALUE==1&&vstup_COUNT>=12){if(memcmp(vstup_VALUE,"RFB 003.008\n",12)){Zatvoriť();return;}použiť_VALUE(12);const unsigned char metóda_overovania[]={1,2};내보내기(metóda_overovania,2);etapa_VALUE=2;return;}
    if(etapa_VALUE==2&&vstup_COUNT){if(vstup_VALUE[0]!=2||vzdialený_náhodný(výzva_VALUE,16)){Zatvoriť();return;}použiť_VALUE(1);내보내기(výzva_VALUE,16);etapa_VALUE=3;return;}
    if(etapa_VALUE==3&&vstup_COUNT>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys heslo_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&heslo_VALUE,열쇠,8);memcpy(정답,výzva_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&heslo_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^vstup_VALUE[순번];použiť_VALUE(16);memset(&heslo_VALUE,0,sizeof(heslo_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(výzva_VALUE,0,16);
        zapísať_32(Výstup,차이?1:0);출력수=4;보낸수=0;
        if(차이){zapísať_32(Výstup+4,19);memcpy(Výstup+8,"Authentication fail",19);출력수=27;닫을예정=1;}else etapa_VALUE=4;return;}
    if(etapa_VALUE==4&&vstup_COUNT){použiť_VALUE(1);너비=보드화면너비();výška_VALUE=보드화면높이();if(!너비||!výška_VALUE||너비>1920||výška_VALUE>1080){Zatvoriť();return;}
        if(!Panel_Terminál(7)){const unsigned char Udalosť[]={30,2,1,0,0,0,0};súhrnný_obsah_vzdialený_vstup(Udalosť,7);}
        memset(Výstup,0,40);zapísať_16(Výstup,너비);zapísať_16(Výstup+2,výška_VALUE);Výstup[4]=32;Výstup[5]=24;Výstup[7]=1;
        zapísať_16(Výstup+8,255);zapísať_16(Výstup+10,255);zapísať_16(Výstup+12,255);Výstup[14]=16;Výstup[15]=8;
        const char *Názov="jkoros native";zapísať_32(Výstup+20,strlen(Názov));memcpy(Výstup+24,Názov,strlen(Názov));출력수=24+strlen(Názov);보낸수=0;etapa_VALUE=5;return;}
    if(etapa_VALUE!=5||!vstup_COUNT)return;
    unsigned Typ_oblasť=vstup_VALUE[0],필요=Typ_oblasť==0?20:Typ_oblasť==2?4:Typ_oblasť==3?10:Typ_oblasť==4?8:Typ_oblasť==5?6:Typ_oblasť==6?8:0;
    if(!필요){Zatvoriť();return;}if(vstup_COUNT<필요)return;
    if(Typ_oblasť==2){unsigned 수=읽기16(vstup_VALUE+2);if(수>128){Zatvoriť();return;}필요+=수*4;}
    if(Typ_oblasť==6){unsigned 수=읽기32(vstup_VALUE+4);if(수>4096){Zatvoriť();return;}필요+=수;}
    if(vstup_COUNT<필요)return;
    if(Typ_oblasť==0){unsigned Bit_VALUE=vstup_VALUE[4],빨=읽기16(vstup_VALUE+8),초=읽기16(vstup_VALUE+10),파=읽기16(vstup_VALUE+12),빨이=vstup_VALUE[14],초이=vstup_VALUE[15],파이=vstup_VALUE[16];
        if((Bit_VALUE!=16&&Bit_VALUE!=32)||!vstup_VALUE[7]||vstup_VALUE[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<Bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<Bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<Bit_VALUE)-1)){Zatvoriť();return;}
        pixel_zmeniť_veľkosť=Bit_VALUE/8;vo_formáte_Big_Endian_VALUE=vstup_VALUE[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(Typ_oblasť==3)화면요청(vstup_VALUE);
    else if(Typ_oblasť==4)vzdialený_Kľúč_ťah_perom(읽기32(vstup_VALUE+4),vstup_VALUE[1]!=0);
    else if(Typ_oblasť==5){unsigned X_súradnica=읽기16(vstup_VALUE+2),Y_súradnica=읽기16(vstup_VALUE+4);if(X_súradnica>=너비)X_súradnica=너비-1;if(Y_súradnica>=výška_VALUE)Y_súradnica=výška_VALUE-1;
        if(vstup_VALUE[1])potvrdenie_vzdialený_Kľúč();
        unsigned char Udalosť[]={30,1,vstup_VALUE[1],X_súradnica&255,X_súradnica>>8,Y_súradnica&255,Y_súradnica>>8};súhrnný_obsah_vzdialený_vstup(Udalosť,sizeof(Udalosť));}
    použiť_VALUE(필요);
}
