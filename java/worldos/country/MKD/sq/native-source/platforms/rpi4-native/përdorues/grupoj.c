#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "grupoj.h"
#include "uzlib.h"
static unsigned char arkiv[16384], 풀린자료[16385];
static unsigned Madhësi, 중앙목록, 항목들;
static char futje_klasë[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return arkiv[현재위치] | arkiv[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int fragment(unsigned 현재위치, unsigned njësi_COUNT, unsigned 한도) { return 현재위치 <= 한도 && njësi_COUNT <= 한도-현재위치; }
static size_t gjatësi_VALUE(const char *varg_të_dhëna) { size_t njësi_COUNT=0; while(varg_të_dhëna[njësi_COUNT]) njësi_COUNT++; return njësi_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned njësi_COUNT) { for(unsigned 순번=0;순번<njësi_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int skedar_mbaroj(void *미사용값) { (void)미사용값; return -1; }
static int atribut_të_dhëna(const char *linjë,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)linjë,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)linjë,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(futje_klasë))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char kodi_i_karakterit=linjë[12+순번];if(kodi_i_karakterit<=32||kodi_i_karakterit=='/'||kodi_i_karakterit=='\\')return -8;futje_klasë[순번]=kodi_i_karakterit;}
        futje_klasë[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int anëtar(unsigned 현재위치, unsigned char *llogaritje_të_dhëna, unsigned 용량한도) {
    unsigned metoda_futje=두바이트읽기(현재위치+10), konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), liroj_ndryshoj_përmasat=네바이트읽기(현재위치+24), lokal=네바이트읽기(현재위치+42);
    unsigned Emër=두바이트읽기(현재위치+28);
    if(liroj_ndryshoj_përmasat>용량한도 || liroj_ndryshoj_përmasat>16384 || (metoda_futje!=0 && metoda_futje!=8) || (konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&~0x80e))return -8;
    if(!fragment(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metoda_futje || 두바이트읽기(lokal+6)!=konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond || 두바이트읽기(lokal+26)!=Emër)return -8;
    unsigned nis_OFFSET=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!fragment(nis_OFFSET,Emër,중앙목록) || !같음(arkiv+nis_OFFSET,arkiv+현재위치+46,Emër))return -8;
    nis_OFFSET+=Emër;if(!fragment(nis_OFFSET,추가영역,중앙목록))return -8;nis_OFFSET+=추가영역;
    if(!fragment(nis_OFFSET,압축크기,중앙목록))return -8;
    if(!(konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&8) && (네바이트읽기(lokal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=liroj_ndryshoj_përmasat))return -8;
    if(metoda_futje==0) { if(압축크기!=liroj_ndryshoj_përmasat)return -8; for(unsigned 순번=0;순번<liroj_ndryshoj_përmasat;순번++)llogaritje_të_dhëna[순번]=arkiv[nis_OFFSET+순번]; }
    else {
        uzlib_uncomp_t vendmbërritje_të_dhëna={0};uzlib_uncompress_init(&vendmbërritje_të_dhëna,0,0);
        vendmbërritje_të_dhëna.source=arkiv+nis_OFFSET;vendmbërritje_të_dhëna.source_limit=vendmbërritje_të_dhëna.source+압축크기;vendmbërritje_të_dhëna.source_read_cb=skedar_mbaroj;
        /* One extra output byte lets inflate consume/check the end marker. */
        vendmbërritje_të_dhëna.dest_start=vendmbërritje_të_dhëna.dest=풀린자료;vendmbërritje_të_dhëna.dest_limit=풀린자료+liroj_ndryshoj_përmasat+1;
        int 반환값=uzlib_uncompress(&vendmbërritje_të_dhëna);
        if(반환값!=UZLIB_DONE || vendmbërritje_të_dhëna.eof || vendmbërritje_të_dhëna.dest!=풀린자료+liroj_ndryshoj_përmasat || vendmbërritje_të_dhëna.source!=vendmbërritje_të_dhëna.source_limit)return -8;
        for(unsigned 순번=0;순번<liroj_ndryshoj_përmasat;순번++)llogaritje_të_dhëna[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(llogaritje_të_dhëna,liroj_ndryshoj_përmasat,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return liroj_ndryshoj_përmasat;
}
int 꾸러미읽기(const char *Emër, unsigned char *llogaritje_të_dhëna, unsigned 수용량) {
    if(!항목들)return -2;unsigned njësi_COUNT=gjatësi_VALUE(Emër),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==njësi_COUNT && 같음(arkiv+현재위치+46,(const unsigned char*)Emër,njësi_COUNT))return anëtar(현재위치,llogaritje_të_dhëna,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return futje_klasë; }
int 꾸러미열기(const char *skedar_futje_emër) {
    항목들=0;futje_klasë[0]=0;
    intptr_t skedar_dorezë=사용자호출(3,(uintptr_t)skedar_futje_emër,0,0,0,0,0);if(skedar_dorezë<0)return skedar_dorezë;
    intptr_t njësi_COUNT=사용자호출(9,skedar_dorezë,0,0,0,0,0);
    if(njësi_COUNT<22 || njësi_COUNT>(intptr_t)sizeof(arkiv)) { 사용자호출(4,skedar_dorezë,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,skedar_dorezë,(uintptr_t)arkiv,njësi_COUNT,0,0,0);사용자호출(4,skedar_dorezë,0,0,0,0,0);
    if(RECEIVED_COUNT!=njësi_COUNT)return -5;Madhësi=njësi_COUNT;
    unsigned mbaroj_OFFSET=Madhësi-22;
    for(;;) { if(네바이트읽기(mbaroj_OFFSET)==0x06054b50 && mbaroj_OFFSET+22+두바이트읽기(mbaroj_OFFSET+20)==Madhësi)break; if(!mbaroj_OFFSET)return -8;mbaroj_OFFSET--; }
    unsigned futje_COUNT=두바이트읽기(mbaroj_OFFSET+10);중앙목록=네바이트읽기(mbaroj_OFFSET+16);
    if(두바이트읽기(mbaroj_OFFSET+4)||두바이트읽기(mbaroj_OFFSET+6)||두바이트읽기(mbaroj_OFFSET+8)!=futje_COUNT||!futje_COUNT||futje_COUNT>256||!fragment(중앙목록,네바이트읽기(mbaroj_OFFSET+12),mbaroj_OFFSET)||중앙목록+네바이트읽기(mbaroj_OFFSET+12)!=mbaroj_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<futje_COUNT;순번++) {
        if(!fragment(현재위치,46,mbaroj_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Tjetër_njësi=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!fragment(현재위치,Tjetër_njësi,mbaroj_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!arkiv[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned gjatësi_të_dhëna=두바이트읽기(다른항목+28);if(gjatësi_të_dhëna==이름길이&&같음(arkiv+다른항목+46,arkiv+현재위치+46,gjatësi_të_dhëna))return -8;다른항목+=46+gjatësi_të_dhëna+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Tjetër_njësi;
    }
    if(현재위치!=mbaroj_OFFSET)return -8;항목들=futje_COUNT;
    unsigned char 꾸러미명세[4096];int grup_ndryshoj_përmasat=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(grup_ndryshoj_përmasat<0){항목들=0;return -8;}
    꾸러미명세[grup_ndryshoj_përmasat]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)grup_ndryshoj_përmasat) {
        unsigned Ekzekuto=INDEX_VALUE;while(INDEX_VALUE<(unsigned)grup_ndryshoj_përmasat && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned gjatësi_të_dhëna=INDEX_VALUE-Ekzekuto;if(INDEX_VALUE<(unsigned)grup_ndryshoj_përmasat)INDEX_VALUE++;if(gjatësi_të_dhëna && 꾸러미명세[Ekzekuto+gjatësi_të_dhëna-1]=='\r')gjatësi_të_dhëna--;
        if(사용량 && gjatësi_të_dhëna && 꾸러미명세[Ekzekuto]==' ') {Ekzekuto++;gjatësi_të_dhëna--;}
        else {
            int llogaritje=atribut_të_dhëna(논리크기,사용량,&진입점있음);if(llogaritje)return llogaritje;
            사용량=0;if(!gjatësi_të_dhëna)break;
        }
        if(gjatësi_të_dhëna>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<gjatësi_të_dhëna;순번++)논리크기[사용량++]=꾸러미명세[Ekzekuto+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int llogaritje=atribut_të_dhëna(논리크기,사용량,&진입점있음);if(llogaritje)return llogaritje;
    return 진입점있음?0:-8;
}
