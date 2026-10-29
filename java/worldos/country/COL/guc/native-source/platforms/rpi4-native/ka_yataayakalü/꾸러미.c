#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "꾸러미.h"
#include "uzlib.h"
static unsigned char anaajawaa[16384], 풀린자료[16385];
static unsigned 크기, 중앙목록, 항목들;
static char ekeroliaa_akotchijuushi[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return anaajawaa[현재위치] | anaajawaa[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int külipü_ayaakuaapijana(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t akaliaa_ajutuu(const char *kaleena_atijaaya) { size_t 개수=0; while(kaleena_atijaaya[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int anaajaalaa_ajattiraa(void *미사용값) { (void)미사용값; return -1; }
static int anaajaalaakua_ipa_atijaaya(const char *liinia,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)liinia,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)liinia,(const unsigned char*)"Main-Class: ",12)) {
        unsigned ajutuu=사용량-12;if(*진입점있음||!ajutuu||ajutuu>=sizeof(ekeroliaa_akotchijuushi))return -8;
        for(unsigned 순번=0;순번<ajutuu;순번++){unsigned char 문자값=liinia[12+순번];if(문자값<=32||문자값=='/'||문자값=='\\')return -8;ekeroliaa_akotchijuushi[순번]=문자값;}
        ekeroliaa_akotchijuushi[ajutuu]=0;*진입점있음=1;
    }
    return 0;
}
static int a_akaajatü(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), 해제크기=네바이트읽기(현재위치+24), 내부값=네바이트읽기(현재위치+42);
    unsigned 이름=두바이트읽기(현재위치+28);
    if(해제크기>용량한도 || 해제크기>16384 || (메소드!=0 && 메소드!=8) || (설정비트&~0x80e))return -8;
    if(!külipü_ayaakuaapijana(내부값,30,중앙목록) || 네바이트읽기(내부값)!=0x04034b50 || 두바이트읽기(내부값+8)!=메소드 || 두바이트읽기(내부값+6)!=설정비트 || 두바이트읽기(내부값+26)!=이름)return -8;
    unsigned 시작위치=내부값+30, 추가영역=두바이트읽기(내부값+28);
    if(!külipü_ayaakuaapijana(시작위치,이름,중앙목록) || !같음(anaajawaa+시작위치,anaajawaa+현재위치+46,이름))return -8;
    시작위치+=이름;if(!külipü_ayaakuaapijana(시작위치,추가영역,중앙목록))return -8;시작위치+=추가영역;
    if(!külipü_ayaakuaapijana(시작위치,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(내부값+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(내부값+18)!=압축크기 || 네바이트읽기(내부값+22)!=해제크기))return -8;
    if(메소드==0) { if(압축크기!=해제크기)return -8; for(unsigned 순번=0;순번<해제크기;순번++)결과자료[순번]=anaajawaa[시작위치+순번]; }
    else {
        uzlib_uncomp_t jalamüinjatü_atijaaya={0};uzlib_uncompress_init(&jalamüinjatü_atijaaya,0,0);
        jalamüinjatü_atijaaya.source=anaajawaa+시작위치;jalamüinjatü_atijaaya.source_limit=jalamüinjatü_atijaaya.source+압축크기;jalamüinjatü_atijaaya.source_read_cb=anaajaalaa_ajattiraa;
        /* One extra output byte lets inflate consume/check the end marker. */
        jalamüinjatü_atijaaya.dest_start=jalamüinjatü_atijaaya.dest=풀린자료;jalamüinjatü_atijaaya.dest_limit=풀린자료+해제크기+1;
        int 반환값=uzlib_uncompress(&jalamüinjatü_atijaaya);
        if(반환값!=UZLIB_DONE || jalamüinjatü_atijaaya.eof || jalamüinjatü_atijaaya.dest!=풀린자료+해제크기 || jalamüinjatü_atijaaya.source!=jalamüinjatü_atijaaya.source_limit)return -8;
        for(unsigned 순번=0;순번<해제크기;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,해제크기,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return 해제크기;
}
int 꾸러미읽기(const char *이름, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=akaliaa_ajutuu(이름),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(anaajawaa+현재위치+46,(const unsigned char*)이름,개수))return a_akaajatü(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ekeroliaa_akotchijuushi; }
int 꾸러미열기(const char *파일이름) {
    항목들=0;ekeroliaa_akotchijuushi[0]=0;
    intptr_t anaajaalaa_aapaaya=사용자호출(3,(uintptr_t)파일이름,0,0,0,0,0);if(anaajaalaa_aapaaya<0)return anaajaalaa_aapaaya;
    intptr_t 개수=사용자호출(9,anaajaalaa_aapaaya,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(anaajawaa)) { 사용자호출(4,anaajaalaa_aapaaya,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,anaajaalaa_aapaaya,(uintptr_t)anaajawaa,개수,0,0,0);사용자호출(4,anaajaalaa_aapaaya,0,0,0,0,0);
    if(받은수!=개수)return -5;크기=개수;
    unsigned 끝위치=크기-22;
    for(;;) { if(네바이트읽기(끝위치)==0x06054b50 && 끝위치+22+두바이트읽기(끝위치+20)==크기)break; if(!끝위치)return -8;끝위치--; }
    unsigned 항목수=두바이트읽기(끝위치+10);중앙목록=네바이트읽기(끝위치+16);
    if(두바이트읽기(끝위치+4)||두바이트읽기(끝위치+6)||두바이트읽기(끝위치+8)!=항목수||!항목수||항목수>256||!külipü_ayaakuaapijana(중앙목록,네바이트읽기(끝위치+12),끝위치)||중앙목록+네바이트읽기(끝위치+12)!=끝위치)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!külipü_ayaakuaapijana(현재위치,46,끝위치)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!külipü_ayaakuaapijana(현재위치,다음,끝위치)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!anaajawaa[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned akaliaa_atijaaya=두바이트읽기(다른항목+28);if(akaliaa_atijaaya==이름길이&&같음(anaajawaa+다른항목+46,anaajawaa+현재위치+46,akaliaa_atijaaya))return -8;다른항목+=46+akaliaa_atijaaya+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=끝위치)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int 묶음수=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(묶음수<0){항목들=0;return -8;}
    꾸러미명세[묶음수]=0;
    char 논리크기[512];unsigned 사용량=0,ee_iyatialujuna_ajutuu=0;int 진입점있음=0;
    while(ee_iyatialujuna_ajutuu<(unsigned)묶음수) {
        unsigned 시작=ee_iyatialujuna_ajutuu;while(ee_iyatialujuna_ajutuu<(unsigned)묶음수 && 꾸러미명세[ee_iyatialujuna_ajutuu]!='\n')ee_iyatialujuna_ajutuu++;
        unsigned akaliaa_atijaaya=ee_iyatialujuna_ajutuu-시작;if(ee_iyatialujuna_ajutuu<(unsigned)묶음수)ee_iyatialujuna_ajutuu++;if(akaliaa_atijaaya && 꾸러미명세[시작+akaliaa_atijaaya-1]=='\r')akaliaa_atijaaya--;
        if(사용량 && akaliaa_atijaaya && 꾸러미명세[시작]==' ') {시작++;akaliaa_atijaaya--;}
        else {
            int 결과=anaajaalaakua_ipa_atijaaya(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!akaliaa_atijaaya)break;
        }
        if(akaliaa_atijaaya>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<akaliaa_atijaaya;순번++)논리크기[사용량++]=꾸러미명세[시작+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=anaajaalaakua_ipa_atijaaya(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
