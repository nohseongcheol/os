/* ፍረ_ዋጋ 전용 할당기와 መሕለፊ_ቃል_ዋጋ 난수 공급. ተጠቃሚ ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ማህደር_ዝኽረት_ምዕጋት { size_t ንውሓት_ዋጋ; struct ማህደር_ዝኽረት_ምዕጋት *다음; int 사용; } ማህደር_ዝኽረት_ምዕጋት;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ማህደር_ዝኽረት_ምዕጋት *첫조각;
void *ምምዳብ_ርሑቕ(size_t ንውሓት_ዋጋ) {
    if (!ንውሓት_ዋጋ || ንውሓት_ዋጋ>sizeof(기억터)-64) return 0;
    ንውሓት_ዋጋ=(ንውሓት_ዋጋ+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->ንውሓት_ዋጋ=sizeof(기억터)-32;}
    for(ማህደር_ዝኽረት_ምዕጋት *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->ንውሓት_ዋጋ>=ንውሓት_ዋጋ){
        if(조각->ንውሓት_ዋጋ>=ንውሓት_ዋጋ+64){ማህደር_ዝኽረት_ምዕጋት *새조각=(void*)((char*)조각+32+ንውሓት_ዋጋ);
            새조각->ንውሓት_ዋጋ=조각->ንውሓት_ዋጋ-ንውሓት_ዋጋ-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->ንውሓት_ዋጋ=ንውሓት_ዋጋ;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void ፍታሕ_ርሑቕ(void *ኣድራሻ) {
    if(!ኣድራሻ)return;ማህደር_ዝኽረት_ምዕጋት *조각=(void*)((char*)ኣድራሻ-32);
    volatile unsigned char *지움=ኣድራሻ;for(size_t 순번=0;순번<조각->ንውሓት_ዋጋ;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->ንውሓት_ዋጋ+=32+조각->다음->ንውሓት_ዋጋ;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *ኣድራሻ,size_t ንውሓት_ዋጋ){
    if(!ኣድራሻ)return ምምዳብ_ርሑቕ(ንውሓት_ዋጋ);if(!ንውሓት_ዋጋ){ፍታሕ_ርሑቕ(ኣድራሻ);return 0;}
    ማህደር_ዝኽረት_ምዕጋት *조각=(void*)((char*)ኣድራሻ-32);void *새주소=ምምዳብ_ርሑቕ(ንውሓት_ዋጋ);
    if(새주소){memcpy(새주소,ኣድራሻ,ንውሓት_ዋጋ<조각->ንውሓት_ዋጋ?ንውሓት_ዋጋ:조각->ንውሓት_ዋጋ);ፍታሕ_ርሑቕ(ኣድራሻ);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *ናይ_ቃል_ጸወታ_ጽሑፍ,int ፊደል_ዋጋ){for(;;ናይ_ቃል_ጸወታ_ጽሑፍ++){if(*ናይ_ቃል_ጸወታ_ጽሑፍ==(char)ፊደል_ዋጋ)return(char*)ናይ_ቃል_ጸወታ_ጽሑፍ;if(!*ናይ_ቃል_ጸወታ_ጽሑፍ)return 0;}}
char *strstr(const char *ናይ_ቃል_ጸወታ_ጽሑፍ,const char *찾음){size_t ንውሓት_ዋጋ=strlen(찾음);for(;*ናይ_ቃል_ጸወታ_ጽሑፍ;ናይ_ቃል_ጸወታ_ጽሑፍ++)if(!strncmp(ናይ_ቃል_ጸወታ_ጽሑፍ,찾음,ንውሓት_ዋጋ))return(char*)ናይ_ቃል_ጸወታ_ጽሑፍ;return ንውሓት_ዋጋ?0:(char*)ናይ_ቃል_ጸወታ_ጽሑፍ;}
char *strncpy(char *መዓልቦ_ዋጋ,const char *원본,size_t ንውሓት_ዋጋ){size_t 순번=0;for(;순번<ንውሓት_ዋጋ&&원본[순번];순번++)መዓልቦ_ዋጋ[순번]=원본[순번];for(;순번<ንውሓት_ዋጋ;순번++)መዓልቦ_ዋጋ[순번]=0;return መዓልቦ_ዋጋ;}
char *strncat(char *መዓልቦ_ዋጋ,const char *원본,size_t ንውሓት_ዋጋ){char *끝=መዓልቦ_ዋጋ+strlen(መዓልቦ_ዋጋ);while(ንውሓት_ዋጋ--&&*원본)*끝++=*원본++;*끝=0;return መዓልቦ_ዋጋ;}
int strncasecmp(const char *가,const char *나,size_t ንውሓት_ዋጋ){while(ንውሓት_ዋጋ--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *ናይ_ቃል_ጸወታ_ጽሑፍ,const char *ደራቲ_ዋጋ,char **다음){if(!ናይ_ቃል_ጸወታ_ጽሑፍ)ናይ_ቃል_ጸወታ_ጽሑፍ=*다음;while(*ናይ_ቃል_ጸወታ_ጽሑፍ&&strchr(ደራቲ_ዋጋ,*ናይ_ቃል_ጸወታ_ጽሑፍ))ናይ_ቃል_ጸወታ_ጽሑፍ++;if(!*ናይ_ቃል_ጸወታ_ጽሑፍ){*다음=ናይ_ቃል_ጸወታ_ጽሑፍ;return 0;}char *처음=ናይ_ቃል_ጸወታ_ጽሑፍ;while(*ናይ_ቃል_ጸወታ_ጽሑፍ&&!strchr(ደራቲ_ዋጋ,*ናይ_ቃል_ጸወታ_ጽሑፍ))ናይ_ቃል_ጸወታ_ጽሑፍ++;if(*ናይ_ቃል_ጸወታ_ጽሑፍ)*ናይ_ቃል_ጸወታ_ጽሑፍ++=0;*다음=ናይ_ቃል_ጸወታ_ጽሑፍ;return 처음;}
unsigned long strtoul(const char *ናይ_ቃል_ጸወታ_ጽሑፍ, char **끝, int 밑) {
    const char *ምንጪ=ናይ_ቃል_ጸወታ_ጽሑፍ;unsigned long ዋጋ=0;int 음수=0,ፍሳስ_ዋጋ=0;
    while(*ናይ_ቃል_ጸወታ_ጽሑፍ==' '||(*ናይ_ቃል_ጸወታ_ጽሑፍ>=9&&*ናይ_ቃል_ጸወታ_ጽሑፍ<=13))ናይ_ቃል_ጸወታ_ጽሑፍ++;
    if(*ናይ_ቃል_ጸወታ_ጽሑፍ=='-'||*ናይ_ቃል_ጸወታ_ጽሑፍ=='+')음수=*ናይ_ቃል_ጸወታ_ጽሑፍ++=='-';
    if((밑==0||밑==16)&&ናይ_ቃል_ጸወታ_ጽሑፍ[0]=='0'&&(ናይ_ቃል_ጸወታ_ጽሑፍ[1]=='x'||ናይ_ቃል_ጸወታ_ጽሑፍ[1]=='X')&&
       ((ናይ_ቃል_ጸወታ_ጽሑፍ[2]>='0'&&ናይ_ቃል_ጸወታ_ጽሑፍ[2]<='9')||(ናይ_ቃል_ጸወታ_ጽሑፍ[2]>='a'&&ናይ_ቃል_ጸወታ_ጽሑፍ[2]<='f')||(ናይ_ቃል_ጸወታ_ጽሑፍ[2]>='A'&&ናይ_ቃል_ጸወታ_ጽሑፍ[2]<='F'))) {밑=16;ናይ_ቃል_ጸወታ_ጽሑፍ+=2;}
    if(!밑)밑=*ናይ_ቃል_ጸወታ_ጽሑፍ=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ምንጪ;return 0;}
    const char *처음=ናይ_ቃል_ጸወታ_ጽሑፍ;
    for(;;ናይ_ቃል_ጸወታ_ጽሑፍ++) {
        unsigned ፊደል_ዋጋ=(unsigned char)*ናይ_ቃል_ጸወታ_ጽሑፍ;
        unsigned 수=ፊደል_ዋጋ>='0'&&ፊደል_ዋጋ<='9'?ፊደል_ዋጋ-'0':ፊደል_ዋጋ>='a'&&ፊደል_ዋጋ<='z'?ፊደል_ዋጋ-'a'+10:ፊደል_ዋጋ>='A'&&ፊደል_ዋጋ<='Z'?ፊደል_ዋጋ-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(ዋጋ>(~0ul-수)/(unsigned)밑)ፍሳስ_ዋጋ=1;
        if(!ፍሳስ_ዋጋ)ዋጋ=ዋጋ*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(ናይ_ቃል_ጸወታ_ጽሑፍ==처음?ምንጪ:ናይ_ቃል_ጸወታ_ጽሑፍ);
    return ፍሳስ_ዋጋ?~0ul:음수?0ul-ዋጋ:ዋጋ;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int 씨앗상태;
void 원격요약(const void *ሓበሬታ, size_t ንውሓት_ዋጋ, unsigned char 결과[32]) {
    br_sha256_context ኣተኣታትዋ_ዋጋ;
    br_sha256_init(&ኣተኣታትዋ_ዋጋ); br_sha256_update(&ኣተኣታትዋ_ዋጋ, ሓበሬታ, ንውሓት_ዋጋ); br_sha256_out(&ኣተኣታትዋ_ዋጋ, 결과);
    memset(&ኣተኣታትዋ_ዋጋ, 0, sizeof(ኣተኣታትዋ_ዋጋ));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *መዓልቦ_ዋጋ,unsigned ንውሓት_ዋጋ){
    if(!씨앗상태){volatile unsigned char *ሓበሬታ=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=ሓበሬታ[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=ሓበሬታ[8+순번];for(unsigned 순번=0;순번<40;순번++)ሓበሬታ[순번]=0;씨앗상태=2;}
        else {씨앗상태=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(씨앗상태==2){while(ንውሓት_ዋጋ){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=ንውሓት_ዋጋ<32?ንውሓት_ዋጋ:32;memcpy(መዓልቦ_ዋጋ,다음,수);memset(다음,0,32);መዓልቦ_ዋጋ+=수;ንውሓት_ዋጋ-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(ንውሓት_ዋጋ){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t ዋጋ=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&ንውሓት_ዋጋ;순번++,ንውሓት_ዋጋ--){*መዓልቦ_ዋጋ++=ዋጋ&255;ዋጋ>>=8;}}
    return 0;
}
