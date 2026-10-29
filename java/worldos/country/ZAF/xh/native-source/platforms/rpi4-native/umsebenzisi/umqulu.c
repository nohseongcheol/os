#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "umqulu.h"
#include "uzlib.h"
static unsigned char Uvimba[16384], 풀린자료[16385];
static unsigned Ubukhulu, 중앙목록, 항목들;
static char ufako_nkcukacha_iklasi[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Uvimba[현재위치] | Uvimba[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int ikliphu(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t ubude_ixabiso(const char *uluhlu_lweekharektha_iingcombolo) { size_t 개수=0; while(uluhlu_lweekharektha_iingcombolo[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int ifayile_phela(void *미사용값) { (void)미사용값; return -1; }
static int uphawu_iingcombolo(const char *umgca,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)umgca,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)umgca,(const unsigned char*)"Main-Class: ",12)) {
        unsigned ixabiso=사용량-12;if(*진입점있음||!ixabiso||ixabiso>=sizeof(ufako_nkcukacha_iklasi))return -8;
        for(unsigned 순번=0;순번<ixabiso;순번++){unsigned char ikhowudi_yekharakhtha=umgca[12+순번];if(ikhowudi_yekharakhtha<=32||ikhowudi_yekharakhtha=='/'||ikhowudi_yekharakhtha=='\\')return -8;ufako_nkcukacha_iklasi[순번]=ikhowudi_yekharakhtha;}
        ufako_nkcukacha_iklasi[ixabiso]=0;*진입점있음=1;
    }
    return 0;
}
static int ilungu(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned imethodi_ufako_nkcukacha=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), vulela_isayizi=네바이트읽기(현재위치+24), eyale_ndawo=네바이트읽기(현재위치+42);
    unsigned Igama=두바이트읽기(현재위치+28);
    if(vulela_isayizi>용량한도 || vulela_isayizi>16384 || (imethodi_ufako_nkcukacha!=0 && imethodi_ufako_nkcukacha!=8) || (설정비트&~0x80e))return -8;
    if(!ikliphu(eyale_ndawo,30,중앙목록) || 네바이트읽기(eyale_ndawo)!=0x04034b50 || 두바이트읽기(eyale_ndawo+8)!=imethodi_ufako_nkcukacha || 두바이트읽기(eyale_ndawo+6)!=설정비트 || 두바이트읽기(eyale_ndawo+26)!=Igama)return -8;
    unsigned qala_Ukulinganisa=eyale_ndawo+30, 추가영역=두바이트읽기(eyale_ndawo+28);
    if(!ikliphu(qala_Ukulinganisa,Igama,중앙목록) || !같음(Uvimba+qala_Ukulinganisa,Uvimba+현재위치+46,Igama))return -8;
    qala_Ukulinganisa+=Igama;if(!ikliphu(qala_Ukulinganisa,추가영역,중앙목록))return -8;qala_Ukulinganisa+=추가영역;
    if(!ikliphu(qala_Ukulinganisa,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(eyale_ndawo+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(eyale_ndawo+18)!=압축크기 || 네바이트읽기(eyale_ndawo+22)!=vulela_isayizi))return -8;
    if(imethodi_ufako_nkcukacha==0) { if(압축크기!=vulela_isayizi)return -8; for(unsigned 순번=0;순번<vulela_isayizi;순번++)결과자료[순번]=Uvimba[qala_Ukulinganisa+순번]; }
    else {
        uzlib_uncomp_t indawo_ekuyiwa_kuyo_iingcombolo={0};uzlib_uncompress_init(&indawo_ekuyiwa_kuyo_iingcombolo,0,0);
        indawo_ekuyiwa_kuyo_iingcombolo.source=Uvimba+qala_Ukulinganisa;indawo_ekuyiwa_kuyo_iingcombolo.source_limit=indawo_ekuyiwa_kuyo_iingcombolo.source+압축크기;indawo_ekuyiwa_kuyo_iingcombolo.source_read_cb=ifayile_phela;
        /* One extra output byte lets inflate consume/check the end marker. */
        indawo_ekuyiwa_kuyo_iingcombolo.dest_start=indawo_ekuyiwa_kuyo_iingcombolo.dest=풀린자료;indawo_ekuyiwa_kuyo_iingcombolo.dest_limit=풀린자료+vulela_isayizi+1;
        int 반환값=uzlib_uncompress(&indawo_ekuyiwa_kuyo_iingcombolo);
        if(반환값!=UZLIB_DONE || indawo_ekuyiwa_kuyo_iingcombolo.eof || indawo_ekuyiwa_kuyo_iingcombolo.dest!=풀린자료+vulela_isayizi || indawo_ekuyiwa_kuyo_iingcombolo.source!=indawo_ekuyiwa_kuyo_iingcombolo.source_limit)return -8;
        for(unsigned 순번=0;순번<vulela_isayizi;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,vulela_isayizi,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return vulela_isayizi;
}
int 꾸러미읽기(const char *Igama, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=ubude_ixabiso(Igama),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(Uvimba+현재위치+46,(const unsigned char*)Igama,개수))return ilungu(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ufako_nkcukacha_iklasi; }
int 꾸러미열기(const char *ifayile_ufako_nkcukacha_igama) {
    항목들=0;ufako_nkcukacha_iklasi[0]=0;
    intptr_t ifayile_isibambi=사용자호출(3,(uintptr_t)ifayile_ufako_nkcukacha_igama,0,0,0,0,0);if(ifayile_isibambi<0)return ifayile_isibambi;
    intptr_t 개수=사용자호출(9,ifayile_isibambi,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(Uvimba)) { 사용자호출(4,ifayile_isibambi,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,ifayile_isibambi,(uintptr_t)Uvimba,개수,0,0,0);사용자호출(4,ifayile_isibambi,0,0,0,0,0);
    if(받은수!=개수)return -5;Ubukhulu=개수;
    unsigned phela_Ukulinganisa=Ubukhulu-22;
    for(;;) { if(네바이트읽기(phela_Ukulinganisa)==0x06054b50 && phela_Ukulinganisa+22+두바이트읽기(phela_Ukulinganisa+20)==Ubukhulu)break; if(!phela_Ukulinganisa)return -8;phela_Ukulinganisa--; }
    unsigned 항목수=두바이트읽기(phela_Ukulinganisa+10);중앙목록=네바이트읽기(phela_Ukulinganisa+16);
    if(두바이트읽기(phela_Ukulinganisa+4)||두바이트읽기(phela_Ukulinganisa+6)||두바이트읽기(phela_Ukulinganisa+8)!=항목수||!항목수||항목수>256||!ikliphu(중앙목록,네바이트읽기(phela_Ukulinganisa+12),phela_Ukulinganisa)||중앙목록+네바이트읽기(phela_Ukulinganisa+12)!=phela_Ukulinganisa)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!ikliphu(현재위치,46,phela_Ukulinganisa)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!ikliphu(현재위치,다음,phela_Ukulinganisa)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Uvimba[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned ubude_iingcombolo=두바이트읽기(다른항목+28);if(ubude_iingcombolo==이름길이&&같음(Uvimba+다른항목+46,Uvimba+현재위치+46,ubude_iingcombolo))return -8;다른항목+=46+ubude_iingcombolo+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=phela_Ukulinganisa)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int iqela_isayizi=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(iqela_isayizi<0){항목들=0;return -8;}
    꾸러미명세[iqela_isayizi]=0;
    char 논리크기[512];unsigned 사용량=0,indeksa_ixabiso=0;int 진입점있음=0;
    while(indeksa_ixabiso<(unsigned)iqela_isayizi) {
        unsigned Phumeza=indeksa_ixabiso;while(indeksa_ixabiso<(unsigned)iqela_isayizi && 꾸러미명세[indeksa_ixabiso]!='\n')indeksa_ixabiso++;
        unsigned ubude_iingcombolo=indeksa_ixabiso-Phumeza;if(indeksa_ixabiso<(unsigned)iqela_isayizi)indeksa_ixabiso++;if(ubude_iingcombolo && 꾸러미명세[Phumeza+ubude_iingcombolo-1]=='\r')ubude_iingcombolo--;
        if(사용량 && ubude_iingcombolo && 꾸러미명세[Phumeza]==' ') {Phumeza++;ubude_iingcombolo--;}
        else {
            int 결과=uphawu_iingcombolo(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!ubude_iingcombolo)break;
        }
        if(ubude_iingcombolo>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<ubude_iingcombolo;순번++)논리크기[사용량++]=꾸러미명세[Phumeza+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=uphawu_iingcombolo(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
