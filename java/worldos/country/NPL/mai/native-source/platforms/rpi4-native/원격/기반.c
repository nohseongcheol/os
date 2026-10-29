/* 커널 전용 할당기와 암호 난수 공급. 사용자 ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct 기억조각 { size_t 길이; struct 기억조각 *다음; int 사용; } 기억조각;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static 기억조각 *첫조각;
void *원격할당(size_t 길이) {
    if (!길이 || 길이>sizeof(기억터)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->길이=sizeof(기억터)-32;}
    for(기억조각 *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->길이>=길이){
        if(조각->길이>=길이+64){기억조각 *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->길이=길이;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void 원격해제(void *주소) {
    if(!주소)return;기억조각 *조각=(void*)((char*)주소-32);
    volatile unsigned char *지움=주소;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->길이+=32+조각->다음->길이;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *주소,size_t 길이){
    if(!주소)return 원격할당(길이);if(!길이){원격해제(주소);return 0;}
    기억조각 *조각=(void*)((char*)주소-32);void *새주소=원격할당(길이);
    if(새주소){memcpy(새주소,주소,길이<조각->길이?길이:조각->길이);원격해제(주소);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *말,int 글자){for(;;말++){if(*말==(char)글자)return(char*)말;if(!*말)return 0;}}
char *strstr(const char *말,const char *찾음){size_t 길이=strlen(찾음);for(;*말;말++)if(!strncmp(말,찾음,길이))return(char*)말;return 길이?0:(char*)말;}
char *strncpy(char *목적,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)목적[순번]=원본[순번];for(;순번<길이;순번++)목적[순번]=0;return 목적;}
char *strncat(char *목적,const char *원본,size_t 길이){char *끝=목적+strlen(목적);while(길이--&&*원본)*끝++=*원본++;*끝=0;return 목적;}
int strncasecmp(const char *가,const char *나,size_t 길이){while(길이--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *말,const char *구분,char **다음){if(!말)말=*다음;while(*말&&strchr(구분,*말))말++;if(!*말){*다음=말;return 0;}char *처음=말;while(*말&&!strchr(구분,*말))말++;if(*말)*말++=0;*다음=말;return 처음;}
unsigned long strtoul(const char *말, char **끝, int 밑) {
    const char *श्रोोत=말;unsigned long 값=0;int 음수=0,넘침=0;
    while(*말==' '||(*말>=9&&*말<=13))말++;
    if(*말=='-'||*말=='+')음수=*말++=='-';
    if((밑==0||밑==16)&&말[0]=='0'&&(말[1]=='x'||말[1]=='X')&&
       ((말[2]>='0'&&말[2]<='9')||(말[2]>='a'&&말[2]<='f')||(말[2]>='A'&&말[2]<='F'))) {밑=16;말+=2;}
    if(!밑)밑=*말=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)श्रोोत;return 0;}
    const char *처음=말;
    for(;;말++) {
        unsigned 글자=(unsigned char)*말;
        unsigned 수=글자>='0'&&글자<='9'?글자-'0':글자>='a'&&글자<='z'?글자-'a'+10:글자>='A'&&글자<='Z'?글자-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(값>(~0ul-수)/(unsigned)밑)넘침=1;
        if(!넘침)값=값*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(말==처음?श्रोोत:말);
    return 넘침?~0ul:음수?0ul-값:값;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int 씨앗상태;
void 원격요약(const void *자료, size_t 길이, unsigned char 결과[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, 자료, 길이); br_sha256_out(&문맥, 결과);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(स्थिति) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(स्थिति)))
int 원격난수(unsigned char *목적,unsigned 길이){
    if(!씨앗상태){volatile unsigned char *자료=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=자료[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=자료[8+순번];for(unsigned 순번=0;순번<40;순번++)자료[순번]=0;씨앗상태=2;}
        else {씨앗상태=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(씨앗상태==2){while(길이){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=길이<32?길이:32;memcpy(목적,다음,수);memset(다음,0,32);목적+=수;길이-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t 값=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*목적++=값&255;값>>=8;}}
    return 0;
}
