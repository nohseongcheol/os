#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paket.h"
#include "uzlib.h"
static unsigned char Arxiv[16384], 풀린자료[16385];
static unsigned Böyüklük, 중앙목록, 항목들;
static char daxiletmə_Sinif[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Arxiv[현재위치] | Arxiv[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int klip(unsigned 현재위치, unsigned element_COUNT, unsigned 한도) { return 현재위치 <= 한도 && element_COUNT <= 한도-현재위치; }
static size_t uzunluq_VALUE(const char *sətir_verilənlər) { size_t element_COUNT=0; while(sətir_verilənlər[element_COUNT]) element_COUNT++; return element_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned element_COUNT) { for(unsigned 순번=0;순번<element_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int fayl_bitirmək(void *미사용값) { (void)미사용값; return -1; }
static int atribut_verilənlər(const char *Giriş,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Giriş,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Giriş,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(daxiletmə_Sinif))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char simvol_kodu=Giriş[12+순번];if(simvol_kodu<=32||simvol_kodu=='/'||simvol_kodu=='\\')return -8;daxiletmə_Sinif[순번]=simvol_kodu;}
        daxiletmə_Sinif[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int üzv(unsigned 현재위치, unsigned char *ölçü_verilənlər, unsigned 용량한도) {
    unsigned metod_daxiletmə=두바이트읽기(현재위치+10), konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), burax_ölçünü_dəyişmək=네바이트읽기(현재위치+24), lokal=네바이트읽기(현재위치+42);
    unsigned Ad=두바이트읽기(현재위치+28);
    if(burax_ölçünü_dəyişmək>용량한도 || burax_ölçünü_dəyişmək>16384 || (metod_daxiletmə!=0 && metod_daxiletmə!=8) || (konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&~0x80e))return -8;
    if(!klip(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metod_daxiletmə || 두바이트읽기(lokal+6)!=konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti || 두바이트읽기(lokal+26)!=Ad)return -8;
    unsigned Başla_OFFSET=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klip(Başla_OFFSET,Ad,중앙목록) || !같음(Arxiv+Başla_OFFSET,Arxiv+현재위치+46,Ad))return -8;
    Başla_OFFSET+=Ad;if(!klip(Başla_OFFSET,추가영역,중앙목록))return -8;Başla_OFFSET+=추가영역;
    if(!klip(Başla_OFFSET,압축크기,중앙목록))return -8;
    if(!(konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&8) && (네바이트읽기(lokal+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=burax_ölçünü_dəyişmək))return -8;
    if(metod_daxiletmə==0) { if(압축크기!=burax_ölçünü_dəyişmək)return -8; for(unsigned 순번=0;순번<burax_ölçünü_dəyişmək;순번++)ölçü_verilənlər[순번]=Arxiv[Başla_OFFSET+순번]; }
    else {
        uzlib_uncomp_t təyinat_verilənlər={0};uzlib_uncompress_init(&təyinat_verilənlər,0,0);
        təyinat_verilənlər.source=Arxiv+Başla_OFFSET;təyinat_verilənlər.source_limit=təyinat_verilənlər.source+압축크기;təyinat_verilənlər.source_read_cb=fayl_bitirmək;
        /* One extra output byte lets inflate consume/check the end marker. */
        təyinat_verilənlər.dest_start=təyinat_verilənlər.dest=풀린자료;təyinat_verilənlər.dest_limit=풀린자료+burax_ölçünü_dəyişmək+1;
        int 반환값=uzlib_uncompress(&təyinat_verilənlər);
        if(반환값!=UZLIB_DONE || təyinat_verilənlər.eof || təyinat_verilənlər.dest!=풀린자료+burax_ölçünü_dəyişmək || təyinat_verilənlər.source!=təyinat_verilənlər.source_limit)return -8;
        for(unsigned 순번=0;순번<burax_ölçünü_dəyişmək;순번++)ölçü_verilənlər[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(ölçü_verilənlər,burax_ölçünü_dəyişmək,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return burax_ölçünü_dəyişmək;
}
int 꾸러미읽기(const char *Ad, unsigned char *ölçü_verilənlər, unsigned 수용량) {
    if(!항목들)return -2;unsigned element_COUNT=uzunluq_VALUE(Ad),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==element_COUNT && 같음(Arxiv+현재위치+46,(const unsigned char*)Ad,element_COUNT))return üzv(현재위치,ölçü_verilənlər,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return daxiletmə_Sinif; }
int 꾸러미열기(const char *fayl_daxiletmə_ad) {
    항목들=0;daxiletmə_Sinif[0]=0;
    intptr_t fayl_tutacaq=사용자호출(3,(uintptr_t)fayl_daxiletmə_ad,0,0,0,0,0);if(fayl_tutacaq<0)return fayl_tutacaq;
    intptr_t element_COUNT=사용자호출(9,fayl_tutacaq,0,0,0,0,0);
    if(element_COUNT<22 || element_COUNT>(intptr_t)sizeof(Arxiv)) { 사용자호출(4,fayl_tutacaq,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,fayl_tutacaq,(uintptr_t)Arxiv,element_COUNT,0,0,0);사용자호출(4,fayl_tutacaq,0,0,0,0,0);
    if(RECEIVED_COUNT!=element_COUNT)return -5;Böyüklük=element_COUNT;
    unsigned bitirmək_OFFSET=Böyüklük-22;
    for(;;) { if(네바이트읽기(bitirmək_OFFSET)==0x06054b50 && bitirmək_OFFSET+22+두바이트읽기(bitirmək_OFFSET+20)==Böyüklük)break; if(!bitirmək_OFFSET)return -8;bitirmək_OFFSET--; }
    unsigned daxiletmə_COUNT=두바이트읽기(bitirmək_OFFSET+10);중앙목록=네바이트읽기(bitirmək_OFFSET+16);
    if(두바이트읽기(bitirmək_OFFSET+4)||두바이트읽기(bitirmək_OFFSET+6)||두바이트읽기(bitirmək_OFFSET+8)!=daxiletmə_COUNT||!daxiletmə_COUNT||daxiletmə_COUNT>256||!klip(중앙목록,네바이트읽기(bitirmək_OFFSET+12),bitirmək_OFFSET)||중앙목록+네바이트읽기(bitirmək_OFFSET+12)!=bitirmək_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<daxiletmə_COUNT;순번++) {
        if(!klip(현재위치,46,bitirmək_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Sonrakı_element=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!klip(현재위치,Sonrakı_element,bitirmək_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arxiv[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned uzunluq_verilənlər=두바이트읽기(다른항목+28);if(uzunluq_verilənlər==이름길이&&같음(Arxiv+다른항목+46,Arxiv+현재위치+46,uzunluq_verilənlər))return -8;다른항목+=46+uzunluq_verilənlər+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Sonrakı_element;
    }
    if(현재위치!=bitirmək_OFFSET)return -8;항목들=daxiletmə_COUNT;
    unsigned char 꾸러미명세[4096];int Qrup_ölçünü_dəyişmək=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Qrup_ölçünü_dəyişmək<0){항목들=0;return -8;}
    꾸러미명세[Qrup_ölçünü_dəyişmək]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Qrup_ölçünü_dəyişmək) {
        unsigned İcra_Et=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Qrup_ölçünü_dəyişmək && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned uzunluq_verilənlər=INDEX_VALUE-İcra_Et;if(INDEX_VALUE<(unsigned)Qrup_ölçünü_dəyişmək)INDEX_VALUE++;if(uzunluq_verilənlər && 꾸러미명세[İcra_Et+uzunluq_verilənlər-1]=='\r')uzunluq_verilənlər--;
        if(사용량 && uzunluq_verilənlər && 꾸러미명세[İcra_Et]==' ') {İcra_Et++;uzunluq_verilənlər--;}
        else {
            int ölçü=atribut_verilənlər(논리크기,사용량,&진입점있음);if(ölçü)return ölçü;
            사용량=0;if(!uzunluq_verilənlər)break;
        }
        if(uzunluq_verilənlər>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<uzunluq_verilənlər;순번++)논리크기[사용량++]=꾸러미명세[İcra_Et+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int ölçü=atribut_verilənlər(논리크기,사용량,&진입점있음);if(ölçü)return ölçü;
    return 진입점있음?0:-8;
}
