#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "sveženj.h"
#include "uzlib.h"
static unsigned char Arhiv[16384], 풀린자료[16385];
static unsigned Velikost, 중앙목록, 항목들;
static char vnos_Razred[256];
static unsigned 두바이트읽기(unsigned sprotno_položaj) { return Arhiv[sprotno_položaj] | Arhiv[sprotno_položaj+1] << 8; }
static uint32_t 네바이트읽기(unsigned sprotno_položaj) { return 두바이트읽기(sprotno_položaj) | (uint32_t)두바이트읽기(sprotno_položaj+2) << 16; }
static int izrezek(unsigned sprotno_položaj, unsigned element_COUNT, unsigned 한도) { return sprotno_položaj <= 한도 && element_COUNT <= 한도-sprotno_položaj; }
static size_t 길이(const char *niz_podatki) { size_t element_COUNT=0; while(niz_podatki[element_COUNT]) element_COUNT++; return element_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned element_COUNT) { for(unsigned 순번=0;순번<element_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Datoteka_končati_klic(void *미사용값) { (void)미사용값; return -1; }
static int atribut_podatki(const char *Črtni,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Črtni,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Črtni,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(vnos_Razred))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char koda_znaka=Črtni[12+순번];if(koda_znaka<=32||koda_znaka=='/'||koda_znaka=='\\')return -8;vnos_Razred[순번]=koda_znaka;}
        vnos_Razred[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int član(unsigned sprotno_položaj, unsigned char *KR_podatki, unsigned 용량한도) {
    unsigned metoda_vnos=두바이트읽기(sprotno_položaj+10), konfiguracija_storitev_Background_Intelligent_Transfer_Service=두바이트읽기(sprotno_položaj+8), 압축크기=네바이트읽기(sprotno_položaj+20), izdaja_spremeniti_velikost=네바이트읽기(sprotno_položaj+24), lokalen_krajeven=네바이트읽기(sprotno_položaj+42);
    unsigned Ime=두바이트읽기(sprotno_položaj+28);
    if(izdaja_spremeniti_velikost>용량한도 || izdaja_spremeniti_velikost>16384 || (metoda_vnos!=0 && metoda_vnos!=8) || (konfiguracija_storitev_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!izrezek(lokalen_krajeven,30,중앙목록) || 네바이트읽기(lokalen_krajeven)!=0x04034b50 || 두바이트읽기(lokalen_krajeven+8)!=metoda_vnos || 두바이트읽기(lokalen_krajeven+6)!=konfiguracija_storitev_Background_Intelligent_Transfer_Service || 두바이트읽기(lokalen_krajeven+26)!=Ime)return -8;
    unsigned Start_odmik=lokalen_krajeven+30, 추가영역=두바이트읽기(lokalen_krajeven+28);
    if(!izrezek(Start_odmik,Ime,중앙목록) || !같음(Arhiv+Start_odmik,Arhiv+sprotno_položaj+46,Ime))return -8;
    Start_odmik+=Ime;if(!izrezek(Start_odmik,추가영역,중앙목록))return -8;Start_odmik+=추가영역;
    if(!izrezek(Start_odmik,압축크기,중앙목록))return -8;
    if(!(konfiguracija_storitev_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(lokalen_krajeven+14)!=네바이트읽기(sprotno_položaj+16) || 네바이트읽기(lokalen_krajeven+18)!=압축크기 || 네바이트읽기(lokalen_krajeven+22)!=izdaja_spremeniti_velikost))return -8;
    if(metoda_vnos==0) { if(압축크기!=izdaja_spremeniti_velikost)return -8; for(unsigned 순번=0;순번<izdaja_spremeniti_velikost;순번++)KR_podatki[순번]=Arhiv[Start_odmik+순번]; }
    else {
        uzlib_uncomp_t cilj_podatki={0};uzlib_uncompress_init(&cilj_podatki,0,0);
        cilj_podatki.source=Arhiv+Start_odmik;cilj_podatki.source_limit=cilj_podatki.source+압축크기;cilj_podatki.source_read_cb=Datoteka_končati_klic;
        /* One extra output byte lets inflate consume/check the end marker. */
        cilj_podatki.dest_start=cilj_podatki.dest=풀린자료;cilj_podatki.dest_limit=풀린자료+izdaja_spremeniti_velikost+1;
        int 반환값=uzlib_uncompress(&cilj_podatki);
        if(반환값!=UZLIB_DONE || cilj_podatki.eof || cilj_podatki.dest!=풀린자료+izdaja_spremeniti_velikost || cilj_podatki.source!=cilj_podatki.source_limit)return -8;
        for(unsigned 순번=0;순번<izdaja_spremeniti_velikost;순번++)KR_podatki[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_podatki,izdaja_spremeniti_velikost,0xffffffffu)^0xffffffffu)!=네바이트읽기(sprotno_položaj+16))return -8;
    return izdaja_spremeniti_velikost;
}
int 꾸러미읽기(const char *Ime, unsigned char *KR_podatki, unsigned medpomnilnik_zmogljivost) {
    if(!항목들)return -2;unsigned element_COUNT=길이(Ime),sprotno_položaj=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(sprotno_položaj+28);
        if(이름길이==element_COUNT && 같음(Arhiv+sprotno_položaj+46,(const unsigned char*)Ime,element_COUNT))return član(sprotno_položaj,KR_podatki,medpomnilnik_zmogljivost);
        sprotno_položaj+=46+이름길이+두바이트읽기(sprotno_položaj+30)+두바이트읽기(sprotno_položaj+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return vnos_Razred; }
int 꾸러미열기(const char *Datoteka_vnos_ime) {
    항목들=0;vnos_Razred[0]=0;
    intptr_t Datoteka_ročica=사용자호출(3,(uintptr_t)Datoteka_vnos_ime,0,0,0,0,0);if(Datoteka_ročica<0)return Datoteka_ročica;
    intptr_t element_COUNT=사용자호출(9,Datoteka_ročica,0,0,0,0,0);
    if(element_COUNT<22 || element_COUNT>(intptr_t)sizeof(Arhiv)) { 사용자호출(4,Datoteka_ročica,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Datoteka_ročica,(uintptr_t)Arhiv,element_COUNT,0,0,0);사용자호출(4,Datoteka_ročica,0,0,0,0,0);
    if(RECEIVED_COUNT!=element_COUNT)return -5;Velikost=element_COUNT;
    unsigned končati_klic_odmik=Velikost-22;
    for(;;) { if(네바이트읽기(končati_klic_odmik)==0x06054b50 && končati_klic_odmik+22+두바이트읽기(končati_klic_odmik+20)==Velikost)break; if(!končati_klic_odmik)return -8;končati_klic_odmik--; }
    unsigned vnos_COUNT=두바이트읽기(končati_klic_odmik+10);중앙목록=네바이트읽기(končati_klic_odmik+16);
    if(두바이트읽기(končati_klic_odmik+4)||두바이트읽기(končati_klic_odmik+6)||두바이트읽기(končati_klic_odmik+8)!=vnos_COUNT||!vnos_COUNT||vnos_COUNT>256||!izrezek(중앙목록,네바이트읽기(končati_klic_odmik+12),končati_klic_odmik)||중앙목록+네바이트읽기(končati_klic_odmik+12)!=končati_klic_odmik)return -8;
    unsigned sprotno_položaj=중앙목록;
    for(unsigned 순번=0;순번<vnos_COUNT;순번++) {
        if(!izrezek(sprotno_položaj,46,končati_klic_odmik)||네바이트읽기(sprotno_položaj)!=0x02014b50||두바이트읽기(sprotno_položaj+34))return -8;
        unsigned 이름길이=두바이트읽기(sprotno_položaj+28),Naprej_element=46+이름길이+두바이트읽기(sprotno_položaj+30)+두바이트읽기(sprotno_položaj+32);
        if(!이름길이||이름길이>511||!izrezek(sprotno_položaj,Naprej_element,končati_klic_odmik)||네바이트읽기(sprotno_položaj+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhiv[sprotno_položaj+46+안쪽순번])return -8;
        unsigned Drugo_vnos=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(Drugo_vnos+28);if(길이값==이름길이&&같음(Arhiv+Drugo_vnos+46,Arhiv+sprotno_položaj+46,길이값))return -8;Drugo_vnos+=46+길이값+두바이트읽기(Drugo_vnos+30)+두바이트읽기(Drugo_vnos+32);}
        sprotno_položaj+=Naprej_element;
    }
    if(sprotno_položaj!=končati_klic_odmik)return -8;항목들=vnos_COUNT;
    unsigned char 꾸러미명세[4096];int Skupina_spremeniti_velikost=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Skupina_spremeniti_velikost<0){항목들=0;return -8;}
    꾸러미명세[Skupina_spremeniti_velikost]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Skupina_spremeniti_velikost) {
        unsigned Zaženi=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Skupina_spremeniti_velikost && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned 길이값=INDEX_VALUE-Zaženi;if(INDEX_VALUE<(unsigned)Skupina_spremeniti_velikost)INDEX_VALUE++;if(길이값 && 꾸러미명세[Zaženi+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[Zaženi]==' ') {Zaženi++;길이값--;}
        else {
            int REZULTAT=atribut_podatki(논리크기,사용량,&진입점있음);if(REZULTAT)return REZULTAT;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[Zaženi+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int REZULTAT=atribut_podatki(논리크기,사용량,&진입점있음);if(REZULTAT)return REZULTAT;
    return 진입점있음?0:-8;
}
