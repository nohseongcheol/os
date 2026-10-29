#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "saistīt.h"
#include "uzlib.h"
static unsigned char Arhīvs[16384], 풀린자료[16385];
static unsigned Izmērs, 중앙목록, 항목들;
static char ievade_klase[256];
static unsigned 두바이트읽기(unsigned pašreizējais_amats) { return Arhīvs[pašreizējais_amats] | Arhīvs[pašreizējais_amats+1] << 8; }
static uint32_t 네바이트읽기(unsigned pašreizējais_amats) { return 두바이트읽기(pašreizējais_amats) | (uint32_t)두바이트읽기(pašreizējais_amats+2) << 16; }
static int klips(unsigned pašreizējais_amats, unsigned krājums_COUNT, unsigned 한도) { return pašreizējais_amats <= 한도 && krājums_COUNT <= 한도-pašreizējais_amats; }
static size_t 길이(const char *virkne_dati) { size_t krājums_COUNT=0; while(virkne_dati[krājums_COUNT]) krājums_COUNT++; return krājums_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned krājums_COUNT) { for(unsigned 순번=0;순번<krājums_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Fails_beigt_zvanu(void *미사용값) { (void)미사용값; return -1; }
static int atribūts_dati(const char *Līniju,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Līniju,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Līniju,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(ievade_klase))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char koda_punkts=Līniju[12+순번];if(koda_punkts<=32||koda_punkts=='/'||koda_punkts=='\\')return -8;ievade_klase[순번]=koda_punkts;}
        ievade_klase[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int elements(unsigned pašreizējais_amats, unsigned char *mērs_dati, unsigned 용량한도) {
    unsigned metode_ievade=두바이트읽기(pašreizējais_amats+10), konfigurācija_Background_Intelligent_Transfer_Service=두바이트읽기(pašreizējais_amats+8), 압축크기=네바이트읽기(pašreizējais_amats+20), izlaist_mainīt_izmērus=네바이트읽기(pašreizējais_amats+24), vietējs=네바이트읽기(pašreizējais_amats+42);
    unsigned Nosaukums=두바이트읽기(pašreizējais_amats+28);
    if(izlaist_mainīt_izmērus>용량한도 || izlaist_mainīt_izmērus>16384 || (metode_ievade!=0 && metode_ievade!=8) || (konfigurācija_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!klips(vietējs,30,중앙목록) || 네바이트읽기(vietējs)!=0x04034b50 || 두바이트읽기(vietējs+8)!=metode_ievade || 두바이트읽기(vietējs+6)!=konfigurācija_Background_Intelligent_Transfer_Service || 두바이트읽기(vietējs+26)!=Nosaukums)return -8;
    unsigned Sākt_Nobīde=vietējs+30, 추가영역=두바이트읽기(vietējs+28);
    if(!klips(Sākt_Nobīde,Nosaukums,중앙목록) || !같음(Arhīvs+Sākt_Nobīde,Arhīvs+pašreizējais_amats+46,Nosaukums))return -8;
    Sākt_Nobīde+=Nosaukums;if(!klips(Sākt_Nobīde,추가영역,중앙목록))return -8;Sākt_Nobīde+=추가영역;
    if(!klips(Sākt_Nobīde,압축크기,중앙목록))return -8;
    if(!(konfigurācija_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(vietējs+14)!=네바이트읽기(pašreizējais_amats+16) || 네바이트읽기(vietējs+18)!=압축크기 || 네바이트읽기(vietējs+22)!=izlaist_mainīt_izmērus))return -8;
    if(metode_ievade==0) { if(압축크기!=izlaist_mainīt_izmērus)return -8; for(unsigned 순번=0;순번<izlaist_mainīt_izmērus;순번++)mērs_dati[순번]=Arhīvs[Sākt_Nobīde+순번]; }
    else {
        uzlib_uncomp_t mērķis_dati={0};uzlib_uncompress_init(&mērķis_dati,0,0);
        mērķis_dati.source=Arhīvs+Sākt_Nobīde;mērķis_dati.source_limit=mērķis_dati.source+압축크기;mērķis_dati.source_read_cb=Fails_beigt_zvanu;
        /* One extra output byte lets inflate consume/check the end marker. */
        mērķis_dati.dest_start=mērķis_dati.dest=풀린자료;mērķis_dati.dest_limit=풀린자료+izlaist_mainīt_izmērus+1;
        int 반환값=uzlib_uncompress(&mērķis_dati);
        if(반환값!=UZLIB_DONE || mērķis_dati.eof || mērķis_dati.dest!=풀린자료+izlaist_mainīt_izmērus || mērķis_dati.source!=mērķis_dati.source_limit)return -8;
        for(unsigned 순번=0;순번<izlaist_mainīt_izmērus;순번++)mērs_dati[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(mērs_dati,izlaist_mainīt_izmērus,0xffffffffu)^0xffffffffu)!=네바이트읽기(pašreizējais_amats+16))return -8;
    return izlaist_mainīt_izmērus;
}
int 꾸러미읽기(const char *Nosaukums, unsigned char *mērs_dati, unsigned buferis_noslodze) {
    if(!항목들)return -2;unsigned krājums_COUNT=길이(Nosaukums),pašreizējais_amats=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(pašreizējais_amats+28);
        if(이름길이==krājums_COUNT && 같음(Arhīvs+pašreizējais_amats+46,(const unsigned char*)Nosaukums,krājums_COUNT))return elements(pašreizējais_amats,mērs_dati,buferis_noslodze);
        pašreizējais_amats+=46+이름길이+두바이트읽기(pašreizējais_amats+30)+두바이트읽기(pašreizējais_amats+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ievade_klase; }
int 꾸러미열기(const char *Fails_ievade_nosaukums) {
    항목들=0;ievade_klase[0]=0;
    intptr_t Fails_turis=사용자호출(3,(uintptr_t)Fails_ievade_nosaukums,0,0,0,0,0);if(Fails_turis<0)return Fails_turis;
    intptr_t krājums_COUNT=사용자호출(9,Fails_turis,0,0,0,0,0);
    if(krājums_COUNT<22 || krājums_COUNT>(intptr_t)sizeof(Arhīvs)) { 사용자호출(4,Fails_turis,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Fails_turis,(uintptr_t)Arhīvs,krājums_COUNT,0,0,0);사용자호출(4,Fails_turis,0,0,0,0,0);
    if(RECEIVED_COUNT!=krājums_COUNT)return -5;Izmērs=krājums_COUNT;
    unsigned beigt_zvanu_Nobīde=Izmērs-22;
    for(;;) { if(네바이트읽기(beigt_zvanu_Nobīde)==0x06054b50 && beigt_zvanu_Nobīde+22+두바이트읽기(beigt_zvanu_Nobīde+20)==Izmērs)break; if(!beigt_zvanu_Nobīde)return -8;beigt_zvanu_Nobīde--; }
    unsigned ievade_COUNT=두바이트읽기(beigt_zvanu_Nobīde+10);중앙목록=네바이트읽기(beigt_zvanu_Nobīde+16);
    if(두바이트읽기(beigt_zvanu_Nobīde+4)||두바이트읽기(beigt_zvanu_Nobīde+6)||두바이트읽기(beigt_zvanu_Nobīde+8)!=ievade_COUNT||!ievade_COUNT||ievade_COUNT>256||!klips(중앙목록,네바이트읽기(beigt_zvanu_Nobīde+12),beigt_zvanu_Nobīde)||중앙목록+네바이트읽기(beigt_zvanu_Nobīde+12)!=beigt_zvanu_Nobīde)return -8;
    unsigned pašreizējais_amats=중앙목록;
    for(unsigned 순번=0;순번<ievade_COUNT;순번++) {
        if(!klips(pašreizējais_amats,46,beigt_zvanu_Nobīde)||네바이트읽기(pašreizējais_amats)!=0x02014b50||두바이트읽기(pašreizējais_amats+34))return -8;
        unsigned 이름길이=두바이트읽기(pašreizējais_amats+28),Tālāk_krājums=46+이름길이+두바이트읽기(pašreizējais_amats+30)+두바이트읽기(pašreizējais_amats+32);
        if(!이름길이||이름길이>511||!klips(pašreizējais_amats,Tālāk_krājums,beigt_zvanu_Nobīde)||네바이트읽기(pašreizējais_amats+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhīvs[pašreizējais_amats+46+안쪽순번])return -8;
        unsigned Citi_ievade=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(Citi_ievade+28);if(길이값==이름길이&&같음(Arhīvs+Citi_ievade+46,Arhīvs+pašreizējais_amats+46,길이값))return -8;Citi_ievade+=46+길이값+두바이트읽기(Citi_ievade+30)+두바이트읽기(Citi_ievade+32);}
        pašreizējais_amats+=Tālāk_krājums;
    }
    if(pašreizējais_amats!=beigt_zvanu_Nobīde)return -8;항목들=ievade_COUNT;
    unsigned char 꾸러미명세[4096];int Grupa_mainīt_izmērus=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupa_mainīt_izmērus<0){항목들=0;return -8;}
    꾸러미명세[Grupa_mainīt_izmērus]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupa_mainīt_izmērus) {
        unsigned Palaist=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupa_mainīt_izmērus && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned 길이값=INDEX_VALUE-Palaist;if(INDEX_VALUE<(unsigned)Grupa_mainīt_izmērus)INDEX_VALUE++;if(길이값 && 꾸러미명세[Palaist+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[Palaist]==' ') {Palaist++;길이값--;}
        else {
            int mērs=atribūts_dati(논리크기,사용량,&진입점있음);if(mērs)return mērs;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[Palaist+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int mērs=atribūts_dati(논리크기,사용량,&진입점있음);if(mērs)return mērs;
    return 진입점있음?0:-8;
}
