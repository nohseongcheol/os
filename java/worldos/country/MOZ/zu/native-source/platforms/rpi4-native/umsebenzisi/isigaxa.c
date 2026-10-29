#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "isigaxa.h"
#include "uzlib.h"
static unsigned char londoloza[16384], 풀린자료[16385];
static unsigned Ubungako, 중앙목록, 항목들;
static char okufakwayo_uhlobo[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return londoloza[현재위치] | londoloza[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int isiqeshana(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t ubude_inani(const char *uchunge_imininingwane) { size_t 개수=0; while(uchunge_imininingwane[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int ifayela_yekisa(void *미사용값) { (void)미사용값; return -1; }
static int isibaluli_imininingwane(const char *umugqa,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)umugqa,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)umugqa,(const unsigned char*)"Main-Class: ",12)) {
        unsigned inani=사용량-12;if(*진입점있음||!inani||inani>=sizeof(okufakwayo_uhlobo))return -8;
        for(unsigned 순번=0;순번<inani;순번++){unsigned char ikhodi_yohlamvu=umugqa[12+순번];if(ikhodi_yohlamvu<=32||ikhodi_yohlamvu=='/'||ikhodi_yohlamvu=='\\')return -8;okufakwayo_uhlobo[순번]=ikhodi_yohlamvu;}
        okufakwayo_uhlobo[inani]=0;*진입점있음=1;
    }
    return 0;
}
static int ilungu(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned indlela_okufakwayo=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), khulula_linganisa=네바이트읽기(현재위치+24), endaweni=네바이트읽기(현재위치+42);
    unsigned Igama=두바이트읽기(현재위치+28);
    if(khulula_linganisa>용량한도 || khulula_linganisa>16384 || (indlela_okufakwayo!=0 && indlela_okufakwayo!=8) || (설정비트&~0x80e))return -8;
    if(!isiqeshana(endaweni,30,중앙목록) || 네바이트읽기(endaweni)!=0x04034b50 || 두바이트읽기(endaweni+8)!=indlela_okufakwayo || 두바이트읽기(endaweni+6)!=설정비트 || 두바이트읽기(endaweni+26)!=Igama)return -8;
    unsigned qala_I_ofisethi=endaweni+30, 추가영역=두바이트읽기(endaweni+28);
    if(!isiqeshana(qala_I_ofisethi,Igama,중앙목록) || !같음(londoloza+qala_I_ofisethi,londoloza+현재위치+46,Igama))return -8;
    qala_I_ofisethi+=Igama;if(!isiqeshana(qala_I_ofisethi,추가영역,중앙목록))return -8;qala_I_ofisethi+=추가영역;
    if(!isiqeshana(qala_I_ofisethi,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(endaweni+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(endaweni+18)!=압축크기 || 네바이트읽기(endaweni+22)!=khulula_linganisa))return -8;
    if(indlela_okufakwayo==0) { if(압축크기!=khulula_linganisa)return -8; for(unsigned 순번=0;순번<khulula_linganisa;순번++)결과자료[순번]=londoloza[qala_I_ofisethi+순번]; }
    else {
        uzlib_uncomp_t isikhumulo_imininingwane={0};uzlib_uncompress_init(&isikhumulo_imininingwane,0,0);
        isikhumulo_imininingwane.source=londoloza+qala_I_ofisethi;isikhumulo_imininingwane.source_limit=isikhumulo_imininingwane.source+압축크기;isikhumulo_imininingwane.source_read_cb=ifayela_yekisa;
        /* One extra output byte lets inflate consume/check the end marker. */
        isikhumulo_imininingwane.dest_start=isikhumulo_imininingwane.dest=풀린자료;isikhumulo_imininingwane.dest_limit=풀린자료+khulula_linganisa+1;
        int 반환값=uzlib_uncompress(&isikhumulo_imininingwane);
        if(반환값!=UZLIB_DONE || isikhumulo_imininingwane.eof || isikhumulo_imininingwane.dest!=풀린자료+khulula_linganisa || isikhumulo_imininingwane.source!=isikhumulo_imininingwane.source_limit)return -8;
        for(unsigned 순번=0;순번<khulula_linganisa;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,khulula_linganisa,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return khulula_linganisa;
}
int 꾸러미읽기(const char *Igama, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=ubude_inani(Igama),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(londoloza+현재위치+46,(const unsigned char*)Igama,개수))return ilungu(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return okufakwayo_uhlobo; }
int 꾸러미열기(const char *ifayela_okufakwayo_igama) {
    항목들=0;okufakwayo_uhlobo[0]=0;
    intptr_t ifayela_isibambo=사용자호출(3,(uintptr_t)ifayela_okufakwayo_igama,0,0,0,0,0);if(ifayela_isibambo<0)return ifayela_isibambo;
    intptr_t 개수=사용자호출(9,ifayela_isibambo,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(londoloza)) { 사용자호출(4,ifayela_isibambo,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,ifayela_isibambo,(uintptr_t)londoloza,개수,0,0,0);사용자호출(4,ifayela_isibambo,0,0,0,0,0);
    if(받은수!=개수)return -5;Ubungako=개수;
    unsigned yekisa_I_ofisethi=Ubungako-22;
    for(;;) { if(네바이트읽기(yekisa_I_ofisethi)==0x06054b50 && yekisa_I_ofisethi+22+두바이트읽기(yekisa_I_ofisethi+20)==Ubungako)break; if(!yekisa_I_ofisethi)return -8;yekisa_I_ofisethi--; }
    unsigned 항목수=두바이트읽기(yekisa_I_ofisethi+10);중앙목록=네바이트읽기(yekisa_I_ofisethi+16);
    if(두바이트읽기(yekisa_I_ofisethi+4)||두바이트읽기(yekisa_I_ofisethi+6)||두바이트읽기(yekisa_I_ofisethi+8)!=항목수||!항목수||항목수>256||!isiqeshana(중앙목록,네바이트읽기(yekisa_I_ofisethi+12),yekisa_I_ofisethi)||중앙목록+네바이트읽기(yekisa_I_ofisethi+12)!=yekisa_I_ofisethi)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!isiqeshana(현재위치,46,yekisa_I_ofisethi)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!isiqeshana(현재위치,다음,yekisa_I_ofisethi)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!londoloza[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned ubude_imininingwane=두바이트읽기(다른항목+28);if(ubude_imininingwane==이름길이&&같음(londoloza+다른항목+46,londoloza+현재위치+46,ubude_imininingwane))return -8;다른항목+=46+ubude_imininingwane+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=yekisa_I_ofisethi)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int iqoqo_linganisa=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(iqoqo_linganisa<0){항목들=0;return -8;}
    꾸러미명세[iqoqo_linganisa]=0;
    char 논리크기[512];unsigned 사용량=0,thola_inkomba_inani=0;int 진입점있음=0;
    while(thola_inkomba_inani<(unsigned)iqoqo_linganisa) {
        unsigned Sebenzisa=thola_inkomba_inani;while(thola_inkomba_inani<(unsigned)iqoqo_linganisa && 꾸러미명세[thola_inkomba_inani]!='\n')thola_inkomba_inani++;
        unsigned ubude_imininingwane=thola_inkomba_inani-Sebenzisa;if(thola_inkomba_inani<(unsigned)iqoqo_linganisa)thola_inkomba_inani++;if(ubude_imininingwane && 꾸러미명세[Sebenzisa+ubude_imininingwane-1]=='\r')ubude_imininingwane--;
        if(사용량 && ubude_imininingwane && 꾸러미명세[Sebenzisa]==' ') {Sebenzisa++;ubude_imininingwane--;}
        else {
            int 결과=isibaluli_imininingwane(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!ubude_imininingwane)break;
        }
        if(ubude_imininingwane>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<ubude_imininingwane;순번++)논리크기[사용량++]=꾸러미명세[Sebenzisa+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=isibaluli_imininingwane(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
