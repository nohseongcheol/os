#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "Bëndel.h"
#include "uzlib.h"
static unsigned char Archiv[16384], 풀린자료[16385];
static unsigned d_Gréisst_veränneren, 중앙목록, 항목들;
static char Agab_Klass[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Archiv[현재위치] | Archiv[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int Clip(unsigned 현재위치, unsigned Element_COUNT, unsigned 한도) { return 현재위치 <= 한도 && Element_COUNT <= 한도-현재위치; }
static size_t Längt_VALUE(const char *Zeechefolleg_Daten) { size_t Element_COUNT=0; while(Zeechefolleg_Daten[Element_COUNT]) Element_COUNT++; return Element_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned Element_COUNT) { for(unsigned 순번=0;순번<Element_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int Fichier_bëennegen(void *미사용값) { (void)미사용값; return -1; }
static int Attribut_Daten(const char *Zeil,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Zeil,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Zeil,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(Agab_Klass))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char Zeechecode=Zeil[12+순번];if(Zeechecode<=32||Zeechecode=='/'||Zeechecode=='\\')return -8;Agab_Klass[순번]=Zeechecode;}
        Agab_Klass[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int Member(unsigned 현재위치, unsigned char *Mooss_Daten, unsigned 용량한도) {
    unsigned Method_Agab=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), Versioun_d_Gréisst_veränneren=네바이트읽기(현재위치+24), lokal=네바이트읽기(현재위치+42);
    unsigned Numm=두바이트읽기(현재위치+28);
    if(Versioun_d_Gréisst_veränneren>용량한도 || Versioun_d_Gréisst_veränneren>16384 || (Method_Agab!=0 && Method_Agab!=8) || (설정비트&~0x80e))return -8;
    if(!Clip(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=Method_Agab || 두바이트읽기(lokal+6)!=설정비트 || 두바이트읽기(lokal+26)!=Numm)return -8;
    unsigned Start_OFFSET=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!Clip(Start_OFFSET,Numm,중앙목록) || !같음(Archiv+Start_OFFSET,Archiv+현재위치+46,Numm))return -8;
    Start_OFFSET+=Numm;if(!Clip(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!Clip(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(lokal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=Versioun_d_Gréisst_veränneren))return -8;
    if(Method_Agab==0) { if(압축크기!=Versioun_d_Gréisst_veränneren)return -8; for(unsigned 순번=0;순번<Versioun_d_Gréisst_veränneren;순번++)Mooss_Daten[순번]=Archiv[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t Zil_Daten={0};uzlib_uncompress_init(&Zil_Daten,0,0);
        Zil_Daten.source=Archiv+Start_OFFSET;Zil_Daten.source_limit=Zil_Daten.source+압축크기;Zil_Daten.source_read_cb=Fichier_bëennegen;
        /* One extra output byte lets inflate consume/check the end marker. */
        Zil_Daten.dest_start=Zil_Daten.dest=풀린자료;Zil_Daten.dest_limit=풀린자료+Versioun_d_Gréisst_veränneren+1;
        int 반환값=uzlib_uncompress(&Zil_Daten);
        if(반환값!=UZLIB_DONE || Zil_Daten.eof || Zil_Daten.dest!=풀린자료+Versioun_d_Gréisst_veränneren || Zil_Daten.source!=Zil_Daten.source_limit)return -8;
        for(unsigned 순번=0;순번<Versioun_d_Gréisst_veränneren;순번++)Mooss_Daten[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(Mooss_Daten,Versioun_d_Gréisst_veränneren,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return Versioun_d_Gréisst_veränneren;
}
int 꾸러미읽기(const char *Numm, unsigned char *Mooss_Daten, unsigned 수용량) {
    if(!항목들)return -2;unsigned Element_COUNT=Längt_VALUE(Numm),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==Element_COUNT && 같음(Archiv+현재위치+46,(const unsigned char*)Numm,Element_COUNT))return Member(현재위치,Mooss_Daten,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return Agab_Klass; }
int 꾸러미열기(const char *Fichier_Agab_Numm) {
    항목들=0;Agab_Klass[0]=0;
    intptr_t Fichier_Handle=사용자호출(3,(uintptr_t)Fichier_Agab_Numm,0,0,0,0,0);if(Fichier_Handle<0)return Fichier_Handle;
    intptr_t Element_COUNT=사용자호출(9,Fichier_Handle,0,0,0,0,0);
    if(Element_COUNT<22 || Element_COUNT>(intptr_t)sizeof(Archiv)) { 사용자호출(4,Fichier_Handle,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,Fichier_Handle,(uintptr_t)Archiv,Element_COUNT,0,0,0);사용자호출(4,Fichier_Handle,0,0,0,0,0);
    if(RECEIVED_COUNT!=Element_COUNT)return -5;d_Gréisst_veränneren=Element_COUNT;
    unsigned bëennegen_OFFSET=d_Gréisst_veränneren-22;
    for(;;) { if(네바이트읽기(bëennegen_OFFSET)==0x06054b50 && bëennegen_OFFSET+22+두바이트읽기(bëennegen_OFFSET+20)==d_Gréisst_veränneren)break; if(!bëennegen_OFFSET)return -8;bëennegen_OFFSET--; }
    unsigned Agab_COUNT=두바이트읽기(bëennegen_OFFSET+10);중앙목록=네바이트읽기(bëennegen_OFFSET+16);
    if(두바이트읽기(bëennegen_OFFSET+4)||두바이트읽기(bëennegen_OFFSET+6)||두바이트읽기(bëennegen_OFFSET+8)!=Agab_COUNT||!Agab_COUNT||Agab_COUNT>256||!Clip(중앙목록,네바이트읽기(bëennegen_OFFSET+12),bëennegen_OFFSET)||중앙목록+네바이트읽기(bëennegen_OFFSET+12)!=bëennegen_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<Agab_COUNT;순번++) {
        if(!Clip(현재위치,46,bëennegen_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Weider_Element=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!Clip(현재위치,Weider_Element,bëennegen_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Archiv[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned Längt_Daten=두바이트읽기(다른항목+28);if(Längt_Daten==이름길이&&같음(Archiv+다른항목+46,Archiv+현재위치+46,Längt_Daten))return -8;다른항목+=46+Längt_Daten+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Weider_Element;
    }
    if(현재위치!=bëennegen_OFFSET)return -8;항목들=Agab_COUNT;
    unsigned char 꾸러미명세[4096];int Grupp_d_Gréisst_veränneren=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grupp_d_Gréisst_veränneren<0){항목들=0;return -8;}
    꾸러미명세[Grupp_d_Gréisst_veränneren]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grupp_d_Gréisst_veränneren) {
        unsigned Laf=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grupp_d_Gréisst_veränneren && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned Längt_Daten=INDEX_VALUE-Laf;if(INDEX_VALUE<(unsigned)Grupp_d_Gréisst_veränneren)INDEX_VALUE++;if(Längt_Daten && 꾸러미명세[Laf+Längt_Daten-1]=='\r')Längt_Daten--;
        if(사용량 && Längt_Daten && 꾸러미명세[Laf]==' ') {Laf++;Längt_Daten--;}
        else {
            int Mooss=Attribut_Daten(논리크기,사용량,&진입점있음);if(Mooss)return Mooss;
            사용량=0;if(!Längt_Daten)break;
        }
        if(Längt_Daten>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<Längt_Daten;순번++)논리크기[사용량++]=꾸러미명세[Laf+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int Mooss=Attribut_Daten(논리크기,사용량,&진입점있음);if(Mooss)return Mooss;
    return 진입점있음?0:-8;
}
