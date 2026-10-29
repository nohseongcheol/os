#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "to_plam.h"
#include "uzlib.h"
static unsigned char Arxiv[16384], 풀린자료[16385];
static unsigned Hajmi, 중앙목록, 항목들;
static char kiritish_Sinf[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Arxiv[현재위치] | Arxiv[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int klip(unsigned 현재위치, unsigned element_COUNT, unsigned 한도) { return 현재위치 <= 한도 && element_COUNT <= 한도-현재위치; }
static size_t uzunlik_VALUE(const char *satr_ma_lumotlar) { size_t element_COUNT=0; while(satr_ma_lumotlar[element_COUNT]) element_COUNT++; return element_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned element_COUNT) { for(unsigned 순번=0;순번<element_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int fayl_to_xtatmoq(void *미사용값) { (void)미사용값; return -1; }
static int xususiyat_ma_lumotlar(const char *satr,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)satr,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)satr,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(kiritish_Sinf))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char belgi_kodi=satr[12+순번];if(belgi_kodi<=32||belgi_kodi=='/'||belgi_kodi=='\\')return -8;kiritish_Sinf[순번]=belgi_kodi;}
        kiritish_Sinf[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int a_zo(unsigned 현재위치, unsigned char *o_lchov_ma_lumotlar, unsigned 용량한도) {
    unsigned uslub_kiritish=두바이트읽기(현재위치+10), tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), nashr_o_lcham=네바이트읽기(현재위치+24), mahalliy=네바이트읽기(현재위치+42);
    unsigned Nomi=두바이트읽기(현재위치+28);
    if(nashr_o_lcham>용량한도 || nashr_o_lcham>16384 || (uslub_kiritish!=0 && uslub_kiritish!=8) || (tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&~0x80e))return -8;
    if(!klip(mahalliy,30,중앙목록) || 네바이트읽기(mahalliy)!=0x04034b50 || 두바이트읽기(mahalliy+8)!=uslub_kiritish || 두바이트읽기(mahalliy+6)!=tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati || 두바이트읽기(mahalliy+26)!=Nomi)return -8;
    unsigned Start_OFFSET=mahalliy+30, 추가영역=두바이트읽기(mahalliy+28);
    if(!klip(Start_OFFSET,Nomi,중앙목록) || !같음(Arxiv+Start_OFFSET,Arxiv+현재위치+46,Nomi))return -8;
    Start_OFFSET+=Nomi;if(!klip(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!klip(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&8) && (네바이트읽기(mahalliy+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(mahalliy+18)!=압축크기 || 네바이트읽기(mahalliy+22)!=nashr_o_lcham))return -8;
    if(uslub_kiritish==0) { if(압축크기!=nashr_o_lcham)return -8; for(unsigned 순번=0;순번<nashr_o_lcham;순번++)o_lchov_ma_lumotlar[순번]=Arxiv[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t ko_chirish_joyi_ma_lumotlar={0};uzlib_uncompress_init(&ko_chirish_joyi_ma_lumotlar,0,0);
        ko_chirish_joyi_ma_lumotlar.source=Arxiv+Start_OFFSET;ko_chirish_joyi_ma_lumotlar.source_limit=ko_chirish_joyi_ma_lumotlar.source+압축크기;ko_chirish_joyi_ma_lumotlar.source_read_cb=fayl_to_xtatmoq;
        /* One extra output byte lets inflate consume/check the end marker. */
        ko_chirish_joyi_ma_lumotlar.dest_start=ko_chirish_joyi_ma_lumotlar.dest=풀린자료;ko_chirish_joyi_ma_lumotlar.dest_limit=풀린자료+nashr_o_lcham+1;
        int 반환값=uzlib_uncompress(&ko_chirish_joyi_ma_lumotlar);
        if(반환값!=UZLIB_DONE || ko_chirish_joyi_ma_lumotlar.eof || ko_chirish_joyi_ma_lumotlar.dest!=풀린자료+nashr_o_lcham || ko_chirish_joyi_ma_lumotlar.source!=ko_chirish_joyi_ma_lumotlar.source_limit)return -8;
        for(unsigned 순번=0;순번<nashr_o_lcham;순번++)o_lchov_ma_lumotlar[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(o_lchov_ma_lumotlar,nashr_o_lcham,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return nashr_o_lcham;
}
int 꾸러미읽기(const char *Nomi, unsigned char *o_lchov_ma_lumotlar, unsigned 수용량) {
    if(!항목들)return -2;unsigned element_COUNT=uzunlik_VALUE(Nomi),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==element_COUNT && 같음(Arxiv+현재위치+46,(const unsigned char*)Nomi,element_COUNT))return a_zo(현재위치,o_lchov_ma_lumotlar,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return kiritish_Sinf; }
int 꾸러미열기(const char *fayl_kiritish_nom) {
    항목들=0;kiritish_Sinf[0]=0;
    intptr_t fayl_deskriptor=사용자호출(3,(uintptr_t)fayl_kiritish_nom,0,0,0,0,0);if(fayl_deskriptor<0)return fayl_deskriptor;
    intptr_t element_COUNT=사용자호출(9,fayl_deskriptor,0,0,0,0,0);
    if(element_COUNT<22 || element_COUNT>(intptr_t)sizeof(Arxiv)) { 사용자호출(4,fayl_deskriptor,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,fayl_deskriptor,(uintptr_t)Arxiv,element_COUNT,0,0,0);사용자호출(4,fayl_deskriptor,0,0,0,0,0);
    if(RECEIVED_COUNT!=element_COUNT)return -5;Hajmi=element_COUNT;
    unsigned to_xtatmoq_OFFSET=Hajmi-22;
    for(;;) { if(네바이트읽기(to_xtatmoq_OFFSET)==0x06054b50 && to_xtatmoq_OFFSET+22+두바이트읽기(to_xtatmoq_OFFSET+20)==Hajmi)break; if(!to_xtatmoq_OFFSET)return -8;to_xtatmoq_OFFSET--; }
    unsigned kiritish_COUNT=두바이트읽기(to_xtatmoq_OFFSET+10);중앙목록=네바이트읽기(to_xtatmoq_OFFSET+16);
    if(두바이트읽기(to_xtatmoq_OFFSET+4)||두바이트읽기(to_xtatmoq_OFFSET+6)||두바이트읽기(to_xtatmoq_OFFSET+8)!=kiritish_COUNT||!kiritish_COUNT||kiritish_COUNT>256||!klip(중앙목록,네바이트읽기(to_xtatmoq_OFFSET+12),to_xtatmoq_OFFSET)||중앙목록+네바이트읽기(to_xtatmoq_OFFSET+12)!=to_xtatmoq_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<kiritish_COUNT;순번++) {
        if(!klip(현재위치,46,to_xtatmoq_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Keyingi_element=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!klip(현재위치,Keyingi_element,to_xtatmoq_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arxiv[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned uzunlik_ma_lumotlar=두바이트읽기(다른항목+28);if(uzunlik_ma_lumotlar==이름길이&&같음(Arxiv+다른항목+46,Arxiv+현재위치+46,uzunlik_ma_lumotlar))return -8;다른항목+=46+uzunlik_ma_lumotlar+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Keyingi_element;
    }
    if(현재위치!=to_xtatmoq_OFFSET)return -8;항목들=kiritish_COUNT;
    unsigned char 꾸러미명세[4096];int Guruh_o_lcham=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Guruh_o_lcham<0){항목들=0;return -8;}
    꾸러미명세[Guruh_o_lcham]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Guruh_o_lcham) {
        unsigned Bajarish=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Guruh_o_lcham && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned uzunlik_ma_lumotlar=INDEX_VALUE-Bajarish;if(INDEX_VALUE<(unsigned)Guruh_o_lcham)INDEX_VALUE++;if(uzunlik_ma_lumotlar && 꾸러미명세[Bajarish+uzunlik_ma_lumotlar-1]=='\r')uzunlik_ma_lumotlar--;
        if(사용량 && uzunlik_ma_lumotlar && 꾸러미명세[Bajarish]==' ') {Bajarish++;uzunlik_ma_lumotlar--;}
        else {
            int o_lchov=xususiyat_ma_lumotlar(논리크기,사용량,&진입점있음);if(o_lchov)return o_lchov;
            사용량=0;if(!uzunlik_ma_lumotlar)break;
        }
        if(uzunlik_ma_lumotlar>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<uzunlik_ma_lumotlar;순번++)논리크기[사용량++]=꾸러미명세[Bajarish+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int o_lchov=xususiyat_ma_lumotlar(논리크기,사용량,&진입점있음);if(o_lchov)return o_lchov;
    return 진입점있음?0:-8;
}
