#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "꾸러미.h"
#include "uzlib.h"
static unsigned char 압축꾸러미[16384], 풀린자료[16385];
static unsigned Величина, 중앙목록, 항목들;
static char 시작클래스[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return 압축꾸러미[현재위치] | 압축꾸러미[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int 범위(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t 길이(const char *문자열값) { size_t 개수=0; while(문자열값[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int 파일끝(void *미사용값) { (void)미사용값; return -1; }
static int 속성값(const char *Ред,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Ред,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Ред,(const unsigned char*)"Main-Class: ",12)) {
        unsigned 값=사용량-12;if(*진입점있음||!값||값>=sizeof(시작클래스))return -8;
        for(unsigned 순번=0;순번<값;순번++){unsigned char 문자값=Ред[12+순번];if(문자값<=32||문자값=='/'||문자값=='\\')return -8;시작클래스[순번]=문자값;}
        시작클래스[값]=0;*진입점있음=1;
    }
    return 0;
}
static int 구성원(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), 해제크기=네바이트읽기(현재위치+24), 내부값=네바이트읽기(현재위치+42);
    unsigned Назив=두바이트읽기(현재위치+28);
    if(해제크기>용량한도 || 해제크기>16384 || (메소드!=0 && 메소드!=8) || (설정비트&~0x80e))return -8;
    if(!범위(내부값,30,중앙목록) || 네바이트읽기(내부값)!=0x04034b50 || 두바이트읽기(내부값+8)!=메소드 || 두바이트읽기(내부값+6)!=설정비트 || 두바이트읽기(내부값+26)!=Назив)return -8;
    unsigned 시작위치=내부값+30, 추가영역=두바이트읽기(내부값+28);
    if(!범위(시작위치,Назив,중앙목록) || !같음(압축꾸러미+시작위치,압축꾸러미+현재위치+46,Назив))return -8;
    시작위치+=Назив;if(!범위(시작위치,추가영역,중앙목록))return -8;시작위치+=추가영역;
    if(!범위(시작위치,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(내부값+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(내부값+18)!=압축크기 || 네바이트읽기(내부값+22)!=해제크기))return -8;
    if(메소드==0) { if(압축크기!=해제크기)return -8; for(unsigned 순번=0;순번<해제크기;순번++)결과자료[순번]=압축꾸러미[시작위치+순번]; }
    else {
        uzlib_uncomp_t 목적자료={0};uzlib_uncompress_init(&목적자료,0,0);
        목적자료.source=압축꾸러미+시작위치;목적자료.source_limit=목적자료.source+압축크기;목적자료.source_read_cb=파일끝;
        /* One extra output byte lets inflate consume/check the end marker. */
        목적자료.dest_start=목적자료.dest=풀린자료;목적자료.dest_limit=풀린자료+해제크기+1;
        int 반환값=uzlib_uncompress(&목적자료);
        if(반환값!=UZLIB_DONE || 목적자료.eof || 목적자료.dest!=풀린자료+해제크기 || 목적자료.source!=목적자료.source_limit)return -8;
        for(unsigned 순번=0;순번<해제크기;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,해제크기,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return 해제크기;
}
int 꾸러미읽기(const char *Назив, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=길이(Назив),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(압축꾸러미+현재위치+46,(const unsigned char*)Назив,개수))return 구성원(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return 시작클래스; }
int 꾸러미열기(const char *파일이름) {
    항목들=0;시작클래스[0]=0;
    intptr_t 파일기술자=사용자호출(3,(uintptr_t)파일이름,0,0,0,0,0);if(파일기술자<0)return 파일기술자;
    intptr_t 개수=사용자호출(9,파일기술자,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(압축꾸러미)) { 사용자호출(4,파일기술자,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,파일기술자,(uintptr_t)압축꾸러미,개수,0,0,0);사용자호출(4,파일기술자,0,0,0,0,0);
    if(받은수!=개수)return -5;Величина=개수;
    unsigned 끝위치=Величина-22;
    for(;;) { if(네바이트읽기(끝위치)==0x06054b50 && 끝위치+22+두바이트읽기(끝위치+20)==Величина)break; if(!끝위치)return -8;끝위치--; }
    unsigned 항목수=두바이트읽기(끝위치+10);중앙목록=네바이트읽기(끝위치+16);
    if(두바이트읽기(끝위치+4)||두바이트읽기(끝위치+6)||두바이트읽기(끝위치+8)!=항목수||!항목수||항목수>256||!범위(중앙목록,네바이트읽기(끝위치+12),끝위치)||중앙목록+네바이트읽기(끝위치+12)!=끝위치)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!범위(현재위치,46,끝위치)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!범위(현재위치,다음,끝위치)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!압축꾸러미[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(다른항목+28);if(길이값==이름길이&&같음(압축꾸러미+다른항목+46,압축꾸러미+현재위치+46,길이값))return -8;다른항목+=46+길이값+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=끝위치)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int 묶음수=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(묶음수<0){항목들=0;return -8;}
    꾸러미명세[묶음수]=0;
    char 논리크기[512];unsigned 사용량=0,자리값=0;int 진입점있음=0;
    while(자리값<(unsigned)묶음수) {
        unsigned Покрени=자리값;while(자리값<(unsigned)묶음수 && 꾸러미명세[자리값]!='\n')자리값++;
        unsigned 길이값=자리값-Покрени;if(자리값<(unsigned)묶음수)자리값++;if(길이값 && 꾸러미명세[Покрени+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[Покрени]==' ') {Покрени++;길이값--;}
        else {
            int ИСХОД=속성값(논리크기,사용량,&진입점있음);if(ИСХОД)return ИСХОД;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[Покрени+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int ИСХОД=속성값(논리크기,사용량,&진입점있음);if(ИСХОД)return ИСХОД;
    return 진입점있음?0:-8;
}
