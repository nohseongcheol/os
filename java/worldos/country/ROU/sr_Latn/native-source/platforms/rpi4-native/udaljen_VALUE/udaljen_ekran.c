/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 veze, 제한된 입력 길이, 비동기 poslati_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 podaci 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "udaljen_VALUE.h"
#include "kriptografija_Podrška.h"
#include "Profil.h"
#include "../Mreža_stek/Mreža_stek.h"
#include "../računar/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tabla_Terminal(uintptr_t);
void udaljen_Ključ_potez_mastilom(unsigned,int);
void 원격글쇠초기화(void);
void izvršavanje_udaljen_Ključ(void);
static int Slušanje_učesnik=-1,ravnopravni_uređaj_VALUE=-1,faza_VALUE,닫을예정;
static uintptr_t veza_TIME,다시받을때;
static unsigned char 입력[8192],출력[4096],izazov_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,piksel_promeniti_veličinu=4,big_endian_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned pločica_COUNT,pločica_pozicija,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *podaci_pozicija){return(unsigned)podaci_pozicija[0]*256+podaci_pozicija[1];}
static uint32_t 읽기32(const unsigned char *podaci_pozicija){return(uint32_t)podaci_pozicija[0]<<24|(uint32_t)podaci_pozicija[1]<<16|(uint32_t)podaci_pozicija[2]<<8|podaci_pozicija[3];}
static void 쓰기16(unsigned char *podaci_pozicija,unsigned VALUE){podaci_pozicija[0]=VALUE>>8;podaci_pozicija[1]=VALUE;}
static void 쓰기32(unsigned char *podaci_pozicija,uint32_t VALUE){podaci_pozicija[0]=VALUE>>24;podaci_pozicija[1]=VALUE>>16;podaci_pozicija[2]=VALUE>>8;podaci_pozicija[3]=VALUE;}
static void Zatvori(void){if(ravnopravni_uređaj_VALUE>=0)Zatvori_Mreža(ravnopravni_uređaj_VALUE);ravnopravni_uređaj_VALUE=-1;faza_VALUE=0;입력수=출력수=보낸수=0;pločica_COUNT=pločica_pozicija=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *podaci,unsigned 수){memcpy(출력,podaci,수);출력수=수;보낸수=0;}
static void iskoristiti_VALUE(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int kontrola_udaljen_ekran(unsigned radnja){
    if(radnja==0){Zatvori();if(Slušanje_učesnik>=0)Zatvori_Mreža(Slušanje_učesnik);Slušanje_učesnik=-1;return 0;}
    if(radnja!=1)return Slušanje_učesnik>=0;
    if(Slušanje_učesnik>=0)return 0;
    int port_VALUE=통신끝점만들기(1);if(port_VALUE<0)return port_VALUE;통신주소재사용(port_VALUE);
    int KR=NET_povezati(port_VALUE,0,5900);if(!KR)KR=NET_slušati(port_VALUE);
    if(KR<0){Zatvori_Mreža(port_VALUE);return KR;}Slušanje_učesnik=port_VALUE;return 0;
}
static uint32_t pločica_rezime(unsigned 가로,unsigned vertikala_pozicija){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=vertikala_pozicija;세로좌표<vertikala_pozicija+16&&세로좌표<높이;세로좌표++)for(unsigned x_koordinata=가로;x_koordinata<가로+32&&x_koordinata<너비;x_koordinata++)VALUE=(VALUE^보드화면읽기(x_koordinata,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *podaci_pozicija){
    요청가로=읽기16(podaci_pozicija+2);요청세로=읽기16(podaci_pozicija+4);요청폭=읽기16(podaci_pozicija+6);요청높이=읽기16(podaci_pozicija+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    pločica_COUNT=pločica_pozicija=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned x_koordinata=요청가로/32;x_koordinata<=(요청가로+요청폭-1)/32;x_koordinata++){
        unsigned indeks_pozicije=세로좌표*60+x_koordinata;uint32_t rezime_VALUE=pločica_rezime(x_koordinata*32,세로좌표*16);
        if(!podaci_pozicija[1]||지난요약[indeks_pozicije]!=rezime_VALUE)바뀐타일[pločica_COUNT++]=indeks_pozicije;
    }
    출력[0]=출력[1]=0;쓰기16(출력+2,pločica_COUNT);출력수=4;보낸수=0;
}
static void poslati_pločica(void){
    unsigned indeks_pozicije=바뀐타일[pločica_pozicija++],가로=(indeks_pozicije%60)*32,vertikala_pozicija=(indeks_pozicije/60)*16;
    unsigned završiti_razgovor_X=가로+32,završiti_razgovor_Y=vertikala_pozicija+16;if(završiti_razgovor_X>너비)završiti_razgovor_X=너비;if(završiti_razgovor_Y>높이)završiti_razgovor_Y=높이;
    /* 부분 타일 zahtev 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&vertikala_pozicija>=요청세로&&završiti_razgovor_X<=요청가로+요청폭&&završiti_razgovor_Y<=요청세로+요청높이;
    if(전부)지난요약[indeks_pozicije]=pločica_rezime(가로,vertikala_pozicija);
    if(가로<요청가로)가로=요청가로;if(vertikala_pozicija<요청세로)vertikala_pozicija=요청세로;
    if(završiti_razgovor_X>요청가로+요청폭)završiti_razgovor_X=요청가로+요청폭;if(završiti_razgovor_Y>요청세로+요청높이)završiti_razgovor_Y=요청세로+요청높이;
    쓰기16(출력,가로);쓰기16(출력+2,vertikala_pozicija);쓰기16(출력+4,završiti_razgovor_X-가로);쓰기16(출력+6,završiti_razgovor_Y-vertikala_pozicija);쓰기32(출력+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=vertikala_pozicija;세로좌표<završiti_razgovor_Y;세로좌표++)for(unsigned x_koordinata=가로;x_koordinata<završiti_razgovor_X;x_koordinata++){
        uint32_t 색=보드화면읽기(x_koordinata,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<piksel_promeniti_veličinu;순번++)출력[출력수++]=VALUE>>(8*(big_endian_VALUE?piksel_promeniti_veličinu-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Slušanje_učesnik<0)return;
    if(ravnopravni_uređaj_VALUE<0){if(보드밀리초()<다시받을때)return;ravnopravni_uređaj_VALUE=NET_prihvatiti(Slušanje_učesnik);if(ravnopravni_uređaj_VALUE<0)return;
        veza_TIME=보드밀리초();faza_VALUE=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        piksel_promeniti_veličinu=4;big_endian_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(faza_VALUE<5&&보드밀리초()-veza_TIME>15000){Zatvori();return;}
    if(출력수){int 수=통신쓰기(ravnopravni_uređaj_VALUE,출력+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Zatvori();return;}}
    if(!출력수&&닫을예정){Zatvori();return;}
    if(!출력수&&pločica_pozicija<pločica_COUNT)poslati_pločica();
    if(입력수==sizeof(입력)){Zatvori();return;}
    int RECEIVED_COUNT=통신읽기(ravnopravni_uređaj_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Zatvori();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||pločica_pozicija<pločica_COUNT)return;
    if(faza_VALUE==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Zatvori();return;}iskoristiti_VALUE(12);const unsigned char metod_potvrde_identiteta[]={1,2};내보내기(metod_potvrde_identiteta,2);faza_VALUE=2;return;}
    if(faza_VALUE==2&&입력수){if(입력[0]!=2||원격난수(izazov_VALUE,16)){Zatvori();return;}iskoristiti_VALUE(1);내보내기(izazov_VALUE,16);faza_VALUE=3;return;}
    if(faza_VALUE==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys lozinka_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&lozinka_VALUE,열쇠,8);memcpy(정답,izazov_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&lozinka_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];iskoristiti_VALUE(16);memset(&lozinka_VALUE,0,sizeof(lozinka_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(izazov_VALUE,0,16);
        쓰기32(출력,차이?1:0);출력수=4;보낸수=0;
        if(차이){쓰기32(출력+4,19);memcpy(출력+8,"Authentication fail",19);출력수=27;닫을예정=1;}else faza_VALUE=4;return;}
    if(faza_VALUE==4&&입력수){iskoristiti_VALUE(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Zatvori();return;}
        if(!Tabla_Terminal(7)){const unsigned char događaj[]={30,2,1,0,0,0,0};원격입력넣기(događaj,7);}
        memset(출력,0,40);쓰기16(출력,너비);쓰기16(출력+2,높이);출력[4]=32;출력[5]=24;출력[7]=1;
        쓰기16(출력+8,255);쓰기16(출력+10,255);쓰기16(출력+12,255);출력[14]=16;출력[15]=8;
        const char *ime="jkoros native";쓰기32(출력+20,strlen(ime));memcpy(출력+24,ime,strlen(ime));출력수=24+strlen(ime);보낸수=0;faza_VALUE=5;return;}
    if(faza_VALUE!=5||!입력수)return;
    unsigned tip_oblast=입력[0],필요=tip_oblast==0?20:tip_oblast==2?4:tip_oblast==3?10:tip_oblast==4?8:tip_oblast==5?6:tip_oblast==6?8:0;
    if(!필요){Zatvori();return;}if(입력수<필요)return;
    if(tip_oblast==2){unsigned 수=읽기16(입력+2);if(수>128){Zatvori();return;}필요+=수*4;}
    if(tip_oblast==6){unsigned 수=읽기32(입력+4);if(수>4096){Zatvori();return;}필요+=수;}
    if(입력수<필요)return;
    if(tip_oblast==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Zatvori();return;}
        piksel_promeniti_veličinu=bit_VALUE/8;big_endian_VALUE=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(tip_oblast==3)화면요청(입력);
    else if(tip_oblast==4)udaljen_Ključ_potez_mastilom(읽기32(입력+4),입력[1]!=0);
    else if(tip_oblast==5){unsigned x_koordinata=읽기16(입력+2),세로좌표=읽기16(입력+4);if(x_koordinata>=너비)x_koordinata=너비-1;if(세로좌표>=높이)세로좌표=높이-1;
        if(입력[1])izvršavanje_udaljen_Ključ();
        unsigned char događaj[]={30,1,입력[1],x_koordinata&255,x_koordinata>>8,세로좌표&255,세로좌표>>8};원격입력넣기(događaj,sizeof(događaj));}
    iskoristiti_VALUE(필요);
}
