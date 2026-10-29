/* कर्नेल_मान 전용 할당기와 पासवर्ड_मान 난수 공급. उपयोगकर्ता ELF의 libc와 별개이다. */
#include "क्रिप्टोग्राफ़ी_समर्थन.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct मेमोरी_ब्_लॉक { size_t 길이; struct मेमोरी_ब्_लॉक *अगला_आइटम; int 사용; } मेमोरी_ब्_लॉक;
static unsigned char मेमोरी_एरेना[2*1024*1024] __attribute__((aligned(16)));
static मेमोरी_ब्_लॉक *첫조각;
void *आवंटित_करें_दूरस्थ(size_t 길이) {
    if (!길이 || 길이>sizeof(मेमोरी_एरेना)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)मेमोरी_एरेना;첫조각->길이=sizeof(मेमोरी_एरेना)-32;}
    for(मेमोरी_ब्_लॉक *조각=첫조각;조각;조각=조각->अगला_आइटम)if(!조각->사용&&조각->길이>=길이){
        if(조각->길이>=길이+64){मेमोरी_ब्_लॉक *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->अगला_आइटम=조각->अगला_आइटम;새조각->사용=0;조각->अगला_आइटम=새조각;조각->길이=길이;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void रिलीज़_दूरस्थ(void *पता) {
    if(!पता)return;मेमोरी_ब्_लॉक *조각=(void*)((char*)पता-32);
    volatile unsigned char *지움=पता;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->अगला_आइटम;){if(!조각->사용&&!조각->अगला_आइटम->사용){조각->길이+=32+조각->अगला_आइटम->길이;조각->अगला_आइटम=조각->अगला_आइटम->अगला_आइटम;}else 조각=조각->अगला_आइटम;}
}
void *원격재할당(void *पता,size_t 길이){
    if(!पता)return आवंटित_करें_दूरस्थ(길이);if(!길이){रिलीज़_दूरस्थ(पता);return 0;}
    मेमोरी_ब्_लॉक *조각=(void*)((char*)पता-32);void *새주소=आवंटित_करें_दूरस्थ(길이);
    if(새주소){memcpy(새주소,पता,길이<조각->길이?길이:조각->길이);रिलीज़_दूरस्थ(पता);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *शब्द_पाठ,int कैरेक्टर_मान){for(;;शब्द_पाठ++){if(*शब्द_पाठ==(char)कैरेक्टर_मान)return(char*)शब्द_पाठ;if(!*शब्द_पाठ)return 0;}}
char *strstr(const char *शब्द_पाठ,const char *찾음){size_t 길이=strlen(찾음);for(;*शब्द_पाठ;शब्द_पाठ++)if(!strncmp(शब्द_पाठ,찾음,길이))return(char*)शब्द_पाठ;return 길이?0:(char*)शब्द_पाठ;}
char *strncpy(char *गंतव्य_मान,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)गंतव्य_मान[순번]=원본[순번];for(;순번<길이;순번++)गंतव्य_मान[순번]=0;return गंतव्य_मान;}
char *strncat(char *गंतव्य_मान,const char *원본,size_t 길이){char *끝=गंतव्य_मान+strlen(गंतव्य_मान);while(길이--&&*원본)*끝++=*원본++;*끝=0;return गंतव्य_मान;}
int strncasecmp(const char *가,const char *나,size_t 길이){while(길이--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *शब्द_पाठ,const char *डिलिमिटर_मान,char **अगला_आइटम){if(!शब्द_पाठ)शब्द_पाठ=*अगला_आइटम;while(*शब्द_पाठ&&strchr(डिलिमिटर_मान,*शब्द_पाठ))शब्द_पाठ++;if(!*शब्द_पाठ){*अगला_आइटम=शब्द_पाठ;return 0;}char *처음=शब्द_पाठ;while(*शब्द_पाठ&&!strchr(डिलिमिटर_मान,*शब्द_पाठ))शब्द_पाठ++;if(*शब्द_पाठ)*शब्द_पाठ++=0;*अगला_आइटम=शब्द_पाठ;return 처음;}
unsigned long strtoul(const char *शब्द_पाठ, char **끝, int 밑) {
    const char *स्रोत=शब्द_पाठ;unsigned long मान=0;int 음수=0,ओवरफ्लो_मान=0;
    while(*शब्द_पाठ==' '||(*शब्द_पाठ>=9&&*शब्द_पाठ<=13))शब्द_पाठ++;
    if(*शब्द_पाठ=='-'||*शब्द_पाठ=='+')음수=*शब्द_पाठ++=='-';
    if((밑==0||밑==16)&&शब्द_पाठ[0]=='0'&&(शब्द_पाठ[1]=='x'||शब्द_पाठ[1]=='X')&&
       ((शब्द_पाठ[2]>='0'&&शब्द_पाठ[2]<='9')||(शब्द_पाठ[2]>='a'&&शब्द_पाठ[2]<='f')||(शब्द_पाठ[2]>='A'&&शब्द_पाठ[2]<='F'))) {밑=16;शब्द_पाठ+=2;}
    if(!밑)밑=*शब्द_पाठ=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)स्रोत;return 0;}
    const char *처음=शब्द_पाठ;
    for(;;शब्द_पाठ++) {
        unsigned कैरेक्टर_मान=(unsigned char)*शब्द_पाठ;
        unsigned 수=कैरेक्टर_मान>='0'&&कैरेक्टर_मान<='9'?कैरेक्टर_मान-'0':कैरेक्टर_मान>='a'&&कैरेक्टर_मान<='z'?कैरेक्टर_मान-'a'+10:कैरेक्टर_मान>='A'&&कैरेक्टर_मान<='Z'?कैरेक्टर_मान-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(मान>(~0ul-수)/(unsigned)밑)ओवरफ्लो_मान=1;
        if(!ओवरफ्लो_मान)मान=मान*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(शब्द_पाठ==처음?स्रोत:शब्द_पाठ);
    return ओवरफ्लो_मान?~0ul:음수?0ul-मान:मान;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int मूल_अवस्था;
void दूरस्थ_सारांश(const void *आँकड़े, size_t 길이, unsigned char परिणाम[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, आँकड़े, 길이); br_sha256_out(&문맥, परिणाम);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(स्थान) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(स्थान)))
int दूरस्थ_यादृच्_छिक(unsigned char *गंतव्य_मान,unsigned 길이){
    if(!मूल_अवस्था){volatile unsigned char *आँकड़े=(void*)0x01ff0000ul;const char *मार्कर_मान="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=आँकड़े[순번]^(unsigned char)मार्कर_मान[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=आँकड़े[8+순번];for(unsigned 순번=0;순번<40;순번++)आँकड़े[순번]=0;मूल_अवस्था=2;}
        else {मूल_अवस्था=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(मूल_अवस्था==2){while(길이){unsigned char अगला_आइटम[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;दूरस्थ_सारांश(입력,33,अगला_आइटम);
        입력[32]=1;दूरस्थ_सारांश(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=길이<32?길이:32;memcpy(गंतव्य_मान,अगला_आइटम,수);memset(अगला_आइटम,0,32);गंतव्य_मान+=수;길이-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t मान=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*गंतव्य_मान++=मान&255;मान>>=8;}}
    return 0;
}
