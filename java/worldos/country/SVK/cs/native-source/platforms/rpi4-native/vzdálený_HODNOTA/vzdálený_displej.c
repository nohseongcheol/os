/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Připojit, 제한된 vstup_HODNOTA délka_HODNOTA, 비동기 poslat_HODNOTA, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "vzdálený_HODNOTA.h"
#include "šifrování_vzpěra.h"
#include "Profil.h"
#include "../síť_Štos/síť_Štos.h"
#include "../počítač/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Panel_Terminál(uintptr_t);
void vzdálený_Klíč_tah(unsigned,int);
void inicializovat_vzdálený_Klíč_tah(void);
void zápis_vzdálený_Klíč(void);
static int Poslouchám_účastník=-1,partner_HODNOTA=-1,fáze_HODNOTA,닫을예정;
static uintptr_t kontakt_ČAS,다시받을때;
static unsigned char vstup_HODNOTA[8192],výstupní_pozice[4096],výzva_HODNOTA[16];
static unsigned vstup_POČET,výstup_POČET,보낸수;
static unsigned 너비,výška_HODNOTA,pixel_změnit_velikost=4,ve_formátu_Big_Endian_HODNOTA,빨강최대=255,초록최대=255,파랑최대=255,červená_posunout=16,zelená_posunout=8,modrá_posunout;
static uint32_t Předchozí_souhrn[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned čtverec_POČET,čtverec_pozice,vyžádáno_X,vyžádáno_Y,요청폭,vyžádáno_výška;
static unsigned 읽기16(const unsigned char *data_pozice){return(unsigned)data_pozice[0]*256+data_pozice[1];}
static uint32_t 읽기32(const unsigned char *data_pozice){return(uint32_t)data_pozice[0]<<24|(uint32_t)data_pozice[1]<<16|(uint32_t)data_pozice[2]<<8|data_pozice[3];}
static void zápis_16(unsigned char *data_pozice,unsigned HODNOTA){data_pozice[0]=HODNOTA>>8;data_pozice[1]=HODNOTA;}
static void zápis_32(unsigned char *data_pozice,uint32_t HODNOTA){data_pozice[0]=HODNOTA>>24;data_pozice[1]=HODNOTA>>16;data_pozice[2]=HODNOTA>>8;data_pozice[3]=HODNOTA;}
static void Zavřené(void){if(partner_HODNOTA>=0)Zavřít_síť(partner_HODNOTA);partner_HODNOTA=-1;fáze_HODNOTA=0;vstup_POČET=výstup_POČET=보낸수=0;čtverec_POČET=čtverec_pozice=0;닫을예정=0;inicializovat_vzdálený_Klíč_tah();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned číslo){memcpy(výstupní_pozice,data,číslo);výstup_POČET=číslo;보낸수=0;}
static void využívat_HODNOTA(unsigned číslo){vstup_POČET-=číslo;memmove(vstup_HODNOTA,vstup_HODNOTA+číslo,vstup_POČET);}
int řízení_vzdálený_displej(unsigned Akce){
    if(Akce==0){Zavřené();if(Poslouchám_účastník>=0)Zavřít_síť(Poslouchám_účastník);Poslouchám_účastník=-1;return 0;}
    if(Akce!=1)return Poslouchám_účastník>=0;
    if(Poslouchám_účastník>=0)return 0;
    int port_HODNOTA=Create_soket_účastník(1);if(port_HODNOTA<0)return port_HODNOTA;통신주소재사용(port_HODNOTA);
    int VÝSLEDEK=čistý_vázat(port_HODNOTA,0,5900);if(!VÝSLEDEK)VÝSLEDEK=čistý_naslouchat(port_HODNOTA);
    if(VÝSLEDEK<0){Zavřít_síť(port_HODNOTA);return VÝSLEDEK;}Poslouchám_účastník=port_HODNOTA;return 0;
}
static uint32_t čtverec_souhrn(unsigned 가로,unsigned Svislá_pozice){
    uint32_t HODNOTA=2166136261u;
    for(unsigned Y_souřadnice=Svislá_pozice;Y_souřadnice<Svislá_pozice+16&&Y_souřadnice<výška_HODNOTA;Y_souřadnice++)for(unsigned souřadnice_x=가로;souřadnice_x<가로+32&&souřadnice_x<너비;souřadnice_x++)HODNOTA=(HODNOTA^보드화면읽기(souřadnice_x,Y_souřadnice))*16777619u;
    return HODNOTA;
}
static void 화면요청(const unsigned char *data_pozice){
    vyžádáno_X=읽기16(data_pozice+2);vyžádáno_Y=읽기16(data_pozice+4);요청폭=읽기16(data_pozice+6);vyžádáno_výška=읽기16(data_pozice+8);
    if(vyžádáno_X>=너비||vyžádáno_Y>=výška_HODNOTA)요청폭=vyžádáno_výška=0;
    if(요청폭>너비-vyžádáno_X&&vyžádáno_X<너비)요청폭=너비-vyžádáno_X;
    if(vyžádáno_výška>výška_HODNOTA-vyžádáno_Y&&vyžádáno_Y<výška_HODNOTA)vyžádáno_výška=výška_HODNOTA-vyžádáno_Y;
    čtverec_POČET=čtverec_pozice=0;
    if(요청폭&&vyžádáno_výška)for(unsigned Y_souřadnice=vyžádáno_Y/16;Y_souřadnice<=(vyžádáno_Y+vyžádáno_výška-1)/16;Y_souřadnice++)for(unsigned souřadnice_x=vyžádáno_X/32;souřadnice_x<=(vyžádáno_X+요청폭-1)/32;souřadnice_x++){
        unsigned poziční_index=Y_souřadnice*60+souřadnice_x;uint32_t souhrn_HODNOTA=čtverec_souhrn(souřadnice_x*32,Y_souřadnice*16);
        if(!data_pozice[1]||Předchozí_souhrn[poziční_index]!=souhrn_HODNOTA)바뀐타일[čtverec_POČET++]=poziční_index;
    }
    výstupní_pozice[0]=výstupní_pozice[1]=0;zápis_16(výstupní_pozice+2,čtverec_POČET);výstup_POČET=4;보낸수=0;
}
static void poslat_čtverec(void){
    unsigned poziční_index=바뀐타일[čtverec_pozice++],가로=(poziční_index%60)*32,Svislá_pozice=(poziční_index/60)*16;
    unsigned konec_X=가로+32,konec_Y=Svislá_pozice+16;if(konec_X>너비)konec_X=너비;if(konec_Y>výška_HODNOTA)konec_Y=výška_HODNOTA;
    /* 부분 타일 žádost 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=vyžádáno_X&&Svislá_pozice>=vyžádáno_Y&&konec_X<=vyžádáno_X+요청폭&&konec_Y<=vyžádáno_Y+vyžádáno_výška;
    if(전부)Předchozí_souhrn[poziční_index]=čtverec_souhrn(가로,Svislá_pozice);
    if(가로<vyžádáno_X)가로=vyžádáno_X;if(Svislá_pozice<vyžádáno_Y)Svislá_pozice=vyžádáno_Y;
    if(konec_X>vyžádáno_X+요청폭)konec_X=vyžádáno_X+요청폭;if(konec_Y>vyžádáno_Y+vyžádáno_výška)konec_Y=vyžádáno_Y+vyžádáno_výška;
    zápis_16(výstupní_pozice,가로);zápis_16(výstupní_pozice+2,Svislá_pozice);zápis_16(výstupní_pozice+4,konec_X-가로);zápis_16(výstupní_pozice+6,konec_Y-Svislá_pozice);zápis_32(výstupní_pozice+8,0);
    výstup_POČET=12;보낸수=0;
    for(unsigned Y_souřadnice=Svislá_pozice;Y_souřadnice<konec_Y;Y_souřadnice++)for(unsigned souřadnice_x=가로;souřadnice_x<konec_X;souřadnice_x++){
        uint32_t 색=보드화면읽기(souřadnice_x,Y_souřadnice),HODNOTA=(((색>>16)&255)*빨강최대/255)<<červená_posunout|
            (((색>>8)&255)*초록최대/255)<<zelená_posunout|((색&255)*파랑최대/255)<<modrá_posunout;
        for(unsigned 순번=0;순번<pixel_změnit_velikost;순번++)výstupní_pozice[výstup_POČET++]=HODNOTA>>(8*(ve_formátu_Big_Endian_HODNOTA?pixel_změnit_velikost-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Poslouchám_účastník<0)return;
    if(partner_HODNOTA<0){if(보드밀리초()<다시받을때)return;partner_HODNOTA=čistý_přijmout(Poslouchám_účastník);if(partner_HODNOTA<0)return;
        kontakt_ČAS=보드밀리초();fáze_HODNOTA=1;내보내기("RFB 003.008\n",12);memset(Předchozí_souhrn,0,sizeof(Předchozí_souhrn));
        pixel_změnit_velikost=4;ve_formátu_Big_Endian_HODNOTA=0;빨강최대=초록최대=파랑최대=255;červená_posunout=16;zelená_posunout=8;modrá_posunout=0;}
    if(fáze_HODNOTA<5&&보드밀리초()-kontakt_ČAS>15000){Zavřené();return;}
    if(výstup_POČET){int číslo=čistý_zápis(partner_HODNOTA,výstupní_pozice+보낸수,výstup_POČET-보낸수);if(číslo>0){보낸수+=číslo;if(보낸수==výstup_POČET)výstup_POČET=보낸수=0;}else if(číslo!=-11){Zavřené();return;}}
    if(!výstup_POČET&&닫을예정){Zavřené();return;}
    if(!výstup_POČET&&čtverec_pozice<čtverec_POČET)poslat_čtverec();
    if(vstup_POČET==sizeof(vstup_HODNOTA)){Zavřené();return;}
    int RECEIVED_POČET=통신읽기(partner_HODNOTA,vstup_HODNOTA+vstup_POČET,sizeof(vstup_HODNOTA)-vstup_POČET);
    if(RECEIVED_POČET==0||(RECEIVED_POČET<0&&RECEIVED_POČET!=-11)){Zavřené();return;}if(RECEIVED_POČET>0)vstup_POČET+=RECEIVED_POČET;
    if(výstup_POČET||čtverec_pozice<čtverec_POČET)return;
    if(fáze_HODNOTA==1&&vstup_POČET>=12){if(memcmp(vstup_HODNOTA,"RFB 003.008\n",12)){Zavřené();return;}využívat_HODNOTA(12);const unsigned char metoda_ověřování[]={1,2};내보내기(metoda_ověřování,2);fáze_HODNOTA=2;return;}
    if(fáze_HODNOTA==2&&vstup_POČET){if(vstup_HODNOTA[0]!=2||원격난수(výzva_HODNOTA,16)){Zavřené();return;}využívat_HODNOTA(1);내보내기(výzva_HODNOTA,16);fáze_HODNOTA=3;return;}
    if(fáze_HODNOTA==3&&vstup_POČET>=16){unsigned char Klíč_materiál[8],정답[16];br_des_ct_cbcenc_keys heslo_HODNOTA;
        for(unsigned 순번=0;순번<8;순번++){unsigned HODNOTA=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(HODNOTA&1);HODNOTA>>=1;}Klíč_materiál[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&heslo_HODNOTA,Klíč_materiál,8);memcpy(정답,výzva_HODNOTA,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_HODNOTA[8]={0};br_des_ct_cbcenc_run(&heslo_HODNOTA,vektor_HODNOTA,정답+순번,8);memset(vektor_HODNOTA,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^vstup_HODNOTA[순번];využívat_HODNOTA(16);memset(&heslo_HODNOTA,0,sizeof(heslo_HODNOTA));memset(Klíč_materiál,0,8);memset(정답,0,16);memset(výzva_HODNOTA,0,16);
        zápis_32(výstupní_pozice,차이?1:0);výstup_POČET=4;보낸수=0;
        if(차이){zápis_32(výstupní_pozice+4,19);memcpy(výstupní_pozice+8,"Authentication fail",19);výstup_POČET=27;닫을예정=1;}else fáze_HODNOTA=4;return;}
    if(fáze_HODNOTA==4&&vstup_POČET){využívat_HODNOTA(1);너비=보드화면너비();výška_HODNOTA=보드화면높이();if(!너비||!výška_HODNOTA||너비>1920||výška_HODNOTA>1080){Zavřené();return;}
        if(!Panel_Terminál(7)){const unsigned char Události[]={30,2,1,0,0,0,0};novinky_vzdálený_vstup(Události,7);}
        memset(výstupní_pozice,0,40);zápis_16(výstupní_pozice,너비);zápis_16(výstupní_pozice+2,výška_HODNOTA);výstupní_pozice[4]=32;výstupní_pozice[5]=24;výstupní_pozice[7]=1;
        zápis_16(výstupní_pozice+8,255);zápis_16(výstupní_pozice+10,255);zápis_16(výstupní_pozice+12,255);výstupní_pozice[14]=16;výstupní_pozice[15]=8;
        const char *Název="jkoros native";zápis_32(výstupní_pozice+20,strlen(Název));memcpy(výstupní_pozice+24,Název,strlen(Název));výstup_POČET=24+strlen(Název);보낸수=0;fáze_HODNOTA=5;return;}
    if(fáze_HODNOTA!=5||!vstup_POČET)return;
    unsigned TYP_oblast=vstup_HODNOTA[0],필요=TYP_oblast==0?20:TYP_oblast==2?4:TYP_oblast==3?10:TYP_oblast==4?8:TYP_oblast==5?6:TYP_oblast==6?8:0;
    if(!필요){Zavřené();return;}if(vstup_POČET<필요)return;
    if(TYP_oblast==2){unsigned číslo=읽기16(vstup_HODNOTA+2);if(číslo>128){Zavřené();return;}필요+=číslo*4;}
    if(TYP_oblast==6){unsigned číslo=읽기32(vstup_HODNOTA+4);if(číslo>4096){Zavřené();return;}필요+=číslo;}
    if(vstup_POČET<필요)return;
    if(TYP_oblast==0){unsigned bit_HODNOTA=vstup_HODNOTA[4],빨=읽기16(vstup_HODNOTA+8),초=읽기16(vstup_HODNOTA+10),파=읽기16(vstup_HODNOTA+12),červená_Kanál_posunout=vstup_HODNOTA[14],zelená_Kanál_posunout=vstup_HODNOTA[15],modrá_Kanál_posunout=vstup_HODNOTA[16];
        if((bit_HODNOTA!=16&&bit_HODNOTA!=32)||!vstup_HODNOTA[7]||vstup_HODNOTA[6]>1||!빨||!초||!파||빨>255||초>255||파>255||červená_Kanál_posunout>24||zelená_Kanál_posunout>24||modrá_Kanál_posunout>24||
           ((uint64_t)빨<<červená_Kanál_posunout)>((1ull<<bit_HODNOTA)-1)||((uint64_t)초<<zelená_Kanál_posunout)>((1ull<<bit_HODNOTA)-1)||((uint64_t)파<<modrá_Kanál_posunout)>((1ull<<bit_HODNOTA)-1)){Zavřené();return;}
        pixel_změnit_velikost=bit_HODNOTA/8;ve_formátu_Big_Endian_HODNOTA=vstup_HODNOTA[6];빨강최대=빨;초록최대=초;파랑최대=파;červená_posunout=červená_Kanál_posunout;zelená_posunout=zelená_Kanál_posunout;modrá_posunout=modrá_Kanál_posunout;memset(Předchozí_souhrn,0,sizeof(Předchozí_souhrn));
    }else if(TYP_oblast==3)화면요청(vstup_HODNOTA);
    else if(TYP_oblast==4)vzdálený_Klíč_tah(읽기32(vstup_HODNOTA+4),vstup_HODNOTA[1]!=0);
    else if(TYP_oblast==5){unsigned souřadnice_x=읽기16(vstup_HODNOTA+2),Y_souřadnice=읽기16(vstup_HODNOTA+4);if(souřadnice_x>=너비)souřadnice_x=너비-1;if(Y_souřadnice>=výška_HODNOTA)Y_souřadnice=výška_HODNOTA-1;
        if(vstup_HODNOTA[1])zápis_vzdálený_Klíč();
        unsigned char Události[]={30,1,vstup_HODNOTA[1],souřadnice_x&255,souřadnice_x>>8,Y_souřadnice&255,Y_souřadnice>>8};novinky_vzdálený_vstup(Události,sizeof(Události));}
    využívat_HODNOTA(필요);
}
