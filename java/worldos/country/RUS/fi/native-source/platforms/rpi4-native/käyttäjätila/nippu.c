#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "nippu.h"
#include "uzlib.h"
static unsigned char Arkisto[16384], 풀린자료[16385];
static unsigned Koko, 중앙목록, 항목들;
static char merkintä_Luokka[256];
static unsigned 두바이트읽기(unsigned nykyinen_toimi) { return Arkisto[nykyinen_toimi] | Arkisto[nykyinen_toimi+1] << 8; }
static uint32_t 네바이트읽기(unsigned nykyinen_toimi) { return 두바이트읽기(nykyinen_toimi) | (uint32_t)두바이트읽기(nykyinen_toimi+2) << 16; }
static int leikata(unsigned nykyinen_toimi, unsigned kohde_LASKE, unsigned 한도) { return nykyinen_toimi <= 한도 && kohde_LASKE <= 한도-nykyinen_toimi; }
static size_t kesto_ARVO(const char *merkkijono_data) { size_t kohde_LASKE=0; while(merkkijono_data[kohde_LASKE]) kohde_LASKE++; return kohde_LASKE; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEKUNNIT_ARVO, unsigned kohde_LASKE) { for(unsigned 순번=0;순번<kohde_LASKE;순번++)if(첫째값[순번]!=SEKUNNIT_ARVO[순번])return 0;return 1; }
static int Tiedosto_lopettaa_puhelu(void *미사용값) { (void)미사용값; return -1; }
static int määrite_data(const char *syöterivi,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)syöterivi,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)syöterivi,(const unsigned char*)"Main-Class: ",12)) {
        unsigned ARVO=사용량-12;if(*진입점있음||!ARVO||ARVO>=sizeof(merkintä_Luokka))return -8;
        for(unsigned 순번=0;순번<ARVO;순번++){unsigned char merkkikoodi=syöterivi[12+순번];if(merkkikoodi<=32||merkkikoodi=='/'||merkkikoodi=='\\')return -8;merkintä_Luokka[순번]=merkkikoodi;}
        merkintä_Luokka[ARVO]=0;*진입점있음=1;
    }
    return 0;
}
static int jäsen(unsigned nykyinen_toimi, unsigned char *KR_data, unsigned 용량한도) {
    unsigned menetelmä_merkintä=두바이트읽기(nykyinen_toimi+10), määritys_Background_Intelligent_Transfer_Service=두바이트읽기(nykyinen_toimi+8), 압축크기=네바이트읽기(nykyinen_toimi+20), julkaista_muuttaa_kokoa=네바이트읽기(nykyinen_toimi+24), paikallinen=네바이트읽기(nykyinen_toimi+42);
    unsigned Nimi=두바이트읽기(nykyinen_toimi+28);
    if(julkaista_muuttaa_kokoa>용량한도 || julkaista_muuttaa_kokoa>16384 || (menetelmä_merkintä!=0 && menetelmä_merkintä!=8) || (määritys_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!leikata(paikallinen,30,중앙목록) || 네바이트읽기(paikallinen)!=0x04034b50 || 두바이트읽기(paikallinen+8)!=menetelmä_merkintä || 두바이트읽기(paikallinen+6)!=määritys_Background_Intelligent_Transfer_Service || 두바이트읽기(paikallinen+26)!=Nimi)return -8;
    unsigned alku_SIIRTYMÄ=paikallinen+30, 추가영역=두바이트읽기(paikallinen+28);
    if(!leikata(alku_SIIRTYMÄ,Nimi,중앙목록) || !같음(Arkisto+alku_SIIRTYMÄ,Arkisto+nykyinen_toimi+46,Nimi))return -8;
    alku_SIIRTYMÄ+=Nimi;if(!leikata(alku_SIIRTYMÄ,추가영역,중앙목록))return -8;alku_SIIRTYMÄ+=추가영역;
    if(!leikata(alku_SIIRTYMÄ,압축크기,중앙목록))return -8;
    if(!(määritys_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(paikallinen+14)!=네바이트읽기(nykyinen_toimi+16) || 네바이트읽기(paikallinen+18)!=압축크기 || 네바이트읽기(paikallinen+22)!=julkaista_muuttaa_kokoa))return -8;
    if(menetelmä_merkintä==0) { if(압축크기!=julkaista_muuttaa_kokoa)return -8; for(unsigned 순번=0;순번<julkaista_muuttaa_kokoa;순번++)KR_data[순번]=Arkisto[alku_SIIRTYMÄ+순번]; }
    else {
        uzlib_uncomp_t kohde_data={0};uzlib_uncompress_init(&kohde_data,0,0);
        kohde_data.source=Arkisto+alku_SIIRTYMÄ;kohde_data.source_limit=kohde_data.source+압축크기;kohde_data.source_read_cb=Tiedosto_lopettaa_puhelu;
        /* One extra output byte lets inflate consume/check the end marker. */
        kohde_data.dest_start=kohde_data.dest=풀린자료;kohde_data.dest_limit=풀린자료+julkaista_muuttaa_kokoa+1;
        int 반환값=uzlib_uncompress(&kohde_data);
        if(반환값!=UZLIB_DONE || kohde_data.eof || kohde_data.dest!=풀린자료+julkaista_muuttaa_kokoa || kohde_data.source!=kohde_data.source_limit)return -8;
        for(unsigned 순번=0;순번<julkaista_muuttaa_kokoa;순번++)KR_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_data,julkaista_muuttaa_kokoa,0xffffffffu)^0xffffffffu)!=네바이트읽기(nykyinen_toimi+16))return -8;
    return julkaista_muuttaa_kokoa;
}
int 꾸러미읽기(const char *Nimi, unsigned char *KR_data, unsigned puskuri_kapasiteetti) {
    if(!항목들)return -2;unsigned kohde_LASKE=kesto_ARVO(Nimi),nykyinen_toimi=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(nykyinen_toimi+28);
        if(이름길이==kohde_LASKE && 같음(Arkisto+nykyinen_toimi+46,(const unsigned char*)Nimi,kohde_LASKE))return jäsen(nykyinen_toimi,KR_data,puskuri_kapasiteetti);
        nykyinen_toimi+=46+이름길이+두바이트읽기(nykyinen_toimi+30)+두바이트읽기(nykyinen_toimi+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return merkintä_Luokka; }
int 꾸러미열기(const char *Tiedosto_merkintä_nimi) {
    항목들=0;merkintä_Luokka[0]=0;
    intptr_t Tiedosto_kahva=사용자호출(3,(uintptr_t)Tiedosto_merkintä_nimi,0,0,0,0,0);if(Tiedosto_kahva<0)return Tiedosto_kahva;
    intptr_t kohde_LASKE=사용자호출(9,Tiedosto_kahva,0,0,0,0,0);
    if(kohde_LASKE<22 || kohde_LASKE>(intptr_t)sizeof(Arkisto)) { 사용자호출(4,Tiedosto_kahva,0,0,0,0,0);return -8; }
    intptr_t SAATU_HINTA_LASKE=사용자호출(2,Tiedosto_kahva,(uintptr_t)Arkisto,kohde_LASKE,0,0,0);사용자호출(4,Tiedosto_kahva,0,0,0,0,0);
    if(SAATU_HINTA_LASKE!=kohde_LASKE)return -5;Koko=kohde_LASKE;
    unsigned lopettaa_puhelu_SIIRTYMÄ=Koko-22;
    for(;;) { if(네바이트읽기(lopettaa_puhelu_SIIRTYMÄ)==0x06054b50 && lopettaa_puhelu_SIIRTYMÄ+22+두바이트읽기(lopettaa_puhelu_SIIRTYMÄ+20)==Koko)break; if(!lopettaa_puhelu_SIIRTYMÄ)return -8;lopettaa_puhelu_SIIRTYMÄ--; }
    unsigned merkintä_LASKE=두바이트읽기(lopettaa_puhelu_SIIRTYMÄ+10);중앙목록=네바이트읽기(lopettaa_puhelu_SIIRTYMÄ+16);
    if(두바이트읽기(lopettaa_puhelu_SIIRTYMÄ+4)||두바이트읽기(lopettaa_puhelu_SIIRTYMÄ+6)||두바이트읽기(lopettaa_puhelu_SIIRTYMÄ+8)!=merkintä_LASKE||!merkintä_LASKE||merkintä_LASKE>256||!leikata(중앙목록,네바이트읽기(lopettaa_puhelu_SIIRTYMÄ+12),lopettaa_puhelu_SIIRTYMÄ)||중앙목록+네바이트읽기(lopettaa_puhelu_SIIRTYMÄ+12)!=lopettaa_puhelu_SIIRTYMÄ)return -8;
    unsigned nykyinen_toimi=중앙목록;
    for(unsigned 순번=0;순번<merkintä_LASKE;순번++) {
        if(!leikata(nykyinen_toimi,46,lopettaa_puhelu_SIIRTYMÄ)||네바이트읽기(nykyinen_toimi)!=0x02014b50||두바이트읽기(nykyinen_toimi+34))return -8;
        unsigned 이름길이=두바이트읽기(nykyinen_toimi+28),Seuraava_kohde=46+이름길이+두바이트읽기(nykyinen_toimi+30)+두바이트읽기(nykyinen_toimi+32);
        if(!이름길이||이름길이>511||!leikata(nykyinen_toimi,Seuraava_kohde,lopettaa_puhelu_SIIRTYMÄ)||네바이트읽기(nykyinen_toimi+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkisto[nykyinen_toimi+46+안쪽순번])return -8;
        unsigned muut_merkintä=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned kesto_data=두바이트읽기(muut_merkintä+28);if(kesto_data==이름길이&&같음(Arkisto+muut_merkintä+46,Arkisto+nykyinen_toimi+46,kesto_data))return -8;muut_merkintä+=46+kesto_data+두바이트읽기(muut_merkintä+30)+두바이트읽기(muut_merkintä+32);}
        nykyinen_toimi+=Seuraava_kohde;
    }
    if(nykyinen_toimi!=lopettaa_puhelu_SIIRTYMÄ)return -8;항목들=merkintä_LASKE;
    unsigned char nippu_kokoonpanotiedot[4096];int Ryhmä_muuttaa_kokoa=꾸러미읽기("META-INF/MANIFEST.MF",nippu_kokoonpanotiedot,sizeof(nippu_kokoonpanotiedot)-1);if(Ryhmä_muuttaa_kokoa<0){항목들=0;return -8;}
    nippu_kokoonpanotiedot[Ryhmä_muuttaa_kokoa]=0;
    char 논리크기[512];unsigned 사용량=0,INDEKSI_ARVO=0;int 진입점있음=0;
    while(INDEKSI_ARVO<(unsigned)Ryhmä_muuttaa_kokoa) {
        unsigned Suorita_2=INDEKSI_ARVO;while(INDEKSI_ARVO<(unsigned)Ryhmä_muuttaa_kokoa && nippu_kokoonpanotiedot[INDEKSI_ARVO]!='\n')INDEKSI_ARVO++;
        unsigned kesto_data=INDEKSI_ARVO-Suorita_2;if(INDEKSI_ARVO<(unsigned)Ryhmä_muuttaa_kokoa)INDEKSI_ARVO++;if(kesto_data && nippu_kokoonpanotiedot[Suorita_2+kesto_data-1]=='\r')kesto_data--;
        if(사용량 && kesto_data && nippu_kokoonpanotiedot[Suorita_2]==' ') {Suorita_2++;kesto_data--;}
        else {
            int TULOS=määrite_data(논리크기,사용량,&진입점있음);if(TULOS)return TULOS;
            사용량=0;if(!kesto_data)break;
        }
        if(kesto_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<kesto_data;순번++)논리크기[사용량++]=nippu_kokoonpanotiedot[Suorita_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int TULOS=määrite_data(논리크기,사용량,&진입점있음);if(TULOS)return TULOS;
    return 진입점있음?0:-8;
}
