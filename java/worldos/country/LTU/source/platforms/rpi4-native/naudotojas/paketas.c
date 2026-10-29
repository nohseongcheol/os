#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paketas.h"
#include "uzlib.h"
static unsigned char Archyvas[16384], 풀린자료[16385];
static unsigned Dydis, 중앙목록, 항목들;
static char įrašas_klasė[256];
static unsigned 두바이트읽기(unsigned dabartinis_padėtis) { return Archyvas[dabartinis_padėtis] | Archyvas[dabartinis_padėtis+1] << 8; }
static uint32_t 네바이트읽기(unsigned dabartinis_padėtis) { return 두바이트읽기(dabartinis_padėtis) | (uint32_t)두바이트읽기(dabartinis_padėtis+2) << 16; }
static int klipas(unsigned dabartinis_padėtis, unsigned prekė_COUNT, unsigned 한도) { return dabartinis_padėtis <= 한도 && prekė_COUNT <= 한도-dabartinis_padėtis; }
static size_t 길이(const char *eilutė_duomenys) { size_t prekė_COUNT=0; while(eilutė_duomenys[prekė_COUNT]) prekė_COUNT++; return prekė_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned prekė_COUNT) { for(unsigned 순번=0;순번<prekė_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Failas_baigti_pokalbį(void *미사용값) { (void)미사용값; return -1; }
static int atributas_duomenys(const char *Eilutė,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Eilutė,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Eilutė,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(įrašas_klasė))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char simbolio_kodas=Eilutė[12+순번];if(simbolio_kodas<=32||simbolio_kodas=='/'||simbolio_kodas=='\\')return -8;įrašas_klasė[순번]=simbolio_kodas;}
        įrašas_klasė[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int narys(unsigned dabartinis_padėtis, unsigned char *KR_duomenys, unsigned 용량한도) {
    unsigned metodas_įrašas=두바이트읽기(dabartinis_padėtis+10), konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba=두바이트읽기(dabartinis_padėtis+8), 압축크기=네바이트읽기(dabartinis_padėtis+20), išleisti_dydis=네바이트읽기(dabartinis_padėtis+24), vietinis=네바이트읽기(dabartinis_padėtis+42);
    unsigned Pavadinimas_2=두바이트읽기(dabartinis_padėtis+28);
    if(išleisti_dydis>용량한도 || išleisti_dydis>16384 || (metodas_įrašas!=0 && metodas_įrašas!=8) || (konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&~0x80e))return -8;
    if(!klipas(vietinis,30,중앙목록) || 네바이트읽기(vietinis)!=0x04034b50 || 두바이트읽기(vietinis+8)!=metodas_įrašas || 두바이트읽기(vietinis+6)!=konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba || 두바이트읽기(vietinis+26)!=Pavadinimas_2)return -8;
    unsigned Start_OFFSET=vietinis+30, 추가영역=두바이트읽기(vietinis+28);
    if(!klipas(Start_OFFSET,Pavadinimas_2,중앙목록) || !같음(Archyvas+Start_OFFSET,Archyvas+dabartinis_padėtis+46,Pavadinimas_2))return -8;
    Start_OFFSET+=Pavadinimas_2;if(!klipas(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!klipas(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&8) && (네바이트읽기(vietinis+14)!=네바이트읽기(dabartinis_padėtis+16) || 네바이트읽기(vietinis+18)!=압축크기 || 네바이트읽기(vietinis+22)!=išleisti_dydis))return -8;
    if(metodas_įrašas==0) { if(압축크기!=išleisti_dydis)return -8; for(unsigned 순번=0;순번<išleisti_dydis;순번++)KR_duomenys[순번]=Archyvas[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t vieta_duomenys={0};uzlib_uncompress_init(&vieta_duomenys,0,0);
        vieta_duomenys.source=Archyvas+Start_OFFSET;vieta_duomenys.source_limit=vieta_duomenys.source+압축크기;vieta_duomenys.source_read_cb=Failas_baigti_pokalbį;
        /* One extra output byte lets inflate consume/check the end marker. */
        vieta_duomenys.dest_start=vieta_duomenys.dest=풀린자료;vieta_duomenys.dest_limit=풀린자료+išleisti_dydis+1;
        int 반환값=uzlib_uncompress(&vieta_duomenys);
        if(반환값!=UZLIB_DONE || vieta_duomenys.eof || vieta_duomenys.dest!=풀린자료+išleisti_dydis || vieta_duomenys.source!=vieta_duomenys.source_limit)return -8;
        for(unsigned 순번=0;순번<išleisti_dydis;순번++)KR_duomenys[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_duomenys,išleisti_dydis,0xffffffffu)^0xffffffffu)!=네바이트읽기(dabartinis_padėtis+16))return -8;
    return išleisti_dydis;
}
int 꾸러미읽기(const char *Pavadinimas_2, unsigned char *KR_duomenys, unsigned kaupti_pajėgumas) {
    if(!항목들)return -2;unsigned prekė_COUNT=길이(Pavadinimas_2),dabartinis_padėtis=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(dabartinis_padėtis+28);
        if(이름길이==prekė_COUNT && 같음(Archyvas+dabartinis_padėtis+46,(const unsigned char*)Pavadinimas_2,prekė_COUNT))return narys(dabartinis_padėtis,KR_duomenys,kaupti_pajėgumas);
        dabartinis_padėtis+=46+이름길이+두바이트읽기(dabartinis_padėtis+30)+두바이트읽기(dabartinis_padėtis+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return įrašas_klasė; }
int 꾸러미열기(const char *Failas_įrašas_pavadinimas) {
    항목들=0;įrašas_klasė[0]=0;
    intptr_t Failas_rodyklė=사용자호출(3,(uintptr_t)Failas_įrašas_pavadinimas,0,0,0,0,0);if(Failas_rodyklė<0)return Failas_rodyklė;
    intptr_t prekė_COUNT=사용자호출(9,Failas_rodyklė,0,0,0,0,0);
    if(prekė_COUNT<22 || prekė_COUNT>(intptr_t)sizeof(Archyvas)) { 사용자호출(4,Failas_rodyklė,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Failas_rodyklė,(uintptr_t)Archyvas,prekė_COUNT,0,0,0);사용자호출(4,Failas_rodyklė,0,0,0,0,0);
    if(RECEIVED_COUNT!=prekė_COUNT)return -5;Dydis=prekė_COUNT;
    unsigned baigti_pokalbį_OFFSET=Dydis-22;
    for(;;) { if(네바이트읽기(baigti_pokalbį_OFFSET)==0x06054b50 && baigti_pokalbį_OFFSET+22+두바이트읽기(baigti_pokalbį_OFFSET+20)==Dydis)break; if(!baigti_pokalbį_OFFSET)return -8;baigti_pokalbį_OFFSET--; }
    unsigned įrašas_COUNT=두바이트읽기(baigti_pokalbį_OFFSET+10);중앙목록=네바이트읽기(baigti_pokalbį_OFFSET+16);
    if(두바이트읽기(baigti_pokalbį_OFFSET+4)||두바이트읽기(baigti_pokalbį_OFFSET+6)||두바이트읽기(baigti_pokalbį_OFFSET+8)!=įrašas_COUNT||!įrašas_COUNT||įrašas_COUNT>256||!klipas(중앙목록,네바이트읽기(baigti_pokalbį_OFFSET+12),baigti_pokalbį_OFFSET)||중앙목록+네바이트읽기(baigti_pokalbį_OFFSET+12)!=baigti_pokalbį_OFFSET)return -8;
    unsigned dabartinis_padėtis=중앙목록;
    for(unsigned 순번=0;순번<įrašas_COUNT;순번++) {
        if(!klipas(dabartinis_padėtis,46,baigti_pokalbį_OFFSET)||네바이트읽기(dabartinis_padėtis)!=0x02014b50||두바이트읽기(dabartinis_padėtis+34))return -8;
        unsigned 이름길이=두바이트읽기(dabartinis_padėtis+28),toliau_prekė=46+이름길이+두바이트읽기(dabartinis_padėtis+30)+두바이트읽기(dabartinis_padėtis+32);
        if(!이름길이||이름길이>511||!klipas(dabartinis_padėtis,toliau_prekė,baigti_pokalbį_OFFSET)||네바이트읽기(dabartinis_padėtis+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archyvas[dabartinis_padėtis+46+안쪽순번])return -8;
        unsigned Kita_įrašas=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned 길이값=두바이트읽기(Kita_įrašas+28);if(길이값==이름길이&&같음(Archyvas+Kita_įrašas+46,Archyvas+dabartinis_padėtis+46,길이값))return -8;Kita_įrašas+=46+길이값+두바이트읽기(Kita_įrašas+30)+두바이트읽기(Kita_įrašas+32);}
        dabartinis_padėtis+=toliau_prekė;
    }
    if(dabartinis_padėtis!=baigti_pokalbį_OFFSET)return -8;항목들=įrašas_COUNT;
    unsigned char 꾸러미명세[4096];int Grupė_dydis=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupė_dydis<0){항목들=0;return -8;}
    꾸러미명세[Grupė_dydis]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupė_dydis) {
        unsigned Paleisti=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupė_dydis && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned 길이값=INDEX_VALUE-Paleisti;if(INDEX_VALUE<(unsigned)Grupė_dydis)INDEX_VALUE++;if(길이값 && 꾸러미명세[Paleisti+길이값-1]=='\r')길이값--;
        if(사용량 && 길이값 && 꾸러미명세[Paleisti]==' ') {Paleisti++;길이값--;}
        else {
            int REZULTATAS=atributas_duomenys(논리크기,사용량,&진입점있음);if(REZULTATAS)return REZULTATAS;
            사용량=0;if(!길이값)break;
        }
        if(길이값>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<길이값;순번++)논리크기[사용량++]=꾸러미명세[Paleisti+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int REZULTATAS=atributas_duomenys(논리크기,사용량,&진입점있음);if(REZULTATAS)return REZULTATAS;
    return 진입점있음?0:-8;
}
