/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Anslut, 제한된 indata_värde längd_värde, 비동기 skicka_värde_f993dacd, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 skärmbild data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "fjärr_värde.h"
#include "kryptografi_stöd.h"
#include "Profil.h"
#include "../nätverk_Stack/nätverk_Stack.h"
#include "../dator/skärmbild_info.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(skärmbild_lösenord)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tavla_Terminal(uintptr_t);
void fjärr_Nyckel_pennstreck(unsigned,int);
void starta_fjärr_Nyckel_pennstreck(void);
void incheckning_fjärr_Nyckel(void);
static int Lyssnar_deltagare=-1,peer_värde=-1,scen_värde,닫을예정;
static uintptr_t kontakt_tid,다시받을때;
static unsigned char indata_värde[8192],utmatningsposition[4096],kontroll_värde_c2a235ad[16];
static unsigned indata_ANTAL,utleverans_ANTAL,보낸수;
static unsigned 너비,높이,bildpunkt_storlek=4,big_endian_värde,빨강최대=255,초록최대=255,파랑최대=255,röd_skifta=16,grön_skifta=8,blå_skifta;
static uint32_t Föregående_sammanfattning[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned ikon_ANTAL,ikon_placera,begärd_X,begärd_Y,요청폭,요청높이;
static unsigned läsa_16(const unsigned char *data_placera){return(unsigned)data_placera[0]*256+data_placera[1];}
static uint32_t läsa_32(const unsigned char *data_placera){return(uint32_t)data_placera[0]<<24|(uint32_t)data_placera[1]<<16|(uint32_t)data_placera[2]<<8|data_placera[3];}
static void skriva_16(unsigned char *data_placera,unsigned värde){data_placera[0]=värde>>8;data_placera[1]=värde;}
static void skriva_32(unsigned char *data_placera,uint32_t värde){data_placera[0]=värde>>24;data_placera[1]=värde>>16;data_placera[2]=värde>>8;data_placera[3]=värde;}
static void Stäng(void){if(peer_värde>=0)Stäng_nätverk(peer_värde);peer_värde=-1;scen_värde=0;indata_ANTAL=utleverans_ANTAL=보낸수=0;ikon_ANTAL=ikon_placera=0;닫을예정=0;starta_fjärr_Nyckel_pennstreck();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned nummer){memcpy(utmatningsposition,data,nummer);utleverans_ANTAL=nummer;보낸수=0;}
static void använda_värde_84aa75c8(unsigned nummer){indata_ANTAL-=nummer;memmove(indata_värde,indata_värde+nummer,indata_ANTAL);}
int kontroll_fjärr_visa(unsigned Åtgärd){
    if(Åtgärd==0){Stäng();if(Lyssnar_deltagare>=0)Stäng_nätverk(Lyssnar_deltagare);Lyssnar_deltagare=-1;return 0;}
    if(Åtgärd!=1)return Lyssnar_deltagare>=0;
    if(Lyssnar_deltagare>=0)return 0;
    int port_värde=Skapa_socket_deltagare(1);if(port_värde<0)return port_värde;통신주소재사용(port_värde);
    int RESULTAT=NET_BIND(port_värde,0,5900);if(!RESULTAT)RESULTAT=NET_lyssna(port_värde);
    if(RESULTAT<0){Stäng_nätverk(port_värde);return RESULTAT;}Lyssnar_deltagare=port_värde;return 0;
}
static uint32_t ikon_sammanfattning(unsigned 가로,unsigned bransch_placera){
    uint32_t värde=2166136261u;
    for(unsigned Y_koordinat=bransch_placera;Y_koordinat<bransch_placera+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned x_koordinat=가로;x_koordinat<가로+32&&x_koordinat<너비;x_koordinat++)värde=(värde^Tavla_läsa_skärmbild(x_koordinat,Y_koordinat))*16777619u;
    return värde;
}
static void skärmbild_begäran(const unsigned char *data_placera){
    begärd_X=läsa_16(data_placera+2);begärd_Y=läsa_16(data_placera+4);요청폭=läsa_16(data_placera+6);요청높이=läsa_16(data_placera+8);
    if(begärd_X>=너비||begärd_Y>=높이)요청폭=요청높이=0;
    if(요청폭>너비-begärd_X&&begärd_X<너비)요청폭=너비-begärd_X;
    if(요청높이>높이-begärd_Y&&begärd_Y<높이)요청높이=높이-begärd_Y;
    ikon_ANTAL=ikon_placera=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=begärd_Y/16;Y_koordinat<=(begärd_Y+요청높이-1)/16;Y_koordinat++)for(unsigned x_koordinat=begärd_X/32;x_koordinat<=(begärd_X+요청폭-1)/32;x_koordinat++){
        unsigned positionsindex=Y_koordinat*60+x_koordinat;uint32_t sammanfattning_värde=ikon_sammanfattning(x_koordinat*32,Y_koordinat*16);
        if(!data_placera[1]||Föregående_sammanfattning[positionsindex]!=sammanfattning_värde)바뀐타일[ikon_ANTAL++]=positionsindex;
    }
    utmatningsposition[0]=utmatningsposition[1]=0;skriva_16(utmatningsposition+2,ikon_ANTAL);utleverans_ANTAL=4;보낸수=0;
}
static void skicka_ikon(void){
    unsigned positionsindex=바뀐타일[ikon_placera++],가로=(positionsindex%60)*32,bransch_placera=(positionsindex/60)*16;
    unsigned avsluta_X=가로+32,avsluta_Y=bransch_placera+16;if(avsluta_X>너비)avsluta_X=너비;if(avsluta_Y>높이)avsluta_Y=높이;
    /* 부분 타일 begäran 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=begärd_X&&bransch_placera>=begärd_Y&&avsluta_X<=begärd_X+요청폭&&avsluta_Y<=begärd_Y+요청높이;
    if(전부)Föregående_sammanfattning[positionsindex]=ikon_sammanfattning(가로,bransch_placera);
    if(가로<begärd_X)가로=begärd_X;if(bransch_placera<begärd_Y)bransch_placera=begärd_Y;
    if(avsluta_X>begärd_X+요청폭)avsluta_X=begärd_X+요청폭;if(avsluta_Y>begärd_Y+요청높이)avsluta_Y=begärd_Y+요청높이;
    skriva_16(utmatningsposition,가로);skriva_16(utmatningsposition+2,bransch_placera);skriva_16(utmatningsposition+4,avsluta_X-가로);skriva_16(utmatningsposition+6,avsluta_Y-bransch_placera);skriva_32(utmatningsposition+8,0);
    utleverans_ANTAL=12;보낸수=0;
    for(unsigned Y_koordinat=bransch_placera;Y_koordinat<avsluta_Y;Y_koordinat++)for(unsigned x_koordinat=가로;x_koordinat<avsluta_X;x_koordinat++){
        uint32_t 색=Tavla_läsa_skärmbild(x_koordinat,Y_koordinat),värde=(((색>>16)&255)*빨강최대/255)<<röd_skifta|
            (((색>>8)&255)*초록최대/255)<<grön_skifta|((색&255)*파랑최대/255)<<blå_skifta;
        for(unsigned 순번=0;순번<bildpunkt_storlek;순번++)utmatningsposition[utleverans_ANTAL++]=värde>>(8*(big_endian_värde?bildpunkt_storlek-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Lyssnar_deltagare<0)return;
    if(peer_värde<0){if(보드밀리초()<다시받을때)return;peer_värde=NET_acceptera(Lyssnar_deltagare);if(peer_värde<0)return;
        kontakt_tid=보드밀리초();scen_värde=1;내보내기("RFB 003.008\n",12);memset(Föregående_sammanfattning,0,sizeof(Föregående_sammanfattning));
        bildpunkt_storlek=4;big_endian_värde=0;빨강최대=초록최대=파랑최대=255;röd_skifta=16;grön_skifta=8;blå_skifta=0;}
    if(scen_värde<5&&보드밀리초()-kontakt_tid>15000){Stäng();return;}
    if(utleverans_ANTAL){int nummer=NET_skriva(peer_värde,utmatningsposition+보낸수,utleverans_ANTAL-보낸수);if(nummer>0){보낸수+=nummer;if(보낸수==utleverans_ANTAL)utleverans_ANTAL=보낸수=0;}else if(nummer!=-11){Stäng();return;}}
    if(!utleverans_ANTAL&&닫을예정){Stäng();return;}
    if(!utleverans_ANTAL&&ikon_placera<ikon_ANTAL)skicka_ikon();
    if(indata_ANTAL==sizeof(indata_värde)){Stäng();return;}
    int BELOPP_ANTAL=NET_läsa(peer_värde,indata_värde+indata_ANTAL,sizeof(indata_värde)-indata_ANTAL);
    if(BELOPP_ANTAL==0||(BELOPP_ANTAL<0&&BELOPP_ANTAL!=-11)){Stäng();return;}if(BELOPP_ANTAL>0)indata_ANTAL+=BELOPP_ANTAL;
    if(utleverans_ANTAL||ikon_placera<ikon_ANTAL)return;
    if(scen_värde==1&&indata_ANTAL>=12){if(memcmp(indata_värde,"RFB 003.008\n",12)){Stäng();return;}använda_värde_84aa75c8(12);const unsigned char autentiseringsmetod[]={1,2};내보내기(autentiseringsmetod,2);scen_värde=2;return;}
    if(scen_värde==2&&indata_ANTAL){if(indata_värde[0]!=2||fjärr_slumpmässig(kontroll_värde_c2a235ad,16)){Stäng();return;}använda_värde_84aa75c8(1);내보내기(kontroll_värde_c2a235ad,16);scen_värde=3;return;}
    if(scen_värde==3&&indata_ANTAL>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys lösenord_värde;
        for(unsigned 순번=0;순번<8;순번++){unsigned värde=skärmbild_lösenord[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(värde&1);värde>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&lösenord_värde,열쇠,8);memcpy(정답,kontroll_värde_c2a235ad,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_värde[8]={0};br_des_ct_cbcenc_run(&lösenord_värde,vektor_värde,정답+순번,8);memset(vektor_värde,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^indata_värde[순번];använda_värde_84aa75c8(16);memset(&lösenord_värde,0,sizeof(lösenord_värde));memset(열쇠,0,8);memset(정답,0,16);memset(kontroll_värde_c2a235ad,0,16);
        skriva_32(utmatningsposition,차이?1:0);utleverans_ANTAL=4;보낸수=0;
        if(차이){skriva_32(utmatningsposition+4,19);memcpy(utmatningsposition+8,"Authentication fail",19);utleverans_ANTAL=27;닫을예정=1;}else scen_värde=4;return;}
    if(scen_värde==4&&indata_ANTAL){använda_värde_84aa75c8(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Stäng();return;}
        if(!Tavla_Terminal(7)){const unsigned char Händelse[]={30,2,1,0,0,0,0};feed_fjärr_indata(Händelse,7);}
        memset(utmatningsposition,0,40);skriva_16(utmatningsposition,너비);skriva_16(utmatningsposition+2,높이);utmatningsposition[4]=32;utmatningsposition[5]=24;utmatningsposition[7]=1;
        skriva_16(utmatningsposition+8,255);skriva_16(utmatningsposition+10,255);skriva_16(utmatningsposition+12,255);utmatningsposition[14]=16;utmatningsposition[15]=8;
        const char *Namn="jkoros native";skriva_32(utmatningsposition+20,strlen(Namn));memcpy(utmatningsposition+24,Namn,strlen(Namn));utleverans_ANTAL=24+strlen(Namn);보낸수=0;scen_värde=5;return;}
    if(scen_värde!=5||!indata_ANTAL)return;
    unsigned Typ_område=indata_värde[0],필요=Typ_område==0?20:Typ_område==2?4:Typ_område==3?10:Typ_område==4?8:Typ_område==5?6:Typ_område==6?8:0;
    if(!필요){Stäng();return;}if(indata_ANTAL<필요)return;
    if(Typ_område==2){unsigned nummer=läsa_16(indata_värde+2);if(nummer>128){Stäng();return;}필요+=nummer*4;}
    if(Typ_område==6){unsigned nummer=läsa_32(indata_värde+4);if(nummer>4096){Stäng();return;}필요+=nummer;}
    if(indata_ANTAL<필요)return;
    if(Typ_område==0){unsigned bit_värde=indata_värde[4],빨=läsa_16(indata_värde+8),초=läsa_16(indata_värde+10),파=läsa_16(indata_värde+12),röd_Kanal_skifta=indata_värde[14],grön_Kanal_skifta=indata_värde[15],blå_Kanal_skifta=indata_värde[16];
        if((bit_värde!=16&&bit_värde!=32)||!indata_värde[7]||indata_värde[6]>1||!빨||!초||!파||빨>255||초>255||파>255||röd_Kanal_skifta>24||grön_Kanal_skifta>24||blå_Kanal_skifta>24||
           ((uint64_t)빨<<röd_Kanal_skifta)>((1ull<<bit_värde)-1)||((uint64_t)초<<grön_Kanal_skifta)>((1ull<<bit_värde)-1)||((uint64_t)파<<blå_Kanal_skifta)>((1ull<<bit_värde)-1)){Stäng();return;}
        bildpunkt_storlek=bit_värde/8;big_endian_värde=indata_värde[6];빨강최대=빨;초록최대=초;파랑최대=파;röd_skifta=röd_Kanal_skifta;grön_skifta=grön_Kanal_skifta;blå_skifta=blå_Kanal_skifta;memset(Föregående_sammanfattning,0,sizeof(Föregående_sammanfattning));
    }else if(Typ_område==3)skärmbild_begäran(indata_värde);
    else if(Typ_område==4)fjärr_Nyckel_pennstreck(läsa_32(indata_värde+4),indata_värde[1]!=0);
    else if(Typ_område==5){unsigned x_koordinat=läsa_16(indata_värde+2),Y_koordinat=läsa_16(indata_värde+4);if(x_koordinat>=너비)x_koordinat=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(indata_värde[1])incheckning_fjärr_Nyckel();
        unsigned char Händelse[]={30,1,indata_värde[1],x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8};feed_fjärr_indata(Händelse,sizeof(Händelse));}
    använda_värde_84aa75c8(필요);
}
