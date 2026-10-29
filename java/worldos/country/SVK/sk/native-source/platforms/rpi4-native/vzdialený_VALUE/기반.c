/* jadro_VALUE 전용 할당기와 heslo_VALUE 난수 공급. používateľ ELF의 libc와 별개이다. */
#include "kryptografia_Podpora.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Pamäť_blok { size_t dĺžka_VALUE; struct Pamäť_blok *Ďalej_položka; int používať_VALUE; } Pamäť_blok;
static unsigned char Pamäť_Aréna[2*1024*1024] __attribute__((aligned(16)));
static Pamäť_blok *첫조각;
void *vyhradiť_vzdialený(size_t dĺžka_VALUE) {
    if (!dĺžka_VALUE || dĺžka_VALUE>sizeof(Pamäť_Aréna)-64) return 0;
    dĺžka_VALUE=(dĺžka_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Pamäť_Aréna;첫조각->dĺžka_VALUE=sizeof(Pamäť_Aréna)-32;}
    for(Pamäť_blok *조각=첫조각;조각;조각=조각->Ďalej_položka)if(!조각->používať_VALUE&&조각->dĺžka_VALUE>=dĺžka_VALUE){
        if(조각->dĺžka_VALUE>=dĺžka_VALUE+64){Pamäť_blok *새조각=(void*)((char*)조각+32+dĺžka_VALUE);
            새조각->dĺžka_VALUE=조각->dĺžka_VALUE-dĺžka_VALUE-32;새조각->Ďalej_položka=조각->Ďalej_položka;새조각->používať_VALUE=0;조각->Ďalej_položka=새조각;조각->dĺžka_VALUE=dĺžka_VALUE;}
        조각->používať_VALUE=1;return(char*)조각+32;
    }return 0;
}
void vydať_vzdialený(void *adresa) {
    if(!adresa)return;Pamäť_blok *조각=(void*)((char*)adresa-32);
    volatile unsigned char *지움=adresa;for(size_t 순번=0;순번<조각->dĺžka_VALUE;순번++)지움[순번]=0;
    조각->používať_VALUE=0;
    for(조각=첫조각;조각&&조각->Ďalej_položka;){if(!조각->používať_VALUE&&!조각->Ďalej_položka->používať_VALUE){조각->dĺžka_VALUE+=32+조각->Ďalej_položka->dĺžka_VALUE;조각->Ďalej_položka=조각->Ďalej_položka->Ďalej_položka;}else 조각=조각->Ďalej_položka;}
}
void *원격재할당(void *adresa,size_t dĺžka_VALUE){
    if(!adresa)return vyhradiť_vzdialený(dĺžka_VALUE);if(!dĺžka_VALUE){vydať_vzdialený(adresa);return 0;}
    Pamäť_blok *조각=(void*)((char*)adresa-32);void *새주소=vyhradiť_vzdialený(dĺžka_VALUE);
    if(새주소){memcpy(새주소,adresa,dĺžka_VALUE<조각->dĺžka_VALUE?dĺžka_VALUE:조각->dĺžka_VALUE);vydať_vzdialený(adresa);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operand){while(*가&&*가==*SECOND_operand){가++;SECOND_operand++;}return(unsigned char)*가-(unsigned char)*SECOND_operand;}
char *strchr(const char *Word_SMS,int znak_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)znak_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t dĺžka_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,dĺžka_VALUE))return(char*)Word_SMS;return dĺžka_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *cieľ_VALUE,const char *원본,size_t dĺžka_VALUE){size_t 순번=0;for(;순번<dĺžka_VALUE&&원본[순번];순번++)cieľ_VALUE[순번]=원본[순번];for(;순번<dĺžka_VALUE;순번++)cieľ_VALUE[순번]=0;return cieľ_VALUE;}
char *strncat(char *cieľ_VALUE,const char *원본,size_t dĺžka_VALUE){char *끝=cieľ_VALUE+strlen(cieľ_VALUE);while(dĺžka_VALUE--&&*원본)*끝++=*원본++;*끝=0;return cieľ_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operand,size_t dĺžka_VALUE){while(dĺžka_VALUE--){unsigned 첫글자=*가++,SECOND_znak=*SECOND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_znak>='A'&&SECOND_znak<='Z')SECOND_znak+=32;if(첫글자!=SECOND_znak)return(int)첫글자-(int)SECOND_znak;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operand){return strncasecmp(가,SECOND_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *oddeľovač_VALUE_d8ba4873,char **Ďalej_položka){if(!Word_SMS)Word_SMS=*Ďalej_položka;while(*Word_SMS&&strchr(oddeľovač_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Ďalej_položka=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(oddeľovač_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Ďalej_položka=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *ZDROJ=Word_SMS;unsigned long VALUE=0;int 음수=0,pretečenie_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)ZDROJ;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned znak_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=znak_VALUE>='0'&&znak_VALUE<='9'?znak_VALUE-'0':znak_VALUE>='a'&&znak_VALUE<='z'?znak_VALUE-'a'+10:znak_VALUE>='A'&&znak_VALUE<='Z'?znak_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)pretečenie_VALUE=1;
        if(!pretečenie_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?ZDROJ:Word_SMS);
    return pretečenie_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int počiatočná_hodnota_Stav;
void vzdialený_súhrn(const void *údaje, size_t dĺžka_VALUE, unsigned char KR[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, údaje, dĺžka_VALUE); br_sha256_out(&문맥, KR);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(Pozícia) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Pozícia)))
int vzdialený_náhodný(unsigned char *cieľ_VALUE,unsigned dĺžka_VALUE){
    if(!počiatočná_hodnota_Stav){volatile unsigned char *údaje=(void*)0x01ff0000ul;const char *fixka_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=údaje[순번]^(unsigned char)fixka_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=údaje[8+순번];for(unsigned 순번=0;순번<40;순번++)údaje[순번]=0;počiatočná_hodnota_Stav=2;}
        else {počiatočná_hodnota_Stav=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(počiatočná_hodnota_Stav==2){while(dĺžka_VALUE){unsigned char Ďalej_položka[32],vstup_VALUE[33];memcpy(vstup_VALUE,모의씨앗,32);vstup_VALUE[32]=0;vzdialený_súhrn(vstup_VALUE,33,Ďalej_položka);
        vstup_VALUE[32]=1;vzdialený_súhrn(vstup_VALUE,33,모의씨앗);memset(vstup_VALUE,0,33);
        unsigned 수=dĺžka_VALUE<32?dĺžka_VALUE:32;memcpy(cieľ_VALUE,Ďalej_položka,수);memset(Ďalej_položka,0,32);cieľ_VALUE+=수;dĺžka_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(dĺžka_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&dĺžka_VALUE;순번++,dĺžka_VALUE--){*cieľ_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
