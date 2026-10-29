#include "../benennung/maschineBindenNamen.h"
#include "../maschine/bildschirmInformation.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void betriebskernNotstopp(const char *beschreibung){fputs(beschreibung,stderr);abort();}
extern uintptr_t platineTerminal(uintptr_t),platineBildpunkt(uintptr_t,uintptr_t,uintptr_t);
extern void terminalZeiger(unsigned,int,int),terminalByte(unsigned);
extern int bildschirmAufrufen(int,unsigned,int,int,int,int,int);
static uint32_t Bildschirm[1080][1936],vergleichAbbild[1080][1936];
uintptr_t platineBildpuffer(void){return 1;}
static void gesamtVergleichAnstellen(void){
    platineZeiger(0,0,0);memcpy(vergleichAbbild,Bildschirm,sizeof(Bildschirm));
    uint64_t vorherigElementeintrag=platineZeichnungAnzahl();platineTerminal(3);
    assert(memcmp(vergleichAbbild,Bildschirm,sizeof(Bildschirm))==0);
    assert(platineZeichnungAnzahl()==vorherigElementeintrag); /* 같은 화면을 erneutVersuchenWert 그려도 wertAnzeigen 메모리에 쓰지 않는다. */
}
static void textSchreiben(const char *Text){while(*Text)terminalByte((unsigned char)*Text++);}
int main(void){
    platineVorbereitenZeichnung(&Bildschirm[0][0],1920,1080,sizeof(Bildschirm[0]));
    platineTerminal(300);textSchreiben("ersterElementeintrag 창의 한글 Daten\n");
    for(int Nummer=1;Nummer<4;Nummer++){platineTerminal(1);platineTerminal(100+Nummer);textSchreiben("겹친 창의 한글 Daten\n\033[41m색칠한 leerraumÜberspringen     \033[0m\n");}
    gesamtVergleichAnstellen();
    int waagerechtPosition=60,senkrechtPosition=102,breiteSpannweite=568,höheWert=360;
    uint64_t bewegenProtokolldatei=0;double bewegungZeit=0;
    for(int folgeWert=0;folgeWert<80;folgeWert++){
        terminalZeiger(1,waagerechtPosition+100,senkrechtPosition+15);
        int neuWaagerechtPosition=80+(folgeWert*37)%850,neuSenkrechtPosition=50+(folgeWert*13)%450;
        platineBildpunkt(1900,1050,0x123456); /* auffrischen gebietWert 밖의 Benutzer Zeichnung */
        uint64_t vorherigElementeintrag=platineZeichnungAnzahl();clock_t ausführenVorgang=clock();
        terminalZeiger(1,neuWaagerechtPosition+100,neuSenkrechtPosition+15);
        bewegungZeit+=(double)(clock()-ausführenVorgang)/CLOCKS_PER_SEC;
        bewegenProtokolldatei+=platineZeichnungAnzahl()-vorherigElementeintrag;
        assert(platineZeichnungAnzahl()-vorherigElementeintrag<=2u*breiteSpannweite*höheWert);
        assert(Bildschirm[1050][1900]==0x123456);
        platineBildpunkt(1900,1050,0x302018);
        terminalZeiger(0,neuWaagerechtPosition+100,neuSenkrechtPosition+15);waagerechtPosition=neuWaagerechtPosition;senkrechtPosition=neuSenkrechtPosition;
        gesamtVergleichAnstellen();
    }
    for(int folgeWert=0;folgeWert<40;folgeWert++){
        int neuBreite=360+(folgeWert*29)%700,neuHöhe=216+(folgeWert*17)%350;
        if(neuBreite>1920-waagerechtPosition)neuBreite=1920-waagerechtPosition;if(neuHöhe>1080-senkrechtPosition)neuHöhe=1080-senkrechtPosition;
        terminalZeiger(1,waagerechtPosition+breiteSpannweite-4,senkrechtPosition+höheWert-4);
        terminalZeiger(1,waagerechtPosition+neuBreite-4,senkrechtPosition+neuHöhe-4);
        uint64_t vorherigElementeintrag=platineZeichnungAnzahl();
        terminalZeiger(1,waagerechtPosition+neuBreite-4,senkrechtPosition+neuHöhe-4);
        assert(platineZeichnungAnzahl()==vorherigElementeintrag); /* 같은 좌표의 중복 ereignis */
        terminalZeiger(0,waagerechtPosition+neuBreite-4,senkrechtPosition+neuHöhe-4);breiteSpannweite=neuBreite;höheWert=neuHöhe;
        gesamtVergleichAnstellen();
    }
    /* beschnittenWert 범위와 tatsächlichDaten zeile 간격을 지킨다. */
    for(int zeile=0;zeile<1080;zeile++)for(int platzEintrag=1920;platzEintrag<1936;platzEintrag++)assert(Bildschirm[zeile][platzEintrag]==0);
    assert(!platineStartenZeichnung(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",bewegungZeit*1000/80,(unsigned long long)(bewegenProtokolldatei/80));
    return 0;
}
