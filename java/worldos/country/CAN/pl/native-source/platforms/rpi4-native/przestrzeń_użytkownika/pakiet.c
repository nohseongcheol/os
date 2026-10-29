#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "pakiet.h"
#include "uzlib.h"
static unsigned char Archiwum[16384], 풀린자료[16385];
static unsigned Rozmiar, 중앙목록, 항목들;
static char wpis_Klasa[256];
static unsigned 두바이트읽기(unsigned bieżący_stanowisko) { return Archiwum[bieżący_stanowisko] | Archiwum[bieżący_stanowisko+1] << 8; }
static uint32_t 네바이트읽기(unsigned bieżący_stanowisko) { return 두바이트읽기(bieżący_stanowisko) | (uint32_t)두바이트읽기(bieżący_stanowisko+2) << 16; }
static int obcinać(unsigned bieżący_stanowisko, unsigned towar_ILE_LICZB, unsigned 한도) { return bieżący_stanowisko <= 한도 && towar_ILE_LICZB <= 한도-bieżący_stanowisko; }
static size_t długość_WARTOŚĆ(const char *ciąg_dane) { size_t towar_ILE_LICZB=0; while(ciąg_dane[towar_ILE_LICZB]) towar_ILE_LICZB++; return towar_ILE_LICZB; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEKUNDA_WARTOŚĆ, unsigned towar_ILE_LICZB) { for(unsigned 순번=0;순번<towar_ILE_LICZB;순번++)if(첫째값[순번]!=SEKUNDA_WARTOŚĆ[순번])return 0;return 1; }
static int Plik_Koniec(void *미사용값) { (void)미사용값; return -1; }
static int atrybut_dane(const char *wiersz_wejścia,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)wiersz_wejścia,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)wiersz_wejścia,(const unsigned char*)"Main-Class: ",12)) {
        unsigned WARTOŚĆ=사용량-12;if(*진입점있음||!WARTOŚĆ||WARTOŚĆ>=sizeof(wpis_Klasa))return -8;
        for(unsigned 순번=0;순번<WARTOŚĆ;순번++){unsigned char kod_znaku=wiersz_wejścia[12+순번];if(kod_znaku<=32||kod_znaku=='/'||kod_znaku=='\\')return -8;wpis_Klasa[순번]=kod_znaku;}
        wpis_Klasa[WARTOŚĆ]=0;*진입점있음=1;
    }
    return 0;
}
static int członek(unsigned bieżący_stanowisko, unsigned char *KR_dane, unsigned 용량한도) {
    unsigned metoda_wpis=두바이트읽기(bieżący_stanowisko+10), konfiguracja_BITS=두바이트읽기(bieżący_stanowisko+8), 압축크기=네바이트읽기(bieżący_stanowisko+20), wersja_zmienić_rozmiar=네바이트읽기(bieżący_stanowisko+24), lokalny=네바이트읽기(bieżący_stanowisko+42);
    unsigned Nazwa=두바이트읽기(bieżący_stanowisko+28);
    if(wersja_zmienić_rozmiar>용량한도 || wersja_zmienić_rozmiar>16384 || (metoda_wpis!=0 && metoda_wpis!=8) || (konfiguracja_BITS&~0x80e))return -8;
    if(!obcinać(lokalny,30,중앙목록) || 네바이트읽기(lokalny)!=0x04034b50 || 두바이트읽기(lokalny+8)!=metoda_wpis || 두바이트읽기(lokalny+6)!=konfiguracja_BITS || 두바이트읽기(lokalny+26)!=Nazwa)return -8;
    unsigned START_przesunąć=lokalny+30, 추가영역=두바이트읽기(lokalny+28);
    if(!obcinać(START_przesunąć,Nazwa,중앙목록) || !같음(Archiwum+START_przesunąć,Archiwum+bieżący_stanowisko+46,Nazwa))return -8;
    START_przesunąć+=Nazwa;if(!obcinać(START_przesunąć,추가영역,중앙목록))return -8;START_przesunąć+=추가영역;
    if(!obcinać(START_przesunąć,압축크기,중앙목록))return -8;
    if(!(konfiguracja_BITS&8) && (네바이트읽기(lokalny+14)!=네바이트읽기(bieżący_stanowisko+16) || 네바이트읽기(lokalny+18)!=압축크기 || 네바이트읽기(lokalny+22)!=wersja_zmienić_rozmiar))return -8;
    if(metoda_wpis==0) { if(압축크기!=wersja_zmienić_rozmiar)return -8; for(unsigned 순번=0;순번<wersja_zmienić_rozmiar;순번++)KR_dane[순번]=Archiwum[START_przesunąć+순번]; }
    else {
        uzlib_uncomp_t cel_dane={0};uzlib_uncompress_init(&cel_dane,0,0);
        cel_dane.source=Archiwum+START_przesunąć;cel_dane.source_limit=cel_dane.source+압축크기;cel_dane.source_read_cb=Plik_Koniec;
        /* One extra output byte lets inflate consume/check the end marker. */
        cel_dane.dest_start=cel_dane.dest=풀린자료;cel_dane.dest_limit=풀린자료+wersja_zmienić_rozmiar+1;
        int 반환값=uzlib_uncompress(&cel_dane);
        if(반환값!=UZLIB_DONE || cel_dane.eof || cel_dane.dest!=풀린자료+wersja_zmienić_rozmiar || cel_dane.source!=cel_dane.source_limit)return -8;
        for(unsigned 순번=0;순번<wersja_zmienić_rozmiar;순번++)KR_dane[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_dane,wersja_zmienić_rozmiar,0xffffffffu)^0xffffffffu)!=네바이트읽기(bieżący_stanowisko+16))return -8;
    return wersja_zmienić_rozmiar;
}
int 꾸러미읽기(const char *Nazwa, unsigned char *KR_dane, unsigned bufor_pojemność) {
    if(!항목들)return -2;unsigned towar_ILE_LICZB=długość_WARTOŚĆ(Nazwa),bieżący_stanowisko=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(bieżący_stanowisko+28);
        if(이름길이==towar_ILE_LICZB && 같음(Archiwum+bieżący_stanowisko+46,(const unsigned char*)Nazwa,towar_ILE_LICZB))return członek(bieżący_stanowisko,KR_dane,bufor_pojemność);
        bieżący_stanowisko+=46+이름길이+두바이트읽기(bieżący_stanowisko+30)+두바이트읽기(bieżący_stanowisko+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return wpis_Klasa; }
int 꾸러미열기(const char *Plik_wpis_nazwa) {
    항목들=0;wpis_Klasa[0]=0;
    intptr_t dojście_do_pliku=사용자호출(3,(uintptr_t)Plik_wpis_nazwa,0,0,0,0,0);if(dojście_do_pliku<0)return dojście_do_pliku;
    intptr_t towar_ILE_LICZB=사용자호출(9,dojście_do_pliku,0,0,0,0,0);
    if(towar_ILE_LICZB<22 || towar_ILE_LICZB>(intptr_t)sizeof(Archiwum)) { 사용자호출(4,dojście_do_pliku,0,0,0,0,0);return -8; }
    intptr_t KWOTA_WYKUP_ILE_LICZB=사용자호출(2,dojście_do_pliku,(uintptr_t)Archiwum,towar_ILE_LICZB,0,0,0);사용자호출(4,dojście_do_pliku,0,0,0,0,0);
    if(KWOTA_WYKUP_ILE_LICZB!=towar_ILE_LICZB)return -5;Rozmiar=towar_ILE_LICZB;
    unsigned Koniec_przesunąć=Rozmiar-22;
    for(;;) { if(네바이트읽기(Koniec_przesunąć)==0x06054b50 && Koniec_przesunąć+22+두바이트읽기(Koniec_przesunąć+20)==Rozmiar)break; if(!Koniec_przesunąć)return -8;Koniec_przesunąć--; }
    unsigned wpis_ILE_LICZB=두바이트읽기(Koniec_przesunąć+10);중앙목록=네바이트읽기(Koniec_przesunąć+16);
    if(두바이트읽기(Koniec_przesunąć+4)||두바이트읽기(Koniec_przesunąć+6)||두바이트읽기(Koniec_przesunąć+8)!=wpis_ILE_LICZB||!wpis_ILE_LICZB||wpis_ILE_LICZB>256||!obcinać(중앙목록,네바이트읽기(Koniec_przesunąć+12),Koniec_przesunąć)||중앙목록+네바이트읽기(Koniec_przesunąć+12)!=Koniec_przesunąć)return -8;
    unsigned bieżący_stanowisko=중앙목록;
    for(unsigned 순번=0;순번<wpis_ILE_LICZB;순번++) {
        if(!obcinać(bieżący_stanowisko,46,Koniec_przesunąć)||네바이트읽기(bieżący_stanowisko)!=0x02014b50||두바이트읽기(bieżący_stanowisko+34))return -8;
        unsigned 이름길이=두바이트읽기(bieżący_stanowisko+28),Dalej_towar=46+이름길이+두바이트읽기(bieżący_stanowisko+30)+두바이트읽기(bieżący_stanowisko+32);
        if(!이름길이||이름길이>511||!obcinać(bieżący_stanowisko,Dalej_towar,Koniec_przesunąć)||네바이트읽기(bieżący_stanowisko+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archiwum[bieżący_stanowisko+46+안쪽순번])return -8;
        unsigned Inne_wpis=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned długość_dane=두바이트읽기(Inne_wpis+28);if(długość_dane==이름길이&&같음(Archiwum+Inne_wpis+46,Archiwum+bieżący_stanowisko+46,długość_dane))return -8;Inne_wpis+=46+długość_dane+두바이트읽기(Inne_wpis+30)+두바이트읽기(Inne_wpis+32);}
        bieżący_stanowisko+=Dalej_towar;
    }
    if(bieżący_stanowisko!=Koniec_przesunąć)return -8;항목들=wpis_ILE_LICZB;
    unsigned char pakiet_manifest[4096];int grupa_zmienić_rozmiar=꾸러미읽기("META-INF/MANIFEST.MF",pakiet_manifest,sizeof(pakiet_manifest)-1);if(grupa_zmienić_rozmiar<0){항목들=0;return -8;}
    pakiet_manifest[grupa_zmienić_rozmiar]=0;
    char 논리크기[512];unsigned 사용량=0,INDEKS_WARTOŚĆ=0;int 진입점있음=0;
    while(INDEKS_WARTOŚĆ<(unsigned)grupa_zmienić_rozmiar) {
        unsigned Uruchom_2=INDEKS_WARTOŚĆ;while(INDEKS_WARTOŚĆ<(unsigned)grupa_zmienić_rozmiar && pakiet_manifest[INDEKS_WARTOŚĆ]!='\n')INDEKS_WARTOŚĆ++;
        unsigned długość_dane=INDEKS_WARTOŚĆ-Uruchom_2;if(INDEKS_WARTOŚĆ<(unsigned)grupa_zmienić_rozmiar)INDEKS_WARTOŚĆ++;if(długość_dane && pakiet_manifest[Uruchom_2+długość_dane-1]=='\r')długość_dane--;
        if(사용량 && długość_dane && pakiet_manifest[Uruchom_2]==' ') {Uruchom_2++;długość_dane--;}
        else {
            int WYNIK=atrybut_dane(논리크기,사용량,&진입점있음);if(WYNIK)return WYNIK;
            사용량=0;if(!długość_dane)break;
        }
        if(długość_dane>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<długość_dane;순번++)논리크기[사용량++]=pakiet_manifest[Uruchom_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int WYNIK=atrybut_dane(논리크기,사용량,&진입점있음);if(WYNIK)return WYNIK;
    return 진입점있음?0:-8;
}
