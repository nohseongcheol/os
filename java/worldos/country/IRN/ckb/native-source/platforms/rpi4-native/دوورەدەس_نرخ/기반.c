/* کوورەک_نرخ 전용 할당기와 نهێنوشە_نرخ 난수 공급. بەکارهێنەر ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct بیرگە_بلۆک_کردن { size_t درێژی_نرخ; struct بیرگە_بلۆک_کردن *다음; int 사용; } بیرگە_بلۆک_کردن;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static بیرگە_بلۆک_کردن *첫조각;
void *تەرخانکردن_دوورەدەس(size_t درێژی_نرخ) {
    if (!درێژی_نرخ || درێژی_نرخ>sizeof(기억터)-64) return 0;
    درێژی_نرخ=(درێژی_نرخ+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->درێژی_نرخ=sizeof(기억터)-32;}
    for(بیرگە_بلۆک_کردن *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->درێژی_نرخ>=درێژی_نرخ){
        if(조각->درێژی_نرخ>=درێژی_نرخ+64){بیرگە_بلۆک_کردن *새조각=(void*)((char*)조각+32+درێژی_نرخ);
            새조각->درێژی_نرخ=조각->درێژی_نرخ-درێژی_نرخ-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->درێژی_نرخ=درێژی_نرخ;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void وەشان_دوورەدەس(void *ناونیشان) {
    if(!ناونیشان)return;بیرگە_بلۆک_کردن *조각=(void*)((char*)ناونیشان-32);
    volatile unsigned char *지움=ناونیشان;for(size_t 순번=0;순번<조각->درێژی_نرخ;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->درێژی_نرخ+=32+조각->다음->درێژی_نرخ;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *ناونیشان,size_t درێژی_نرخ){
    if(!ناونیشان)return تەرخانکردن_دوورەدەس(درێژی_نرخ);if(!درێژی_نرخ){وەشان_دوورەدەس(ناونیشان);return 0;}
    بیرگە_بلۆک_کردن *조각=(void*)((char*)ناونیشان-32);void *새주소=تەرخانکردن_دوورەدەس(درێژی_نرخ);
    if(새주소){memcpy(새주소,ناونیشان,درێژی_نرخ<조각->درێژی_نرخ?درێژی_نرخ:조각->درێژی_نرخ);وەشان_دوورەدەس(ناونیشان);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *وشە_دەق,int نووسە_نرخ){for(;;وشە_دەق++){if(*وشە_دەق==(char)نووسە_نرخ)return(char*)وشە_دەق;if(!*وشە_دەق)return 0;}}
char *strstr(const char *وشە_دەق,const char *찾음){size_t درێژی_نرخ=strlen(찾음);for(;*وشە_دەق;وشە_دەق++)if(!strncmp(وشە_دەق,찾음,درێژی_نرخ))return(char*)وشە_دەق;return درێژی_نرخ?0:(char*)وشە_دەق;}
char *strncpy(char *جێمەبەست_نرخ,const char *원본,size_t درێژی_نرخ){size_t 순번=0;for(;순번<درێژی_نرخ&&원본[순번];순번++)جێمەبەست_نرخ[순번]=원본[순번];for(;순번<درێژی_نرخ;순번++)جێمەبەست_نرخ[순번]=0;return جێمەبەست_نرخ;}
char *strncat(char *جێمەبەست_نرخ,const char *원본,size_t درێژی_نرخ){char *끝=جێمەبەست_نرخ+strlen(جێمەبەست_نرخ);while(درێژی_نرخ--&&*원본)*끝++=*원본++;*끝=0;return جێمەبەست_نرخ;}
int strncasecmp(const char *가,const char *나,size_t درێژی_نرخ){while(درێژی_نرخ--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *وشە_دەق,const char *دێلیمیتەر_نرخ,char **다음){if(!وشە_دەق)وشە_دەق=*다음;while(*وشە_دەق&&strchr(دێلیمیتەر_نرخ,*وشە_دەق))وشە_دەق++;if(!*وشە_دەق){*다음=وشە_دەق;return 0;}char *처음=وشە_دەق;while(*وشە_دەق&&!strchr(دێلیمیتەر_نرخ,*وشە_دەق))وشە_دەق++;if(*وشە_دەق)*وشە_دەق++=0;*다음=وشە_دەق;return 처음;}
unsigned long strtoul(const char *وشە_دەق, char **끝, int 밑) {
    const char *ژێدەر=وشە_دەق;unsigned long نرخ=0;int 음수=0,لێوڕێژ_نرخ=0;
    while(*وشە_دەق==' '||(*وشە_دەق>=9&&*وشە_دەق<=13))وشە_دەق++;
    if(*وشە_دەق=='-'||*وشە_دەق=='+')음수=*وشە_دەق++=='-';
    if((밑==0||밑==16)&&وشە_دەق[0]=='0'&&(وشە_دەق[1]=='x'||وشە_دەق[1]=='X')&&
       ((وشە_دەق[2]>='0'&&وشە_دەق[2]<='9')||(وشە_دەق[2]>='a'&&وشە_دەق[2]<='f')||(وشە_دەق[2]>='A'&&وشە_دەق[2]<='F'))) {밑=16;وشە_دەق+=2;}
    if(!밑)밑=*وشە_دەق=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ژێدەر;return 0;}
    const char *처음=وشە_دەق;
    for(;;وشە_دەق++) {
        unsigned نووسە_نرخ=(unsigned char)*وشە_دەق;
        unsigned 수=نووسە_نرخ>='0'&&نووسە_نرخ<='9'?نووسە_نرخ-'0':نووسە_نرخ>='a'&&نووسە_نرخ<='z'?نووسە_نرخ-'a'+10:نووسە_نرخ>='A'&&نووسە_نرخ<='Z'?نووسە_نرخ-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(نرخ>(~0ul-수)/(unsigned)밑)لێوڕێژ_نرخ=1;
        if(!لێوڕێژ_نرخ)نرخ=نرخ*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(وشە_دەق==처음?ژێدەر:وشە_دەق);
    return لێوڕێژ_نرخ?~0ul:음수?0ul-نرخ:نرخ;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int تۆو_دۆخ;
void 원격요약(const void *دەیتا, size_t درێژی_نرخ, unsigned char 결과[32]) {
    br_sha256_context ریزکردنی_سیاق_نرخ;
    br_sha256_init(&ریزکردنی_سیاق_نرخ); br_sha256_update(&ریزکردنی_سیاق_نرخ, دەیتا, درێژی_نرخ); br_sha256_out(&ریزکردنی_سیاق_نرخ, 결과);
    memset(&ریزکردنی_سیاق_نرخ, 0, sizeof(ریزکردنی_سیاق_نرخ));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *جێمەبەست_نرخ,unsigned درێژی_نرخ){
    if(!تۆو_دۆخ){volatile unsigned char *دەیتا=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=دەیتا[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=دەیتا[8+순번];for(unsigned 순번=0;순번<40;순번++)دەیتا[순번]=0;تۆو_دۆخ=2;}
        else {تۆو_دۆخ=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(تۆو_دۆخ==2){while(درێژی_نرخ){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=درێژی_نرخ<32?درێژی_نرخ:32;memcpy(جێمەبەست_نرخ,다음,수);memset(다음,0,32);جێمەبەست_نرخ+=수;درێژی_نرخ-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(درێژی_نرخ){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t نرخ=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&درێژی_نرخ;순번++,درێژی_نرخ--){*جێمەبەست_نرخ++=نرخ&255;نرخ>>=8;}}
    return 0;
}
