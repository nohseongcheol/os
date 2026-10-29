/* कर्नेल_मोल 전용 할당기와 पासवर्ड_मोल 난수 공급. उपेगकर्तो ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct मेमरी_आडावचें { size_t लांबाय_मोल; struct मेमरी_आडावचें *फुडलें_आयटम; int 사용; } मेमरी_आडावचें;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static मेमरी_आडावचें *첫조각;
void *नेमून_दिवचें_दुर्मीळ(size_t लांबाय_मोल) {
    if (!लांबाय_मोल || लांबाय_मोल>sizeof(기억터)-64) return 0;
    लांबाय_मोल=(लांबाय_मोल+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->लांबाय_मोल=sizeof(기억터)-32;}
    for(मेमरी_आडावचें *조각=첫조각;조각;조각=조각->फुडलें_आयटम)if(!조각->사용&&조각->लांबाय_मोल>=लांबाय_मोल){
        if(조각->लांबाय_मोल>=लांबाय_मोल+64){मेमरी_आडावचें *새조각=(void*)((char*)조각+32+लांबाय_मोल);
            새조각->लांबाय_मोल=조각->लांबाय_मोल-लांबाय_मोल-32;새조각->फुडलें_आयटम=조각->फुडलें_आयटम;새조각->사용=0;조각->फुडलें_आयटम=새조각;조각->लांबाय_मोल=लांबाय_मोल;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void रिलीज_दुर्मीळ(void *नामो) {
    if(!नामो)return;मेमरी_आडावचें *조각=(void*)((char*)नामो-32);
    volatile unsigned char *지움=नामो;for(size_t 순번=0;순번<조각->लांबाय_मोल;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->फुडलें_आयटम;){if(!조각->사용&&!조각->फुडलें_आयटम->사용){조각->लांबाय_मोल+=32+조각->फुडलें_आयटम->लांबाय_मोल;조각->फुडलें_आयटम=조각->फुडलें_आयटम->फुडलें_आयटम;}else 조각=조각->फुडलें_आयटम;}
}
void *원격재할당(void *नामो,size_t लांबाय_मोल){
    if(!नामो)return नेमून_दिवचें_दुर्मीळ(लांबाय_मोल);if(!लांबाय_मोल){रिलीज_दुर्मीळ(नामो);return 0;}
    मेमरी_आडावचें *조각=(void*)((char*)नामो-32);void *새주소=नेमून_दिवचें_दुर्मीळ(लांबाय_मोल);
    if(새주소){memcpy(새주소,नामो,लांबाय_मोल<조각->लांबाय_मोल?लांबाय_मोल:조각->लांबाय_मोल);रिलीज_दुर्मीळ(नामो);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int वर्ण_मोल){for(;;Word_SMS++){if(*Word_SMS==(char)वर्ण_मोल)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t लांबाय_मोल=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,लांबाय_मोल))return(char*)Word_SMS;return लांबाय_मोल?0:(char*)Word_SMS;}
char *strncpy(char *नियुक्त_स्थान_मोल,const char *원본,size_t लांबाय_मोल){size_t 순번=0;for(;순번<लांबाय_मोल&&원본[순번];순번++)नियुक्त_स्थान_मोल[순번]=원본[순번];for(;순번<लांबाय_मोल;순번++)नियुक्त_स्थान_मोल[순번]=0;return नियुक्त_स्थान_मोल;}
char *strncat(char *नियुक्त_स्थान_मोल,const char *원본,size_t लांबाय_मोल){char *끝=नियुक्त_स्थान_मोल+strlen(नियुक्त_स्थान_मोल);while(लांबाय_मोल--&&*원본)*끝++=*원본++;*끝=0;return नियुक्त_स्थान_मोल;}
int strncasecmp(const char *가,const char *나,size_t लांबाय_मोल){while(लांबाय_मोल--){unsigned 첫글자=*가++,SECOND_वर्ण=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_वर्ण>='A'&&SECOND_वर्ण<='Z')SECOND_वर्ण+=32;if(첫글자!=SECOND_वर्ण)return(int)첫글자-(int)SECOND_वर्ण;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *डिलिमिटर_मोल,char **फुडलें_आयटम){if(!Word_SMS)Word_SMS=*फुडलें_आयटम;while(*Word_SMS&&strchr(डिलिमिटर_मोल,*Word_SMS))Word_SMS++;if(!*Word_SMS){*फुडलें_आयटम=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(डिलिमिटर_मोल,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*फुडलें_आयटम=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_मोल) {
    const char *स्त्रोत=Word_SMS;unsigned long मोल=0;int 음수=0,ओवरफ्लो_मोल=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_मोल==0||BASE_मोल==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_मोल=16;Word_SMS+=2;}
    if(!BASE_मोल)BASE_मोल=*Word_SMS=='0'?8:10;
    if(BASE_मोल<2||BASE_मोल>36){if(끝)*끝=(char*)स्त्रोत;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned वर्ण_मोल=(unsigned char)*Word_SMS;
        unsigned 수=वर्ण_मोल>='0'&&वर्ण_मोल<='9'?वर्ण_मोल-'0':वर्ण_मोल>='a'&&वर्ण_मोल<='z'?वर्ण_मोल-'a'+10:वर्ण_मोल>='A'&&वर्ण_मोल<='Z'?वर्ण_मोल-'A'+10:36;
        if(수>=(unsigned)BASE_मोल)break;
        if(मोल>(~0ul-수)/(unsigned)BASE_मोल)ओवरफ्लो_मोल=1;
        if(!ओवरफ्लो_मोल)मोल=मोल*(unsigned)BASE_मोल+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?स्त्रोत:Word_SMS);
    return ओवरफ्लो_मोल?~0ul:음수?0ul-मोल:मोल;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int सीड_स्थिती;
void दुर्मीळ_सारांश(const void *डेटा, size_t लांबाय_मोल, unsigned char मेजप[32]) {
    br_sha256_context मजकूर_मोल;
    br_sha256_init(&मजकूर_मोल); br_sha256_update(&मजकूर_मोल, डेटा, लांबाय_मोल); br_sha256_out(&मजकूर_मोल, मेजप);
    memset(&मजकूर_मोल, 0, sizeof(मजकूर_मोल));
}
#define 난수저장기(स्थिती) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(स्थिती)))
int 원격난수(unsigned char *नियुक्त_स्थान_मोल,unsigned लांबाय_मोल){
    if(!सीड_स्थिती){volatile unsigned char *डेटा=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=डेटा[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=डेटा[8+순번];for(unsigned 순번=0;순번<40;순번++)डेटा[순번]=0;सीड_स्थिती=2;}
        else {सीड_स्थिती=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(सीड_स्थिती==2){while(लांबाय_मोल){unsigned char फुडलें_आयटम[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;दुर्मीळ_सारांश(입력,33,फुडलें_आयटम);
        입력[32]=1;दुर्मीळ_सारांश(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=लांबाय_मोल<32?लांबाय_मोल:32;memcpy(नियुक्त_स्थान_मोल,फुडलें_आयटम,수);memset(फुडलें_आयटम,0,32);नियुक्त_स्थान_मोल+=수;लांबाय_मोल-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(लांबाय_मोल){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t मोल=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&लांबाय_मोल;순번++,लांबाय_मोल--){*नियुक्त_स्थान_मोल++=मोल&255;मोल>>=8;}}
    return 0;
}
