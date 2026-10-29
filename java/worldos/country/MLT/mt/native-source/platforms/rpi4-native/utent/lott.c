#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "lott.h"
#include "uzlib.h"
static unsigned char Arkivju[16384], 풀린자료[16385];
static unsigned daqqas, 중앙목록, 항목들;
static char entrata_klassi[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Arkivju[현재위치] | Arkivju[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int klipp(unsigned 현재위치, unsigned element_COUNT, unsigned 한도) { return 현재위치 <= 한도 && element_COUNT <= 한도-현재위치; }
static size_t tul_VALUE(const char *string_data) { size_t element_COUNT=0; while(string_data[element_COUNT]) element_COUNT++; return element_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned element_COUNT) { for(unsigned 순번=0;순번<element_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int fajl_ttermina(void *미사용값) { (void)미사용값; return -1; }
static int attribut_data(const char *linja,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)linja,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)linja,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(entrata_klassi))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char kodiċi_tal_karattru=linja[12+순번];if(kodiċi_tal_karattru<=32||kodiċi_tal_karattru=='/'||kodiċi_tal_karattru=='\\')return -8;entrata_klassi[순번]=kodiċi_tal_karattru;}
        entrata_klassi[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int membru(unsigned 현재위치, unsigned char *miżura_data, unsigned 용량한도) {
    unsigned metodu_entrata=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), mexxi_daqqas=네바이트읽기(현재위치+24), lokali=네바이트읽기(현재위치+42);
    unsigned isem=두바이트읽기(현재위치+28);
    if(mexxi_daqqas>용량한도 || mexxi_daqqas>16384 || (metodu_entrata!=0 && metodu_entrata!=8) || (설정비트&~0x80e))return -8;
    if(!klipp(lokali,30,중앙목록) || 네바이트읽기(lokali)!=0x04034b50 || 두바이트읽기(lokali+8)!=metodu_entrata || 두바이트읽기(lokali+6)!=설정비트 || 두바이트읽기(lokali+26)!=isem)return -8;
    unsigned Bidu_OFFSET=lokali+30, 추가영역=두바이트읽기(lokali+28);
    if(!klipp(Bidu_OFFSET,isem,중앙목록) || !같음(Arkivju+Bidu_OFFSET,Arkivju+현재위치+46,isem))return -8;
    Bidu_OFFSET+=isem;if(!klipp(Bidu_OFFSET,추가영역,중앙목록))return -8;Bidu_OFFSET+=추가영역;
    if(!klipp(Bidu_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(lokali+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokali+18)!=압축크기 || 네바이트읽기(lokali+22)!=mexxi_daqqas))return -8;
    if(metodu_entrata==0) { if(압축크기!=mexxi_daqqas)return -8; for(unsigned 순번=0;순번<mexxi_daqqas;순번++)miżura_data[순번]=Arkivju[Bidu_OFFSET+순번]; }
    else {
        uzlib_uncomp_t destinazzjoni_data={0};uzlib_uncompress_init(&destinazzjoni_data,0,0);
        destinazzjoni_data.source=Arkivju+Bidu_OFFSET;destinazzjoni_data.source_limit=destinazzjoni_data.source+압축크기;destinazzjoni_data.source_read_cb=fajl_ttermina;
        /* One extra output byte lets inflate consume/check the end marker. */
        destinazzjoni_data.dest_start=destinazzjoni_data.dest=풀린자료;destinazzjoni_data.dest_limit=풀린자료+mexxi_daqqas+1;
        int 반환값=uzlib_uncompress(&destinazzjoni_data);
        if(반환값!=UZLIB_DONE || destinazzjoni_data.eof || destinazzjoni_data.dest!=풀린자료+mexxi_daqqas || destinazzjoni_data.source!=destinazzjoni_data.source_limit)return -8;
        for(unsigned 순번=0;순번<mexxi_daqqas;순번++)miżura_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(miżura_data,mexxi_daqqas,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return mexxi_daqqas;
}
int 꾸러미읽기(const char *isem, unsigned char *miżura_data, unsigned 수용량) {
    if(!항목들)return -2;unsigned element_COUNT=tul_VALUE(isem),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==element_COUNT && 같음(Arkivju+현재위치+46,(const unsigned char*)isem,element_COUNT))return membru(현재위치,miżura_data,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return entrata_klassi; }
int 꾸러미열기(const char *fajl_entrata_isem) {
    항목들=0;entrata_klassi[0]=0;
    intptr_t fajl_handle=사용자호출(3,(uintptr_t)fajl_entrata_isem,0,0,0,0,0);if(fajl_handle<0)return fajl_handle;
    intptr_t element_COUNT=사용자호출(9,fajl_handle,0,0,0,0,0);
    if(element_COUNT<22 || element_COUNT>(intptr_t)sizeof(Arkivju)) { 사용자호출(4,fajl_handle,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,fajl_handle,(uintptr_t)Arkivju,element_COUNT,0,0,0);사용자호출(4,fajl_handle,0,0,0,0,0);
    if(RECEIVED_COUNT!=element_COUNT)return -5;daqqas=element_COUNT;
    unsigned ttermina_OFFSET=daqqas-22;
    for(;;) { if(네바이트읽기(ttermina_OFFSET)==0x06054b50 && ttermina_OFFSET+22+두바이트읽기(ttermina_OFFSET+20)==daqqas)break; if(!ttermina_OFFSET)return -8;ttermina_OFFSET--; }
    unsigned entrata_COUNT=두바이트읽기(ttermina_OFFSET+10);중앙목록=네바이트읽기(ttermina_OFFSET+16);
    if(두바이트읽기(ttermina_OFFSET+4)||두바이트읽기(ttermina_OFFSET+6)||두바이트읽기(ttermina_OFFSET+8)!=entrata_COUNT||!entrata_COUNT||entrata_COUNT>256||!klipp(중앙목록,네바이트읽기(ttermina_OFFSET+12),ttermina_OFFSET)||중앙목록+네바이트읽기(ttermina_OFFSET+12)!=ttermina_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<entrata_COUNT;순번++) {
        if(!klipp(현재위치,46,ttermina_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Li_Jmiss_element=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!klipp(현재위치,Li_Jmiss_element,ttermina_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkivju[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned tul_data=두바이트읽기(다른항목+28);if(tul_data==이름길이&&같음(Arkivju+다른항목+46,Arkivju+현재위치+46,tul_data))return -8;다른항목+=46+tul_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Li_Jmiss_element;
    }
    if(현재위치!=ttermina_OFFSET)return -8;항목들=entrata_COUNT;
    unsigned char 꾸러미명세[4096];int grupp_daqqas=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(grupp_daqqas<0){항목들=0;return -8;}
    꾸러미명세[grupp_daqqas]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)grupp_daqqas) {
        unsigned serje=INDEX_VALUE;while(INDEX_VALUE<(unsigned)grupp_daqqas && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned tul_data=INDEX_VALUE-serje;if(INDEX_VALUE<(unsigned)grupp_daqqas)INDEX_VALUE++;if(tul_data && 꾸러미명세[serje+tul_data-1]=='\r')tul_data--;
        if(사용량 && tul_data && 꾸러미명세[serje]==' ') {serje++;tul_data--;}
        else {
            int miżura=attribut_data(논리크기,사용량,&진입점있음);if(miżura)return miżura;
            사용량=0;if(!tul_data)break;
        }
        if(tul_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<tul_data;순번++)논리크기[사용량++]=꾸러미명세[serje+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int miżura=attribut_data(논리크기,사용량,&진입점있음);if(miżura)return miżura;
    return 진입점있음?0:-8;
}
