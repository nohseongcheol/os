#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "búnt.h"
#include "uzlib.h"
static unsigned char Safn[16384], 풀린자료[16385];
static unsigned Stærð, 중앙목록, 항목들;
static char færsla_klasi[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Safn[현재위치] | Safn[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int miðlaskrá(unsigned 현재위치, unsigned vara_COUNT, unsigned 한도) { return 현재위치 <= 한도 && vara_COUNT <= 한도-현재위치; }
static size_t lengd_VALUE(const char *strengur_gögn) { size_t vara_COUNT=0; while(strengur_gögn[vara_COUNT]) vara_COUNT++; return vara_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned vara_COUNT) { for(unsigned 순번=0;순번<vara_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int skrá_ljúka(void *미사용값) { (void)미사용값; return -1; }
static int eigind_gögn(const char *Lína,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Lína,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Lína,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(færsla_klasi))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char stafkóði=Lína[12+순번];if(stafkóði<=32||stafkóði=='/'||stafkóði=='\\')return -8;færsla_klasi[순번]=stafkóði;}
        færsla_klasi[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int aðili(unsigned 현재위치, unsigned char *mæld_stærð_gögn, unsigned 용량한도) {
    unsigned aðferð_færsla=두바이트읽기(현재위치+10), afbrigði_Background_Intelligent_Transfer_Service=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), losa_breyta_stærð=네바이트읽기(현재위치+24), staðbundið=네바이트읽기(현재위치+42);
    unsigned Heiti=두바이트읽기(현재위치+28);
    if(losa_breyta_stærð>용량한도 || losa_breyta_stærð>16384 || (aðferð_færsla!=0 && aðferð_færsla!=8) || (afbrigði_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!miðlaskrá(staðbundið,30,중앙목록) || 네바이트읽기(staðbundið)!=0x04034b50 || 두바이트읽기(staðbundið+8)!=aðferð_færsla || 두바이트읽기(staðbundið+6)!=afbrigði_Background_Intelligent_Transfer_Service || 두바이트읽기(staðbundið+26)!=Heiti)return -8;
    unsigned Opna_OFFSET=staðbundið+30, 추가영역=두바이트읽기(staðbundið+28);
    if(!miðlaskrá(Opna_OFFSET,Heiti,중앙목록) || !같음(Safn+Opna_OFFSET,Safn+현재위치+46,Heiti))return -8;
    Opna_OFFSET+=Heiti;if(!miðlaskrá(Opna_OFFSET,추가영역,중앙목록))return -8;Opna_OFFSET+=추가영역;
    if(!miðlaskrá(Opna_OFFSET,압축크기,중앙목록))return -8;
    if(!(afbrigði_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(staðbundið+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(staðbundið+18)!=압축크기 || 네바이트읽기(staðbundið+22)!=losa_breyta_stærð))return -8;
    if(aðferð_færsla==0) { if(압축크기!=losa_breyta_stærð)return -8; for(unsigned 순번=0;순번<losa_breyta_stærð;순번++)mæld_stærð_gögn[순번]=Safn[Opna_OFFSET+순번]; }
    else {
        uzlib_uncomp_t endastaður_gögn={0};uzlib_uncompress_init(&endastaður_gögn,0,0);
        endastaður_gögn.source=Safn+Opna_OFFSET;endastaður_gögn.source_limit=endastaður_gögn.source+압축크기;endastaður_gögn.source_read_cb=skrá_ljúka;
        /* One extra output byte lets inflate consume/check the end marker. */
        endastaður_gögn.dest_start=endastaður_gögn.dest=풀린자료;endastaður_gögn.dest_limit=풀린자료+losa_breyta_stærð+1;
        int 반환값=uzlib_uncompress(&endastaður_gögn);
        if(반환값!=UZLIB_DONE || endastaður_gögn.eof || endastaður_gögn.dest!=풀린자료+losa_breyta_stærð || endastaður_gögn.source!=endastaður_gögn.source_limit)return -8;
        for(unsigned 순번=0;순번<losa_breyta_stærð;순번++)mæld_stærð_gögn[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(mæld_stærð_gögn,losa_breyta_stærð,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return losa_breyta_stærð;
}
int 꾸러미읽기(const char *Heiti, unsigned char *mæld_stærð_gögn, unsigned biðminni_afkastageta) {
    if(!항목들)return -2;unsigned vara_COUNT=lengd_VALUE(Heiti),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==vara_COUNT && 같음(Safn+현재위치+46,(const unsigned char*)Heiti,vara_COUNT))return aðili(현재위치,mæld_stærð_gögn,biðminni_afkastageta);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return færsla_klasi; }
int 꾸러미열기(const char *skrá_færsla_heiti) {
    항목들=0;færsla_klasi[0]=0;
    intptr_t skrá_hald=사용자호출(3,(uintptr_t)skrá_færsla_heiti,0,0,0,0,0);if(skrá_hald<0)return skrá_hald;
    intptr_t vara_COUNT=사용자호출(9,skrá_hald,0,0,0,0,0);
    if(vara_COUNT<22 || vara_COUNT>(intptr_t)sizeof(Safn)) { 사용자호출(4,skrá_hald,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,skrá_hald,(uintptr_t)Safn,vara_COUNT,0,0,0);사용자호출(4,skrá_hald,0,0,0,0,0);
    if(RECEIVED_COUNT!=vara_COUNT)return -5;Stærð=vara_COUNT;
    unsigned ljúka_OFFSET=Stærð-22;
    for(;;) { if(네바이트읽기(ljúka_OFFSET)==0x06054b50 && ljúka_OFFSET+22+두바이트읽기(ljúka_OFFSET+20)==Stærð)break; if(!ljúka_OFFSET)return -8;ljúka_OFFSET--; }
    unsigned færsla_COUNT=두바이트읽기(ljúka_OFFSET+10);중앙목록=네바이트읽기(ljúka_OFFSET+16);
    if(두바이트읽기(ljúka_OFFSET+4)||두바이트읽기(ljúka_OFFSET+6)||두바이트읽기(ljúka_OFFSET+8)!=færsla_COUNT||!færsla_COUNT||færsla_COUNT>256||!miðlaskrá(중앙목록,네바이트읽기(ljúka_OFFSET+12),ljúka_OFFSET)||중앙목록+네바이트읽기(ljúka_OFFSET+12)!=ljúka_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<færsla_COUNT;순번++) {
        if(!miðlaskrá(현재위치,46,ljúka_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Áfram_vara=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!miðlaskrá(현재위치,Áfram_vara,ljúka_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Safn[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned lengd_gögn=두바이트읽기(다른항목+28);if(lengd_gögn==이름길이&&같음(Safn+다른항목+46,Safn+현재위치+46,lengd_gögn))return -8;다른항목+=46+lengd_gögn+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Áfram_vara;
    }
    if(현재위치!=ljúka_OFFSET)return -8;항목들=færsla_COUNT;
    unsigned char búnt_skrá[4096];int Hópur_breyta_stærð=꾸러미읽기("META-INF/MANIFEST.MF",búnt_skrá,sizeof(búnt_skrá)-1);if(Hópur_breyta_stærð<0){항목들=0;return -8;}
    búnt_skrá[Hópur_breyta_stærð]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Hópur_breyta_stærð) {
        unsigned Keyra_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Hópur_breyta_stærð && búnt_skrá[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned lengd_gögn=INDEX_VALUE-Keyra_2;if(INDEX_VALUE<(unsigned)Hópur_breyta_stærð)INDEX_VALUE++;if(lengd_gögn && búnt_skrá[Keyra_2+lengd_gögn-1]=='\r')lengd_gögn--;
        if(사용량 && lengd_gögn && búnt_skrá[Keyra_2]==' ') {Keyra_2++;lengd_gögn--;}
        else {
            int NIÐURSTAÐA=eigind_gögn(논리크기,사용량,&진입점있음);if(NIÐURSTAÐA)return NIÐURSTAÐA;
            사용량=0;if(!lengd_gögn)break;
        }
        if(lengd_gögn>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<lengd_gögn;순번++)논리크기[사용량++]=búnt_skrá[Keyra_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int NIÐURSTAÐA=eigind_gögn(논리크기,사용량,&진입점있음);if(NIÐURSTAÐA)return NIÐURSTAÐA;
    return 진입점있음?0:-8;
}
