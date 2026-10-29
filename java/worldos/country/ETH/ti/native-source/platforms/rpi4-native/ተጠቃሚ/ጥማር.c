#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "ጥማር.h"
#include "uzlib.h"
static unsigned char ሰንድ[16384], 풀린자료[16385];
static unsigned መጠን, 중앙목록, 항목들;
static char ምእታው_ክፍሊ[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return ሰንድ[현재위치] | ሰንድ[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int ቅንጣብ(unsigned 현재위치, unsigned 개수, unsigned 한도) { return 현재위치 <= 한도 && 개수 <= 한도-현재위치; }
static size_t ንውሓት_ዋጋ(const char *ሕብረ_ቁምፊ_ሓበሬታ) { size_t 개수=0; while(ሕብረ_ቁምፊ_ሓበሬታ[개수]) 개수++; return 개수; }
static int 같음(const unsigned char *첫째값, const unsigned char *둘째값, unsigned 개수) { for(unsigned 순번=0;순번<개수;순번++)if(첫째값[순번]!=둘째값[순번])return 0;return 1; }
static int ፋይል_ኣቑም(void *미사용값) { (void)미사용값; return -1; }
static int ባህሪ_ሓበሬታ(const char *መስመር,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)መስመር,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)መስመር,(const unsigned char*)"Main-Class: ",12)) {
        unsigned ዋጋ=사용량-12;if(*진입점있음||!ዋጋ||ዋጋ>=sizeof(ምእታው_ክፍሊ))return -8;
        for(unsigned 순번=0;순번<ዋጋ;순번++){unsigned char ኮድ_ፊደል=መስመር[12+순번];if(ኮድ_ፊደል<=32||ኮድ_ፊደል=='/'||ኮድ_ፊደል=='\\')return -8;ምእታው_ክፍሊ[순번]=ኮድ_ፊደል;}
        ምእታው_ክፍሊ[ዋጋ]=0;*진입점있음=1;
    }
    return 0;
}
static int አባል(unsigned 현재위치, unsigned char *결과자료, unsigned 용량한도) {
    unsigned ሜላ_ምእታው=두바이트읽기(현재위치+10), 설정비트=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), ፍታሕ_መጠን=네바이트읽기(현재위치+24), ኣካባብያዊ=네바이트읽기(현재위치+42);
    unsigned ሽም=두바이트읽기(현재위치+28);
    if(ፍታሕ_መጠን>용량한도 || ፍታሕ_መጠን>16384 || (ሜላ_ምእታው!=0 && ሜላ_ምእታው!=8) || (설정비트&~0x80e))return -8;
    if(!ቅንጣብ(ኣካባብያዊ,30,중앙목록) || 네바이트읽기(ኣካባብያዊ)!=0x04034b50 || 두바이트읽기(ኣካባብያዊ+8)!=ሜላ_ምእታው || 두바이트읽기(ኣካባብያዊ+6)!=설정비트 || 두바이트읽기(ኣካባብያዊ+26)!=ሽም)return -8;
    unsigned ጀምር_ሽፋን=ኣካባብያዊ+30, 추가영역=두바이트읽기(ኣካባብያዊ+28);
    if(!ቅንጣብ(ጀምር_ሽፋን,ሽም,중앙목록) || !같음(ሰንድ+ጀምር_ሽፋን,ሰንድ+현재위치+46,ሽም))return -8;
    ጀምር_ሽፋን+=ሽም;if(!ቅንጣብ(ጀምር_ሽፋን,추가영역,중앙목록))return -8;ጀምር_ሽፋን+=추가영역;
    if(!ቅንጣብ(ጀምር_ሽፋን,압축크기,중앙목록))return -8;
    if(!(설정비트&8) && (네바이트읽기(ኣካባብያዊ+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(ኣካባብያዊ+18)!=압축크기 || 네바이트읽기(ኣካባብያዊ+22)!=ፍታሕ_መጠን))return -8;
    if(ሜላ_ምእታው==0) { if(압축크기!=ፍታሕ_መጠን)return -8; for(unsigned 순번=0;순번<ፍታሕ_መጠን;순번++)결과자료[순번]=ሰንድ[ጀምር_ሽፋን+순번]; }
    else {
        uzlib_uncomp_t መዓልቦ_ሓበሬታ={0};uzlib_uncompress_init(&መዓልቦ_ሓበሬታ,0,0);
        መዓልቦ_ሓበሬታ.source=ሰንድ+ጀምር_ሽፋን;መዓልቦ_ሓበሬታ.source_limit=መዓልቦ_ሓበሬታ.source+압축크기;መዓልቦ_ሓበሬታ.source_read_cb=ፋይል_ኣቑም;
        /* One extra output byte lets inflate consume/check the end marker. */
        መዓልቦ_ሓበሬታ.dest_start=መዓልቦ_ሓበሬታ.dest=풀린자료;መዓልቦ_ሓበሬታ.dest_limit=풀린자료+ፍታሕ_መጠን+1;
        int 반환값=uzlib_uncompress(&መዓልቦ_ሓበሬታ);
        if(반환값!=UZLIB_DONE || መዓልቦ_ሓበሬታ.eof || መዓልቦ_ሓበሬታ.dest!=풀린자료+ፍታሕ_መጠን || መዓልቦ_ሓበሬታ.source!=መዓልቦ_ሓበሬታ.source_limit)return -8;
        for(unsigned 순번=0;순번<ፍታሕ_መጠን;순번++)결과자료[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(결과자료,ፍታሕ_መጠን,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return ፍታሕ_መጠን;
}
int 꾸러미읽기(const char *ሽም, unsigned char *결과자료, unsigned 수용량) {
    if(!항목들)return -2;unsigned 개수=ንውሓት_ዋጋ(ሽም),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==개수 && 같음(ሰንድ+현재위치+46,(const unsigned char*)ሽም,개수))return አባል(현재위치,결과자료,수용량);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return ምእታው_ክፍሊ; }
int 꾸러미열기(const char *ፋይል_ምእታው_ሽም) {
    항목들=0;ምእታው_ክፍሊ[0]=0;
    intptr_t ፋይል_መትሓዚ=사용자호출(3,(uintptr_t)ፋይል_ምእታው_ሽም,0,0,0,0,0);if(ፋይል_መትሓዚ<0)return ፋይል_መትሓዚ;
    intptr_t 개수=사용자호출(9,ፋይል_መትሓዚ,0,0,0,0,0);
    if(개수<22 || 개수>(intptr_t)sizeof(ሰንድ)) { 사용자호출(4,ፋይል_መትሓዚ,0,0,0,0,0);return -8; }
    intptr_t 받은수=사용자호출(2,ፋይል_መትሓዚ,(uintptr_t)ሰንድ,개수,0,0,0);사용자호출(4,ፋይል_መትሓዚ,0,0,0,0,0);
    if(받은수!=개수)return -5;መጠን=개수;
    unsigned ኣቑም_ሽፋን=መጠን-22;
    for(;;) { if(네바이트읽기(ኣቑም_ሽፋን)==0x06054b50 && ኣቑም_ሽፋን+22+두바이트읽기(ኣቑም_ሽፋን+20)==መጠን)break; if(!ኣቑም_ሽፋን)return -8;ኣቑም_ሽፋን--; }
    unsigned 항목수=두바이트읽기(ኣቑም_ሽፋን+10);중앙목록=네바이트읽기(ኣቑም_ሽፋን+16);
    if(두바이트읽기(ኣቑም_ሽፋን+4)||두바이트읽기(ኣቑም_ሽፋን+6)||두바이트읽기(ኣቑም_ሽፋን+8)!=항목수||!항목수||항목수>256||!ቅንጣብ(중앙목록,네바이트읽기(ኣቑም_ሽፋን+12),ኣቑም_ሽፋን)||중앙목록+네바이트읽기(ኣቑም_ሽፋን+12)!=ኣቑም_ሽፋን)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목수;순번++) {
        if(!ቅንጣብ(현재위치,46,ኣቑም_ሽፋን)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),다음=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!ቅንጣብ(현재위치,다음,ኣቑም_ሽፋን)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!ሰንድ[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned ንውሓት_ሓበሬታ=두바이트읽기(다른항목+28);if(ንውሓት_ሓበሬታ==이름길이&&같음(ሰንድ+다른항목+46,ሰንድ+현재위치+46,ንውሓት_ሓበሬታ))return -8;다른항목+=46+ንውሓት_ሓበሬታ+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=다음;
    }
    if(현재위치!=ኣቑም_ሽፋን)return -8;항목들=항목수;
    unsigned char 꾸러미명세[4096];int ጉጅለ_መጠን=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(ጉጅለ_መጠን<0){항목들=0;return -8;}
    꾸러미명세[ጉጅለ_መጠን]=0;
    char 논리크기[512];unsigned 사용량=0,መሐበሪ_ዋጋ=0;int 진입점있음=0;
    while(መሐበሪ_ዋጋ<(unsigned)ጉጅለ_መጠን) {
        unsigned ኣኺድ=መሐበሪ_ዋጋ;while(መሐበሪ_ዋጋ<(unsigned)ጉጅለ_መጠን && 꾸러미명세[መሐበሪ_ዋጋ]!='\n')መሐበሪ_ዋጋ++;
        unsigned ንውሓት_ሓበሬታ=መሐበሪ_ዋጋ-ኣኺድ;if(መሐበሪ_ዋጋ<(unsigned)ጉጅለ_መጠን)መሐበሪ_ዋጋ++;if(ንውሓት_ሓበሬታ && 꾸러미명세[ኣኺድ+ንውሓት_ሓበሬታ-1]=='\r')ንውሓት_ሓበሬታ--;
        if(사용량 && ንውሓት_ሓበሬታ && 꾸러미명세[ኣኺድ]==' ') {ኣኺድ++;ንውሓት_ሓበሬታ--;}
        else {
            int 결과=ባህሪ_ሓበሬታ(논리크기,사용량,&진입점있음);if(결과)return 결과;
            사용량=0;if(!ንውሓት_ሓበሬታ)break;
        }
        if(ንውሓት_ሓበሬታ>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<ንውሓት_ሓበሬታ;순번++)논리크기[사용량++]=꾸러미명세[ኣኺድ+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int 결과=ባህሪ_ሓበሬታ(논리크기,사용량,&진입점있음);if(결과)return 결과;
    return 진입점있음?0:-8;
}
