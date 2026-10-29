#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bundel.h"
#include "uzlib.h"
static unsigned char Archief[16384], 풀린자료[16385];
static unsigned Grootte, 중앙목록, 항목들;
static char invoer_les[256];
static unsigned 두바이트읽기(unsigned actueel_functie) { return Archief[actueel_functie] | Archief[actueel_functie+1] << 8; }
static uint32_t 네바이트읽기(unsigned actueel_functie) { return 두바이트읽기(actueel_functie) | (uint32_t)두바이트읽기(actueel_functie+2) << 16; }
static int clip(unsigned actueel_functie, unsigned item_AANTAL, unsigned 한도) { return actueel_functie <= 한도 && item_AANTAL <= 한도-actueel_functie; }
static size_t tijdsduur_WAARDE(const char *tekenreeks_gegevens) { size_t item_AANTAL=0; while(tekenreeks_gegevens[item_AANTAL]) item_AANTAL++; return item_AANTAL; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECONDE_WAARDE, unsigned item_AANTAL) { for(unsigned 순번=0;순번<item_AANTAL;순번++)if(첫째값[순번]!=SECONDE_WAARDE[순번])return 0;return 1; }
static int Bestand_beëindigen(void *미사용값) { (void)미사용값; return -1; }
static int kenmerk_gegevens(const char *invoerregel,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)invoerregel,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)invoerregel,(const unsigned char*)"Main-Class: ",12)) {
        unsigned WAARDE=사용량-12;if(*진입점있음||!WAARDE||WAARDE>=sizeof(invoer_les))return -8;
        for(unsigned 순번=0;순번<WAARDE;순번++){unsigned char codepoint=invoerregel[12+순번];if(codepoint<=32||codepoint=='/'||codepoint=='\\')return -8;invoer_les[순번]=codepoint;}
        invoer_les[WAARDE]=0;*진입점있음=1;
    }
    return 0;
}
static int lid(unsigned actueel_functie, unsigned char *HR_gegevens, unsigned 용량한도) {
    unsigned methode_invoer=두바이트읽기(actueel_functie+10), configuratie_BITS=두바이트읽기(actueel_functie+8), 압축크기=네바이트읽기(actueel_functie+20), versie_formaat_wijzigen=네바이트읽기(actueel_functie+24), lokaal=네바이트읽기(actueel_functie+42);
    unsigned Naam=두바이트읽기(actueel_functie+28);
    if(versie_formaat_wijzigen>용량한도 || versie_formaat_wijzigen>16384 || (methode_invoer!=0 && methode_invoer!=8) || (configuratie_BITS&~0x80e))return -8;
    if(!clip(lokaal,30,중앙목록) || 네바이트읽기(lokaal)!=0x04034b50 || 두바이트읽기(lokaal+8)!=methode_invoer || 두바이트읽기(lokaal+6)!=configuratie_BITS || 두바이트읽기(lokaal+26)!=Naam)return -8;
    unsigned START_VERSCHUIVING=lokaal+30, 추가영역=두바이트읽기(lokaal+28);
    if(!clip(START_VERSCHUIVING,Naam,중앙목록) || !같음(Archief+START_VERSCHUIVING,Archief+actueel_functie+46,Naam))return -8;
    START_VERSCHUIVING+=Naam;if(!clip(START_VERSCHUIVING,추가영역,중앙목록))return -8;START_VERSCHUIVING+=추가영역;
    if(!clip(START_VERSCHUIVING,압축크기,중앙목록))return -8;
    if(!(configuratie_BITS&8) && (네바이트읽기(lokaal+14)!=네바이트읽기(actueel_functie+16) || 네바이트읽기(lokaal+18)!=압축크기 || 네바이트읽기(lokaal+22)!=versie_formaat_wijzigen))return -8;
    if(methode_invoer==0) { if(압축크기!=versie_formaat_wijzigen)return -8; for(unsigned 순번=0;순번<versie_formaat_wijzigen;순번++)HR_gegevens[순번]=Archief[START_VERSCHUIVING+순번]; }
    else {
        uzlib_uncomp_t doel_gegevens={0};uzlib_uncompress_init(&doel_gegevens,0,0);
        doel_gegevens.source=Archief+START_VERSCHUIVING;doel_gegevens.source_limit=doel_gegevens.source+압축크기;doel_gegevens.source_read_cb=Bestand_beëindigen;
        /* One extra output byte lets inflate consume/check the end marker. */
        doel_gegevens.dest_start=doel_gegevens.dest=풀린자료;doel_gegevens.dest_limit=풀린자료+versie_formaat_wijzigen+1;
        int 반환값=uzlib_uncompress(&doel_gegevens);
        if(반환값!=UZLIB_DONE || doel_gegevens.eof || doel_gegevens.dest!=풀린자료+versie_formaat_wijzigen || doel_gegevens.source!=doel_gegevens.source_limit)return -8;
        for(unsigned 순번=0;순번<versie_formaat_wijzigen;순번++)HR_gegevens[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(HR_gegevens,versie_formaat_wijzigen,0xffffffffu)^0xffffffffu)!=네바이트읽기(actueel_functie+16))return -8;
    return versie_formaat_wijzigen;
}
int 꾸러미읽기(const char *Naam, unsigned char *HR_gegevens, unsigned buffer_capaciteit) {
    if(!항목들)return -2;unsigned item_AANTAL=tijdsduur_WAARDE(Naam),actueel_functie=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(actueel_functie+28);
        if(이름길이==item_AANTAL && 같음(Archief+actueel_functie+46,(const unsigned char*)Naam,item_AANTAL))return lid(actueel_functie,HR_gegevens,buffer_capaciteit);
        actueel_functie+=46+이름길이+두바이트읽기(actueel_functie+30)+두바이트읽기(actueel_functie+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return invoer_les; }
int 꾸러미열기(const char *Bestand_invoer_naam) {
    항목들=0;invoer_les[0]=0;
    intptr_t bestandsingang=사용자호출(3,(uintptr_t)Bestand_invoer_naam,0,0,0,0,0);if(bestandsingang<0)return bestandsingang;
    intptr_t item_AANTAL=사용자호출(9,bestandsingang,0,0,0,0,0);
    if(item_AANTAL<22 || item_AANTAL>(intptr_t)sizeof(Archief)) { 사용자호출(4,bestandsingang,0,0,0,0,0);return -8; }
    intptr_t OPBRENGST_AANTAL=사용자호출(2,bestandsingang,(uintptr_t)Archief,item_AANTAL,0,0,0);사용자호출(4,bestandsingang,0,0,0,0,0);
    if(OPBRENGST_AANTAL!=item_AANTAL)return -5;Grootte=item_AANTAL;
    unsigned beëindigen_VERSCHUIVING=Grootte-22;
    for(;;) { if(네바이트읽기(beëindigen_VERSCHUIVING)==0x06054b50 && beëindigen_VERSCHUIVING+22+두바이트읽기(beëindigen_VERSCHUIVING+20)==Grootte)break; if(!beëindigen_VERSCHUIVING)return -8;beëindigen_VERSCHUIVING--; }
    unsigned invoer_AANTAL_8f7753a1=두바이트읽기(beëindigen_VERSCHUIVING+10);중앙목록=네바이트읽기(beëindigen_VERSCHUIVING+16);
    if(두바이트읽기(beëindigen_VERSCHUIVING+4)||두바이트읽기(beëindigen_VERSCHUIVING+6)||두바이트읽기(beëindigen_VERSCHUIVING+8)!=invoer_AANTAL_8f7753a1||!invoer_AANTAL_8f7753a1||invoer_AANTAL_8f7753a1>256||!clip(중앙목록,네바이트읽기(beëindigen_VERSCHUIVING+12),beëindigen_VERSCHUIVING)||중앙목록+네바이트읽기(beëindigen_VERSCHUIVING+12)!=beëindigen_VERSCHUIVING)return -8;
    unsigned actueel_functie=중앙목록;
    for(unsigned 순번=0;순번<invoer_AANTAL_8f7753a1;순번++) {
        if(!clip(actueel_functie,46,beëindigen_VERSCHUIVING)||네바이트읽기(actueel_functie)!=0x02014b50||두바이트읽기(actueel_functie+34))return -8;
        unsigned 이름길이=두바이트읽기(actueel_functie+28),Volgende_item=46+이름길이+두바이트읽기(actueel_functie+30)+두바이트읽기(actueel_functie+32);
        if(!이름길이||이름길이>511||!clip(actueel_functie,Volgende_item,beëindigen_VERSCHUIVING)||네바이트읽기(actueel_functie+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archief[actueel_functie+46+안쪽순번])return -8;
        unsigned Overige_invoer=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned tijdsduur_gegevens=두바이트읽기(Overige_invoer+28);if(tijdsduur_gegevens==이름길이&&같음(Archief+Overige_invoer+46,Archief+actueel_functie+46,tijdsduur_gegevens))return -8;Overige_invoer+=46+tijdsduur_gegevens+두바이트읽기(Overige_invoer+30)+두바이트읽기(Overige_invoer+32);}
        actueel_functie+=Volgende_item;
    }
    if(actueel_functie!=beëindigen_VERSCHUIVING)return -8;항목들=invoer_AANTAL_8f7753a1;
    unsigned char bundel_manifest[4096];int Groep_formaat_wijzigen=꾸러미읽기("META-INF/MANIFEST.MF",bundel_manifest,sizeof(bundel_manifest)-1);if(Groep_formaat_wijzigen<0){항목들=0;return -8;}
    bundel_manifest[Groep_formaat_wijzigen]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_WAARDE=0;int 진입점있음=0;
    while(INDEX_WAARDE<(unsigned)Groep_formaat_wijzigen) {
        unsigned starten=INDEX_WAARDE;while(INDEX_WAARDE<(unsigned)Groep_formaat_wijzigen && bundel_manifest[INDEX_WAARDE]!='\n')INDEX_WAARDE++;
        unsigned tijdsduur_gegevens=INDEX_WAARDE-starten;if(INDEX_WAARDE<(unsigned)Groep_formaat_wijzigen)INDEX_WAARDE++;if(tijdsduur_gegevens && bundel_manifest[starten+tijdsduur_gegevens-1]=='\r')tijdsduur_gegevens--;
        if(사용량 && tijdsduur_gegevens && bundel_manifest[starten]==' ') {starten++;tijdsduur_gegevens--;}
        else {
            int resultaat=kenmerk_gegevens(논리크기,사용량,&진입점있음);if(resultaat)return resultaat;
            사용량=0;if(!tijdsduur_gegevens)break;
        }
        if(tijdsduur_gegevens>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<tijdsduur_gegevens;순번++)논리크기[사용량++]=bundel_manifest[starten+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int resultaat=kenmerk_gegevens(논리크기,사용량,&진입점있음);if(resultaat)return resultaat;
    return 진입점있음?0:-8;
}
