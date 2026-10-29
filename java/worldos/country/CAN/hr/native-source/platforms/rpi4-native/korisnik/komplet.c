#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "komplet.h"
#include "uzlib.h"
static unsigned char Arhiva[16384], 풀린자료[16385];
static unsigned Veličina, 중앙목록, 항목들;
static char unos_poduka[256];
static unsigned 두바이트읽기(unsigned redovno_položaj) { return Arhiva[redovno_položaj] | Arhiva[redovno_položaj+1] << 8; }
static uint32_t 네바이트읽기(unsigned redovno_položaj) { return 두바이트읽기(redovno_položaj) | (uint32_t)두바이트읽기(redovno_položaj+2) << 16; }
static int isječak(unsigned redovno_položaj, unsigned artikl_COUNT, unsigned 한도) { return redovno_položaj <= 한도 && artikl_COUNT <= 한도-redovno_položaj; }
static size_t 길이(const char *niz_podaci) { size_t artikl_COUNT=0; while(niz_podaci[artikl_COUNT]) artikl_COUNT++; return artikl_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned artikl_COUNT) { for(unsigned 순번=0;순번<artikl_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Datoteka_završiti_razgovor(void *미사용값) { (void)미사용값; return -1; }
static int atribut_podaci(const char *red,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)red,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)red,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(unos_poduka))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char kodna_točka=red[12+순번];if(kodna_točka<=32||kodna_točka=='/'||kodna_točka=='\\')return -8;unos_poduka[순번]=kodna_točka;}
        unos_poduka[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int član(unsigned redovno_položaj, unsigned char *KR_podaci, unsigned 용량한도) {
    unsigned postupak_unos=두바이트읽기(redovno_položaj+10), konfiguracija_Pozadinski_pametni_servis_za_transfer=두바이트읽기(redovno_položaj+8), 압축크기=네바이트읽기(redovno_položaj+20), izdati_promijeniti_veličinu=네바이트읽기(redovno_položaj+24), lokalno=네바이트읽기(redovno_položaj+42);
    unsigned Ime=두바이트읽기(redovno_položaj+28);
    if(izdati_promijeniti_veličinu>용량한도 || izdati_promijeniti_veličinu>16384 || (postupak_unos!=0 && postupak_unos!=8) || (konfiguracija_Pozadinski_pametni_servis_za_transfer&~0x80e))return -8;
    if(!isječak(lokalno,30,중앙목록) || 네바이트읽기(lokalno)!=0x04034b50 || 두바이트읽기(lokalno+8)!=postupak_unos || 두바이트읽기(lokalno+6)!=konfiguracija_Pozadinski_pametni_servis_za_transfer || 두바이트읽기(lokalno+26)!=Ime)return -8;
    unsigned START_pomak=lokalno+30, 추가영역=두바이트읽기(lokalno+28);
    if(!isječak(START_pomak,Ime,중앙목록) || !같음(Arhiva+START_pomak,Arhiva+redovno_položaj+46,Ime))return -8;
    START_pomak+=Ime;if(!isječak(START_pomak,추가영역,중앙목록))return -8;START_pomak+=추가영역;
    if(!isječak(START_pomak,압축크기,중앙목록))return -8;
    if(!(konfiguracija_Pozadinski_pametni_servis_za_transfer&8) && (네바이트읽기(lokalno+14)!=네바이트읽기(redovno_položaj+16) || 네바이트읽기(lokalno+18)!=압축크기 || 네바이트읽기(lokalno+22)!=izdati_promijeniti_veličinu))return -8;
    if(postupak_unos==0) { if(압축크기!=izdati_promijeniti_veličinu)return -8; for(unsigned 순번=0;순번<izdati_promijeniti_veličinu;순번++)KR_podaci[순번]=Arhiva[START_pomak+순번]; }
    else {
        uzlib_uncomp_t odredište_podaci={0};uzlib_uncompress_init(&odredište_podaci,0,0);
        odredište_podaci.source=Arhiva+START_pomak;odredište_podaci.source_limit=odredište_podaci.source+압축크기;odredište_podaci.source_read_cb=Datoteka_završiti_razgovor;
        /* One extra output byte lets inflate consume/check the end marker. */
        odredište_podaci.dest_start=odredište_podaci.dest=풀린자료;odredište_podaci.dest_limit=풀린자료+izdati_promijeniti_veličinu+1;
        int 반환값=uzlib_uncompress(&odredište_podaci);
        if(반환값!=UZLIB_DONE || odredište_podaci.eof || odredište_podaci.dest!=풀린자료+izdati_promijeniti_veličinu || odredište_podaci.source!=odredište_podaci.source_limit)return -8;
        for(unsigned 순번=0;순번<izdati_promijeniti_veličinu;순번++)KR_podaci[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_podaci,izdati_promijeniti_veličinu,0xffffffffu)^0xffffffffu)!=네바이트읽기(redovno_položaj+16))return -8;
    return izdati_promijeniti_veličinu;
}
int 꾸러미읽기(const char *Ime, unsigned char *KR_podaci, unsigned međuspremnik_kapacitet) {
    if(!항목들)return -2;unsigned artikl_COUNT=길이(Ime),redovno_položaj=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(redovno_položaj+28);
        if(이름길이==artikl_COUNT && 같음(Arhiva+redovno_položaj+46,(const unsigned char*)Ime,artikl_COUNT))return član(redovno_položaj,KR_podaci,međuspremnik_kapacitet);
        redovno_položaj+=46+이름길이+두바이트읽기(redovno_položaj+30)+두바이트읽기(redovno_položaj+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return unos_poduka; }
int 꾸러미열기(const char *Datoteka_unos_naziv) {
    항목들=0;unos_poduka[0]=0;
    intptr_t Datoteka_ustroj=사용자호출(3,(uintptr_t)Datoteka_unos_naziv,0,0,0,0,0);if(Datoteka_ustroj<0)return Datoteka_ustroj;
    intptr_t artikl_COUNT=사용자호출(9,Datoteka_ustroj,0,0,0,0,0);
    if(artikl_COUNT<22 || artikl_COUNT>(intptr_t)sizeof(Arhiva)) { 사용자호출(4,Datoteka_ustroj,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Datoteka_ustroj,(uintptr_t)Arhiva,artikl_COUNT,0,0,0);사용자호출(4,Datoteka_ustroj,0,0,0,0,0);
    if(RECEIVED_COUNT!=artikl_COUNT)return -5;Veličina=artikl_COUNT;
    unsigned završiti_razgovor_pomak=Veličina-22;
    for(;;) { if(네바이트읽기(završiti_razgovor_pomak)==0x06054b50 && završiti_razgovor_pomak+22+두바이트읽기(završiti_razgovor_pomak+20)==Veličina)break; if(!završiti_razgovor_pomak)return -8;završiti_razgovor_pomak--; }
    unsigned unos_COUNT=두바이트읽기(završiti_razgovor_pomak+10);중앙목록=네바이트읽기(završiti_razgovor_pomak+16);
    if(두바이트읽기(završiti_razgovor_pomak+4)||두바이트읽기(završiti_razgovor_pomak+6)||두바이트읽기(završiti_razgovor_pomak+8)!=unos_COUNT||!unos_COUNT||unos_COUNT>256||!isječak(중앙목록,네바이트읽기(završiti_razgovor_pomak+12),završiti_razgovor_pomak)||중앙목록+네바이트읽기(završiti_razgovor_pomak+12)!=završiti_razgovor_pomak)return -8;
    unsigned redovno_položaj=중앙목록;
    for(unsigned 순번=0;순번<unos_COUNT;순번++) {
        if(!isječak(redovno_položaj,46,završiti_razgovor_pomak)||네바이트읽기(redovno_položaj)!=0x02014b50||두바이트읽기(redovno_položaj+34))return -8;
        unsigned 이름길이=두바이트읽기(redovno_položaj+28),Dalje_artikl=46+이름길이+두바이트읽기(redovno_položaj+30)+두바이트읽기(redovno_položaj+32);
        if(!이름길이||이름길이>511||!isječak(redovno_položaj,Dalje_artikl,završiti_razgovor_pomak)||네바이트읽기(redovno_položaj+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhiva[redovno_položaj+46+안쪽순번])return -8;
        unsigned Ostalo_unos=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(Ostalo_unos+28);if(길이값==이름길이&&같음(Arhiva+Ostalo_unos+46,Arhiva+redovno_položaj+46,길이값))return -8;Ostalo_unos+=46+길이값+두바이트읽기(Ostalo_unos+30)+두바이트읽기(Ostalo_unos+32);}
        redovno_položaj+=Dalje_artikl;
    }
    if(redovno_položaj!=završiti_razgovor_pomak)return -8;항목들=unos_COUNT;
    unsigned char 꾸러미명세[4096];int Grupa_promijeniti_veličinu=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupa_promijeniti_veličinu<0){항목들=0;return -8;}
    꾸러미명세[Grupa_promijeniti_veličinu]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupa_promijeniti_veličinu) {
        unsigned Pokreni=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupa_promijeniti_veličinu && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned 길이값=INDEX_VALUE-Pokreni;if(INDEX_VALUE<(unsigned)Grupa_promijeniti_veličinu)INDEX_VALUE++;if(길이값 && 꾸러미명세[Pokreni+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[Pokreni]==' ') {Pokreni++;길이값--;}
        else {
            int REZULTAT=atribut_podaci(논리크기,사용량,&진입점있음);if(REZULTAT)return REZULTAT;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[Pokreni+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int REZULTAT=atribut_podaci(논리크기,사용량,&진입점있음);if(REZULTAT)return REZULTAT;
    return 진입점있음?0:-8;
}
