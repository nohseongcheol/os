#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* własny 네 Okno 합성과 UTF-8 interpretator_poleceń. 바뀐 영역의 Wykonane_WARTOŚĆ 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t maszyna_Word;
extern maszyna_Word Tablica_piksel(maszyna_Word,maszyna_Word,maszyna_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_czcionka[];
#define 최대열수 237
#define Historia_linia_ILE_LICZB 160
typedef struct {
    uint32_t 글자칸들[Historia_linia_ILE_LICZB][최대열수]; uint8_t 모양들[Historia_linia_ILE_LICZB][최대열수];
    unsigned 너비,wysokość_WARTOŚĆ,LICZBA_KOLUMN,WIERSZ_ILE_LICZB,크기바뀜;
    unsigned 살아있음,współrzędna_X,Y_współrzędna,WIERSZ_stanowisko,kolumna_stanowisko,맨위,przewijać,전경색,배경색,탈출상태,parametr_WARTOŚĆ[4],parametr_INDEKS,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,MIN_K_WARTOŚĆ,대체화면,가리개보임;
} Terminal;
static Terminal Windows_Lista[4];
static int Fokus=-1,produkt_wyjściowy,zamówić_WARTOŚĆ[4],wpis_ILE_LICZB,przeciągnąć_WARTOŚĆ=-1,przeciągnąć_X,przeciągnąć_Y;
static unsigned systemy_informacyjne_oczekujący,단추들,Pulpit_Widok,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_wpis;
static unsigned znak_dwubajtowy(unsigned kod_znaku){return kod_znaku>=256?2:1;}
static void 사각영역(unsigned współrzędna_X,unsigned Y_współrzędna,unsigned 너비값,unsigned wymagane_wysokość_WARTOŚĆ,unsigned 색상){
    Tablica_prostokąt_Wypełnij(współrzędna_X,Y_współrzędna,너비값,wymagane_wysokość_WARTOŚĆ,색상);
}
void Terminal_symbol(unsigned współrzędna_X,unsigned Y_współrzędna,unsigned kod_znaku,unsigned 전경색,unsigned 배경색){
    unsigned 너비=znak_dwubajtowy(kod_znaku)*8;if(kod_znaku==0xffffffffu)return;
    int 왼쪽=współrzędna_X,위쪽=Y_współrzędna,폭=너비,długość_WARTOŚĆ=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&długość_WARTOŚĆ))return;
    if(kod_znaku==' '){Tablica_prostokąt_Wypełnij(왼쪽,위쪽,폭,długość_WARTOŚĆ,배경색);return;}
    unsigned WYSZUKAJ_INDEKS=kod_znaku<65536?kod_znaku:kod_znaku>=0x1f600&&kod_znaku<0x1f650?65536+kod_znaku-0x1f600:0xfffd;
    const unsigned char *czcionka_WARTOŚĆ=Terminal_czcionka+WYSZUKAJ_INDEKS*32;
    for(int wiersz_wejścia=위쪽;wiersz_wejścia<위쪽+długość_WARTOŚĆ;wiersz_wejścia++){unsigned BITS_Lista=czcionka_WARTOŚĆ[(wiersz_wejścia-Y_współrzędna)*2]*256+czcionka_WARTOŚĆ[(wiersz_wejścia-Y_współrzędna)*2+1];for(int gniazdo_wpis=왼쪽;gniazdo_wpis<왼쪽+폭;gniazdo_wpis++)Tablica_piksel(gniazdo_wpis,wiersz_wejścia,(BITS_Lista&(0x8000>>(gniazdo_wpis-współrzędna_X)))?전경색:배경색);}
}
static void nazwa_tabela(unsigned współrzędna_X,unsigned Y_współrzędna,const char *ciąg_dane,unsigned 전경색,unsigned 배경색){while(*ciąg_dane){unsigned kod_znaku=(unsigned char)*ciąg_dane++, 남은수=0;if(kod_znaku>=0xc0){남은수=kod_znaku<0xe0?1:kod_znaku<0xf0?2:3;kod_znaku&=(1u<<(6-남은수))-1;while(남은수--&&*ciąg_dane)kod_znaku=(kod_znaku<<6)|((unsigned char)*ciąg_dane++&63);}Terminal_symbol(współrzędna_X,Y_współrzędna,kod_znaku,전경색,배경색);współrzędna_X+=znak_dwubajtowy(kod_znaku)*8;}}
static unsigned 첫항목(void){return Terminal_wpis->맨위;}
static int 보이는지(void){return Terminal_wpis->살아있음&&Fokus>=0&&Terminal_wpis==&Windows_Lista[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned WIERSZ_stanowisko,unsigned kolumna_stanowisko){
    if(!보이는지()||WIERSZ_stanowisko<첫항목()-Terminal_wpis->przewijać||WIERSZ_stanowisko>=첫항목()-Terminal_wpis->przewijać+Terminal_wpis->WIERSZ_ILE_LICZB||kolumna_stanowisko>=Terminal_wpis->LICZBA_KOLUMN)return;
    unsigned kod_znaku=Terminal_wpis->글자칸들[WIERSZ_stanowisko%Historia_linia_ILE_LICZB][kolumna_stanowisko],ciąg_dane=Terminal_wpis->모양들[WIERSZ_stanowisko%Historia_linia_ILE_LICZB][kolumna_stanowisko];
    if(znak_dwubajtowy(kod_znaku)==2&&kolumna_stanowisko+1>=Terminal_wpis->LICZBA_KOLUMN)kod_znaku=' ';
    Terminal_symbol(Terminal_wpis->współrzędna_X+12+kolumna_stanowisko*8,Terminal_wpis->Y_współrzędna+36+(WIERSZ_stanowisko-첫항목()+Terminal_wpis->przewijać)*16,kod_znaku?kod_znaku:' ',색상들[ciąg_dane&15],색상들[ciąg_dane>>4]);
}
static void daszek_WARTOŚĆ(int program_okno){if(!보이는지()||Terminal_wpis->przewijać||Terminal_wpis->kolumna_stanowisko>=Terminal_wpis->LICZBA_KOLUMN||Terminal_wpis->WIERSZ_stanowisko<Terminal_wpis->맨위||Terminal_wpis->WIERSZ_stanowisko>=Terminal_wpis->맨위+Terminal_wpis->WIERSZ_ILE_LICZB)return;
    if(!program_okno||!Terminal_wpis->가리개보임)그리기(Terminal_wpis->WIERSZ_stanowisko,Terminal_wpis->kolumna_stanowisko);else 사각영역(Terminal_wpis->współrzędna_X+12+Terminal_wpis->kolumna_stanowisko*8,Terminal_wpis->Y_współrzędna+36+(Terminal_wpis->WIERSZ_stanowisko-Terminal_wpis->맨위)*16+14,8,2,색상들[Terminal_wpis->전경색]);}
static void treść_WARTOŚĆ_cb0f2404(void){
    사각영역(Terminal_wpis->współrzędna_X+12,Terminal_wpis->Y_współrzędna+36,Terminal_wpis->LICZBA_KOLUMN*8,Terminal_wpis->WIERSZ_ILE_LICZB*16,색상들[0]);
    int 가로=Terminal_wpis->współrzędna_X+12,gałąź_stanowisko=Terminal_wpis->Y_współrzędna+36,폭=Terminal_wpis->LICZBA_KOLUMN*8,długość_WARTOŚĆ=Terminal_wpis->WIERSZ_ILE_LICZB*16;
    if(보드그림범위(&가로,&gałąź_stanowisko,&폭,&długość_WARTOŚĆ)){
    unsigned 첫줄=(gałąź_stanowisko-Terminal_wpis->Y_współrzędna-36)/16,끝줄=(gałąź_stanowisko+długość_WARTOŚĆ-Terminal_wpis->Y_współrzędna-36+15)/16;
    unsigned 첫칸=(가로-Terminal_wpis->współrzędna_X-12)/8,끝칸=(가로+폭-Terminal_wpis->współrzędna_X-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 granica_WARTOŚĆ 왼쪽에서 시작한 두 gniazdo_wpis 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kod_znaku=첫칸;kod_znaku<끝칸;kod_znaku++){
        unsigned WIERSZ_stanowisko=첫항목()-Terminal_wpis->przewijać+반환값,znak_WARTOŚĆ=Terminal_wpis->글자칸들[WIERSZ_stanowisko%Historia_linia_ILE_LICZB][kod_znaku],ciąg_dane=Terminal_wpis->모양들[WIERSZ_stanowisko%Historia_linia_ILE_LICZB][kod_znaku];
        if(znak_dwubajtowy(znak_WARTOŚĆ)==2&&kod_znaku+1>=Terminal_wpis->LICZBA_KOLUMN)znak_WARTOŚĆ=' ';
        if((znak_WARTOŚĆ==0||znak_WARTOŚĆ==' ')&&(ciąg_dane>>4)==0)continue;
        Terminal_symbol(Terminal_wpis->współrzędna_X+12+kod_znaku*8,Terminal_wpis->Y_współrzędna+36+반환값*16,znak_WARTOŚĆ?znak_WARTOŚĆ:' ',색상들[ciąg_dane&15],색상들[ciąg_dane>>4]);
    }}
    nazwa_tabela(Terminal_wpis->współrzędna_X+12,Terminal_wpis->Y_współrzędna+Terminal_wpis->wysokość_WARTOŚĆ-18,Terminal_wpis->przewijać?"PgDn: recent output":Terminal_wpis->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);daszek_WARTOŚĆ(1);
}
static void wykonanie_kadr(int identyfikator_WARTOŚĆ){
    Terminal_wpis=&Windows_Lista[identyfikator_WARTOŚĆ];
    int 가로=Terminal_wpis->współrzędna_X,gałąź_stanowisko=Terminal_wpis->Y_współrzędna,폭=Terminal_wpis->너비,długość_WARTOŚĆ=Terminal_wpis->wysokość_WARTOŚĆ;
    if(!보드그림범위(&가로,&gałąź_stanowisko,&폭,&długość_WARTOŚĆ))return;
    사각영역(Terminal_wpis->współrzędna_X,Terminal_wpis->Y_współrzędna,Terminal_wpis->너비,Terminal_wpis->wysokość_WARTOŚĆ,0x403127);
    unsigned 색상=identyfikator_WARTOŚĆ==Fokus?0x905020:0x604438;사각영역(Terminal_wpis->współrzędna_X,Terminal_wpis->Y_współrzędna,Terminal_wpis->너비,30,색상);
    nazwa_tabela(Terminal_wpis->współrzędna_X+12,Terminal_wpis->Y_współrzędna+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identyfikator_WARTOŚĆ),0};nazwa_tabela(Terminal_wpis->współrzędna_X+148,Terminal_wpis->Y_współrzędna+7,수치,0xffffff,색상);
    nazwa_tabela(Terminal_wpis->współrzędna_X+240,Terminal_wpis->Y_współrzędna+7,Terminal_wpis->너비>=500?(한글입력?"[PL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[PL]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_wpis->współrzędna_X+Terminal_wpis->너비-32,Terminal_wpis->Y_współrzędna+4,26,22,0x5555b8);nazwa_tabela(Terminal_wpis->współrzędna_X+Terminal_wpis->너비-24,Terminal_wpis->Y_współrzędna+7,"X",0xffffff,0x5555b8);
    treść_WARTOŚĆ_cb0f2404();
}
static void rysować_scena(void){
    if(!Pulpit_Widok)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nazwa_tabela(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lista[순번].살아있음){unsigned kod_znaku=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kod_znaku);nazwa_tabela(160+순번*112,8,"Terminal",0xffffff,kod_znaku);char ciąg_dane[2]={(char)('1'+순번),0};nazwa_tabela(232+순번*112,8,ciąg_dane,0xffffff,kod_znaku);}
    if(!wpis_ILE_LICZB)nazwa_tabela(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<wpis_ILE_LICZB;순번++)wykonanie_kadr(zamówić_WARTOŚĆ[순번]);화면다시그림(Fokus);Terminal_wpis=&Windows_Lista[produkt_wyjściowy];
}
static void Paint_region(int 가로,int gałąź_stanowisko,int 폭,int długość_WARTOŚĆ){
    if(!Pulpit_Widok||!보드그림범위(&가로,&gałąź_stanowisko,&폭,&długość_WARTOŚĆ))return;
    for(int wiersz_wejścia=gałąź_stanowisko;wiersz_wejścia<gałąź_stanowisko+długość_WARTOŚĆ;wiersz_wejścia+=32){
        int pasek_wysokość=gałąź_stanowisko+długość_WARTOŚĆ-wiersz_wejścia;if(pasek_wysokość>32)pasek_wysokość=32;
        if(Tablica_START_rysunek(가로,wiersz_wejścia,폭,pasek_wysokość)){rysować_scena();Tablica_Zakończ_rysunek();}
    }
}
static void 다시그리기(void){Paint_region(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Okno 영역과 Wstecz_towar 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int gałąź_stanowisko,int 폭,int długość_WARTOŚĆ,Terminal *Okno){
    int 왼쪽=가로>(int)Okno->współrzędna_X?가로:(int)Okno->współrzędna_X;
    int 위쪽=gałąź_stanowisko>(int)Okno->Y_współrzędna?gałąź_stanowisko:(int)Okno->Y_współrzędna;
    int PRAWY=가로+폭<(int)(Okno->współrzędna_X+Okno->너비)?가로+폭:(int)(Okno->współrzędna_X+Okno->너비);
    int 아래쪽=gałąź_stanowisko+długość_WARTOŚĆ<(int)(Okno->Y_współrzędna+Okno->wysokość_WARTOŚĆ)?gałąź_stanowisko+długość_WARTOŚĆ:(int)(Okno->Y_współrzędna+Okno->wysokość_WARTOŚĆ);
    Paint_region(Okno->współrzędna_X,Okno->Y_współrzędna,Okno->너비,Okno->wysokość_WARTOŚĆ);
    if(왼쪽>=PRAWY||위쪽>=아래쪽){Paint_region(가로,gałąź_stanowisko,폭,długość_WARTOŚĆ);return;}
    Paint_region(가로,gałąź_stanowisko,폭,위쪽-gałąź_stanowisko);
    Paint_region(가로,아래쪽,폭,gałąź_stanowisko+długość_WARTOŚĆ-아래쪽);
    Paint_region(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_region(PRAWY,위쪽,가로+폭-PRAWY,아래쪽-위쪽);
}
static void sygnał_Fokus(void){systemy_informacyjne_oczekujący=(systemy_informacyjne_oczekujący&~15u)|(unsigned)(Fokus+1)|0x10000;}
void Terminal_wejście_tryb(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal *okno_wpis=&Windows_Lista[Fokus];
        nazwa_tabela(okno_wpis->współrzędna_X+240,okno_wpis->Y_współrzędna+7,okno_wpis->너비>=500?(한글입력?"[PL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[PL]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identyfikator_WARTOŚĆ){if(identyfikator_WARTOŚĆ<0||identyfikator_WARTOŚĆ>=4||!Windows_Lista[identyfikator_WARTOŚĆ].살아있음)return;int bieżący_stanowisko=0;while(bieżący_stanowisko<wpis_ILE_LICZB&&zamówić_WARTOŚĆ[bieżący_stanowisko]!=identyfikator_WARTOŚĆ)bieżący_stanowisko++;for(;bieżący_stanowisko+1<wpis_ILE_LICZB;bieżący_stanowisko++)zamówić_WARTOŚĆ[bieżący_stanowisko]=zamówić_WARTOŚĆ[bieżący_stanowisko+1];zamówić_WARTOŚĆ[wpis_ILE_LICZB-1]=identyfikator_WARTOŚĆ;Fokus=identyfikator_WARTOŚĆ;sygnał_Fokus();다시그리기();}
static void 빈칸채우기(unsigned WIERSZ_stanowisko){for(unsigned kod_znaku=0;kod_znaku<최대열수;kod_znaku++){Terminal_wpis->글자칸들[WIERSZ_stanowisko%Historia_linia_ILE_LICZB][kod_znaku]=0;Terminal_wpis->모양들[WIERSZ_stanowisko%Historia_linia_ILE_LICZB][kod_znaku]=Terminal_wpis->전경색|(Terminal_wpis->배경색<<4);}}
static void czyścić_Spis_treści(void){Terminal_wpis->WIERSZ_stanowisko=Terminal_wpis->kolumna_stanowisko=Terminal_wpis->맨위=Terminal_wpis->przewijać=0;for(unsigned 반환값=0;반환값<Historia_linia_ILE_LICZB;반환값++)빈칸채우기(반환값);if(보이는지())treść_WARTOŚĆ_cb0f2404();}
static int Twórca_wpis(void){
    if(!보드화면기억공간())return -19;int identyfikator_WARTOŚĆ=0;while(identyfikator_WARTOŚĆ<4&&Windows_Lista[identyfikator_WARTOŚĆ].살아있음)identyfikator_WARTOŚĆ++;if(identyfikator_WARTOŚĆ==4)return -28;
    Pulpit_Widok=1;Terminal_wpis=&Windows_Lista[identyfikator_WARTOŚĆ];memset(Terminal_wpis,0,sizeof(*Terminal_wpis));Terminal_wpis->살아있음=1;Terminal_wpis->너비=568;Terminal_wpis->wysokość_WARTOŚĆ=360;Terminal_wpis->LICZBA_KOLUMN=68;Terminal_wpis->WIERSZ_ILE_LICZB=19;Terminal_wpis->współrzędna_X=12+identyfikator_WARTOŚĆ*16;Terminal_wpis->Y_współrzędna=48+identyfikator_WARTOŚĆ*18;Terminal_wpis->전경색=7;Terminal_wpis->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historia_linia_ILE_LICZB;반환값++)빈칸채우기(반환값);zamówić_WARTOŚĆ[wpis_ILE_LICZB++]=identyfikator_WARTOŚĆ;Fokus=identyfikator_WARTOŚĆ;systemy_informacyjne_oczekujący|=1u<<(4+identyfikator_WARTOŚĆ);sygnał_Fokus();다시그리기();return identyfikator_WARTOŚĆ+1;
}
static void Zamknij_okno(int identyfikator_WARTOŚĆ){
    if(identyfikator_WARTOŚĆ<0||identyfikator_WARTOŚĆ>=4||!Windows_Lista[identyfikator_WARTOŚĆ].살아있음)return;Windows_Lista[identyfikator_WARTOŚĆ].살아있음=0;systemy_informacyjne_oczekujący|=1u<<(8+identyfikator_WARTOŚĆ);
    int bieżący_stanowisko=0;while(bieżący_stanowisko<wpis_ILE_LICZB&&zamówić_WARTOŚĆ[bieżący_stanowisko]!=identyfikator_WARTOŚĆ)bieżący_stanowisko++;for(;bieżący_stanowisko+1<wpis_ILE_LICZB;bieżący_stanowisko++)zamówić_WARTOŚĆ[bieżący_stanowisko]=zamówić_WARTOŚĆ[bieżący_stanowisko+1];wpis_ILE_LICZB--;
    if(Fokus==identyfikator_WARTOŚĆ)Fokus=wpis_ILE_LICZB?zamówić_WARTOŚĆ[wpis_ILE_LICZB-1]:-1;sygnał_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_wpis->kolumna_stanowisko=0;Terminal_wpis->WIERSZ_stanowisko++;if(Terminal_wpis->WIERSZ_stanowisko>=Terminal_wpis->맨위+Terminal_wpis->WIERSZ_ILE_LICZB){Terminal_wpis->맨위++;빈칸채우기(Terminal_wpis->WIERSZ_stanowisko);if(보이는지())treść_WARTOŚĆ_cb0f2404();}}
static void kod_znaku_451f2815(unsigned kod_znaku){
    if(kod_znaku==13){Terminal_wpis->kolumna_stanowisko=0;return;}if(kod_znaku==10){줄바꿈();return;}if(kod_znaku==8){if(Terminal_wpis->kolumna_stanowisko)Terminal_wpis->kolumna_stanowisko--;return;}
    if(kod_znaku==9){unsigned towar_ILE_LICZB=8-Terminal_wpis->kolumna_stanowisko%8;while(towar_ILE_LICZB--)kod_znaku_451f2815(' ');return;}if(kod_znaku<32||kod_znaku==127)return;
    unsigned 너비값=znak_dwubajtowy(kod_znaku);if(Terminal_wpis->kolumna_stanowisko+너비값>Terminal_wpis->LICZBA_KOLUMN)줄바꿈();
    if(Terminal_wpis->글자칸들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko]==0xffffffffu&&Terminal_wpis->kolumna_stanowisko){Terminal_wpis->글자칸들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko-1]=' ';그리기(Terminal_wpis->WIERSZ_stanowisko,Terminal_wpis->kolumna_stanowisko-1);}
    if(znak_dwubajtowy(Terminal_wpis->글자칸들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko])==2&&Terminal_wpis->kolumna_stanowisko+1<Terminal_wpis->LICZBA_KOLUMN){Terminal_wpis->글자칸들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko+1]=' ';그리기(Terminal_wpis->WIERSZ_stanowisko,Terminal_wpis->kolumna_stanowisko+1);}
    Terminal_wpis->글자칸들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko]=kod_znaku;Terminal_wpis->모양들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko]=Terminal_wpis->전경색|(Terminal_wpis->배경색<<4);
    if(너비값==2)Terminal_wpis->글자칸들[Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB][Terminal_wpis->kolumna_stanowisko+1]=0xffffffffu;
    그리기(Terminal_wpis->WIERSZ_stanowisko,Terminal_wpis->kolumna_stanowisko);Terminal_wpis->kolumna_stanowisko+=너비값;
}
static void uchwyt_kontrola_SEKWENCJA(unsigned kod_znaku){
    unsigned towar_ILE_LICZB=Terminal_wpis->parametr_WARTOŚĆ[0]?Terminal_wpis->parametr_WARTOŚĆ[0]:1;
    if(kod_znaku=='m')for(unsigned 순번=0;순번<=Terminal_wpis->parametr_INDEKS;순번++){unsigned dane_stanowisko=Terminal_wpis->parametr_WARTOŚĆ[순번];if(!dane_stanowisko){Terminal_wpis->전경색=7;Terminal_wpis->배경색=0;}if(dane_stanowisko==1&&Terminal_wpis->전경색<8)Terminal_wpis->전경색+=8;if(dane_stanowisko==7){unsigned 유지=Terminal_wpis->전경색;Terminal_wpis->전경색=Terminal_wpis->배경색;Terminal_wpis->배경색=유지;}if(dane_stanowisko>=30&&dane_stanowisko<=37)Terminal_wpis->전경색=dane_stanowisko-30;if(dane_stanowisko>=90&&dane_stanowisko<=97)Terminal_wpis->전경색=dane_stanowisko-90+8;if(dane_stanowisko>=40&&dane_stanowisko<=47)Terminal_wpis->배경색=dane_stanowisko-40;if(dane_stanowisko>=100&&dane_stanowisko<=107)Terminal_wpis->배경색=dane_stanowisko-100+8;if(dane_stanowisko==39)Terminal_wpis->전경색=7;if(dane_stanowisko==49)Terminal_wpis->배경색=0;}
    if(kod_znaku=='J'&&(Terminal_wpis->parametr_WARTOŚĆ[0]==2||Terminal_wpis->parametr_WARTOŚĆ[0]==3))czyścić_Spis_treści();
    if(kod_znaku=='K'){unsigned 출발위치=Terminal_wpis->parametr_WARTOŚĆ[0]==2?0:Terminal_wpis->kolumna_stanowisko,도착위치=Terminal_wpis->parametr_WARTOŚĆ[0]==1?Terminal_wpis->kolumna_stanowisko+1:Terminal_wpis->LICZBA_KOLUMN;if(Terminal_wpis->parametr_WARTOŚĆ[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_wpis->LICZBA_KOLUMN;순번++){
        unsigned WIERSZ_WARTOŚĆ=Terminal_wpis->WIERSZ_stanowisko%Historia_linia_ILE_LICZB,znak_WARTOŚĆ=Terminal_wpis->글자칸들[WIERSZ_WARTOŚĆ][순번],kształt_WARTOŚĆ=Terminal_wpis->전경색|(Terminal_wpis->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 czcionka_WARTOŚĆ 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_WARTOŚĆ!=0&&znak_WARTOŚĆ!=' ')||Terminal_wpis->모양들[WIERSZ_WARTOŚĆ][순번]!=kształt_WARTOŚĆ;
        Terminal_wpis->글자칸들[WIERSZ_WARTOŚĆ][순번]=' ';Terminal_wpis->모양들[WIERSZ_WARTOŚĆ][순번]=kształt_WARTOŚĆ;
        if(바뀜)그리기(Terminal_wpis->WIERSZ_stanowisko,순번);
    }}
    if(kod_znaku=='D')Terminal_wpis->kolumna_stanowisko=towar_ILE_LICZB>Terminal_wpis->kolumna_stanowisko?0:Terminal_wpis->kolumna_stanowisko-towar_ILE_LICZB;if(kod_znaku=='C')Terminal_wpis->kolumna_stanowisko=Terminal_wpis->kolumna_stanowisko+towar_ILE_LICZB>=Terminal_wpis->LICZBA_KOLUMN?Terminal_wpis->LICZBA_KOLUMN-1:Terminal_wpis->kolumna_stanowisko+towar_ILE_LICZB;
    if(kod_znaku=='G')Terminal_wpis->kolumna_stanowisko=towar_ILE_LICZB>Terminal_wpis->LICZBA_KOLUMN?Terminal_wpis->LICZBA_KOLUMN-1:towar_ILE_LICZB-1;if(kod_znaku=='A')Terminal_wpis->WIERSZ_stanowisko=towar_ILE_LICZB>Terminal_wpis->WIERSZ_stanowisko-Terminal_wpis->맨위?Terminal_wpis->맨위:Terminal_wpis->WIERSZ_stanowisko-towar_ILE_LICZB;
    if(kod_znaku=='B')Terminal_wpis->WIERSZ_stanowisko=Terminal_wpis->WIERSZ_stanowisko+towar_ILE_LICZB>=Terminal_wpis->맨위+Terminal_wpis->WIERSZ_ILE_LICZB?Terminal_wpis->맨위+Terminal_wpis->WIERSZ_ILE_LICZB-1:Terminal_wpis->WIERSZ_stanowisko+towar_ILE_LICZB;
    if(kod_znaku=='H'||kod_znaku=='f'){Terminal_wpis->WIERSZ_stanowisko=Terminal_wpis->맨위+(towar_ILE_LICZB>Terminal_wpis->WIERSZ_ILE_LICZB?Terminal_wpis->WIERSZ_ILE_LICZB:towar_ILE_LICZB)-1;unsigned współrzędna_X=Terminal_wpis->parametr_WARTOŚĆ[1]?Terminal_wpis->parametr_WARTOŚĆ[1]:1;Terminal_wpis->kolumna_stanowisko=(współrzędna_X>Terminal_wpis->LICZBA_KOLUMN?Terminal_wpis->LICZBA_KOLUMN:współrzędna_X)-1;}
    if(kod_znaku=='s'){Terminal_wpis->저장행=Terminal_wpis->WIERSZ_stanowisko;Terminal_wpis->저장열=Terminal_wpis->kolumna_stanowisko;}if(kod_znaku=='u'){Terminal_wpis->WIERSZ_stanowisko=Terminal_wpis->저장행;Terminal_wpis->kolumna_stanowisko=Terminal_wpis->저장열<Terminal_wpis->LICZBA_KOLUMN?Terminal_wpis->저장열:Terminal_wpis->LICZBA_KOLUMN-1;}
    if((kod_znaku=='h'||kod_znaku=='l')&&Terminal_wpis->parametr_WARTOŚĆ[0]==25)Terminal_wpis->가리개보임=kod_znaku=='h';
}
void Terminal_bajt(unsigned SEKUNDA_WARTOŚĆ){
    Terminal_wpis=&Windows_Lista[produkt_wyjściowy];if(!Terminal_wpis->살아있음)return;daszek_WARTOŚĆ(0);if(Terminal_wpis->przewijać){Terminal_wpis->przewijać=0;if(보이는지())treść_WARTOŚĆ_cb0f2404();}
    if(Terminal_wpis->탈출상태==1){Terminal_wpis->탈출상태=SEKUNDA_WARTOŚĆ=='['?2:0;Terminal_wpis->parametr_INDEKS=0;for(unsigned 순번=0;순번<4;순번++)Terminal_wpis->parametr_WARTOŚĆ[순번]=0;}
    else if(Terminal_wpis->탈출상태==2){if(SEKUNDA_WARTOŚĆ=='?'){}else if(SEKUNDA_WARTOŚĆ>='0'&&SEKUNDA_WARTOŚĆ<='9'){if(Terminal_wpis->parametr_WARTOŚĆ[Terminal_wpis->parametr_INDEKS]<10000)Terminal_wpis->parametr_WARTOŚĆ[Terminal_wpis->parametr_INDEKS]=Terminal_wpis->parametr_WARTOŚĆ[Terminal_wpis->parametr_INDEKS]*10+SEKUNDA_WARTOŚĆ-'0';}else if(SEKUNDA_WARTOŚĆ==';'&&Terminal_wpis->parametr_INDEKS<3)Terminal_wpis->parametr_INDEKS++;else{uchwyt_kontrola_SEKWENCJA(SEKUNDA_WARTOŚĆ);Terminal_wpis->탈출상태=0;}}
    else if(SEKUNDA_WARTOŚĆ==27){Terminal_wpis->긴부호없는값=0;Terminal_wpis->탈출상태=1;}else{
        if(Terminal_wpis->긴부호없는값&&(SEKUNDA_WARTOŚĆ&0xc0)!=0x80){Terminal_wpis->긴부호없는값=0;kod_znaku_451f2815(0xfffd);}
        if(Terminal_wpis->긴부호없는값){Terminal_wpis->부호없는결과=Terminal_wpis->부호없는결과*64+(SEKUNDA_WARTOŚĆ&63);if(--Terminal_wpis->긴부호없는값==0)kod_znaku_451f2815(Terminal_wpis->부호없는결과<Terminal_wpis->MIN_K_WARTOŚĆ||Terminal_wpis->부호없는결과>0x10ffff||(Terminal_wpis->부호없는결과>=0xd800&&Terminal_wpis->부호없는결과<=0xdfff)?0xfffd:Terminal_wpis->부호없는결과);}
        else if(SEKUNDA_WARTOŚĆ<128)kod_znaku_451f2815(SEKUNDA_WARTOŚĆ);else if(SEKUNDA_WARTOŚĆ>=0xc2&&SEKUNDA_WARTOŚĆ<=0xf4){Terminal_wpis->긴부호없는값=SEKUNDA_WARTOŚĆ<0xe0?1:SEKUNDA_WARTOŚĆ<0xf0?2:3;Terminal_wpis->부호없는결과=SEKUNDA_WARTOŚĆ&((1u<<(6-Terminal_wpis->긴부호없는값))-1);Terminal_wpis->MIN_K_WARTOŚĆ=Terminal_wpis->긴부호없는값==1?128:Terminal_wpis->긴부호없는값==2?2048:65536;}else kod_znaku_451f2815(0xfffd);
    }daszek_WARTOŚĆ(1);
}
int Terminal_oczekujący(void){return systemy_informacyjne_oczekujący!=0;}
/* 모서리 INDEKS: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int zmienić_rozmiar_przeciągnąć=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int gałąź_stanowisko) {
    for(int SEKWENCJA_WARTOŚĆ=wpis_ILE_LICZB-1;SEKWENCJA_WARTOŚĆ>=0;SEKWENCJA_WARTOŚĆ--){
        int identyfikator_WARTOŚĆ=zamówić_WARTOŚĆ[SEKWENCJA_WARTOŚĆ];Terminal *Okno=&Windows_Lista[identyfikator_WARTOŚĆ];
        if(가로>=(int)Okno->współrzędna_X&&gałąź_stanowisko>=(int)Okno->Y_współrzędna&&
           가로<(int)(Okno->współrzędna_X+Okno->너비)&&gałąź_stanowisko<(int)(Okno->Y_współrzędna+Okno->wysokość_WARTOŚĆ))return identyfikator_WARTOŚĆ;
    }return -1;
}
static int 모서리찾기(int identyfikator_WARTOŚĆ,int 가로,int gałąź_stanowisko) {
    if(identyfikator_WARTOŚĆ<0)return 0;Terminal *Okno=&Windows_Lista[identyfikator_WARTOŚĆ];
    int 왼쪽=가로<(int)Okno->współrzędna_X+8,PRAWY=가로>=(int)(Okno->współrzędna_X+Okno->너비)-8;
    int 위쪽=gałąź_stanowisko<(int)Okno->Y_współrzędna+8,아래쪽=gałąź_stanowisko>=(int)(Okno->Y_współrzędna+Okno->wysokość_WARTOŚĆ)-8;
    return (왼쪽||PRAWY)&&(위쪽||아래쪽)?1+PRAWY+아래쪽*2:0;
}
static int separator_WARTOŚĆ(int WARTOŚĆ,int 최소,int 최대){return WARTOŚĆ<최소?최소:WARTOŚĆ>최대?최대:WARTOŚĆ;}
static void przenosić_zmienić_rozmiar(int 가로,int gałąź_stanowisko) {
    Terminal *Okno=&Windows_Lista[zmienić_rozmiar_przeciągnąć];int 왼쪽=처음가로,위쪽=처음세로,PRAWY=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=separator_WARTOŚĆ(처음가로+가로-잡은가로,0,PRAWY-360);
    else PRAWY=separator_WARTOŚĆ(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=separator_WARTOŚĆ(처음세로+gałąź_stanowisko-잡은세로,34,아래쪽-216);
    else 아래쪽=separator_WARTOŚĆ(처음세로+처음높이+gałąź_stanowisko-잡은세로,위쪽+216,보드화면높이());
    unsigned LICZBA_KOLUMN=(PRAWY-왼쪽-24)/8,WIERSZ_ILE_LICZB=(아래쪽-위쪽-56)/16;
    if(Okno->LICZBA_KOLUMN!=LICZBA_KOLUMN||Okno->WIERSZ_ILE_LICZB!=WIERSZ_ILE_LICZB){
        Okno->크기바뀜=1;Okno->LICZBA_KOLUMN=LICZBA_KOLUMN;Okno->WIERSZ_ILE_LICZB=WIERSZ_ILE_LICZB;
        if(Okno->kolumna_stanowisko>=LICZBA_KOLUMN)Okno->kolumna_stanowisko=LICZBA_KOLUMN-1;
        if(Okno->WIERSZ_stanowisko>=Okno->맨위+WIERSZ_ILE_LICZB)Okno->맨위=Okno->WIERSZ_stanowisko-WIERSZ_ILE_LICZB+1;
        unsigned 한도=Okno->맨위;if(한도>Historia_linia_ILE_LICZB-WIERSZ_ILE_LICZB)한도=Historia_linia_ILE_LICZB-WIERSZ_ILE_LICZB;
        if(Okno->przewijać>한도)Okno->przewijać=한도;
    }
    int 옛가로=Okno->współrzędna_X,옛세로=Okno->Y_współrzędna,옛폭=Okno->너비,옛길이=Okno->wysokość_WARTOŚĆ;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==PRAWY-왼쪽&&옛길이==아래쪽-위쪽)return;
    Okno->współrzędna_X=왼쪽;Okno->Y_współrzędna=위쪽;Okno->너비=PRAWY-왼쪽;Okno->wysokość_WARTOŚĆ=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Okno);
}
void Terminal_wskaźnik(unsigned Dalej_towar,int współrzędna_X,int Y_współrzędna){
    unsigned 눌림=Dalej_towar&~단추들;단추들=Dalej_towar;
    if(!Pulpit_Widok){przeciągnąć_WARTOŚĆ=-1;zmienić_rozmiar_przeciągnąć=-1;Tablica_wskaźnik(współrzędna_X,Y_współrzędna,1);return;}
    if(!(Dalej_towar&1)){przeciągnąć_WARTOŚĆ=-1;zmienić_rozmiar_przeciągnąć=-1;}
    if(zmienić_rozmiar_przeciągnąć>=0&&!Windows_Lista[zmienić_rozmiar_przeciągnąć].살아있음)zmienić_rozmiar_przeciągnąć=-1;
    if(przeciągnąć_WARTOŚĆ>=0&&!Windows_Lista[przeciągnąć_WARTOŚĆ].살아있음)przeciągnąć_WARTOŚĆ=-1;
    if(zmienić_rozmiar_przeciągnąć>=0){
        przenosić_zmienić_rozmiar(współrzędna_X,Y_współrzędna);Tablica_wskaźnik(współrzędna_X,Y_współrzędna,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tablica_wskaźnik(współrzędna_X,Y_współrzędna,1);
    if(przeciągnąć_WARTOŚĆ>=0){
        Terminal *Okno=&Windows_Lista[przeciągnąć_WARTOŚĆ];
        int 옛가로=Okno->współrzędna_X,옛세로=Okno->Y_współrzędna;
        Okno->współrzędna_X=separator_WARTOŚĆ(współrzędna_X-przeciągnąć_X,0,보드화면너비()-Okno->너비);
        Okno->Y_współrzędna=separator_WARTOŚĆ(Y_współrzędna-przeciągnąć_Y,34,보드화면높이()-Okno->wysokość_WARTOŚĆ);
        if(옛가로!=(int)Okno->współrzędna_X||옛세로!=(int)Okno->Y_współrzędna)창자리그리기(옛가로,옛세로,Okno->너비,Okno->wysokość_WARTOŚĆ,Okno);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,współrzędna_X,Y_współrzędna)){화면가리킴(Fokus,눌림,współrzędna_X,Y_współrzędna);return;}
    int identyfikator_WARTOŚĆ=가리킨창(współrzędna_X,Y_współrzędna),모서리=모서리찾기(identyfikator_WARTOŚĆ,współrzędna_X,Y_współrzędna);
    if(모서리)Tablica_wskaźnik(współrzędna_X,Y_współrzędna,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Okno=&Windows_Lista[identyfikator_WARTOŚĆ];zmienić_rozmiar_przeciągnąć=identyfikator_WARTOŚĆ;잡은모서리=모서리;잡은가로=współrzędna_X;잡은세로=Y_współrzędna;
            처음가로=Okno->współrzędna_X;처음세로=Okno->Y_współrzędna;처음너비=Okno->너비;처음높이=Okno->wysokość_WARTOŚĆ;
            if(identyfikator_WARTOŚĆ!=Fokus)앞으로올리기(identyfikator_WARTOŚĆ);return;
        }
        if(Y_współrzędna<32&&współrzędna_X>=6&&współrzędna_X<142){Twórca_wpis();return;}
        if(Y_współrzędna<32&&współrzędna_X>=154&&współrzędna_X<602){앞으로올리기((współrzędna_X-154)/112);return;}
        if(identyfikator_WARTOŚĆ>=0){
            Terminal *Okno=&Windows_Lista[identyfikator_WARTOŚĆ];
            if(Y_współrzędna<(int)Okno->Y_współrzędna+30&&współrzędna_X>=(int)(Okno->współrzędna_X+Okno->너비)-32){Zamknij_okno(identyfikator_WARTOŚĆ);return;}
            if(identyfikator_WARTOŚĆ!=Fokus)앞으로올리기(identyfikator_WARTOŚĆ);
            if(Y_współrzędna<(int)Okno->Y_współrzędna+30){przeciągnąć_WARTOŚĆ=identyfikator_WARTOŚĆ;przeciągnąć_X=współrzędna_X-Okno->współrzędna_X;przeciągnąć_Y=Y_współrzędna-Okno->Y_współrzędna;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_wpis=&Windows_Lista[Fokus];if(눌림&8){unsigned 한도=Terminal_wpis->맨위;if(한도>Historia_linia_ILE_LICZB-Terminal_wpis->WIERSZ_ILE_LICZB)한도=Historia_linia_ILE_LICZB-Terminal_wpis->WIERSZ_ILE_LICZB;Terminal_wpis->przewijać=Terminal_wpis->przewijać+9>한도?한도:Terminal_wpis->przewijać+9;}else Terminal_wpis->przewijać=Terminal_wpis->przewijać<9?0:Terminal_wpis->przewijać-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Twórca_wpis();if(누름값==2&&wpis_ILE_LICZB)앞으로올리기(zamówić_WARTOŚĆ[0]);if(누름값==3)Zamknij_okno(Fokus);}
maszyna_Word Tablica_Terminal(maszyna_Word Akcja){
    if(Akcja==300){if(!Windows_Lista[produkt_wyjściowy].살아있음)return Twórca_wpis();Pulpit_Widok=1;다시그리기();return 0;}
    if(Akcja==0){Zamknij_okno(Fokus);return 0;}if(Akcja==1)return (uint32_t)Twórca_wpis();if(Akcja==2)return Fokus>=0;
    if(Akcja==9){Pulpit_Widok=0;return 0;}if(Akcja==7)return wpis_ILE_LICZB;if(Akcja==10)return Fokus+1;if(Akcja==11)return produkt_wyjściowy;
    if(Akcja==13){Terminal *Okno=&Windows_Lista[produkt_wyjściowy];return Okno->살아있음?(Okno->WIERSZ_ILE_LICZB<<16)|Okno->LICZBA_KOLUMN:(19<<16)|68;}
    if(Akcja==14){unsigned WARTOŚĆ=Windows_Lista[produkt_wyjściowy].크기바뀜;Windows_Lista[produkt_wyjściowy].크기바뀜=0;return WARTOŚĆ;}
    if(Akcja==12){unsigned WARTOŚĆ=systemy_informacyjne_oczekujący;systemy_informacyjne_oczekujący=0;return WARTOŚĆ;}
    if(Akcja>=20&&Akcja<24)return Windows_Lista[Akcja-20].살아있음;
    if(Akcja>=100&&Akcja<104){produkt_wyjściowy=Akcja-100;Terminal_wpis=&Windows_Lista[produkt_wyjściowy];return 0;}
    if(Akcja>=200&&Akcja<204){앞으로올리기(Akcja-200);return 0;}
    if(Akcja==3){다시그리기();return 0;}Terminal_wpis=&Windows_Lista[produkt_wyjściowy];if(!Terminal_wpis->살아있음)return 0;
    if(Akcja==4)czyścić_Spis_treści();if(Akcja==5||Akcja==6){unsigned Wstecz_towar=단추들;Terminal_wskaźnik(Akcja==5?8:16,0,0);단추들=Wstecz_towar;}return 1;
}
