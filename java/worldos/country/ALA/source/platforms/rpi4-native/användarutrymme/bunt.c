#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bunt.h"
#include "uzlib.h"
static unsigned char Arkiv[16384], 풀린자료[16385];
static unsigned Storlek, 중앙목록, 항목들;
static char post_Kurs[256];
static unsigned 두바이트읽기(unsigned aktuellt_placera) { return Arkiv[aktuellt_placera] | Arkiv[aktuellt_placera+1] << 8; }
static uint32_t 네바이트읽기(unsigned aktuellt_placera) { return 두바이트읽기(aktuellt_placera) | (uint32_t)두바이트읽기(aktuellt_placera+2) << 16; }
static int klipp(unsigned aktuellt_placera, unsigned objekt_ANTAL, unsigned 한도) { return aktuellt_placera <= 한도 && objekt_ANTAL <= 한도-aktuellt_placera; }
static size_t längd_värde(const char *sträng_data) { size_t objekt_ANTAL=0; while(sträng_data[objekt_ANTAL]) objekt_ANTAL++; return objekt_ANTAL; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEKUND_värde, unsigned objekt_ANTAL) { for(unsigned 순번=0;순번<objekt_ANTAL;순번++)if(첫째값[순번]!=SEKUND_värde[순번])return 0;return 1; }
static int fil_avsluta(void *미사용값) { (void)미사용값; return -1; }
static int attribut_data(const char *inmatningsrad,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)inmatningsrad,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)inmatningsrad,(const unsigned char*)"Main-Class: ",12)) {
        unsigned värde=사용량-12;if(*진입점있음||!värde||värde>=sizeof(post_Kurs))return -8;
        for(unsigned 순번=0;순번<värde;순번++){unsigned char kodpunkt=inmatningsrad[12+순번];if(kodpunkt<=32||kodpunkt=='/'||kodpunkt=='\\')return -8;post_Kurs[순번]=kodpunkt;}
        post_Kurs[värde]=0;*진입점있음=1;
    }
    return 0;
}
static int medlem(unsigned aktuellt_placera, unsigned char *KR_data, unsigned 용량한도) {
    unsigned metod_post=두바이트읽기(aktuellt_placera+10), konfiguration_BITS=두바이트읽기(aktuellt_placera+8), 압축크기=네바이트읽기(aktuellt_placera+20), släppa_storlek=네바이트읽기(aktuellt_placera+24), lokal=네바이트읽기(aktuellt_placera+42);
    unsigned Namn=두바이트읽기(aktuellt_placera+28);
    if(släppa_storlek>용량한도 || släppa_storlek>16384 || (metod_post!=0 && metod_post!=8) || (konfiguration_BITS&~0x80e))return -8;
    if(!klipp(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metod_post || 두바이트읽기(lokal+6)!=konfiguration_BITS || 두바이트읽기(lokal+26)!=Namn)return -8;
    unsigned START_FÖRSKJUTNING=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klipp(START_FÖRSKJUTNING,Namn,중앙목록) || !같음(Arkiv+START_FÖRSKJUTNING,Arkiv+aktuellt_placera+46,Namn))return -8;
    START_FÖRSKJUTNING+=Namn;if(!klipp(START_FÖRSKJUTNING,추가영역,중앙목록))return -8;START_FÖRSKJUTNING+=추가영역;
    if(!klipp(START_FÖRSKJUTNING,압축크기,중앙목록))return -8;
    if(!(konfiguration_BITS&8) && (네바이트읽기(lokal+14)!=네바이트읽기(aktuellt_placera+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=släppa_storlek))return -8;
    if(metod_post==0) { if(압축크기!=släppa_storlek)return -8; for(unsigned 순번=0;순번<släppa_storlek;순번++)KR_data[순번]=Arkiv[START_FÖRSKJUTNING+순번]; }
    else {
        uzlib_uncomp_t mål_data={0};uzlib_uncompress_init(&mål_data,0,0);
        mål_data.source=Arkiv+START_FÖRSKJUTNING;mål_data.source_limit=mål_data.source+압축크기;mål_data.source_read_cb=fil_avsluta;
        /* One extra output byte lets inflate consume/check the end marker. */
        mål_data.dest_start=mål_data.dest=풀린자료;mål_data.dest_limit=풀린자료+släppa_storlek+1;
        int 반환값=uzlib_uncompress(&mål_data);
        if(반환값!=UZLIB_DONE || mål_data.eof || mål_data.dest!=풀린자료+släppa_storlek || mål_data.source!=mål_data.source_limit)return -8;
        for(unsigned 순번=0;순번<släppa_storlek;순번++)KR_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_data,släppa_storlek,0xffffffffu)^0xffffffffu)!=네바이트읽기(aktuellt_placera+16))return -8;
    return släppa_storlek;
}
int 꾸러미읽기(const char *Namn, unsigned char *KR_data, unsigned buffra_kapacitet) {
    if(!항목들)return -2;unsigned objekt_ANTAL=längd_värde(Namn),aktuellt_placera=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(aktuellt_placera+28);
        if(이름길이==objekt_ANTAL && 같음(Arkiv+aktuellt_placera+46,(const unsigned char*)Namn,objekt_ANTAL))return medlem(aktuellt_placera,KR_data,buffra_kapacitet);
        aktuellt_placera+=46+이름길이+두바이트읽기(aktuellt_placera+30)+두바이트읽기(aktuellt_placera+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return post_Kurs; }
int 꾸러미열기(const char *fil_post_namn) {
    항목들=0;post_Kurs[0]=0;
    intptr_t filreferens=사용자호출(3,(uintptr_t)fil_post_namn,0,0,0,0,0);if(filreferens<0)return filreferens;
    intptr_t objekt_ANTAL=사용자호출(9,filreferens,0,0,0,0,0);
    if(objekt_ANTAL<22 || objekt_ANTAL>(intptr_t)sizeof(Arkiv)) { 사용자호출(4,filreferens,0,0,0,0,0);return -8; }
    intptr_t BELOPP_ANTAL=사용자호출(2,filreferens,(uintptr_t)Arkiv,objekt_ANTAL,0,0,0);사용자호출(4,filreferens,0,0,0,0,0);
    if(BELOPP_ANTAL!=objekt_ANTAL)return -5;Storlek=objekt_ANTAL;
    unsigned avsluta_FÖRSKJUTNING=Storlek-22;
    for(;;) { if(네바이트읽기(avsluta_FÖRSKJUTNING)==0x06054b50 && avsluta_FÖRSKJUTNING+22+두바이트읽기(avsluta_FÖRSKJUTNING+20)==Storlek)break; if(!avsluta_FÖRSKJUTNING)return -8;avsluta_FÖRSKJUTNING--; }
    unsigned post_ANTAL=두바이트읽기(avsluta_FÖRSKJUTNING+10);중앙목록=네바이트읽기(avsluta_FÖRSKJUTNING+16);
    if(두바이트읽기(avsluta_FÖRSKJUTNING+4)||두바이트읽기(avsluta_FÖRSKJUTNING+6)||두바이트읽기(avsluta_FÖRSKJUTNING+8)!=post_ANTAL||!post_ANTAL||post_ANTAL>256||!klipp(중앙목록,네바이트읽기(avsluta_FÖRSKJUTNING+12),avsluta_FÖRSKJUTNING)||중앙목록+네바이트읽기(avsluta_FÖRSKJUTNING+12)!=avsluta_FÖRSKJUTNING)return -8;
    unsigned aktuellt_placera=중앙목록;
    for(unsigned 순번=0;순번<post_ANTAL;순번++) {
        if(!klipp(aktuellt_placera,46,avsluta_FÖRSKJUTNING)||네바이트읽기(aktuellt_placera)!=0x02014b50||두바이트읽기(aktuellt_placera+34))return -8;
        unsigned 이름길이=두바이트읽기(aktuellt_placera+28),Nästa_objekt=46+이름길이+두바이트읽기(aktuellt_placera+30)+두바이트읽기(aktuellt_placera+32);
        if(!이름길이||이름길이>511||!klipp(aktuellt_placera,Nästa_objekt,avsluta_FÖRSKJUTNING)||네바이트읽기(aktuellt_placera+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkiv[aktuellt_placera+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned längd_data=두바이트읽기(다른항목+28);if(längd_data==이름길이&&같음(Arkiv+다른항목+46,Arkiv+aktuellt_placera+46,längd_data))return -8;다른항목+=46+längd_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        aktuellt_placera+=Nästa_objekt;
    }
    if(aktuellt_placera!=avsluta_FÖRSKJUTNING)return -8;항목들=post_ANTAL;
    unsigned char bunt_manifest[4096];int grupp_storlek=꾸러미읽기("META-INF/MANIFEST.MF",bunt_manifest,sizeof(bunt_manifest)-1);if(grupp_storlek<0){항목들=0;return -8;}
    bunt_manifest[grupp_storlek]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_värde=0;int 진입점있음=0;
    while(INDEX_värde<(unsigned)grupp_storlek) {
        unsigned Kör=INDEX_värde;while(INDEX_värde<(unsigned)grupp_storlek && bunt_manifest[INDEX_värde]!='\n')INDEX_värde++;
        unsigned längd_data=INDEX_värde-Kör;if(INDEX_värde<(unsigned)grupp_storlek)INDEX_värde++;if(längd_data && bunt_manifest[Kör+längd_data-1]=='\r')längd_data--;
        if(사용량 && längd_data && bunt_manifest[Kör]==' ') {Kör++;längd_data--;}
        else {
            int RESULTAT=attribut_data(논리크기,사용량,&진입점있음);if(RESULTAT)return RESULTAT;
            사용량=0;if(!längd_data)break;
        }
        if(längd_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<längd_data;순번++)논리크기[사용량++]=bunt_manifest[Kör+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int RESULTAT=attribut_data(논리크기,사용량,&진입점있음);if(RESULTAT)return RESULTAT;
    return 진입점있음?0:-8;
}
