#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "takku_xéewël.h"
#include "uzlib.h"
static unsigned char denc[16384], 풀린자료[16385];
static unsigned tolluwaay, 중앙목록, 항목들;
static char dugal_xabaar_maas[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return denc[현재위치] | denc[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int kilip(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t diir_xëyma(const char *araf_yu_bennoo_mbir) { size_t 개수=0; while(araf_yu_bennoo_mbir[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int bara_denc_jeexal(void *미사용값) { (void)미사용값; return -1; }
static int jagle_mbir(const char *buum,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)buum,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)buum,(const unsigned char*)"Main-Class: ",12)) {
        unsigned xëyma=사용량-12;if(*진입점있음||!xëyma||xëyma>=sizeof(dugal_xabaar_maas))return -8;
        for(unsigned 순번=0;순번<xëyma;순번++){unsigned char kotu_araf=buum[12+순번];if(kotu_araf<=32||kotu_araf=='/'||kotu_araf=='\\')return -8;dugal_xabaar_maas[순번]=kotu_araf;}
        dugal_xabaar_maas[xëyma]=0;*진입점있음=1;
    }
    return 0;
}
static int Way_bokk(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned doxalin_dugal_xabaar=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), yewwi_tolluwaay=네바이트읽기(현재위치+24), dënnd=네바이트읽기(현재위치+42);
    unsigned tur_253d1510=두바이트읽기(현재위치+28);
    if(yewwi_tolluwaay>용량한도 || yewwi_tolluwaay>16384 || (doxalin_dugal_xabaar!=0 && doxalin_dugal_xabaar!=8) || (설정비트&~0x80e))return -8;
    if(!kilip(dënnd,30,중앙목록) || 네바이트읽기(dënnd)!=0x04034b50 || 두바이트읽기(dënnd+8)!=doxalin_dugal_xabaar || 두바이트읽기(dënnd+6)!=설정비트 || 두바이트읽기(dënnd+26)!=tur_253d1510)return -8;
    unsigned Door_Randal=dënnd+30, 추가영역=두바이트읽기(dënnd+28);
    if(!kilip(Door_Randal,tur_253d1510,중앙목록) || !같음(denc+Door_Randal,denc+현재위치+46,tur_253d1510))return -8;
    Door_Randal+=tur_253d1510;if(!kilip(Door_Randal,추가영역,중앙목록))return -8;Door_Randal+=추가영역;
    if(!kilip(Door_Randal,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(dënnd+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(dënnd+18)!=압축크기 || 네바이트읽기(dënnd+22)!=yewwi_tolluwaay))return -8;
    if(doxalin_dugal_xabaar==0) { if(압축크기!=yewwi_tolluwaay)return -8; for(unsigned 순번=0;순번<yewwi_tolluwaay;순번++)결과자료[순번]=denc[Door_Randal+순번]; }
    else {
        uzlib_uncomp_t jëmmukaay_mbir={0};uzlib_uncompress_init(&jëmmukaay_mbir,0,0);
        jëmmukaay_mbir.source=denc+Door_Randal;jëmmukaay_mbir.source_limit=jëmmukaay_mbir.source+압축크기;jëmmukaay_mbir.source_read_cb=bara_denc_jeexal;
        /* One extra output byte lets inflate consume/check the end marker. */
        jëmmukaay_mbir.dest_start=jëmmukaay_mbir.dest=풀린자료;jëmmukaay_mbir.dest_limit=풀린자료+yewwi_tolluwaay+1;
        int 반환값=uzlib_uncompress(&jëmmukaay_mbir);
        if(반환값!=UZLIB_DONE || jëmmukaay_mbir.eof || jëmmukaay_mbir.dest!=풀린자료+yewwi_tolluwaay || jëmmukaay_mbir.source!=jëmmukaay_mbir.source_limit)return -8;
        for(unsigned 순번=0;순번<yewwi_tolluwaay;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,yewwi_tolluwaay,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return yewwi_tolluwaay;
}
int 꾸러미읽기(const char *tur_253d1510, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=diir_xëyma(tur_253d1510),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(denc+현재위치+46,(const unsigned char*)tur_253d1510,개수))return Way_bokk(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return dugal_xabaar_maas; }
int 꾸러미열기(const char *bara_denc_dugal_xabaar_tur) {
    항목들=0;dugal_xabaar_maas[0]=0;
    intptr_t bara_denc_yombal=사용자호출(3,(uintptr_t)bara_denc_dugal_xabaar_tur,0,0,0,0,0);if(bara_denc_yombal<0)return bara_denc_yombal;
    intptr_t 개수=사용자호출(9,bara_denc_yombal,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(denc)) { 사용자호출(4,bara_denc_yombal,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,bara_denc_yombal,(uintptr_t)denc,개수,0,0,0);사용자호출(4,bara_denc_yombal,0,0,0,0,0);
    if(받은수!=개수)return -5;tolluwaay=개수;
    unsigned jeexal_Randal=tolluwaay-22;
    for(;;) { if(네바이트읽기(jeexal_Randal)==0x06054b50 && jeexal_Randal+22+두바이트읽기(jeexal_Randal+20)==tolluwaay)break; if(!jeexal_Randal)return -8;jeexal_Randal--; }
    unsigned 항목수=두바이트읽기(jeexal_Randal+10);중앙목록=네바이트읽기(jeexal_Randal+16);
    if(두바이트읽기(jeexal_Randal+4)||두바이트읽기(jeexal_Randal+6)||두바이트읽기(jeexal_Randal+8)!=항목수||!항목수||항목수>256||!kilip(중앙목록,네바이트읽기(jeexal_Randal+12),jeexal_Randal)||중앙목록+네바이트읽기(jeexal_Randal+12)!=jeexal_Randal)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!kilip(현재위치,46,jeexal_Randal)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!kilip(현재위치,다음,jeexal_Randal)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!denc[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned diir_mbir=두바이트읽기(다른항목+28);if(diir_mbir==이름길이&&같음(denc+다른항목+46,denc+현재위치+46,diir_mbir))return -8;다른항목+=46+diir_mbir+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=jeexal_Randal)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int mboolo_tolluwaay=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(mboolo_tolluwaay<0){항목들=0;return -8;}
    꾸러미명세[mboolo_tolluwaay]=0;
    char 논리크기[512];unsigned 사용량=0,àlluwa_tur_xëyma=0;int 진입점있음=0;
    while(àlluwa_tur_xëyma<(unsigned)mboolo_tolluwaay) {
        unsigned daw=àlluwa_tur_xëyma;while(àlluwa_tur_xëyma<(unsigned)mboolo_tolluwaay && 꾸러미명세[àlluwa_tur_xëyma]!='\n')àlluwa_tur_xëyma++;
        unsigned diir_mbir=àlluwa_tur_xëyma-daw;if(àlluwa_tur_xëyma<(unsigned)mboolo_tolluwaay)àlluwa_tur_xëyma++;if(diir_mbir && 꾸러미명세[daw+diir_mbir-1]=='\r')diir_mbir--;
        if(사용량 && diir_mbir && 꾸러미명세[daw]==' ') {daw++;diir_mbir--;}
        else {
            int 결과=jagle_mbir(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!diir_mbir)break;
        }
        if(diir_mbir>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<diir_mbir;순번++)논리크기[사용량++]=꾸러미명세[daw+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=jagle_mbir(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
