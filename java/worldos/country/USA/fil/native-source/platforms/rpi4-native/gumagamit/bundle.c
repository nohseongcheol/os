#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bundle.h"
#include "uzlib.h"
static unsigned char Archive[16384], 풀린자료[16385];
static unsigned sukat_82232621, 중앙목록, 항목들;
static char pagpasok_kategorya[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Archive[현재위치] | Archive[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int clip(unsigned 현재위치, unsigned item_COUNT, unsigned 한도) { return 현재위치 <= 한도 && item_COUNT <= 한도-현재위치; }
static size_t haba_VALUE(const char *string_data) { size_t item_COUNT=0; while(string_data[item_COUNT]) item_COUNT++; return item_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned item_COUNT) { for(unsigned 순번=0;순번<item_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int file_tapusin(void *미사용값) { (void)미사용값; return -1; }
static int katangian_data(const char *linya,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)linya,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)linya,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(pagpasok_kategorya))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char character_code=linya[12+순번];if(character_code<=32||character_code=='/'||character_code=='\\')return -8;pagpasok_kategorya[순번]=character_code;}
        pagpasok_kategorya[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int miyembro(unsigned 현재위치, unsigned char *sukat_data, unsigned 용량한도) {
    unsigned pamamaraan_pagpasok=두바이트읽기(현재위치+10), kompigurasyon_Background_Intelligent_Transfer_Service=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), release_sukat=네바이트읽기(현재위치+24), lokal=네바이트읽기(현재위치+42);
    unsigned pangalan=두바이트읽기(현재위치+28);
    if(release_sukat>용량한도 || release_sukat>16384 || (pamamaraan_pagpasok!=0 && pamamaraan_pagpasok!=8) || (kompigurasyon_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!clip(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=pamamaraan_pagpasok || 두바이트읽기(lokal+6)!=kompigurasyon_Background_Intelligent_Transfer_Service || 두바이트읽기(lokal+26)!=pangalan)return -8;
    unsigned Start_OFFSET=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!clip(Start_OFFSET,pangalan,중앙목록) || !같음(Archive+Start_OFFSET,Archive+현재위치+46,pangalan))return -8;
    Start_OFFSET+=pangalan;if(!clip(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!clip(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(kompigurasyon_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(lokal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=release_sukat))return -8;
    if(pamamaraan_pagpasok==0) { if(압축크기!=release_sukat)return -8; for(unsigned 순번=0;순번<release_sukat;순번++)sukat_data[순번]=Archive[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t patutunguhan_data={0};uzlib_uncompress_init(&patutunguhan_data,0,0);
        patutunguhan_data.source=Archive+Start_OFFSET;patutunguhan_data.source_limit=patutunguhan_data.source+압축크기;patutunguhan_data.source_read_cb=file_tapusin;
        /* One extra output byte lets inflate consume/check the end marker. */
        patutunguhan_data.dest_start=patutunguhan_data.dest=풀린자료;patutunguhan_data.dest_limit=풀린자료+release_sukat+1;
        int 반환값=uzlib_uncompress(&patutunguhan_data);
        if(반환값!=UZLIB_DONE || patutunguhan_data.eof || patutunguhan_data.dest!=풀린자료+release_sukat || patutunguhan_data.source!=patutunguhan_data.source_limit)return -8;
        for(unsigned 순번=0;순번<release_sukat;순번++)sukat_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(sukat_data,release_sukat,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return release_sukat;
}
int 꾸러미읽기(const char *pangalan, unsigned char *sukat_data, unsigned 수용량) {
    if(!항목들)return -2;unsigned item_COUNT=haba_VALUE(pangalan),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==item_COUNT && 같음(Archive+현재위치+46,(const unsigned char*)pangalan,item_COUNT))return miyembro(현재위치,sukat_data,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return pagpasok_kategorya; }
int 꾸러미열기(const char *file_pagpasok_pangalan) {
    항목들=0;pagpasok_kategorya[0]=0;
    intptr_t file_hawakán=사용자호출(3,(uintptr_t)file_pagpasok_pangalan,0,0,0,0,0);if(file_hawakán<0)return file_hawakán;
    intptr_t item_COUNT=사용자호출(9,file_hawakán,0,0,0,0,0);
    if(item_COUNT<22 || item_COUNT>(intptr_t)sizeof(Archive)) { 사용자호출(4,file_hawakán,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,file_hawakán,(uintptr_t)Archive,item_COUNT,0,0,0);사용자호출(4,file_hawakán,0,0,0,0,0);
    if(RECEIVED_COUNT!=item_COUNT)return -5;sukat_82232621=item_COUNT;
    unsigned tapusin_OFFSET=sukat_82232621-22;
    for(;;) { if(네바이트읽기(tapusin_OFFSET)==0x06054b50 && tapusin_OFFSET+22+두바이트읽기(tapusin_OFFSET+20)==sukat_82232621)break; if(!tapusin_OFFSET)return -8;tapusin_OFFSET--; }
    unsigned pagpasok_COUNT=두바이트읽기(tapusin_OFFSET+10);중앙목록=네바이트읽기(tapusin_OFFSET+16);
    if(두바이트읽기(tapusin_OFFSET+4)||두바이트읽기(tapusin_OFFSET+6)||두바이트읽기(tapusin_OFFSET+8)!=pagpasok_COUNT||!pagpasok_COUNT||pagpasok_COUNT>256||!clip(중앙목록,네바이트읽기(tapusin_OFFSET+12),tapusin_OFFSET)||중앙목록+네바이트읽기(tapusin_OFFSET+12)!=tapusin_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<pagpasok_COUNT;순번++) {
        if(!clip(현재위치,46,tapusin_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Susunod_item=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!clip(현재위치,Susunod_item,tapusin_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archive[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned haba_data=두바이트읽기(다른항목+28);if(haba_data==이름길이&&같음(Archive+다른항목+46,Archive+현재위치+46,haba_data))return -8;다른항목+=46+haba_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Susunod_item;
    }
    if(현재위치!=tapusin_OFFSET)return -8;항목들=pagpasok_COUNT;
    unsigned char 꾸러미명세[4096];int Grupo_sukat=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupo_sukat<0){항목들=0;return -8;}
    꾸러미명세[Grupo_sukat]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupo_sukat) {
        unsigned run=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupo_sukat && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned haba_data=INDEX_VALUE-run;if(INDEX_VALUE<(unsigned)Grupo_sukat)INDEX_VALUE++;if(haba_data && 꾸러미명세[run+haba_data-1]=='\r')haba_data--;
        if(사용량 && haba_data && 꾸러미명세[run]==' ') {run++;haba_data--;}
        else {
            int sukat=katangian_data(논리크기,사용량,&진입점있음);if(sukat)return sukat;
            사용량=0;if(!haba_data)break;
        }
        if(haba_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<haba_data;순번++)논리크기[사용량++]=꾸러미명세[run+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int sukat=katangian_data(논리크기,사용량,&진입점있음);if(sukat)return sukat;
    return 진입점있음?0:-8;
}
