#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "ngatanngwe.h"
#include "uzlib.h"
static unsigned char boloka[16384], 풀린자료[16385];
static unsigned lekanya, 중앙목록, 항목들;
static char tsenyo_mofuta[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return boloka[현재위치] | boloka[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int faelekhutshwe_ya_media(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t boleele_Boleng(const char *dikwalwa_tshedimosetso) { size_t 개수=0; while(dikwalwa_tshedimosetso[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int faele_kgaola(void *미사용값) { (void)미사용값; return -1; }
static int nonofo_tshedimosetso(const char *Mola,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Mola,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Mola,(const unsigned char*)"Main-Class: ",12)) {
        unsigned Boleng=사용량-12;if(*진입점있음||!Boleng||Boleng>=sizeof(tsenyo_mofuta))return -8;
        for(unsigned 순번=0;순번<Boleng;순번++){unsigned char khoutuletshwao=Mola[12+순번];if(khoutuletshwao<=32||khoutuletshwao=='/'||khoutuletshwao=='\\')return -8;tsenyo_mofuta[순번]=khoutuletshwao;}
        tsenyo_mofuta[Boleng]=0;*진입점있음=1;
    }
    return 0;
}
static int karolo(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned mokgwa_tsenyo=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), ntsha_lekanya=네바이트읽기(현재위치+24), e_e_gaufi=네바이트읽기(현재위치+42);
    unsigned leina=두바이트읽기(현재위치+28);
    if(ntsha_lekanya>용량한도 || ntsha_lekanya>16384 || (mokgwa_tsenyo!=0 && mokgwa_tsenyo!=8) || (설정비트&~0x80e))return -8;
    if(!faelekhutshwe_ya_media(e_e_gaufi,30,중앙목록) || 네바이트읽기(e_e_gaufi)!=0x04034b50 || 두바이트읽기(e_e_gaufi+8)!=mokgwa_tsenyo || 두바이트읽기(e_e_gaufi+6)!=설정비트 || 두바이트읽기(e_e_gaufi+26)!=leina)return -8;
    unsigned simolola_Baya_ka_Tekatekanyo=e_e_gaufi+30, 추가영역=두바이트읽기(e_e_gaufi+28);
    if(!faelekhutshwe_ya_media(simolola_Baya_ka_Tekatekanyo,leina,중앙목록) || !같음(boloka+simolola_Baya_ka_Tekatekanyo,boloka+현재위치+46,leina))return -8;
    simolola_Baya_ka_Tekatekanyo+=leina;if(!faelekhutshwe_ya_media(simolola_Baya_ka_Tekatekanyo,추가영역,중앙목록))return -8;simolola_Baya_ka_Tekatekanyo+=추가영역;
    if(!faelekhutshwe_ya_media(simolola_Baya_ka_Tekatekanyo,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(e_e_gaufi+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(e_e_gaufi+18)!=압축크기 || 네바이트읽기(e_e_gaufi+22)!=ntsha_lekanya))return -8;
    if(mokgwa_tsenyo==0) { if(압축크기!=ntsha_lekanya)return -8; for(unsigned 순번=0;순번<ntsha_lekanya;순번++)결과자료[순번]=boloka[simolola_Baya_ka_Tekatekanyo+순번]; }
    else {
        uzlib_uncomp_t bogorogelo_tshedimosetso={0};uzlib_uncompress_init(&bogorogelo_tshedimosetso,0,0);
        bogorogelo_tshedimosetso.source=boloka+simolola_Baya_ka_Tekatekanyo;bogorogelo_tshedimosetso.source_limit=bogorogelo_tshedimosetso.source+압축크기;bogorogelo_tshedimosetso.source_read_cb=faele_kgaola;
        /* One extra output byte lets inflate consume/check the end marker. */
        bogorogelo_tshedimosetso.dest_start=bogorogelo_tshedimosetso.dest=풀린자료;bogorogelo_tshedimosetso.dest_limit=풀린자료+ntsha_lekanya+1;
        int 반환값=uzlib_uncompress(&bogorogelo_tshedimosetso);
        if(반환값!=UZLIB_DONE || bogorogelo_tshedimosetso.eof || bogorogelo_tshedimosetso.dest!=풀린자료+ntsha_lekanya || bogorogelo_tshedimosetso.source!=bogorogelo_tshedimosetso.source_limit)return -8;
        for(unsigned 순번=0;순번<ntsha_lekanya;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,ntsha_lekanya,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return ntsha_lekanya;
}
int 꾸러미읽기(const char *leina, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=boleele_Boleng(leina),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(boloka+현재위치+46,(const unsigned char*)leina,개수))return karolo(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return tsenyo_mofuta; }
int 꾸러미열기(const char *faele_tsenyo_leina) {
    항목들=0;tsenyo_mofuta[0]=0;
    intptr_t faele_mokgwakamogelo=사용자호출(3,(uintptr_t)faele_tsenyo_leina,0,0,0,0,0);if(faele_mokgwakamogelo<0)return faele_mokgwakamogelo;
    intptr_t 개수=사용자호출(9,faele_mokgwakamogelo,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(boloka)) { 사용자호출(4,faele_mokgwakamogelo,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,faele_mokgwakamogelo,(uintptr_t)boloka,개수,0,0,0);사용자호출(4,faele_mokgwakamogelo,0,0,0,0,0);
    if(받은수!=개수)return -5;lekanya=개수;
    unsigned kgaola_Baya_ka_Tekatekanyo=lekanya-22;
    for(;;) { if(네바이트읽기(kgaola_Baya_ka_Tekatekanyo)==0x06054b50 && kgaola_Baya_ka_Tekatekanyo+22+두바이트읽기(kgaola_Baya_ka_Tekatekanyo+20)==lekanya)break; if(!kgaola_Baya_ka_Tekatekanyo)return -8;kgaola_Baya_ka_Tekatekanyo--; }
    unsigned 항목수=두바이트읽기(kgaola_Baya_ka_Tekatekanyo+10);중앙목록=네바이트읽기(kgaola_Baya_ka_Tekatekanyo+16);
    if(두바이트읽기(kgaola_Baya_ka_Tekatekanyo+4)||두바이트읽기(kgaola_Baya_ka_Tekatekanyo+6)||두바이트읽기(kgaola_Baya_ka_Tekatekanyo+8)!=항목수||!항목수||항목수>256||!faelekhutshwe_ya_media(중앙목록,네바이트읽기(kgaola_Baya_ka_Tekatekanyo+12),kgaola_Baya_ka_Tekatekanyo)||중앙목록+네바이트읽기(kgaola_Baya_ka_Tekatekanyo+12)!=kgaola_Baya_ka_Tekatekanyo)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!faelekhutshwe_ya_media(현재위치,46,kgaola_Baya_ka_Tekatekanyo)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!faelekhutshwe_ya_media(현재위치,다음,kgaola_Baya_ka_Tekatekanyo)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!boloka[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned boleele_tshedimosetso=두바이트읽기(다른항목+28);if(boleele_tshedimosetso==이름길이&&같음(boloka+다른항목+46,boloka+현재위치+46,boleele_tshedimosetso))return -8;다른항목+=46+boleele_tshedimosetso+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=kgaola_Baya_ka_Tekatekanyo)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int setlhopha_lekanya=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(setlhopha_lekanya<0){항목들=0;return -8;}
    꾸러미명세[setlhopha_lekanya]=0;
    char 논리크기[512];unsigned 사용량=0,tshupane_Boleng=0;int 진입점있음=0;
    while(tshupane_Boleng<(unsigned)setlhopha_lekanya) {
        unsigned dirisa=tshupane_Boleng;while(tshupane_Boleng<(unsigned)setlhopha_lekanya && 꾸러미명세[tshupane_Boleng]!='\n')tshupane_Boleng++;
        unsigned boleele_tshedimosetso=tshupane_Boleng-dirisa;if(tshupane_Boleng<(unsigned)setlhopha_lekanya)tshupane_Boleng++;if(boleele_tshedimosetso && 꾸러미명세[dirisa+boleele_tshedimosetso-1]=='\r')boleele_tshedimosetso--;
        if(사용량 && boleele_tshedimosetso && 꾸러미명세[dirisa]==' ') {dirisa++;boleele_tshedimosetso--;}
        else {
            int 결과=nonofo_tshedimosetso(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!boleele_tshedimosetso)break;
        }
        if(boleele_tshedimosetso>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<boleele_tshedimosetso;순번++)논리크기[사용량++]=꾸러미명세[dirisa+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=nonofo_tshedimosetso(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
