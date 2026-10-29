/* nucleu_VALUE 전용 할당기와 parolă_VALUE 난수 공급. utilizator ELF의 libc와 별개이다. */
#include "criptografie_suport.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memorie_bloc { size_t lungime_VALUE; struct Memorie_bloc *Următorul_element; int utiliza_VALUE; } Memorie_bloc;
static unsigned char Memorie_Arenă[2*1024*1024] __attribute__((aligned(16)));
static Memorie_bloc *첫조각;
void *aloca_la_distanță(size_t lungime_VALUE) {
    if (!lungime_VALUE || lungime_VALUE>sizeof(Memorie_Arenă)-64) return 0;
    lungime_VALUE=(lungime_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memorie_Arenă;첫조각->lungime_VALUE=sizeof(Memorie_Arenă)-32;}
    for(Memorie_bloc *조각=첫조각;조각;조각=조각->Următorul_element)if(!조각->utiliza_VALUE&&조각->lungime_VALUE>=lungime_VALUE){
        if(조각->lungime_VALUE>=lungime_VALUE+64){Memorie_bloc *새조각=(void*)((char*)조각+32+lungime_VALUE);
            새조각->lungime_VALUE=조각->lungime_VALUE-lungime_VALUE-32;새조각->Următorul_element=조각->Următorul_element;새조각->utiliza_VALUE=0;조각->Următorul_element=새조각;조각->lungime_VALUE=lungime_VALUE;}
        조각->utiliza_VALUE=1;return(char*)조각+32;
    }return 0;
}
void lansa_la_distanță(void *adresa) {
    if(!adresa)return;Memorie_bloc *조각=(void*)((char*)adresa-32);
    volatile unsigned char *지움=adresa;for(size_t 순번=0;순번<조각->lungime_VALUE;순번++)지움[순번]=0;
    조각->utiliza_VALUE=0;
    for(조각=첫조각;조각&&조각->Următorul_element;){if(!조각->utiliza_VALUE&&!조각->Următorul_element->utiliza_VALUE){조각->lungime_VALUE+=32+조각->Următorul_element->lungime_VALUE;조각->Următorul_element=조각->Următorul_element->Următorul_element;}else 조각=조각->Următorul_element;}
}
void *원격재할당(void *adresa,size_t lungime_VALUE){
    if(!adresa)return aloca_la_distanță(lungime_VALUE);if(!lungime_VALUE){lansa_la_distanță(adresa);return 0;}
    Memorie_bloc *조각=(void*)((char*)adresa-32);void *새주소=aloca_la_distanță(lungime_VALUE);
    if(새주소){memcpy(새주소,adresa,lungime_VALUE<조각->lungime_VALUE?lungime_VALUE:조각->lungime_VALUE);lansa_la_distanță(adresa);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operand){while(*가&&*가==*SECOND_operand){가++;SECOND_operand++;}return(unsigned char)*가-(unsigned char)*SECOND_operand;}
char *strchr(const char *Word_SMS,int caracter_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)caracter_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t lungime_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,lungime_VALUE))return(char*)Word_SMS;return lungime_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *destinație_VALUE,const char *원본,size_t lungime_VALUE){size_t 순번=0;for(;순번<lungime_VALUE&&원본[순번];순번++)destinație_VALUE[순번]=원본[순번];for(;순번<lungime_VALUE;순번++)destinație_VALUE[순번]=0;return destinație_VALUE;}
char *strncat(char *destinație_VALUE,const char *원본,size_t lungime_VALUE){char *끝=destinație_VALUE+strlen(destinație_VALUE);while(lungime_VALUE--&&*원본)*끝++=*원본++;*끝=0;return destinație_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operand,size_t lungime_VALUE){while(lungime_VALUE--){unsigned 첫글자=*가++,SECOND_caracter=*SECOND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_caracter>='A'&&SECOND_caracter<='Z')SECOND_caracter+=32;if(첫글자!=SECOND_caracter)return(int)첫글자-(int)SECOND_caracter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operand){return strncasecmp(가,SECOND_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *delimitator_VALUE,char **Următorul_element){if(!Word_SMS)Word_SMS=*Următorul_element;while(*Word_SMS&&strchr(delimitator_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Următorul_element=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(delimitator_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Următorul_element=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *SURSĂ=Word_SMS;unsigned long VALUE=0;int 음수=0,depășire_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)SURSĂ;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned caracter_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=caracter_VALUE>='0'&&caracter_VALUE<='9'?caracter_VALUE-'0':caracter_VALUE>='a'&&caracter_VALUE<='z'?caracter_VALUE-'a'+10:caracter_VALUE>='A'&&caracter_VALUE<='Z'?caracter_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)depășire_VALUE=1;
        if(!depășire_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?SURSĂ:Word_SMS);
    return depășire_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int adăugare_sursă_Stare;
void la_distanță_rezumat(const void *date, size_t lungime_VALUE, unsigned char KR[32]) {
    br_sha256_context context_VALUE;
    br_sha256_init(&context_VALUE); br_sha256_update(&context_VALUE, date, lungime_VALUE); br_sha256_out(&context_VALUE, KR);
    memset(&context_VALUE, 0, sizeof(context_VALUE));
}
#define 난수저장기(Poziție) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Poziție)))
int la_distanță_aleator(unsigned char *destinație_VALUE,unsigned lungime_VALUE){
    if(!adăugare_sursă_Stare){volatile unsigned char *date=(void*)0x01ff0000ul;const char *marcaj_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=date[순번]^(unsigned char)marcaj_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=date[8+순번];for(unsigned 순번=0;순번<40;순번++)date[순번]=0;adăugare_sursă_Stare=2;}
        else {adăugare_sursă_Stare=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(adăugare_sursă_Stare==2){while(lungime_VALUE){unsigned char Următorul_element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;la_distanță_rezumat(입력,33,Următorul_element);
        입력[32]=1;la_distanță_rezumat(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=lungime_VALUE<32?lungime_VALUE:32;memcpy(destinație_VALUE,Următorul_element,수);memset(Următorul_element,0,32);destinație_VALUE+=수;lungime_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(lungime_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&lungime_VALUE;순번++,lungime_VALUE--){*destinație_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
