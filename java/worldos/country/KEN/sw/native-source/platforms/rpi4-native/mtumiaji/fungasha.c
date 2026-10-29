#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "fungasha.h"
#include "uzlib.h"
static unsigned char Hifadhi_eb6be19d[16384], 풀린자료[16385];
static unsigned panga_ukubwa, 중앙목록, 항목들;
static char ingizo_tabaka[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Hifadhi_eb6be19d[현재위치] | Hifadhi_eb6be19d[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int dondoo(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t urefu_thamani(const char *tungo_data) { size_t 개수=0; while(tungo_data[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int faili_tamatia(void *미사용값) { (void)미사용값; return -1; }
static int sifa_data(const char *laini,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)laini,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)laini,(const unsigned char*)"Main-Class: ",12)) {
        unsigned thamani=사용량-12;if(*진입점있음||!thamani||thamani>=sizeof(ingizo_tabaka))return -8;
        for(unsigned 순번=0;순번<thamani;순번++){unsigned char msimbo_wa_kibambo=laini[12+순번];if(msimbo_wa_kibambo<=32||msimbo_wa_kibambo=='/'||msimbo_wa_kibambo=='\\')return -8;ingizo_tabaka[순번]=msimbo_wa_kibambo;}
        ingizo_tabaka[thamani]=0;*진입점있음=1;
    }
    return 0;
}
static int mwanachama(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned mbinu_ingizo=두바이트읽기(현재위치+10), usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), toleo_panga_ukubwa=네바이트읽기(현재위치+24), jirani=네바이트읽기(현재위치+42);
    unsigned Jina=두바이트읽기(현재위치+28);
    if(toleo_panga_ukubwa>용량한도 || toleo_panga_ukubwa>16384 || (mbinu_ingizo!=0 && mbinu_ingizo!=8) || (usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&~0x80e))return -8;
    if(!dondoo(jirani,30,중앙목록) || 네바이트읽기(jirani)!=0x04034b50 || 두바이트읽기(jirani+8)!=mbinu_ingizo || 두바이트읽기(jirani+6)!=usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma || 두바이트읽기(jirani+26)!=Jina)return -8;
    unsigned Anza_Chipua=jirani+30, 추가영역=두바이트읽기(jirani+28);
    if(!dondoo(Anza_Chipua,Jina,중앙목록) || !같음(Hifadhi_eb6be19d+Anza_Chipua,Hifadhi_eb6be19d+현재위치+46,Jina))return -8;
    Anza_Chipua+=Jina;if(!dondoo(Anza_Chipua,추가영역,중앙목록))return -8;Anza_Chipua+=추가영역;
    if(!dondoo(Anza_Chipua,압축크기,중앙목록))return -8;
    if(!(usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&8) && (네바이트읽기(jirani+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(jirani+18)!=압축크기 || 네바이트읽기(jirani+22)!=toleo_panga_ukubwa))return -8;
    if(mbinu_ingizo==0) { if(압축크기!=toleo_panga_ukubwa)return -8; for(unsigned 순번=0;순번<toleo_panga_ukubwa;순번++)결과자료[순번]=Hifadhi_eb6be19d[Anza_Chipua+순번]; }
    else {
        uzlib_uncomp_t fikio_data={0};uzlib_uncompress_init(&fikio_data,0,0);
        fikio_data.source=Hifadhi_eb6be19d+Anza_Chipua;fikio_data.source_limit=fikio_data.source+압축크기;fikio_data.source_read_cb=faili_tamatia;
        /* One extra output byte lets inflate consume/check the end marker. */
        fikio_data.dest_start=fikio_data.dest=풀린자료;fikio_data.dest_limit=풀린자료+toleo_panga_ukubwa+1;
        int 반환값=uzlib_uncompress(&fikio_data);
        if(반환값!=UZLIB_DONE || fikio_data.eof || fikio_data.dest!=풀린자료+toleo_panga_ukubwa || fikio_data.source!=fikio_data.source_limit)return -8;
        for(unsigned 순번=0;순번<toleo_panga_ukubwa;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,toleo_panga_ukubwa,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return toleo_panga_ukubwa;
}
int 꾸러미읽기(const char *Jina, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=urefu_thamani(Jina),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(Hifadhi_eb6be19d+현재위치+46,(const unsigned char*)Jina,개수))return mwanachama(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ingizo_tabaka; }
int 꾸러미열기(const char *faili_ingizo_jina) {
    항목들=0;ingizo_tabaka[0]=0;
    intptr_t faili_kishiko=사용자호출(3,(uintptr_t)faili_ingizo_jina,0,0,0,0,0);if(faili_kishiko<0)return faili_kishiko;
    intptr_t 개수=사용자호출(9,faili_kishiko,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(Hifadhi_eb6be19d)) { 사용자호출(4,faili_kishiko,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,faili_kishiko,(uintptr_t)Hifadhi_eb6be19d,개수,0,0,0);사용자호출(4,faili_kishiko,0,0,0,0,0);
    if(받은수!=개수)return -5;panga_ukubwa=개수;
    unsigned tamatia_Chipua=panga_ukubwa-22;
    for(;;) { if(네바이트읽기(tamatia_Chipua)==0x06054b50 && tamatia_Chipua+22+두바이트읽기(tamatia_Chipua+20)==panga_ukubwa)break; if(!tamatia_Chipua)return -8;tamatia_Chipua--; }
    unsigned 항목수=두바이트읽기(tamatia_Chipua+10);중앙목록=네바이트읽기(tamatia_Chipua+16);
    if(두바이트읽기(tamatia_Chipua+4)||두바이트읽기(tamatia_Chipua+6)||두바이트읽기(tamatia_Chipua+8)!=항목수||!항목수||항목수>256||!dondoo(중앙목록,네바이트읽기(tamatia_Chipua+12),tamatia_Chipua)||중앙목록+네바이트읽기(tamatia_Chipua+12)!=tamatia_Chipua)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!dondoo(현재위치,46,tamatia_Chipua)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!dondoo(현재위치,다음,tamatia_Chipua)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Hifadhi_eb6be19d[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned urefu_data=두바이트읽기(다른항목+28);if(urefu_data==이름길이&&같음(Hifadhi_eb6be19d+다른항목+46,Hifadhi_eb6be19d+현재위치+46,urefu_data))return -8;다른항목+=46+urefu_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=tamatia_Chipua)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int Kikundi_panga_ukubwa=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Kikundi_panga_ukubwa<0){항목들=0;return -8;}
    꾸러미명세[Kikundi_panga_ukubwa]=0;
    char 논리크기[512];unsigned 사용량=0,kielezo_thamani=0;int 진입점있음=0;
    while(kielezo_thamani<(unsigned)Kikundi_panga_ukubwa) {
        unsigned endesha=kielezo_thamani;while(kielezo_thamani<(unsigned)Kikundi_panga_ukubwa && 꾸러미명세[kielezo_thamani]!='\n')kielezo_thamani++;
        unsigned urefu_data=kielezo_thamani-endesha;if(kielezo_thamani<(unsigned)Kikundi_panga_ukubwa)kielezo_thamani++;if(urefu_data && 꾸러미명세[endesha+urefu_data-1]=='\r')urefu_data--;
        if(사용량 && urefu_data && 꾸러미명세[endesha]==' ') {endesha++;urefu_data--;}
        else {
            int 결과=sifa_data(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!urefu_data)break;
        }
        if(urefu_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<urefu_data;순번++)논리크기[사용량++]=꾸러미명세[endesha+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=sifa_data(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
