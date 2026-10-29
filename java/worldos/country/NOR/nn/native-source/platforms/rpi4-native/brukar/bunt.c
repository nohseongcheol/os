#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bunt.h"
#include "uzlib.h"
static unsigned char Arkiv[16384], 풀린자료[16385];
static unsigned Storleik, 중앙목록, 항목들;
static char oppføring_time[256];
static unsigned 두바이트읽기(unsigned betalt_plassere) { return Arkiv[betalt_plassere] | Arkiv[betalt_plassere+1] << 8; }
static uint32_t 네바이트읽기(unsigned betalt_plassere) { return 두바이트읽기(betalt_plassere) | (uint32_t)두바이트읽기(betalt_plassere+2) << 16; }
static int klipp(unsigned betalt_plassere, unsigned vare_COUNT, unsigned 한도) { return betalt_plassere <= 한도 && vare_COUNT <= 한도-betalt_plassere; }
static size_t lengd_VALUE(const char *streng_data) { size_t vare_COUNT=0; while(streng_data[vare_COUNT]) vare_COUNT++; return vare_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned vare_COUNT) { for(unsigned 순번=0;순번<vare_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int fil_avslutte(void *미사용값) { (void)미사용값; return -1; }
static int attributt_data(const char *linje,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)linje,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)linje,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(oppføring_time))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char teiknkode=linje[12+순번];if(teiknkode<=32||teiknkode=='/'||teiknkode=='\\')return -8;oppføring_time[순번]=teiknkode;}
        oppføring_time[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int medlem(unsigned betalt_plassere, unsigned char *forretningsmål_data, unsigned 용량한도) {
    unsigned metode_oppføring=두바이트읽기(betalt_plassere+10), 설정비트=두바이트읽기(betalt_plassere+8), 압축크기=네바이트읽기(betalt_plassere+20), frigi_endre_storleik=네바이트읽기(betalt_plassere+24), lokal=네바이트읽기(betalt_plassere+42);
    unsigned Namn=두바이트읽기(betalt_plassere+28);
    if(frigi_endre_storleik>용량한도 || frigi_endre_storleik>16384 || (metode_oppføring!=0 && metode_oppføring!=8) || (설정비트&~0x80e))return -8;
    if(!klipp(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metode_oppføring || 두바이트읽기(lokal+6)!=설정비트 || 두바이트읽기(lokal+26)!=Namn)return -8;
    unsigned START_OFFSET=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klipp(START_OFFSET,Namn,중앙목록) || !같음(Arkiv+START_OFFSET,Arkiv+betalt_plassere+46,Namn))return -8;
    START_OFFSET+=Namn;if(!klipp(START_OFFSET,추가영역,중앙목록))return -8;START_OFFSET+=추가영역;
    if(!klipp(START_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(lokal+14)!=네바이트읽기(betalt_plassere+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=frigi_endre_storleik))return -8;
    if(metode_oppføring==0) { if(압축크기!=frigi_endre_storleik)return -8; for(unsigned 순번=0;순번<frigi_endre_storleik;순번++)forretningsmål_data[순번]=Arkiv[START_OFFSET+순번]; }
    else {
        uzlib_uncomp_t mål_data={0};uzlib_uncompress_init(&mål_data,0,0);
        mål_data.source=Arkiv+START_OFFSET;mål_data.source_limit=mål_data.source+압축크기;mål_data.source_read_cb=fil_avslutte;
        /* One extra output byte lets inflate consume/check the end marker. */
        mål_data.dest_start=mål_data.dest=풀린자료;mål_data.dest_limit=풀린자료+frigi_endre_storleik+1;
        int 반환값=uzlib_uncompress(&mål_data);
        if(반환값!=UZLIB_DONE || mål_data.eof || mål_data.dest!=풀린자료+frigi_endre_storleik || mål_data.source!=mål_data.source_limit)return -8;
        for(unsigned 순번=0;순번<frigi_endre_storleik;순번++)forretningsmål_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(forretningsmål_data,frigi_endre_storleik,0xffffffffu)^0xffffffffu)!=네바이트읽기(betalt_plassere+16))return -8;
    return frigi_endre_storleik;
}
int 꾸러미읽기(const char *Namn, unsigned char *forretningsmål_data, unsigned 수용량) {
    if(!항목들)return -2;unsigned vare_COUNT=lengd_VALUE(Namn),betalt_plassere=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(betalt_plassere+28);
        if(이름길이==vare_COUNT && 같음(Arkiv+betalt_plassere+46,(const unsigned char*)Namn,vare_COUNT))return medlem(betalt_plassere,forretningsmål_data,수용량);
        betalt_plassere+=46+이름길이+두바이트읽기(betalt_plassere+30)+두바이트읽기(betalt_plassere+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return oppføring_time; }
int 꾸러미열기(const char *fil_oppføring_namn) {
    항목들=0;oppføring_time[0]=0;
    intptr_t fil_handtak=사용자호출(3,(uintptr_t)fil_oppføring_namn,0,0,0,0,0);if(fil_handtak<0)return fil_handtak;
    intptr_t vare_COUNT=사용자호출(9,fil_handtak,0,0,0,0,0);
    if(vare_COUNT<22 || vare_COUNT>(intptr_t)sizeof(Arkiv)) { 사용자호출(4,fil_handtak,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,fil_handtak,(uintptr_t)Arkiv,vare_COUNT,0,0,0);사용자호출(4,fil_handtak,0,0,0,0,0);
    if(RECEIVED_COUNT!=vare_COUNT)return -5;Storleik=vare_COUNT;
    unsigned avslutte_OFFSET=Storleik-22;
    for(;;) { if(네바이트읽기(avslutte_OFFSET)==0x06054b50 && avslutte_OFFSET+22+두바이트읽기(avslutte_OFFSET+20)==Storleik)break; if(!avslutte_OFFSET)return -8;avslutte_OFFSET--; }
    unsigned oppføring_COUNT=두바이트읽기(avslutte_OFFSET+10);중앙목록=네바이트읽기(avslutte_OFFSET+16);
    if(두바이트읽기(avslutte_OFFSET+4)||두바이트읽기(avslutte_OFFSET+6)||두바이트읽기(avslutte_OFFSET+8)!=oppføring_COUNT||!oppføring_COUNT||oppføring_COUNT>256||!klipp(중앙목록,네바이트읽기(avslutte_OFFSET+12),avslutte_OFFSET)||중앙목록+네바이트읽기(avslutte_OFFSET+12)!=avslutte_OFFSET)return -8;
    unsigned betalt_plassere=중앙목록;
    for(unsigned 순번=0;순번<oppføring_COUNT;순번++) {
        if(!klipp(betalt_plassere,46,avslutte_OFFSET)||네바이트읽기(betalt_plassere)!=0x02014b50||두바이트읽기(betalt_plassere+34))return -8;
        unsigned 이름길이=두바이트읽기(betalt_plassere+28),Neste_vare=46+이름길이+두바이트읽기(betalt_plassere+30)+두바이트읽기(betalt_plassere+32);
        if(!이름길이||이름길이>511||!klipp(betalt_plassere,Neste_vare,avslutte_OFFSET)||네바이트읽기(betalt_plassere+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkiv[betalt_plassere+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned lengd_data=두바이트읽기(다른항목+28);if(lengd_data==이름길이&&같음(Arkiv+다른항목+46,Arkiv+betalt_plassere+46,lengd_data))return -8;다른항목+=46+lengd_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        betalt_plassere+=Neste_vare;
    }
    if(betalt_plassere!=avslutte_OFFSET)return -8;항목들=oppføring_COUNT;
    unsigned char 꾸러미명세[4096];int gruppe_endre_storleik=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(gruppe_endre_storleik<0){항목들=0;return -8;}
    꾸러미명세[gruppe_endre_storleik]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)gruppe_endre_storleik) {
        unsigned Køyr_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)gruppe_endre_storleik && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned lengd_data=INDEX_VALUE-Køyr_2;if(INDEX_VALUE<(unsigned)gruppe_endre_storleik)INDEX_VALUE++;if(lengd_data && 꾸러미명세[Køyr_2+lengd_data-1]=='\r')lengd_data--;
        if(사용량 && lengd_data && 꾸러미명세[Køyr_2]==' ') {Køyr_2++;lengd_data--;}
        else {
            int forretningsmål=attributt_data(논리크기,사용량,&진입점있음);if(forretningsmål)return forretningsmål;
            사용량=0;if(!lengd_data)break;
        }
        if(lengd_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<lengd_data;순번++)논리크기[사용량++]=꾸러미명세[Køyr_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int forretningsmål=attributt_data(논리크기,사용량,&진입점있음);if(forretningsmål)return forretningsmål;
    return 진입점있음?0:-8;
}
