/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Tilslut, 제한된 input_VÆRDI varighed_VÆRDI, 비동기 maile_VÆRDI, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 skærmbillede data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "fjern_VÆRDI.h"
#include "kryptografi_støtte.h"
#include "Profil.h"
#include "../netværk_Stak/netværk_Stak.h"
#include "../maskine/skærmbillede_info.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(skærmbillede_adgangskode)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tavle_Terminal(uintptr_t);
void fjern_tast_pennestrøg(unsigned,int);
void starte_fjern_tast_pennestrøg(void);
void udføre_fjern_tast(void);
static int Lytter_slutpunkt=-1,peer_VÆRDI=-1,fase_VÆRDI,닫을예정;
static uintptr_t forbindelse_TID,다시받을때;
static unsigned char input_VÆRDI[8192],Udgang[4096],udfordring_VÆRDI[16];
static unsigned input_TÆL,produktoutput_TÆL,보낸수;
static unsigned 너비,높이,pixel_tilpasse_størrelse=4,big_endian_VÆRDI,빨강최대=255,초록최대=255,파랑최대=255,rød_flytte=16,grøn_flytte=8,blå_flytte;
static uint32_t Forrige_resume[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned del_TÆL,del_placere,anmodet_X,anmodet_Y,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *data_placere){return(unsigned)data_placere[0]*256+data_placere[1];}
static uint32_t 읽기32(const unsigned char *data_placere){return(uint32_t)data_placere[0]<<24|(uint32_t)data_placere[1]<<16|(uint32_t)data_placere[2]<<8|data_placere[3];}
static void skrive_16(unsigned char *data_placere,unsigned VÆRDI){data_placere[0]=VÆRDI>>8;data_placere[1]=VÆRDI;}
static void skrive_32(unsigned char *data_placere,uint32_t VÆRDI){data_placere[0]=VÆRDI>>24;data_placere[1]=VÆRDI>>16;data_placere[2]=VÆRDI>>8;data_placere[3]=VÆRDI;}
static void Luk(void){if(peer_VÆRDI>=0)Luk_netværk(peer_VÆRDI);peer_VÆRDI=-1;fase_VÆRDI=0;input_TÆL=produktoutput_TÆL=보낸수=0;del_TÆL=del_placere=0;닫을예정=0;starte_fjern_tast_pennestrøg();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned tal){memcpy(Udgang,data,tal);produktoutput_TÆL=tal;보낸수=0;}
static void bruge_VÆRDI(unsigned tal){input_TÆL-=tal;memmove(input_VÆRDI,input_VÆRDI+tal,input_TÆL);}
int kontrol_fjern_vise(unsigned Handling){
    if(Handling==0){Luk();if(Lytter_slutpunkt>=0)Luk_netværk(Lytter_slutpunkt);Lytter_slutpunkt=-1;return 0;}
    if(Handling!=1)return Lytter_slutpunkt>=0;
    if(Lytter_slutpunkt>=0)return 0;
    int port_VÆRDI=åbne_socket_slutpunkt(1);if(port_VÆRDI<0)return port_VÆRDI;통신주소재사용(port_VÆRDI);
    int KR=NET_BIND(port_VÆRDI,0,5900);if(!KR)KR=NET_lytte(port_VÆRDI);
    if(KR<0){Luk_netværk(port_VÆRDI);return KR;}Lytter_slutpunkt=port_VÆRDI;return 0;
}
static uint32_t del_resume(unsigned 가로,unsigned Lodret_placere){
    uint32_t VÆRDI=2166136261u;
    for(unsigned Y_koordinat=Lodret_placere;Y_koordinat<Lodret_placere+16&&Y_koordinat<높이;Y_koordinat++)for(unsigned X_koordinat=가로;X_koordinat<가로+32&&X_koordinat<너비;X_koordinat++)VÆRDI=(VÆRDI^보드화면읽기(X_koordinat,Y_koordinat))*16777619u;
    return VÆRDI;
}
static void skærmbillede_anmodning(const unsigned char *data_placere){
    anmodet_X=읽기16(data_placere+2);anmodet_Y=읽기16(data_placere+4);요청폭=읽기16(data_placere+6);요청높이=읽기16(data_placere+8);
    if(anmodet_X>=너비||anmodet_Y>=높이)요청폭=요청높이=0;
    if(요청폭>너비-anmodet_X&&anmodet_X<너비)요청폭=너비-anmodet_X;
    if(요청높이>높이-anmodet_Y&&anmodet_Y<높이)요청높이=높이-anmodet_Y;
    del_TÆL=del_placere=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinat=anmodet_Y/16;Y_koordinat<=(anmodet_Y+요청높이-1)/16;Y_koordinat++)for(unsigned X_koordinat=anmodet_X/32;X_koordinat<=(anmodet_X+요청폭-1)/32;X_koordinat++){
        unsigned positionsindeks=Y_koordinat*60+X_koordinat;uint32_t resume_VÆRDI=del_resume(X_koordinat*32,Y_koordinat*16);
        if(!data_placere[1]||Forrige_resume[positionsindeks]!=resume_VÆRDI)바뀐타일[del_TÆL++]=positionsindeks;
    }
    Udgang[0]=Udgang[1]=0;skrive_16(Udgang+2,del_TÆL);produktoutput_TÆL=4;보낸수=0;
}
static void maile_del(void){
    unsigned positionsindeks=바뀐타일[del_placere++],가로=(positionsindeks%60)*32,Lodret_placere=(positionsindeks/60)*16;
    unsigned afslutte_et_opkald_X=가로+32,afslutte_et_opkald_Y=Lodret_placere+16;if(afslutte_et_opkald_X>너비)afslutte_et_opkald_X=너비;if(afslutte_et_opkald_Y>높이)afslutte_et_opkald_Y=높이;
    /* 부분 타일 anmodning 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=anmodet_X&&Lodret_placere>=anmodet_Y&&afslutte_et_opkald_X<=anmodet_X+요청폭&&afslutte_et_opkald_Y<=anmodet_Y+요청높이;
    if(전부)Forrige_resume[positionsindeks]=del_resume(가로,Lodret_placere);
    if(가로<anmodet_X)가로=anmodet_X;if(Lodret_placere<anmodet_Y)Lodret_placere=anmodet_Y;
    if(afslutte_et_opkald_X>anmodet_X+요청폭)afslutte_et_opkald_X=anmodet_X+요청폭;if(afslutte_et_opkald_Y>anmodet_Y+요청높이)afslutte_et_opkald_Y=anmodet_Y+요청높이;
    skrive_16(Udgang,가로);skrive_16(Udgang+2,Lodret_placere);skrive_16(Udgang+4,afslutte_et_opkald_X-가로);skrive_16(Udgang+6,afslutte_et_opkald_Y-Lodret_placere);skrive_32(Udgang+8,0);
    produktoutput_TÆL=12;보낸수=0;
    for(unsigned Y_koordinat=Lodret_placere;Y_koordinat<afslutte_et_opkald_Y;Y_koordinat++)for(unsigned X_koordinat=가로;X_koordinat<afslutte_et_opkald_X;X_koordinat++){
        uint32_t 색=보드화면읽기(X_koordinat,Y_koordinat),VÆRDI=(((색>>16)&255)*빨강최대/255)<<rød_flytte|
            (((색>>8)&255)*초록최대/255)<<grøn_flytte|((색&255)*파랑최대/255)<<blå_flytte;
        for(unsigned 순번=0;순번<pixel_tilpasse_størrelse;순번++)Udgang[produktoutput_TÆL++]=VÆRDI>>(8*(big_endian_VÆRDI?pixel_tilpasse_størrelse-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Lytter_slutpunkt<0)return;
    if(peer_VÆRDI<0){if(보드밀리초()<다시받을때)return;peer_VÆRDI=NET_acceptere(Lytter_slutpunkt);if(peer_VÆRDI<0)return;
        forbindelse_TID=보드밀리초();fase_VÆRDI=1;내보내기("RFB 003.008\n",12);memset(Forrige_resume,0,sizeof(Forrige_resume));
        pixel_tilpasse_størrelse=4;big_endian_VÆRDI=0;빨강최대=초록최대=파랑최대=255;rød_flytte=16;grøn_flytte=8;blå_flytte=0;}
    if(fase_VÆRDI<5&&보드밀리초()-forbindelse_TID>15000){Luk();return;}
    if(produktoutput_TÆL){int tal=NET_skrive(peer_VÆRDI,Udgang+보낸수,produktoutput_TÆL-보낸수);if(tal>0){보낸수+=tal;if(보낸수==produktoutput_TÆL)produktoutput_TÆL=보낸수=0;}else if(tal!=-11){Luk();return;}}
    if(!produktoutput_TÆL&&닫을예정){Luk();return;}
    if(!produktoutput_TÆL&&del_placere<del_TÆL)maile_del();
    if(input_TÆL==sizeof(input_VÆRDI)){Luk();return;}
    int MODTAGET_VED_UDLØB_TÆL=통신읽기(peer_VÆRDI,input_VÆRDI+input_TÆL,sizeof(input_VÆRDI)-input_TÆL);
    if(MODTAGET_VED_UDLØB_TÆL==0||(MODTAGET_VED_UDLØB_TÆL<0&&MODTAGET_VED_UDLØB_TÆL!=-11)){Luk();return;}if(MODTAGET_VED_UDLØB_TÆL>0)input_TÆL+=MODTAGET_VED_UDLØB_TÆL;
    if(produktoutput_TÆL||del_placere<del_TÆL)return;
    if(fase_VÆRDI==1&&input_TÆL>=12){if(memcmp(input_VÆRDI,"RFB 003.008\n",12)){Luk();return;}bruge_VÆRDI(12);const unsigned char godkendelsesmetode[]={1,2};내보내기(godkendelsesmetode,2);fase_VÆRDI=2;return;}
    if(fase_VÆRDI==2&&input_TÆL){if(input_VÆRDI[0]!=2||fjern_vilkårlig(udfordring_VÆRDI,16)){Luk();return;}bruge_VÆRDI(1);내보내기(udfordring_VÆRDI,16);fase_VÆRDI=3;return;}
    if(fase_VÆRDI==3&&input_TÆL>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys adgangskode_VÆRDI;
        for(unsigned 순번=0;순번<8;순번++){unsigned VÆRDI=skærmbillede_adgangskode[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VÆRDI&1);VÆRDI>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&adgangskode_VÆRDI,열쇠,8);memcpy(정답,udfordring_VÆRDI,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VÆRDI[8]={0};br_des_ct_cbcenc_run(&adgangskode_VÆRDI,vektor_VÆRDI,정답+순번,8);memset(vektor_VÆRDI,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^input_VÆRDI[순번];bruge_VÆRDI(16);memset(&adgangskode_VÆRDI,0,sizeof(adgangskode_VÆRDI));memset(열쇠,0,8);memset(정답,0,16);memset(udfordring_VÆRDI,0,16);
        skrive_32(Udgang,차이?1:0);produktoutput_TÆL=4;보낸수=0;
        if(차이){skrive_32(Udgang+4,19);memcpy(Udgang+8,"Authentication fail",19);produktoutput_TÆL=27;닫을예정=1;}else fase_VÆRDI=4;return;}
    if(fase_VÆRDI==4&&input_TÆL){bruge_VÆRDI(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Luk();return;}
        if(!Tavle_Terminal(7)){const unsigned char hændelse[]={30,2,1,0,0,0,0};feed_fjern_input(hændelse,7);}
        memset(Udgang,0,40);skrive_16(Udgang,너비);skrive_16(Udgang+2,높이);Udgang[4]=32;Udgang[5]=24;Udgang[7]=1;
        skrive_16(Udgang+8,255);skrive_16(Udgang+10,255);skrive_16(Udgang+12,255);Udgang[14]=16;Udgang[15]=8;
        const char *Navn="jkoros native";skrive_32(Udgang+20,strlen(Navn));memcpy(Udgang+24,Navn,strlen(Navn));produktoutput_TÆL=24+strlen(Navn);보낸수=0;fase_VÆRDI=5;return;}
    if(fase_VÆRDI!=5||!input_TÆL)return;
    unsigned Type_område=input_VÆRDI[0],필요=Type_område==0?20:Type_område==2?4:Type_område==3?10:Type_område==4?8:Type_område==5?6:Type_område==6?8:0;
    if(!필요){Luk();return;}if(input_TÆL<필요)return;
    if(Type_område==2){unsigned tal=읽기16(input_VÆRDI+2);if(tal>128){Luk();return;}필요+=tal*4;}
    if(Type_område==6){unsigned tal=읽기32(input_VÆRDI+4);if(tal>4096){Luk();return;}필요+=tal;}
    if(input_TÆL<필요)return;
    if(Type_område==0){unsigned bit_VÆRDI=input_VÆRDI[4],빨=읽기16(input_VÆRDI+8),초=읽기16(input_VÆRDI+10),파=읽기16(input_VÆRDI+12),rød_Kanal_flytte=input_VÆRDI[14],grøn_Kanal_flytte=input_VÆRDI[15],blå_Kanal_flytte=input_VÆRDI[16];
        if((bit_VÆRDI!=16&&bit_VÆRDI!=32)||!input_VÆRDI[7]||input_VÆRDI[6]>1||!빨||!초||!파||빨>255||초>255||파>255||rød_Kanal_flytte>24||grøn_Kanal_flytte>24||blå_Kanal_flytte>24||
           ((uint64_t)빨<<rød_Kanal_flytte)>((1ull<<bit_VÆRDI)-1)||((uint64_t)초<<grøn_Kanal_flytte)>((1ull<<bit_VÆRDI)-1)||((uint64_t)파<<blå_Kanal_flytte)>((1ull<<bit_VÆRDI)-1)){Luk();return;}
        pixel_tilpasse_størrelse=bit_VÆRDI/8;big_endian_VÆRDI=input_VÆRDI[6];빨강최대=빨;초록최대=초;파랑최대=파;rød_flytte=rød_Kanal_flytte;grøn_flytte=grøn_Kanal_flytte;blå_flytte=blå_Kanal_flytte;memset(Forrige_resume,0,sizeof(Forrige_resume));
    }else if(Type_område==3)skærmbillede_anmodning(input_VÆRDI);
    else if(Type_område==4)fjern_tast_pennestrøg(읽기32(input_VÆRDI+4),input_VÆRDI[1]!=0);
    else if(Type_område==5){unsigned X_koordinat=읽기16(input_VÆRDI+2),Y_koordinat=읽기16(input_VÆRDI+4);if(X_koordinat>=너비)X_koordinat=너비-1;if(Y_koordinat>=높이)Y_koordinat=높이-1;
        if(input_VÆRDI[1])udføre_fjern_tast();
        unsigned char hændelse[]={30,1,input_VÆRDI[1],X_koordinat&255,X_koordinat>>8,Y_koordinat&255,Y_koordinat>>8};feed_fjern_input(hændelse,sizeof(hændelse));}
    bruge_VÆRDI(필요);
}
