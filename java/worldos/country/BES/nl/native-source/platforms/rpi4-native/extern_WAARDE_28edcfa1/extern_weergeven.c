/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Verbinden, 제한된 invoer_WAARDE tijdsduur_WAARDE, 비동기 e_mailen_WAARDE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 scherm gegevens 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "extern_WAARDE_28edcfa1.h"
#include "cryptografie_steun.h"
#include "Profiel.h"
#include "../net_stack/net_stack.h"
#include "../machine/scherm_info.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(scherm_wachtwoord)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Bord_Terminal(uintptr_t);
void extern_toets_kwaststreek(unsigned,int);
void initialiseren_extern_toets_kwaststreek(void);
void doorvoeren_extern_toets(void);
static int Luisteren_eindpunt=-1,peer_WAARDE=-1,fase_WAARDE,닫을예정;
static uintptr_t verbinding_TIJD,다시받을때;
static unsigned char invoer_WAARDE[8192],tekstuitvoer[4096],vraag_WAARDE[16];
static unsigned invoer_AANTAL,uitvoer_AANTAL,보낸수;
static unsigned 너비,hoogte_WAARDE,pixel_formaat_wijzigen=4,big_endian_WAARDE,빨강최대=255,초록최대=255,파랑최대=255,rood_verplaatsen=16,groen_verplaatsen=8,blauw_verplaatsen;
static uint32_t Vorige_samenvatting[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned deel_AANTAL,deel_functie,aangevraagd_X,aangevraagd_Y,요청폭,aangevraagd_hoogte;
static unsigned 읽기16(const unsigned char *gegevens_functie){return(unsigned)gegevens_functie[0]*256+gegevens_functie[1];}
static uint32_t 읽기32(const unsigned char *gegevens_functie){return(uint32_t)gegevens_functie[0]<<24|(uint32_t)gegevens_functie[1]<<16|(uint32_t)gegevens_functie[2]<<8|gegevens_functie[3];}
static void schrijven_16(unsigned char *gegevens_functie,unsigned WAARDE){gegevens_functie[0]=WAARDE>>8;gegevens_functie[1]=WAARDE;}
static void schrijven_32(unsigned char *gegevens_functie,uint32_t WAARDE){gegevens_functie[0]=WAARDE>>24;gegevens_functie[1]=WAARDE>>16;gegevens_functie[2]=WAARDE>>8;gegevens_functie[3]=WAARDE;}
static void Sluiten(void){if(peer_WAARDE>=0)Sluiten_net(peer_WAARDE);peer_WAARDE=-1;fase_WAARDE=0;invoer_AANTAL=uitvoer_AANTAL=보낸수=0;deel_AANTAL=deel_functie=0;닫을예정=0;initialiseren_extern_toets_kwaststreek();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *gegevens,unsigned nummer){memcpy(tekstuitvoer,gegevens,nummer);uitvoer_AANTAL=nummer;보낸수=0;}
static void gebruiken_WAARDE(unsigned nummer){invoer_AANTAL-=nummer;memmove(invoer_WAARDE,invoer_WAARDE+nummer,invoer_AANTAL);}
int controle_extern_weergeven(unsigned Actie){
    if(Actie==0){Sluiten();if(Luisteren_eindpunt>=0)Sluiten_net(Luisteren_eindpunt);Luisteren_eindpunt=-1;return 0;}
    if(Actie!=1)return Luisteren_eindpunt>=0;
    if(Luisteren_eindpunt>=0)return 0;
    int poort_WAARDE=maken_socket_eindpunt(1);if(poort_WAARDE<0)return poort_WAARDE;통신주소재사용(poort_WAARDE);
    int resultaat=NET_BIND(poort_WAARDE,0,5900);if(!resultaat)resultaat=연결기다리기(poort_WAARDE);
    if(resultaat<0){Sluiten_net(poort_WAARDE);return resultaat;}Luisteren_eindpunt=poort_WAARDE;return 0;
}
static uint32_t deel_samenvatting(unsigned 가로,unsigned Verticaal_functie){
    uint32_t WAARDE=2166136261u;
    for(unsigned Y_coördinaat=Verticaal_functie;Y_coördinaat<Verticaal_functie+16&&Y_coördinaat<hoogte_WAARDE;Y_coördinaat++)for(unsigned x_coördinaat=가로;x_coördinaat<가로+32&&x_coördinaat<너비;x_coördinaat++)WAARDE=(WAARDE^보드화면읽기(x_coördinaat,Y_coördinaat))*16777619u;
    return WAARDE;
}
static void scherm_aanvraag(const unsigned char *gegevens_functie){
    aangevraagd_X=읽기16(gegevens_functie+2);aangevraagd_Y=읽기16(gegevens_functie+4);요청폭=읽기16(gegevens_functie+6);aangevraagd_hoogte=읽기16(gegevens_functie+8);
    if(aangevraagd_X>=너비||aangevraagd_Y>=hoogte_WAARDE)요청폭=aangevraagd_hoogte=0;
    if(요청폭>너비-aangevraagd_X&&aangevraagd_X<너비)요청폭=너비-aangevraagd_X;
    if(aangevraagd_hoogte>hoogte_WAARDE-aangevraagd_Y&&aangevraagd_Y<hoogte_WAARDE)aangevraagd_hoogte=hoogte_WAARDE-aangevraagd_Y;
    deel_AANTAL=deel_functie=0;
    if(요청폭&&aangevraagd_hoogte)for(unsigned Y_coördinaat=aangevraagd_Y/16;Y_coördinaat<=(aangevraagd_Y+aangevraagd_hoogte-1)/16;Y_coördinaat++)for(unsigned x_coördinaat=aangevraagd_X/32;x_coördinaat<=(aangevraagd_X+요청폭-1)/32;x_coördinaat++){
        unsigned plaatsingsindex=Y_coördinaat*60+x_coördinaat;uint32_t samenvatting_WAARDE=deel_samenvatting(x_coördinaat*32,Y_coördinaat*16);
        if(!gegevens_functie[1]||Vorige_samenvatting[plaatsingsindex]!=samenvatting_WAARDE)바뀐타일[deel_AANTAL++]=plaatsingsindex;
    }
    tekstuitvoer[0]=tekstuitvoer[1]=0;schrijven_16(tekstuitvoer+2,deel_AANTAL);uitvoer_AANTAL=4;보낸수=0;
}
static void e_mailen_deel(void){
    unsigned plaatsingsindex=바뀐타일[deel_functie++],가로=(plaatsingsindex%60)*32,Verticaal_functie=(plaatsingsindex/60)*16;
    unsigned beëindigen_X=가로+32,beëindigen_Y=Verticaal_functie+16;if(beëindigen_X>너비)beëindigen_X=너비;if(beëindigen_Y>hoogte_WAARDE)beëindigen_Y=hoogte_WAARDE;
    /* 부분 타일 aanvraag 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=aangevraagd_X&&Verticaal_functie>=aangevraagd_Y&&beëindigen_X<=aangevraagd_X+요청폭&&beëindigen_Y<=aangevraagd_Y+aangevraagd_hoogte;
    if(전부)Vorige_samenvatting[plaatsingsindex]=deel_samenvatting(가로,Verticaal_functie);
    if(가로<aangevraagd_X)가로=aangevraagd_X;if(Verticaal_functie<aangevraagd_Y)Verticaal_functie=aangevraagd_Y;
    if(beëindigen_X>aangevraagd_X+요청폭)beëindigen_X=aangevraagd_X+요청폭;if(beëindigen_Y>aangevraagd_Y+aangevraagd_hoogte)beëindigen_Y=aangevraagd_Y+aangevraagd_hoogte;
    schrijven_16(tekstuitvoer,가로);schrijven_16(tekstuitvoer+2,Verticaal_functie);schrijven_16(tekstuitvoer+4,beëindigen_X-가로);schrijven_16(tekstuitvoer+6,beëindigen_Y-Verticaal_functie);schrijven_32(tekstuitvoer+8,0);
    uitvoer_AANTAL=12;보낸수=0;
    for(unsigned Y_coördinaat=Verticaal_functie;Y_coördinaat<beëindigen_Y;Y_coördinaat++)for(unsigned x_coördinaat=가로;x_coördinaat<beëindigen_X;x_coördinaat++){
        uint32_t 색=보드화면읽기(x_coördinaat,Y_coördinaat),WAARDE=(((색>>16)&255)*빨강최대/255)<<rood_verplaatsen|
            (((색>>8)&255)*초록최대/255)<<groen_verplaatsen|((색&255)*파랑최대/255)<<blauw_verplaatsen;
        for(unsigned 순번=0;순번<pixel_formaat_wijzigen;순번++)tekstuitvoer[uitvoer_AANTAL++]=WAARDE>>(8*(big_endian_WAARDE?pixel_formaat_wijzigen-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Luisteren_eindpunt<0)return;
    if(peer_WAARDE<0){if(보드밀리초()<다시받을때)return;peer_WAARDE=NET_accepteren(Luisteren_eindpunt);if(peer_WAARDE<0)return;
        verbinding_TIJD=보드밀리초();fase_WAARDE=1;내보내기("RFB 003.008\n",12);memset(Vorige_samenvatting,0,sizeof(Vorige_samenvatting));
        pixel_formaat_wijzigen=4;big_endian_WAARDE=0;빨강최대=초록최대=파랑최대=255;rood_verplaatsen=16;groen_verplaatsen=8;blauw_verplaatsen=0;}
    if(fase_WAARDE<5&&보드밀리초()-verbinding_TIJD>15000){Sluiten();return;}
    if(uitvoer_AANTAL){int nummer=NET_schrijven(peer_WAARDE,tekstuitvoer+보낸수,uitvoer_AANTAL-보낸수);if(nummer>0){보낸수+=nummer;if(보낸수==uitvoer_AANTAL)uitvoer_AANTAL=보낸수=0;}else if(nummer!=-11){Sluiten();return;}}
    if(!uitvoer_AANTAL&&닫을예정){Sluiten();return;}
    if(!uitvoer_AANTAL&&deel_functie<deel_AANTAL)e_mailen_deel();
    if(invoer_AANTAL==sizeof(invoer_WAARDE)){Sluiten();return;}
    int OPBRENGST_AANTAL=통신읽기(peer_WAARDE,invoer_WAARDE+invoer_AANTAL,sizeof(invoer_WAARDE)-invoer_AANTAL);
    if(OPBRENGST_AANTAL==0||(OPBRENGST_AANTAL<0&&OPBRENGST_AANTAL!=-11)){Sluiten();return;}if(OPBRENGST_AANTAL>0)invoer_AANTAL+=OPBRENGST_AANTAL;
    if(uitvoer_AANTAL||deel_functie<deel_AANTAL)return;
    if(fase_WAARDE==1&&invoer_AANTAL>=12){if(memcmp(invoer_WAARDE,"RFB 003.008\n",12)){Sluiten();return;}gebruiken_WAARDE(12);const unsigned char verificatiemethode[]={1,2};내보내기(verificatiemethode,2);fase_WAARDE=2;return;}
    if(fase_WAARDE==2&&invoer_AANTAL){if(invoer_WAARDE[0]!=2||extern_willekeurig(vraag_WAARDE,16)){Sluiten();return;}gebruiken_WAARDE(1);내보내기(vraag_WAARDE,16);fase_WAARDE=3;return;}
    if(fase_WAARDE==3&&invoer_AANTAL>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys wachtwoord_WAARDE;
        for(unsigned 순번=0;순번<8;순번++){unsigned WAARDE=scherm_wachtwoord[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(WAARDE&1);WAARDE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&wachtwoord_WAARDE,열쇠,8);memcpy(정답,vraag_WAARDE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vector_WAARDE[8]={0};br_des_ct_cbcenc_run(&wachtwoord_WAARDE,vector_WAARDE,정답+순번,8);memset(vector_WAARDE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^invoer_WAARDE[순번];gebruiken_WAARDE(16);memset(&wachtwoord_WAARDE,0,sizeof(wachtwoord_WAARDE));memset(열쇠,0,8);memset(정답,0,16);memset(vraag_WAARDE,0,16);
        schrijven_32(tekstuitvoer,차이?1:0);uitvoer_AANTAL=4;보낸수=0;
        if(차이){schrijven_32(tekstuitvoer+4,19);memcpy(tekstuitvoer+8,"Authentication fail",19);uitvoer_AANTAL=27;닫을예정=1;}else fase_WAARDE=4;return;}
    if(fase_WAARDE==4&&invoer_AANTAL){gebruiken_WAARDE(1);너비=보드화면너비();hoogte_WAARDE=Bord_scherm_hoogte();if(!너비||!hoogte_WAARDE||너비>1920||hoogte_WAARDE>1080){Sluiten();return;}
        if(!Bord_Terminal(7)){const unsigned char Gebeurtenis[]={30,2,1,0,0,0,0};feed_extern_invoer(Gebeurtenis,7);}
        memset(tekstuitvoer,0,40);schrijven_16(tekstuitvoer,너비);schrijven_16(tekstuitvoer+2,hoogte_WAARDE);tekstuitvoer[4]=32;tekstuitvoer[5]=24;tekstuitvoer[7]=1;
        schrijven_16(tekstuitvoer+8,255);schrijven_16(tekstuitvoer+10,255);schrijven_16(tekstuitvoer+12,255);tekstuitvoer[14]=16;tekstuitvoer[15]=8;
        const char *Naam="jkoros native";schrijven_32(tekstuitvoer+20,strlen(Naam));memcpy(tekstuitvoer+24,Naam,strlen(Naam));uitvoer_AANTAL=24+strlen(Naam);보낸수=0;fase_WAARDE=5;return;}
    if(fase_WAARDE!=5||!invoer_AANTAL)return;
    unsigned TYPE_gebied=invoer_WAARDE[0],필요=TYPE_gebied==0?20:TYPE_gebied==2?4:TYPE_gebied==3?10:TYPE_gebied==4?8:TYPE_gebied==5?6:TYPE_gebied==6?8:0;
    if(!필요){Sluiten();return;}if(invoer_AANTAL<필요)return;
    if(TYPE_gebied==2){unsigned nummer=읽기16(invoer_WAARDE+2);if(nummer>128){Sluiten();return;}필요+=nummer*4;}
    if(TYPE_gebied==6){unsigned nummer=읽기32(invoer_WAARDE+4);if(nummer>4096){Sluiten();return;}필요+=nummer;}
    if(invoer_AANTAL<필요)return;
    if(TYPE_gebied==0){unsigned bit_WAARDE=invoer_WAARDE[4],빨=읽기16(invoer_WAARDE+8),초=읽기16(invoer_WAARDE+10),파=읽기16(invoer_WAARDE+12),rood_Kanaal_verplaatsen=invoer_WAARDE[14],groen_Kanaal_verplaatsen=invoer_WAARDE[15],blauw_Kanaal_verplaatsen=invoer_WAARDE[16];
        if((bit_WAARDE!=16&&bit_WAARDE!=32)||!invoer_WAARDE[7]||invoer_WAARDE[6]>1||!빨||!초||!파||빨>255||초>255||파>255||rood_Kanaal_verplaatsen>24||groen_Kanaal_verplaatsen>24||blauw_Kanaal_verplaatsen>24||
           ((uint64_t)빨<<rood_Kanaal_verplaatsen)>((1ull<<bit_WAARDE)-1)||((uint64_t)초<<groen_Kanaal_verplaatsen)>((1ull<<bit_WAARDE)-1)||((uint64_t)파<<blauw_Kanaal_verplaatsen)>((1ull<<bit_WAARDE)-1)){Sluiten();return;}
        pixel_formaat_wijzigen=bit_WAARDE/8;big_endian_WAARDE=invoer_WAARDE[6];빨강최대=빨;초록최대=초;파랑최대=파;rood_verplaatsen=rood_Kanaal_verplaatsen;groen_verplaatsen=groen_Kanaal_verplaatsen;blauw_verplaatsen=blauw_Kanaal_verplaatsen;memset(Vorige_samenvatting,0,sizeof(Vorige_samenvatting));
    }else if(TYPE_gebied==3)scherm_aanvraag(invoer_WAARDE);
    else if(TYPE_gebied==4)extern_toets_kwaststreek(읽기32(invoer_WAARDE+4),invoer_WAARDE[1]!=0);
    else if(TYPE_gebied==5){unsigned x_coördinaat=읽기16(invoer_WAARDE+2),Y_coördinaat=읽기16(invoer_WAARDE+4);if(x_coördinaat>=너비)x_coördinaat=너비-1;if(Y_coördinaat>=hoogte_WAARDE)Y_coördinaat=hoogte_WAARDE-1;
        if(invoer_WAARDE[1])doorvoeren_extern_toets();
        unsigned char Gebeurtenis[]={30,1,invoer_WAARDE[1],x_coördinaat&255,x_coördinaat>>8,Y_coördinaat&255,Y_coördinaat>>8};feed_extern_invoer(Gebeurtenis,sizeof(Gebeurtenis));}
    gebruiken_WAARDE(필요);
}
