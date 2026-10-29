#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "pūpū.h"
#include "uzlib.h"
static unsigned char Pūranga[16384], 풀린자료[16385];
static unsigned rahi, 중앙목록, 항목들;
static char tāurunga_tauaha[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Pūranga[현재위치] | Pūranga[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int topenga(unsigned 현재위치, unsigned tuemi_COUNT, unsigned 한도) { return 현재위치 <= 한도 && tuemi_COUNT <= 한도-현재위치; }
static size_t roa_uara(const char *aho_raraunga) { size_t tuemi_COUNT=0; while(aho_raraunga[tuemi_COUNT]) tuemi_COUNT++; return tuemi_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_uara, unsigned tuemi_COUNT) { for(unsigned 순번=0;순번<tuemi_COUNT;순번++)if(첫째값[순번]!=SECOND_uara[순번])return 0;return 1; }
static int kōnae_mutu(void *미사용값) { (void)미사용값; return -1; }
static int huanga_raraunga(const char *hononga,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)hononga,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)hononga,(const unsigned char*)"Main-Class: ",12)) {
        unsigned uara=사용량-12;if(*진입점있음||!uara||uara>=sizeof(tāurunga_tauaha))return -8;
        for(unsigned 순번=0;순번<uara;순번++){unsigned char waehere_pūāhua=hononga[12+순번];if(waehere_pūāhua<=32||waehere_pūāhua=='/'||waehere_pūāhua=='\\')return -8;tāurunga_tauaha[순번]=waehere_pūāhua;}
        tāurunga_tauaha[uara]=0;*진입점있음=1;
    }
    return 0;
}
static int mema(unsigned 현재위치, unsigned char *mēhua_raraunga, unsigned 용량한도) {
    unsigned aratuka_tāurunga=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), tuku_rahi=네바이트읽기(현재위치+24), paetata=네바이트읽기(현재위치+42);
    unsigned Ingoa=두바이트읽기(현재위치+28);
    if(tuku_rahi>용량한도 || tuku_rahi>16384 || (aratuka_tāurunga!=0 && aratuka_tāurunga!=8) || (설정비트&~0x80e))return -8;
    if(!topenga(paetata,30,중앙목록) || 네바이트읽기(paetata)!=0x04034b50 || 두바이트읽기(paetata+8)!=aratuka_tāurunga || 두바이트읽기(paetata+6)!=설정비트 || 두바이트읽기(paetata+26)!=Ingoa)return -8;
    unsigned Start_OFFSET=paetata+30, 추가영역=두바이트읽기(paetata+28);
    if(!topenga(Start_OFFSET,Ingoa,중앙목록) || !같음(Pūranga+Start_OFFSET,Pūranga+현재위치+46,Ingoa))return -8;
    Start_OFFSET+=Ingoa;if(!topenga(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!topenga(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(paetata+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(paetata+18)!=압축크기 || 네바이트읽기(paetata+22)!=tuku_rahi))return -8;
    if(aratuka_tāurunga==0) { if(압축크기!=tuku_rahi)return -8; for(unsigned 순번=0;순번<tuku_rahi;순번++)mēhua_raraunga[순번]=Pūranga[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t ūnga_raraunga={0};uzlib_uncompress_init(&ūnga_raraunga,0,0);
        ūnga_raraunga.source=Pūranga+Start_OFFSET;ūnga_raraunga.source_limit=ūnga_raraunga.source+압축크기;ūnga_raraunga.source_read_cb=kōnae_mutu;
        /* One extra output byte lets inflate consume/check the end marker. */
        ūnga_raraunga.dest_start=ūnga_raraunga.dest=풀린자료;ūnga_raraunga.dest_limit=풀린자료+tuku_rahi+1;
        int 반환값=uzlib_uncompress(&ūnga_raraunga);
        if(반환값!=UZLIB_DONE || ūnga_raraunga.eof || ūnga_raraunga.dest!=풀린자료+tuku_rahi || ūnga_raraunga.source!=ūnga_raraunga.source_limit)return -8;
        for(unsigned 순번=0;순번<tuku_rahi;순번++)mēhua_raraunga[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(mēhua_raraunga,tuku_rahi,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return tuku_rahi;
}
int 꾸러미읽기(const char *Ingoa, unsigned char *mēhua_raraunga, unsigned 수용량) {
    if(!항목들)return -2;unsigned tuemi_COUNT=roa_uara(Ingoa),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==tuemi_COUNT && 같음(Pūranga+현재위치+46,(const unsigned char*)Ingoa,tuemi_COUNT))return mema(현재위치,mēhua_raraunga,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return tāurunga_tauaha; }
int 꾸러미열기(const char *kōnae_tāurunga_ingoa) {
    항목들=0;tāurunga_tauaha[0]=0;
    intptr_t kōnae_raweke=사용자호출(3,(uintptr_t)kōnae_tāurunga_ingoa,0,0,0,0,0);if(kōnae_raweke<0)return kōnae_raweke;
    intptr_t tuemi_COUNT=사용자호출(9,kōnae_raweke,0,0,0,0,0);
    if(tuemi_COUNT<22 || tuemi_COUNT>(intptr_t)sizeof(Pūranga)) { 사용자호출(4,kōnae_raweke,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,kōnae_raweke,(uintptr_t)Pūranga,tuemi_COUNT,0,0,0);사용자호출(4,kōnae_raweke,0,0,0,0,0);
    if(RECEIVED_COUNT!=tuemi_COUNT)return -5;rahi=tuemi_COUNT;
    unsigned mutu_OFFSET=rahi-22;
    for(;;) { if(네바이트읽기(mutu_OFFSET)==0x06054b50 && mutu_OFFSET+22+두바이트읽기(mutu_OFFSET+20)==rahi)break; if(!mutu_OFFSET)return -8;mutu_OFFSET--; }
    unsigned tāurunga_COUNT=두바이트읽기(mutu_OFFSET+10);중앙목록=네바이트읽기(mutu_OFFSET+16);
    if(두바이트읽기(mutu_OFFSET+4)||두바이트읽기(mutu_OFFSET+6)||두바이트읽기(mutu_OFFSET+8)!=tāurunga_COUNT||!tāurunga_COUNT||tāurunga_COUNT>256||!topenga(중앙목록,네바이트읽기(mutu_OFFSET+12),mutu_OFFSET)||중앙목록+네바이트읽기(mutu_OFFSET+12)!=mutu_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<tāurunga_COUNT;순번++) {
        if(!topenga(현재위치,46,mutu_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Panuku_tuemi=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!topenga(현재위치,Panuku_tuemi,mutu_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Pūranga[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned roa_raraunga=두바이트읽기(다른항목+28);if(roa_raraunga==이름길이&&같음(Pūranga+다른항목+46,Pūranga+현재위치+46,roa_raraunga))return -8;다른항목+=46+roa_raraunga+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Panuku_tuemi;
    }
    if(현재위치!=mutu_OFFSET)return -8;항목들=tāurunga_COUNT;
    unsigned char 꾸러미명세[4096];int rōpū_rahi=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(rōpū_rahi<0){항목들=0;return -8;}
    꾸러미명세[rōpū_rahi]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_uara=0;int 진입점있음=0;
    while(INDEX_uara<(unsigned)rōpū_rahi) {
        unsigned whakahaere=INDEX_uara;while(INDEX_uara<(unsigned)rōpū_rahi && 꾸러미명세[INDEX_uara]!='\n')INDEX_uara++;
        unsigned roa_raraunga=INDEX_uara-whakahaere;if(INDEX_uara<(unsigned)rōpū_rahi)INDEX_uara++;if(roa_raraunga && 꾸러미명세[whakahaere+roa_raraunga-1]=='\r')roa_raraunga--;
        if(사용량 && roa_raraunga && 꾸러미명세[whakahaere]==' ') {whakahaere++;roa_raraunga--;}
        else {
            int mēhua=huanga_raraunga(논리크기,사용량,&진입점있음);if(mēhua)return mēhua;
            사용량=0;if(!roa_raraunga)break;
        }
        if(roa_raraunga>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<roa_raraunga;순번++)논리크기[사용량++]=꾸러미명세[whakahaere+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int mēhua=huanga_raraunga(논리크기,사용량,&진입점있음);if(mēhua)return mēhua;
    return 진입점있음?0:-8;
}
