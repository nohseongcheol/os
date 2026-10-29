#include "../명명/기계연결이름.h"
#include "../maszyna/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tablica_Terminal(uintptr_t),Tablica_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_wskaźnik(unsigned,int,int),Terminal_bajt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Porównanie_OBRAZ[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tablica_wskaźnik(0,0,0);memcpy(Porównanie_OBRAZ,화면,sizeof(화면));
    uint64_t Wstecz_towar=Tablica_rysunek_ILE_LICZB();Tablica_Terminal(3);
    assert(memcmp(Porównanie_OBRAZ,화면,sizeof(화면))==0);
    assert(Tablica_rysunek_ILE_LICZB()==Wstecz_towar); /* 같은 화면을 다시 그려도 program_WARTOŚĆ 메모리에 쓰지 않는다. */
}
static void zapis_SMS(const char *tekst){while(*tekst)Terminal_bajt((unsigned char)*tekst++);}
int main(void){
    Tablica_Przygotuj_rysunek(&화면[0][0],1920,1080,sizeof(화면[0]));
    Tablica_Terminal(300);zapis_SMS("첫 창의 한글 dane\n");
    for(int INDEKS=1;INDEKS<4;INDEKS++){Tablica_Terminal(1);Tablica_Terminal(100+INDEKS);zapis_SMS("겹친 창의 한글 dane\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,gałąź_stanowisko=102,폭=568,wysokość_WARTOŚĆ=360;
    uint64_t przenosić_LOG=0;double 이동시간=0;
    for(int SEKWENCJA_WARTOŚĆ=0;SEKWENCJA_WARTOŚĆ<80;SEKWENCJA_WARTOŚĆ++){
        Terminal_wskaźnik(1,가로+100,gałąź_stanowisko+15);
        int 새가로=80+(SEKWENCJA_WARTOŚĆ*37)%850,새세로=50+(SEKWENCJA_WARTOŚĆ*13)%450;
        Tablica_piksel(1900,1050,0x123456); /* odświeżyć region_WARTOŚĆ 밖의 przestrzeń_użytkownika rysunek_WARTOŚĆ */
        uint64_t Wstecz_towar=Tablica_rysunek_ILE_LICZB();clock_t Uruchom_2=clock();
        Terminal_wskaźnik(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Uruchom_2)/CLOCKS_PER_SEC;
        przenosić_LOG+=Tablica_rysunek_ILE_LICZB()-Wstecz_towar;
        assert(Tablica_rysunek_ILE_LICZB()-Wstecz_towar<=2u*폭*wysokość_WARTOŚĆ);
        assert(화면[1050][1900]==0x123456);
        Tablica_piksel(1900,1050,0x302018);
        Terminal_wskaźnik(0,새가로+100,새세로+15);가로=새가로;gałąź_stanowisko=새세로;
        전체와비교();
    }
    for(int SEKWENCJA_WARTOŚĆ=0;SEKWENCJA_WARTOŚĆ<40;SEKWENCJA_WARTOŚĆ++){
        int 새폭=360+(SEKWENCJA_WARTOŚĆ*29)%700,새높이=216+(SEKWENCJA_WARTOŚĆ*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-gałąź_stanowisko)새높이=1080-gałąź_stanowisko;
        Terminal_wskaźnik(1,가로+폭-4,gałąź_stanowisko+wysokość_WARTOŚĆ-4);
        Terminal_wskaźnik(1,가로+새폭-4,gałąź_stanowisko+새높이-4);
        uint64_t Wstecz_towar=Tablica_rysunek_ILE_LICZB();
        Terminal_wskaźnik(1,가로+새폭-4,gałąź_stanowisko+새높이-4);
        assert(Tablica_rysunek_ILE_LICZB()==Wstecz_towar); /* 같은 좌표의 중복 Wydarzenie */
        Terminal_wskaźnik(0,가로+새폭-4,gałąź_stanowisko+새높이-4);폭=새폭;wysokość_WARTOŚĆ=새높이;
        전체와비교();
    }
    /* 잘린 범위와 rzeczywisty_dane wiersz_wejścia 간격을 지킨다. */
    for(int wiersz_wejścia=0;wiersz_wejścia<1080;wiersz_wejścia++)for(int gniazdo_wpis=1920;gniazdo_wpis<1936;gniazdo_wpis++)assert(화면[wiersz_wejścia][gniazdo_wpis]==0);
    assert(!Tablica_START_rysunek(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(przenosić_LOG/80));
    return 0;
}
