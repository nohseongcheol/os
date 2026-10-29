#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bunt.h"
#include "uzlib.h"
static unsigned char Arkiv[16384], 풀린자료[16385];
static unsigned Størrelse, 중앙목록, 항목들;
static char oppføring_time[256];
static unsigned 두바이트읽기(unsigned betalt_plassere) { return Arkiv[betalt_plassere] | Arkiv[betalt_plassere+1] << 8; }
static uint32_t 네바이트읽기(unsigned betalt_plassere) { return 두바이트읽기(betalt_plassere) | (uint32_t)두바이트읽기(betalt_plassere+2) << 16; }
static int klippe(unsigned betalt_plassere, unsigned vare_ANTALL, unsigned 한도) { return betalt_plassere <= 한도 && vare_ANTALL <= 한도-betalt_plassere; }
static size_t lengde_VERDI(const char *streng_data) { size_t vare_ANTALL=0; while(streng_data[vare_ANTALL]) vare_ANTALL++; return vare_ANTALL; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEKUND_VERDI, unsigned vare_ANTALL) { for(unsigned 순번=0;순번<vare_ANTALL;순번++)if(첫째값[순번]!=SEKUND_VERDI[순번])return 0;return 1; }
static int Fil_avslutte_en_samtale(void *미사용값) { (void)미사용값; return -1; }
static int attributt_data(const char *Linje,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Linje,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Linje,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VERDI=사용량-12;if(*진입점있음||!VERDI||VERDI>=sizeof(oppføring_time))return -8;
        for(unsigned 순번=0;순번<VERDI;순번++){unsigned char tegnkode=Linje[12+순번];if(tegnkode<=32||tegnkode=='/'||tegnkode=='\\')return -8;oppføring_time[순번]=tegnkode;}
        oppføring_time[VERDI]=0;*진입점있음=1;
    }
    return 0;
}
static int medlem(unsigned betalt_plassere, unsigned char *KR_data, unsigned 용량한도) {
    unsigned metode_oppføring=두바이트읽기(betalt_plassere+10), konfigurasjon_BITS=두바이트읽기(betalt_plassere+8), 압축크기=네바이트읽기(betalt_plassere+20), frigi_skalere=네바이트읽기(betalt_plassere+24), lokal=네바이트읽기(betalt_plassere+42);
    unsigned Navn=두바이트읽기(betalt_plassere+28);
    if(frigi_skalere>용량한도 || frigi_skalere>16384 || (metode_oppføring!=0 && metode_oppføring!=8) || (konfigurasjon_BITS&~0x80e))return -8;
    if(!klippe(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metode_oppføring || 두바이트읽기(lokal+6)!=konfigurasjon_BITS || 두바이트읽기(lokal+26)!=Navn)return -8;
    unsigned START_FORSKYVNING=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klippe(START_FORSKYVNING,Navn,중앙목록) || !같음(Arkiv+START_FORSKYVNING,Arkiv+betalt_plassere+46,Navn))return -8;
    START_FORSKYVNING+=Navn;if(!klippe(START_FORSKYVNING,추가영역,중앙목록))return -8;START_FORSKYVNING+=추가영역;
    if(!klippe(START_FORSKYVNING,압축크기,중앙목록))return -8;
    if(!(konfigurasjon_BITS&8) && (네바이트읽기(lokal+14)!=네바이트읽기(betalt_plassere+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=frigi_skalere))return -8;
    if(metode_oppføring==0) { if(압축크기!=frigi_skalere)return -8; for(unsigned 순번=0;순번<frigi_skalere;순번++)KR_data[순번]=Arkiv[START_FORSKYVNING+순번]; }
    else {
        uzlib_uncomp_t mål_data={0};uzlib_uncompress_init(&mål_data,0,0);
        mål_data.source=Arkiv+START_FORSKYVNING;mål_data.source_limit=mål_data.source+압축크기;mål_data.source_read_cb=Fil_avslutte_en_samtale;
        /* One extra output byte lets inflate consume/check the end marker. */
        mål_data.dest_start=mål_data.dest=풀린자료;mål_data.dest_limit=풀린자료+frigi_skalere+1;
        int 반환값=uzlib_uncompress(&mål_data);
        if(반환값!=UZLIB_DONE || mål_data.eof || mål_data.dest!=풀린자료+frigi_skalere || mål_data.source!=mål_data.source_limit)return -8;
        for(unsigned 순번=0;순번<frigi_skalere;순번++)KR_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_data,frigi_skalere,0xffffffffu)^0xffffffffu)!=네바이트읽기(betalt_plassere+16))return -8;
    return frigi_skalere;
}
int 꾸러미읽기(const char *Navn, unsigned char *KR_data, unsigned bufre_kapasitet) {
    if(!항목들)return -2;unsigned vare_ANTALL=lengde_VERDI(Navn),betalt_plassere=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(betalt_plassere+28);
        if(이름길이==vare_ANTALL && 같음(Arkiv+betalt_plassere+46,(const unsigned char*)Navn,vare_ANTALL))return medlem(betalt_plassere,KR_data,bufre_kapasitet);
        betalt_plassere+=46+이름길이+두바이트읽기(betalt_plassere+30)+두바이트읽기(betalt_plassere+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return oppføring_time; }
int 꾸러미열기(const char *Fil_oppføring_navn) {
    항목들=0;oppføring_time[0]=0;
    intptr_t Fil_håndtak=사용자호출(3,(uintptr_t)Fil_oppføring_navn,0,0,0,0,0);if(Fil_håndtak<0)return Fil_håndtak;
    intptr_t vare_ANTALL=사용자호출(9,Fil_håndtak,0,0,0,0,0);
    if(vare_ANTALL<22 || vare_ANTALL>(intptr_t)sizeof(Arkiv)) { 사용자호출(4,Fil_håndtak,0,0,0,0,0);return -8; }
    intptr_t MOTTATT_AVKAST_ANTALL=사용자호출(2,Fil_håndtak,(uintptr_t)Arkiv,vare_ANTALL,0,0,0);사용자호출(4,Fil_håndtak,0,0,0,0,0);
    if(MOTTATT_AVKAST_ANTALL!=vare_ANTALL)return -5;Størrelse=vare_ANTALL;
    unsigned avslutte_en_samtale_FORSKYVNING=Størrelse-22;
    for(;;) { if(네바이트읽기(avslutte_en_samtale_FORSKYVNING)==0x06054b50 && avslutte_en_samtale_FORSKYVNING+22+두바이트읽기(avslutte_en_samtale_FORSKYVNING+20)==Størrelse)break; if(!avslutte_en_samtale_FORSKYVNING)return -8;avslutte_en_samtale_FORSKYVNING--; }
    unsigned oppføring_ANTALL=두바이트읽기(avslutte_en_samtale_FORSKYVNING+10);중앙목록=네바이트읽기(avslutte_en_samtale_FORSKYVNING+16);
    if(두바이트읽기(avslutte_en_samtale_FORSKYVNING+4)||두바이트읽기(avslutte_en_samtale_FORSKYVNING+6)||두바이트읽기(avslutte_en_samtale_FORSKYVNING+8)!=oppføring_ANTALL||!oppføring_ANTALL||oppføring_ANTALL>256||!klippe(중앙목록,네바이트읽기(avslutte_en_samtale_FORSKYVNING+12),avslutte_en_samtale_FORSKYVNING)||중앙목록+네바이트읽기(avslutte_en_samtale_FORSKYVNING+12)!=avslutte_en_samtale_FORSKYVNING)return -8;
    unsigned betalt_plassere=중앙목록;
    for(unsigned 순번=0;순번<oppføring_ANTALL;순번++) {
        if(!klippe(betalt_plassere,46,avslutte_en_samtale_FORSKYVNING)||네바이트읽기(betalt_plassere)!=0x02014b50||두바이트읽기(betalt_plassere+34))return -8;
        unsigned 이름길이=두바이트읽기(betalt_plassere+28),Neste_vare=46+이름길이+두바이트읽기(betalt_plassere+30)+두바이트읽기(betalt_plassere+32);
        if(!이름길이||이름길이>511||!klippe(betalt_plassere,Neste_vare,avslutte_en_samtale_FORSKYVNING)||네바이트읽기(betalt_plassere+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkiv[betalt_plassere+46+안쪽순번])return -8;
        unsigned Annet_oppføring=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned lengde_data=두바이트읽기(Annet_oppføring+28);if(lengde_data==이름길이&&같음(Arkiv+Annet_oppføring+46,Arkiv+betalt_plassere+46,lengde_data))return -8;Annet_oppføring+=46+lengde_data+두바이트읽기(Annet_oppføring+30)+두바이트읽기(Annet_oppføring+32);}
        betalt_plassere+=Neste_vare;
    }
    if(betalt_plassere!=avslutte_en_samtale_FORSKYVNING)return -8;항목들=oppføring_ANTALL;
    unsigned char bunt_manifest[4096];int gruppe_skalere=꾸러미읽기("META-INF/MANIFEST.MF",bunt_manifest,sizeof(bunt_manifest)-1);if(gruppe_skalere<0){항목들=0;return -8;}
    bunt_manifest[gruppe_skalere]=0;
    char 논리크기[512];unsigned 사용량=0,INDEKS_VERDI=0;int 진입점있음=0;
    while(INDEKS_VERDI<(unsigned)gruppe_skalere) {
        unsigned Kjør_2=INDEKS_VERDI;while(INDEKS_VERDI<(unsigned)gruppe_skalere && bunt_manifest[INDEKS_VERDI]!='\n')INDEKS_VERDI++;
        unsigned lengde_data=INDEKS_VERDI-Kjør_2;if(INDEKS_VERDI<(unsigned)gruppe_skalere)INDEKS_VERDI++;if(lengde_data && bunt_manifest[Kjør_2+lengde_data-1]=='\r')lengde_data--;
        if(사용량 && lengde_data && bunt_manifest[Kjør_2]==' ') {Kjør_2++;lengde_data--;}
        else {
            int KR=attributt_data(논리크기,사용량,&진입점있음);if(KR)return KR;
            사용량=0;if(!lengde_data)break;
        }
        if(lengde_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<lengde_data;순번++)논리크기[사용량++]=bunt_manifest[Kjør_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int KR=attributt_data(논리크기,사용량,&진입점있음);if(KR)return KR;
    return 진입점있음?0:-8;
}
