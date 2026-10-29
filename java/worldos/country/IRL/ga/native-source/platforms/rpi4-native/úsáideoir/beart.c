#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "beart.h"
#include "uzlib.h"
static unsigned char Cartlann[16384], 풀린자료[16385];
static unsigned Méid, 중앙목록, 항목들;
static char iontráil_aicme[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Cartlann[현재위치] | Cartlann[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int gearrthóg(unsigned 현재위치, unsigned mír_COUNT, unsigned 한도) { return 현재위치 <= 한도 && mír_COUNT <= 한도-현재위치; }
static size_t fad_VALUE(const char *teaghrán_sonraí) { size_t mír_COUNT=0; while(teaghrán_sonraí[mír_COUNT]) mír_COUNT++; return mír_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned mír_COUNT) { for(unsigned 순번=0;순번<mír_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int comhad_cuir_deireadh_le(void *미사용값) { (void)미사용값; return -1; }
static int tréith_sonraí(const char *Líne,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)Líne,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)Líne,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(iontráil_aicme))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char pointe_cóid=Líne[12+순번];if(pointe_cóid<=32||pointe_cóid=='/'||pointe_cóid=='\\')return -8;iontráil_aicme[순번]=pointe_cóid;}
        iontráil_aicme[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int ball(unsigned 현재위치, unsigned char *tomhas_sonraí, unsigned 용량한도) {
    unsigned modh_iontráil=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), leagan_socraigh_méid=네바이트읽기(현재위치+24), logánta=네바이트읽기(현재위치+42);
    unsigned Ainm=두바이트읽기(현재위치+28);
    if(leagan_socraigh_méid>용량한도 || leagan_socraigh_méid>16384 || (modh_iontráil!=0 && modh_iontráil!=8) || (설정비트&~0x80e))return -8;
    if(!gearrthóg(logánta,30,중앙목록) || 네바이트읽기(logánta)!=0x04034b50 || 두바이트읽기(logánta+8)!=modh_iontráil || 두바이트읽기(logánta+6)!=설정비트 || 두바이트읽기(logánta+26)!=Ainm)return -8;
    unsigned Start_OFFSET=logánta+30, 추가영역=두바이트읽기(logánta+28);
    if(!gearrthóg(Start_OFFSET,Ainm,중앙목록) || !같음(Cartlann+Start_OFFSET,Cartlann+현재위치+46,Ainm))return -8;
    Start_OFFSET+=Ainm;if(!gearrthóg(Start_OFFSET,추가영역,중앙목록))return -8;Start_OFFSET+=추가영역;
    if(!gearrthóg(Start_OFFSET,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(logánta+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(logánta+18)!=압축크기 || 네바이트읽기(logánta+22)!=leagan_socraigh_méid))return -8;
    if(modh_iontráil==0) { if(압축크기!=leagan_socraigh_méid)return -8; for(unsigned 순번=0;순번<leagan_socraigh_méid;순번++)tomhas_sonraí[순번]=Cartlann[Start_OFFSET+순번]; }
    else {
        uzlib_uncomp_t sprioc_sonraí={0};uzlib_uncompress_init(&sprioc_sonraí,0,0);
        sprioc_sonraí.source=Cartlann+Start_OFFSET;sprioc_sonraí.source_limit=sprioc_sonraí.source+압축크기;sprioc_sonraí.source_read_cb=comhad_cuir_deireadh_le;
        /* One extra output byte lets inflate consume/check the end marker. */
        sprioc_sonraí.dest_start=sprioc_sonraí.dest=풀린자료;sprioc_sonraí.dest_limit=풀린자료+leagan_socraigh_méid+1;
        int 반환값=uzlib_uncompress(&sprioc_sonraí);
        if(반환값!=UZLIB_DONE || sprioc_sonraí.eof || sprioc_sonraí.dest!=풀린자료+leagan_socraigh_méid || sprioc_sonraí.source!=sprioc_sonraí.source_limit)return -8;
        for(unsigned 순번=0;순번<leagan_socraigh_méid;순번++)tomhas_sonraí[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(tomhas_sonraí,leagan_socraigh_méid,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return leagan_socraigh_méid;
}
int 꾸러미읽기(const char *Ainm, unsigned char *tomhas_sonraí, unsigned 수용량) {
    if(!항목들)return -2;unsigned mír_COUNT=fad_VALUE(Ainm),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==mír_COUNT && 같음(Cartlann+현재위치+46,(const unsigned char*)Ainm,mír_COUNT))return ball(현재위치,tomhas_sonraí,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return iontráil_aicme; }
int 꾸러미열기(const char *comhad_iontráil_ainm) {
    항목들=0;iontráil_aicme[0]=0;
    intptr_t comhad_hanla=사용자호출(3,(uintptr_t)comhad_iontráil_ainm,0,0,0,0,0);if(comhad_hanla<0)return comhad_hanla;
    intptr_t mír_COUNT=사용자호출(9,comhad_hanla,0,0,0,0,0);
    if(mír_COUNT<22 || mír_COUNT>(intptr_t)sizeof(Cartlann)) { 사용자호출(4,comhad_hanla,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,comhad_hanla,(uintptr_t)Cartlann,mír_COUNT,0,0,0);사용자호출(4,comhad_hanla,0,0,0,0,0);
    if(RECEIVED_COUNT!=mír_COUNT)return -5;Méid=mír_COUNT;
    unsigned cuir_deireadh_le_OFFSET=Méid-22;
    for(;;) { if(네바이트읽기(cuir_deireadh_le_OFFSET)==0x06054b50 && cuir_deireadh_le_OFFSET+22+두바이트읽기(cuir_deireadh_le_OFFSET+20)==Méid)break; if(!cuir_deireadh_le_OFFSET)return -8;cuir_deireadh_le_OFFSET--; }
    unsigned iontráil_COUNT=두바이트읽기(cuir_deireadh_le_OFFSET+10);중앙목록=네바이트읽기(cuir_deireadh_le_OFFSET+16);
    if(두바이트읽기(cuir_deireadh_le_OFFSET+4)||두바이트읽기(cuir_deireadh_le_OFFSET+6)||두바이트읽기(cuir_deireadh_le_OFFSET+8)!=iontráil_COUNT||!iontráil_COUNT||iontráil_COUNT>256||!gearrthóg(중앙목록,네바이트읽기(cuir_deireadh_le_OFFSET+12),cuir_deireadh_le_OFFSET)||중앙목록+네바이트읽기(cuir_deireadh_le_OFFSET+12)!=cuir_deireadh_le_OFFSET)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<iontráil_COUNT;순번++) {
        if(!gearrthóg(현재위치,46,cuir_deireadh_le_OFFSET)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Ar_aghaidh_mír=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!gearrthóg(현재위치,Ar_aghaidh_mír,cuir_deireadh_le_OFFSET)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Cartlann[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned fad_sonraí=두바이트읽기(다른항목+28);if(fad_sonraí==이름길이&&같음(Cartlann+다른항목+46,Cartlann+현재위치+46,fad_sonraí))return -8;다른항목+=46+fad_sonraí+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Ar_aghaidh_mír;
    }
    if(현재위치!=cuir_deireadh_le_OFFSET)return -8;항목들=iontráil_COUNT;
    unsigned char 꾸러미명세[4096];int Grúpa_socraigh_méid=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(Grúpa_socraigh_méid<0){항목들=0;return -8;}
    꾸러미명세[Grúpa_socraigh_méid]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Grúpa_socraigh_méid) {
        unsigned Rith_2=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Grúpa_socraigh_méid && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned fad_sonraí=INDEX_VALUE-Rith_2;if(INDEX_VALUE<(unsigned)Grúpa_socraigh_méid)INDEX_VALUE++;if(fad_sonraí && 꾸러미명세[Rith_2+fad_sonraí-1]=='\r')fad_sonraí--;
        if(사용량 && fad_sonraí && 꾸러미명세[Rith_2]==' ') {Rith_2++;fad_sonraí--;}
        else {
            int tomhas=tréith_sonraí(논리크기,사용량,&진입점있음);if(tomhas)return tomhas;
            사용량=0;if(!fad_sonraí)break;
        }
        if(fad_sonraí>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<fad_sonraí;순번++)논리크기[사용량++]=꾸러미명세[Rith_2+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int tomhas=tréith_sonraí(논리크기,사용량,&진입점있음);if(tomhas)return tomhas;
    return 진입점있음?0:-8;
}
