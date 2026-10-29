/* ዓንኳር_እሴት 전용 할당기와 የይለፍ_ቃል_እሴት 난수 공급. ተጠቃሚ ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ማስቀመጫ_አግድ { size_t ርዝመት_እሴት; struct ማስቀመጫ_አግድ *ቀጣይ_ንጥል_ነገር; int 사용; } ማስቀመጫ_አግድ;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ማስቀመጫ_አግድ *첫조각;
void *መደብ_የሩቅ(size_t ርዝመት_እሴት) {
    if (!ርዝመት_እሴት || ርዝመት_እሴት>sizeof(기억터)-64) return 0;
    ርዝመት_እሴት=(ርዝመት_እሴት+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->ርዝመት_እሴት=sizeof(기억터)-32;}
    for(ማስቀመጫ_አግድ *조각=첫조각;조각;조각=조각->ቀጣይ_ንጥል_ነገር)if(!조각->사용&&조각->ርዝመት_እሴት>=ርዝመት_እሴት){
        if(조각->ርዝመት_እሴት>=ርዝመት_እሴት+64){ማስቀመጫ_አግድ *새조각=(void*)((char*)조각+32+ርዝመት_እሴት);
            새조각->ርዝመት_እሴት=조각->ርዝመት_እሴት-ርዝመት_እሴት-32;새조각->ቀጣይ_ንጥል_ነገር=조각->ቀጣይ_ንጥል_ነገር;새조각->사용=0;조각->ቀጣይ_ንጥል_ነገር=새조각;조각->ርዝመት_እሴት=ርዝመት_እሴት;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void ልቀቅ_የሩቅ(void *አድራሻ) {
    if(!አድራሻ)return;ማስቀመጫ_አግድ *조각=(void*)((char*)አድራሻ-32);
    volatile unsigned char *지움=አድራሻ;for(size_t 순번=0;순번<조각->ርዝመት_እሴት;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->ቀጣይ_ንጥል_ነገር;){if(!조각->사용&&!조각->ቀጣይ_ንጥል_ነገር->사용){조각->ርዝመት_እሴት+=32+조각->ቀጣይ_ንጥል_ነገር->ርዝመት_እሴት;조각->ቀጣይ_ንጥል_ነገር=조각->ቀጣይ_ንጥል_ነገር->ቀጣይ_ንጥል_ነገር;}else 조각=조각->ቀጣይ_ንጥል_ነገር;}
}
void *원격재할당(void *አድራሻ,size_t ርዝመት_እሴት){
    if(!አድራሻ)return መደብ_የሩቅ(ርዝመት_እሴት);if(!ርዝመት_እሴት){ልቀቅ_የሩቅ(አድራሻ);return 0;}
    ማስቀመጫ_አግድ *조각=(void*)((char*)አድራሻ-32);void *새주소=መደብ_የሩቅ(ርዝመት_እሴት);
    if(새주소){memcpy(새주소,አድራሻ,ርዝመት_እሴት<조각->ርዝመት_እሴት?ርዝመት_እሴት:조각->ርዝመት_እሴት);ልቀቅ_የሩቅ(አድራሻ);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *ቃል_ጽሁፍ,int ቁምፊ_እሴት){for(;;ቃል_ጽሁፍ++){if(*ቃል_ጽሁፍ==(char)ቁምፊ_እሴት)return(char*)ቃል_ጽሁፍ;if(!*ቃል_ጽሁፍ)return 0;}}
char *strstr(const char *ቃል_ጽሁፍ,const char *찾음){size_t ርዝመት_እሴት=strlen(찾음);for(;*ቃል_ጽሁፍ;ቃል_ጽሁፍ++)if(!strncmp(ቃል_ጽሁፍ,찾음,ርዝመት_እሴት))return(char*)ቃል_ጽሁፍ;return ርዝመት_እሴት?0:(char*)ቃል_ጽሁፍ;}
char *strncpy(char *መድረሻ_እሴት,const char *원본,size_t ርዝመት_እሴት){size_t 순번=0;for(;순번<ርዝመት_እሴት&&원본[순번];순번++)መድረሻ_እሴት[순번]=원본[순번];for(;순번<ርዝመት_እሴት;순번++)መድረሻ_እሴት[순번]=0;return መድረሻ_እሴት;}
char *strncat(char *መድረሻ_እሴት,const char *원본,size_t ርዝመት_እሴት){char *끝=መድረሻ_እሴት+strlen(መድረሻ_እሴት);while(ርዝመት_እሴት--&&*원본)*끝++=*원본++;*끝=0;return መድረሻ_እሴት;}
int strncasecmp(const char *가,const char *나,size_t ርዝመት_እሴት){while(ርዝመት_እሴት--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *ቃል_ጽሁፍ,const char *ገዳቢ_እሴት,char **ቀጣይ_ንጥል_ነገር){if(!ቃል_ጽሁፍ)ቃል_ጽሁፍ=*ቀጣይ_ንጥል_ነገር;while(*ቃል_ጽሁፍ&&strchr(ገዳቢ_እሴት,*ቃል_ጽሁፍ))ቃል_ጽሁፍ++;if(!*ቃል_ጽሁፍ){*ቀጣይ_ንጥል_ነገር=ቃል_ጽሁፍ;return 0;}char *처음=ቃል_ጽሁፍ;while(*ቃል_ጽሁፍ&&!strchr(ገዳቢ_እሴት,*ቃል_ጽሁፍ))ቃል_ጽሁፍ++;if(*ቃል_ጽሁፍ)*ቃል_ጽሁፍ++=0;*ቀጣይ_ንጥል_ነገር=ቃል_ጽሁፍ;return 처음;}
unsigned long strtoul(const char *ቃል_ጽሁፍ, char **끝, int 밑) {
    const char *ምንጭ=ቃል_ጽሁፍ;unsigned long እሴት=0;int 음수=0,መትረፍ_እሴት=0;
    while(*ቃል_ጽሁፍ==' '||(*ቃል_ጽሁፍ>=9&&*ቃል_ጽሁፍ<=13))ቃል_ጽሁፍ++;
    if(*ቃል_ጽሁፍ=='-'||*ቃል_ጽሁፍ=='+')음수=*ቃል_ጽሁፍ++=='-';
    if((밑==0||밑==16)&&ቃል_ጽሁፍ[0]=='0'&&(ቃል_ጽሁፍ[1]=='x'||ቃል_ጽሁፍ[1]=='X')&&
       ((ቃል_ጽሁፍ[2]>='0'&&ቃል_ጽሁፍ[2]<='9')||(ቃል_ጽሁፍ[2]>='a'&&ቃል_ጽሁፍ[2]<='f')||(ቃል_ጽሁፍ[2]>='A'&&ቃል_ጽሁፍ[2]<='F'))) {밑=16;ቃል_ጽሁፍ+=2;}
    if(!밑)밑=*ቃል_ጽሁፍ=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ምንጭ;return 0;}
    const char *처음=ቃል_ጽሁፍ;
    for(;;ቃል_ጽሁፍ++) {
        unsigned ቁምፊ_እሴት=(unsigned char)*ቃል_ጽሁፍ;
        unsigned 수=ቁምፊ_እሴት>='0'&&ቁምፊ_እሴት<='9'?ቁምፊ_እሴት-'0':ቁምፊ_እሴት>='a'&&ቁምፊ_እሴት<='z'?ቁምፊ_እሴት-'a'+10:ቁምፊ_እሴት>='A'&&ቁምፊ_እሴት<='Z'?ቁምፊ_እሴት-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(እሴት>(~0ul-수)/(unsigned)밑)መትረፍ_እሴት=1;
        if(!መትረፍ_እሴት)እሴት=እሴት*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(ቃል_ጽሁፍ==처음?ምንጭ:ቃል_ጽሁፍ);
    return መትረፍ_እሴት?~0ul:음수?0ul-እሴት:እሴት;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int ዘር_ዞን;
void የሩቅ_ማጠቃለያ(const void *ውሂብ, size_t ርዝመት_እሴት, unsigned char ልኬት[32]) {
    br_sha256_context አገባበ_ነገር_እሴት;
    br_sha256_init(&አገባበ_ነገር_እሴት); br_sha256_update(&አገባበ_ነገር_እሴት, ውሂብ, ርዝመት_እሴት); br_sha256_out(&አገባበ_ነገር_እሴት, ልኬት);
    memset(&አገባበ_ነገር_እሴት, 0, sizeof(አገባበ_ነገር_እሴት));
}
#define 난수저장기(አካባቢ) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(አካባቢ)))
int 원격난수(unsigned char *መድረሻ_እሴት,unsigned ርዝመት_እሴት){
    if(!ዘር_ዞን){volatile unsigned char *ውሂብ=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=ውሂብ[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=ውሂብ[8+순번];for(unsigned 순번=0;순번<40;순번++)ውሂብ[순번]=0;ዘር_ዞን=2;}
        else {ዘር_ዞን=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(ዘር_ዞን==2){while(ርዝመት_እሴት){unsigned char ቀጣይ_ንጥል_ነገር[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;የሩቅ_ማጠቃለያ(입력,33,ቀጣይ_ንጥል_ነገር);
        입력[32]=1;የሩቅ_ማጠቃለያ(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=ርዝመት_እሴት<32?ርዝመት_እሴት:32;memcpy(መድረሻ_እሴት,ቀጣይ_ንጥል_ነገር,수);memset(ቀጣይ_ንጥል_ነገር,0,32);መድረሻ_እሴት+=수;ርዝመት_እሴት-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(ርዝመት_እሴት){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t እሴት=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&ርዝመት_እሴት;순번++,ርዝመት_እሴት--){*መድረሻ_እሴት++=እሴት&255;እሴት>>=8;}}
    return 0;
}
