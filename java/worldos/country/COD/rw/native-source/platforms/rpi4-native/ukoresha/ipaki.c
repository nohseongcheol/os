#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "ipaki.h"
#include "uzlib.h"
static unsigned char gushyingura[16384], 풀린자료[16385];
static unsigned Ingano, 중앙목록, 항목들;
static char icyinjizwa_icyiciro[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return gushyingura[현재위치] | gushyingura[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int kiripu(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t uburebure_agaciro(const char *igicenteruro_amakurushingiro) { size_t 개수=0; while(igicenteruro_amakurushingiro[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int dosiye_kurangiza(void *미사용값) { (void)미사용값; return -1; }
static int ikiranga_amakurushingiro(const char *umurongo,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)umurongo,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)umurongo,(const unsigned char*)"Main-Class: ",12)) {
        unsigned agaciro=사용량-12;if(*진입점있음||!agaciro||agaciro>=sizeof(icyinjizwa_icyiciro))return -8;
        for(unsigned 순번=0;순번<agaciro;순번++){unsigned char 문자값=umurongo[12+순번];if(문자값<=32||문자값=='/'||문자값=='\\')return -8;icyinjizwa_icyiciro[순번]=문자값;}
        icyinjizwa_icyiciro[agaciro]=0;*진입점있음=1;
    }
    return 0;
}
static int ugize_itsinda(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned uburyo_icyinjizwa=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), kurekura_ingano=네바이트읽기(현재위치+24), mu_gace=네바이트읽기(현재위치+42);
    unsigned Izina=두바이트읽기(현재위치+28);
    if(kurekura_ingano>용량한도 || kurekura_ingano>16384 || (uburyo_icyinjizwa!=0 && uburyo_icyinjizwa!=8) || (설정비트&~0x80e))return -8;
    if(!kiripu(mu_gace,30,중앙목록) || 네바이트읽기(mu_gace)!=0x04034b50 || 두바이트읽기(mu_gace+8)!=uburyo_icyinjizwa || 두바이트읽기(mu_gace+6)!=설정비트 || 두바이트읽기(mu_gace+26)!=Izina)return -8;
    unsigned Itangira_Ofuseti=mu_gace+30, 추가영역=두바이트읽기(mu_gace+28);
    if(!kiripu(Itangira_Ofuseti,Izina,중앙목록) || !같음(gushyingura+Itangira_Ofuseti,gushyingura+현재위치+46,Izina))return -8;
    Itangira_Ofuseti+=Izina;if(!kiripu(Itangira_Ofuseti,추가영역,중앙목록))return -8;Itangira_Ofuseti+=추가영역;
    if(!kiripu(Itangira_Ofuseti,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(mu_gace+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(mu_gace+18)!=압축크기 || 네바이트읽기(mu_gace+22)!=kurekura_ingano))return -8;
    if(uburyo_icyinjizwa==0) { if(압축크기!=kurekura_ingano)return -8; for(unsigned 순번=0;순번<kurekura_ingano;순번++)결과자료[순번]=gushyingura[Itangira_Ofuseti+순번]; }
    else {
        uzlib_uncomp_t aho_ijya_amakurushingiro={0};uzlib_uncompress_init(&aho_ijya_amakurushingiro,0,0);
        aho_ijya_amakurushingiro.source=gushyingura+Itangira_Ofuseti;aho_ijya_amakurushingiro.source_limit=aho_ijya_amakurushingiro.source+압축크기;aho_ijya_amakurushingiro.source_read_cb=dosiye_kurangiza;
        /* One extra output byte lets inflate consume/check the end marker. */
        aho_ijya_amakurushingiro.dest_start=aho_ijya_amakurushingiro.dest=풀린자료;aho_ijya_amakurushingiro.dest_limit=풀린자료+kurekura_ingano+1;
        int 반환값=uzlib_uncompress(&aho_ijya_amakurushingiro);
        if(반환값!=UZLIB_DONE || aho_ijya_amakurushingiro.eof || aho_ijya_amakurushingiro.dest!=풀린자료+kurekura_ingano || aho_ijya_amakurushingiro.source!=aho_ijya_amakurushingiro.source_limit)return -8;
        for(unsigned 순번=0;순번<kurekura_ingano;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,kurekura_ingano,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return kurekura_ingano;
}
int 꾸러미읽기(const char *Izina, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=uburebure_agaciro(Izina),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(gushyingura+현재위치+46,(const unsigned char*)Izina,개수))return ugize_itsinda(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return icyinjizwa_icyiciro; }
int 꾸러미열기(const char *dosiye_icyinjizwa_izina) {
    항목들=0;icyinjizwa_icyiciro[0]=0;
    intptr_t dosiye_umukondo=사용자호출(3,(uintptr_t)dosiye_icyinjizwa_izina,0,0,0,0,0);if(dosiye_umukondo<0)return dosiye_umukondo;
    intptr_t 개수=사용자호출(9,dosiye_umukondo,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(gushyingura)) { 사용자호출(4,dosiye_umukondo,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,dosiye_umukondo,(uintptr_t)gushyingura,개수,0,0,0);사용자호출(4,dosiye_umukondo,0,0,0,0,0);
    if(받은수!=개수)return -5;Ingano=개수;
    unsigned kurangiza_Ofuseti=Ingano-22;
    for(;;) { if(네바이트읽기(kurangiza_Ofuseti)==0x06054b50 && kurangiza_Ofuseti+22+두바이트읽기(kurangiza_Ofuseti+20)==Ingano)break; if(!kurangiza_Ofuseti)return -8;kurangiza_Ofuseti--; }
    unsigned 항목수=두바이트읽기(kurangiza_Ofuseti+10);중앙목록=네바이트읽기(kurangiza_Ofuseti+16);
    if(두바이트읽기(kurangiza_Ofuseti+4)||두바이트읽기(kurangiza_Ofuseti+6)||두바이트읽기(kurangiza_Ofuseti+8)!=항목수||!항목수||항목수>256||!kiripu(중앙목록,네바이트읽기(kurangiza_Ofuseti+12),kurangiza_Ofuseti)||중앙목록+네바이트읽기(kurangiza_Ofuseti+12)!=kurangiza_Ofuseti)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!kiripu(현재위치,46,kurangiza_Ofuseti)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!kiripu(현재위치,다음,kurangiza_Ofuseti)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!gushyingura[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned uburebure_amakurushingiro=두바이트읽기(다른항목+28);if(uburebure_amakurushingiro==이름길이&&같음(gushyingura+다른항목+46,gushyingura+현재위치+46,uburebure_amakurushingiro))return -8;다른항목+=46+uburebure_amakurushingiro+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=kurangiza_Ofuseti)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int itsinda_ingano=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(itsinda_ingano<0){항목들=0;return -8;}
    꾸러미명세[itsinda_ingano]=0;
    char 논리크기[512];unsigned 사용량=0,umugerekashakiro_agaciro=0;int 진입점있음=0;
    while(umugerekashakiro_agaciro<(unsigned)itsinda_ingano) {
        unsigned ihuriro=umugerekashakiro_agaciro;while(umugerekashakiro_agaciro<(unsigned)itsinda_ingano && 꾸러미명세[umugerekashakiro_agaciro]!='\n')umugerekashakiro_agaciro++;
        unsigned uburebure_amakurushingiro=umugerekashakiro_agaciro-ihuriro;if(umugerekashakiro_agaciro<(unsigned)itsinda_ingano)umugerekashakiro_agaciro++;if(uburebure_amakurushingiro && 꾸러미명세[ihuriro+uburebure_amakurushingiro-1]=='\r')uburebure_amakurushingiro--;
        if(사용량 && uburebure_amakurushingiro && 꾸러미명세[ihuriro]==' ') {ihuriro++;uburebure_amakurushingiro--;}
        else {
            int 결과=ikiranga_amakurushingiro(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!uburebure_amakurushingiro)break;
        }
        if(uburebure_amakurushingiro>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<uburebure_amakurushingiro;순번++)논리크기[사용량++]=꾸러미명세[ihuriro+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=ikiranga_amakurushingiro(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
