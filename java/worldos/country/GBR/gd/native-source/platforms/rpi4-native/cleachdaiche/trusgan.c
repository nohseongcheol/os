#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "trusgan.h"
#include "uzlib.h"
static unsigned char taisg[16384], 풀린자료[16385];
static unsigned atharraich_am_meud, 중앙목록, 항목들;
static char cur_a_steach_clas[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return taisg[현재위치] | taisg[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int cliop(unsigned 현재위치, unsigned nì_COUNT, unsigned 한도) { return 현재위치 <= 한도 && nì_COUNT <= 한도-현재위치; }
static size_t faid_VALUE(const char *sreang_dàta) { size_t nì_COUNT=0; while(sreang_dàta[nì_COUNT]) nì_COUNT++; return nì_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned nì_COUNT) { for(unsigned 순번=0;순번<nì_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int faidhle_crìochnaich(void *미사용값) { (void)미사용값; return -1; }
static int buadh_dàta(const char *loidhne,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)loidhne,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)loidhne,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(cur_a_steach_clas))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char còd_a_charactair=loidhne[12+순번];if(còd_a_charactair<=32||còd_a_charactair=='/'||còd_a_charactair=='\\')return -8;cur_a_steach_clas[순번]=còd_a_charactair;}
        cur_a_steach_clas[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int ball(unsigned 현재위치, unsigned char *tomhas_dàta, unsigned 용량한도) {
    unsigned dòigh_cur_a_steach=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), sgaoileadh_atharraich_am_meud=네바이트읽기(현재위치+24), ionadail=네바이트읽기(현재위치+42);
    unsigned Ainm=두바이트읽기(현재위치+28);
    if(sgaoileadh_atharraich_am_meud>용량한도 || sgaoileadh_atharraich_am_meud>16384 || (dòigh_cur_a_steach!=0 && dòigh_cur_a_steach!=8) || (설정비트&~0x80e))return -8;
    if(!cliop(ionadail,30,중앙목록) || 네바이트읽기(ionadail)!=0x04034b50 || 두바이트읽기(ionadail+8)!=dòigh_cur_a_steach || 두바이트읽기(ionadail+6)!=설정비트 || 두바이트읽기(ionadail+26)!=Ainm)return -8;
    unsigned Start_OFFSET=ionadail+30, 추가영역=두바이트읽기(ionadail+28);
    if(!cliop(Start_OFFSET,Ainm,중앙목록) || !같음(taisg+Start_OFFSET,taisg+현재위치+46,Ainm))return -8;
    Start_OFFSET+=Ainm;if(!cliop(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!cliop(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(ionadail+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(ionadail+18)!=압축크기 || 네바이트읽기(ionadail+22)!=sgaoileadh_atharraich_am_meud))return -8;
    if(dòigh_cur_a_steach==0) { if(압축크기!=sgaoileadh_atharraich_am_meud)return -8; for(unsigned 순번=0;순번<sgaoileadh_atharraich_am_meud;순번++)tomhas_dàta[순번]=taisg[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t ceann_uidhe_dàta={0};uzlib_uncompress_init(&ceann_uidhe_dàta,0,0);
        ceann_uidhe_dàta.source=taisg+Start_OFFSET;ceann_uidhe_dàta.source_limit=ceann_uidhe_dàta.source+압축크기;ceann_uidhe_dàta.source_read_cb=faidhle_crìochnaich;
        /* One extra output byte lets inflate consume/check the end marker. */
        ceann_uidhe_dàta.dest_start=ceann_uidhe_dàta.dest=풀린자료;ceann_uidhe_dàta.dest_limit=풀린자료+sgaoileadh_atharraich_am_meud+1;
        int 반환값=uzlib_uncompress(&ceann_uidhe_dàta);
        if(반환값!=UZLIB_DONE || ceann_uidhe_dàta.eof || ceann_uidhe_dàta.dest!=풀린자료+sgaoileadh_atharraich_am_meud || ceann_uidhe_dàta.source!=ceann_uidhe_dàta.source_limit)return -8;
        for(unsigned 순번=0;순번<sgaoileadh_atharraich_am_meud;순번++)tomhas_dàta[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(tomhas_dàta,sgaoileadh_atharraich_am_meud,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return sgaoileadh_atharraich_am_meud;
}
int 꾸러미읽기(const char *Ainm, unsigned char *tomhas_dàta, unsigned 수용량) {
    if(!항목들)return -2;unsigned nì_COUNT=faid_VALUE(Ainm),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==nì_COUNT && 같음(taisg+현재위치+46,(const unsigned char*)Ainm,nì_COUNT))return ball(현재위치,tomhas_dàta,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return cur_a_steach_clas; }
int 꾸러미열기(const char *faidhle_cur_a_steach_ainm) {
    항목들=0;cur_a_steach_clas[0]=0;
    intptr_t faidhle_làmhrachan=사용자호출(3,(uintptr_t)faidhle_cur_a_steach_ainm,0,0,0,0,0);if(faidhle_làmhrachan<0)return faidhle_làmhrachan;
    intptr_t nì_COUNT=사용자호출(9,faidhle_làmhrachan,0,0,0,0,0);
    if(nì_COUNT<22 || nì_COUNT>(intptr_t)sizeof(taisg)) { 사용자호출(4,faidhle_làmhrachan,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,faidhle_làmhrachan,(uintptr_t)taisg,nì_COUNT,0,0,0);사용자호출(4,faidhle_làmhrachan,0,0,0,0,0);
    if(RECEIVED_COUNT!=nì_COUNT)return -5;atharraich_am_meud=nì_COUNT;
    unsigned crìochnaich_OFFSET=atharraich_am_meud-22;
    for(;;) { if(네바이트읽기(crìochnaich_OFFSET)==0x06054b50 && crìochnaich_OFFSET+22+두바이트읽기(crìochnaich_OFFSET+20)==atharraich_am_meud)break; if(!crìochnaich_OFFSET)return -8;crìochnaich_OFFSET--; }
    unsigned cur_a_steach_COUNT=두바이트읽기(crìochnaich_OFFSET+10);중앙목록=네바이트읽기(crìochnaich_OFFSET+16);
    if(두바이트읽기(crìochnaich_OFFSET+4)||두바이트읽기(crìochnaich_OFFSET+6)||두바이트읽기(crìochnaich_OFFSET+8)!=cur_a_steach_COUNT||!cur_a_steach_COUNT||cur_a_steach_COUNT>256||!cliop(중앙목록,네바이트읽기(crìochnaich_OFFSET+12),crìochnaich_OFFSET)||중앙목록+네바이트읽기(crìochnaich_OFFSET+12)!=crìochnaich_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<cur_a_steach_COUNT;순번++) {
        if(!cliop(현재위치,46,crìochnaich_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),air_adhart_nì=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!cliop(현재위치,air_adhart_nì,crìochnaich_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!taisg[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned faid_dàta=두바이트읽기(다른항목+28);if(faid_dàta==이름길이&&같음(taisg+다른항목+46,taisg+현재위치+46,faid_dàta))return -8;다른항목+=46+faid_dàta+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=air_adhart_nì;
    }
    if(현재위치!=crìochnaich_OFFSET)return -8;항목들=cur_a_steach_COUNT;
    unsigned char 꾸러미명세[4096];int buidheann_atharraich_am_meud=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(buidheann_atharraich_am_meud<0){항목들=0;return -8;}
    꾸러미명세[buidheann_atharraich_am_meud]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)buidheann_atharraich_am_meud) {
        unsigned ruith=INDEX_VALUE;while(INDEX_VALUE<(unsigned)buidheann_atharraich_am_meud && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned faid_dàta=INDEX_VALUE-ruith;if(INDEX_VALUE<(unsigned)buidheann_atharraich_am_meud)INDEX_VALUE++;if(faid_dàta && 꾸러미명세[ruith+faid_dàta-1]=='\r')faid_dàta--;
        if(사용량 && faid_dàta && 꾸러미명세[ruith]==' ') {ruith++;faid_dàta--;}
        else {
            int tomhas=buadh_dàta(논리크기,사용량,&진입점있음);if(tomhas)return tomhas;
            사용량=0;if(!faid_dàta)break;
        }
        if(faid_dàta>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<faid_dàta;순번++)논리크기[사용량++]=꾸러미명세[ruith+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int tomhas=buadh_dàta(논리크기,사용량,&진입점있음);if(tomhas)return tomhas;
    return 진입점있음?0:-8;
}
