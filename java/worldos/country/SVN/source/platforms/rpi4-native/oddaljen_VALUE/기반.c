/* jedro_VALUE 전용 할당기와 geslo_VALUE 난수 공급. uporabnik ELF의 libc와 별개이다. */
#include "kriptografija_Podpora.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct pomnilnik_blok { size_t 길이; struct pomnilnik_blok *Naprej_element; int uporaba_VALUE; } pomnilnik_blok;
static unsigned char pomnilnik_Arena[2*1024*1024] __attribute__((aligned(16)));
static pomnilnik_blok *첫조각;
void *dodeliti_oddaljen(size_t 길이) {
    if (!길이 || 길이>sizeof(pomnilnik_Arena)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)pomnilnik_Arena;첫조각->길이=sizeof(pomnilnik_Arena)-32;}
    for(pomnilnik_blok *조각=첫조각;조각;조각=조각->Naprej_element)if(!조각->uporaba_VALUE&&조각->길이>=길이){
        if(조각->길이>=길이+64){pomnilnik_blok *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->Naprej_element=조각->Naprej_element;새조각->uporaba_VALUE=0;조각->Naprej_element=새조각;조각->길이=길이;}
        조각->uporaba_VALUE=1;return(char*)조각+32;
    }return 0;
}
void izdaja_oddaljen(void *naslov) {
    if(!naslov)return;pomnilnik_blok *조각=(void*)((char*)naslov-32);
    volatile unsigned char *지움=naslov;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->uporaba_VALUE=0;
    for(조각=첫조각;조각&&조각->Naprej_element;){if(!조각->uporaba_VALUE&&!조각->Naprej_element->uporaba_VALUE){조각->길이+=32+조각->Naprej_element->길이;조각->Naprej_element=조각->Naprej_element->Naprej_element;}else 조각=조각->Naprej_element;}
}
void *원격재할당(void *naslov,size_t 길이){
    if(!naslov)return dodeliti_oddaljen(길이);if(!길이){izdaja_oddaljen(naslov);return 0;}
    pomnilnik_blok *조각=(void*)((char*)naslov-32);void *새주소=dodeliti_oddaljen(길이);
    if(새주소){memcpy(새주소,naslov,길이<조각->길이?길이:조각->길이);izdaja_oddaljen(naslov);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operand){while(*가&&*가==*SECOND_operand){가++;SECOND_operand++;}return(unsigned char)*가-(unsigned char)*SECOND_operand;}
char *strchr(const char *Word_SMS,int znak_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)znak_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t 길이=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,길이))return(char*)Word_SMS;return 길이?0:(char*)Word_SMS;}
char *strncpy(char *cilj_VALUE,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)cilj_VALUE[순번]=원본[순번];for(;순번<길이;순번++)cilj_VALUE[순번]=0;return cilj_VALUE;}
char *strncat(char *cilj_VALUE,const char *원본,size_t 길이){char *끝=cilj_VALUE+strlen(cilj_VALUE);while(길이--&&*원본)*끝++=*원본++;*끝=0;return cilj_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operand,size_t 길이){while(길이--){unsigned 첫글자=*가++,SECOND_znak=*SECOND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_znak>='A'&&SECOND_znak<='Z')SECOND_znak+=32;if(첫글자!=SECOND_znak)return(int)첫글자-(int)SECOND_znak;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operand){return strncasecmp(가,SECOND_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *ločilo_VALUE_d8ba4873,char **Naprej_element){if(!Word_SMS)Word_SMS=*Naprej_element;while(*Word_SMS&&strchr(ločilo_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Naprej_element=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(ločilo_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Naprej_element=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *VIR=Word_SMS;unsigned long VALUE=0;int 음수=0,presežek_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)VIR;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned znak_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=znak_VALUE>='0'&&znak_VALUE<='9'?znak_VALUE-'0':znak_VALUE>='a'&&znak_VALUE<='z'?znak_VALUE-'a'+10:znak_VALUE>='A'&&znak_VALUE<='Z'?znak_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)presežek_VALUE=1;
        if(!presežek_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?VIR:Word_SMS);
    return presežek_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int seme_stanje;
void oddaljen_povzetek(const void *podatki, size_t 길이, unsigned char REZULTAT[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, podatki, 길이); br_sha256_out(&문맥, REZULTAT);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(Položaj) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Položaj)))
int 원격난수(unsigned char *cilj_VALUE,unsigned 길이){
    if(!seme_stanje){volatile unsigned char *podatki=(void*)0x01ff0000ul;const char *oznaka_VALUE_7e8f90bd="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=podatki[순번]^(unsigned char)oznaka_VALUE_7e8f90bd[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=podatki[8+순번];for(unsigned 순번=0;순번<40;순번++)podatki[순번]=0;seme_stanje=2;}
        else {seme_stanje=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(seme_stanje==2){while(길이){unsigned char Naprej_element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;oddaljen_povzetek(입력,33,Naprej_element);
        입력[32]=1;oddaljen_povzetek(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=길이<32?길이:32;memcpy(cilj_VALUE,Naprej_element,수);memset(Naprej_element,0,32);cilj_VALUE+=수;길이-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*cilj_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
