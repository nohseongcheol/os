#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "пакет.h"
#include "uzlib.h"
static unsigned char Архива[16384], 풀린자료[16385];
static unsigned Големина, 중앙목록, 항목들;
static char внес_класа[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Архива[현재위치] | Архива[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int клип(unsigned 현재위치, unsigned ставка_COUNT, unsigned 한도) { return 현재위치 <= 한도 && ставка_COUNT <= 한도-현재위치; }
static size_t должина_VALUE(const char *низа_податоци) { size_t ставка_COUNT=0; while(низа_податоци[ставка_COUNT]) ставка_COUNT++; return ставка_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned ставка_COUNT) { for(unsigned 순번=0;순번<ставка_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int датотека_крај(void *미사용값) { (void)미사용값; return -1; }
static int атрибут_податоци(const char *ред,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)ред,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)ред,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(внес_класа))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char кодна_точка=ред[12+순번];if(кодна_точка<=32||кодна_точка=='/'||кодна_точка=='\\')return -8;внес_класа[순번]=кодна_точка;}
        внес_класа[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int член(unsigned 현재위치, unsigned char *мерка_податоци, unsigned 용량한도) {
    unsigned метод_внес=두바이트읽기(현재위치+10), конфигурација_Услуга_за_интелигентен_пренос_во_заднина=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), издание_големина=네바이트읽기(현재위치+24), локален=네바이트읽기(현재위치+42);
    unsigned Име=두바이트읽기(현재위치+28);
    if(издание_големина>용량한도 || издание_големина>16384 || (метод_внес!=0 && метод_внес!=8) || (конфигурација_Услуга_за_интелигентен_пренос_во_заднина&~0x80e))return -8;
    if(!клип(локален,30,중앙목록) || 네바이트읽기(локален)!=0x04034b50 || 두바이트읽기(локален+8)!=метод_внес || 두바이트읽기(локален+6)!=конфигурација_Услуга_за_интелигентен_пренос_во_заднина || 두바이트읽기(локален+26)!=Име)return -8;
    unsigned Start_OFFSET=локален+30, 추가영역=두바이트읽기(локален+28);
    if(!клип(Start_OFFSET,Име,중앙목록) || !같음(Архива+Start_OFFSET,Архива+현재위치+46,Име))return -8;
    Start_OFFSET+=Име;if(!клип(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!клип(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(конфигурација_Услуга_за_интелигентен_пренос_во_заднина&8) && (네바이트읽기(локален+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(локален+18)!=압축크기 || 네바이트읽기(локален+22)!=издание_големина))return -8;
    if(метод_внес==0) { if(압축크기!=издание_големина)return -8; for(unsigned 순번=0;순번<издание_големина;순번++)мерка_податоци[순번]=Архива[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t одредиште_податоци={0};uzlib_uncompress_init(&одредиште_податоци,0,0);
        одредиште_податоци.source=Архива+Start_OFFSET;одредиште_податоци.source_limit=одредиште_податоци.source+압축크기;одредиште_податоци.source_read_cb=датотека_крај;
        /* One extra output byte lets inflate consume/check the end marker. */
        одредиште_податоци.dest_start=одредиште_податоци.dest=풀린자료;одредиште_податоци.dest_limit=풀린자료+издание_големина+1;
        int 반환값=uzlib_uncompress(&одредиште_податоци);
        if(반환값!=UZLIB_DONE || одредиште_податоци.eof || одредиште_податоци.dest!=풀린자료+издание_големина || одредиште_податоци.source!=одредиште_податоци.source_limit)return -8;
        for(unsigned 순번=0;순번<издание_големина;순번++)мерка_податоци[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(мерка_податоци,издание_големина,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return издание_големина;
}
int 꾸러미읽기(const char *Име, unsigned char *мерка_податоци, unsigned 수용량) {
    if(!항목들)return -2;unsigned ставка_COUNT=должина_VALUE(Име),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==ставка_COUNT && 같음(Архива+현재위치+46,(const unsigned char*)Име,ставка_COUNT))return член(현재위치,мерка_податоци,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return внес_класа; }
int 꾸러미열기(const char *датотека_внес_име) {
    항목들=0;внес_класа[0]=0;
    intptr_t датотека_рачка=사용자호출(3,(uintptr_t)датотека_внес_име,0,0,0,0,0);if(датотека_рачка<0)return датотека_рачка;
    intptr_t ставка_COUNT=사용자호출(9,датотека_рачка,0,0,0,0,0);
    if(ставка_COUNT<22 || ставка_COUNT>(intptr_t)sizeof(Архива)) { 사용자호출(4,датотека_рачка,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,датотека_рачка,(uintptr_t)Архива,ставка_COUNT,0,0,0);사용자호출(4,датотека_рачка,0,0,0,0,0);
    if(RECEIVED_COUNT!=ставка_COUNT)return -5;Големина=ставка_COUNT;
    unsigned крај_OFFSET=Големина-22;
    for(;;) { if(네바이트읽기(крај_OFFSET)==0x06054b50 && крај_OFFSET+22+두바이트읽기(крај_OFFSET+20)==Големина)break; if(!крај_OFFSET)return -8;крај_OFFSET--; }
    unsigned внес_COUNT=두바이트읽기(крај_OFFSET+10);중앙목록=네바이트읽기(крај_OFFSET+16);
    if(두바이트읽기(крај_OFFSET+4)||두바이트읽기(крај_OFFSET+6)||두바이트읽기(крај_OFFSET+8)!=внес_COUNT||!внес_COUNT||внес_COUNT>256||!клип(중앙목록,네바이트읽기(крај_OFFSET+12),крај_OFFSET)||중앙목록+네바이트읽기(крај_OFFSET+12)!=крај_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<внес_COUNT;순번++) {
        if(!клип(현재위치,46,крај_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Следно_ставка=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!клип(현재위치,Следно_ставка,крај_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Архива[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned должина_податоци=두바이트읽기(다른항목+28);if(должина_податоци==이름길이&&같음(Архива+다른항목+46,Архива+현재위치+46,должина_податоци))return -8;다른항목+=46+должина_податоци+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Следно_ставка;
    }
    if(현재위치!=крај_OFFSET)return -8;항목들=внес_COUNT;
    unsigned char 꾸러미명세[4096];int Група_големина=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Група_големина<0){항목들=0;return -8;}
    꾸러미명세[Група_големина]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Група_големина) {
        unsigned Изврши_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Група_големина && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned должина_податоци=INDEX_VALUE-Изврши_2;if(INDEX_VALUE<(unsigned)Група_големина)INDEX_VALUE++;if(должина_податоци && 꾸러미명세[Изврши_2+должина_податоци-1]=='\r')должина_податоци--;
        if(사용량 && должина_податоци && 꾸러미명세[Изврши_2]==' ') {Изврши_2++;должина_податоци--;}
        else {
            int мерка=атрибут_податоци(논리크기,사용량,&진입점있음);if(мерка)return мерка;
            사용량=0;if(!должина_податоци)break;
        }
        if(должина_податоци>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<должина_податоци;순번++)논리크기[사용량++]=꾸러미명세[Изврши_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int мерка=атрибут_податоци(논리크기,사용량,&진입점있음);if(мерка)return мерка;
    return 진입점있음?0:-8;
}
