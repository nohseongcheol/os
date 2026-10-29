/* xoox_xëyma 전용 할당기와 pasu_dugg_xëyma 난수 공급. kiy_jariñoo_internet ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct fatlekookaay_gatandu { size_t diir_xëyma; struct fatlekookaay_gatandu *다음; int 사용; } fatlekookaay_gatandu;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static fatlekookaay_gatandu *첫조각;
void *jagleel_lu_soree(size_t diir_xëyma) {
    if (!diir_xëyma || diir_xëyma>sizeof(기억터)-64) return 0;
    diir_xëyma=(diir_xëyma+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->diir_xëyma=sizeof(기억터)-32;}
    for(fatlekookaay_gatandu *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->diir_xëyma>=diir_xëyma){
        if(조각->diir_xëyma>=diir_xëyma+64){fatlekookaay_gatandu *새조각=(void*)((char*)조각+32+diir_xëyma);
            새조각->diir_xëyma=조각->diir_xëyma-diir_xëyma-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->diir_xëyma=diir_xëyma;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void yewwi_lu_soree(void *dëkkuwaay) {
    if(!dëkkuwaay)return;fatlekookaay_gatandu *조각=(void*)((char*)dëkkuwaay-32);
    volatile unsigned char *지움=dëkkuwaay;for(size_t 순번=0;순번<조각->diir_xëyma;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->diir_xëyma+=32+조각->다음->diir_xëyma;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *dëkkuwaay,size_t diir_xëyma){
    if(!dëkkuwaay)return jagleel_lu_soree(diir_xëyma);if(!diir_xëyma){yewwi_lu_soree(dëkkuwaay);return 0;}
    fatlekookaay_gatandu *조각=(void*)((char*)dëkkuwaay-32);void *새주소=jagleel_lu_soree(diir_xëyma);
    if(새주소){memcpy(새주소,dëkkuwaay,diir_xëyma<조각->diir_xëyma?diir_xëyma:조각->diir_xëyma);yewwi_lu_soree(dëkkuwaay);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int Araf_xëyma){for(;;Word_SMS++){if(*Word_SMS==(char)Araf_xëyma)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t diir_xëyma=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,diir_xëyma))return(char*)Word_SMS;return diir_xëyma?0:(char*)Word_SMS;}
char *strncpy(char *jëmmukaay_xëyma,const char *원본,size_t diir_xëyma){size_t 순번=0;for(;순번<diir_xëyma&&원본[순번];순번++)jëmmukaay_xëyma[순번]=원본[순번];for(;순번<diir_xëyma;순번++)jëmmukaay_xëyma[순번]=0;return jëmmukaay_xëyma;}
char *strncat(char *jëmmukaay_xëyma,const char *원본,size_t diir_xëyma){char *끝=jëmmukaay_xëyma+strlen(jëmmukaay_xëyma);while(diir_xëyma--&&*원본)*끝++=*원본++;*끝=0;return jëmmukaay_xëyma;}
int strncasecmp(const char *가,const char *나,size_t diir_xëyma){while(diir_xëyma--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *yemalekat_xëyma,char **다음){if(!Word_SMS)Word_SMS=*다음;while(*Word_SMS&&strchr(yemalekat_xëyma,*Word_SMS))Word_SMS++;if(!*Word_SMS){*다음=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(yemalekat_xëyma,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*다음=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int 밑) {
    const char *Cosaan=Word_SMS;unsigned long xëyma=0;int 음수=0,luëppe_xëyma=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((밑==0||밑==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {밑=16;Word_SMS+=2;}
    if(!밑)밑=*Word_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)Cosaan;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned Araf_xëyma=(unsigned char)*Word_SMS;
        unsigned 수=Araf_xëyma>='0'&&Araf_xëyma<='9'?Araf_xëyma-'0':Araf_xëyma>='a'&&Araf_xëyma<='z'?Araf_xëyma-'a'+10:Araf_xëyma>='A'&&Araf_xëyma<='Z'?Araf_xëyma-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(xëyma>(~0ul-수)/(unsigned)밑)luëppe_xëyma=1;
        if(!luëppe_xëyma)xëyma=xëyma*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?Cosaan:Word_SMS);
    return luëppe_xëyma?~0ul:음수?0ul-xëyma:xëyma;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int tolluwaay_bu_njëkk_nekkin;
void 원격요약(const void *mbir, size_t diir_xëyma, unsigned char 결과[32]) {
    br_sha256_context péete_xëyma;
    br_sha256_init(&péete_xëyma); br_sha256_update(&péete_xëyma, mbir, diir_xëyma); br_sha256_out(&péete_xëyma, 결과);
    memset(&péete_xëyma, 0, sizeof(péete_xëyma));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *jëmmukaay_xëyma,unsigned diir_xëyma){
    if(!tolluwaay_bu_njëkk_nekkin){volatile unsigned char *mbir=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=mbir[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=mbir[8+순번];for(unsigned 순번=0;순번<40;순번++)mbir[순번]=0;tolluwaay_bu_njëkk_nekkin=2;}
        else {tolluwaay_bu_njëkk_nekkin=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(tolluwaay_bu_njëkk_nekkin==2){while(diir_xëyma){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=diir_xëyma<32?diir_xëyma:32;memcpy(jëmmukaay_xëyma,다음,수);memset(다음,0,32);jëmmukaay_xëyma+=수;diir_xëyma-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(diir_xëyma){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t xëyma=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&diir_xëyma;순번++,diir_xëyma--){*jëmmukaay_xëyma++=xëyma&255;xëyma>>=8;}}
    return 0;
}
