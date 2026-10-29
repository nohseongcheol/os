#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "komplet.h"
#include "uzlib.h"
static unsigned char Arhiva[16384], 풀린자료[16385];
static unsigned promeniti_veličinu, 중앙목록, 항목들;
static char stavka_Razred[256];
static unsigned 두바이트읽기(unsigned aktuelno_pozicija) { return Arhiva[aktuelno_pozicija] | Arhiva[aktuelno_pozicija+1] << 8; }
static uint32_t 네바이트읽기(unsigned aktuelno_pozicija) { return 두바이트읽기(aktuelno_pozicija) | (uint32_t)두바이트읽기(aktuelno_pozicija+2) << 16; }
static int klip(unsigned aktuelno_pozicija, unsigned stavka_COUNT, unsigned 한도) { return aktuelno_pozicija <= 한도 && stavka_COUNT <= 한도-aktuelno_pozicija; }
static size_t 길이(const char *niska_podaci) { size_t stavka_COUNT=0; while(niska_podaci[stavka_COUNT]) stavka_COUNT++; return stavka_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned stavka_COUNT) { for(unsigned 순번=0;순번<stavka_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Datoteka_završiti_razgovor(void *미사용값) { (void)미사용값; return -1; }
static int atribut_podaci(const char *red,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)red,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)red,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(stavka_Razred))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char kôd_znaka=red[12+순번];if(kôd_znaka<=32||kôd_znaka=='/'||kôd_znaka=='\\')return -8;stavka_Razred[순번]=kôd_znaka;}
        stavka_Razred[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int član(unsigned aktuelno_pozicija, unsigned char *KR_podaci, unsigned 용량한도) {
    unsigned metod_stavka=두바이트읽기(aktuelno_pozicija+10), konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini=두바이트읽기(aktuelno_pozicija+8), 압축크기=네바이트읽기(aktuelno_pozicija+20), izdanje_promeniti_veličinu=네바이트읽기(aktuelno_pozicija+24), lokalni=네바이트읽기(aktuelno_pozicija+42);
    unsigned ime=두바이트읽기(aktuelno_pozicija+28);
    if(izdanje_promeniti_veličinu>용량한도 || izdanje_promeniti_veličinu>16384 || (metod_stavka!=0 && metod_stavka!=8) || (konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&~0x80e))return -8;
    if(!klip(lokalni,30,중앙목록) || 네바이트읽기(lokalni)!=0x04034b50 || 두바이트읽기(lokalni+8)!=metod_stavka || 두바이트읽기(lokalni+6)!=konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini || 두바이트읽기(lokalni+26)!=ime)return -8;
    unsigned START_Pomak=lokalni+30, 추가영역=두바이트읽기(lokalni+28);
    if(!klip(START_Pomak,ime,중앙목록) || !같음(Arhiva+START_Pomak,Arhiva+aktuelno_pozicija+46,ime))return -8;
    START_Pomak+=ime;if(!klip(START_Pomak,추가영역,중앙목록))return -8;START_Pomak+=추가영역;
    if(!klip(START_Pomak,압축크기,중앙목록))return -8;
    if(!(konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&8) && (네바이트읽기(lokalni+14)!=네바이트읽기(aktuelno_pozicija+16) || 네바이트읽기(lokalni+18)!=압축크기 || 네바이트읽기(lokalni+22)!=izdanje_promeniti_veličinu))return -8;
    if(metod_stavka==0) { if(압축크기!=izdanje_promeniti_veličinu)return -8; for(unsigned 순번=0;순번<izdanje_promeniti_veličinu;순번++)KR_podaci[순번]=Arhiva[START_Pomak+순번]; }
    else {
        uzlib_uncomp_t odredište_podaci={0};uzlib_uncompress_init(&odredište_podaci,0,0);
        odredište_podaci.source=Arhiva+START_Pomak;odredište_podaci.source_limit=odredište_podaci.source+압축크기;odredište_podaci.source_read_cb=Datoteka_završiti_razgovor;
        /* One extra output byte lets inflate consume/check the end marker. */
        odredište_podaci.dest_start=odredište_podaci.dest=풀린자료;odredište_podaci.dest_limit=풀린자료+izdanje_promeniti_veličinu+1;
        int 반환값=uzlib_uncompress(&odredište_podaci);
        if(반환값!=UZLIB_DONE || odredište_podaci.eof || odredište_podaci.dest!=풀린자료+izdanje_promeniti_veličinu || odredište_podaci.source!=odredište_podaci.source_limit)return -8;
        for(unsigned 순번=0;순번<izdanje_promeniti_veličinu;순번++)KR_podaci[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_podaci,izdanje_promeniti_veličinu,0xffffffffu)^0xffffffffu)!=네바이트읽기(aktuelno_pozicija+16))return -8;
    return izdanje_promeniti_veličinu;
}
int 꾸러미읽기(const char *ime, unsigned char *KR_podaci, unsigned bafer_kapacitet) {
    if(!항목들)return -2;unsigned stavka_COUNT=길이(ime),aktuelno_pozicija=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(aktuelno_pozicija+28);
        if(이름길이==stavka_COUNT && 같음(Arhiva+aktuelno_pozicija+46,(const unsigned char*)ime,stavka_COUNT))return član(aktuelno_pozicija,KR_podaci,bafer_kapacitet);
        aktuelno_pozicija+=46+이름길이+두바이트읽기(aktuelno_pozicija+30)+두바이트읽기(aktuelno_pozicija+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return stavka_Razred; }
int 꾸러미열기(const char *Datoteka_stavka_ime) {
    항목들=0;stavka_Razred[0]=0;
    intptr_t Datoteka_pokazivač=사용자호출(3,(uintptr_t)Datoteka_stavka_ime,0,0,0,0,0);if(Datoteka_pokazivač<0)return Datoteka_pokazivač;
    intptr_t stavka_COUNT=사용자호출(9,Datoteka_pokazivač,0,0,0,0,0);
    if(stavka_COUNT<22 || stavka_COUNT>(intptr_t)sizeof(Arhiva)) { 사용자호출(4,Datoteka_pokazivač,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Datoteka_pokazivač,(uintptr_t)Arhiva,stavka_COUNT,0,0,0);사용자호출(4,Datoteka_pokazivač,0,0,0,0,0);
    if(RECEIVED_COUNT!=stavka_COUNT)return -5;promeniti_veličinu=stavka_COUNT;
    unsigned završiti_razgovor_Pomak=promeniti_veličinu-22;
    for(;;) { if(네바이트읽기(završiti_razgovor_Pomak)==0x06054b50 && završiti_razgovor_Pomak+22+두바이트읽기(završiti_razgovor_Pomak+20)==promeniti_veličinu)break; if(!završiti_razgovor_Pomak)return -8;završiti_razgovor_Pomak--; }
    unsigned stavka_COUNT_8f7753a1=두바이트읽기(završiti_razgovor_Pomak+10);중앙목록=네바이트읽기(završiti_razgovor_Pomak+16);
    if(두바이트읽기(završiti_razgovor_Pomak+4)||두바이트읽기(završiti_razgovor_Pomak+6)||두바이트읽기(završiti_razgovor_Pomak+8)!=stavka_COUNT_8f7753a1||!stavka_COUNT_8f7753a1||stavka_COUNT_8f7753a1>256||!klip(중앙목록,네바이트읽기(završiti_razgovor_Pomak+12),završiti_razgovor_Pomak)||중앙목록+네바이트읽기(završiti_razgovor_Pomak+12)!=završiti_razgovor_Pomak)return -8;
    unsigned aktuelno_pozicija=중앙목록;
    for(unsigned 순번=0;순번<stavka_COUNT_8f7753a1;순번++) {
        if(!klip(aktuelno_pozicija,46,završiti_razgovor_Pomak)||네바이트읽기(aktuelno_pozicija)!=0x02014b50||두바이트읽기(aktuelno_pozicija+34))return -8;
        unsigned 이름길이=두바이트읽기(aktuelno_pozicija+28),Dalje_stavka=46+이름길이+두바이트읽기(aktuelno_pozicija+30)+두바이트읽기(aktuelno_pozicija+32);
        if(!이름길이||이름길이>511||!klip(aktuelno_pozicija,Dalje_stavka,završiti_razgovor_Pomak)||네바이트읽기(aktuelno_pozicija+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhiva[aktuelno_pozicija+46+안쪽순번])return -8;
        unsigned Ostalo_stavka=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(Ostalo_stavka+28);if(길이값==이름길이&&같음(Arhiva+Ostalo_stavka+46,Arhiva+aktuelno_pozicija+46,길이값))return -8;Ostalo_stavka+=46+길이값+두바이트읽기(Ostalo_stavka+30)+두바이트읽기(Ostalo_stavka+32);}
        aktuelno_pozicija+=Dalje_stavka;
    }
    if(aktuelno_pozicija!=završiti_razgovor_Pomak)return -8;항목들=stavka_COUNT_8f7753a1;
    unsigned char 꾸러미명세[4096];int Grupa_promeniti_veličinu=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupa_promeniti_veličinu<0){항목들=0;return -8;}
    꾸러미명세[Grupa_promeniti_veličinu]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupa_promeniti_veličinu) {
        unsigned koristiti=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupa_promeniti_veličinu && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned 길이값=INDEX_VALUE-koristiti;if(INDEX_VALUE<(unsigned)Grupa_promeniti_veličinu)INDEX_VALUE++;if(길이값 && 꾸러미명세[koristiti+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[koristiti]==' ') {koristiti++;길이값--;}
        else {
            int KR=atribut_podaci(논리크기,사용량,&진입점있음);if(KR)return KR;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[koristiti+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int KR=atribut_podaci(논리크기,사용량,&진입점있음);if(KR)return KR;
    return 진입점있음?0:-8;
}
