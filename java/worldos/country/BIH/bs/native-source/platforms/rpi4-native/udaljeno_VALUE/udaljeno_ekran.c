/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Spoji_se, 제한된 입력 dužina_VALUE, 비동기 poslati_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 podaci 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "udaljeno_VALUE.h"
#include "암호기반.h"
#include "Profil.h"
#include "../Mreža_snop/Mreža_snop.h"
#include "../mašina/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t ploča_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int 듣는곳=-1,peer_VALUE=-1,faza_VALUE,닫을예정;
static uintptr_t veza_TIME,다시받을때;
static unsigned char 입력[8192],Ispis[4096],test_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,pel_podesiti_veličinu=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned dodatak_COUNT,dodatak_položaj,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *podaci_položaj){return(unsigned)podaci_položaj[0]*256+podaci_položaj[1];}
static uint32_t 읽기32(const unsigned char *podaci_položaj){return(uint32_t)podaci_položaj[0]<<24|(uint32_t)podaci_položaj[1]<<16|(uint32_t)podaci_položaj[2]<<8|podaci_položaj[3];}
static void pisati_16(unsigned char *podaci_položaj,unsigned VALUE){podaci_položaj[0]=VALUE>>8;podaci_položaj[1]=VALUE;}
static void pisati_32(unsigned char *podaci_položaj,uint32_t VALUE){podaci_položaj[0]=VALUE>>24;podaci_položaj[1]=VALUE>>16;podaci_položaj[2]=VALUE>>8;podaci_položaj[3]=VALUE;}
static void Zatvori(void){if(peer_VALUE>=0)zatvoriti_Mreža(peer_VALUE);peer_VALUE=-1;faza_VALUE=0;입력수=출력수=보낸수=0;dodatak_COUNT=dodatak_položaj=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *podaci,unsigned 수){memcpy(Ispis,podaci,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int kontrola_udaljeno_ekran(unsigned radnja){
    if(radnja==0){Zatvori();if(듣는곳>=0)zatvoriti_Mreža(듣는곳);듣는곳=-1;return 0;}
    if(radnja!=1)return 듣는곳>=0;
    if(듣는곳>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int mjera=망주소묶기(port_VALUE,0,5900);if(!mjera)mjera=연결기다리기(port_VALUE);
    if(mjera<0){zatvoriti_Mreža(port_VALUE);return mjera;}듣는곳=port_VALUE;return 0;
}
static uint32_t dodatak_rezime(unsigned 가로,unsigned Vertikalno_položaj){
    uint32_t VALUE=2166136261u;
    for(unsigned Y_koordinata=Vertikalno_položaj;Y_koordinata<Vertikalno_položaj+16&&Y_koordinata<높이;Y_koordinata++)for(unsigned koordinata_x=가로;koordinata_x<가로+32&&koordinata_x<너비;koordinata_x++)VALUE=(VALUE^보드화면읽기(koordinata_x,Y_koordinata))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *podaci_položaj){
    요청가로=읽기16(podaci_položaj+2);요청세로=읽기16(podaci_položaj+4);요청폭=읽기16(podaci_položaj+6);요청높이=읽기16(podaci_položaj+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    dodatak_COUNT=dodatak_položaj=0;
    if(요청폭&&요청높이)for(unsigned Y_koordinata=요청세로/16;Y_koordinata<=(요청세로+요청높이-1)/16;Y_koordinata++)for(unsigned koordinata_x=요청가로/32;koordinata_x<=(요청가로+요청폭-1)/32;koordinata_x++){
        unsigned položaj_INDEX=Y_koordinata*60+koordinata_x;uint32_t rezime_VALUE=dodatak_rezime(koordinata_x*32,Y_koordinata*16);
        if(!podaci_položaj[1]||지난요약[položaj_INDEX]!=rezime_VALUE)바뀐타일[dodatak_COUNT++]=položaj_INDEX;
    }
    Ispis[0]=Ispis[1]=0;pisati_16(Ispis+2,dodatak_COUNT);출력수=4;보낸수=0;
}
static void poslati_dodatak(void){
    unsigned položaj_INDEX=바뀐타일[dodatak_položaj++],가로=(položaj_INDEX%60)*32,Vertikalno_položaj=(položaj_INDEX/60)*16;
    unsigned završiti_X=가로+32,završiti_Y=Vertikalno_položaj+16;if(završiti_X>너비)završiti_X=너비;if(završiti_Y>높이)završiti_Y=높이;
    /* 부분 타일 HTTP_zahtjev 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Vertikalno_položaj>=요청세로&&završiti_X<=요청가로+요청폭&&završiti_Y<=요청세로+요청높이;
    if(전부)지난요약[položaj_INDEX]=dodatak_rezime(가로,Vertikalno_položaj);
    if(가로<요청가로)가로=요청가로;if(Vertikalno_položaj<요청세로)Vertikalno_položaj=요청세로;
    if(završiti_X>요청가로+요청폭)završiti_X=요청가로+요청폭;if(završiti_Y>요청세로+요청높이)završiti_Y=요청세로+요청높이;
    pisati_16(Ispis,가로);pisati_16(Ispis+2,Vertikalno_položaj);pisati_16(Ispis+4,završiti_X-가로);pisati_16(Ispis+6,završiti_Y-Vertikalno_položaj);pisati_32(Ispis+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_koordinata=Vertikalno_položaj;Y_koordinata<završiti_Y;Y_koordinata++)for(unsigned koordinata_x=가로;koordinata_x<završiti_X;koordinata_x++){
        uint32_t 색=보드화면읽기(koordinata_x,Y_koordinata),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<pel_podesiti_veličinu;순번++)Ispis[출력수++]=VALUE>>(8*(큰끝?pel_podesiti_veličinu-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(듣는곳<0)return;
    if(peer_VALUE<0){if(보드밀리초()<다시받을때)return;peer_VALUE=망연결받기(듣는곳);if(peer_VALUE<0)return;
        veza_TIME=보드밀리초();faza_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        pel_podesiti_veličinu=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(faza_VALUE<5&&보드밀리초()-veza_TIME>15000){Zatvori();return;}
    if(출력수){int 수=통신쓰기(peer_VALUE,Ispis+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Zatvori();return;}}
    if(!출력수&&닫을예정){Zatvori();return;}
    if(!출력수&&dodatak_položaj<dodatak_COUNT)poslati_dodatak();
    if(입력수==sizeof(입력)){Zatvori();return;}
    int RECEIVED_COUNT=통신읽기(peer_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Zatvori();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||dodatak_položaj<dodatak_COUNT)return;
    if(faza_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Zatvori();return;}소비(12);const unsigned char metoda_provjere_vjerodostojnosti[]={1,2};내보내기(metoda_provjere_vjerodostojnosti,2);faza_VALUE=2;return;}
    if(faza_VALUE==2&&입력수){if(입력[0]!=2||원격난수(test_VALUE,16)){Zatvori();return;}소비(1);내보내기(test_VALUE,16);faza_VALUE=3;return;}
    if(faza_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys lozinka_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&lozinka_VALUE,열쇠,8);memcpy(정답,test_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&lozinka_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&lozinka_VALUE,0,sizeof(lozinka_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(test_VALUE,0,16);
        pisati_32(Ispis,차이?1:0);출력수=4;보낸수=0;
        if(차이){pisati_32(Ispis+4,19);memcpy(Ispis+8,"Authentication fail",19);출력수=27;닫을예정=1;}else faza_VALUE=4;return;}
    if(faza_VALUE==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Zatvori();return;}
        if(!ploča_Terminal(7)){const unsigned char događaj[]={30,2,1,0,0,0,0};원격입력넣기(događaj,7);}
        memset(Ispis,0,40);pisati_16(Ispis,너비);pisati_16(Ispis+2,높이);Ispis[4]=32;Ispis[5]=24;Ispis[7]=1;
        pisati_16(Ispis+8,255);pisati_16(Ispis+10,255);pisati_16(Ispis+12,255);Ispis[14]=16;Ispis[15]=8;
        const char *Naziv="jkoros native";pisati_32(Ispis+20,strlen(Naziv));memcpy(Ispis+24,Naziv,strlen(Naziv));출력수=24+strlen(Naziv);보낸수=0;faza_VALUE=5;return;}
    if(faza_VALUE!=5||!입력수)return;
    unsigned TYPE_oblast=입력[0],필요=TYPE_oblast==0?20:TYPE_oblast==2?4:TYPE_oblast==3?10:TYPE_oblast==4?8:TYPE_oblast==5?6:TYPE_oblast==6?8:0;
    if(!필요){Zatvori();return;}if(입력수<필요)return;
    if(TYPE_oblast==2){unsigned 수=읽기16(입력+2);if(수>128){Zatvori();return;}필요+=수*4;}
    if(TYPE_oblast==6){unsigned 수=읽기32(입력+4);if(수>4096){Zatvori();return;}필요+=수;}
    if(입력수<필요)return;
    if(TYPE_oblast==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Zatvori();return;}
        pel_podesiti_veličinu=bit_VALUE/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TYPE_oblast==3)화면요청(입력);
    else if(TYPE_oblast==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TYPE_oblast==5){unsigned koordinata_x=읽기16(입력+2),Y_koordinata=읽기16(입력+4);if(koordinata_x>=너비)koordinata_x=너비-1;if(Y_koordinata>=높이)Y_koordinata=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char događaj[]={30,1,입력[1],koordinata_x&255,koordinata_x>>8,Y_koordinata&255,Y_koordinata>>8};원격입력넣기(događaj,sizeof(događaj));}
    소비(필요);
}
