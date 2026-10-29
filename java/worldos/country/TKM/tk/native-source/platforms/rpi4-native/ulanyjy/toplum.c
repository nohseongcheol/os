#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "toplum.h"
#include "uzlib.h"
static unsigned char Arhiw[16384], 풀린자료[16385];
static unsigned Ululyk, 중앙목록, 항목들;
static char girizmeklik_klas[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Arhiw[현재위치] | Arhiw[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int klip(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t dowamlylyk_baha(const char *setir_maglumat) { size_t 개수=0; while(setir_maglumat[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int faýl_tamamla(void *미사용값) { (void)미사용값; return -1; }
static int alamat_maglumat(const char *setir,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)setir,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)setir,(const unsigned char*)"Main-Class: ",12)) {
        unsigned baha=사용량-12;if(*진입점있음||!baha||baha>=sizeof(girizmeklik_klas))return -8;
        for(unsigned 순번=0;순번<baha;순번++){unsigned char nyşanyň_kody=setir[12+순번];if(nyşanyň_kody<=32||nyşanyň_kody=='/'||nyşanyň_kody=='\\')return -8;girizmeklik_klas[순번]=nyşanyň_kody;}
        girizmeklik_klas[baha]=0;*진입점있음=1;
    }
    return 0;
}
static int agza(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned usul_girizmeklik=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), goýbermek_ölçegi_üýtget=네바이트읽기(현재위치+24), ýerli=네바이트읽기(현재위치+42);
    unsigned Ad=두바이트읽기(현재위치+28);
    if(goýbermek_ölçegi_üýtget>용량한도 || goýbermek_ölçegi_üýtget>16384 || (usul_girizmeklik!=0 && usul_girizmeklik!=8) || (설정비트&~0x80e))return -8;
    if(!klip(ýerli,30,중앙목록) || 네바이트읽기(ýerli)!=0x04034b50 || 두바이트읽기(ýerli+8)!=usul_girizmeklik || 두바이트읽기(ýerli+6)!=설정비트 || 두바이트읽기(ýerli+26)!=Ad)return -8;
    unsigned başlat_Süýşüriş=ýerli+30, 추가영역=두바이트읽기(ýerli+28);
    if(!klip(başlat_Süýşüriş,Ad,중앙목록) || !같음(Arhiw+başlat_Süýşüriş,Arhiw+현재위치+46,Ad))return -8;
    başlat_Süýşüriş+=Ad;if(!klip(başlat_Süýşüriş,추가영역,중앙목록))return -8;başlat_Süýşüriş+=추가영역;
    if(!klip(başlat_Süýşüriş,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(ýerli+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(ýerli+18)!=압축크기 || 네바이트읽기(ýerli+22)!=goýbermek_ölçegi_üýtget))return -8;
    if(usul_girizmeklik==0) { if(압축크기!=goýbermek_ölçegi_üýtget)return -8; for(unsigned 순번=0;순번<goýbermek_ölçegi_üýtget;순번++)결과자료[순번]=Arhiw[başlat_Süýşüriş+순번]; }
    else {
        uzlib_uncomp_t barylmaly_ýer_maglumat={0};uzlib_uncompress_init(&barylmaly_ýer_maglumat,0,0);
        barylmaly_ýer_maglumat.source=Arhiw+başlat_Süýşüriş;barylmaly_ýer_maglumat.source_limit=barylmaly_ýer_maglumat.source+압축크기;barylmaly_ýer_maglumat.source_read_cb=faýl_tamamla;
        /* One extra output byte lets inflate consume/check the end marker. */
        barylmaly_ýer_maglumat.dest_start=barylmaly_ýer_maglumat.dest=풀린자료;barylmaly_ýer_maglumat.dest_limit=풀린자료+goýbermek_ölçegi_üýtget+1;
        int 반환값=uzlib_uncompress(&barylmaly_ýer_maglumat);
        if(반환값!=UZLIB_DONE || barylmaly_ýer_maglumat.eof || barylmaly_ýer_maglumat.dest!=풀린자료+goýbermek_ölçegi_üýtget || barylmaly_ýer_maglumat.source!=barylmaly_ýer_maglumat.source_limit)return -8;
        for(unsigned 순번=0;순번<goýbermek_ölçegi_üýtget;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,goýbermek_ölçegi_üýtget,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return goýbermek_ölçegi_üýtget;
}
int 꾸러미읽기(const char *Ad, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=dowamlylyk_baha(Ad),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(Arhiw+현재위치+46,(const unsigned char*)Ad,개수))return agza(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return girizmeklik_klas; }
int 꾸러미열기(const char *faýl_girizmeklik_at) {
    항목들=0;girizmeklik_klas[0]=0;
    intptr_t faýl_ryçag=사용자호출(3,(uintptr_t)faýl_girizmeklik_at,0,0,0,0,0);if(faýl_ryçag<0)return faýl_ryçag;
    intptr_t 개수=사용자호출(9,faýl_ryçag,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(Arhiw)) { 사용자호출(4,faýl_ryçag,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,faýl_ryçag,(uintptr_t)Arhiw,개수,0,0,0);사용자호출(4,faýl_ryçag,0,0,0,0,0);
    if(받은수!=개수)return -5;Ululyk=개수;
    unsigned tamamla_Süýşüriş=Ululyk-22;
    for(;;) { if(네바이트읽기(tamamla_Süýşüriş)==0x06054b50 && tamamla_Süýşüriş+22+두바이트읽기(tamamla_Süýşüriş+20)==Ululyk)break; if(!tamamla_Süýşüriş)return -8;tamamla_Süýşüriş--; }
    unsigned 항목수=두바이트읽기(tamamla_Süýşüriş+10);중앙목록=네바이트읽기(tamamla_Süýşüriş+16);
    if(두바이트읽기(tamamla_Süýşüriş+4)||두바이트읽기(tamamla_Süýşüriş+6)||두바이트읽기(tamamla_Süýşüriş+8)!=항목수||!항목수||항목수>256||!klip(중앙목록,네바이트읽기(tamamla_Süýşüriş+12),tamamla_Süýşüriş)||중앙목록+네바이트읽기(tamamla_Süýşüriş+12)!=tamamla_Süýşüriş)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!klip(현재위치,46,tamamla_Süýşüriş)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!klip(현재위치,다음,tamamla_Süýşüriş)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhiw[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned dowamlylyk_maglumat=두바이트읽기(다른항목+28);if(dowamlylyk_maglumat==이름길이&&같음(Arhiw+다른항목+46,Arhiw+현재위치+46,dowamlylyk_maglumat))return -8;다른항목+=46+dowamlylyk_maglumat+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=tamamla_Süýşüriş)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int topar_ölçegi_üýtget=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(topar_ölçegi_üýtget<0){항목들=0;return -8;}
    꾸러미명세[topar_ölçegi_üýtget]=0;
    char 논리크기[512];unsigned 사용량=0,indeks_baha=0;int 진입점있음=0;
    while(indeks_baha<(unsigned)topar_ölçegi_üýtget) {
        unsigned Bitir=indeks_baha;while(indeks_baha<(unsigned)topar_ölçegi_üýtget && 꾸러미명세[indeks_baha]!='\n')indeks_baha++;
        unsigned dowamlylyk_maglumat=indeks_baha-Bitir;if(indeks_baha<(unsigned)topar_ölçegi_üýtget)indeks_baha++;if(dowamlylyk_maglumat && 꾸러미명세[Bitir+dowamlylyk_maglumat-1]=='\r')dowamlylyk_maglumat--;
        if(사용량 && dowamlylyk_maglumat && 꾸러미명세[Bitir]==' ') {Bitir++;dowamlylyk_maglumat--;}
        else {
            int 결과=alamat_maglumat(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!dowamlylyk_maglumat)break;
        }
        if(dowamlylyk_maglumat>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<dowamlylyk_maglumat;순번++)논리크기[사용량++]=꾸러미명세[Bitir+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=alamat_maglumat(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
