#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "zväzok.h"
#include "uzlib.h"
static unsigned char Archív[16384], 풀린자료[16385];
static unsigned Veľkosť, 중앙목록, 항목들;
static char položka_lekcia[256];
static unsigned 두바이트읽기(unsigned v_termíne_splatnosti_pozícia) { return Archív[v_termíne_splatnosti_pozícia] | Archív[v_termíne_splatnosti_pozícia+1] << 8; }
static uint32_t 네바이트읽기(unsigned v_termíne_splatnosti_pozícia) { return 두바이트읽기(v_termíne_splatnosti_pozícia) | (uint32_t)두바이트읽기(v_termíne_splatnosti_pozícia+2) << 16; }
static int klip(unsigned v_termíne_splatnosti_pozícia, unsigned položka_COUNT, unsigned 한도) { return v_termíne_splatnosti_pozícia <= 한도 && položka_COUNT <= 한도-v_termíne_splatnosti_pozícia; }
static size_t dĺžka_VALUE(const char *reťazec_údaje) { size_t položka_COUNT=0; while(reťazec_údaje[položka_COUNT]) položka_COUNT++; return položka_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned položka_COUNT) { for(unsigned 순번=0;순번<položka_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Súbor_ukončiť_hovor(void *미사용값) { (void)미사용값; return -1; }
static int atribút_údaje(const char *riadok,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)riadok,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)riadok,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(položka_lekcia))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char bod_kódu=riadok[12+순번];if(bod_kódu<=32||bod_kódu=='/'||bod_kódu=='\\')return -8;položka_lekcia[순번]=bod_kódu;}
        položka_lekcia[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int člen(unsigned v_termíne_splatnosti_pozícia, unsigned char *KR_údaje, unsigned 용량한도) {
    unsigned metóda_položka=두바이트읽기(v_termíne_splatnosti_pozícia+10), konfigurácia_Background_Intelligent_Transfer_Service=두바이트읽기(v_termíne_splatnosti_pozícia+8), 압축크기=네바이트읽기(v_termíne_splatnosti_pozícia+20), vydať_zmeniť_veľkosť=네바이트읽기(v_termíne_splatnosti_pozícia+24), miestny=네바이트읽기(v_termíne_splatnosti_pozícia+42);
    unsigned Názov=두바이트읽기(v_termíne_splatnosti_pozícia+28);
    if(vydať_zmeniť_veľkosť>용량한도 || vydať_zmeniť_veľkosť>16384 || (metóda_položka!=0 && metóda_položka!=8) || (konfigurácia_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!klip(miestny,30,중앙목록) || 네바이트읽기(miestny)!=0x04034b50 || 두바이트읽기(miestny+8)!=metóda_položka || 두바이트읽기(miestny+6)!=konfigurácia_Background_Intelligent_Transfer_Service || 두바이트읽기(miestny+26)!=Názov)return -8;
    unsigned START_Posun=miestny+30, 추가영역=두바이트읽기(miestny+28);
    if(!klip(START_Posun,Názov,중앙목록) || !같음(Archív+START_Posun,Archív+v_termíne_splatnosti_pozícia+46,Názov))return -8;
    START_Posun+=Názov;if(!klip(START_Posun,추가영역,중앙목록))return -8;START_Posun+=추가영역;
    if(!klip(START_Posun,압축크기,중앙목록))return -8;
    if(!(konfigurácia_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(miestny+14)!=네바이트읽기(v_termíne_splatnosti_pozícia+16) || 네바이트읽기(miestny+18)!=압축크기 || 네바이트읽기(miestny+22)!=vydať_zmeniť_veľkosť))return -8;
    if(metóda_položka==0) { if(압축크기!=vydať_zmeniť_veľkosť)return -8; for(unsigned 순번=0;순번<vydať_zmeniť_veľkosť;순번++)KR_údaje[순번]=Archív[START_Posun+순번]; }
    else {
        uzlib_uncomp_t cieľ_údaje={0};uzlib_uncompress_init(&cieľ_údaje,0,0);
        cieľ_údaje.source=Archív+START_Posun;cieľ_údaje.source_limit=cieľ_údaje.source+압축크기;cieľ_údaje.source_read_cb=Súbor_ukončiť_hovor;
        /* One extra output byte lets inflate consume/check the end marker. */
        cieľ_údaje.dest_start=cieľ_údaje.dest=풀린자료;cieľ_údaje.dest_limit=풀린자료+vydať_zmeniť_veľkosť+1;
        int 반환값=uzlib_uncompress(&cieľ_údaje);
        if(반환값!=UZLIB_DONE || cieľ_údaje.eof || cieľ_údaje.dest!=풀린자료+vydať_zmeniť_veľkosť || cieľ_údaje.source!=cieľ_údaje.source_limit)return -8;
        for(unsigned 순번=0;순번<vydať_zmeniť_veľkosť;순번++)KR_údaje[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_údaje,vydať_zmeniť_veľkosť,0xffffffffu)^0xffffffffu)!=네바이트읽기(v_termíne_splatnosti_pozícia+16))return -8;
    return vydať_zmeniť_veľkosť;
}
int 꾸러미읽기(const char *Názov, unsigned char *KR_údaje, unsigned medzipamäť_kapacita) {
    if(!항목들)return -2;unsigned položka_COUNT=dĺžka_VALUE(Názov),v_termíne_splatnosti_pozícia=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(v_termíne_splatnosti_pozícia+28);
        if(이름길이==položka_COUNT && 같음(Archív+v_termíne_splatnosti_pozícia+46,(const unsigned char*)Názov,položka_COUNT))return člen(v_termíne_splatnosti_pozícia,KR_údaje,medzipamäť_kapacita);
        v_termíne_splatnosti_pozícia+=46+이름길이+두바이트읽기(v_termíne_splatnosti_pozícia+30)+두바이트읽기(v_termíne_splatnosti_pozícia+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return položka_lekcia; }
int 꾸러미열기(const char *Súbor_položka_názov) {
    항목들=0;položka_lekcia[0]=0;
    intptr_t Súbor_rukoväť=사용자호출(3,(uintptr_t)Súbor_položka_názov,0,0,0,0,0);if(Súbor_rukoväť<0)return Súbor_rukoväť;
    intptr_t položka_COUNT=사용자호출(9,Súbor_rukoväť,0,0,0,0,0);
    if(položka_COUNT<22 || položka_COUNT>(intptr_t)sizeof(Archív)) { 사용자호출(4,Súbor_rukoväť,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Súbor_rukoväť,(uintptr_t)Archív,položka_COUNT,0,0,0);사용자호출(4,Súbor_rukoväť,0,0,0,0,0);
    if(RECEIVED_COUNT!=položka_COUNT)return -5;Veľkosť=položka_COUNT;
    unsigned ukončiť_hovor_Posun=Veľkosť-22;
    for(;;) { if(네바이트읽기(ukončiť_hovor_Posun)==0x06054b50 && ukončiť_hovor_Posun+22+두바이트읽기(ukončiť_hovor_Posun+20)==Veľkosť)break; if(!ukončiť_hovor_Posun)return -8;ukončiť_hovor_Posun--; }
    unsigned položka_COUNT_8f7753a1=두바이트읽기(ukončiť_hovor_Posun+10);중앙목록=네바이트읽기(ukončiť_hovor_Posun+16);
    if(두바이트읽기(ukončiť_hovor_Posun+4)||두바이트읽기(ukončiť_hovor_Posun+6)||두바이트읽기(ukončiť_hovor_Posun+8)!=položka_COUNT_8f7753a1||!položka_COUNT_8f7753a1||položka_COUNT_8f7753a1>256||!klip(중앙목록,네바이트읽기(ukončiť_hovor_Posun+12),ukončiť_hovor_Posun)||중앙목록+네바이트읽기(ukončiť_hovor_Posun+12)!=ukončiť_hovor_Posun)return -8;
    unsigned v_termíne_splatnosti_pozícia=중앙목록;
    for(unsigned 순번=0;순번<položka_COUNT_8f7753a1;순번++) {
        if(!klip(v_termíne_splatnosti_pozícia,46,ukončiť_hovor_Posun)||네바이트읽기(v_termíne_splatnosti_pozícia)!=0x02014b50||두바이트읽기(v_termíne_splatnosti_pozícia+34))return -8;
        unsigned 이름길이=두바이트읽기(v_termíne_splatnosti_pozícia+28),Ďalej_položka=46+이름길이+두바이트읽기(v_termíne_splatnosti_pozícia+30)+두바이트읽기(v_termíne_splatnosti_pozícia+32);
        if(!이름길이||이름길이>511||!klip(v_termíne_splatnosti_pozícia,Ďalej_položka,ukončiť_hovor_Posun)||네바이트읽기(v_termíne_splatnosti_pozícia+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archív[v_termíne_splatnosti_pozícia+46+안쪽순번])return -8;
        unsigned Iné_položka=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned dĺžka_údaje=두바이트읽기(Iné_položka+28);if(dĺžka_údaje==이름길이&&같음(Archív+Iné_položka+46,Archív+v_termíne_splatnosti_pozícia+46,dĺžka_údaje))return -8;Iné_položka+=46+dĺžka_údaje+두바이트읽기(Iné_položka+30)+두바이트읽기(Iné_položka+32);}
        v_termíne_splatnosti_pozícia+=Ďalej_položka;
    }
    if(v_termíne_splatnosti_pozícia!=ukončiť_hovor_Posun)return -8;항목들=položka_COUNT_8f7753a1;
    unsigned char zväzok_manifest_zostáv[4096];int Skupina_zmeniť_veľkosť=꾸러미읽기("META-INF/MANIFEST.MF",zväzok_manifest_zostáv,sizeof(zväzok_manifest_zostáv)-1);if(Skupina_zmeniť_veľkosť<0){항목들=0;return -8;}
    zväzok_manifest_zostáv[Skupina_zmeniť_veľkosť]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Skupina_zmeniť_veľkosť) {
        unsigned Spustiť_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Skupina_zmeniť_veľkosť && zväzok_manifest_zostáv[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned dĺžka_údaje=INDEX_VALUE-Spustiť_2;if(INDEX_VALUE<(unsigned)Skupina_zmeniť_veľkosť)INDEX_VALUE++;if(dĺžka_údaje && zväzok_manifest_zostáv[Spustiť_2+dĺžka_údaje-1]=='\r')dĺžka_údaje--;
        if(사용량 && dĺžka_údaje && zväzok_manifest_zostáv[Spustiť_2]==' ') {Spustiť_2++;dĺžka_údaje--;}
        else {
            int KR=atribút_údaje(논리크기,사용량,&진입점있음);if(KR)return KR;
            사용량=0;if(!dĺžka_údaje)break;
        }
        if(dĺžka_údaje>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<dĺžka_údaje;순번++)논리크기[사용량++]=zväzok_manifest_zostáv[Spustiť_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int KR=atribút_údaje(논리크기,사용량,&진입점있음);if(KR)return KR;
    return 진입점있음?0:-8;
}
