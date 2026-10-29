#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "multzo.h"
#include "uzlib.h"
static unsigned char artxibo[16384], 풀린자료[16385];
static unsigned Tamaina, 중앙목록, 항목들;
static char sarrera_Gela[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return artxibo[현재위치] | artxibo[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int klip(unsigned 현재위치, unsigned elementu_ZENBATU, unsigned 한도) { return 현재위치 <= 한도 && elementu_ZENBATU <= 한도-현재위치; }
static size_t luzera_balio(const char *kate_datuak) { size_t elementu_ZENBATU=0; while(kate_datuak[elementu_ZENBATU]) elementu_ZENBATU++; return elementu_ZENBATU; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEGUNDOA_balio, unsigned elementu_ZENBATU) { for(unsigned 순번=0;순번<elementu_ZENBATU;순번++)if(첫째값[순번]!=SEGUNDOA_balio[순번])return 0;return 1; }
static int fitxategi_amaitu(void *미사용값) { (void)미사용값; return -1; }
static int atributu_datuak(const char *Marra,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Marra,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Marra,(const unsigned char*)"Main-Class: ",12)) {
        unsigned balio=사용량-12;if(*진입점있음||!balio||balio>=sizeof(sarrera_Gela))return -8;
        for(unsigned 순번=0;순번<balio;순번++){unsigned char karaktere_kode=Marra[12+순번];if(karaktere_kode<=32||karaktere_kode=='/'||karaktere_kode=='\\')return -8;sarrera_Gela[순번]=karaktere_kode;}
        sarrera_Gela[balio]=0;*진입점있음=1;
    }
    return 0;
}
static int kide(unsigned 현재위치, unsigned char *neurria_datuak, unsigned 용량한도) {
    unsigned 메소드=두바이트읽기(현재위치+10), konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), 해제크기=네바이트읽기(현재위치+24), lokal=네바이트읽기(현재위치+42);
    unsigned Izena=두바이트읽기(현재위치+28);
    if(해제크기>용량한도 || 해제크기>16384 || (메소드!=0 && 메소드!=8) || (konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&~0x80e))return -8;
    if(!klip(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=메소드 || 두바이트읽기(lokal+6)!=konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna || 두바이트읽기(lokal+26)!=Izena)return -8;
    unsigned HASI_Geruzak=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klip(HASI_Geruzak,Izena,중앙목록) || !같음(artxibo+HASI_Geruzak,artxibo+현재위치+46,Izena))return -8;
    HASI_Geruzak+=Izena;if(!klip(HASI_Geruzak,추가영역,중앙목록))return -8;HASI_Geruzak+=추가영역;
    if(!klip(HASI_Geruzak,압축크기,중앙목록))return -8;
    if(!(konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&8) && (네바이트읽기(lokal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=해제크기))return -8;
    if(메소드==0) { if(압축크기!=해제크기)return -8; for(unsigned 순번=0;순번<해제크기;순번++)neurria_datuak[순번]=artxibo[HASI_Geruzak+순번]; }
    else {
        uzlib_uncomp_t helburu_datuak={0};uzlib_uncompress_init(&helburu_datuak,0,0);
        helburu_datuak.source=artxibo+HASI_Geruzak;helburu_datuak.source_limit=helburu_datuak.source+압축크기;helburu_datuak.source_read_cb=fitxategi_amaitu;
        /* One extra output byte lets inflate consume/check the end marker. */
        helburu_datuak.dest_start=helburu_datuak.dest=풀린자료;helburu_datuak.dest_limit=풀린자료+해제크기+1;
        int 반환값=uzlib_uncompress(&helburu_datuak);
        if(반환값!=UZLIB_DONE || helburu_datuak.eof || helburu_datuak.dest!=풀린자료+해제크기 || helburu_datuak.source!=helburu_datuak.source_limit)return -8;
        for(unsigned 순번=0;순번<해제크기;순번++)neurria_datuak[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(neurria_datuak,해제크기,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return 해제크기;
}
int 꾸러미읽기(const char *Izena, unsigned char *neurria_datuak, unsigned buffer_ahalmen) {
    if(!항목들)return -2;unsigned elementu_ZENBATU=luzera_balio(Izena),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==elementu_ZENBATU && 같음(artxibo+현재위치+46,(const unsigned char*)Izena,elementu_ZENBATU))return kide(현재위치,neurria_datuak,buffer_ahalmen);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return sarrera_Gela; }
int 꾸러미열기(const char *fitxategi_sarrera_izen) {
    항목들=0;sarrera_Gela[0]=0;
    intptr_t fitxategi_helduleku=사용자호출(3,(uintptr_t)fitxategi_sarrera_izen,0,0,0,0,0);if(fitxategi_helduleku<0)return fitxategi_helduleku;
    intptr_t elementu_ZENBATU=사용자호출(9,fitxategi_helduleku,0,0,0,0,0);
    if(elementu_ZENBATU<22 || elementu_ZENBATU>(intptr_t)sizeof(artxibo)) { 사용자호출(4,fitxategi_helduleku,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_ZENBATU=사용자호출(2,fitxategi_helduleku,(uintptr_t)artxibo,elementu_ZENBATU,0,0,0);사용자호출(4,fitxategi_helduleku,0,0,0,0,0);
    if(RECEIVED_ZENBATU!=elementu_ZENBATU)return -5;Tamaina=elementu_ZENBATU;
    unsigned amaitu_Geruzak=Tamaina-22;
    for(;;) { if(네바이트읽기(amaitu_Geruzak)==0x06054b50 && amaitu_Geruzak+22+두바이트읽기(amaitu_Geruzak+20)==Tamaina)break; if(!amaitu_Geruzak)return -8;amaitu_Geruzak--; }
    unsigned sarrera_ZENBATU=두바이트읽기(amaitu_Geruzak+10);중앙목록=네바이트읽기(amaitu_Geruzak+16);
    if(두바이트읽기(amaitu_Geruzak+4)||두바이트읽기(amaitu_Geruzak+6)||두바이트읽기(amaitu_Geruzak+8)!=sarrera_ZENBATU||!sarrera_ZENBATU||sarrera_ZENBATU>256||!klip(중앙목록,네바이트읽기(amaitu_Geruzak+12),amaitu_Geruzak)||중앙목록+네바이트읽기(amaitu_Geruzak+12)!=amaitu_Geruzak)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<sarrera_ZENBATU;순번++) {
        if(!klip(현재위치,46,amaitu_Geruzak)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Hurrengoa_elementu=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!klip(현재위치,Hurrengoa_elementu,amaitu_Geruzak)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!artxibo[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned luzera_datuak=두바이트읽기(다른항목+28);if(luzera_datuak==이름길이&&같음(artxibo+다른항목+46,artxibo+현재위치+46,luzera_datuak))return -8;다른항목+=46+luzera_datuak+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Hurrengoa_elementu;
    }
    if(현재위치!=amaitu_Geruzak)return -8;항목들=sarrera_ZENBATU;
    unsigned char 꾸러미명세[4096];int 묶음수=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(묶음수<0){항목들=0;return -8;}
    꾸러미명세[묶음수]=0;
    char 논리크기[512];unsigned 사용량=0,INDIZE_balio=0;int 진입점있음=0;
    while(INDIZE_balio<(unsigned)묶음수) {
        unsigned Exekutatu_2=INDIZE_balio;while(INDIZE_balio<(unsigned)묶음수 && 꾸러미명세[INDIZE_balio]!='\n')INDIZE_balio++;
        unsigned luzera_datuak=INDIZE_balio-Exekutatu_2;if(INDIZE_balio<(unsigned)묶음수)INDIZE_balio++;if(luzera_datuak && 꾸러미명세[Exekutatu_2+luzera_datuak-1]=='\r')luzera_datuak--;
        if(사용량 && luzera_datuak && 꾸러미명세[Exekutatu_2]==' ') {Exekutatu_2++;luzera_datuak--;}
        else {
            int EMAITZA=atributu_datuak(논리크기,사용량,&진입점있음);if(EMAITZA)return EMAITZA;
            사용량=0;if(!luzera_datuak)break;
        }
        if(luzera_datuak>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<luzera_datuak;순번++)논리크기[사용량++]=꾸러미명세[Exekutatu_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int EMAITZA=atributu_datuak(논리크기,사용량,&진입점있음);if(EMAITZA)return EMAITZA;
    return 진입점있음?0:-8;
}
