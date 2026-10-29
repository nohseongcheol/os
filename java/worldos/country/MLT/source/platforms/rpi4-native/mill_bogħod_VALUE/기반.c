/* kernel_VALUE 전용 할당기와 password_VALUE 난수 공급. utent ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memorja_imblokka { size_t tul_VALUE; struct Memorja_imblokka *Li_Jmiss_element; int 사용; } Memorja_imblokka;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static Memorja_imblokka *첫조각;
void *alloka_mill_bogħod(size_t tul_VALUE) {
    if (!tul_VALUE || tul_VALUE>sizeof(기억터)-64) return 0;
    tul_VALUE=(tul_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->tul_VALUE=sizeof(기억터)-32;}
    for(Memorja_imblokka *조각=첫조각;조각;조각=조각->Li_Jmiss_element)if(!조각->사용&&조각->tul_VALUE>=tul_VALUE){
        if(조각->tul_VALUE>=tul_VALUE+64){Memorja_imblokka *새조각=(void*)((char*)조각+32+tul_VALUE);
            새조각->tul_VALUE=조각->tul_VALUE-tul_VALUE-32;새조각->Li_Jmiss_element=조각->Li_Jmiss_element;새조각->사용=0;조각->Li_Jmiss_element=새조각;조각->tul_VALUE=tul_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void mexxi_mill_bogħod(void *ADDRESS) {
    if(!ADDRESS)return;Memorja_imblokka *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->tul_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Li_Jmiss_element;){if(!조각->사용&&!조각->Li_Jmiss_element->사용){조각->tul_VALUE+=32+조각->Li_Jmiss_element->tul_VALUE;조각->Li_Jmiss_element=조각->Li_Jmiss_element->Li_Jmiss_element;}else 조각=조각->Li_Jmiss_element;}
}
void *원격재할당(void *ADDRESS,size_t tul_VALUE){
    if(!ADDRESS)return alloka_mill_bogħod(tul_VALUE);if(!tul_VALUE){mexxi_mill_bogħod(ADDRESS);return 0;}
    Memorja_imblokka *조각=(void*)((char*)ADDRESS-32);void *새주소=alloka_mill_bogħod(tul_VALUE);
    if(새주소){memcpy(새주소,ADDRESS,tul_VALUE<조각->tul_VALUE?tul_VALUE:조각->tul_VALUE);mexxi_mill_bogħod(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int karattru_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)karattru_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t tul_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,tul_VALUE))return(char*)Word_SMS;return tul_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *destinazzjoni_VALUE,const char *원본,size_t tul_VALUE){size_t 순번=0;for(;순번<tul_VALUE&&원본[순번];순번++)destinazzjoni_VALUE[순번]=원본[순번];for(;순번<tul_VALUE;순번++)destinazzjoni_VALUE[순번]=0;return destinazzjoni_VALUE;}
char *strncat(char *destinazzjoni_VALUE,const char *원본,size_t tul_VALUE){char *끝=destinazzjoni_VALUE+strlen(destinazzjoni_VALUE);while(tul_VALUE--&&*원본)*끝++=*원본++;*끝=0;return destinazzjoni_VALUE;}
int strncasecmp(const char *가,const char *나,size_t tul_VALUE){while(tul_VALUE--){unsigned 첫글자=*가++,SECOND_karattru=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_karattru>='A'&&SECOND_karattru<='Z')SECOND_karattru+=32;if(첫글자!=SECOND_karattru)return(int)첫글자-(int)SECOND_karattru;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *delimitatur_VALUE,char **Li_Jmiss_element){if(!Word_SMS)Word_SMS=*Li_Jmiss_element;while(*Word_SMS&&strchr(delimitatur_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Li_Jmiss_element=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(delimitatur_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Li_Jmiss_element=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *sors=Word_SMS;unsigned long VALUE=0;int 음수=0,overflow_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)sors;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned karattru_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=karattru_VALUE>='0'&&karattru_VALUE<='9'?karattru_VALUE-'0':karattru_VALUE>='a'&&karattru_VALUE<='z'?karattru_VALUE-'a'+10:karattru_VALUE>='A'&&karattru_VALUE<='Z'?karattru_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)overflow_VALUE=1;
        if(!overflow_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?sors:Word_SMS);
    return overflow_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int valur_inizjali_stat;
void mill_bogħod_sommarju(const void *data, size_t tul_VALUE, unsigned char miżura[32]) {
    br_sha256_context Kuntest_VALUE;
    br_sha256_init(&Kuntest_VALUE); br_sha256_update(&Kuntest_VALUE, data, tul_VALUE); br_sha256_out(&Kuntest_VALUE, miżura);
    memset(&Kuntest_VALUE, 0, sizeof(Kuntest_VALUE));
}
#define 난수저장기(pożizzjoni) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(pożizzjoni)))
int 원격난수(unsigned char *destinazzjoni_VALUE,unsigned tul_VALUE){
    if(!valur_inizjali_stat){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;valur_inizjali_stat=2;}
        else {valur_inizjali_stat=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(valur_inizjali_stat==2){while(tul_VALUE){unsigned char Li_Jmiss_element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;mill_bogħod_sommarju(입력,33,Li_Jmiss_element);
        입력[32]=1;mill_bogħod_sommarju(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=tul_VALUE<32?tul_VALUE:32;memcpy(destinazzjoni_VALUE,Li_Jmiss_element,수);memset(Li_Jmiss_element,0,32);destinazzjoni_VALUE+=수;tul_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(tul_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&tul_VALUE;순번++,tul_VALUE--){*destinazzjoni_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
