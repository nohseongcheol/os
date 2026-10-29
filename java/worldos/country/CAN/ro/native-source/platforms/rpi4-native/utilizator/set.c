#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "set.h"
#include "uzlib.h"
static unsigned char Arhivă[16384], 풀린자료[16385];
static unsigned Mărime, 중앙목록, 항목들;
static char intrare_Clasă[256];
static unsigned 두바이트읽기(unsigned curent_poziție) { return Arhivă[curent_poziție] | Arhivă[curent_poziție+1] << 8; }
static uint32_t 네바이트읽기(unsigned curent_poziție) { return 두바이트읽기(curent_poziție) | (uint32_t)두바이트읽기(curent_poziție+2) << 16; }
static int clip(unsigned curent_poziție, unsigned element_COUNT, unsigned 한도) { return curent_poziție <= 한도 && element_COUNT <= 한도-curent_poziție; }
static size_t lungime_VALUE(const char *șir_date) { size_t element_COUNT=0; while(șir_date[element_COUNT]) element_COUNT++; return element_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned element_COUNT) { for(unsigned 순번=0;순번<element_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Fișier_termina_un_apel(void *미사용값) { (void)미사용값; return -1; }
static int atribut_date(const char *Linie,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Linie,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Linie,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(intrare_Clasă))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char cod_caracter=Linie[12+순번];if(cod_caracter<=32||cod_caracter=='/'||cod_caracter=='\\')return -8;intrare_Clasă[순번]=cod_caracter;}
        intrare_Clasă[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int membru(unsigned curent_poziție, unsigned char *KR_date, unsigned 용량한도) {
    unsigned metodă_intrare=두바이트읽기(curent_poziție+10), configurație_Serviciu_de_transfer_inteligent_în_fundal=두바이트읽기(curent_poziție+8), 압축크기=네바이트읽기(curent_poziție+20), lansa_dimensiona=네바이트읽기(curent_poziție+24), local=네바이트읽기(curent_poziție+42);
    unsigned Nume=두바이트읽기(curent_poziție+28);
    if(lansa_dimensiona>용량한도 || lansa_dimensiona>16384 || (metodă_intrare!=0 && metodă_intrare!=8) || (configurație_Serviciu_de_transfer_inteligent_în_fundal&~0x80e))return -8;
    if(!clip(local,30,중앙목록) || 네바이트읽기(local)!=0x04034b50 || 두바이트읽기(local+8)!=metodă_intrare || 두바이트읽기(local+6)!=configurație_Serviciu_de_transfer_inteligent_în_fundal || 두바이트읽기(local+26)!=Nume)return -8;
    unsigned buta_OFFSET=local+30, 추가영역=두바이트읽기(local+28);
    if(!clip(buta_OFFSET,Nume,중앙목록) || !같음(Arhivă+buta_OFFSET,Arhivă+curent_poziție+46,Nume))return -8;
    buta_OFFSET+=Nume;if(!clip(buta_OFFSET,추가영역,중앙목록))return -8;buta_OFFSET+=추가영역;
    if(!clip(buta_OFFSET,압축크기,중앙목록))return -8;
    if(!(configurație_Serviciu_de_transfer_inteligent_în_fundal&8) && (네바이트읽기(local+14)!=네바이트읽기(curent_poziție+16) || 네바이트읽기(local+18)!=압축크기 || 네바이트읽기(local+22)!=lansa_dimensiona))return -8;
    if(metodă_intrare==0) { if(압축크기!=lansa_dimensiona)return -8; for(unsigned 순번=0;순번<lansa_dimensiona;순번++)KR_date[순번]=Arhivă[buta_OFFSET+순번]; }
    else {
        uzlib_uncomp_t destinație_date={0};uzlib_uncompress_init(&destinație_date,0,0);
        destinație_date.source=Arhivă+buta_OFFSET;destinație_date.source_limit=destinație_date.source+압축크기;destinație_date.source_read_cb=Fișier_termina_un_apel;
        /* One extra output byte lets inflate consume/check the end marker. */
        destinație_date.dest_start=destinație_date.dest=풀린자료;destinație_date.dest_limit=풀린자료+lansa_dimensiona+1;
        int 반환값=uzlib_uncompress(&destinație_date);
        if(반환값!=UZLIB_DONE || destinație_date.eof || destinație_date.dest!=풀린자료+lansa_dimensiona || destinație_date.source!=destinație_date.source_limit)return -8;
        for(unsigned 순번=0;순번<lansa_dimensiona;순번++)KR_date[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_date,lansa_dimensiona,0xffffffffu)^0xffffffffu)!=네바이트읽기(curent_poziție+16))return -8;
    return lansa_dimensiona;
}
int 꾸러미읽기(const char *Nume, unsigned char *KR_date, unsigned tampon_capacitate) {
    if(!항목들)return -2;unsigned element_COUNT=lungime_VALUE(Nume),curent_poziție=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(curent_poziție+28);
        if(이름길이==element_COUNT && 같음(Arhivă+curent_poziție+46,(const unsigned char*)Nume,element_COUNT))return membru(curent_poziție,KR_date,tampon_capacitate);
        curent_poziție+=46+이름길이+두바이트읽기(curent_poziție+30)+두바이트읽기(curent_poziție+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return intrare_Clasă; }
int 꾸러미열기(const char *Fișier_intrare_nume) {
    항목들=0;intrare_Clasă[0]=0;
    intptr_t Fișier_handle=사용자호출(3,(uintptr_t)Fișier_intrare_nume,0,0,0,0,0);if(Fișier_handle<0)return Fișier_handle;
    intptr_t element_COUNT=사용자호출(9,Fișier_handle,0,0,0,0,0);
    if(element_COUNT<22 || element_COUNT>(intptr_t)sizeof(Arhivă)) { 사용자호출(4,Fișier_handle,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Fișier_handle,(uintptr_t)Arhivă,element_COUNT,0,0,0);사용자호출(4,Fișier_handle,0,0,0,0,0);
    if(RECEIVED_COUNT!=element_COUNT)return -5;Mărime=element_COUNT;
    unsigned termina_un_apel_OFFSET=Mărime-22;
    for(;;) { if(네바이트읽기(termina_un_apel_OFFSET)==0x06054b50 && termina_un_apel_OFFSET+22+두바이트읽기(termina_un_apel_OFFSET+20)==Mărime)break; if(!termina_un_apel_OFFSET)return -8;termina_un_apel_OFFSET--; }
    unsigned intrare_COUNT=두바이트읽기(termina_un_apel_OFFSET+10);중앙목록=네바이트읽기(termina_un_apel_OFFSET+16);
    if(두바이트읽기(termina_un_apel_OFFSET+4)||두바이트읽기(termina_un_apel_OFFSET+6)||두바이트읽기(termina_un_apel_OFFSET+8)!=intrare_COUNT||!intrare_COUNT||intrare_COUNT>256||!clip(중앙목록,네바이트읽기(termina_un_apel_OFFSET+12),termina_un_apel_OFFSET)||중앙목록+네바이트읽기(termina_un_apel_OFFSET+12)!=termina_un_apel_OFFSET)return -8;
    unsigned curent_poziție=중앙목록;
    for(unsigned 순번=0;순번<intrare_COUNT;순번++) {
        if(!clip(curent_poziție,46,termina_un_apel_OFFSET)||네바이트읽기(curent_poziție)!=0x02014b50||두바이트읽기(curent_poziție+34))return -8;
        unsigned 이름길이=두바이트읽기(curent_poziție+28),Următorul_element=46+이름길이+두바이트읽기(curent_poziție+30)+두바이트읽기(curent_poziție+32);
        if(!이름길이||이름길이>511||!clip(curent_poziție,Următorul_element,termina_un_apel_OFFSET)||네바이트읽기(curent_poziție+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arhivă[curent_poziție+46+안쪽순번])return -8;
        unsigned Altele_intrare=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned lungime_date=두바이트읽기(Altele_intrare+28);if(lungime_date==이름길이&&같음(Arhivă+Altele_intrare+46,Arhivă+curent_poziție+46,lungime_date))return -8;Altele_intrare+=46+lungime_date+두바이트읽기(Altele_intrare+30)+두바이트읽기(Altele_intrare+32);}
        curent_poziție+=Următorul_element;
    }
    if(curent_poziție!=termina_un_apel_OFFSET)return -8;항목들=intrare_COUNT;
    unsigned char 꾸러미명세[4096];int grup_dimensiona=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(grup_dimensiona<0){항목들=0;return -8;}
    꾸러미명세[grup_dimensiona]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)grup_dimensiona) {
        unsigned Pornește=INDEX_VALUE;while(INDEX_VALUE<(unsigned)grup_dimensiona && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned lungime_date=INDEX_VALUE-Pornește;if(INDEX_VALUE<(unsigned)grup_dimensiona)INDEX_VALUE++;if(lungime_date && 꾸러미명세[Pornește+lungime_date-1]=='\r')lungime_date--;
        if(사용량 && lungime_date && 꾸러미명세[Pornește]==' ') {Pornește++;lungime_date--;}
        else {
            int KR=atribut_date(논리크기,사용량,&진입점있음);if(KR)return KR;
            사용량=0;if(!lungime_date)break;
        }
        if(lungime_date>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<lungime_date;순번++)논리크기[사용량++]=꾸러미명세[Pornește+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int KR=atribut_date(논리크기,사용량,&진입점있음);if(KR)return KR;
    return 진입점있음?0:-8;
}
