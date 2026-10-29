/* jądro_WARTOŚĆ 전용 할당기와 hasło_WARTOŚĆ 난수 공급. przestrzeń_użytkownika ELF의 libc와 별개이다. */
#include "kryptografia_wsparcie.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Pamięć_blok { size_t długość_WARTOŚĆ; struct Pamięć_blok *Dalej_towar; int używać_WARTOŚĆ; } Pamięć_blok;
static unsigned char Pamięć_Arena[2*1024*1024] __attribute__((aligned(16)));
static Pamięć_blok *첫조각;
void *przydzielić_zdalny(size_t długość_WARTOŚĆ) {
    if (!długość_WARTOŚĆ || długość_WARTOŚĆ>sizeof(Pamięć_Arena)-64) return 0;
    długość_WARTOŚĆ=(długość_WARTOŚĆ+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Pamięć_Arena;첫조각->długość_WARTOŚĆ=sizeof(Pamięć_Arena)-32;}
    for(Pamięć_blok *fragment_WARTOŚĆ_652d4b53=첫조각;fragment_WARTOŚĆ_652d4b53;fragment_WARTOŚĆ_652d4b53=fragment_WARTOŚĆ_652d4b53->Dalej_towar)if(!fragment_WARTOŚĆ_652d4b53->używać_WARTOŚĆ&&fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ>=długość_WARTOŚĆ){
        if(fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ>=długość_WARTOŚĆ+64){Pamięć_blok *새조각=(void*)((char*)fragment_WARTOŚĆ_652d4b53+32+długość_WARTOŚĆ);
            새조각->długość_WARTOŚĆ=fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ-długość_WARTOŚĆ-32;새조각->Dalej_towar=fragment_WARTOŚĆ_652d4b53->Dalej_towar;새조각->używać_WARTOŚĆ=0;fragment_WARTOŚĆ_652d4b53->Dalej_towar=새조각;fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ=długość_WARTOŚĆ;}
        fragment_WARTOŚĆ_652d4b53->używać_WARTOŚĆ=1;return(char*)fragment_WARTOŚĆ_652d4b53+32;
    }return 0;
}
void wersja_zdalny(void *Adres) {
    if(!Adres)return;Pamięć_blok *fragment_WARTOŚĆ_652d4b53=(void*)((char*)Adres-32);
    volatile unsigned char *지움=Adres;for(size_t 순번=0;순번<fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ;순번++)지움[순번]=0;
    fragment_WARTOŚĆ_652d4b53->używać_WARTOŚĆ=0;
    for(fragment_WARTOŚĆ_652d4b53=첫조각;fragment_WARTOŚĆ_652d4b53&&fragment_WARTOŚĆ_652d4b53->Dalej_towar;){if(!fragment_WARTOŚĆ_652d4b53->używać_WARTOŚĆ&&!fragment_WARTOŚĆ_652d4b53->Dalej_towar->używać_WARTOŚĆ){fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ+=32+fragment_WARTOŚĆ_652d4b53->Dalej_towar->długość_WARTOŚĆ;fragment_WARTOŚĆ_652d4b53->Dalej_towar=fragment_WARTOŚĆ_652d4b53->Dalej_towar->Dalej_towar;}else fragment_WARTOŚĆ_652d4b53=fragment_WARTOŚĆ_652d4b53->Dalej_towar;}
}
void *원격재할당(void *Adres,size_t długość_WARTOŚĆ){
    if(!Adres)return przydzielić_zdalny(długość_WARTOŚĆ);if(!długość_WARTOŚĆ){wersja_zdalny(Adres);return 0;}
    Pamięć_blok *fragment_WARTOŚĆ_652d4b53=(void*)((char*)Adres-32);void *새주소=przydzielić_zdalny(długość_WARTOŚĆ);
    if(새주소){memcpy(새주소,Adres,długość_WARTOŚĆ<fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ?długość_WARTOŚĆ:fragment_WARTOŚĆ_652d4b53->długość_WARTOŚĆ);wersja_zdalny(Adres);}return 새주소;
}
int strcmp(const char *가,const char *SEKUNDA_operand){while(*가&&*가==*SEKUNDA_operand){가++;SEKUNDA_operand++;}return(unsigned char)*가-(unsigned char)*SEKUNDA_operand;}
char *strchr(const char *Word_SMS,int znak_WARTOŚĆ){for(;;Word_SMS++){if(*Word_SMS==(char)znak_WARTOŚĆ)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t długość_WARTOŚĆ=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,długość_WARTOŚĆ))return(char*)Word_SMS;return długość_WARTOŚĆ?0:(char*)Word_SMS;}
char *strncpy(char *cel_WARTOŚĆ,const char *원본,size_t długość_WARTOŚĆ){size_t 순번=0;for(;순번<długość_WARTOŚĆ&&원본[순번];순번++)cel_WARTOŚĆ[순번]=원본[순번];for(;순번<długość_WARTOŚĆ;순번++)cel_WARTOŚĆ[순번]=0;return cel_WARTOŚĆ;}
char *strncat(char *cel_WARTOŚĆ,const char *원본,size_t długość_WARTOŚĆ){char *끝=cel_WARTOŚĆ+strlen(cel_WARTOŚĆ);while(długość_WARTOŚĆ--&&*원본)*끝++=*원본++;*끝=0;return cel_WARTOŚĆ;}
int strncasecmp(const char *가,const char *SEKUNDA_operand,size_t długość_WARTOŚĆ){while(długość_WARTOŚĆ--){unsigned 첫글자=*가++,SEKUNDA_znak=*SEKUNDA_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEKUNDA_znak>='A'&&SEKUNDA_znak<='Z')SEKUNDA_znak+=32;if(첫글자!=SEKUNDA_znak)return(int)첫글자-(int)SEKUNDA_znak;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEKUNDA_operand){return strncasecmp(가,SEKUNDA_operand,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *ogranicznik_WARTOŚĆ,char **Dalej_towar){if(!Word_SMS)Word_SMS=*Dalej_towar;while(*Word_SMS&&strchr(ogranicznik_WARTOŚĆ,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Dalej_towar=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(ogranicznik_WARTOŚĆ,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Dalej_towar=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int baza_WARTOŚĆ) {
    const char *plik_źródłowy=Word_SMS;unsigned long WARTOŚĆ=0;int negatywny_WARTOŚĆ=0,przepełnienie_WARTOŚĆ=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')negatywny_WARTOŚĆ=*Word_SMS++=='-';
    if((baza_WARTOŚĆ==0||baza_WARTOŚĆ==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {baza_WARTOŚĆ=16;Word_SMS+=2;}
    if(!baza_WARTOŚĆ)baza_WARTOŚĆ=*Word_SMS=='0'?8:10;
    if(baza_WARTOŚĆ<2||baza_WARTOŚĆ>36){if(끝)*끝=(char*)plik_źródłowy;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned znak_WARTOŚĆ=(unsigned char)*Word_SMS;
        unsigned identyfikator=znak_WARTOŚĆ>='0'&&znak_WARTOŚĆ<='9'?znak_WARTOŚĆ-'0':znak_WARTOŚĆ>='a'&&znak_WARTOŚĆ<='z'?znak_WARTOŚĆ-'a'+10:znak_WARTOŚĆ>='A'&&znak_WARTOŚĆ<='Z'?znak_WARTOŚĆ-'A'+10:36;
        if(identyfikator>=(unsigned)baza_WARTOŚĆ)break;
        if(WARTOŚĆ>(~0ul-identyfikator)/(unsigned)baza_WARTOŚĆ)przepełnienie_WARTOŚĆ=1;
        if(!przepełnienie_WARTOŚĆ)WARTOŚĆ=WARTOŚĆ*(unsigned)baza_WARTOŚĆ+identyfikator;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?plik_źródłowy:Word_SMS);
    return przepełnienie_WARTOŚĆ?~0ul:negatywny_WARTOŚĆ?0ul-WARTOŚĆ:WARTOŚĆ;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int umieścić_Stan;
void zdalny_podsumowanie(const void *dane, size_t długość_WARTOŚĆ, unsigned char WYNIK[32]) {
    br_sha256_context kontekst_WARTOŚĆ;
    br_sha256_init(&kontekst_WARTOŚĆ); br_sha256_update(&kontekst_WARTOŚĆ, dane, długość_WARTOŚĆ); br_sha256_out(&kontekst_WARTOŚĆ, WYNIK);
    memset(&kontekst_WARTOŚĆ, 0, sizeof(kontekst_WARTOŚĆ));
}
#define 난수저장기(pozycja) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(pozycja)))
int zdalny_losowy(unsigned char *cel_WARTOŚĆ,unsigned długość_WARTOŚĆ){
    if(!umieścić_Stan){volatile unsigned char *dane=(void*)0x01ff0000ul;const char *pisak_WARTOŚĆ="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=dane[순번]^(unsigned char)pisak_WARTOŚĆ[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=dane[8+순번];for(unsigned 순번=0;순번<40;순번++)dane[순번]=0;umieścić_Stan=2;}
        else {umieścić_Stan=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(umieścić_Stan==2){while(długość_WARTOŚĆ){unsigned char Dalej_towar[32],wejście_WARTOŚĆ[33];memcpy(wejście_WARTOŚĆ,모의씨앗,32);wejście_WARTOŚĆ[32]=0;zdalny_podsumowanie(wejście_WARTOŚĆ,33,Dalej_towar);
        wejście_WARTOŚĆ[32]=1;zdalny_podsumowanie(wejście_WARTOŚĆ,33,모의씨앗);memset(wejście_WARTOŚĆ,0,33);
        unsigned identyfikator=długość_WARTOŚĆ<32?długość_WARTOŚĆ:32;memcpy(cel_WARTOŚĆ,Dalej_towar,identyfikator);memset(Dalej_towar,0,32);cel_WARTOŚĆ+=identyfikator;długość_WARTOŚĆ-=identyfikator;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(długość_WARTOŚĆ){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t WARTOŚĆ=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&długość_WARTOŚĆ;순번++,długość_WARTOŚĆ--){*cel_WARTOŚĆ++=WARTOŚĆ&255;WARTOŚĆ>>=8;}}
    return 0;
}
