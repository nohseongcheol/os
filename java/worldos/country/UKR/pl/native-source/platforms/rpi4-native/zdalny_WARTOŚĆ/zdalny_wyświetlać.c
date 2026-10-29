/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Połącz, 제한된 wejście_WARTOŚĆ długość_WARTOŚĆ, 비동기 wysłać_WARTOŚĆ, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 dane 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "zdalny_WARTOŚĆ.h"
#include "kryptografia_wsparcie.h"
#include "Profil.h"
#include "../sieć_Stos/sieć_Stos.h"
#include "../maszyna/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tablica_Terminal(uintptr_t);
void zdalny_Klucz_ślad_pędzla(unsigned,int);
void inicjuj_zdalny_Klucz_ślad_pędzla(void);
void przekazywać_zdalny_Klucz(void);
static int Nasłuchiwanie_uczestnik=-1,węzeł_równorzędny_WARTOŚĆ=-1,etap_WARTOŚĆ,닫을예정;
static uintptr_t połączenie_CZAS,다시받을때;
static unsigned char wejście_WARTOŚĆ[8192],pozycja_wyjścia[4096],test_WARTOŚĆ[16];
static unsigned wejście_ILE_LICZB,produkt_wyjściowy_ILE_LICZB,보낸수;
static unsigned 너비,wysokość_WARTOŚĆ,piksel_zmienić_rozmiar=4,big_endian_WARTOŚĆ,빨강최대=255,초록최대=255,파랑최대=255,czerwony_przesunąć=16,zielony_przesunąć=8,niebieski_przesunąć;
static uint32_t Wstecz_podsumowanie[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned kafelek_ILE_LICZB,kafelek_stanowisko,wymagane_X,wymagane_Y,요청폭,wymagane_wysokość;
static unsigned 읽기16(const unsigned char *dane_stanowisko){return(unsigned)dane_stanowisko[0]*256+dane_stanowisko[1];}
static uint32_t 읽기32(const unsigned char *dane_stanowisko){return(uint32_t)dane_stanowisko[0]<<24|(uint32_t)dane_stanowisko[1]<<16|(uint32_t)dane_stanowisko[2]<<8|dane_stanowisko[3];}
static void zapis_PEGI_16(unsigned char *dane_stanowisko,unsigned WARTOŚĆ){dane_stanowisko[0]=WARTOŚĆ>>8;dane_stanowisko[1]=WARTOŚĆ;}
static void zapis_32(unsigned char *dane_stanowisko,uint32_t WARTOŚĆ){dane_stanowisko[0]=WARTOŚĆ>>24;dane_stanowisko[1]=WARTOŚĆ>>16;dane_stanowisko[2]=WARTOŚĆ>>8;dane_stanowisko[3]=WARTOŚĆ;}
static void Zamknięte(void){if(węzeł_równorzędny_WARTOŚĆ>=0)Zamknij_sieć(węzeł_równorzędny_WARTOŚĆ);węzeł_równorzędny_WARTOŚĆ=-1;etap_WARTOŚĆ=0;wejście_ILE_LICZB=produkt_wyjściowy_ILE_LICZB=보낸수=0;kafelek_ILE_LICZB=kafelek_stanowisko=0;닫을예정=0;inicjuj_zdalny_Klucz_ślad_pędzla();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *dane,unsigned identyfikator){memcpy(pozycja_wyjścia,dane,identyfikator);produkt_wyjściowy_ILE_LICZB=identyfikator;보낸수=0;}
static void zużycie_WARTOŚĆ(unsigned identyfikator){wejście_ILE_LICZB-=identyfikator;memmove(wejście_WARTOŚĆ,wejście_WARTOŚĆ+identyfikator,wejście_ILE_LICZB);}
int kontrola_zdalny_wyświetlać(unsigned Akcja){
    if(Akcja==0){Zamknięte();if(Nasłuchiwanie_uczestnik>=0)Zamknij_sieć(Nasłuchiwanie_uczestnik);Nasłuchiwanie_uczestnik=-1;return 0;}
    if(Akcja!=1)return Nasłuchiwanie_uczestnik>=0;
    if(Nasłuchiwanie_uczestnik>=0)return 0;
    int port_WARTOŚĆ=Twórca_gniazdo_uczestnik(1);if(port_WARTOŚĆ<0)return port_WARTOŚĆ;통신주소재사용(port_WARTOŚĆ);
    int WYNIK=NET_BIND(port_WARTOŚĆ,0,5900);if(!WYNIK)WYNIK=NET_nasłuchiwać(port_WARTOŚĆ);
    if(WYNIK<0){Zamknij_sieć(port_WARTOŚĆ);return WYNIK;}Nasłuchiwanie_uczestnik=port_WARTOŚĆ;return 0;
}
static uint32_t kafelek_podsumowanie(unsigned 가로,unsigned gałąź_stanowisko){
    uint32_t WARTOŚĆ=2166136261u;
    for(unsigned Y_współrzędna=gałąź_stanowisko;Y_współrzędna<gałąź_stanowisko+16&&Y_współrzędna<wysokość_WARTOŚĆ;Y_współrzędna++)for(unsigned współrzędna_X=가로;współrzędna_X<가로+32&&współrzędna_X<너비;współrzędna_X++)WARTOŚĆ=(WARTOŚĆ^보드화면읽기(współrzędna_X,Y_współrzędna))*16777619u;
    return WARTOŚĆ;
}
static void 화면요청(const unsigned char *dane_stanowisko){
    wymagane_X=읽기16(dane_stanowisko+2);wymagane_Y=읽기16(dane_stanowisko+4);요청폭=읽기16(dane_stanowisko+6);wymagane_wysokość=읽기16(dane_stanowisko+8);
    if(wymagane_X>=너비||wymagane_Y>=wysokość_WARTOŚĆ)요청폭=wymagane_wysokość=0;
    if(요청폭>너비-wymagane_X&&wymagane_X<너비)요청폭=너비-wymagane_X;
    if(wymagane_wysokość>wysokość_WARTOŚĆ-wymagane_Y&&wymagane_Y<wysokość_WARTOŚĆ)wymagane_wysokość=wysokość_WARTOŚĆ-wymagane_Y;
    kafelek_ILE_LICZB=kafelek_stanowisko=0;
    if(요청폭&&wymagane_wysokość)for(unsigned Y_współrzędna=wymagane_Y/16;Y_współrzędna<=(wymagane_Y+wymagane_wysokość-1)/16;Y_współrzędna++)for(unsigned współrzędna_X=wymagane_X/32;współrzędna_X<=(wymagane_X+요청폭-1)/32;współrzędna_X++){
        unsigned indeks_pozycji=Y_współrzędna*60+współrzędna_X;uint32_t podsumowanie_WARTOŚĆ=kafelek_podsumowanie(współrzędna_X*32,Y_współrzędna*16);
        if(!dane_stanowisko[1]||Wstecz_podsumowanie[indeks_pozycji]!=podsumowanie_WARTOŚĆ)바뀐타일[kafelek_ILE_LICZB++]=indeks_pozycji;
    }
    pozycja_wyjścia[0]=pozycja_wyjścia[1]=0;zapis_PEGI_16(pozycja_wyjścia+2,kafelek_ILE_LICZB);produkt_wyjściowy_ILE_LICZB=4;보낸수=0;
}
static void wysłać_kafelek(void){
    unsigned indeks_pozycji=바뀐타일[kafelek_stanowisko++],가로=(indeks_pozycji%60)*32,gałąź_stanowisko=(indeks_pozycji/60)*16;
    unsigned Koniec_X=가로+32,Koniec_Y=gałąź_stanowisko+16;if(Koniec_X>너비)Koniec_X=너비;if(Koniec_Y>wysokość_WARTOŚĆ)Koniec_Y=wysokość_WARTOŚĆ;
    /* 부분 타일 żądanie 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=wymagane_X&&gałąź_stanowisko>=wymagane_Y&&Koniec_X<=wymagane_X+요청폭&&Koniec_Y<=wymagane_Y+wymagane_wysokość;
    if(전부)Wstecz_podsumowanie[indeks_pozycji]=kafelek_podsumowanie(가로,gałąź_stanowisko);
    if(가로<wymagane_X)가로=wymagane_X;if(gałąź_stanowisko<wymagane_Y)gałąź_stanowisko=wymagane_Y;
    if(Koniec_X>wymagane_X+요청폭)Koniec_X=wymagane_X+요청폭;if(Koniec_Y>wymagane_Y+wymagane_wysokość)Koniec_Y=wymagane_Y+wymagane_wysokość;
    zapis_PEGI_16(pozycja_wyjścia,가로);zapis_PEGI_16(pozycja_wyjścia+2,gałąź_stanowisko);zapis_PEGI_16(pozycja_wyjścia+4,Koniec_X-가로);zapis_PEGI_16(pozycja_wyjścia+6,Koniec_Y-gałąź_stanowisko);zapis_32(pozycja_wyjścia+8,0);
    produkt_wyjściowy_ILE_LICZB=12;보낸수=0;
    for(unsigned Y_współrzędna=gałąź_stanowisko;Y_współrzędna<Koniec_Y;Y_współrzędna++)for(unsigned współrzędna_X=가로;współrzędna_X<Koniec_X;współrzędna_X++){
        uint32_t 색=보드화면읽기(współrzędna_X,Y_współrzędna),WARTOŚĆ=(((색>>16)&255)*빨강최대/255)<<czerwony_przesunąć|
            (((색>>8)&255)*초록최대/255)<<zielony_przesunąć|((색&255)*파랑최대/255)<<niebieski_przesunąć;
        for(unsigned 순번=0;순번<piksel_zmienić_rozmiar;순번++)pozycja_wyjścia[produkt_wyjściowy_ILE_LICZB++]=WARTOŚĆ>>(8*(big_endian_WARTOŚĆ?piksel_zmienić_rozmiar-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(Nasłuchiwanie_uczestnik<0)return;
    if(węzeł_równorzędny_WARTOŚĆ<0){if(보드밀리초()<다시받을때)return;węzeł_równorzędny_WARTOŚĆ=NET_akceptować(Nasłuchiwanie_uczestnik);if(węzeł_równorzędny_WARTOŚĆ<0)return;
        połączenie_CZAS=보드밀리초();etap_WARTOŚĆ=1;내보내기("RFB 003.008\n",12);memset(Wstecz_podsumowanie,0,sizeof(Wstecz_podsumowanie));
        piksel_zmienić_rozmiar=4;big_endian_WARTOŚĆ=0;빨강최대=초록최대=파랑최대=255;czerwony_przesunąć=16;zielony_przesunąć=8;niebieski_przesunąć=0;}
    if(etap_WARTOŚĆ<5&&보드밀리초()-połączenie_CZAS>15000){Zamknięte();return;}
    if(produkt_wyjściowy_ILE_LICZB){int identyfikator=NET_zapis(węzeł_równorzędny_WARTOŚĆ,pozycja_wyjścia+보낸수,produkt_wyjściowy_ILE_LICZB-보낸수);if(identyfikator>0){보낸수+=identyfikator;if(보낸수==produkt_wyjściowy_ILE_LICZB)produkt_wyjściowy_ILE_LICZB=보낸수=0;}else if(identyfikator!=-11){Zamknięte();return;}}
    if(!produkt_wyjściowy_ILE_LICZB&&닫을예정){Zamknięte();return;}
    if(!produkt_wyjściowy_ILE_LICZB&&kafelek_stanowisko<kafelek_ILE_LICZB)wysłać_kafelek();
    if(wejście_ILE_LICZB==sizeof(wejście_WARTOŚĆ)){Zamknięte();return;}
    int KWOTA_WYKUP_ILE_LICZB=통신읽기(węzeł_równorzędny_WARTOŚĆ,wejście_WARTOŚĆ+wejście_ILE_LICZB,sizeof(wejście_WARTOŚĆ)-wejście_ILE_LICZB);
    if(KWOTA_WYKUP_ILE_LICZB==0||(KWOTA_WYKUP_ILE_LICZB<0&&KWOTA_WYKUP_ILE_LICZB!=-11)){Zamknięte();return;}if(KWOTA_WYKUP_ILE_LICZB>0)wejście_ILE_LICZB+=KWOTA_WYKUP_ILE_LICZB;
    if(produkt_wyjściowy_ILE_LICZB||kafelek_stanowisko<kafelek_ILE_LICZB)return;
    if(etap_WARTOŚĆ==1&&wejście_ILE_LICZB>=12){if(memcmp(wejście_WARTOŚĆ,"RFB 003.008\n",12)){Zamknięte();return;}zużycie_WARTOŚĆ(12);const unsigned char metoda_uwierzytelniania[]={1,2};내보내기(metoda_uwierzytelniania,2);etap_WARTOŚĆ=2;return;}
    if(etap_WARTOŚĆ==2&&wejście_ILE_LICZB){if(wejście_WARTOŚĆ[0]!=2||zdalny_losowy(test_WARTOŚĆ,16)){Zamknięte();return;}zużycie_WARTOŚĆ(1);내보내기(test_WARTOŚĆ,16);etap_WARTOŚĆ=3;return;}
    if(etap_WARTOŚĆ==3&&wejście_ILE_LICZB>=16){unsigned char Klucz_materiał[8],정답[16];br_des_ct_cbcenc_keys hasło_WARTOŚĆ;
        for(unsigned 순번=0;순번<8;순번++){unsigned WARTOŚĆ=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(WARTOŚĆ&1);WARTOŚĆ>>=1;}Klucz_materiał[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&hasło_WARTOŚĆ,Klucz_materiał,8);memcpy(정답,test_WARTOŚĆ,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char wektor_WARTOŚĆ[8]={0};br_des_ct_cbcenc_run(&hasło_WARTOŚĆ,wektor_WARTOŚĆ,정답+순번,8);memset(wektor_WARTOŚĆ,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^wejście_WARTOŚĆ[순번];zużycie_WARTOŚĆ(16);memset(&hasło_WARTOŚĆ,0,sizeof(hasło_WARTOŚĆ));memset(Klucz_materiał,0,8);memset(정답,0,16);memset(test_WARTOŚĆ,0,16);
        zapis_32(pozycja_wyjścia,차이?1:0);produkt_wyjściowy_ILE_LICZB=4;보낸수=0;
        if(차이){zapis_32(pozycja_wyjścia+4,19);memcpy(pozycja_wyjścia+8,"Authentication fail",19);produkt_wyjściowy_ILE_LICZB=27;닫을예정=1;}else etap_WARTOŚĆ=4;return;}
    if(etap_WARTOŚĆ==4&&wejście_ILE_LICZB){zużycie_WARTOŚĆ(1);너비=보드화면너비();wysokość_WARTOŚĆ=보드화면높이();if(!너비||!wysokość_WARTOŚĆ||너비>1920||wysokość_WARTOŚĆ>1080){Zamknięte();return;}
        if(!Tablica_Terminal(7)){const unsigned char Wydarzenie[]={30,2,1,0,0,0,0};kanał_zdalny_wejście(Wydarzenie,7);}
        memset(pozycja_wyjścia,0,40);zapis_PEGI_16(pozycja_wyjścia,너비);zapis_PEGI_16(pozycja_wyjścia+2,wysokość_WARTOŚĆ);pozycja_wyjścia[4]=32;pozycja_wyjścia[5]=24;pozycja_wyjścia[7]=1;
        zapis_PEGI_16(pozycja_wyjścia+8,255);zapis_PEGI_16(pozycja_wyjścia+10,255);zapis_PEGI_16(pozycja_wyjścia+12,255);pozycja_wyjścia[14]=16;pozycja_wyjścia[15]=8;
        const char *Nazwa="jkoros native";zapis_32(pozycja_wyjścia+20,strlen(Nazwa));memcpy(pozycja_wyjścia+24,Nazwa,strlen(Nazwa));produkt_wyjściowy_ILE_LICZB=24+strlen(Nazwa);보낸수=0;etap_WARTOŚĆ=5;return;}
    if(etap_WARTOŚĆ!=5||!wejście_ILE_LICZB)return;
    unsigned TYP_obszar=wejście_WARTOŚĆ[0],필요=TYP_obszar==0?20:TYP_obszar==2?4:TYP_obszar==3?10:TYP_obszar==4?8:TYP_obszar==5?6:TYP_obszar==6?8:0;
    if(!필요){Zamknięte();return;}if(wejście_ILE_LICZB<필요)return;
    if(TYP_obszar==2){unsigned identyfikator=읽기16(wejście_WARTOŚĆ+2);if(identyfikator>128){Zamknięte();return;}필요+=identyfikator*4;}
    if(TYP_obszar==6){unsigned identyfikator=읽기32(wejście_WARTOŚĆ+4);if(identyfikator>4096){Zamknięte();return;}필요+=identyfikator;}
    if(wejście_ILE_LICZB<필요)return;
    if(TYP_obszar==0){unsigned bit_WARTOŚĆ=wejście_WARTOŚĆ[4],빨=읽기16(wejście_WARTOŚĆ+8),초=읽기16(wejście_WARTOŚĆ+10),파=읽기16(wejście_WARTOŚĆ+12),czerwony_Kanał_przesunąć=wejście_WARTOŚĆ[14],zielony_Kanał_przesunąć=wejście_WARTOŚĆ[15],niebieski_Kanał_przesunąć=wejście_WARTOŚĆ[16];
        if((bit_WARTOŚĆ!=16&&bit_WARTOŚĆ!=32)||!wejście_WARTOŚĆ[7]||wejście_WARTOŚĆ[6]>1||!빨||!초||!파||빨>255||초>255||파>255||czerwony_Kanał_przesunąć>24||zielony_Kanał_przesunąć>24||niebieski_Kanał_przesunąć>24||
           ((uint64_t)빨<<czerwony_Kanał_przesunąć)>((1ull<<bit_WARTOŚĆ)-1)||((uint64_t)초<<zielony_Kanał_przesunąć)>((1ull<<bit_WARTOŚĆ)-1)||((uint64_t)파<<niebieski_Kanał_przesunąć)>((1ull<<bit_WARTOŚĆ)-1)){Zamknięte();return;}
        piksel_zmienić_rozmiar=bit_WARTOŚĆ/8;big_endian_WARTOŚĆ=wejście_WARTOŚĆ[6];빨강최대=빨;초록최대=초;파랑최대=파;czerwony_przesunąć=czerwony_Kanał_przesunąć;zielony_przesunąć=zielony_Kanał_przesunąć;niebieski_przesunąć=niebieski_Kanał_przesunąć;memset(Wstecz_podsumowanie,0,sizeof(Wstecz_podsumowanie));
    }else if(TYP_obszar==3)화면요청(wejście_WARTOŚĆ);
    else if(TYP_obszar==4)zdalny_Klucz_ślad_pędzla(읽기32(wejście_WARTOŚĆ+4),wejście_WARTOŚĆ[1]!=0);
    else if(TYP_obszar==5){unsigned współrzędna_X=읽기16(wejście_WARTOŚĆ+2),Y_współrzędna=읽기16(wejście_WARTOŚĆ+4);if(współrzędna_X>=너비)współrzędna_X=너비-1;if(Y_współrzędna>=wysokość_WARTOŚĆ)Y_współrzędna=wysokość_WARTOŚĆ-1;
        if(wejście_WARTOŚĆ[1])przekazywać_zdalny_Klucz();
        unsigned char Wydarzenie[]={30,1,wejście_WARTOŚĆ[1],współrzędna_X&255,współrzędna_X>>8,Y_współrzędna&255,Y_współrzędna>>8};kanał_zdalny_wejście(Wydarzenie,sizeof(Wydarzenie));}
    zużycie_WARTOŚĆ(필요);
}
