#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "dami.h"
#include "uzlib.h"
static unsigned char Rumbun_ajiya[16384], 풀린자료[16385];
static unsigned Girma, 중앙목록, 항목들;
static char Mashigar_bayanai_Aji[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Rumbun_ajiya[현재위치] | Rumbun_ajiya[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int darfi(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t Tsawo_Daraja(const char *Zare_Tarin_bayani) { size_t 개수=0; while(Zare_Tarin_bayani[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int Fayil_Ƙarshe(void *미사용값) { (void)미사용값; return -1; }
static int siffofi_Tarin_bayani(const char *Layi,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Layi,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Layi,(const unsigned char*)"Main-Class: ",12)) {
        unsigned Daraja=사용량-12;if(*진입점있음||!Daraja||Daraja>=sizeof(Mashigar_bayanai_Aji))return -8;
        for(unsigned 순번=0;순번<Daraja;순번++){unsigned char Lambar_sirrin_harafi=Layi[12+순번];if(Lambar_sirrin_harafi<=32||Lambar_sirrin_harafi=='/'||Lambar_sirrin_harafi=='\\')return -8;Mashigar_bayanai_Aji[순번]=Lambar_sirrin_harafi;}
        Mashigar_bayanai_Aji[Daraja]=0;*진입점있음=1;
    }
    return 0;
}
static int Memba(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned tsari_Mashigar_bayanai=두바이트읽기(현재위치+10), saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), saka_girma=네바이트읽기(현재위치+24), na_gida=네바이트읽기(현재위치+42);
    unsigned Suna=두바이트읽기(현재위치+28);
    if(saka_girma>용량한도 || saka_girma>16384 || (tsari_Mashigar_bayanai!=0 && tsari_Mashigar_bayanai!=8) || (saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&~0x80e))return -8;
    if(!darfi(na_gida,30,중앙목록) || 네바이트읽기(na_gida)!=0x04034b50 || 두바이트읽기(na_gida+8)!=tsari_Mashigar_bayanai || 두바이트읽기(na_gida+6)!=saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango || 두바이트읽기(na_gida+26)!=Suna)return -8;
    unsigned Fara_Sassautawa=na_gida+30, 추가영역=두바이트읽기(na_gida+28);
    if(!darfi(Fara_Sassautawa,Suna,중앙목록) || !같음(Rumbun_ajiya+Fara_Sassautawa,Rumbun_ajiya+현재위치+46,Suna))return -8;
    Fara_Sassautawa+=Suna;if(!darfi(Fara_Sassautawa,추가영역,중앙목록))return -8;Fara_Sassautawa+=추가영역;
    if(!darfi(Fara_Sassautawa,압축크기,중앙목록))return -8;
    if(!(saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&8) && (네바이트읽기(na_gida+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(na_gida+18)!=압축크기 || 네바이트읽기(na_gida+22)!=saka_girma))return -8;
    if(tsari_Mashigar_bayanai==0) { if(압축크기!=saka_girma)return -8; for(unsigned 순번=0;순번<saka_girma;순번++)결과자료[순번]=Rumbun_ajiya[Fara_Sassautawa+순번]; }
    else {
        uzlib_uncomp_t Zangon_ƙarshe_Tarin_bayani={0};uzlib_uncompress_init(&Zangon_ƙarshe_Tarin_bayani,0,0);
        Zangon_ƙarshe_Tarin_bayani.source=Rumbun_ajiya+Fara_Sassautawa;Zangon_ƙarshe_Tarin_bayani.source_limit=Zangon_ƙarshe_Tarin_bayani.source+압축크기;Zangon_ƙarshe_Tarin_bayani.source_read_cb=Fayil_Ƙarshe;
        /* One extra output byte lets inflate consume/check the end marker. */
        Zangon_ƙarshe_Tarin_bayani.dest_start=Zangon_ƙarshe_Tarin_bayani.dest=풀린자료;Zangon_ƙarshe_Tarin_bayani.dest_limit=풀린자료+saka_girma+1;
        int 반환값=uzlib_uncompress(&Zangon_ƙarshe_Tarin_bayani);
        if(반환값!=UZLIB_DONE || Zangon_ƙarshe_Tarin_bayani.eof || Zangon_ƙarshe_Tarin_bayani.dest!=풀린자료+saka_girma || Zangon_ƙarshe_Tarin_bayani.source!=Zangon_ƙarshe_Tarin_bayani.source_limit)return -8;
        for(unsigned 순번=0;순번<saka_girma;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,saka_girma,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return saka_girma;
}
int 꾸러미읽기(const char *Suna, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=Tsawo_Daraja(Suna),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(Rumbun_ajiya+현재위치+46,(const unsigned char*)Suna,개수))return Memba(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return Mashigar_bayanai_Aji; }
int 꾸러미열기(const char *Fayil_Mashigar_bayanai_Suna) {
    항목들=0;Mashigar_bayanai_Aji[0]=0;
    intptr_t Fayil_Mariki=사용자호출(3,(uintptr_t)Fayil_Mashigar_bayanai_Suna,0,0,0,0,0);if(Fayil_Mariki<0)return Fayil_Mariki;
    intptr_t 개수=사용자호출(9,Fayil_Mariki,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(Rumbun_ajiya)) { 사용자호출(4,Fayil_Mariki,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,Fayil_Mariki,(uintptr_t)Rumbun_ajiya,개수,0,0,0);사용자호출(4,Fayil_Mariki,0,0,0,0,0);
    if(받은수!=개수)return -5;Girma=개수;
    unsigned Ƙarshe_Sassautawa=Girma-22;
    for(;;) { if(네바이트읽기(Ƙarshe_Sassautawa)==0x06054b50 && Ƙarshe_Sassautawa+22+두바이트읽기(Ƙarshe_Sassautawa+20)==Girma)break; if(!Ƙarshe_Sassautawa)return -8;Ƙarshe_Sassautawa--; }
    unsigned 항목수=두바이트읽기(Ƙarshe_Sassautawa+10);중앙목록=네바이트읽기(Ƙarshe_Sassautawa+16);
    if(두바이트읽기(Ƙarshe_Sassautawa+4)||두바이트읽기(Ƙarshe_Sassautawa+6)||두바이트읽기(Ƙarshe_Sassautawa+8)!=항목수||!항목수||항목수>256||!darfi(중앙목록,네바이트읽기(Ƙarshe_Sassautawa+12),Ƙarshe_Sassautawa)||중앙목록+네바이트읽기(Ƙarshe_Sassautawa+12)!=Ƙarshe_Sassautawa)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!darfi(현재위치,46,Ƙarshe_Sassautawa)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!darfi(현재위치,다음,Ƙarshe_Sassautawa)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Rumbun_ajiya[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned Tsawo_Tarin_bayani=두바이트읽기(다른항목+28);if(Tsawo_Tarin_bayani==이름길이&&같음(Rumbun_ajiya+다른항목+46,Rumbun_ajiya+현재위치+46,Tsawo_Tarin_bayani))return -8;다른항목+=46+Tsawo_Tarin_bayani+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=Ƙarshe_Sassautawa)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int gungu_girma=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(gungu_girma<0){항목들=0;return -8;}
    꾸러미명세[gungu_girma]=0;
    char 논리크기[512];unsigned 사용량=0,Indes_Daraja=0;int 진입점있음=0;
    while(Indes_Daraja<(unsigned)gungu_girma) {
        unsigned Tafiyar_da=Indes_Daraja;while(Indes_Daraja<(unsigned)gungu_girma && 꾸러미명세[Indes_Daraja]!='\n')Indes_Daraja++;
        unsigned Tsawo_Tarin_bayani=Indes_Daraja-Tafiyar_da;if(Indes_Daraja<(unsigned)gungu_girma)Indes_Daraja++;if(Tsawo_Tarin_bayani && 꾸러미명세[Tafiyar_da+Tsawo_Tarin_bayani-1]=='\r')Tsawo_Tarin_bayani--;
        if(사용량 && Tsawo_Tarin_bayani && 꾸러미명세[Tafiyar_da]==' ') {Tafiyar_da++;Tsawo_Tarin_bayani--;}
        else {
            int 결과=siffofi_Tarin_bayani(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!Tsawo_Tarin_bayani)break;
        }
        if(Tsawo_Tarin_bayani>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<Tsawo_Tarin_bayani;순번++)논리크기[사용량++]=꾸러미명세[Tafiyar_da+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=siffofi_Tarin_bayani(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
