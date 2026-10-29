/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Yhdistä, 제한된 syöte_ARVO kesto_ARVO, 비동기 lähettää_ARVO, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "etä_ARVO.h"
#include "salaus_Tuki.h"
#include "Profiili.h"
#include "../verkko_Pino/verkko_Pino.h"
#include "../kone/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Taulu_Pääte(uintptr_t);
void etä_Avain_kynänpiirto(unsigned,int);
void alustaa_etä_Avain_kynänpiirto(void);
void vahvistaa_muutokset_etä_Avain(void);
static int Kuuntelee_päätepiste=-1,vertaissolmu_ARVO=-1,vaihe_ARVO,닫을예정;
static uintptr_t yhteys_AIKA,다시받을때;
static unsigned char syöte_ARVO[8192],tulostuspaikka[4096],haaste_ARVO[16];
static unsigned syöte_LASKE,tulos_LASKE,보낸수;
static unsigned 너비,높이,kuvapiste_muuttaa_kokoa=4,big_endian_ARVO,빨강최대=255,초록최대=255,파랑최대=255,punainen_siirrä=16,vihreä_siirrä=8,sininen_siirrä;
static uint32_t Edellinen_yhteenveto[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned ruutu_LASKE,ruutu_toimi,pyydetty_X,pyydetty_Y,요청폭,요청높이;
static unsigned lukea_16(const unsigned char *data_toimi){return(unsigned)data_toimi[0]*256+data_toimi[1];}
static uint32_t lukea_32(const unsigned char *data_toimi){return(uint32_t)data_toimi[0]<<24|(uint32_t)data_toimi[1]<<16|(uint32_t)data_toimi[2]<<8|data_toimi[3];}
static void kirjoitus_16(unsigned char *data_toimi,unsigned ARVO){data_toimi[0]=ARVO>>8;data_toimi[1]=ARVO;}
static void kirjoitus_32(unsigned char *data_toimi,uint32_t ARVO){data_toimi[0]=ARVO>>24;data_toimi[1]=ARVO>>16;data_toimi[2]=ARVO>>8;data_toimi[3]=ARVO;}
static void Sulje(void){if(vertaissolmu_ARVO>=0)Sulje_verkko(vertaissolmu_ARVO);vertaissolmu_ARVO=-1;vaihe_ARVO=0;syöte_LASKE=tulos_LASKE=보낸수=0;ruutu_LASKE=ruutu_toimi=0;닫을예정=0;alustaa_etä_Avain_kynänpiirto();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *data,unsigned numero){memcpy(tulostuspaikka,data,numero);tulos_LASKE=numero;보낸수=0;}
static void käyttää_ARVO(unsigned numero){syöte_LASKE-=numero;memmove(syöte_ARVO,syöte_ARVO+numero,syöte_LASKE);}
int ohjain_etä_näyttö(unsigned Toiminto){
    if(Toiminto==0){Sulje();if(Kuuntelee_päätepiste>=0)Sulje_verkko(Kuuntelee_päätepiste);Kuuntelee_päätepiste=-1;return 0;}
    if(Toiminto!=1)return Kuuntelee_päätepiste>=0;
    if(Kuuntelee_päätepiste>=0)return 0;
    int portti_ARVO=Luo_vastake_päätepiste(1);if(portti_ARVO<0)return portti_ARVO;통신주소재사용(portti_ARVO);
    int TULOS=NET_BIND(portti_ARVO,0,5900);if(!TULOS)TULOS=NET_kuunnella(portti_ARVO);
    if(TULOS<0){Sulje_verkko(portti_ARVO);return TULOS;}Kuuntelee_päätepiste=portti_ARVO;return 0;
}
static uint32_t ruutu_yhteenveto(unsigned 가로,unsigned toimiala_toimi){
    uint32_t ARVO=2166136261u;
    for(unsigned Y_koordinaatti=toimiala_toimi;Y_koordinaatti<toimiala_toimi+16&&Y_koordinaatti<높이;Y_koordinaatti++)for(unsigned x_koordinaatti=가로;x_koordinaatti<가로+32&&x_koordinaatti<너비;x_koordinaatti++)ARVO=(ARVO^보드화면읽기(x_koordinaatti,Y_koordinaatti))*16777619u;
    return ARVO;
}
static void 화면요청(const unsigned char *data_toimi){
    pyydetty_X=lukea_16(data_toimi+2);pyydetty_Y=lukea_16(data_toimi+4);요청폭=lukea_16(data_toimi+6);요청높이=lukea_16(data_toimi+8);
    if(pyydetty_X>=너비||pyydetty_Y>=높이)요청폭=요청높이=0;
    if(요청폭>너비-pyydetty_X&&pyydetty_X<너비)요청폭=너비-pyydetty_X;
    if(요청높이>높이-pyydetty_Y&&pyydetty_Y<높이)요청높이=높이-pyydetty_Y;
    ruutu_LASKE=ruutu_toimi=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinaatti=pyydetty_Y/16;Y_koordinaatti<=(pyydetty_Y+요청높이-1)/16;Y_koordinaatti++)for(unsigned x_koordinaatti=pyydetty_X/32;x_koordinaatti<=(pyydetty_X+요청폭-1)/32;x_koordinaatti++){
        unsigned sijainti=Y_koordinaatti*60+x_koordinaatti;uint32_t yhteenveto_ARVO=ruutu_yhteenveto(x_koordinaatti*32,Y_koordinaatti*16);
        if(!data_toimi[1]||Edellinen_yhteenveto[sijainti]!=yhteenveto_ARVO)바뀐타일[ruutu_LASKE++]=sijainti;
    }
    tulostuspaikka[0]=tulostuspaikka[1]=0;kirjoitus_16(tulostuspaikka+2,ruutu_LASKE);tulos_LASKE=4;보낸수=0;
}
static void lähettää_ruutu(void){
    unsigned sijainti=바뀐타일[ruutu_toimi++],가로=(sijainti%60)*32,toimiala_toimi=(sijainti/60)*16;
    unsigned lopettaa_puhelu_X=가로+32,lopettaa_puhelu_Y=toimiala_toimi+16;if(lopettaa_puhelu_X>너비)lopettaa_puhelu_X=너비;if(lopettaa_puhelu_Y>높이)lopettaa_puhelu_Y=높이;
    /* 부분 타일 pyyntö 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=pyydetty_X&&toimiala_toimi>=pyydetty_Y&&lopettaa_puhelu_X<=pyydetty_X+요청폭&&lopettaa_puhelu_Y<=pyydetty_Y+요청높이;
    if(전부)Edellinen_yhteenveto[sijainti]=ruutu_yhteenveto(가로,toimiala_toimi);
    if(가로<pyydetty_X)가로=pyydetty_X;if(toimiala_toimi<pyydetty_Y)toimiala_toimi=pyydetty_Y;
    if(lopettaa_puhelu_X>pyydetty_X+요청폭)lopettaa_puhelu_X=pyydetty_X+요청폭;if(lopettaa_puhelu_Y>pyydetty_Y+요청높이)lopettaa_puhelu_Y=pyydetty_Y+요청높이;
    kirjoitus_16(tulostuspaikka,가로);kirjoitus_16(tulostuspaikka+2,toimiala_toimi);kirjoitus_16(tulostuspaikka+4,lopettaa_puhelu_X-가로);kirjoitus_16(tulostuspaikka+6,lopettaa_puhelu_Y-toimiala_toimi);kirjoitus_32(tulostuspaikka+8,0);
    tulos_LASKE=12;보낸수=0;
    for(unsigned Y_koordinaatti=toimiala_toimi;Y_koordinaatti<lopettaa_puhelu_Y;Y_koordinaatti++)for(unsigned x_koordinaatti=가로;x_koordinaatti<lopettaa_puhelu_X;x_koordinaatti++){
        uint32_t 색=보드화면읽기(x_koordinaatti,Y_koordinaatti),ARVO=(((색>>16)&255)*빨강최대/255)<<punainen_siirrä|
            (((색>>8)&255)*초록최대/255)<<vihreä_siirrä|((색&255)*파랑최대/255)<<sininen_siirrä;
        for(unsigned 순번=0;순번<kuvapiste_muuttaa_kokoa;순번++)tulostuspaikka[tulos_LASKE++]=ARVO>>(8*(big_endian_ARVO?kuvapiste_muuttaa_kokoa-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Kuuntelee_päätepiste<0)return;
    if(vertaissolmu_ARVO<0){if(보드밀리초()<다시받을때)return;vertaissolmu_ARVO=NET_hyväksyä(Kuuntelee_päätepiste);if(vertaissolmu_ARVO<0)return;
        yhteys_AIKA=보드밀리초();vaihe_ARVO=1;내보내기("RFB 003.008\n",12);memset(Edellinen_yhteenveto,0,sizeof(Edellinen_yhteenveto));
        kuvapiste_muuttaa_kokoa=4;big_endian_ARVO=0;빨강최대=초록최대=파랑최대=255;punainen_siirrä=16;vihreä_siirrä=8;sininen_siirrä=0;}
    if(vaihe_ARVO<5&&보드밀리초()-yhteys_AIKA>15000){Sulje();return;}
    if(tulos_LASKE){int numero=NET_kirjoitus(vertaissolmu_ARVO,tulostuspaikka+보낸수,tulos_LASKE-보낸수);if(numero>0){보낸수+=numero;if(보낸수==tulos_LASKE)tulos_LASKE=보낸수=0;}else if(numero!=-11){Sulje();return;}}
    if(!tulos_LASKE&&닫을예정){Sulje();return;}
    if(!tulos_LASKE&&ruutu_toimi<ruutu_LASKE)lähettää_ruutu();
    if(syöte_LASKE==sizeof(syöte_ARVO)){Sulje();return;}
    int SAATU_HINTA_LASKE=NET_lukea(vertaissolmu_ARVO,syöte_ARVO+syöte_LASKE,sizeof(syöte_ARVO)-syöte_LASKE);
    if(SAATU_HINTA_LASKE==0||(SAATU_HINTA_LASKE<0&&SAATU_HINTA_LASKE!=-11)){Sulje();return;}if(SAATU_HINTA_LASKE>0)syöte_LASKE+=SAATU_HINTA_LASKE;
    if(tulos_LASKE||ruutu_toimi<ruutu_LASKE)return;
    if(vaihe_ARVO==1&&syöte_LASKE>=12){if(memcmp(syöte_ARVO,"RFB 003.008\n",12)){Sulje();return;}käyttää_ARVO(12);const unsigned char todentamistapa[]={1,2};내보내기(todentamistapa,2);vaihe_ARVO=2;return;}
    if(vaihe_ARVO==2&&syöte_LASKE){if(syöte_ARVO[0]!=2||원격난수(haaste_ARVO,16)){Sulje();return;}käyttää_ARVO(1);내보내기(haaste_ARVO,16);vaihe_ARVO=3;return;}
    if(vaihe_ARVO==3&&syöte_LASKE>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys salasana_ARVO;
        for(unsigned 순번=0;순번<8;순번++){unsigned ARVO=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(ARVO&1);ARVO>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&salasana_ARVO,열쇠,8);memcpy(정답,haaste_ARVO,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektori_ARVO[8]={0};br_des_ct_cbcenc_run(&salasana_ARVO,vektori_ARVO,정답+순번,8);memset(vektori_ARVO,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^syöte_ARVO[순번];käyttää_ARVO(16);memset(&salasana_ARVO,0,sizeof(salasana_ARVO));memset(열쇠,0,8);memset(정답,0,16);memset(haaste_ARVO,0,16);
        kirjoitus_32(tulostuspaikka,차이?1:0);tulos_LASKE=4;보낸수=0;
        if(차이){kirjoitus_32(tulostuspaikka+4,19);memcpy(tulostuspaikka+8,"Authentication fail",19);tulos_LASKE=27;닫을예정=1;}else vaihe_ARVO=4;return;}
    if(vaihe_ARVO==4&&syöte_LASKE){käyttää_ARVO(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Sulje();return;}
        if(!Taulu_Pääte(7)){const unsigned char Tapahtuma[]={30,2,1,0,0,0,0};syöte_etä_syöte(Tapahtuma,7);}
        memset(tulostuspaikka,0,40);kirjoitus_16(tulostuspaikka,너비);kirjoitus_16(tulostuspaikka+2,높이);tulostuspaikka[4]=32;tulostuspaikka[5]=24;tulostuspaikka[7]=1;
        kirjoitus_16(tulostuspaikka+8,255);kirjoitus_16(tulostuspaikka+10,255);kirjoitus_16(tulostuspaikka+12,255);tulostuspaikka[14]=16;tulostuspaikka[15]=8;
        const char *Nimi="jkoros native";kirjoitus_32(tulostuspaikka+20,strlen(Nimi));memcpy(tulostuspaikka+24,Nimi,strlen(Nimi));tulos_LASKE=24+strlen(Nimi);보낸수=0;vaihe_ARVO=5;return;}
    if(vaihe_ARVO!=5||!syöte_LASKE)return;
    unsigned TYYPPI_alue=syöte_ARVO[0],필요=TYYPPI_alue==0?20:TYYPPI_alue==2?4:TYYPPI_alue==3?10:TYYPPI_alue==4?8:TYYPPI_alue==5?6:TYYPPI_alue==6?8:0;
    if(!필요){Sulje();return;}if(syöte_LASKE<필요)return;
    if(TYYPPI_alue==2){unsigned numero=lukea_16(syöte_ARVO+2);if(numero>128){Sulje();return;}필요+=numero*4;}
    if(TYYPPI_alue==6){unsigned numero=lukea_32(syöte_ARVO+4);if(numero>4096){Sulje();return;}필요+=numero;}
    if(syöte_LASKE<필요)return;
    if(TYYPPI_alue==0){unsigned bitti_ARVO=syöte_ARVO[4],빨=lukea_16(syöte_ARVO+8),초=lukea_16(syöte_ARVO+10),파=lukea_16(syöte_ARVO+12),punainen_Media_siirrä=syöte_ARVO[14],vihreä_Media_siirrä=syöte_ARVO[15],sininen_Media_siirrä=syöte_ARVO[16];
        if((bitti_ARVO!=16&&bitti_ARVO!=32)||!syöte_ARVO[7]||syöte_ARVO[6]>1||!빨||!초||!파||빨>255||초>255||파>255||punainen_Media_siirrä>24||vihreä_Media_siirrä>24||sininen_Media_siirrä>24||
           ((uint64_t)빨<<punainen_Media_siirrä)>((1ull<<bitti_ARVO)-1)||((uint64_t)초<<vihreä_Media_siirrä)>((1ull<<bitti_ARVO)-1)||((uint64_t)파<<sininen_Media_siirrä)>((1ull<<bitti_ARVO)-1)){Sulje();return;}
        kuvapiste_muuttaa_kokoa=bitti_ARVO/8;big_endian_ARVO=syöte_ARVO[6];빨강최대=빨;초록최대=초;파랑최대=파;punainen_siirrä=punainen_Media_siirrä;vihreä_siirrä=vihreä_Media_siirrä;sininen_siirrä=sininen_Media_siirrä;memset(Edellinen_yhteenveto,0,sizeof(Edellinen_yhteenveto));
    }else if(TYYPPI_alue==3)화면요청(syöte_ARVO);
    else if(TYYPPI_alue==4)etä_Avain_kynänpiirto(lukea_32(syöte_ARVO+4),syöte_ARVO[1]!=0);
    else if(TYYPPI_alue==5){unsigned x_koordinaatti=lukea_16(syöte_ARVO+2),Y_koordinaatti=lukea_16(syöte_ARVO+4);if(x_koordinaatti>=너비)x_koordinaatti=너비-1;if(Y_koordinaatti>=높이)Y_koordinaatti=높이-1;
        if(syöte_ARVO[1])vahvistaa_muutokset_etä_Avain();
        unsigned char Tapahtuma[]={30,1,syöte_ARVO[1],x_koordinaatti&255,x_koordinaatti>>8,Y_koordinaatti&255,Y_koordinaatti>>8};syöte_etä_syöte(Tapahtuma,sizeof(Tapahtuma));}
    käyttää_ARVO(필요);
}
