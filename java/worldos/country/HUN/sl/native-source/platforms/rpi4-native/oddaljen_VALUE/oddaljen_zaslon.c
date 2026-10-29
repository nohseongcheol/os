/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Poveži, 제한된 입력 길이, 비동기 poslati_VALUE, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 podatki 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "oddaljen_VALUE.h"
#include "kriptografija_Podpora.h"
#include "Profil.h"
#include "../mreža_Sklad/mreža_Sklad.h"
#include "../računalnik/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tabla_Terminal(uintptr_t);
void oddaljen_Ključ_poteza_rokopisa(unsigned,int);
void inicializirati_oddaljen_Ključ_poteza_rokopisa(void);
void potrjevanje_oddaljen_Ključ(void);
static int Poslušanje_končna_točka=-1,enakovreden_VALUE=-1,območje_VALUE_29ee1bb7,닫을예정;
static uintptr_t povezava_čas,다시받을때;
static unsigned char 입력[8192],Izpis[4096],izziv_VALUE[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,višina_VALUE,slikovna_pika_spremeniti_velikost=4,big_endian_VALUE,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned ploščica_COUNT,ploščica_položaj,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *podatki_položaj){return(unsigned)podatki_položaj[0]*256+podatki_položaj[1];}
static uint32_t 읽기32(const unsigned char *podatki_položaj){return(uint32_t)podatki_položaj[0]<<24|(uint32_t)podatki_položaj[1]<<16|(uint32_t)podatki_položaj[2]<<8|podatki_položaj[3];}
static void pisati_16(unsigned char *podatki_položaj,unsigned VALUE){podatki_položaj[0]=VALUE>>8;podatki_položaj[1]=VALUE;}
static void pisati_32(unsigned char *podatki_položaj,uint32_t VALUE){podatki_položaj[0]=VALUE>>24;podatki_položaj[1]=VALUE>>16;podatki_položaj[2]=VALUE>>8;podatki_položaj[3]=VALUE;}
static void Zapri(void){if(enakovreden_VALUE>=0)Zapri_mreža(enakovreden_VALUE);enakovreden_VALUE=-1;območje_VALUE_29ee1bb7=0;입력수=출력수=보낸수=0;ploščica_COUNT=ploščica_položaj=0;닫을예정=0;inicializirati_oddaljen_Ključ_poteza_rokopisa();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *podatki,unsigned 수){memcpy(Izpis,podatki,수);출력수=수;보낸수=0;}
static void porabiti_VALUE(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int nadzor_oddaljen_zaslon(unsigned Dejanje){
    if(Dejanje==0){Zapri();if(Poslušanje_končna_točka>=0)Zapri_mreža(Poslušanje_končna_točka);Poslušanje_končna_točka=-1;return 0;}
    if(Dejanje!=1)return Poslušanje_končna_točka>=0;
    if(Poslušanje_končna_točka>=0)return 0;
    int vrata_VALUE=Ustvari_vtičnica_končna_točka(1);if(vrata_VALUE<0)return vrata_VALUE;통신주소재사용(vrata_VALUE);
    int REZULTAT=NET_BIND(vrata_VALUE,0,5900);if(!REZULTAT)REZULTAT=NET_poslušati(vrata_VALUE);
    if(REZULTAT<0){Zapri_mreža(vrata_VALUE);return REZULTAT;}Poslušanje_končna_točka=vrata_VALUE;return 0;
}
static uint32_t ploščica_povzetek(unsigned 가로,unsigned Navpično_položaj){
    uint32_t VALUE=2166136261u;
    for(unsigned 세로좌표=Navpično_položaj;세로좌표<Navpično_položaj+16&&세로좌표<višina_VALUE;세로좌표++)for(unsigned koordinata_x=가로;koordinata_x<가로+32&&koordinata_x<너비;koordinata_x++)VALUE=(VALUE^보드화면읽기(koordinata_x,세로좌표))*16777619u;
    return VALUE;
}
static void 화면요청(const unsigned char *podatki_položaj){
    요청가로=읽기16(podatki_položaj+2);요청세로=읽기16(podatki_položaj+4);요청폭=읽기16(podatki_položaj+6);요청높이=읽기16(podatki_položaj+8);
    if(요청가로>=너비||요청세로>=višina_VALUE)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>višina_VALUE-요청세로&&요청세로<višina_VALUE)요청높이=višina_VALUE-요청세로;
    ploščica_COUNT=ploščica_položaj=0;
    if(요청폭&&요청높이)for(unsigned 세로좌표=요청세로/16;세로좌표<=(요청세로+요청높이-1)/16;세로좌표++)for(unsigned koordinata_x=요청가로/32;koordinata_x<=(요청가로+요청폭-1)/32;koordinata_x++){
        unsigned kazalec_mesta=세로좌표*60+koordinata_x;uint32_t povzetek_VALUE=ploščica_povzetek(koordinata_x*32,세로좌표*16);
        if(!podatki_položaj[1]||지난요약[kazalec_mesta]!=povzetek_VALUE)바뀐타일[ploščica_COUNT++]=kazalec_mesta;
    }
    Izpis[0]=Izpis[1]=0;pisati_16(Izpis+2,ploščica_COUNT);출력수=4;보낸수=0;
}
static void poslati_ploščica(void){
    unsigned kazalec_mesta=바뀐타일[ploščica_položaj++],가로=(kazalec_mesta%60)*32,Navpično_položaj=(kazalec_mesta/60)*16;
    unsigned končati_klic_X=가로+32,končati_klic_Y=Navpično_položaj+16;if(končati_klic_X>너비)končati_klic_X=너비;if(končati_klic_Y>višina_VALUE)končati_klic_Y=višina_VALUE;
    /* 부분 타일 zahteva 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Navpično_položaj>=요청세로&&končati_klic_X<=요청가로+요청폭&&končati_klic_Y<=요청세로+요청높이;
    if(전부)지난요약[kazalec_mesta]=ploščica_povzetek(가로,Navpično_položaj);
    if(가로<요청가로)가로=요청가로;if(Navpično_položaj<요청세로)Navpično_položaj=요청세로;
    if(končati_klic_X>요청가로+요청폭)končati_klic_X=요청가로+요청폭;if(končati_klic_Y>요청세로+요청높이)končati_klic_Y=요청세로+요청높이;
    pisati_16(Izpis,가로);pisati_16(Izpis+2,Navpično_položaj);pisati_16(Izpis+4,končati_klic_X-가로);pisati_16(Izpis+6,končati_klic_Y-Navpično_položaj);pisati_32(Izpis+8,0);
    출력수=12;보낸수=0;
    for(unsigned 세로좌표=Navpično_položaj;세로좌표<končati_klic_Y;세로좌표++)for(unsigned koordinata_x=가로;koordinata_x<končati_klic_X;koordinata_x++){
        uint32_t 색=보드화면읽기(koordinata_x,세로좌표),VALUE=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<slikovna_pika_spremeniti_velikost;순번++)Izpis[출력수++]=VALUE>>(8*(big_endian_VALUE?slikovna_pika_spremeniti_velikost-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Poslušanje_končna_točka<0)return;
    if(enakovreden_VALUE<0){if(보드밀리초()<다시받을때)return;enakovreden_VALUE=NET_sprejeti(Poslušanje_končna_točka);if(enakovreden_VALUE<0)return;
        povezava_čas=보드밀리초();območje_VALUE_29ee1bb7=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        slikovna_pika_spremeniti_velikost=4;big_endian_VALUE=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(območje_VALUE_29ee1bb7<5&&보드밀리초()-povezava_čas>15000){Zapri();return;}
    if(출력수){int 수=NET_pisati(enakovreden_VALUE,Izpis+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Zapri();return;}}
    if(!출력수&&닫을예정){Zapri();return;}
    if(!출력수&&ploščica_položaj<ploščica_COUNT)poslati_ploščica();
    if(입력수==sizeof(입력)){Zapri();return;}
    int RECEIVED_COUNT=통신읽기(enakovreden_VALUE,입력+입력수,sizeof(입력)-입력수);
    if(RECEIVED_COUNT==0||(RECEIVED_COUNT<0&&RECEIVED_COUNT!=-11)){Zapri();return;}if(RECEIVED_COUNT>0)입력수+=RECEIVED_COUNT;
    if(출력수||ploščica_položaj<ploščica_COUNT)return;
    if(območje_VALUE_29ee1bb7==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Zapri();return;}porabiti_VALUE(12);const unsigned char način_preverjanja_pristnosti[]={1,2};내보내기(način_preverjanja_pristnosti,2);območje_VALUE_29ee1bb7=2;return;}
    if(območje_VALUE_29ee1bb7==2&&입력수){if(입력[0]!=2||원격난수(izziv_VALUE,16)){Zapri();return;}porabiti_VALUE(1);내보내기(izziv_VALUE,16);območje_VALUE_29ee1bb7=3;return;}
    if(območje_VALUE_29ee1bb7==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys geslo_VALUE;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALUE=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALUE&1);VALUE>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&geslo_VALUE,열쇠,8);memcpy(정답,izziv_VALUE,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vektor_VALUE[8]={0};br_des_ct_cbcenc_run(&geslo_VALUE,vektor_VALUE,정답+순번,8);memset(vektor_VALUE,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];porabiti_VALUE(16);memset(&geslo_VALUE,0,sizeof(geslo_VALUE));memset(열쇠,0,8);memset(정답,0,16);memset(izziv_VALUE,0,16);
        pisati_32(Izpis,차이?1:0);출력수=4;보낸수=0;
        if(차이){pisati_32(Izpis+4,19);memcpy(Izpis+8,"Authentication fail",19);출력수=27;닫을예정=1;}else območje_VALUE_29ee1bb7=4;return;}
    if(območje_VALUE_29ee1bb7==4&&입력수){porabiti_VALUE(1);너비=보드화면너비();višina_VALUE=보드화면높이();if(!너비||!višina_VALUE||너비>1920||višina_VALUE>1080){Zapri();return;}
        if(!Tabla_Terminal(7)){const unsigned char dogodek[]={30,2,1,0,0,0,0};원격입력넣기(dogodek,7);}
        memset(Izpis,0,40);pisati_16(Izpis,너비);pisati_16(Izpis+2,višina_VALUE);Izpis[4]=32;Izpis[5]=24;Izpis[7]=1;
        pisati_16(Izpis+8,255);pisati_16(Izpis+10,255);pisati_16(Izpis+12,255);Izpis[14]=16;Izpis[15]=8;
        const char *Ime="jkoros native";pisati_32(Izpis+20,strlen(Ime));memcpy(Izpis+24,Ime,strlen(Ime));출력수=24+strlen(Ime);보낸수=0;območje_VALUE_29ee1bb7=5;return;}
    if(območje_VALUE_29ee1bb7!=5||!입력수)return;
    unsigned Tip_območje=입력[0],필요=Tip_območje==0?20:Tip_območje==2?4:Tip_območje==3?10:Tip_območje==4?8:Tip_območje==5?6:Tip_območje==6?8:0;
    if(!필요){Zapri();return;}if(입력수<필요)return;
    if(Tip_območje==2){unsigned 수=읽기16(입력+2);if(수>128){Zapri();return;}필요+=수*4;}
    if(Tip_območje==6){unsigned 수=읽기32(입력+4);if(수>4096){Zapri();return;}필요+=수;}
    if(입력수<필요)return;
    if(Tip_območje==0){unsigned bit_VALUE=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALUE!=16&&bit_VALUE!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALUE)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALUE)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALUE)-1)){Zapri();return;}
        slikovna_pika_spremeniti_velikost=bit_VALUE/8;big_endian_VALUE=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(Tip_območje==3)화면요청(입력);
    else if(Tip_območje==4)oddaljen_Ključ_poteza_rokopisa(읽기32(입력+4),입력[1]!=0);
    else if(Tip_območje==5){unsigned koordinata_x=읽기16(입력+2),세로좌표=읽기16(입력+4);if(koordinata_x>=너비)koordinata_x=너비-1;if(세로좌표>=višina_VALUE)세로좌표=višina_VALUE-1;
        if(입력[1])potrjevanje_oddaljen_Ključ();
        unsigned char dogodek[]={30,1,입력[1],koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8};원격입력넣기(dogodek,sizeof(dogodek));}
    porabiti_VALUE(필요);
}
