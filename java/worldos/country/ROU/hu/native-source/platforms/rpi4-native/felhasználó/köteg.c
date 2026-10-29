#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "köteg.h"
#include "uzlib.h"
static unsigned char archív[16384], 풀린자료[16385];
static unsigned Méret, 중앙목록, 항목들;
static char bejegyzés_tanóra[256];
static unsigned 두바이트읽기(unsigned aktuális_pozíció) { return archív[aktuális_pozíció] | archív[aktuális_pozíció+1] << 8; }
static uint32_t 네바이트읽기(unsigned aktuális_pozíció) { return 두바이트읽기(aktuális_pozíció) | (uint32_t)두바이트읽기(aktuális_pozíció+2) << 16; }
static int klip(unsigned aktuális_pozíció, unsigned cikk_DARAB, unsigned 한도) { return aktuális_pozíció <= 한도 && cikk_DARAB <= 한도-aktuális_pozíció; }
static size_t hossz_ÉRTÉK(const char *sztring_adat) { size_t cikk_DARAB=0; while(sztring_adat[cikk_DARAB]) cikk_DARAB++; return cikk_DARAB; }
static int 같음(const unsigned char *첫째값, const unsigned char *MPERC_ÉRTÉK, unsigned cikk_DARAB) { for(unsigned 순번=0;순번<cikk_DARAB;순번++)if(첫째값[순번]!=MPERC_ÉRTÉK[순번])return 0;return 1; }
static int Fájl_megszüntet(void *미사용값) { (void)미사용값; return -1; }
static int attribútum_adat(const char *Vonal,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Vonal,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Vonal,(const unsigned char*)"Main-Class: ",12)) {
        unsigned ÉRTÉK=사용량-12;if(*진입점있음||!ÉRTÉK||ÉRTÉK>=sizeof(bejegyzés_tanóra))return -8;
        for(unsigned 순번=0;순번<ÉRTÉK;순번++){unsigned char kódpont=Vonal[12+순번];if(kódpont<=32||kódpont=='/'||kódpont=='\\')return -8;bejegyzés_tanóra[순번]=kódpont;}
        bejegyzés_tanóra[ÉRTÉK]=0;*진입점있음=1;
    }
    return 0;
}
static int tag(unsigned aktuális_pozíció, unsigned char *KR_adat, unsigned 용량한도) {
    unsigned metódus_bejegyzés=두바이트읽기(aktuális_pozíció+10), konfiguráció_BITS=두바이트읽기(aktuális_pozíció+8), 압축크기=네바이트읽기(aktuális_pozíció+20), kiad_méretez=네바이트읽기(aktuális_pozíció+24), helyi=네바이트읽기(aktuális_pozíció+42);
    unsigned Név=두바이트읽기(aktuális_pozíció+28);
    if(kiad_méretez>용량한도 || kiad_méretez>16384 || (metódus_bejegyzés!=0 && metódus_bejegyzés!=8) || (konfiguráció_BITS&~0x80e))return -8;
    if(!klip(helyi,30,중앙목록) || 네바이트읽기(helyi)!=0x04034b50 || 두바이트읽기(helyi+8)!=metódus_bejegyzés || 두바이트읽기(helyi+6)!=konfiguráció_BITS || 두바이트읽기(helyi+26)!=Név)return -8;
    unsigned START_Ofszet=helyi+30, 추가영역=두바이트읽기(helyi+28);
    if(!klip(START_Ofszet,Név,중앙목록) || !같음(archív+START_Ofszet,archív+aktuális_pozíció+46,Név))return -8;
    START_Ofszet+=Név;if(!klip(START_Ofszet,추가영역,중앙목록))return -8;START_Ofszet+=추가영역;
    if(!klip(START_Ofszet,압축크기,중앙목록))return -8;
    if(!(konfiguráció_BITS&8) && (네바이트읽기(helyi+14)!=네바이트읽기(aktuális_pozíció+16) || 네바이트읽기(helyi+18)!=압축크기 || 네바이트읽기(helyi+22)!=kiad_méretez))return -8;
    if(metódus_bejegyzés==0) { if(압축크기!=kiad_méretez)return -8; for(unsigned 순번=0;순번<kiad_méretez;순번++)KR_adat[순번]=archív[START_Ofszet+순번]; }
    else {
        uzlib_uncomp_t cél_adat={0};uzlib_uncompress_init(&cél_adat,0,0);
        cél_adat.source=archív+START_Ofszet;cél_adat.source_limit=cél_adat.source+압축크기;cél_adat.source_read_cb=Fájl_megszüntet;
        /* One extra output byte lets inflate consume/check the end marker. */
        cél_adat.dest_start=cél_adat.dest=풀린자료;cél_adat.dest_limit=풀린자료+kiad_méretez+1;
        int 반환값=uzlib_uncompress(&cél_adat);
        if(반환값!=UZLIB_DONE || cél_adat.eof || cél_adat.dest!=풀린자료+kiad_méretez || cél_adat.source!=cél_adat.source_limit)return -8;
        for(unsigned 순번=0;순번<kiad_méretez;순번++)KR_adat[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_adat,kiad_méretez,0xffffffffu)^0xffffffffu)!=네바이트읽기(aktuális_pozíció+16))return -8;
    return kiad_méretez;
}
int 꾸러미읽기(const char *Név, unsigned char *KR_adat, unsigned puffer_kapacitás) {
    if(!항목들)return -2;unsigned cikk_DARAB=hossz_ÉRTÉK(Név),aktuális_pozíció=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(aktuális_pozíció+28);
        if(이름길이==cikk_DARAB && 같음(archív+aktuális_pozíció+46,(const unsigned char*)Név,cikk_DARAB))return tag(aktuális_pozíció,KR_adat,puffer_kapacitás);
        aktuális_pozíció+=46+이름길이+두바이트읽기(aktuális_pozíció+30)+두바이트읽기(aktuális_pozíció+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return bejegyzés_tanóra; }
int 꾸러미열기(const char *Fájl_bejegyzés_név) {
    항목들=0;bejegyzés_tanóra[0]=0;
    intptr_t fájlleíró=사용자호출(3,(uintptr_t)Fájl_bejegyzés_név,0,0,0,0,0);if(fájlleíró<0)return fájlleíró;
    intptr_t cikk_DARAB=사용자호출(9,fájlleíró,0,0,0,0,0);
    if(cikk_DARAB<22 || cikk_DARAB>(intptr_t)sizeof(archív)) { 사용자호출(4,fájlleíró,0,0,0,0,0);return -8; }
    intptr_t KAPOTT_DARAB=사용자호출(2,fájlleíró,(uintptr_t)archív,cikk_DARAB,0,0,0);사용자호출(4,fájlleíró,0,0,0,0,0);
    if(KAPOTT_DARAB!=cikk_DARAB)return -5;Méret=cikk_DARAB;
    unsigned megszüntet_Ofszet=Méret-22;
    for(;;) { if(네바이트읽기(megszüntet_Ofszet)==0x06054b50 && megszüntet_Ofszet+22+두바이트읽기(megszüntet_Ofszet+20)==Méret)break; if(!megszüntet_Ofszet)return -8;megszüntet_Ofszet--; }
    unsigned bejegyzés_DARAB=두바이트읽기(megszüntet_Ofszet+10);중앙목록=네바이트읽기(megszüntet_Ofszet+16);
    if(두바이트읽기(megszüntet_Ofszet+4)||두바이트읽기(megszüntet_Ofszet+6)||두바이트읽기(megszüntet_Ofszet+8)!=bejegyzés_DARAB||!bejegyzés_DARAB||bejegyzés_DARAB>256||!klip(중앙목록,네바이트읽기(megszüntet_Ofszet+12),megszüntet_Ofszet)||중앙목록+네바이트읽기(megszüntet_Ofszet+12)!=megszüntet_Ofszet)return -8;
    unsigned aktuális_pozíció=중앙목록;
    for(unsigned 순번=0;순번<bejegyzés_DARAB;순번++) {
        if(!klip(aktuális_pozíció,46,megszüntet_Ofszet)||네바이트읽기(aktuális_pozíció)!=0x02014b50||두바이트읽기(aktuális_pozíció+34))return -8;
        unsigned 이름길이=두바이트읽기(aktuális_pozíció+28),Tovább_cikk=46+이름길이+두바이트읽기(aktuális_pozíció+30)+두바이트읽기(aktuális_pozíció+32);
        if(!이름길이||이름길이>511||!klip(aktuális_pozíció,Tovább_cikk,megszüntet_Ofszet)||네바이트읽기(aktuális_pozíció+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!archív[aktuális_pozíció+46+안쪽순번])return -8;
        unsigned Egyéb_bejegyzés=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned hossz_adat=두바이트읽기(Egyéb_bejegyzés+28);if(hossz_adat==이름길이&&같음(archív+Egyéb_bejegyzés+46,archív+aktuális_pozíció+46,hossz_adat))return -8;Egyéb_bejegyzés+=46+hossz_adat+두바이트읽기(Egyéb_bejegyzés+30)+두바이트읽기(Egyéb_bejegyzés+32);}
        aktuális_pozíció+=Tovább_cikk;
    }
    if(aktuális_pozíció!=megszüntet_Ofszet)return -8;항목들=bejegyzés_DARAB;
    unsigned char köteg_jegyzékfájl[4096];int Csoport_méretez=꾸러미읽기("META-INF/MANIFEST.MF",köteg_jegyzékfájl,sizeof(köteg_jegyzékfájl)-1);if(Csoport_méretez<0){항목들=0;return -8;}
    köteg_jegyzékfájl[Csoport_méretez]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_ÉRTÉK=0;int 진입점있음=0;
    while(INDEX_ÉRTÉK<(unsigned)Csoport_méretez) {
        unsigned Futtatás=INDEX_ÉRTÉK;while(INDEX_ÉRTÉK<(unsigned)Csoport_méretez && köteg_jegyzékfájl[INDEX_ÉRTÉK]!='\n')INDEX_ÉRTÉK++;
        unsigned hossz_adat=INDEX_ÉRTÉK-Futtatás;if(INDEX_ÉRTÉK<(unsigned)Csoport_méretez)INDEX_ÉRTÉK++;if(hossz_adat && köteg_jegyzékfájl[Futtatás+hossz_adat-1]=='\r')hossz_adat--;
        if(사용량 && hossz_adat && köteg_jegyzékfájl[Futtatás]==' ') {Futtatás++;hossz_adat--;}
        else {
            int KR=attribútum_adat(논리크기,사용량,&진입점있음);if(KR)return KR;
            사용량=0;if(!hossz_adat)break;
        }
        if(hossz_adat>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<hossz_adat;순번++)논리크기[사용량++]=köteg_jegyzékfájl[Futtatás+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int KR=attribútum_adat(논리크기,사용량,&진입점있음);if(KR)return KR;
    return 진입점있음?0:-8;
}
