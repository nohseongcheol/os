/* tuum_VALUE 전용 할당기와 parool_VALUE 난수 공급. kasutaja ELF의 libc와 별개이다. */
#include "krüptograafia_tugi.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Mälu_plokk { size_t 길이; struct Mälu_plokk *Edasi_kaup; int kasutus_VALUE; } Mälu_plokk;
static unsigned char Mälu_Areen[2*1024*1024] __attribute__((aligned(16)));
static Mälu_plokk *첫조각;
void *lisama_kauge(size_t 길이) {
    if (!길이 || 길이>sizeof(Mälu_Areen)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Mälu_Areen;첫조각->길이=sizeof(Mälu_Areen)-32;}
    for(Mälu_plokk *조각=첫조각;조각;조각=조각->Edasi_kaup)if(!조각->kasutus_VALUE&&조각->길이>=길이){
        if(조각->길이>=길이+64){Mälu_plokk *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->Edasi_kaup=조각->Edasi_kaup;새조각->kasutus_VALUE=0;조각->Edasi_kaup=새조각;조각->길이=길이;}
        조각->kasutus_VALUE=1;return(char*)조각+32;
    }return 0;
}
void vabastama_kauge(void *ADDRESS) {
    if(!ADDRESS)return;Mälu_plokk *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->kasutus_VALUE=0;
    for(조각=첫조각;조각&&조각->Edasi_kaup;){if(!조각->kasutus_VALUE&&!조각->Edasi_kaup->kasutus_VALUE){조각->길이+=32+조각->Edasi_kaup->길이;조각->Edasi_kaup=조각->Edasi_kaup->Edasi_kaup;}else 조각=조각->Edasi_kaup;}
}
void *원격재할당(void *ADDRESS,size_t 길이){
    if(!ADDRESS)return lisama_kauge(길이);if(!길이){vabastama_kauge(ADDRESS);return 0;}
    Mälu_plokk *조각=(void*)((char*)ADDRESS-32);void *새주소=lisama_kauge(길이);
    if(새주소){memcpy(새주소,ADDRESS,길이<조각->길이?길이:조각->길이);vabastama_kauge(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operand){while(*가&&*가==*SECOND_operand){가++;SECOND_operand++;}return(unsigned char)*가-(unsigned char)*SECOND_operand;}
char *strchr(const char *Word_SMS,int märk_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)märk_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t 길이=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,길이))return(char*)Word_SMS;return 길이?0:(char*)Word_SMS;}
char *strncpy(char *sihtkoht_VALUE,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)sihtkoht_VALUE[순번]=원본[순번];for(;순번<길이;순번++)sihtkoht_VALUE[순번]=0;return sihtkoht_VALUE;}
char *strncat(char *sihtkoht_VALUE,const char *원본,size_t 길이){char *끝=sihtkoht_VALUE+strlen(sihtkoht_VALUE);while(길이--&&*원본)*끝++=*원본++;*끝=0;return sihtkoht_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operand,size_t 길이){while(길이--){unsigned 첫글자=*가++,SECOND_märk=*SECOND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_märk>='A'&&SECOND_märk<='Z')SECOND_märk+=32;if(첫글자!=SECOND_märk)return(int)첫글자-(int)SECOND_märk;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operand){return strncasecmp(가,SECOND_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *eraldaja_VALUE_d8ba4873,char **Edasi_kaup){if(!Word_SMS)Word_SMS=*Edasi_kaup;while(*Word_SMS&&strchr(eraldaja_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Edasi_kaup=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(eraldaja_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Edasi_kaup=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *ALLIKAS=Word_SMS;unsigned long VALUE=0;int 음수=0,ületäide_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)ALLIKAS;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned märk_VALUE=(unsigned char)*Word_SMS;
        unsigned number=märk_VALUE>='0'&&märk_VALUE<='9'?märk_VALUE-'0':märk_VALUE>='a'&&märk_VALUE<='z'?märk_VALUE-'a'+10:märk_VALUE>='A'&&märk_VALUE<='Z'?märk_VALUE-'A'+10:36;
        if(number>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-number)/(unsigned)BASE_VALUE)ületäide_VALUE=1;
        if(!ületäide_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+number;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?ALLIKAS:Word_SMS);
    return ületäide_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int seemendama_Olek;
void kauge_kokkuvõte(const void *andmed, size_t 길이, unsigned char TULEMUS[32]) {
    br_sha256_context kontekst_VALUE;
    br_sha256_init(&kontekst_VALUE); br_sha256_update(&kontekst_VALUE, andmed, 길이); br_sha256_out(&kontekst_VALUE, TULEMUS);
    memset(&kontekst_VALUE, 0, sizeof(kontekst_VALUE));
}
#define 난수저장기(Asukoht) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Asukoht)))
int kauge_juhuslik(unsigned char *sihtkoht_VALUE,unsigned 길이){
    if(!seemendama_Olek){volatile unsigned char *andmed=(void*)0x01ff0000ul;const char *marker_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=andmed[순번]^(unsigned char)marker_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=andmed[8+순번];for(unsigned 순번=0;순번<40;순번++)andmed[순번]=0;seemendama_Olek=2;}
        else {seemendama_Olek=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(seemendama_Olek==2){while(길이){unsigned char Edasi_kaup[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;kauge_kokkuvõte(입력,33,Edasi_kaup);
        입력[32]=1;kauge_kokkuvõte(입력,33,모의씨앗);memset(입력,0,33);
        unsigned number=길이<32?길이:32;memcpy(sihtkoht_VALUE,Edasi_kaup,number);memset(Edasi_kaup,0,32);sihtkoht_VALUE+=number;길이-=number;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*sihtkoht_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
