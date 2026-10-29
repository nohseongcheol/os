#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paket.h"
#include "uzlib.h"
static unsigned char Arhiva[16384], 풀린자료[16385];
static unsigned Veličina, 중앙목록, 항목들;
static char unos_klasa[256];
static unsigned 두바이트읽기(unsigned trenutno_položaj) { return Arhiva[trenutno_položaj] | Arhiva[trenutno_položaj+1] << 8; }
static uint32_t 네바이트읽기(unsigned trenutno_položaj) { return 두바이트읽기(trenutno_položaj) | (uint32_t)두바이트읽기(trenutno_položaj+2) << 16; }
static int isječak(unsigned trenutno_položaj, unsigned stavka_COUNT, unsigned 한도) { return trenutno_položaj <= 한도 && stavka_COUNT <= 한도-trenutno_položaj; }
static size_t dužina_VALUE(const char *string_podaci) { size_t stavka_COUNT=0; while(string_podaci[stavka_COUNT]) stavka_COUNT++; return stavka_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned stavka_COUNT) { for(unsigned 순번=0;순번<stavka_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int fajl_završiti(void *미사용값) { (void)미사용값; return -1; }
static int atribut_podaci(const char *Linija,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Linija,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Linija,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(unos_klasa))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char kôd_znaka=Linija[12+순번];if(kôd_znaka<=32||kôd_znaka=='/'||kôd_znaka=='\\')return -8;unos_klasa[순번]=kôd_znaka;}
        unos_klasa[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int član(unsigned trenutno_položaj, unsigned char *mjera_podaci, unsigned 용량한도) {
    unsigned metoda_unos=두바이트읽기(trenutno_položaj+10), 설정비트=두바이트읽기(trenutno_položaj+8), 압축크기=네바이트읽기(trenutno_položaj+20), izdanje_podesiti_veličinu=네바이트읽기(trenutno_položaj+24), lokalni=네바이트읽기(trenutno_položaj+42);
    unsigned Naziv=두바이트읽기(trenutno_položaj+28);
    if(izdanje_podesiti_veličinu>용량한도 || izdanje_podesiti_veličinu>16384 || (metoda_unos!=0 && metoda_unos!=8) || (설정비트&~0x80e))return -8;
    if(!isječak(lokalni,30,중앙목록) || 네바이트읽기(lokalni)!=0x04034b50 || 두바이트읽기(lokalni+8)!=metoda_unos || 두바이트읽기(lokalni+6)!=설정비트 || 두바이트읽기(lokalni+26)!=Naziv)return -8;
    unsigned START_Pomak=lokalni+30, 추가영역=두바이트읽기(lokalni+28);
    if(!isječak(START_Pomak,Naziv,중앙목록) || !같음(Arhiva+START_Pomak,Arhiva+trenutno_položaj+46,Naziv))return -8;
    START_Pomak+=Naziv;if(!isječak(START_Pomak,추가영역,중앙목록))return -8;START_Pomak+=추가영역;
    if(!isječak(START_Pomak,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(lokalni+14)!=네바이트읽기(trenutno_položaj+16) || 네바이트읽기(lokalni+18)!=압축크기 || 네바이트읽기(lokalni+22)!=izdanje_podesiti_veličinu))return -8;
    if(metoda_unos==0) { if(압축크기!=izdanje_podesiti_veličinu)return -8; for(unsigned 순번=0;순번<izdanje_podesiti_veličinu;순번++)mjera_podaci[순번]=Arhiva[START_Pomak+순번]; }
    else {
        uzlib_uncomp_t odredište_podaci={0};uzlib_uncompress_init(&odredište_podaci,0,0);
        odredište_podaci.source=Arhiva+START_Pomak;odredište_podaci.source_limit=odredište_podaci.source+압축크기;odredište_podaci.source_read_cb=fajl_završiti;
        /* One extra output byte lets inflate consume/check the end marker. */
        odredište_podaci.dest_start=odredište_podaci.dest=풀린자료;odredište_podaci.dest_limit=풀린자료+izdanje_podesiti_veličinu+1;
        int 반환값=uzlib_uncompress(&odredište_podaci);
        if(반환값!=UZLIB_DONE || odredište_podaci.eof || odredište_podaci.dest!=풀린자료+izdanje_podesiti_veličinu || odredište_podaci.source!=odredište_podaci.source_limit)return -8;
        for(unsigned 순번=0;순번<izdanje_podesiti_veličinu;순번++)mjera_podaci[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(mjera_podaci,izdanje_podesiti_veličinu,0xffffffffu)^0xffffffffu)!=네바이트읽기(trenutno_položaj+16))return -8;
    return izdanje_podesiti_veličinu;
}
int 꾸러미읽기(const char *Naziv, unsigned char *mjera_podaci, unsigned 수용량) {
    if(!항목들)return -2;unsigned stavka_COUNT=dužina_VALUE(Naziv),trenutno_položaj=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(trenutno_položaj+28);
        if(이름길이==stavka_COUNT && 같음(Arhiva+trenutno_položaj+46,(const unsigned char*)Naziv,stavka_COUNT))return član(trenutno_položaj,mjera_podaci,수용량);
        trenutno_položaj+=46+이름길이+두바이트읽기(trenutno_položaj+30)+두바이트읽기(trenutno_položaj+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return unos_klasa; }
int 꾸러미열기(const char *fajl_unos_naziv) {
    항목들=0;unos_klasa[0]=0;
    intptr_t fajl_hvatište=사용자호출(3,(uintptr_t)fajl_unos_naziv,0,0,0,0,0);if(fajl_hvatište<0)return fajl_hvatište;
    intptr_t stavka_COUNT=사용자호출(9,fajl_hvatište,0,0,0,0,0);
    if(stavka_COUNT<22 || stavka_COUNT>(intptr_t)sizeof(Arhiva)) { 사용자호출(4,fajl_hvatište,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,fajl_hvatište,(uintptr_t)Arhiva,stavka_COUNT,0,0,0);사용자호출(4,fajl_hvatište,0,0,0,0,0);
    if(RECEIVED_COUNT!=stavka_COUNT)return -5;Veličina=stavka_COUNT;
    unsigned završiti_Pomak=Veličina-22;
    for(;;) { if(네바이트읽기(završiti_Pomak)==0x06054b50 && završiti_Pomak+22+두바이트읽기(završiti_Pomak+20)==Veličina)break; if(!završiti_Pomak)return -8;završiti_Pomak--; }
    unsigned unos_COUNT=두바이트읽기(završiti_Pomak+10);중앙목록=네바이트읽기(završiti_Pomak+16);
    if(두바이트읽기(završiti_Pomak+4)||두바이트읽기(završiti_Pomak+6)||두바이트읽기(završiti_Pomak+8)!=unos_COUNT||!unos_COUNT||unos_COUNT>256||!isječak(중앙목록,네바이트읽기(završiti_Pomak+12),završiti_Pomak)||중앙목록+네바이트읽기(završiti_Pomak+12)!=završiti_Pomak)return -8;
    unsigned trenutno_položaj=중앙목록;
    for(unsigned 순번=0;순번<unos_COUNT;순번++) {
        if(!isječak(trenutno_položaj,46,završiti_Pomak)||네바이트읽기(trenutno_položaj)!=0x02014b50||두바이트읽기(trenutno_položaj+34))return -8;
        unsigned 이름길이=두바이트읽기(trenutno_položaj+28),Dalje_stavka=46+이름길이+두바이트읽기(trenutno_položaj+30)+두바이트읽기(trenutno_položaj+32);
        if(!이름길이||이름길이>511||!isječak(trenutno_položaj,Dalje_stavka,završiti_Pomak)||네바이트읽기(trenutno_položaj+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhiva[trenutno_položaj+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned dužina_podaci=두바이트읽기(다른항목+28);if(dužina_podaci==이름길이&&같음(Arhiva+다른항목+46,Arhiva+trenutno_položaj+46,dužina_podaci))return -8;다른항목+=46+dužina_podaci+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        trenutno_položaj+=Dalje_stavka;
    }
    if(trenutno_položaj!=završiti_Pomak)return -8;항목들=unos_COUNT;
    unsigned char 꾸러미명세[4096];int Grupa_podesiti_veličinu=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupa_podesiti_veličinu<0){항목들=0;return -8;}
    꾸러미명세[Grupa_podesiti_veličinu]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupa_podesiti_veličinu) {
        unsigned Pokreni=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupa_podesiti_veličinu && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned dužina_podaci=INDEX_VALUE-Pokreni;if(INDEX_VALUE<(unsigned)Grupa_podesiti_veličinu)INDEX_VALUE++;if(dužina_podaci && 꾸러미명세[Pokreni+dužina_podaci-1]=='\r')dužina_podaci--;
        if(사용량 && dužina_podaci && 꾸러미명세[Pokreni]==' ') {Pokreni++;dužina_podaci--;}
        else {
            int mjera=atribut_podaci(논리크기,사용량,&진입점있음);if(mjera)return mjera;
            사용량=0;if(!dužina_podaci)break;
        }
        if(dužina_podaci>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<dužina_podaci;순번++)논리크기[사용량++]=꾸러미명세[Pokreni+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int mjera=atribut_podaci(논리크기,사용량,&진입점있음);if(mjera)return mjera;
    return 진입점있음?0:-8;
}
