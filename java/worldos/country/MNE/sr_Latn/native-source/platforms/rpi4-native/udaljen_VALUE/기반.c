/* jezgro_VALUE 전용 할당기와 lozinka_VALUE 난수 공급. korisnik ELF의 libc와 별개이다. */
#include "kriptografija_Podrška.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memorija_blok { size_t 길이; struct Memorija_blok *Dalje_stavka; int koristiti_VALUE; } Memorija_blok;
static unsigned char Memorija_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memorija_blok *첫조각;
void *dodeliti_udaljen(size_t 길이) {
    if (!길이 || 길이>sizeof(Memorija_Arena)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memorija_Arena;첫조각->길이=sizeof(Memorija_Arena)-32;}
    for(Memorija_blok *조각=첫조각;조각;조각=조각->Dalje_stavka)if(!조각->koristiti_VALUE&&조각->길이>=길이){
        if(조각->길이>=길이+64){Memorija_blok *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->Dalje_stavka=조각->Dalje_stavka;새조각->koristiti_VALUE=0;조각->Dalje_stavka=새조각;조각->길이=길이;}
        조각->koristiti_VALUE=1;return(char*)조각+32;
    }return 0;
}
void izdanje_udaljen(void *adresa) {
    if(!adresa)return;Memorija_blok *조각=(void*)((char*)adresa-32);
    volatile unsigned char *지움=adresa;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->koristiti_VALUE=0;
    for(조각=첫조각;조각&&조각->Dalje_stavka;){if(!조각->koristiti_VALUE&&!조각->Dalje_stavka->koristiti_VALUE){조각->길이+=32+조각->Dalje_stavka->길이;조각->Dalje_stavka=조각->Dalje_stavka->Dalje_stavka;}else 조각=조각->Dalje_stavka;}
}
void *원격재할당(void *adresa,size_t 길이){
    if(!adresa)return dodeliti_udaljen(길이);if(!길이){izdanje_udaljen(adresa);return 0;}
    Memorija_blok *조각=(void*)((char*)adresa-32);void *새주소=dodeliti_udaljen(길이);
    if(새주소){memcpy(새주소,adresa,길이<조각->길이?길이:조각->길이);izdanje_udaljen(adresa);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operand){while(*가&&*가==*SECOND_operand){가++;SECOND_operand++;}return(unsigned char)*가-(unsigned char)*SECOND_operand;}
char *strchr(const char *Word_SMS,int znak_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)znak_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t 길이=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,길이))return(char*)Word_SMS;return 길이?0:(char*)Word_SMS;}
char *strncpy(char *odredište_VALUE,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)odredište_VALUE[순번]=원본[순번];for(;순번<길이;순번++)odredište_VALUE[순번]=0;return odredište_VALUE;}
char *strncat(char *odredište_VALUE,const char *원본,size_t 길이){char *끝=odredište_VALUE+strlen(odredište_VALUE);while(길이--&&*원본)*끝++=*원본++;*끝=0;return odredište_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operand,size_t 길이){while(길이--){unsigned 첫글자=*가++,SECOND_znak=*SECOND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_znak>='A'&&SECOND_znak<='Z')SECOND_znak+=32;if(첫글자!=SECOND_znak)return(int)첫글자-(int)SECOND_znak;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operand){return strncasecmp(가,SECOND_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *znak_za_razgraničavanje_VALUE,char **Dalje_stavka){if(!Word_SMS)Word_SMS=*Dalje_stavka;while(*Word_SMS&&strchr(znak_za_razgraničavanje_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Dalje_stavka=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(znak_za_razgraničavanje_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Dalje_stavka=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *izvor=Word_SMS;unsigned long VALUE=0;int 음수=0,višak_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)izvor;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned znak_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=znak_VALUE>='0'&&znak_VALUE<='9'?znak_VALUE-'0':znak_VALUE>='a'&&znak_VALUE<='z'?znak_VALUE-'a'+10:znak_VALUE>='A'&&znak_VALUE<='Z'?znak_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)višak_VALUE=1;
        if(!višak_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?izvor:Word_SMS);
    return višak_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int dodati_Status;
void udaljen_rezime(const void *podaci, size_t 길이, unsigned char KR[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, podaci, 길이); br_sha256_out(&문맥, KR);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(pozicija) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(pozicija)))
int 원격난수(unsigned char *odredište_VALUE,unsigned 길이){
    if(!dodati_Status){volatile unsigned char *podaci=(void*)0x01ff0000ul;const char *označivač_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=podaci[순번]^(unsigned char)označivač_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=podaci[8+순번];for(unsigned 순번=0;순번<40;순번++)podaci[순번]=0;dodati_Status=2;}
        else {dodati_Status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(dodati_Status==2){while(길이){unsigned char Dalje_stavka[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;udaljen_rezime(입력,33,Dalje_stavka);
        입력[32]=1;udaljen_rezime(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=길이<32?길이:32;memcpy(odredište_VALUE,Dalje_stavka,수);memset(Dalje_stavka,0,32);odredište_VALUE+=수;길이-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*odredište_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
