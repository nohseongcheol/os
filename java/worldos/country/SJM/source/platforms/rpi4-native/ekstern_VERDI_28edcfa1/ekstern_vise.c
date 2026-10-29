/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Koble_til, 제한된 inndata_VERDI lengde_VERDI, 비동기 sende_VERDI_f993dacd, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 skjermbilde data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "ekstern_VERDI_28edcfa1.h"
#include "kryptografi_støtte.h"
#include "Profil.h"
#include "../nettverk_stakk/nettverk_stakk.h"
#include "../maskin/skjermbilde_info.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(skjermbilde_passord)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tavle_Terminal(uintptr_t);
void ekstern_tast_pennestrøk(unsigned,int);
void starte_ekstern_tast_pennestrøk(void);
void 원격글쇠확정(void);
static int Lytter_deltaker=-1,node_VERDI_6a3b6fa7=-1,fase_VERDI,닫을예정;
static uintptr_t kontakt_TID,다시받을때;
static unsigned char inndata_VERDI[8192],Utgang[4096],utfordring_VERDI[16];
static unsigned inndata_ANTALL,produksjon_ANTALL,보낸수;
static unsigned 너비,높이,piksel_skalere=4,big_endian_VERDI,빨강최대=255,초록최대=255,파랑최대=255,rød_flytte=16,grønn_flytte=8,blå_flytte;
static uint32_t Forrige_sammendrag[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned flis_ANTALL,flis_plassere,ønsket_X,ønsket_Y,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_plassere){return(unsigned)data_plassere[0]*256+data_plassere[1];}
static uint32_t 읽기32(const unsigned char *data_plassere){return(uint32_t)data_plassere[0]<<24|(uint32_t)data_plassere[1]<<16|(uint32_t)data_plassere[2]<<8|data_plassere[3];}
static void skrive_16(unsigned char *data_plassere,unsigned VERDI){data_plassere[0]=VERDI>>8;data_plassere[1]=VERDI;}
static void skrive_32(unsigned char *data_plassere,uint32_t VERDI){data_plassere[0]=VERDI>>24;data_plassere[1]=VERDI>>16;data_plassere[2]=VERDI>>8;data_plassere[3]=VERDI;}
static void Lukk(void){if(node_VERDI_6a3b6fa7>=0)Lukk_nettverk(node_VERDI_6a3b6fa7);node_VERDI_6a3b6fa7=-1;fase_VERDI=0;inndata_ANTALL=produksjon_ANTALL=보낸수=0;flis_ANTALL=flis_plassere=0;닫을예정=0;starte_ekstern_tast_pennestrøk();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned nummer){memcpy(Utgang,data,nummer);produksjon_ANTALL=nummer;보낸수=0;}
static void bruke_VERDI(unsigned nummer){inndata_ANTALL-=nummer;memmove(inndata_VERDI,inndata_VERDI+nummer,inndata_ANTALL);}
int kontroll_ekstern_vise(unsigned Handling){
    if(Handling==0){Lukk();if(Lytter_deltaker>=0)Lukk_nettverk(Lytter_deltaker);Lytter_deltaker=-1;return 0;}
    if(Handling!=1)return Lytter_deltaker>=0;
    if(Lytter_deltaker>=0)return 0;
    int port_VERDI=åpne_socket_deltaker(1);if(port_VERDI<0)return port_VERDI;통신주소재사용(port_VERDI);
    int KR=netto_BIND(port_VERDI,0,5900);if(!KR)KR=연결기다리기(port_VERDI);
    if(KR<0){Lukk_nettverk(port_VERDI);return KR;}Lytter_deltaker=port_VERDI;return 0;
}
static uint32_t flis_sammendrag(unsigned 가로,unsigned vertikal_plassere){
    uint32_t VERDI=2166136261u;
    for(unsigned Y_koordinat=vertikal_plassere;Y_koordinat<vertikal_plassere+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned x_koordinat=가로;x_koordinat<가로+32&&x_koordinat<너비;x_koordinat++)VERDI=(VERDI^보드화면읽기(x_koordinat,Y_koordinat))*16777619u;
    return VERDI;
}
static void skjermbilde_forespørsel(const unsigned char *data_plassere){
    ønsket_X=읽기16(data_plassere+2);ønsket_Y=읽기16(data_plassere+4);요청폭=읽기16(data_plassere+6);요청높이=읽기16(data_plassere+8);
    if(ønsket_X>=너비||ønsket_Y>=높이)요청폭=요청높이=0;
    if(요청폭>너비-ønsket_X&&ønsket_X<너비)요청폭=너비-ønsket_X;
    if(요청높이>높이-ønsket_Y&&ønsket_Y<높이)요청높이=높이-ønsket_Y;
    flis_ANTALL=flis_plassere=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=ønsket_Y/16;Y_koordinat<=(ønsket_Y+요청높이-1)/16;Y_koordinat++)for(unsigned x_koordinat=ønsket_X/32;x_koordinat<=(ønsket_X+요청폭-1)/32;x_koordinat++){
        unsigned posisjonsindeks=Y_koordinat*60+x_koordinat;uint32_t sammendrag_VERDI=flis_sammendrag(x_koordinat*32,Y_koordinat*16);
        if(!data_plassere[1]||Forrige_sammendrag[posisjonsindeks]!=sammendrag_VERDI)바뀐타일[flis_ANTALL++]=posisjonsindeks;
    }
    Utgang[0]=Utgang[1]=0;skrive_16(Utgang+2,flis_ANTALL);produksjon_ANTALL=4;보낸수=0;
}
static void sende_flis(void){
    unsigned posisjonsindeks=바뀐타일[flis_plassere++],가로=(posisjonsindeks%60)*32,vertikal_plassere=(posisjonsindeks/60)*16;
    unsigned avslutte_en_samtale_X=가로+32,avslutte_en_samtale_Y=vertikal_plassere+16;if(avslutte_en_samtale_X>너비)avslutte_en_samtale_X=너비;if(avslutte_en_samtale_Y>높이)avslutte_en_samtale_Y=높이;
    /* 부분 타일 forespørsel 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=ønsket_X&&vertikal_plassere>=ønsket_Y&&avslutte_en_samtale_X<=ønsket_X+요청폭&&avslutte_en_samtale_Y<=ønsket_Y+요청높이;
    if(전부)Forrige_sammendrag[posisjonsindeks]=flis_sammendrag(가로,vertikal_plassere);
    if(가로<ønsket_X)가로=ønsket_X;if(vertikal_plassere<ønsket_Y)vertikal_plassere=ønsket_Y;
    if(avslutte_en_samtale_X>ønsket_X+요청폭)avslutte_en_samtale_X=ønsket_X+요청폭;if(avslutte_en_samtale_Y>ønsket_Y+요청높이)avslutte_en_samtale_Y=ønsket_Y+요청높이;
    skrive_16(Utgang,가로);skrive_16(Utgang+2,vertikal_plassere);skrive_16(Utgang+4,avslutte_en_samtale_X-가로);skrive_16(Utgang+6,avslutte_en_samtale_Y-vertikal_plassere);skrive_32(Utgang+8,0);
    produksjon_ANTALL=12;보낸수=0;
    for(unsigned Y_koordinat=vertikal_plassere;Y_koordinat<avslutte_en_samtale_Y;Y_koordinat++)for(unsigned x_koordinat=가로;x_koordinat<avslutte_en_samtale_X;x_koordinat++){
        uint32_t 색=보드화면읽기(x_koordinat,Y_koordinat),VERDI=(((색>>16)&255)*빨강최대/255)<<rød_flytte|
            (((색>>8)&255)*초록최대/255)<<grønn_flytte|((색&255)*파랑최대/255)<<blå_flytte;
        for(unsigned 순번=0;순번<piksel_skalere;순번++)Utgang[produksjon_ANTALL++]=VERDI>>(8*(big_endian_VERDI?piksel_skalere-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Lytter_deltaker<0)return;
    if(node_VERDI_6a3b6fa7<0){if(보드밀리초()<다시받을때)return;node_VERDI_6a3b6fa7=netto_godta(Lytter_deltaker);if(node_VERDI_6a3b6fa7<0)return;
        kontakt_TID=보드밀리초();fase_VERDI=1;내보내기("RFB 003.008\n",12);memset(Forrige_sammendrag,0,sizeof(Forrige_sammendrag));
        piksel_skalere=4;big_endian_VERDI=0;빨강최대=초록최대=파랑최대=255;rød_flytte=16;grønn_flytte=8;blå_flytte=0;}
    if(fase_VERDI<5&&보드밀리초()-kontakt_TID>15000){Lukk();return;}
    if(produksjon_ANTALL){int nummer=netto_skrive(node_VERDI_6a3b6fa7,Utgang+보낸수,produksjon_ANTALL-보낸수);if(nummer>0){보낸수+=nummer;if(보낸수==produksjon_ANTALL)produksjon_ANTALL=보낸수=0;}else if(nummer!=-11){Lukk();return;}}
    if(!produksjon_ANTALL&&닫을예정){Lukk();return;}
    if(!produksjon_ANTALL&&flis_plassere<flis_ANTALL)sende_flis();
    if(inndata_ANTALL==sizeof(inndata_VERDI)){Lukk();return;}
    int MOTTATT_AVKAST_ANTALL=통신읽기(node_VERDI_6a3b6fa7,inndata_VERDI+inndata_ANTALL,sizeof(inndata_VERDI)-inndata_ANTALL);
    if(MOTTATT_AVKAST_ANTALL==0||(MOTTATT_AVKAST_ANTALL<0&&MOTTATT_AVKAST_ANTALL!=-11)){Lukk();return;}if(MOTTATT_AVKAST_ANTALL>0)inndata_ANTALL+=MOTTATT_AVKAST_ANTALL;
    if(produksjon_ANTALL||flis_plassere<flis_ANTALL)return;
    if(fase_VERDI==1&&inndata_ANTALL>=12){if(memcmp(inndata_VERDI,"RFB 003.008\n",12)){Lukk();return;}bruke_VERDI(12);const unsigned char godkjenningsmetode[]={1,2};내보내기(godkjenningsmetode,2);fase_VERDI=2;return;}
    if(fase_VERDI==2&&inndata_ANTALL){if(inndata_VERDI[0]!=2||원격난수(utfordring_VERDI,16)){Lukk();return;}bruke_VERDI(1);내보내기(utfordring_VERDI,16);fase_VERDI=3;return;}
    if(fase_VERDI==3&&inndata_ANTALL>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys passord_VERDI;
        for(unsigned 순번=0;순번<8;순번++){unsigned VERDI=skjermbilde_passord[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VERDI&1);VERDI>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&passord_VERDI,열쇠,8);memcpy(정답,utfordring_VERDI,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VERDI[8]={0};br_des_ct_cbcenc_run(&passord_VERDI,vektor_VERDI,정답+순번,8);memset(vektor_VERDI,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^inndata_VERDI[순번];bruke_VERDI(16);memset(&passord_VERDI,0,sizeof(passord_VERDI));memset(열쇠,0,8);memset(정답,0,16);memset(utfordring_VERDI,0,16);
        skrive_32(Utgang,차이?1:0);produksjon_ANTALL=4;보낸수=0;
        if(차이){skrive_32(Utgang+4,19);memcpy(Utgang+8,"Authentication fail",19);produksjon_ANTALL=27;닫을예정=1;}else fase_VERDI=4;return;}
    if(fase_VERDI==4&&inndata_ANTALL){bruke_VERDI(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Lukk();return;}
        if(!Tavle_Terminal(7)){const unsigned char Hendelse[]={30,2,1,0,0,0,0};feed_ekstern_inndata(Hendelse,7);}
        memset(Utgang,0,40);skrive_16(Utgang,너비);skrive_16(Utgang+2,높이);Utgang[4]=32;Utgang[5]=24;Utgang[7]=1;
        skrive_16(Utgang+8,255);skrive_16(Utgang+10,255);skrive_16(Utgang+12,255);Utgang[14]=16;Utgang[15]=8;
        const char *Navn="jkoros native";skrive_32(Utgang+20,strlen(Navn));memcpy(Utgang+24,Navn,strlen(Navn));produksjon_ANTALL=24+strlen(Navn);보낸수=0;fase_VERDI=5;return;}
    if(fase_VERDI!=5||!inndata_ANTALL)return;
    unsigned Type_område=inndata_VERDI[0],필요=Type_område==0?20:Type_område==2?4:Type_område==3?10:Type_område==4?8:Type_område==5?6:Type_område==6?8:0;
    if(!필요){Lukk();return;}if(inndata_ANTALL<필요)return;
    if(Type_område==2){unsigned nummer=읽기16(inndata_VERDI+2);if(nummer>128){Lukk();return;}필요+=nummer*4;}
    if(Type_område==6){unsigned nummer=읽기32(inndata_VERDI+4);if(nummer>4096){Lukk();return;}필요+=nummer;}
    if(inndata_ANTALL<필요)return;
    if(Type_område==0){unsigned bit_VERDI=inndata_VERDI[4],빨=읽기16(inndata_VERDI+8),초=읽기16(inndata_VERDI+10),파=읽기16(inndata_VERDI+12),rød_Kanal_flytte=inndata_VERDI[14],grønn_Kanal_flytte=inndata_VERDI[15],blå_Kanal_flytte=inndata_VERDI[16];
        if((bit_VERDI!=16&&bit_VERDI!=32)||!inndata_VERDI[7]||inndata_VERDI[6]>1||!빨||!초||!파||빨>255||초>255||파>255||rød_Kanal_flytte>24||grønn_Kanal_flytte>24||blå_Kanal_flytte>24||
           ((uint64_t)빨<<rød_Kanal_flytte)>((1ull<<bit_VERDI)-1)||((uint64_t)초<<grønn_Kanal_flytte)>((1ull<<bit_VERDI)-1)||((uint64_t)파<<blå_Kanal_flytte)>((1ull<<bit_VERDI)-1)){Lukk();return;}
        piksel_skalere=bit_VERDI/8;big_endian_VERDI=inndata_VERDI[6];빨강최대=빨;초록최대=초;파랑최대=파;rød_flytte=rød_Kanal_flytte;grønn_flytte=grønn_Kanal_flytte;blå_flytte=blå_Kanal_flytte;memset(Forrige_sammendrag,0,sizeof(Forrige_sammendrag));
    }else if(Type_område==3)skjermbilde_forespørsel(inndata_VERDI);
    else if(Type_område==4)ekstern_tast_pennestrøk(읽기32(inndata_VERDI+4),inndata_VERDI[1]!=0);
    else if(Type_område==5){unsigned x_koordinat=읽기16(inndata_VERDI+2),Y_koordinat=읽기16(inndata_VERDI+4);if(x_koordinat>=너비)x_koordinat=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(inndata_VERDI[1])원격글쇠확정();
        unsigned char Hendelse[]={30,1,inndata_VERDI[1],x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8};feed_ekstern_inndata(Hendelse,sizeof(Hendelse));}
    bruke_VERDI(필요);
}
