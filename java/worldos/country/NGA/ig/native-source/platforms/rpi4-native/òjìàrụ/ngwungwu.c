#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "ngwungwu.h"
#include "uzlib.h"
static unsigned char ọkpụ[16384], 풀린자료[16385];
static unsigned Ụhara, 중앙목록, 항목들;
static char ndebà_klaàsị[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return ọkpụ[현재위치] | ọkpụ[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int ntipanye(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t ogologo_valuu(const char *ùsòròokwū_datà) { size_t 개수=0; while(ùsòròokwū_datà[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int ọbọakwụkwọ_mèdebe(void *미사용값) { (void)미사용값; return -1; }
static int njìama_datà(const char *ahịrī,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)ahịrī,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)ahịrī,(const unsigned char*)"Main-Class: ",12)) {
        unsigned valuu=사용량-12;if(*진입점있음||!valuu||valuu>=sizeof(ndebà_klaàsị))return -8;
        for(unsigned 순번=0;순번<valuu;순번++){unsigned char koòdù_nkeakàrà=ahịrī[12+순번];if(koòdù_nkeakàrà<=32||koòdù_nkeakàrà=='/'||koòdù_nkeakàrà=='\\')return -8;ndebà_klaàsị[순번]=koòdù_nkeakàrà;}
        ndebà_klaàsị[valuu]=0;*진입점있음=1;
    }
    return 0;
}
static int onyeòtù(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned usoro_ndebà=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), bupute_ụha=네바이트읽기(현재위치+24), otù_ebe=네바이트읽기(현재위치+42);
    unsigned Aha=두바이트읽기(현재위치+28);
    if(bupute_ụha>용량한도 || bupute_ụha>16384 || (usoro_ndebà!=0 && usoro_ndebà!=8) || (설정비트&~0x80e))return -8;
    if(!ntipanye(otù_ebe,30,중앙목록) || 네바이트읽기(otù_ebe)!=0x04034b50 || 두바이트읽기(otù_ebe+8)!=usoro_ndebà || 두바이트읽기(otù_ebe+6)!=설정비트 || 두바이트읽기(otù_ebe+26)!=Aha)return -8;
    unsigned Mbido_Nnokwata=otù_ebe+30, 추가영역=두바이트읽기(otù_ebe+28);
    if(!ntipanye(Mbido_Nnokwata,Aha,중앙목록) || !같음(ọkpụ+Mbido_Nnokwata,ọkpụ+현재위치+46,Aha))return -8;
    Mbido_Nnokwata+=Aha;if(!ntipanye(Mbido_Nnokwata,추가영역,중앙목록))return -8;Mbido_Nnokwata+=추가영역;
    if(!ntipanye(Mbido_Nnokwata,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(otù_ebe+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(otù_ebe+18)!=압축크기 || 네바이트읽기(otù_ebe+22)!=bupute_ụha))return -8;
    if(usoro_ndebà==0) { if(압축크기!=bupute_ụha)return -8; for(unsigned 순번=0;순번<bupute_ụha;순번++)결과자료[순번]=ọkpụ[Mbido_Nnokwata+순번]; }
    else {
        uzlib_uncomp_t ebemwèga_datà={0};uzlib_uncompress_init(&ebemwèga_datà,0,0);
        ebemwèga_datà.source=ọkpụ+Mbido_Nnokwata;ebemwèga_datà.source_limit=ebemwèga_datà.source+압축크기;ebemwèga_datà.source_read_cb=ọbọakwụkwọ_mèdebe;
        /* One extra output byte lets inflate consume/check the end marker. */
        ebemwèga_datà.dest_start=ebemwèga_datà.dest=풀린자료;ebemwèga_datà.dest_limit=풀린자료+bupute_ụha+1;
        int 반환값=uzlib_uncompress(&ebemwèga_datà);
        if(반환값!=UZLIB_DONE || ebemwèga_datà.eof || ebemwèga_datà.dest!=풀린자료+bupute_ụha || ebemwèga_datà.source!=ebemwèga_datà.source_limit)return -8;
        for(unsigned 순번=0;순번<bupute_ụha;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,bupute_ụha,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return bupute_ụha;
}
int 꾸러미읽기(const char *Aha, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=ogologo_valuu(Aha),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(ọkpụ+현재위치+46,(const unsigned char*)Aha,개수))return onyeòtù(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ndebà_klaàsị; }
int 꾸러미열기(const char *ọbọakwụkwọ_ndebà_akara_ahà) {
    항목들=0;ndebà_klaàsị[0]=0;
    intptr_t ọbọakwụkwọ_ebenjìaka=사용자호출(3,(uintptr_t)ọbọakwụkwọ_ndebà_akara_ahà,0,0,0,0,0);if(ọbọakwụkwọ_ebenjìaka<0)return ọbọakwụkwọ_ebenjìaka;
    intptr_t 개수=사용자호출(9,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(ọkpụ)) { 사용자호출(4,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,ọbọakwụkwọ_ebenjìaka,(uintptr_t)ọkpụ,개수,0,0,0);사용자호출(4,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);
    if(받은수!=개수)return -5;Ụhara=개수;
    unsigned mèdebe_Nnokwata=Ụhara-22;
    for(;;) { if(네바이트읽기(mèdebe_Nnokwata)==0x06054b50 && mèdebe_Nnokwata+22+두바이트읽기(mèdebe_Nnokwata+20)==Ụhara)break; if(!mèdebe_Nnokwata)return -8;mèdebe_Nnokwata--; }
    unsigned 항목수=두바이트읽기(mèdebe_Nnokwata+10);중앙목록=네바이트읽기(mèdebe_Nnokwata+16);
    if(두바이트읽기(mèdebe_Nnokwata+4)||두바이트읽기(mèdebe_Nnokwata+6)||두바이트읽기(mèdebe_Nnokwata+8)!=항목수||!항목수||항목수>256||!ntipanye(중앙목록,네바이트읽기(mèdebe_Nnokwata+12),mèdebe_Nnokwata)||중앙목록+네바이트읽기(mèdebe_Nnokwata+12)!=mèdebe_Nnokwata)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!ntipanye(현재위치,46,mèdebe_Nnokwata)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!ntipanye(현재위치,다음,mèdebe_Nnokwata)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!ọkpụ[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned ogologo_datà=두바이트읽기(다른항목+28);if(ogologo_datà==이름길이&&같음(ọkpụ+다른항목+46,ọkpụ+현재위치+46,ogologo_datà))return -8;다른항목+=46+ogologo_datà+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=mèdebe_Nnokwata)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int otu_ụha=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(otu_ụha<0){항목들=0;return -8;}
    꾸러미명세[otu_ụha]=0;
    char 논리크기[512];unsigned 사용량=0,indèks_valuu=0;int 진입점있음=0;
    while(indèks_valuu<(unsigned)otu_ụha) {
        unsigned Bido=indèks_valuu;while(indèks_valuu<(unsigned)otu_ụha && 꾸러미명세[indèks_valuu]!='\n')indèks_valuu++;
        unsigned ogologo_datà=indèks_valuu-Bido;if(indèks_valuu<(unsigned)otu_ụha)indèks_valuu++;if(ogologo_datà && 꾸러미명세[Bido+ogologo_datà-1]=='\r')ogologo_datà--;
        if(사용량 && ogologo_datà && 꾸러미명세[Bido]==' ') {Bido++;ogologo_datà--;}
        else {
            int 결과=njìama_datà(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!ogologo_datà)break;
        }
        if(ogologo_datà>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<ogologo_datà;순번++)논리크기[사용량++]=꾸러미명세[Bido+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=njìama_datà(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
