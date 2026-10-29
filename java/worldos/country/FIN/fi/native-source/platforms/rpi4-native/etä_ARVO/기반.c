/* ydin_ARVO 전용 할당기와 salasana_ARVO 난수 공급. käyttäjätila ELF의 libc와 별개이다. */
#include "salaus_Tuki.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Muisti_Esto { size_t kesto_ARVO; struct Muisti_Esto *Seuraava_kohde; int käyttö_ARVO; } Muisti_Esto;
static unsigned char Muisti_Areena[2*1024*1024] __attribute__((aligned(16)));
static Muisti_Esto *첫조각;
void *jakaa_etä(size_t kesto_ARVO) {
    if (!kesto_ARVO || kesto_ARVO>sizeof(Muisti_Areena)-64) return 0;
    kesto_ARVO=(kesto_ARVO+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Muisti_Areena;첫조각->kesto_ARVO=sizeof(Muisti_Areena)-32;}
    for(Muisti_Esto *조각=첫조각;조각;조각=조각->Seuraava_kohde)if(!조각->käyttö_ARVO&&조각->kesto_ARVO>=kesto_ARVO){
        if(조각->kesto_ARVO>=kesto_ARVO+64){Muisti_Esto *새조각=(void*)((char*)조각+32+kesto_ARVO);
            새조각->kesto_ARVO=조각->kesto_ARVO-kesto_ARVO-32;새조각->Seuraava_kohde=조각->Seuraava_kohde;새조각->käyttö_ARVO=0;조각->Seuraava_kohde=새조각;조각->kesto_ARVO=kesto_ARVO;}
        조각->käyttö_ARVO=1;return(char*)조각+32;
    }return 0;
}
void julkaista_etä(void *OSOITE) {
    if(!OSOITE)return;Muisti_Esto *조각=(void*)((char*)OSOITE-32);
    volatile unsigned char *지움=OSOITE;for(size_t 순번=0;순번<조각->kesto_ARVO;순번++)지움[순번]=0;
    조각->käyttö_ARVO=0;
    for(조각=첫조각;조각&&조각->Seuraava_kohde;){if(!조각->käyttö_ARVO&&!조각->Seuraava_kohde->käyttö_ARVO){조각->kesto_ARVO+=32+조각->Seuraava_kohde->kesto_ARVO;조각->Seuraava_kohde=조각->Seuraava_kohde->Seuraava_kohde;}else 조각=조각->Seuraava_kohde;}
}
void *원격재할당(void *OSOITE,size_t kesto_ARVO){
    if(!OSOITE)return jakaa_etä(kesto_ARVO);if(!kesto_ARVO){julkaista_etä(OSOITE);return 0;}
    Muisti_Esto *조각=(void*)((char*)OSOITE-32);void *새주소=jakaa_etä(kesto_ARVO);
    if(새주소){memcpy(새주소,OSOITE,kesto_ARVO<조각->kesto_ARVO?kesto_ARVO:조각->kesto_ARVO);julkaista_etä(OSOITE);}return 새주소;
}
int strcmp(const char *가,const char *SEKUNNIT_operandi){while(*가&&*가==*SEKUNNIT_operandi){가++;SEKUNNIT_operandi++;}return(unsigned char)*가-(unsigned char)*SEKUNNIT_operandi;}
char *strchr(const char *Word_SMS,int merkki_ARVO){for(;;Word_SMS++){if(*Word_SMS==(char)merkki_ARVO)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t kesto_ARVO=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,kesto_ARVO))return(char*)Word_SMS;return kesto_ARVO?0:(char*)Word_SMS;}
char *strncpy(char *kohde_ARVO,const char *원본,size_t kesto_ARVO){size_t 순번=0;for(;순번<kesto_ARVO&&원본[순번];순번++)kohde_ARVO[순번]=원본[순번];for(;순번<kesto_ARVO;순번++)kohde_ARVO[순번]=0;return kohde_ARVO;}
char *strncat(char *kohde_ARVO,const char *원본,size_t kesto_ARVO){char *끝=kohde_ARVO+strlen(kohde_ARVO);while(kesto_ARVO--&&*원본)*끝++=*원본++;*끝=0;return kohde_ARVO;}
int strncasecmp(const char *가,const char *SEKUNNIT_operandi,size_t kesto_ARVO){while(kesto_ARVO--){unsigned 첫글자=*가++,SEKUNNIT_merkki=*SEKUNNIT_operandi++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEKUNNIT_merkki>='A'&&SEKUNNIT_merkki<='Z')SEKUNNIT_merkki+=32;if(첫글자!=SEKUNNIT_merkki)return(int)첫글자-(int)SEKUNNIT_merkki;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEKUNNIT_operandi){return strncasecmp(가,SEKUNNIT_operandi,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *erotin_ARVO_d8ba4873,char **Seuraava_kohde){if(!Word_SMS)Word_SMS=*Seuraava_kohde;while(*Word_SMS&&strchr(erotin_ARVO_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Seuraava_kohde=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(erotin_ARVO_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Seuraava_kohde=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int PERUS_ARVO) {
    const char *lähdetiedosto=Word_SMS;unsigned long ARVO=0;int 음수=0,ylivuoto_ARVO=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((PERUS_ARVO==0||PERUS_ARVO==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {PERUS_ARVO=16;Word_SMS+=2;}
    if(!PERUS_ARVO)PERUS_ARVO=*Word_SMS=='0'?8:10;
    if(PERUS_ARVO<2||PERUS_ARVO>36){if(끝)*끝=(char*)lähdetiedosto;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned merkki_ARVO=(unsigned char)*Word_SMS;
        unsigned numero=merkki_ARVO>='0'&&merkki_ARVO<='9'?merkki_ARVO-'0':merkki_ARVO>='a'&&merkki_ARVO<='z'?merkki_ARVO-'a'+10:merkki_ARVO>='A'&&merkki_ARVO<='Z'?merkki_ARVO-'A'+10:36;
        if(numero>=(unsigned)PERUS_ARVO)break;
        if(ARVO>(~0ul-numero)/(unsigned)PERUS_ARVO)ylivuoto_ARVO=1;
        if(!ylivuoto_ARVO)ARVO=ARVO*(unsigned)PERUS_ARVO+numero;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?lähdetiedosto:Word_SMS);
    return ylivuoto_ARVO?~0ul:음수?0ul-ARVO:ARVO;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int alustaa_Tila;
void etä_yhteenveto(const void *data, size_t kesto_ARVO, unsigned char TULOS[32]) {
    br_sha256_context konteksti_ARVO;
    br_sha256_init(&konteksti_ARVO); br_sha256_update(&konteksti_ARVO, data, kesto_ARVO); br_sha256_out(&konteksti_ARVO, TULOS);
    memset(&konteksti_ARVO, 0, sizeof(konteksti_ARVO));
}
#define 난수저장기(paikka) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(paikka)))
int 원격난수(unsigned char *kohde_ARVO,unsigned kesto_ARVO){
    if(!alustaa_Tila){volatile unsigned char *data=(void*)0x01ff0000ul;const char *merkintä_ARVO="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)merkintä_ARVO[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;alustaa_Tila=2;}
        else {alustaa_Tila=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(alustaa_Tila==2){while(kesto_ARVO){unsigned char Seuraava_kohde[32],syöte_ARVO[33];memcpy(syöte_ARVO,모의씨앗,32);syöte_ARVO[32]=0;etä_yhteenveto(syöte_ARVO,33,Seuraava_kohde);
        syöte_ARVO[32]=1;etä_yhteenveto(syöte_ARVO,33,모의씨앗);memset(syöte_ARVO,0,33);
        unsigned numero=kesto_ARVO<32?kesto_ARVO:32;memcpy(kohde_ARVO,Seuraava_kohde,numero);memset(Seuraava_kohde,0,32);kohde_ARVO+=numero;kesto_ARVO-=numero;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(kesto_ARVO){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t ARVO=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&kesto_ARVO;순번++,kesto_ARVO--){*kohde_ARVO++=ARVO&255;ARVO>>=8;}}
    return 0;
}
