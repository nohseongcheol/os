#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "kogum.h"
#include "uzlib.h"
static unsigned char Arhiiv[16384], 풀린자료[16385];
static unsigned Suurus, 중앙목록, 항목들;
static char kirje_tund[256];
static unsigned 두바이트읽기(unsigned tähtaja_piires_ametikoht) { return Arhiiv[tähtaja_piires_ametikoht] | Arhiiv[tähtaja_piires_ametikoht+1] << 8; }
static uint32_t 네바이트읽기(unsigned tähtaja_piires_ametikoht) { return 두바이트읽기(tähtaja_piires_ametikoht) | (uint32_t)두바이트읽기(tähtaja_piires_ametikoht+2) << 16; }
static int klipp(unsigned tähtaja_piires_ametikoht, unsigned kaup_COUNT, unsigned 한도) { return tähtaja_piires_ametikoht <= 한도 && kaup_COUNT <= 한도-tähtaja_piires_ametikoht; }
static size_t 길이(const char *string_andmed) { size_t kaup_COUNT=0; while(string_andmed[kaup_COUNT]) kaup_COUNT++; return kaup_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned kaup_COUNT) { for(unsigned 순번=0;순번<kaup_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Fail_lõpeta_kõne(void *미사용값) { (void)미사용값; return -1; }
static int atribuut_andmed(const char *Joon,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Joon,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Joon,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(kirje_tund))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char koodipunkt=Joon[12+순번];if(koodipunkt<=32||koodipunkt=='/'||koodipunkt=='\\')return -8;kirje_tund[순번]=koodipunkt;}
        kirje_tund[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int liige(unsigned tähtaja_piires_ametikoht, unsigned char *näitaja_andmed, unsigned 용량한도) {
    unsigned meetod_kirje=두바이트읽기(tähtaja_piires_ametikoht+10), konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus=두바이트읽기(tähtaja_piires_ametikoht+8), 압축크기=네바이트읽기(tähtaja_piires_ametikoht+20), vabastama_suurust_muutma=네바이트읽기(tähtaja_piires_ametikoht+24), kohalik=네바이트읽기(tähtaja_piires_ametikoht+42);
    unsigned Nimi_2=두바이트읽기(tähtaja_piires_ametikoht+28);
    if(vabastama_suurust_muutma>용량한도 || vabastama_suurust_muutma>16384 || (meetod_kirje!=0 && meetod_kirje!=8) || (konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&~0x80e))return -8;
    if(!klipp(kohalik,30,중앙목록) || 네바이트읽기(kohalik)!=0x04034b50 || 두바이트읽기(kohalik+8)!=meetod_kirje || 두바이트읽기(kohalik+6)!=konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus || 두바이트읽기(kohalik+26)!=Nimi_2)return -8;
    unsigned START_nihe=kohalik+30, 추가영역=두바이트읽기(kohalik+28);
    if(!klipp(START_nihe,Nimi_2,중앙목록) || !같음(Arhiiv+START_nihe,Arhiiv+tähtaja_piires_ametikoht+46,Nimi_2))return -8;
    START_nihe+=Nimi_2;if(!klipp(START_nihe,추가영역,중앙목록))return -8;START_nihe+=추가영역;
    if(!klipp(START_nihe,압축크기,중앙목록))return -8;
    if(!(konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&8) && (네바이트읽기(kohalik+14)!=네바이트읽기(tähtaja_piires_ametikoht+16) || 네바이트읽기(kohalik+18)!=압축크기 || 네바이트읽기(kohalik+22)!=vabastama_suurust_muutma))return -8;
    if(meetod_kirje==0) { if(압축크기!=vabastama_suurust_muutma)return -8; for(unsigned 순번=0;순번<vabastama_suurust_muutma;순번++)näitaja_andmed[순번]=Arhiiv[START_nihe+순번]; }
    else {
        uzlib_uncomp_t sihtkoht_andmed={0};uzlib_uncompress_init(&sihtkoht_andmed,0,0);
        sihtkoht_andmed.source=Arhiiv+START_nihe;sihtkoht_andmed.source_limit=sihtkoht_andmed.source+압축크기;sihtkoht_andmed.source_read_cb=Fail_lõpeta_kõne;
        /* One extra output byte lets inflate consume/check the end marker. */
        sihtkoht_andmed.dest_start=sihtkoht_andmed.dest=풀린자료;sihtkoht_andmed.dest_limit=풀린자료+vabastama_suurust_muutma+1;
        int 반환값=uzlib_uncompress(&sihtkoht_andmed);
        if(반환값!=UZLIB_DONE || sihtkoht_andmed.eof || sihtkoht_andmed.dest!=풀린자료+vabastama_suurust_muutma || sihtkoht_andmed.source!=sihtkoht_andmed.source_limit)return -8;
        for(unsigned 순번=0;순번<vabastama_suurust_muutma;순번++)näitaja_andmed[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(näitaja_andmed,vabastama_suurust_muutma,0xffffffffu)^0xffffffffu)!=네바이트읽기(tähtaja_piires_ametikoht+16))return -8;
    return vabastama_suurust_muutma;
}
int 꾸러미읽기(const char *Nimi_2, unsigned char *näitaja_andmed, unsigned puhver_võimsus) {
    if(!항목들)return -2;unsigned kaup_COUNT=길이(Nimi_2),tähtaja_piires_ametikoht=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(tähtaja_piires_ametikoht+28);
        if(이름길이==kaup_COUNT && 같음(Arhiiv+tähtaja_piires_ametikoht+46,(const unsigned char*)Nimi_2,kaup_COUNT))return liige(tähtaja_piires_ametikoht,näitaja_andmed,puhver_võimsus);
        tähtaja_piires_ametikoht+=46+이름길이+두바이트읽기(tähtaja_piires_ametikoht+30)+두바이트읽기(tähtaja_piires_ametikoht+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return kirje_tund; }
int 꾸러미열기(const char *Fail_kirje_nimetus) {
    항목들=0;kirje_tund[0]=0;
    intptr_t Fail_pide=사용자호출(3,(uintptr_t)Fail_kirje_nimetus,0,0,0,0,0);if(Fail_pide<0)return Fail_pide;
    intptr_t kaup_COUNT=사용자호출(9,Fail_pide,0,0,0,0,0);
    if(kaup_COUNT<22 || kaup_COUNT>(intptr_t)sizeof(Arhiiv)) { 사용자호출(4,Fail_pide,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Fail_pide,(uintptr_t)Arhiiv,kaup_COUNT,0,0,0);사용자호출(4,Fail_pide,0,0,0,0,0);
    if(RECEIVED_COUNT!=kaup_COUNT)return -5;Suurus=kaup_COUNT;
    unsigned lõpeta_kõne_nihe=Suurus-22;
    for(;;) { if(네바이트읽기(lõpeta_kõne_nihe)==0x06054b50 && lõpeta_kõne_nihe+22+두바이트읽기(lõpeta_kõne_nihe+20)==Suurus)break; if(!lõpeta_kõne_nihe)return -8;lõpeta_kõne_nihe--; }
    unsigned kirje_COUNT=두바이트읽기(lõpeta_kõne_nihe+10);중앙목록=네바이트읽기(lõpeta_kõne_nihe+16);
    if(두바이트읽기(lõpeta_kõne_nihe+4)||두바이트읽기(lõpeta_kõne_nihe+6)||두바이트읽기(lõpeta_kõne_nihe+8)!=kirje_COUNT||!kirje_COUNT||kirje_COUNT>256||!klipp(중앙목록,네바이트읽기(lõpeta_kõne_nihe+12),lõpeta_kõne_nihe)||중앙목록+네바이트읽기(lõpeta_kõne_nihe+12)!=lõpeta_kõne_nihe)return -8;
    unsigned tähtaja_piires_ametikoht=중앙목록;
    for(unsigned 순번=0;순번<kirje_COUNT;순번++) {
        if(!klipp(tähtaja_piires_ametikoht,46,lõpeta_kõne_nihe)||네바이트읽기(tähtaja_piires_ametikoht)!=0x02014b50||두바이트읽기(tähtaja_piires_ametikoht+34))return -8;
        unsigned 이름길이=두바이트읽기(tähtaja_piires_ametikoht+28),Edasi_kaup=46+이름길이+두바이트읽기(tähtaja_piires_ametikoht+30)+두바이트읽기(tähtaja_piires_ametikoht+32);
        if(!이름길이||이름길이>511||!klipp(tähtaja_piires_ametikoht,Edasi_kaup,lõpeta_kõne_nihe)||네바이트읽기(tähtaja_piires_ametikoht+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhiiv[tähtaja_piires_ametikoht+46+안쪽순번])return -8;
        unsigned Muud_kirje=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(Muud_kirje+28);if(길이값==이름길이&&같음(Arhiiv+Muud_kirje+46,Arhiiv+tähtaja_piires_ametikoht+46,길이값))return -8;Muud_kirje+=46+길이값+두바이트읽기(Muud_kirje+30)+두바이트읽기(Muud_kirje+32);}
        tähtaja_piires_ametikoht+=Edasi_kaup;
    }
    if(tähtaja_piires_ametikoht!=lõpeta_kõne_nihe)return -8;항목들=kirje_COUNT;
    unsigned char 꾸러미명세[4096];int Rühm_suurust_muutma=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Rühm_suurust_muutma<0){항목들=0;return -8;}
    꾸러미명세[Rühm_suurust_muutma]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Rühm_suurust_muutma) {
        unsigned Käivita_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Rühm_suurust_muutma && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned 길이값=INDEX_VALUE-Käivita_2;if(INDEX_VALUE<(unsigned)Rühm_suurust_muutma)INDEX_VALUE++;if(길이값 && 꾸러미명세[Käivita_2+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[Käivita_2]==' ') {Käivita_2++;길이값--;}
        else {
            int TULEMUS=atribuut_andmed(논리크기,사용량,&진입점있음);if(TULEMUS)return TULEMUS;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[Käivita_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int TULEMUS=atribuut_andmed(논리크기,사용량,&진입점있음);if(TULEMUS)return TULEMUS;
    return 진입점있음?0:-8;
}
