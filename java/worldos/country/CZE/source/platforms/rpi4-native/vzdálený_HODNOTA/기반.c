/* jádro_HODNOTA 전용 할당기와 heslo_HODNOTA 난수 공급. uživatelský_prostor ELF의 libc와 별개이다. */
#include "šifrování_vzpěra.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Paměť_blok { size_t délka_HODNOTA; struct Paměť_blok *Další_zboží; int použít_HODNOTA; } Paměť_blok;
static unsigned char Paměť_Aréna[2*1024*1024] __attribute__((aligned(16)));
static Paměť_blok *첫조각;
void *přidělit_vzdálený(size_t délka_HODNOTA) {
    if (!délka_HODNOTA || délka_HODNOTA>sizeof(Paměť_Aréna)-64) return 0;
    délka_HODNOTA=(délka_HODNOTA+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Paměť_Aréna;첫조각->délka_HODNOTA=sizeof(Paměť_Aréna)-32;}
    for(Paměť_blok *조각=첫조각;조각;조각=조각->Další_zboží)if(!조각->použít_HODNOTA&&조각->délka_HODNOTA>=délka_HODNOTA){
        if(조각->délka_HODNOTA>=délka_HODNOTA+64){Paměť_blok *새조각=(void*)((char*)조각+32+délka_HODNOTA);
            새조각->délka_HODNOTA=조각->délka_HODNOTA-délka_HODNOTA-32;새조각->Další_zboží=조각->Další_zboží;새조각->použít_HODNOTA=0;조각->Další_zboží=새조각;조각->délka_HODNOTA=délka_HODNOTA;}
        조각->použít_HODNOTA=1;return(char*)조각+32;
    }return 0;
}
void verze_vzdálený(void *Adresa) {
    if(!Adresa)return;Paměť_blok *조각=(void*)((char*)Adresa-32);
    volatile unsigned char *지움=Adresa;for(size_t 순번=0;순번<조각->délka_HODNOTA;순번++)지움[순번]=0;
    조각->použít_HODNOTA=0;
    for(조각=첫조각;조각&&조각->Další_zboží;){if(!조각->použít_HODNOTA&&!조각->Další_zboží->použít_HODNOTA){조각->délka_HODNOTA+=32+조각->Další_zboží->délka_HODNOTA;조각->Další_zboží=조각->Další_zboží->Další_zboží;}else 조각=조각->Další_zboží;}
}
void *원격재할당(void *Adresa,size_t délka_HODNOTA){
    if(!Adresa)return přidělit_vzdálený(délka_HODNOTA);if(!délka_HODNOTA){verze_vzdálený(Adresa);return 0;}
    Paměť_blok *조각=(void*)((char*)Adresa-32);void *새주소=přidělit_vzdálený(délka_HODNOTA);
    if(새주소){memcpy(새주소,Adresa,délka_HODNOTA<조각->délka_HODNOTA?délka_HODNOTA:조각->délka_HODNOTA);verze_vzdálený(Adresa);}return 새주소;
}
int strcmp(const char *가,const char *SEKUNDA_operand){while(*가&&*가==*SEKUNDA_operand){가++;SEKUNDA_operand++;}return(unsigned char)*가-(unsigned char)*SEKUNDA_operand;}
char *strchr(const char *Word_SMS,int znak_HODNOTA){for(;;Word_SMS++){if(*Word_SMS==(char)znak_HODNOTA)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t délka_HODNOTA=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,délka_HODNOTA))return(char*)Word_SMS;return délka_HODNOTA?0:(char*)Word_SMS;}
char *strncpy(char *cíl_HODNOTA,const char *원본,size_t délka_HODNOTA){size_t 순번=0;for(;순번<délka_HODNOTA&&원본[순번];순번++)cíl_HODNOTA[순번]=원본[순번];for(;순번<délka_HODNOTA;순번++)cíl_HODNOTA[순번]=0;return cíl_HODNOTA;}
char *strncat(char *cíl_HODNOTA,const char *원본,size_t délka_HODNOTA){char *끝=cíl_HODNOTA+strlen(cíl_HODNOTA);while(délka_HODNOTA--&&*원본)*끝++=*원본++;*끝=0;return cíl_HODNOTA;}
int strncasecmp(const char *가,const char *SEKUNDA_operand,size_t délka_HODNOTA){while(délka_HODNOTA--){unsigned 첫글자=*가++,SEKUNDA_znak=*SEKUNDA_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEKUNDA_znak>='A'&&SEKUNDA_znak<='Z')SEKUNDA_znak+=32;if(첫글자!=SEKUNDA_znak)return(int)첫글자-(int)SEKUNDA_znak;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEKUNDA_operand){return strncasecmp(가,SEKUNDA_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *oddělovač_HODNOTA_d8ba4873,char **Další_zboží){if(!Word_SMS)Word_SMS=*Další_zboží;while(*Word_SMS&&strchr(oddělovač_HODNOTA_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Další_zboží=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(oddělovač_HODNOTA_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Další_zboží=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_HODNOTA) {
    const char *zdrojový_soubor=Word_SMS;unsigned long HODNOTA=0;int 음수=0,přetečení_HODNOTA=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_HODNOTA==0||BASE_HODNOTA==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_HODNOTA=16;Word_SMS+=2;}
    if(!BASE_HODNOTA)BASE_HODNOTA=*Word_SMS=='0'?8:10;
    if(BASE_HODNOTA<2||BASE_HODNOTA>36){if(끝)*끝=(char*)zdrojový_soubor;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned znak_HODNOTA=(unsigned char)*Word_SMS;
        unsigned číslo=znak_HODNOTA>='0'&&znak_HODNOTA<='9'?znak_HODNOTA-'0':znak_HODNOTA>='a'&&znak_HODNOTA<='z'?znak_HODNOTA-'a'+10:znak_HODNOTA>='A'&&znak_HODNOTA<='Z'?znak_HODNOTA-'A'+10:36;
        if(číslo>=(unsigned)BASE_HODNOTA)break;
        if(HODNOTA>(~0ul-číslo)/(unsigned)BASE_HODNOTA)přetečení_HODNOTA=1;
        if(!přetečení_HODNOTA)HODNOTA=HODNOTA*(unsigned)BASE_HODNOTA+číslo;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?zdrojový_soubor:Word_SMS);
    return přetečení_HODNOTA?~0ul:음수?0ul-HODNOTA:HODNOTA;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int přidat_Stav;
void vzdálený_souhrn(const void *data, size_t délka_HODNOTA, unsigned char VÝSLEDEK[32]) {
    br_sha256_context kontext_HODNOTA;
    br_sha256_init(&kontext_HODNOTA); br_sha256_update(&kontext_HODNOTA, data, délka_HODNOTA); br_sha256_out(&kontext_HODNOTA, VÝSLEDEK);
    memset(&kontext_HODNOTA, 0, sizeof(kontext_HODNOTA));
}
#define 난수저장기(pozice) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(pozice)))
int 원격난수(unsigned char *cíl_HODNOTA,unsigned délka_HODNOTA){
    if(!přidat_Stav){volatile unsigned char *data=(void*)0x01ff0000ul;const char *značka_HODNOTA_7e8f90bd="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)značka_HODNOTA_7e8f90bd[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;přidat_Stav=2;}
        else {přidat_Stav=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(přidat_Stav==2){while(délka_HODNOTA){unsigned char Další_zboží[32],vstup_HODNOTA[33];memcpy(vstup_HODNOTA,모의씨앗,32);vstup_HODNOTA[32]=0;vzdálený_souhrn(vstup_HODNOTA,33,Další_zboží);
        vstup_HODNOTA[32]=1;vzdálený_souhrn(vstup_HODNOTA,33,모의씨앗);memset(vstup_HODNOTA,0,33);
        unsigned číslo=délka_HODNOTA<32?délka_HODNOTA:32;memcpy(cíl_HODNOTA,Další_zboží,číslo);memset(Další_zboží,0,32);cíl_HODNOTA+=číslo;délka_HODNOTA-=číslo;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(délka_HODNOTA){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t HODNOTA=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&délka_HODNOTA;순번++,délka_HODNOTA--){*cíl_HODNOTA++=HODNOTA&255;HODNOTA>>=8;}}
    return 0;
}
