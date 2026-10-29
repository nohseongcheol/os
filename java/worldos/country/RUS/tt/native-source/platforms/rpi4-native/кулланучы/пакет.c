#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "пакет.h"
#include "uzlib.h"
static unsigned char Архив[16384], 풀린자료[16385];
static unsigned үлчәмен_үзгәртү, 중앙목록, 항목들;
static char кертү_класс[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Архив[현재위치] | Архив[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int клип(unsigned 현재위치, unsigned элемент_COUNT, unsigned 한도) { return 현재위치 <= 한도 && элемент_COUNT <= 한도-현재위치; }
static size_t озынлык_VALUE(const char *юл_мәгълүмат) { size_t элемент_COUNT=0; while(юл_мәгълүмат[элемент_COUNT]) элемент_COUNT++; return элемент_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned элемент_COUNT) { for(unsigned 순번=0;순번<элемент_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int файл_тәмамлау(void *미사용값) { (void)미사용값; return -1; }
static int аергыч_мәгълүмат(const char *юл,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)юл,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)юл,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(кертү_класс))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char символ_коды=юл[12+순번];if(символ_коды<=32||символ_коды=='/'||символ_коды=='\\')return -8;кертү_класс[순번]=символ_коды;}
        кертү_класс[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int бүлек(unsigned 현재위치, unsigned char *үлчәм_мәгълүмат, unsigned 용량한도) {
    unsigned ысул_кертү=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), Чыгарылыш_үлчәмен_үзгәртү=네바이트읽기(현재위치+24), локаль=네바이트읽기(현재위치+42);
    unsigned исем=두바이트읽기(현재위치+28);
    if(Чыгарылыш_үлчәмен_үзгәртү>용량한도 || Чыгарылыш_үлчәмен_үзгәртү>16384 || (ысул_кертү!=0 && ысул_кертү!=8) || (설정비트&~0x80e))return -8;
    if(!клип(локаль,30,중앙목록) || 네바이트읽기(локаль)!=0x04034b50 || 두바이트읽기(локаль+8)!=ысул_кертү || 두바이트읽기(локаль+6)!=설정비트 || 두바이트읽기(локаль+26)!=исем)return -8;
    unsigned Start_OFFSET=локаль+30, 추가영역=두바이트읽기(локаль+28);
    if(!клип(Start_OFFSET,исем,중앙목록) || !같음(Архив+Start_OFFSET,Архив+현재위치+46,исем))return -8;
    Start_OFFSET+=исем;if(!клип(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!клип(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(локаль+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(локаль+18)!=압축크기 || 네바이트읽기(локаль+22)!=Чыгарылыш_үлчәмен_үзгәртү))return -8;
    if(ысул_кертү==0) { if(압축크기!=Чыгарылыш_үлчәмен_үзгәртү)return -8; for(unsigned 순번=0;순번<Чыгарылыш_үлчәмен_үзгәртү;순번++)үлчәм_мәгълүмат[순번]=Архив[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t күчерү_урыны_мәгълүмат={0};uzlib_uncompress_init(&күчерү_урыны_мәгълүмат,0,0);
        күчерү_урыны_мәгълүмат.source=Архив+Start_OFFSET;күчерү_урыны_мәгълүмат.source_limit=күчерү_урыны_мәгълүмат.source+압축크기;күчерү_урыны_мәгълүмат.source_read_cb=файл_тәмамлау;
        /* One extra output byte lets inflate consume/check the end marker. */
        күчерү_урыны_мәгълүмат.dest_start=күчерү_урыны_мәгълүмат.dest=풀린자료;күчерү_урыны_мәгълүмат.dest_limit=풀린자료+Чыгарылыш_үлчәмен_үзгәртү+1;
        int 반환값=uzlib_uncompress(&күчерү_урыны_мәгълүмат);
        if(반환값!=UZLIB_DONE || күчерү_урыны_мәгълүмат.eof || күчерү_урыны_мәгълүмат.dest!=풀린자료+Чыгарылыш_үлчәмен_үзгәртү || күчерү_урыны_мәгълүмат.source!=күчерү_урыны_мәгълүмат.source_limit)return -8;
        for(unsigned 순번=0;순번<Чыгарылыш_үлчәмен_үзгәртү;순번++)үлчәм_мәгълүмат[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(үлчәм_мәгълүмат,Чыгарылыш_үлчәмен_үзгәртү,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return Чыгарылыш_үлчәмен_үзгәртү;
}
int 꾸러미읽기(const char *исем, unsigned char *үлчәм_мәгълүмат, unsigned 수용량) {
    if(!항목들)return -2;unsigned элемент_COUNT=озынлык_VALUE(исем),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==элемент_COUNT && 같음(Архив+현재위치+46,(const unsigned char*)исем,элемент_COUNT))return бүлек(현재위치,үлчәм_мәгълүмат,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return кертү_класс; }
int 꾸러미열기(const char *файл_кертү_исем) {
    항목들=0;кертү_класс[0]=0;
    intptr_t файл_дескриптор=사용자호출(3,(uintptr_t)файл_кертү_исем,0,0,0,0,0);if(файл_дескриптор<0)return файл_дескриптор;
    intptr_t элемент_COUNT=사용자호출(9,файл_дескриптор,0,0,0,0,0);
    if(элемент_COUNT<22 || элемент_COUNT>(intptr_t)sizeof(Архив)) { 사용자호출(4,файл_дескриптор,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,файл_дескриптор,(uintptr_t)Архив,элемент_COUNT,0,0,0);사용자호출(4,файл_дескриптор,0,0,0,0,0);
    if(RECEIVED_COUNT!=элемент_COUNT)return -5;үлчәмен_үзгәртү=элемент_COUNT;
    unsigned тәмамлау_OFFSET=үлчәмен_үзгәртү-22;
    for(;;) { if(네바이트읽기(тәмамлау_OFFSET)==0x06054b50 && тәмамлау_OFFSET+22+두바이트읽기(тәмамлау_OFFSET+20)==үлчәмен_үзгәртү)break; if(!тәмамлау_OFFSET)return -8;тәмамлау_OFFSET--; }
    unsigned кертү_COUNT=두바이트읽기(тәмамлау_OFFSET+10);중앙목록=네바이트읽기(тәмамлау_OFFSET+16);
    if(두바이트읽기(тәмамлау_OFFSET+4)||두바이트읽기(тәмамлау_OFFSET+6)||두바이트읽기(тәмамлау_OFFSET+8)!=кертү_COUNT||!кертү_COUNT||кертү_COUNT>256||!клип(중앙목록,네바이트읽기(тәмамлау_OFFSET+12),тәмамлау_OFFSET)||중앙목록+네바이트읽기(тәмамлау_OFFSET+12)!=тәмамлау_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<кертү_COUNT;순번++) {
        if(!клип(현재위치,46,тәмамлау_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Киләсе_элемент=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!клип(현재위치,Киләсе_элемент,тәмамлау_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Архив[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned озынлык_мәгълүмат=두바이트읽기(다른항목+28);if(озынлык_мәгълүмат==이름길이&&같음(Архив+다른항목+46,Архив+현재위치+46,озынлык_мәгълүмат))return -8;다른항목+=46+озынлык_мәгълүмат+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Киләсе_элемент;
    }
    if(현재위치!=тәмамлау_OFFSET)return -8;항목들=кертү_COUNT;
    unsigned char 꾸러미명세[4096];int төркем_үлчәмен_үзгәртү=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(төркем_үлчәмен_үзгәртү<0){항목들=0;return -8;}
    꾸러미명세[төркем_үлчәмен_үзгәртү]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)төркем_үлчәмен_үзгәртү) {
        unsigned эшләтү=INDEX_VALUE;while(INDEX_VALUE<(unsigned)төркем_үлчәмен_үзгәртү && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned озынлык_мәгълүмат=INDEX_VALUE-эшләтү;if(INDEX_VALUE<(unsigned)төркем_үлчәмен_үзгәртү)INDEX_VALUE++;if(озынлык_мәгълүмат && 꾸러미명세[эшләтү+озынлык_мәгълүмат-1]=='\r')озынлык_мәгълүмат--;
        if(사용량 && озынлык_мәгълүмат && 꾸러미명세[эшләтү]==' ') {эшләтү++;озынлык_мәгълүмат--;}
        else {
            int үлчәм=аергыч_мәгълүмат(논리크기,사용량,&진입점있음);if(үлчәм)return үлчәм;
            사용량=0;if(!озынлык_мәгълүмат)break;
        }
        if(озынлык_мәгълүмат>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<озынлык_мәгълүмат;순번++)논리크기[사용량++]=꾸러미명세[эшләтү+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int үлчәм=аергыч_мәгълүмат(논리크기,사용량,&진입점있음);if(үлчәм)return үлчәм;
    return 진입점있음?0:-8;
}
