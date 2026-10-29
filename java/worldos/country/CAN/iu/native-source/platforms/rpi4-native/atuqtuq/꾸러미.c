#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "꾸러미.h"
#include "uzlib.h"
static unsigned char tuqqurli[16384], 풀린자료[16385];
static unsigned anininga, 중앙목록, 항목들;
static char Iliniku_naliannuungavik[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return tuqqurli[현재위치] | tuqqurli[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int Nakatigat(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t takininga_atuutilik(const char *qimiaq_titiqqat) { size_t 개수=0; while(qimiaq_titiqqat[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int ini_isulittuq(void *미사용값) { (void)미사용값; return -1; }
static int piuluqqutit_titiqqat(const char *titikutaak,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)titikutaak,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)titikutaak,(const unsigned char*)"Main-Class: ",12)) {
        unsigned atuutilik=사용량-12;if(*진입점있음||!atuutilik||atuutilik>=sizeof(Iliniku_naliannuungavik))return -8;
        for(unsigned 순번=0;순번<atuutilik;순번++){unsigned char immikkuuqtumut_nalunaikkut=titikutaak[12+순번];if(immikkuuqtumut_nalunaikkut<=32||immikkuuqtumut_nalunaikkut=='/'||immikkuuqtumut_nalunaikkut=='\\')return -8;Iliniku_naliannuungavik[순번]=immikkuuqtumut_nalunaikkut;}
        Iliniku_naliannuungavik[atuutilik]=0;*진입점있음=1;
    }
    return 0;
}
static int ilagijaujuq(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), anititaujuq_anininga=네바이트읽기(현재위치+24), tamaani=네바이트읽기(현재위치+42);
    unsigned atiq=두바이트읽기(현재위치+28);
    if(anititaujuq_anininga>용량한도 || anititaujuq_anininga>16384 || (메소드!=0 && 메소드!=8) || (설정비트&~0x80e))return -8;
    if(!Nakatigat(tamaani,30,중앙목록) || 네바이트읽기(tamaani)!=0x04034b50 || 두바이트읽기(tamaani+8)!=메소드 || 두바이트읽기(tamaani+6)!=설정비트 || 두바이트읽기(tamaani+26)!=atiq)return -8;
    unsigned 시작위치=tamaani+30, 추가영역=두바이트읽기(tamaani+28);
    if(!Nakatigat(시작위치,atiq,중앙목록) || !같음(tuqqurli+시작위치,tuqqurli+현재위치+46,atiq))return -8;
    시작위치+=atiq;if(!Nakatigat(시작위치,추가영역,중앙목록))return -8;시작위치+=추가영역;
    if(!Nakatigat(시작위치,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(tamaani+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(tamaani+18)!=압축크기 || 네바이트읽기(tamaani+22)!=anititaujuq_anininga))return -8;
    if(메소드==0) { if(압축크기!=anititaujuq_anininga)return -8; for(unsigned 순번=0;순번<anititaujuq_anininga;순번++)결과자료[순번]=tuqqurli[시작위치+순번]; }
    else {
        uzlib_uncomp_t namunngarvik_titiqqat={0};uzlib_uncompress_init(&namunngarvik_titiqqat,0,0);
        namunngarvik_titiqqat.source=tuqqurli+시작위치;namunngarvik_titiqqat.source_limit=namunngarvik_titiqqat.source+압축크기;namunngarvik_titiqqat.source_read_cb=ini_isulittuq;
        /* One extra output byte lets inflate consume/check the end marker. */
        namunngarvik_titiqqat.dest_start=namunngarvik_titiqqat.dest=풀린자료;namunngarvik_titiqqat.dest_limit=풀린자료+anititaujuq_anininga+1;
        int 반환값=uzlib_uncompress(&namunngarvik_titiqqat);
        if(반환값!=UZLIB_DONE || namunngarvik_titiqqat.eof || namunngarvik_titiqqat.dest!=풀린자료+anititaujuq_anininga || namunngarvik_titiqqat.source!=namunngarvik_titiqqat.source_limit)return -8;
        for(unsigned 순번=0;순번<anititaujuq_anininga;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,anititaujuq_anininga,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return anititaujuq_anininga;
}
int 꾸러미읽기(const char *atiq, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=takininga_atuutilik(atiq),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(tuqqurli+현재위치+46,(const unsigned char*)atiq,개수))return ilagijaujuq(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return Iliniku_naliannuungavik; }
int 꾸러미열기(const char *ini_Iliniku_atiq) {
    항목들=0;Iliniku_naliannuungavik[0]=0;
    intptr_t ini_nuuttarut=사용자호출(3,(uintptr_t)ini_Iliniku_atiq,0,0,0,0,0);if(ini_nuuttarut<0)return ini_nuuttarut;
    intptr_t 개수=사용자호출(9,ini_nuuttarut,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(tuqqurli)) { 사용자호출(4,ini_nuuttarut,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,ini_nuuttarut,(uintptr_t)tuqqurli,개수,0,0,0);사용자호출(4,ini_nuuttarut,0,0,0,0,0);
    if(받은수!=개수)return -5;anininga=개수;
    unsigned 끝위치=anininga-22;
    for(;;) { if(네바이트읽기(끝위치)==0x06054b50 && 끝위치+22+두바이트읽기(끝위치+20)==anininga)break; if(!끝위치)return -8;끝위치--; }
    unsigned 항목수=두바이트읽기(끝위치+10);중앙목록=네바이트읽기(끝위치+16);
    if(두바이트읽기(끝위치+4)||두바이트읽기(끝위치+6)||두바이트읽기(끝위치+8)!=항목수||!항목수||항목수>256||!Nakatigat(중앙목록,네바이트읽기(끝위치+12),끝위치)||중앙목록+네바이트읽기(끝위치+12)!=끝위치)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!Nakatigat(현재위치,46,끝위치)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!Nakatigat(현재위치,다음,끝위치)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!tuqqurli[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned takininga_titiqqat=두바이트읽기(다른항목+28);if(takininga_titiqqat==이름길이&&같음(tuqqurli+다른항목+46,tuqqurli+현재위치+46,takininga_titiqqat))return -8;다른항목+=46+takininga_titiqqat+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=끝위치)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int katinngajut_anininga=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(katinngajut_anininga<0){항목들=0;return -8;}
    꾸러미명세[katinngajut_anininga]=0;
    char 논리크기[512];unsigned 사용량=0,nalunaiqsimavik_atuutilik=0;int 진입점있음=0;
    while(nalunaiqsimavik_atuutilik<(unsigned)katinngajut_anininga) {
        unsigned 시작=nalunaiqsimavik_atuutilik;while(nalunaiqsimavik_atuutilik<(unsigned)katinngajut_anininga && 꾸러미명세[nalunaiqsimavik_atuutilik]!='\n')nalunaiqsimavik_atuutilik++;
        unsigned takininga_titiqqat=nalunaiqsimavik_atuutilik-시작;if(nalunaiqsimavik_atuutilik<(unsigned)katinngajut_anininga)nalunaiqsimavik_atuutilik++;if(takininga_titiqqat && 꾸러미명세[시작+takininga_titiqqat-1]=='\r')takininga_titiqqat--;
        if(사용량 && takininga_titiqqat && 꾸러미명세[시작]==' ') {시작++;takininga_titiqqat--;}
        else {
            int 결과=piuluqqutit_titiqqat(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!takininga_titiqqat)break;
        }
        if(takininga_titiqqat>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<takininga_titiqqat;순번++)논리크기[사용량++]=꾸러미명세[시작+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=piuluqqutit_titiqqat(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
