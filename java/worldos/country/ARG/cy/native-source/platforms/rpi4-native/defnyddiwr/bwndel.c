#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bwndel.h"
#include "uzlib.h"
static unsigned char Archif[16384], 풀린자료[16385];
static unsigned Maint, 중앙목록, 항목들;
static char cofnod_Dosbarth[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Archif[현재위치] | Archif[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int clip(unsigned 현재위치, unsigned eitem_COUNT, unsigned 한도) { return 현재위치 <= 한도 && eitem_COUNT <= 한도-현재위치; }
static size_t hyd_VALUE(const char *testun_data) { size_t eitem_COUNT=0; while(testun_data[eitem_COUNT]) eitem_COUNT++; return eitem_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned eitem_COUNT) { for(unsigned 순번=0;순번<eitem_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int ffeil_gorffen(void *미사용값) { (void)미사용값; return -1; }
static int priodoledd_data(const char *llinell,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)llinell,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)llinell,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(cofnod_Dosbarth))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char cod_nod=llinell[12+순번];if(cod_nod<=32||cod_nod=='/'||cod_nod=='\\')return -8;cofnod_Dosbarth[순번]=cod_nod;}
        cofnod_Dosbarth[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int aelod(unsigned 현재위치, unsigned char *mesur_data, unsigned 용량한도) {
    unsigned dull_cofnod=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), rhyddhau_newid_maint=네바이트읽기(현재위치+24), lleol=네바이트읽기(현재위치+42);
    unsigned Enw=두바이트읽기(현재위치+28);
    if(rhyddhau_newid_maint>용량한도 || rhyddhau_newid_maint>16384 || (dull_cofnod!=0 && dull_cofnod!=8) || (설정비트&~0x80e))return -8;
    if(!clip(lleol,30,중앙목록) || 네바이트읽기(lleol)!=0x04034b50 || 두바이트읽기(lleol+8)!=dull_cofnod || 두바이트읽기(lleol+6)!=설정비트 || 두바이트읽기(lleol+26)!=Enw)return -8;
    unsigned START_OFFSET=lleol+30, 추가영역=두바이트읽기(lleol+28);
    if(!clip(START_OFFSET,Enw,중앙목록) || !같음(Archif+START_OFFSET,Archif+현재위치+46,Enw))return -8;
    START_OFFSET+=Enw;if(!clip(START_OFFSET,추가영역,중앙목록))return -8;START_OFFSET+=추가영역;
    if(!clip(START_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(lleol+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lleol+18)!=압축크기 || 네바이트읽기(lleol+22)!=rhyddhau_newid_maint))return -8;
    if(dull_cofnod==0) { if(압축크기!=rhyddhau_newid_maint)return -8; for(unsigned 순번=0;순번<rhyddhau_newid_maint;순번++)mesur_data[순번]=Archif[START_OFFSET+순번]; }
    else {
        uzlib_uncomp_t cyrchfan_data={0};uzlib_uncompress_init(&cyrchfan_data,0,0);
        cyrchfan_data.source=Archif+START_OFFSET;cyrchfan_data.source_limit=cyrchfan_data.source+압축크기;cyrchfan_data.source_read_cb=ffeil_gorffen;
        /* One extra output byte lets inflate consume/check the end marker. */
        cyrchfan_data.dest_start=cyrchfan_data.dest=풀린자료;cyrchfan_data.dest_limit=풀린자료+rhyddhau_newid_maint+1;
        int 반환값=uzlib_uncompress(&cyrchfan_data);
        if(반환값!=UZLIB_DONE || cyrchfan_data.eof || cyrchfan_data.dest!=풀린자료+rhyddhau_newid_maint || cyrchfan_data.source!=cyrchfan_data.source_limit)return -8;
        for(unsigned 순번=0;순번<rhyddhau_newid_maint;순번++)mesur_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(mesur_data,rhyddhau_newid_maint,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return rhyddhau_newid_maint;
}
int 꾸러미읽기(const char *Enw, unsigned char *mesur_data, unsigned 수용량) {
    if(!항목들)return -2;unsigned eitem_COUNT=hyd_VALUE(Enw),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==eitem_COUNT && 같음(Archif+현재위치+46,(const unsigned char*)Enw,eitem_COUNT))return aelod(현재위치,mesur_data,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return cofnod_Dosbarth; }
int 꾸러미열기(const char *ffeil_cofnod_enw) {
    항목들=0;cofnod_Dosbarth[0]=0;
    intptr_t ffeil_dolen=사용자호출(3,(uintptr_t)ffeil_cofnod_enw,0,0,0,0,0);if(ffeil_dolen<0)return ffeil_dolen;
    intptr_t eitem_COUNT=사용자호출(9,ffeil_dolen,0,0,0,0,0);
    if(eitem_COUNT<22 || eitem_COUNT>(intptr_t)sizeof(Archif)) { 사용자호출(4,ffeil_dolen,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,ffeil_dolen,(uintptr_t)Archif,eitem_COUNT,0,0,0);사용자호출(4,ffeil_dolen,0,0,0,0,0);
    if(RECEIVED_COUNT!=eitem_COUNT)return -5;Maint=eitem_COUNT;
    unsigned gorffen_OFFSET=Maint-22;
    for(;;) { if(네바이트읽기(gorffen_OFFSET)==0x06054b50 && gorffen_OFFSET+22+두바이트읽기(gorffen_OFFSET+20)==Maint)break; if(!gorffen_OFFSET)return -8;gorffen_OFFSET--; }
    unsigned cofnod_COUNT=두바이트읽기(gorffen_OFFSET+10);중앙목록=네바이트읽기(gorffen_OFFSET+16);
    if(두바이트읽기(gorffen_OFFSET+4)||두바이트읽기(gorffen_OFFSET+6)||두바이트읽기(gorffen_OFFSET+8)!=cofnod_COUNT||!cofnod_COUNT||cofnod_COUNT>256||!clip(중앙목록,네바이트읽기(gorffen_OFFSET+12),gorffen_OFFSET)||중앙목록+네바이트읽기(gorffen_OFFSET+12)!=gorffen_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<cofnod_COUNT;순번++) {
        if(!clip(현재위치,46,gorffen_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Nesaf_eitem=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!clip(현재위치,Nesaf_eitem,gorffen_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archif[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned hyd_data=두바이트읽기(다른항목+28);if(hyd_data==이름길이&&같음(Archif+다른항목+46,Archif+현재위치+46,hyd_data))return -8;다른항목+=46+hyd_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Nesaf_eitem;
    }
    if(현재위치!=gorffen_OFFSET)return -8;항목들=cofnod_COUNT;
    unsigned char 꾸러미명세[4096];int Grŵp_newid_maint=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grŵp_newid_maint<0){항목들=0;return -8;}
    꾸러미명세[Grŵp_newid_maint]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grŵp_newid_maint) {
        unsigned Gweithredu_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grŵp_newid_maint && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned hyd_data=INDEX_VALUE-Gweithredu_2;if(INDEX_VALUE<(unsigned)Grŵp_newid_maint)INDEX_VALUE++;if(hyd_data && 꾸러미명세[Gweithredu_2+hyd_data-1]=='\r')hyd_data--;
        if(사용량 && hyd_data && 꾸러미명세[Gweithredu_2]==' ') {Gweithredu_2++;hyd_data--;}
        else {
            int mesur=priodoledd_data(논리크기,사용량,&진입점있음);if(mesur)return mesur;
            사용량=0;if(!hyd_data)break;
        }
        if(hyd_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<hyd_data;순번++)논리크기[사용량++]=꾸러미명세[Gweithredu_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int mesur=priodoledd_data(논리크기,사용량,&진입점있음);if(mesur)return mesur;
    return 진입점있음?0:-8;
}
