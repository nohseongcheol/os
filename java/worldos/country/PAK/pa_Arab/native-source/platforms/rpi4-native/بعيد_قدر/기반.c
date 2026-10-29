/* کرنل_قدر 전용 할당기와 لفظی_کنجی_قدر 난수 공급. صارف ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct میموری_بلاک { size_t لمبائی_قدر; struct میموری_بلاک *다음; int 사용; } میموری_بلاک;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static میموری_بلاک *첫조각;
void *مختص_کرو_بعيد(size_t لمبائی_قدر) {
    if (!لمبائی_قدر || لمبائی_قدر>sizeof(기억터)-64) return 0;
    لمبائی_قدر=(لمبائی_قدر+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->لمبائی_قدر=sizeof(기억터)-32;}
    for(میموری_بلاک *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->لمبائی_قدر>=لمبائی_قدر){
        if(조각->لمبائی_قدر>=لمبائی_قدر+64){میموری_بلاک *새조각=(void*)((char*)조각+32+لمبائی_قدر);
            새조각->لمبائی_قدر=조각->لمبائی_قدر-لمبائی_قدر-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->لمبائی_قدر=لمبائی_قدر;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void اجراء_بعيد(void *پتا) {
    if(!پتا)return;میموری_بلاک *조각=(void*)((char*)پتا-32);
    volatile unsigned char *지움=پتا;for(size_t 순번=0;순번<조각->لمبائی_قدر;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->لمبائی_قدر+=32+조각->다음->لمبائی_قدر;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *پتا,size_t لمبائی_قدر){
    if(!پتا)return مختص_کرو_بعيد(لمبائی_قدر);if(!لمبائی_قدر){اجراء_بعيد(پتا);return 0;}
    میموری_بلاک *조각=(void*)((char*)پتا-32);void *새주소=مختص_کرو_بعيد(لمبائی_قدر);
    if(새주소){memcpy(새주소,پتا,لمبائی_قدر<조각->لمبائی_قدر?لمبائی_قدر:조각->لمبائی_قدر);اجراء_بعيد(پتا);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *لفظ_متن,int کریکٹر_قدر){for(;;لفظ_متن++){if(*لفظ_متن==(char)کریکٹر_قدر)return(char*)لفظ_متن;if(!*لفظ_متن)return 0;}}
char *strstr(const char *لفظ_متن,const char *찾음){size_t لمبائی_قدر=strlen(찾음);for(;*لفظ_متن;لفظ_متن++)if(!strncmp(لفظ_متن,찾음,لمبائی_قدر))return(char*)لفظ_متن;return لمبائی_قدر?0:(char*)لفظ_متن;}
char *strncpy(char *منزل_مقصود_قدر,const char *원본,size_t لمبائی_قدر){size_t 순번=0;for(;순번<لمبائی_قدر&&원본[순번];순번++)منزل_مقصود_قدر[순번]=원본[순번];for(;순번<لمبائی_قدر;순번++)منزل_مقصود_قدر[순번]=0;return منزل_مقصود_قدر;}
char *strncat(char *منزل_مقصود_قدر,const char *원본,size_t لمبائی_قدر){char *끝=منزل_مقصود_قدر+strlen(منزل_مقصود_قدر);while(لمبائی_قدر--&&*원본)*끝++=*원본++;*끝=0;return منزل_مقصود_قدر;}
int strncasecmp(const char *가,const char *나,size_t لمبائی_قدر){while(لمبائی_قدر--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *لفظ_متن,const char *حد_بندی_کرنڑ_آلا_قدر,char **다음){if(!لفظ_متن)لفظ_متن=*다음;while(*لفظ_متن&&strchr(حد_بندی_کرنڑ_آلا_قدر,*لفظ_متن))لفظ_متن++;if(!*لفظ_متن){*다음=لفظ_متن;return 0;}char *처음=لفظ_متن;while(*لفظ_متن&&!strchr(حد_بندی_کرنڑ_آلا_قدر,*لفظ_متن))لفظ_متن++;if(*لفظ_متن)*لفظ_متن++=0;*다음=لفظ_متن;return 처음;}
unsigned long strtoul(const char *لفظ_متن, char **끝, int 밑) {
    const char *ماخذ=لفظ_متن;unsigned long قدر=0;int 음수=0,اوور_فلو_قدر=0;
    while(*لفظ_متن==' '||(*لفظ_متن>=9&&*لفظ_متن<=13))لفظ_متن++;
    if(*لفظ_متن=='-'||*لفظ_متن=='+')음수=*لفظ_متن++=='-';
    if((밑==0||밑==16)&&لفظ_متن[0]=='0'&&(لفظ_متن[1]=='x'||لفظ_متن[1]=='X')&&
       ((لفظ_متن[2]>='0'&&لفظ_متن[2]<='9')||(لفظ_متن[2]>='a'&&لفظ_متن[2]<='f')||(لفظ_متن[2]>='A'&&لفظ_متن[2]<='F'))) {밑=16;لفظ_متن+=2;}
    if(!밑)밑=*لفظ_متن=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ماخذ;return 0;}
    const char *처음=لفظ_متن;
    for(;;لفظ_متن++) {
        unsigned کریکٹر_قدر=(unsigned char)*لفظ_متن;
        unsigned 수=کریکٹر_قدر>='0'&&کریکٹر_قدر<='9'?کریکٹر_قدر-'0':کریکٹر_قدر>='a'&&کریکٹر_قدر<='z'?کریکٹر_قدر-'a'+10:کریکٹر_قدر>='A'&&کریکٹر_قدر<='Z'?کریکٹر_قدر-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(قدر>(~0ul-수)/(unsigned)밑)اوور_فلو_قدر=1;
        if(!اوور_فلو_قدر)قدر=قدر*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(لفظ_متن==처음?ماخذ:لفظ_متن);
    return اوور_فلو_قدر?~0ul:음수?0ul-قدر:قدر;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int نقلی_حالت;
void 원격요약(const void *کوائف, size_t لمبائی_قدر, unsigned char 결과[32]) {
    br_sha256_context سیاق_قدر;
    br_sha256_init(&سیاق_قدر); br_sha256_update(&سیاق_قدر, کوائف, لمبائی_قدر); br_sha256_out(&سیاق_قدر, 결과);
    memset(&سیاق_قدر, 0, sizeof(سیاق_قدر));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *منزل_مقصود_قدر,unsigned لمبائی_قدر){
    if(!نقلی_حالت){volatile unsigned char *کوائف=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=کوائف[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=کوائف[8+순번];for(unsigned 순번=0;순번<40;순번++)کوائف[순번]=0;نقلی_حالت=2;}
        else {نقلی_حالت=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(نقلی_حالت==2){while(لمبائی_قدر){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=لمبائی_قدر<32?لمبائی_قدر:32;memcpy(منزل_مقصود_قدر,다음,수);memset(다음,0,32);منزل_مقصود_قدر+=수;لمبائی_قدر-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(لمبائی_قدر){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t قدر=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&لمبائی_قدر;순번++,لمبائی_قدر--){*منزل_مقصود_قدر++=قدر&255;قدر>>=8;}}
    return 0;
}
