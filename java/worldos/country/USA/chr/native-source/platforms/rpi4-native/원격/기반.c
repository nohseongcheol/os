/* kernel_ᏧᎬᏩᎶᏗᏯ 전용 할당기와 ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ 난수 공급. ᎬᏗᏍᎩ ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ { size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; struct ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ *다음; int 사용; } ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ *첫조각;
void *원격할당(size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    if (!ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ || ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>sizeof(기억터)-64) return 0;
    ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=sizeof(기억터)-32;}
    for(ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){
        if(조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ>=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+64){ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ *새조각=(void*)((char*)조각+32+ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
            새조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ-ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void 원격해제(void *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
    if(!ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)return;ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ *조각=(void*)((char*)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ-32);
    volatile unsigned char *지움=ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;for(size_t 순번=0;순번<조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ+=32+조각->다음->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){
    if(!ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)return 원격할당(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);if(!ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){원격해제(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);return 0;}
    ᎠᏅᏓᏗᏍᏙ_ᎦᏐᎾᎸᏗᏍᏗᎢ *조각=(void*)((char*)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ-32);void *새주소=원격할당(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    if(새주소){memcpy(새주소,ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ<조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ?ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ:조각->ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);원격해제(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *말,int ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ){for(;;말++){if(*말==(char)ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)return(char*)말;if(!*말)return 0;}}
char *strstr(const char *말,const char *찾음){size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ=strlen(찾음);for(;*말;말++)if(!strncmp(말,찾음,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ))return(char*)말;return ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ?0:(char*)말;}
char *strncpy(char *ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ,const char *원본,size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){size_t 순번=0;for(;순번<ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ&&원본[순번];순번++)ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ[순번]=원본[순번];for(;순번<ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;순번++)ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ[순번]=0;return ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ;}
char *strncat(char *ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ,const char *원본,size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){char *끝=ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ+strlen(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ);while(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ--&&*원본)*끝++=*원본++;*끝=0;return ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ;}
int strncasecmp(const char *가,const char *나,size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){while(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *말,const char *ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ,char **다음){if(!말)말=*다음;while(*말&&strchr(ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ,*말))말++;if(!*말){*다음=말;return 0;}char *처음=말;while(*말&&!strchr(ᏩᏍᏛᏍᎩᏊ_ᏧᎬᏩᎶᏗᏯ,*말))말++;if(*말)*말++=0;*다음=말;return 처음;}
unsigned long strtoul(const char *말, char **끝, int 밑) {
    const char *ᎦᏟᏌᏅᎯ_0201f362=말;unsigned long ᏧᎬᏩᎶᏗᏯ=0;int 음수=0,ᎬᎧᎵᏬᎯᏍᎩ_ᏧᎬᏩᎶᏗᏯ=0;
    while(*말==' '||(*말>=9&&*말<=13))말++;
    if(*말=='-'||*말=='+')음수=*말++=='-';
    if((밑==0||밑==16)&&말[0]=='0'&&(말[1]=='x'||말[1]=='X')&&
       ((말[2]>='0'&&말[2]<='9')||(말[2]>='a'&&말[2]<='f')||(말[2]>='A'&&말[2]<='F'))) {밑=16;말+=2;}
    if(!밑)밑=*말=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ᎦᏟᏌᏅᎯ_0201f362;return 0;}
    const char *처음=말;
    for(;;말++) {
        unsigned ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ=(unsigned char)*말;
        unsigned 수=ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ>='0'&&ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ<='9'?ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ-'0':ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ>='a'&&ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ<='z'?ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ-'a'+10:ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ>='A'&&ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ<='Z'?ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(ᏧᎬᏩᎶᏗᏯ>(~0ul-수)/(unsigned)밑)ᎬᎧᎵᏬᎯᏍᎩ_ᏧᎬᏩᎶᏗᏯ=1;
        if(!ᎬᎧᎵᏬᎯᏍᎩ_ᏧᎬᏩᎶᏗᏯ)ᏧᎬᏩᎶᏗᏯ=ᏧᎬᏩᎶᏗᏯ*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(말==처음?ᎦᏟᏌᏅᎯ_0201f362:말);
    return ᎬᎧᎵᏬᎯᏍᎩ_ᏧᎬᏩᎶᏗᏯ?~0ul:음수?0ul-ᏧᎬᏩᎶᏗᏯ:ᏧᎬᏩᎶᏗᏯ;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int 씨앗상태;
void 원격요약(const void *ᎦᏟᏌᏅᎯ, size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ, unsigned char 결과[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, ᎦᏟᏌᏅᎯ, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ); br_sha256_out(&문맥, 결과);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ,unsigned ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){
    if(!씨앗상태){volatile unsigned char *ᎦᏟᏌᏅᎯ=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=ᎦᏟᏌᏅᎯ[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=ᎦᏟᏌᏅᎯ[8+순번];for(unsigned 순번=0;순번<40;순번++)ᎦᏟᏌᏅᎯ[순번]=0;씨앗상태=2;}
        else {씨앗상태=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(씨앗상태==2){while(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ<32?ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ:32;memcpy(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ,다음,수);memset(다음,0,32);ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ+=수;ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t ᏧᎬᏩᎶᏗᏯ=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;순번++,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ--){*ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ++=ᏧᎬᏩᎶᏗᏯ&255;ᏧᎬᏩᎶᏗᏯ>>=8;}}
    return 0;
}
