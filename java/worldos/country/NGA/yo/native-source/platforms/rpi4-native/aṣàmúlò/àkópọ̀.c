#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "àkópọ̀.h"
#include "uzlib.h"
static unsigned char Ìpamọ_ọlọ́jọ́pípẹ́[16384], 풀린자료[16385];
static unsigned Ìwọ̀n, 중앙목록, 항목들;
static char ìgbéwọlé_ọ̀wọ́[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Ìpamọ_ọlọ́jọ́pípẹ́[현재위치] | Ìpamọ_ọlọ́jọ́pípẹ́[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int ní_ṣókí(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t gígùn_iye(const char *fọ́nrán_détà) { size_t 개수=0; while(fọ́nrán_détà[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int fáìlì_parí(void *미사용값) { (void)미사용값; return -1; }
static int àwòmọ́_détà(const char *ìlà,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)ìlà,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)ìlà,(const unsigned char*)"Main-Class: ",12)) {
        unsigned iye=사용량-12;if(*진입점있음||!iye||iye>=sizeof(ìgbéwọlé_ọ̀wọ́))return -8;
        for(unsigned 순번=0;순번<iye;순번++){unsigned char kóòdù_ẹyọ_ọ̀rọ̀=ìlà[12+순번];if(kóòdù_ẹyọ_ọ̀rọ̀<=32||kóòdù_ẹyọ_ọ̀rọ̀=='/'||kóòdù_ẹyọ_ọ̀rọ̀=='\\')return -8;ìgbéwọlé_ọ̀wọ́[순번]=kóòdù_ẹyọ_ọ̀rọ̀;}
        ìgbéwọlé_ọ̀wọ́[iye]=0;*진입점있음=1;
    }
    return 0;
}
static int ọmọ_ẹgbẹ́(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned ìlànà_ìgbéwọlé=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), dápadà_ìwọn=네바이트읽기(현재위치+24), agbègbè=네바이트읽기(현재위치+42);
    unsigned Orúkọ=두바이트읽기(현재위치+28);
    if(dápadà_ìwọn>용량한도 || dápadà_ìwọn>16384 || (ìlànà_ìgbéwọlé!=0 && ìlànà_ìgbéwọlé!=8) || (설정비트&~0x80e))return -8;
    if(!ní_ṣókí(agbègbè,30,중앙목록) || 네바이트읽기(agbègbè)!=0x04034b50 || 두바이트읽기(agbègbè+8)!=ìlànà_ìgbéwọlé || 두바이트읽기(agbègbè+6)!=설정비트 || 두바이트읽기(agbègbè+26)!=Orúkọ)return -8;
    unsigned bẹ̀rẹ̀_Ìtayọ=agbègbè+30, 추가영역=두바이트읽기(agbègbè+28);
    if(!ní_ṣókí(bẹ̀rẹ̀_Ìtayọ,Orúkọ,중앙목록) || !같음(Ìpamọ_ọlọ́jọ́pípẹ́+bẹ̀rẹ̀_Ìtayọ,Ìpamọ_ọlọ́jọ́pípẹ́+현재위치+46,Orúkọ))return -8;
    bẹ̀rẹ̀_Ìtayọ+=Orúkọ;if(!ní_ṣókí(bẹ̀rẹ̀_Ìtayọ,추가영역,중앙목록))return -8;bẹ̀rẹ̀_Ìtayọ+=추가영역;
    if(!ní_ṣókí(bẹ̀rẹ̀_Ìtayọ,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(agbègbè+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(agbègbè+18)!=압축크기 || 네바이트읽기(agbègbè+22)!=dápadà_ìwọn))return -8;
    if(ìlànà_ìgbéwọlé==0) { if(압축크기!=dápadà_ìwọn)return -8; for(unsigned 순번=0;순번<dápadà_ìwọn;순번++)결과자료[순번]=Ìpamọ_ọlọ́jọ́pípẹ́[bẹ̀rẹ̀_Ìtayọ+순번]; }
    else {
        uzlib_uncomp_t èbúté_détà={0};uzlib_uncompress_init(&èbúté_détà,0,0);
        èbúté_détà.source=Ìpamọ_ọlọ́jọ́pípẹ́+bẹ̀rẹ̀_Ìtayọ;èbúté_détà.source_limit=èbúté_détà.source+압축크기;èbúté_détà.source_read_cb=fáìlì_parí;
        /* One extra output byte lets inflate consume/check the end marker. */
        èbúté_détà.dest_start=èbúté_détà.dest=풀린자료;èbúté_détà.dest_limit=풀린자료+dápadà_ìwọn+1;
        int 반환값=uzlib_uncompress(&èbúté_détà);
        if(반환값!=UZLIB_DONE || èbúté_détà.eof || èbúté_détà.dest!=풀린자료+dápadà_ìwọn || èbúté_détà.source!=èbúté_détà.source_limit)return -8;
        for(unsigned 순번=0;순번<dápadà_ìwọn;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,dápadà_ìwọn,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return dápadà_ìwọn;
}
int 꾸러미읽기(const char *Orúkọ, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=gígùn_iye(Orúkọ),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(Ìpamọ_ọlọ́jọ́pípẹ́+현재위치+46,(const unsigned char*)Orúkọ,개수))return ọmọ_ẹgbẹ́(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ìgbéwọlé_ọ̀wọ́; }
int 꾸러미열기(const char *fáìlì_ìgbéwọlé_orúkọ) {
    항목들=0;ìgbéwọlé_ọ̀wọ́[0]=0;
    intptr_t fáìlì_èkù=사용자호출(3,(uintptr_t)fáìlì_ìgbéwọlé_orúkọ,0,0,0,0,0);if(fáìlì_èkù<0)return fáìlì_èkù;
    intptr_t 개수=사용자호출(9,fáìlì_èkù,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(Ìpamọ_ọlọ́jọ́pípẹ́)) { 사용자호출(4,fáìlì_èkù,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,fáìlì_èkù,(uintptr_t)Ìpamọ_ọlọ́jọ́pípẹ́,개수,0,0,0);사용자호출(4,fáìlì_èkù,0,0,0,0,0);
    if(받은수!=개수)return -5;Ìwọ̀n=개수;
    unsigned parí_Ìtayọ=Ìwọ̀n-22;
    for(;;) { if(네바이트읽기(parí_Ìtayọ)==0x06054b50 && parí_Ìtayọ+22+두바이트읽기(parí_Ìtayọ+20)==Ìwọ̀n)break; if(!parí_Ìtayọ)return -8;parí_Ìtayọ--; }
    unsigned 항목수=두바이트읽기(parí_Ìtayọ+10);중앙목록=네바이트읽기(parí_Ìtayọ+16);
    if(두바이트읽기(parí_Ìtayọ+4)||두바이트읽기(parí_Ìtayọ+6)||두바이트읽기(parí_Ìtayọ+8)!=항목수||!항목수||항목수>256||!ní_ṣókí(중앙목록,네바이트읽기(parí_Ìtayọ+12),parí_Ìtayọ)||중앙목록+네바이트읽기(parí_Ìtayọ+12)!=parí_Ìtayọ)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!ní_ṣókí(현재위치,46,parí_Ìtayọ)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!ní_ṣókí(현재위치,다음,parí_Ìtayọ)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Ìpamọ_ọlọ́jọ́pípẹ́[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned gígùn_détà=두바이트읽기(다른항목+28);if(gígùn_détà==이름길이&&같음(Ìpamọ_ọlọ́jọ́pípẹ́+다른항목+46,Ìpamọ_ọlọ́jọ́pípẹ́+현재위치+46,gígùn_détà))return -8;다른항목+=46+gígùn_détà+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=parí_Ìtayọ)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int Àjọṣe_ìwọn=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Àjọṣe_ìwọn<0){항목들=0;return -8;}
    꾸러미명세[Àjọṣe_ìwọn]=0;
    char 논리크기[512];unsigned 사용량=0,wá_atọ̀ka_àkóónú_iye=0;int 진입점있음=0;
    while(wá_atọ̀ka_àkóónú_iye<(unsigned)Àjọṣe_ìwọn) {
        unsigned Rọ́ọ̀nù=wá_atọ̀ka_àkóónú_iye;while(wá_atọ̀ka_àkóónú_iye<(unsigned)Àjọṣe_ìwọn && 꾸러미명세[wá_atọ̀ka_àkóónú_iye]!='\n')wá_atọ̀ka_àkóónú_iye++;
        unsigned gígùn_détà=wá_atọ̀ka_àkóónú_iye-Rọ́ọ̀nù;if(wá_atọ̀ka_àkóónú_iye<(unsigned)Àjọṣe_ìwọn)wá_atọ̀ka_àkóónú_iye++;if(gígùn_détà && 꾸러미명세[Rọ́ọ̀nù+gígùn_détà-1]=='\r')gígùn_détà--;
        if(사용량 && gígùn_détà && 꾸러미명세[Rọ́ọ̀nù]==' ') {Rọ́ọ̀nù++;gígùn_détà--;}
        else {
            int 결과=àwòmọ́_détà(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!gígùn_détà)break;
        }
        if(gígùn_détà>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<gígùn_détà;순번++)논리크기[사용량++]=꾸러미명세[Rọ́ọ̀nù+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=àwòmọ́_détà(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
