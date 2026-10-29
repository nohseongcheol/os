#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "sehlopha.h"
#include "uzlib.h"
static unsigned char Akhaebe[16384], 풀린자료[16385];
static unsigned Bogolo, 중앙목록, 항목들;
static char go_tsenya_tshedimošo_legoro[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Akhaebe[현재위치] | Akhaebe[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int setsopolwa(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t botelele_boleng(const char *molokoloko_data) { size_t 개수=0; while(molokoloko_data[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int faele_fetša(void *미사용값) { (void)미사용값; return -1; }
static int tlhaodi_ya_faele_data(const char *mothaladi,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)mothaladi,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)mothaladi,(const unsigned char*)"Main-Class: ",12)) {
        unsigned boleng=사용량-12;if(*진입점있음||!boleng||boleng>=sizeof(go_tsenya_tshedimošo_legoro))return -8;
        for(unsigned 순번=0;순번<boleng;순번++){unsigned char khouto_ya_tlhaka=mothaladi[12+순번];if(khouto_ya_tlhaka<=32||khouto_ya_tlhaka=='/'||khouto_ya_tlhaka=='\\')return -8;go_tsenya_tshedimošo_legoro[순번]=khouto_ya_tlhaka;}
        go_tsenya_tshedimošo_legoro[boleng]=0;*진입점있음=1;
    }
    return 0;
}
static int setho(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned mokgwa_go_tsenya_tshedimošo=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), lokolla_bogolo=네바이트읽기(현재위치+24), kgauswi=네바이트읽기(현재위치+42);
    unsigned Leina=두바이트읽기(현재위치+28);
    if(lokolla_bogolo>용량한도 || lokolla_bogolo>16384 || (mokgwa_go_tsenya_tshedimošo!=0 && mokgwa_go_tsenya_tshedimošo!=8) || (설정비트&~0x80e))return -8;
    if(!setsopolwa(kgauswi,30,중앙목록) || 네바이트읽기(kgauswi)!=0x04034b50 || 두바이트읽기(kgauswi+8)!=mokgwa_go_tsenya_tshedimošo || 두바이트읽기(kgauswi+6)!=설정비트 || 두바이트읽기(kgauswi+26)!=Leina)return -8;
    unsigned Thomišo_E_Šetšego=kgauswi+30, 추가영역=두바이트읽기(kgauswi+28);
    if(!setsopolwa(Thomišo_E_Šetšego,Leina,중앙목록) || !같음(Akhaebe+Thomišo_E_Šetšego,Akhaebe+현재위치+46,Leina))return -8;
    Thomišo_E_Šetšego+=Leina;if(!setsopolwa(Thomišo_E_Šetšego,추가영역,중앙목록))return -8;Thomišo_E_Šetšego+=추가영역;
    if(!setsopolwa(Thomišo_E_Šetšego,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(kgauswi+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(kgauswi+18)!=압축크기 || 네바이트읽기(kgauswi+22)!=lokolla_bogolo))return -8;
    if(mokgwa_go_tsenya_tshedimošo==0) { if(압축크기!=lokolla_bogolo)return -8; for(unsigned 순번=0;순번<lokolla_bogolo;순번++)결과자료[순번]=Akhaebe[Thomišo_E_Šetšego+순번]; }
    else {
        uzlib_uncomp_t boyo_data={0};uzlib_uncompress_init(&boyo_data,0,0);
        boyo_data.source=Akhaebe+Thomišo_E_Šetšego;boyo_data.source_limit=boyo_data.source+압축크기;boyo_data.source_read_cb=faele_fetša;
        /* One extra output byte lets inflate consume/check the end marker. */
        boyo_data.dest_start=boyo_data.dest=풀린자료;boyo_data.dest_limit=풀린자료+lokolla_bogolo+1;
        int 반환값=uzlib_uncompress(&boyo_data);
        if(반환값!=UZLIB_DONE || boyo_data.eof || boyo_data.dest!=풀린자료+lokolla_bogolo || boyo_data.source!=boyo_data.source_limit)return -8;
        for(unsigned 순번=0;순번<lokolla_bogolo;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,lokolla_bogolo,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return lokolla_bogolo;
}
int 꾸러미읽기(const char *Leina, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=botelele_boleng(Leina),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(Akhaebe+현재위치+46,(const unsigned char*)Leina,개수))return setho(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return go_tsenya_tshedimošo_legoro; }
int 꾸러미열기(const char *faele_go_tsenya_tshedimošo_leina) {
    항목들=0;go_tsenya_tshedimošo_legoro[0]=0;
    intptr_t faele_tshwaro=사용자호출(3,(uintptr_t)faele_go_tsenya_tshedimošo_leina,0,0,0,0,0);if(faele_tshwaro<0)return faele_tshwaro;
    intptr_t 개수=사용자호출(9,faele_tshwaro,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(Akhaebe)) { 사용자호출(4,faele_tshwaro,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,faele_tshwaro,(uintptr_t)Akhaebe,개수,0,0,0);사용자호출(4,faele_tshwaro,0,0,0,0,0);
    if(받은수!=개수)return -5;Bogolo=개수;
    unsigned fetša_E_Šetšego=Bogolo-22;
    for(;;) { if(네바이트읽기(fetša_E_Šetšego)==0x06054b50 && fetša_E_Šetšego+22+두바이트읽기(fetša_E_Šetšego+20)==Bogolo)break; if(!fetša_E_Šetšego)return -8;fetša_E_Šetšego--; }
    unsigned 항목수=두바이트읽기(fetša_E_Šetšego+10);중앙목록=네바이트읽기(fetša_E_Šetšego+16);
    if(두바이트읽기(fetša_E_Šetšego+4)||두바이트읽기(fetša_E_Šetšego+6)||두바이트읽기(fetša_E_Šetšego+8)!=항목수||!항목수||항목수>256||!setsopolwa(중앙목록,네바이트읽기(fetša_E_Šetšego+12),fetša_E_Šetšego)||중앙목록+네바이트읽기(fetša_E_Šetšego+12)!=fetša_E_Šetšego)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!setsopolwa(현재위치,46,fetša_E_Šetšego)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!setsopolwa(현재위치,다음,fetša_E_Šetšego)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Akhaebe[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned botelele_data=두바이트읽기(다른항목+28);if(botelele_data==이름길이&&같음(Akhaebe+다른항목+46,Akhaebe+현재위치+46,botelele_data))return -8;다른항목+=46+botelele_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=fetša_E_Šetšego)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int sehlopha_bogolo=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(sehlopha_bogolo<0){항목들=0;return -8;}
    꾸러미명세[sehlopha_bogolo]=0;
    char 논리크기[512];unsigned 사용량=0,lokela_boleng=0;int 진입점있음=0;
    while(lokela_boleng<(unsigned)sehlopha_bogolo) {
        unsigned Diriša=lokela_boleng;while(lokela_boleng<(unsigned)sehlopha_bogolo && 꾸러미명세[lokela_boleng]!='\n')lokela_boleng++;
        unsigned botelele_data=lokela_boleng-Diriša;if(lokela_boleng<(unsigned)sehlopha_bogolo)lokela_boleng++;if(botelele_data && 꾸러미명세[Diriša+botelele_data-1]=='\r')botelele_data--;
        if(사용량 && botelele_data && 꾸러미명세[Diriša]==' ') {Diriša++;botelele_data--;}
        else {
            int 결과=tlhaodi_ya_faele_data(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!botelele_data)break;
        }
        if(botelele_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<botelele_data;순번++)논리크기[사용량++]=꾸러미명세[Diriša+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=tlhaodi_ya_faele_data(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
