#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "꾸러미.h"
#include "uzlib.h"
static unsigned char ƴeewtirde[16384], 풀린자료[16385];
static unsigned waylude_etannde, 중앙목록, 항목들;
static char naatnugol_fedde[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return ƴeewtirde[현재위치] | ƴeewtirde[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int kilip(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t njuuteendi_njaru(const char *ɓoggol_keɓe) { size_t 개수=0; while(ɓoggol_keɓe[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int fiilde_taƴde(void *미사용값) { (void)미사용값; return -1; }
static int mbaadi_keɓe(const char *diidol,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)diidol,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)diidol,(const unsigned char*)"Main-Class: ",12)) {
        unsigned njaru=사용량-12;if(*진입점있음||!njaru||njaru>=sizeof(naatnugol_fedde))return -8;
        for(unsigned 순번=0;순번<njaru;순번++){unsigned char 문자값=diidol[12+순번];if(문자값<=32||문자값=='/'||문자값=='\\')return -8;naatnugol_fedde[순번]=문자값;}
        naatnugol_fedde[njaru]=0;*진입점있음=1;
    }
    return 0;
}
static int tergal(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), 해제크기=네바이트읽기(현재위치+24), nokkuwal=네바이트읽기(현재위치+42);
    unsigned innde=두바이트읽기(현재위치+28);
    if(해제크기>용량한도 || 해제크기>16384 || (메소드!=0 && 메소드!=8) || (설정비트&~0x80e))return -8;
    if(!kilip(nokkuwal,30,중앙목록) || 네바이트읽기(nokkuwal)!=0x04034b50 || 두바이트읽기(nokkuwal+8)!=메소드 || 두바이트읽기(nokkuwal+6)!=설정비트 || 두바이트읽기(nokkuwal+26)!=innde)return -8;
    unsigned 시작위치=nokkuwal+30, 추가영역=두바이트읽기(nokkuwal+28);
    if(!kilip(시작위치,innde,중앙목록) || !같음(ƴeewtirde+시작위치,ƴeewtirde+현재위치+46,innde))return -8;
    시작위치+=innde;if(!kilip(시작위치,추가영역,중앙목록))return -8;시작위치+=추가영역;
    if(!kilip(시작위치,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(nokkuwal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(nokkuwal+18)!=압축크기 || 네바이트읽기(nokkuwal+22)!=해제크기))return -8;
    if(메소드==0) { if(압축크기!=해제크기)return -8; for(unsigned 순번=0;순번<해제크기;순번++)결과자료[순번]=ƴeewtirde[시작위치+순번]; }
    else {
        uzlib_uncomp_t tiindaare_keɓe={0};uzlib_uncompress_init(&tiindaare_keɓe,0,0);
        tiindaare_keɓe.source=ƴeewtirde+시작위치;tiindaare_keɓe.source_limit=tiindaare_keɓe.source+압축크기;tiindaare_keɓe.source_read_cb=fiilde_taƴde;
        /* One extra output byte lets inflate consume/check the end marker. */
        tiindaare_keɓe.dest_start=tiindaare_keɓe.dest=풀린자료;tiindaare_keɓe.dest_limit=풀린자료+해제크기+1;
        int 반환값=uzlib_uncompress(&tiindaare_keɓe);
        if(반환값!=UZLIB_DONE || tiindaare_keɓe.eof || tiindaare_keɓe.dest!=풀린자료+해제크기 || tiindaare_keɓe.source!=tiindaare_keɓe.source_limit)return -8;
        for(unsigned 순번=0;순번<해제크기;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,해제크기,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return 해제크기;
}
int 꾸러미읽기(const char *innde, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=njuuteendi_njaru(innde),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(ƴeewtirde+현재위치+46,(const unsigned char*)innde,개수))return tergal(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return naatnugol_fedde; }
int 꾸러미열기(const char *fiilde_naatnugol_innde) {
    항목들=0;naatnugol_fedde[0]=0;
    intptr_t fiilde_jaggoode=사용자호출(3,(uintptr_t)fiilde_naatnugol_innde,0,0,0,0,0);if(fiilde_jaggoode<0)return fiilde_jaggoode;
    intptr_t 개수=사용자호출(9,fiilde_jaggoode,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(ƴeewtirde)) { 사용자호출(4,fiilde_jaggoode,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,fiilde_jaggoode,(uintptr_t)ƴeewtirde,개수,0,0,0);사용자호출(4,fiilde_jaggoode,0,0,0,0,0);
    if(받은수!=개수)return -5;waylude_etannde=개수;
    unsigned 끝위치=waylude_etannde-22;
    for(;;) { if(네바이트읽기(끝위치)==0x06054b50 && 끝위치+22+두바이트읽기(끝위치+20)==waylude_etannde)break; if(!끝위치)return -8;끝위치--; }
    unsigned 항목수=두바이트읽기(끝위치+10);중앙목록=네바이트읽기(끝위치+16);
    if(두바이트읽기(끝위치+4)||두바이트읽기(끝위치+6)||두바이트읽기(끝위치+8)!=항목수||!항목수||항목수>256||!kilip(중앙목록,네바이트읽기(끝위치+12),끝위치)||중앙목록+네바이트읽기(끝위치+12)!=끝위치)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!kilip(현재위치,46,끝위치)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!kilip(현재위치,다음,끝위치)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!ƴeewtirde[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned njuuteendi_keɓe=두바이트읽기(다른항목+28);if(njuuteendi_keɓe==이름길이&&같음(ƴeewtirde+다른항목+46,ƴeewtirde+현재위치+46,njuuteendi_keɓe))return -8;다른항목+=46+njuuteendi_keɓe+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=끝위치)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int seto_waylude_etannde=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(seto_waylude_etannde<0){항목들=0;return -8;}
    꾸러미명세[seto_waylude_etannde]=0;
    char 논리크기[512];unsigned 사용량=0,joopirdu_njaru=0;int 진입점있음=0;
    while(joopirdu_njaru<(unsigned)seto_waylude_etannde) {
        unsigned huutoraade=joopirdu_njaru;while(joopirdu_njaru<(unsigned)seto_waylude_etannde && 꾸러미명세[joopirdu_njaru]!='\n')joopirdu_njaru++;
        unsigned njuuteendi_keɓe=joopirdu_njaru-huutoraade;if(joopirdu_njaru<(unsigned)seto_waylude_etannde)joopirdu_njaru++;if(njuuteendi_keɓe && 꾸러미명세[huutoraade+njuuteendi_keɓe-1]=='\r')njuuteendi_keɓe--;
        if(사용량 && njuuteendi_keɓe && 꾸러미명세[huutoraade]==' ') {huutoraade++;njuuteendi_keɓe--;}
        else {
            int 결과=mbaadi_keɓe(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!njuuteendi_keɓe)break;
        }
        if(njuuteendi_keɓe>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<njuuteendi_keɓe;순번++)논리크기[사용량++]=꾸러미명세[huutoraade+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=mbaadi_keɓe(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
