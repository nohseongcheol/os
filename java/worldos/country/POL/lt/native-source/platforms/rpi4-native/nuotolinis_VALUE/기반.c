/* branduolys_VALUE 전용 할당기와 slaptažodis_VALUE 난수 공급. naudotojas ELF의 libc와 별개이다. */
#include "kriptografija_pagalba.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct atmintis_blokas { size_t 길이; struct atmintis_blokas *toliau_prekė; int naudoti_VALUE; } atmintis_blokas;
static unsigned char atmintis_Arena[2*1024*1024] __attribute__((aligned(16)));
static atmintis_blokas *첫조각;
void *priskirti_nuotolinis(size_t 길이) {
    if (!길이 || 길이>sizeof(atmintis_Arena)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)atmintis_Arena;첫조각->길이=sizeof(atmintis_Arena)-32;}
    for(atmintis_blokas *조각=첫조각;조각;조각=조각->toliau_prekė)if(!조각->naudoti_VALUE&&조각->길이>=길이){
        if(조각->길이>=길이+64){atmintis_blokas *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->toliau_prekė=조각->toliau_prekė;새조각->naudoti_VALUE=0;조각->toliau_prekė=새조각;조각->길이=길이;}
        조각->naudoti_VALUE=1;return(char*)조각+32;
    }return 0;
}
void išleisti_nuotolinis(void *ADDRESS) {
    if(!ADDRESS)return;atmintis_blokas *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->naudoti_VALUE=0;
    for(조각=첫조각;조각&&조각->toliau_prekė;){if(!조각->naudoti_VALUE&&!조각->toliau_prekė->naudoti_VALUE){조각->길이+=32+조각->toliau_prekė->길이;조각->toliau_prekė=조각->toliau_prekė->toliau_prekė;}else 조각=조각->toliau_prekė;}
}
void *원격재할당(void *ADDRESS,size_t 길이){
    if(!ADDRESS)return priskirti_nuotolinis(길이);if(!길이){išleisti_nuotolinis(ADDRESS);return 0;}
    atmintis_blokas *조각=(void*)((char*)ADDRESS-32);void *새주소=priskirti_nuotolinis(길이);
    if(새주소){memcpy(새주소,ADDRESS,길이<조각->길이?길이:조각->길이);išleisti_nuotolinis(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operandas){while(*가&&*가==*SECOND_operandas){가++;SECOND_operandas++;}return(unsigned char)*가-(unsigned char)*SECOND_operandas;}
char *strchr(const char *Word_SMS,int simbolis_VALUE_068c2631){for(;;Word_SMS++){if(*Word_SMS==(char)simbolis_VALUE_068c2631)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t 길이=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,길이))return(char*)Word_SMS;return 길이?0:(char*)Word_SMS;}
char *strncpy(char *vieta_VALUE,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)vieta_VALUE[순번]=원본[순번];for(;순번<길이;순번++)vieta_VALUE[순번]=0;return vieta_VALUE;}
char *strncat(char *vieta_VALUE,const char *원본,size_t 길이){char *끝=vieta_VALUE+strlen(vieta_VALUE);while(길이--&&*원본)*끝++=*원본++;*끝=0;return vieta_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operandas,size_t 길이){while(길이--){unsigned 첫글자=*가++,SECOND_simbolis=*SECOND_operandas++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_simbolis>='A'&&SECOND_simbolis<='Z')SECOND_simbolis+=32;if(첫글자!=SECOND_simbolis)return(int)첫글자-(int)SECOND_simbolis;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operandas){return strncasecmp(가,SECOND_operandas,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *skyriklis_VALUE_d8ba4873,char **toliau_prekė){if(!Word_SMS)Word_SMS=*toliau_prekė;while(*Word_SMS&&strchr(skyriklis_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*toliau_prekė=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(skyriklis_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*toliau_prekė=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *ŠALTINIS=Word_SMS;unsigned long VALUE=0;int 음수=0,perpilda_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)ŠALTINIS;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned simbolis_VALUE_068c2631=(unsigned char)*Word_SMS;
        unsigned numeris=simbolis_VALUE_068c2631>='0'&&simbolis_VALUE_068c2631<='9'?simbolis_VALUE_068c2631-'0':simbolis_VALUE_068c2631>='a'&&simbolis_VALUE_068c2631<='z'?simbolis_VALUE_068c2631-'a'+10:simbolis_VALUE_068c2631>='A'&&simbolis_VALUE_068c2631<='Z'?simbolis_VALUE_068c2631-'A'+10:36;
        if(numeris>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-numeris)/(unsigned)BASE_VALUE)perpilda_VALUE=1;
        if(!perpilda_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+numeris;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?ŠALTINIS:Word_SMS);
    return perpilda_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int pirminė_reikšmė_Būsena;
void nuotolinis_suvestinė(const void *duomenys, size_t 길이, unsigned char REZULTATAS[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, duomenys, 길이); br_sha256_out(&문맥, REZULTATAS);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(Pozicija) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Pozicija)))
int nuotolinis_atsitiktinis(unsigned char *vieta_VALUE,unsigned 길이){
    if(!pirminė_reikšmė_Būsena){volatile unsigned char *duomenys=(void*)0x01ff0000ul;const char *žymeklis_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=duomenys[순번]^(unsigned char)žymeklis_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=duomenys[8+순번];for(unsigned 순번=0;순번<40;순번++)duomenys[순번]=0;pirminė_reikšmė_Būsena=2;}
        else {pirminė_reikšmė_Būsena=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(pirminė_reikšmė_Būsena==2){while(길이){unsigned char toliau_prekė[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;nuotolinis_suvestinė(입력,33,toliau_prekė);
        입력[32]=1;nuotolinis_suvestinė(입력,33,모의씨앗);memset(입력,0,33);
        unsigned numeris=길이<32?길이:32;memcpy(vieta_VALUE,toliau_prekė,numeris);memset(toliau_prekė,0,32);vieta_VALUE+=numeris;길이-=numeris;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*vieta_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
