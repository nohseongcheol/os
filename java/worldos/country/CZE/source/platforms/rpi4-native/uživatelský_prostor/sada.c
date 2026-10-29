#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "sada.h"
#include "uzlib.h"
static unsigned char Archiv[16384], 풀린자료[16385];
static unsigned Velikost, 중앙목록, 항목들;
static char položka_Třída[256];
static unsigned 두바이트읽기(unsigned dobrá_pozice) { return Archiv[dobrá_pozice] | Archiv[dobrá_pozice+1] << 8; }
static uint32_t 네바이트읽기(unsigned dobrá_pozice) { return 두바이트읽기(dobrá_pozice) | (uint32_t)두바이트읽기(dobrá_pozice+2) << 16; }
static int oříznout(unsigned dobrá_pozice, unsigned zboží_POČET, unsigned 한도) { return dobrá_pozice <= 한도 && zboží_POČET <= 한도-dobrá_pozice; }
static size_t délka_HODNOTA(const char *řetězec_data) { size_t zboží_POČET=0; while(řetězec_data[zboží_POČET]) zboží_POČET++; return zboží_POČET; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEKUNDA_HODNOTA, unsigned zboží_POČET) { for(unsigned 순번=0;순번<zboží_POČET;순번++)if(첫째값[순번]!=SEKUNDA_HODNOTA[순번])return 0;return 1; }
static int Soubor_konec(void *미사용값) { (void)미사용값; return -1; }
static int atribut_data(const char *vstupní_řádek,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)vstupní_řádek,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)vstupní_řádek,(const unsigned char*)"Main-Class: ",12)) {
        unsigned HODNOTA=사용량-12;if(*진입점있음||!HODNOTA||HODNOTA>=sizeof(položka_Třída))return -8;
        for(unsigned 순번=0;순번<HODNOTA;순번++){unsigned char bod_kódu=vstupní_řádek[12+순번];if(bod_kódu<=32||bod_kódu=='/'||bod_kódu=='\\')return -8;položka_Třída[순번]=bod_kódu;}
        položka_Třída[HODNOTA]=0;*진입점있음=1;
    }
    return 0;
}
static int člen(unsigned dobrá_pozice, unsigned char *KV_data, unsigned 용량한도) {
    unsigned metoda_položka=두바이트읽기(dobrá_pozice+10), konfigurace_BITS=두바이트읽기(dobrá_pozice+8), 압축크기=네바이트읽기(dobrá_pozice+20), verze_změnit_velikost=네바이트읽기(dobrá_pozice+24), místní=네바이트읽기(dobrá_pozice+42);
    unsigned Název=두바이트읽기(dobrá_pozice+28);
    if(verze_změnit_velikost>용량한도 || verze_změnit_velikost>16384 || (metoda_položka!=0 && metoda_položka!=8) || (konfigurace_BITS&~0x80e))return -8;
    if(!oříznout(místní,30,중앙목록) || 네바이트읽기(místní)!=0x04034b50 || 두바이트읽기(místní+8)!=metoda_položka || 두바이트읽기(místní+6)!=konfigurace_BITS || 두바이트읽기(místní+26)!=Název)return -8;
    unsigned START_POSUN=místní+30, 추가영역=두바이트읽기(místní+28);
    if(!oříznout(START_POSUN,Název,중앙목록) || !같음(Archiv+START_POSUN,Archiv+dobrá_pozice+46,Název))return -8;
    START_POSUN+=Název;if(!oříznout(START_POSUN,추가영역,중앙목록))return -8;START_POSUN+=추가영역;
    if(!oříznout(START_POSUN,압축크기,중앙목록))return -8;
    if(!(konfigurace_BITS&8) && (네바이트읽기(místní+14)!=네바이트읽기(dobrá_pozice+16) || 네바이트읽기(místní+18)!=압축크기 || 네바이트읽기(místní+22)!=verze_změnit_velikost))return -8;
    if(metoda_položka==0) { if(압축크기!=verze_změnit_velikost)return -8; for(unsigned 순번=0;순번<verze_změnit_velikost;순번++)KV_data[순번]=Archiv[START_POSUN+순번]; }
    else {
        uzlib_uncomp_t cíl_data={0};uzlib_uncompress_init(&cíl_data,0,0);
        cíl_data.source=Archiv+START_POSUN;cíl_data.source_limit=cíl_data.source+압축크기;cíl_data.source_read_cb=Soubor_konec;
        /* One extra output byte lets inflate consume/check the end marker. */
        cíl_data.dest_start=cíl_data.dest=풀린자료;cíl_data.dest_limit=풀린자료+verze_změnit_velikost+1;
        int 반환값=uzlib_uncompress(&cíl_data);
        if(반환값!=UZLIB_DONE || cíl_data.eof || cíl_data.dest!=풀린자료+verze_změnit_velikost || cíl_data.source!=cíl_data.source_limit)return -8;
        for(unsigned 순번=0;순번<verze_změnit_velikost;순번++)KV_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KV_data,verze_změnit_velikost,0xffffffffu)^0xffffffffu)!=네바이트읽기(dobrá_pozice+16))return -8;
    return verze_změnit_velikost;
}
int 꾸러미읽기(const char *Název, unsigned char *KV_data, unsigned zásobník_kapacita) {
    if(!항목들)return -2;unsigned zboží_POČET=délka_HODNOTA(Název),dobrá_pozice=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(dobrá_pozice+28);
        if(이름길이==zboží_POČET && 같음(Archiv+dobrá_pozice+46,(const unsigned char*)Název,zboží_POČET))return člen(dobrá_pozice,KV_data,zásobník_kapacita);
        dobrá_pozice+=46+이름길이+두바이트읽기(dobrá_pozice+30)+두바이트읽기(dobrá_pozice+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return položka_Třída; }
int 꾸러미열기(const char *Soubor_položka_název) {
    항목들=0;položka_Třída[0]=0;
    intptr_t popisovač_souboru=사용자호출(3,(uintptr_t)Soubor_položka_název,0,0,0,0,0);if(popisovač_souboru<0)return popisovač_souboru;
    intptr_t zboží_POČET=사용자호출(9,popisovač_souboru,0,0,0,0,0);
    if(zboží_POČET<22 || zboží_POČET>(intptr_t)sizeof(Archiv)) { 사용자호출(4,popisovač_souboru,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_POČET=사용자호출(2,popisovač_souboru,(uintptr_t)Archiv,zboží_POČET,0,0,0);사용자호출(4,popisovač_souboru,0,0,0,0,0);
    if(RECEIVED_POČET!=zboží_POČET)return -5;Velikost=zboží_POČET;
    unsigned konec_POSUN=Velikost-22;
    for(;;) { if(네바이트읽기(konec_POSUN)==0x06054b50 && konec_POSUN+22+두바이트읽기(konec_POSUN+20)==Velikost)break; if(!konec_POSUN)return -8;konec_POSUN--; }
    unsigned položka_POČET=두바이트읽기(konec_POSUN+10);중앙목록=네바이트읽기(konec_POSUN+16);
    if(두바이트읽기(konec_POSUN+4)||두바이트읽기(konec_POSUN+6)||두바이트읽기(konec_POSUN+8)!=položka_POČET||!položka_POČET||položka_POČET>256||!oříznout(중앙목록,네바이트읽기(konec_POSUN+12),konec_POSUN)||중앙목록+네바이트읽기(konec_POSUN+12)!=konec_POSUN)return -8;
    unsigned dobrá_pozice=중앙목록;
    for(unsigned 순번=0;순번<položka_POČET;순번++) {
        if(!oříznout(dobrá_pozice,46,konec_POSUN)||네바이트읽기(dobrá_pozice)!=0x02014b50||두바이트읽기(dobrá_pozice+34))return -8;
        unsigned 이름길이=두바이트읽기(dobrá_pozice+28),Další_zboží=46+이름길이+두바이트읽기(dobrá_pozice+30)+두바이트읽기(dobrá_pozice+32);
        if(!이름길이||이름길이>511||!oříznout(dobrá_pozice,Další_zboží,konec_POSUN)||네바이트읽기(dobrá_pozice+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archiv[dobrá_pozice+46+안쪽순번])return -8;
        unsigned Jiný_položka=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned délka_data=두바이트읽기(Jiný_položka+28);if(délka_data==이름길이&&같음(Archiv+Jiný_položka+46,Archiv+dobrá_pozice+46,délka_data))return -8;Jiný_položka+=46+délka_data+두바이트읽기(Jiný_položka+30)+두바이트읽기(Jiný_položka+32);}
        dobrá_pozice+=Další_zboží;
    }
    if(dobrá_pozice!=konec_POSUN)return -8;항목들=položka_POČET;
    unsigned char sada_manifest[4096];int Skupina_změnit_velikost=꾸러미읽기("META-INF/MANIFEST.MF",sada_manifest,sizeof(sada_manifest)-1);if(Skupina_změnit_velikost<0){항목들=0;return -8;}
    sada_manifest[Skupina_změnit_velikost]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_HODNOTA=0;int 진입점있음=0;
    while(INDEX_HODNOTA<(unsigned)Skupina_změnit_velikost) {
        unsigned Spustit_2=INDEX_HODNOTA;while(INDEX_HODNOTA<(unsigned)Skupina_změnit_velikost && sada_manifest[INDEX_HODNOTA]!='\n')INDEX_HODNOTA++;
        unsigned délka_data=INDEX_HODNOTA-Spustit_2;if(INDEX_HODNOTA<(unsigned)Skupina_změnit_velikost)INDEX_HODNOTA++;if(délka_data && sada_manifest[Spustit_2+délka_data-1]=='\r')délka_data--;
        if(사용량 && délka_data && sada_manifest[Spustit_2]==' ') {Spustit_2++;délka_data--;}
        else {
            int VÝSLEDEK=atribut_data(논리크기,사용량,&진입점있음);if(VÝSLEDEK)return VÝSLEDEK;
            사용량=0;if(!délka_data)break;
        }
        if(délka_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<délka_data;순번++)논리크기[사용량++]=sada_manifest[Spustit_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int VÝSLEDEK=atribut_data(논리크기,사용량,&진입점있음);if(VÝSLEDEK)return VÝSLEDEK;
    return 진입점있음?0:-8;
}
