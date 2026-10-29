/* јадро_VALUE 전용 할당기와 лозинка_VALUE 난수 공급. корисник ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Меморија_блокирај { size_t должина_VALUE; struct Меморија_блокирај *Следно_ставка; int 사용; } Меморија_блокирај;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static Меморија_блокирај *첫조각;
void *додели_далечинскo(size_t должина_VALUE) {
    if (!должина_VALUE || должина_VALUE>sizeof(기억터)-64) return 0;
    должина_VALUE=(должина_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->должина_VALUE=sizeof(기억터)-32;}
    for(Меморија_блокирај *조각=첫조각;조각;조각=조각->Следно_ставка)if(!조각->사용&&조각->должина_VALUE>=должина_VALUE){
        if(조각->должина_VALUE>=должина_VALUE+64){Меморија_блокирај *새조각=(void*)((char*)조각+32+должина_VALUE);
            새조각->должина_VALUE=조각->должина_VALUE-должина_VALUE-32;새조각->Следно_ставка=조각->Следно_ставка;새조각->사용=0;조각->Следно_ставка=새조각;조각->должина_VALUE=должина_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void издание_далечинскo(void *адреса) {
    if(!адреса)return;Меморија_блокирај *조각=(void*)((char*)адреса-32);
    volatile unsigned char *지움=адреса;for(size_t 순번=0;순번<조각->должина_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Следно_ставка;){if(!조각->사용&&!조각->Следно_ставка->사용){조각->должина_VALUE+=32+조각->Следно_ставка->должина_VALUE;조각->Следно_ставка=조각->Следно_ставка->Следно_ставка;}else 조각=조각->Следно_ставка;}
}
void *원격재할당(void *адреса,size_t должина_VALUE){
    if(!адреса)return додели_далечинскo(должина_VALUE);if(!должина_VALUE){издание_далечинскo(адреса);return 0;}
    Меморија_блокирај *조각=(void*)((char*)адреса-32);void *새주소=додели_далечинскo(должина_VALUE);
    if(새주소){memcpy(새주소,адреса,должина_VALUE<조각->должина_VALUE?должина_VALUE:조각->должина_VALUE);издание_далечинскo(адреса);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_СМС,int знак_VALUE){for(;;Word_СМС++){if(*Word_СМС==(char)знак_VALUE)return(char*)Word_СМС;if(!*Word_СМС)return 0;}}
char *strstr(const char *Word_СМС,const char *찾음){size_t должина_VALUE=strlen(찾음);for(;*Word_СМС;Word_СМС++)if(!strncmp(Word_СМС,찾음,должина_VALUE))return(char*)Word_СМС;return должина_VALUE?0:(char*)Word_СМС;}
char *strncpy(char *одредиште_VALUE,const char *원본,size_t должина_VALUE){size_t 순번=0;for(;순번<должина_VALUE&&원본[순번];순번++)одредиште_VALUE[순번]=원본[순번];for(;순번<должина_VALUE;순번++)одредиште_VALUE[순번]=0;return одредиште_VALUE;}
char *strncat(char *одредиште_VALUE,const char *원본,size_t должина_VALUE){char *끝=одредиште_VALUE+strlen(одредиште_VALUE);while(должина_VALUE--&&*원본)*끝++=*원본++;*끝=0;return одредиште_VALUE;}
int strncasecmp(const char *가,const char *나,size_t должина_VALUE){while(должина_VALUE--){unsigned 첫글자=*가++,SECOND_знак=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_знак>='A'&&SECOND_знак<='Z')SECOND_знак+=32;if(첫글자!=SECOND_знак)return(int)첫글자-(int)SECOND_знак;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_СМС,const char *разделник_VALUE_d8ba4873,char **Следно_ставка){if(!Word_СМС)Word_СМС=*Следно_ставка;while(*Word_СМС&&strchr(разделник_VALUE_d8ba4873,*Word_СМС))Word_СМС++;if(!*Word_СМС){*Следно_ставка=Word_СМС;return 0;}char *처음=Word_СМС;while(*Word_СМС&&!strchr(разделник_VALUE_d8ba4873,*Word_СМС))Word_СМС++;if(*Word_СМС)*Word_СМС++=0;*Следно_ставка=Word_СМС;return 처음;}
unsigned long strtoul(const char *Word_СМС, char **끝, int BASE_VALUE) {
    const char *ИЗВОР=Word_СМС;unsigned long VALUE=0;int 음수=0,прелевање_VALUE=0;
    while(*Word_СМС==' '||(*Word_СМС>=9&&*Word_СМС<=13))Word_СМС++;
    if(*Word_СМС=='-'||*Word_СМС=='+')음수=*Word_СМС++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_СМС[0]=='0'&&(Word_СМС[1]=='x'||Word_СМС[1]=='X')&&
       ((Word_СМС[2]>='0'&&Word_СМС[2]<='9')||(Word_СМС[2]>='a'&&Word_СМС[2]<='f')||(Word_СМС[2]>='A'&&Word_СМС[2]<='F'))) {BASE_VALUE=16;Word_СМС+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_СМС=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)ИЗВОР;return 0;}
    const char *처음=Word_СМС;
    for(;;Word_СМС++) {
        unsigned знак_VALUE=(unsigned char)*Word_СМС;
        unsigned 수=знак_VALUE>='0'&&знак_VALUE<='9'?знак_VALUE-'0':знак_VALUE>='a'&&знак_VALUE<='z'?знак_VALUE-'a'+10:знак_VALUE>='A'&&знак_VALUE<='Z'?знак_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)прелевање_VALUE=1;
        if(!прелевање_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_СМС==처음?ИЗВОР:Word_СМС);
    return прелевање_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int семе_статус;
void далечинскo_резиме(const void *податоци, size_t должина_VALUE, unsigned char мерка[32]) {
    br_sha256_context Контекст_VALUE;
    br_sha256_init(&Контекст_VALUE); br_sha256_update(&Контекст_VALUE, податоци, должина_VALUE); br_sha256_out(&Контекст_VALUE, мерка);
    memset(&Контекст_VALUE, 0, sizeof(Контекст_VALUE));
}
#define 난수저장기(Позиција) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Позиција)))
int 원격난수(unsigned char *одредиште_VALUE,unsigned должина_VALUE){
    if(!семе_статус){volatile unsigned char *податоци=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=податоци[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=податоци[8+순번];for(unsigned 순번=0;순번<40;순번++)податоци[순번]=0;семе_статус=2;}
        else {семе_статус=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(семе_статус==2){while(должина_VALUE){unsigned char Следно_ставка[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;далечинскo_резиме(입력,33,Следно_ставка);
        입력[32]=1;далечинскo_резиме(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=должина_VALUE<32?должина_VALUE:32;memcpy(одредиште_VALUE,Следно_ставка,수);memset(Следно_ставка,0,32);одредиште_VALUE+=수;должина_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(должина_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&должина_VALUE;순번++,должина_VALUE--){*одредиште_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
