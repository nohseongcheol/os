#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bondel.h"
#include "uzlib.h"
static unsigned char Argief[16384], 풀린자료[16385];
static unsigned Grootte, 중앙목록, 항목들;
static char inskrywing_Klas[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Argief[현재위치] | Argief[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int snit(unsigned 현재위치, unsigned item_COUNT, unsigned 한도) { return 현재위치 <= 한도 && item_COUNT <= 한도-현재위치; }
static size_t lengte_VALUE(const char *string_data) { size_t item_COUNT=0; while(string_data[item_COUNT]) item_COUNT++; return item_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned item_COUNT) { for(unsigned 순번=0;순번<item_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int lêer_beëindig(void *미사용값) { (void)미사용값; return -1; }
static int kenmerk_data(const char *lyn,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)lyn,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)lyn,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(inskrywing_Klas))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char karakterkode=lyn[12+순번];if(karakterkode<=32||karakterkode=='/'||karakterkode=='\\')return -8;inskrywing_Klas[순번]=karakterkode;}
        inskrywing_Klas[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int lid(unsigned 현재위치, unsigned char *maatreël_data, unsigned 용량한도) {
    unsigned metode_inskrywing=두바이트읽기(현재위치+10), konfigurasie_Agtergrond_intelligente_oordragdiens=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), stel_vry_verstel=네바이트읽기(현재위치+24), lokaal=네바이트읽기(현재위치+42);
    unsigned Naam=두바이트읽기(현재위치+28);
    if(stel_vry_verstel>용량한도 || stel_vry_verstel>16384 || (metode_inskrywing!=0 && metode_inskrywing!=8) || (konfigurasie_Agtergrond_intelligente_oordragdiens&~0x80e))return -8;
    if(!snit(lokaal,30,중앙목록) || 네바이트읽기(lokaal)!=0x04034b50 || 두바이트읽기(lokaal+8)!=metode_inskrywing || 두바이트읽기(lokaal+6)!=konfigurasie_Agtergrond_intelligente_oordragdiens || 두바이트읽기(lokaal+26)!=Naam)return -8;
    unsigned BEGIN_OFFSET=lokaal+30, 추가영역=두바이트읽기(lokaal+28);
    if(!snit(BEGIN_OFFSET,Naam,중앙목록) || !같음(Argief+BEGIN_OFFSET,Argief+현재위치+46,Naam))return -8;
    BEGIN_OFFSET+=Naam;if(!snit(BEGIN_OFFSET,추가영역,중앙목록))return -8;BEGIN_OFFSET+=추가영역;
    if(!snit(BEGIN_OFFSET,압축크기,중앙목록))return -8;
    if(!(konfigurasie_Agtergrond_intelligente_oordragdiens&8) && (네바이트읽기(lokaal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokaal+18)!=압축크기 || 네바이트읽기(lokaal+22)!=stel_vry_verstel))return -8;
    if(metode_inskrywing==0) { if(압축크기!=stel_vry_verstel)return -8; for(unsigned 순번=0;순번<stel_vry_verstel;순번++)maatreël_data[순번]=Argief[BEGIN_OFFSET+순번]; }
    else {
        uzlib_uncomp_t bestemming_data={0};uzlib_uncompress_init(&bestemming_data,0,0);
        bestemming_data.source=Argief+BEGIN_OFFSET;bestemming_data.source_limit=bestemming_data.source+압축크기;bestemming_data.source_read_cb=lêer_beëindig;
        /* One extra output byte lets inflate consume/check the end marker. */
        bestemming_data.dest_start=bestemming_data.dest=풀린자료;bestemming_data.dest_limit=풀린자료+stel_vry_verstel+1;
        int 반환값=uzlib_uncompress(&bestemming_data);
        if(반환값!=UZLIB_DONE || bestemming_data.eof || bestemming_data.dest!=풀린자료+stel_vry_verstel || bestemming_data.source!=bestemming_data.source_limit)return -8;
        for(unsigned 순번=0;순번<stel_vry_verstel;순번++)maatreël_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(maatreël_data,stel_vry_verstel,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return stel_vry_verstel;
}
int 꾸러미읽기(const char *Naam, unsigned char *maatreël_data, unsigned 수용량) {
    if(!항목들)return -2;unsigned item_COUNT=lengte_VALUE(Naam),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==item_COUNT && 같음(Argief+현재위치+46,(const unsigned char*)Naam,item_COUNT))return lid(현재위치,maatreël_data,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return inskrywing_Klas; }
int 꾸러미열기(const char *lêer_inskrywing_naam) {
    항목들=0;inskrywing_Klas[0]=0;
    intptr_t lêer_handvatsel=사용자호출(3,(uintptr_t)lêer_inskrywing_naam,0,0,0,0,0);if(lêer_handvatsel<0)return lêer_handvatsel;
    intptr_t item_COUNT=사용자호출(9,lêer_handvatsel,0,0,0,0,0);
    if(item_COUNT<22 || item_COUNT>(intptr_t)sizeof(Argief)) { 사용자호출(4,lêer_handvatsel,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,lêer_handvatsel,(uintptr_t)Argief,item_COUNT,0,0,0);사용자호출(4,lêer_handvatsel,0,0,0,0,0);
    if(RECEIVED_COUNT!=item_COUNT)return -5;Grootte=item_COUNT;
    unsigned beëindig_OFFSET=Grootte-22;
    for(;;) { if(네바이트읽기(beëindig_OFFSET)==0x06054b50 && beëindig_OFFSET+22+두바이트읽기(beëindig_OFFSET+20)==Grootte)break; if(!beëindig_OFFSET)return -8;beëindig_OFFSET--; }
    unsigned inskrywing_COUNT=두바이트읽기(beëindig_OFFSET+10);중앙목록=네바이트읽기(beëindig_OFFSET+16);
    if(두바이트읽기(beëindig_OFFSET+4)||두바이트읽기(beëindig_OFFSET+6)||두바이트읽기(beëindig_OFFSET+8)!=inskrywing_COUNT||!inskrywing_COUNT||inskrywing_COUNT>256||!snit(중앙목록,네바이트읽기(beëindig_OFFSET+12),beëindig_OFFSET)||중앙목록+네바이트읽기(beëindig_OFFSET+12)!=beëindig_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<inskrywing_COUNT;순번++) {
        if(!snit(현재위치,46,beëindig_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Volgende_item=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!snit(현재위치,Volgende_item,beëindig_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Argief[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned lengte_data=두바이트읽기(다른항목+28);if(lengte_data==이름길이&&같음(Argief+다른항목+46,Argief+현재위치+46,lengte_data))return -8;다른항목+=46+lengte_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Volgende_item;
    }
    if(현재위치!=beëindig_OFFSET)return -8;항목들=inskrywing_COUNT;
    unsigned char 꾸러미명세[4096];int Groep_verstel=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Groep_verstel<0){항목들=0;return -8;}
    꾸러미명세[Groep_verstel]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Groep_verstel) {
        unsigned Loop=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Groep_verstel && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned lengte_data=INDEX_VALUE-Loop;if(INDEX_VALUE<(unsigned)Groep_verstel)INDEX_VALUE++;if(lengte_data && 꾸러미명세[Loop+lengte_data-1]=='\r')lengte_data--;
        if(사용량 && lengte_data && 꾸러미명세[Loop]==' ') {Loop++;lengte_data--;}
        else {
            int maatreël=kenmerk_data(논리크기,사용량,&진입점있음);if(maatreël)return maatreël;
            사용량=0;if(!lengte_data)break;
        }
        if(lengte_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<lengte_data;순번++)논리크기[사용량++]=꾸러미명세[Loop+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int maatreël=kenmerk_data(논리크기,사용량,&진입점있음);if(maatreël)return maatreël;
    return 진입점있음?0:-8;
}
