/* ڪرنل_قدر 전용 할당기와 پاس_ورڊ_قدر 난수 공급. صارف ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ميموري_بلاڪ_ڪريو { size_t لمبائي_قدر; struct ميموري_بلاڪ_ڪريو *다음; int 사용; } ميموري_بلاڪ_ڪريو;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ميموري_بلاڪ_ڪريو *첫조각;
void *مختص_ڪريو_بعيد(size_t لمبائي_قدر) {
    if (!لمبائي_قدر || لمبائي_قدر>sizeof(기억터)-64) return 0;
    لمبائي_قدر=(لمبائي_قدر+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->لمبائي_قدر=sizeof(기억터)-32;}
    for(ميموري_بلاڪ_ڪريو *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->لمبائي_قدر>=لمبائي_قدر){
        if(조각->لمبائي_قدر>=لمبائي_قدر+64){ميموري_بلاڪ_ڪريو *새조각=(void*)((char*)조각+32+لمبائي_قدر);
            새조각->لمبائي_قدر=조각->لمبائي_قدر-لمبائي_قدر-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->لمبائي_قدر=لمبائي_قدر;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void جاري_ڪريو_بعيد(void *پتو) {
    if(!پتو)return;ميموري_بلاڪ_ڪريو *조각=(void*)((char*)پتو-32);
    volatile unsigned char *지움=پتو;for(size_t 순번=0;순번<조각->لمبائي_قدر;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->لمبائي_قدر+=32+조각->다음->لمبائي_قدر;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *پتو,size_t لمبائي_قدر){
    if(!پتو)return مختص_ڪريو_بعيد(لمبائي_قدر);if(!لمبائي_قدر){جاري_ڪريو_بعيد(پتو);return 0;}
    ميموري_بلاڪ_ڪريو *조각=(void*)((char*)پتو-32);void *새주소=مختص_ڪريو_بعيد(لمبائي_قدر);
    if(새주소){memcpy(새주소,پتو,لمبائي_قدر<조각->لمبائي_قدر?لمبائي_قدر:조각->لمبائي_قدر);جاري_ڪريو_بعيد(پتو);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *ورڊ_متن,int ڪريڪٽر_قدر){for(;;ورڊ_متن++){if(*ورڊ_متن==(char)ڪريڪٽر_قدر)return(char*)ورڊ_متن;if(!*ورڊ_متن)return 0;}}
char *strstr(const char *ورڊ_متن,const char *찾음){size_t لمبائي_قدر=strlen(찾음);for(;*ورڊ_متن;ورڊ_متن++)if(!strncmp(ورڊ_متن,찾음,لمبائي_قدر))return(char*)ورڊ_متن;return لمبائي_قدر?0:(char*)ورڊ_متن;}
char *strncpy(char *منزل_مقصود_قدر,const char *원본,size_t لمبائي_قدر){size_t 순번=0;for(;순번<لمبائي_قدر&&원본[순번];순번++)منزل_مقصود_قدر[순번]=원본[순번];for(;순번<لمبائي_قدر;순번++)منزل_مقصود_قدر[순번]=0;return منزل_مقصود_قدر;}
char *strncat(char *منزل_مقصود_قدر,const char *원본,size_t لمبائي_قدر){char *끝=منزل_مقصود_قدر+strlen(منزل_مقصود_قدر);while(لمبائي_قدر--&&*원본)*끝++=*원본++;*끝=0;return منزل_مقصود_قدر;}
int strncasecmp(const char *가,const char *나,size_t لمبائي_قدر){while(لمبائي_قدر--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *ورڊ_متن,const char *حد_مقرر_ڪرڻ_وارو_قدر,char **다음){if(!ورڊ_متن)ورڊ_متن=*다음;while(*ورڊ_متن&&strchr(حد_مقرر_ڪرڻ_وارو_قدر,*ورڊ_متن))ورڊ_متن++;if(!*ورڊ_متن){*다음=ورڊ_متن;return 0;}char *처음=ورڊ_متن;while(*ورڊ_متن&&!strchr(حد_مقرر_ڪرڻ_وارو_قدر,*ورڊ_متن))ورڊ_متن++;if(*ورڊ_متن)*ورڊ_متن++=0;*다음=ورڊ_متن;return 처음;}
unsigned long strtoul(const char *ورڊ_متن, char **끝, int 밑) {
    const char *ماخذ=ورڊ_متن;unsigned long قدر=0;int 음수=0,اوور_فلو_قدر=0;
    while(*ورڊ_متن==' '||(*ورڊ_متن>=9&&*ورڊ_متن<=13))ورڊ_متن++;
    if(*ورڊ_متن=='-'||*ورڊ_متن=='+')음수=*ورڊ_متن++=='-';
    if((밑==0||밑==16)&&ورڊ_متن[0]=='0'&&(ورڊ_متن[1]=='x'||ورڊ_متن[1]=='X')&&
       ((ورڊ_متن[2]>='0'&&ورڊ_متن[2]<='9')||(ورڊ_متن[2]>='a'&&ورڊ_متن[2]<='f')||(ورڊ_متن[2]>='A'&&ورڊ_متن[2]<='F'))) {밑=16;ورڊ_متن+=2;}
    if(!밑)밑=*ورڊ_متن=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ماخذ;return 0;}
    const char *처음=ورڊ_متن;
    for(;;ورڊ_متن++) {
        unsigned ڪريڪٽر_قدر=(unsigned char)*ورڊ_متن;
        unsigned 수=ڪريڪٽر_قدر>='0'&&ڪريڪٽر_قدر<='9'?ڪريڪٽر_قدر-'0':ڪريڪٽر_قدر>='a'&&ڪريڪٽر_قدر<='z'?ڪريڪٽر_قدر-'a'+10:ڪريڪٽر_قدر>='A'&&ڪريڪٽر_قدر<='Z'?ڪريڪٽر_قدر-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(قدر>(~0ul-수)/(unsigned)밑)اوور_فلو_قدر=1;
        if(!اوور_فلو_قدر)قدر=قدر*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(ورڊ_متن==처음?ماخذ:ورڊ_متن);
    return اوور_فلو_قدر?~0ul:음수?0ul-قدر:قدر;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int ٻج_حالت;
void 원격요약(const void *ڪوائف, size_t لمبائي_قدر, unsigned char 결과[32]) {
    br_sha256_context مفهوم_قدر;
    br_sha256_init(&مفهوم_قدر); br_sha256_update(&مفهوم_قدر, ڪوائف, لمبائي_قدر); br_sha256_out(&مفهوم_قدر, 결과);
    memset(&مفهوم_قدر, 0, sizeof(مفهوم_قدر));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *منزل_مقصود_قدر,unsigned لمبائي_قدر){
    if(!ٻج_حالت){volatile unsigned char *ڪوائف=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=ڪوائف[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=ڪوائف[8+순번];for(unsigned 순번=0;순번<40;순번++)ڪوائف[순번]=0;ٻج_حالت=2;}
        else {ٻج_حالت=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(ٻج_حالت==2){while(لمبائي_قدر){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=لمبائي_قدر<32?لمبائي_قدر:32;memcpy(منزل_مقصود_قدر,다음,수);memset(다음,0,32);منزل_مقصود_قدر+=수;لمبائي_قدر-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(لمبائي_قدر){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t قدر=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&لمبائي_قدر;순번++,لمبائي_قدر--){*منزل_مقصود_قدر++=قدر&255;قدر>>=8;}}
    return 0;
}
