#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "bundt.h"
#include "uzlib.h"
static unsigned char Arkiv[16384], 풀린자료[16385];
static unsigned Størrelse, 중앙목록, 항목들;
static char post_Hold[256];
static unsigned 두바이트읽기(unsigned aktuel_placere) { return Arkiv[aktuel_placere] | Arkiv[aktuel_placere+1] << 8; }
static uint32_t 네바이트읽기(unsigned aktuel_placere) { return 두바이트읽기(aktuel_placere) | (uint32_t)두바이트읽기(aktuel_placere+2) << 16; }
static int klippe(unsigned aktuel_placere, unsigned vare_TÆL, unsigned 한도) { return aktuel_placere <= 한도 && vare_TÆL <= 한도-aktuel_placere; }
static size_t varighed_VÆRDI(const char *streng_data) { size_t vare_TÆL=0; while(streng_data[vare_TÆL]) vare_TÆL++; return vare_TÆL; }
static int 같음(const unsigned char *첫째값, const unsigned char *SEKUND_VÆRDI, unsigned vare_TÆL) { for(unsigned 순번=0;순번<vare_TÆL;순번++)if(첫째값[순번]!=SEKUND_VÆRDI[순번])return 0;return 1; }
static int fil_afslutte_et_opkald(void *미사용값) { (void)미사용값; return -1; }
static int attribut_data(const char *Linje,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Linje,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Linje,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VÆRDI=사용량-12;if(*진입점있음||!VÆRDI||VÆRDI>=sizeof(post_Hold))return -8;
        for(unsigned 순번=0;순번<VÆRDI;순번++){unsigned char tegnkode=Linje[12+순번];if(tegnkode<=32||tegnkode=='/'||tegnkode=='\\')return -8;post_Hold[순번]=tegnkode;}
        post_Hold[VÆRDI]=0;*진입점있음=1;
    }
    return 0;
}
static int medlem(unsigned aktuel_placere, unsigned char *KR_data, unsigned 용량한도) {
    unsigned metode_post=두바이트읽기(aktuel_placere+10), konfiguration_BITS=두바이트읽기(aktuel_placere+8), 압축크기=네바이트읽기(aktuel_placere+20), udgive_tilpasse_størrelse=네바이트읽기(aktuel_placere+24), lokal=네바이트읽기(aktuel_placere+42);
    unsigned Navn=두바이트읽기(aktuel_placere+28);
    if(udgive_tilpasse_størrelse>용량한도 || udgive_tilpasse_størrelse>16384 || (metode_post!=0 && metode_post!=8) || (konfiguration_BITS&~0x80e))return -8;
    if(!klippe(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metode_post || 두바이트읽기(lokal+6)!=konfiguration_BITS || 두바이트읽기(lokal+26)!=Navn)return -8;
    unsigned START_FORSKYDNING=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klippe(START_FORSKYDNING,Navn,중앙목록) || !같음(Arkiv+START_FORSKYDNING,Arkiv+aktuel_placere+46,Navn))return -8;
    START_FORSKYDNING+=Navn;if(!klippe(START_FORSKYDNING,추가영역,중앙목록))return -8;START_FORSKYDNING+=추가영역;
    if(!klippe(START_FORSKYDNING,압축크기,중앙목록))return -8;
    if(!(konfiguration_BITS&8) && (네바이트읽기(lokal+14)!=네바이트읽기(aktuel_placere+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=udgive_tilpasse_størrelse))return -8;
    if(metode_post==0) { if(압축크기!=udgive_tilpasse_størrelse)return -8; for(unsigned 순번=0;순번<udgive_tilpasse_størrelse;순번++)KR_data[순번]=Arkiv[START_FORSKYDNING+순번]; }
    else {
        uzlib_uncomp_t destination_data={0};uzlib_uncompress_init(&destination_data,0,0);
        destination_data.source=Arkiv+START_FORSKYDNING;destination_data.source_limit=destination_data.source+압축크기;destination_data.source_read_cb=fil_afslutte_et_opkald;
        /* One extra output byte lets inflate consume/check the end marker. */
        destination_data.dest_start=destination_data.dest=풀린자료;destination_data.dest_limit=풀린자료+udgive_tilpasse_størrelse+1;
        int 반환값=uzlib_uncompress(&destination_data);
        if(반환값!=UZLIB_DONE || destination_data.eof || destination_data.dest!=풀린자료+udgive_tilpasse_størrelse || destination_data.source!=destination_data.source_limit)return -8;
        for(unsigned 순번=0;순번<udgive_tilpasse_størrelse;순번++)KR_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_data,udgive_tilpasse_størrelse,0xffffffffu)^0xffffffffu)!=네바이트읽기(aktuel_placere+16))return -8;
    return udgive_tilpasse_størrelse;
}
int 꾸러미읽기(const char *Navn, unsigned char *KR_data, unsigned buffer_kapacitet) {
    if(!항목들)return -2;unsigned vare_TÆL=varighed_VÆRDI(Navn),aktuel_placere=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(aktuel_placere+28);
        if(이름길이==vare_TÆL && 같음(Arkiv+aktuel_placere+46,(const unsigned char*)Navn,vare_TÆL))return medlem(aktuel_placere,KR_data,buffer_kapacitet);
        aktuel_placere+=46+이름길이+두바이트읽기(aktuel_placere+30)+두바이트읽기(aktuel_placere+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return post_Hold; }
int 꾸러미열기(const char *fil_post_navn) {
    항목들=0;post_Hold[0]=0;
    intptr_t fil_handle=사용자호출(3,(uintptr_t)fil_post_navn,0,0,0,0,0);if(fil_handle<0)return fil_handle;
    intptr_t vare_TÆL=사용자호출(9,fil_handle,0,0,0,0,0);
    if(vare_TÆL<22 || vare_TÆL>(intptr_t)sizeof(Arkiv)) { 사용자호출(4,fil_handle,0,0,0,0,0);return -8; }
    intptr_t MODTAGET_VED_UDLØB_TÆL=사용자호출(2,fil_handle,(uintptr_t)Arkiv,vare_TÆL,0,0,0);사용자호출(4,fil_handle,0,0,0,0,0);
    if(MODTAGET_VED_UDLØB_TÆL!=vare_TÆL)return -5;Størrelse=vare_TÆL;
    unsigned afslutte_et_opkald_FORSKYDNING=Størrelse-22;
    for(;;) { if(네바이트읽기(afslutte_et_opkald_FORSKYDNING)==0x06054b50 && afslutte_et_opkald_FORSKYDNING+22+두바이트읽기(afslutte_et_opkald_FORSKYDNING+20)==Størrelse)break; if(!afslutte_et_opkald_FORSKYDNING)return -8;afslutte_et_opkald_FORSKYDNING--; }
    unsigned post_TÆL_8f7753a1=두바이트읽기(afslutte_et_opkald_FORSKYDNING+10);중앙목록=네바이트읽기(afslutte_et_opkald_FORSKYDNING+16);
    if(두바이트읽기(afslutte_et_opkald_FORSKYDNING+4)||두바이트읽기(afslutte_et_opkald_FORSKYDNING+6)||두바이트읽기(afslutte_et_opkald_FORSKYDNING+8)!=post_TÆL_8f7753a1||!post_TÆL_8f7753a1||post_TÆL_8f7753a1>256||!klippe(중앙목록,네바이트읽기(afslutte_et_opkald_FORSKYDNING+12),afslutte_et_opkald_FORSKYDNING)||중앙목록+네바이트읽기(afslutte_et_opkald_FORSKYDNING+12)!=afslutte_et_opkald_FORSKYDNING)return -8;
    unsigned aktuel_placere=중앙목록;
    for(unsigned 순번=0;순번<post_TÆL_8f7753a1;순번++) {
        if(!klippe(aktuel_placere,46,afslutte_et_opkald_FORSKYDNING)||네바이트읽기(aktuel_placere)!=0x02014b50||두바이트읽기(aktuel_placere+34))return -8;
        unsigned 이름길이=두바이트읽기(aktuel_placere+28),Næste_vare=46+이름길이+두바이트읽기(aktuel_placere+30)+두바이트읽기(aktuel_placere+32);
        if(!이름길이||이름길이>511||!klippe(aktuel_placere,Næste_vare,afslutte_et_opkald_FORSKYDNING)||네바이트읽기(aktuel_placere+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkiv[aktuel_placere+46+안쪽순번])return -8;
        unsigned Andet_post=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned varighed_data=두바이트읽기(Andet_post+28);if(varighed_data==이름길이&&같음(Arkiv+Andet_post+46,Arkiv+aktuel_placere+46,varighed_data))return -8;Andet_post+=46+varighed_data+두바이트읽기(Andet_post+30)+두바이트읽기(Andet_post+32);}
        aktuel_placere+=Næste_vare;
    }
    if(aktuel_placere!=afslutte_et_opkald_FORSKYDNING)return -8;항목들=post_TÆL_8f7753a1;
    unsigned char bundt_manifest[4096];int gruppe_tilpasse_størrelse=꾸러미읽기("META-INF/MANIFEST.MF",bundt_manifest,sizeof(bundt_manifest)-1);if(gruppe_tilpasse_størrelse<0){항목들=0;return -8;}
    bundt_manifest[gruppe_tilpasse_størrelse]=0;
    char 논리크기[512];unsigned 사용량=0,INDEKS_VÆRDI=0;int 진입점있음=0;
    while(INDEKS_VÆRDI<(unsigned)gruppe_tilpasse_størrelse) {
        unsigned Kør_2=INDEKS_VÆRDI;while(INDEKS_VÆRDI<(unsigned)gruppe_tilpasse_størrelse && bundt_manifest[INDEKS_VÆRDI]!='\n')INDEKS_VÆRDI++;
        unsigned varighed_data=INDEKS_VÆRDI-Kør_2;if(INDEKS_VÆRDI<(unsigned)gruppe_tilpasse_størrelse)INDEKS_VÆRDI++;if(varighed_data && bundt_manifest[Kør_2+varighed_data-1]=='\r')varighed_data--;
        if(사용량 && varighed_data && bundt_manifest[Kør_2]==' ') {Kør_2++;varighed_data--;}
        else {
            int KR=attribut_data(논리크기,사용량,&진입점있음);if(KR)return KR;
            사용량=0;if(!varighed_data)break;
        }
        if(varighed_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<varighed_data;순번++)논리크기[사용량++]=bundt_manifest[Kør_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int KR=attribut_data(논리크기,사용량,&진입점있음);if(KR)return KR;
    return 진입점있음?0:-8;
}
