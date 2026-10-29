/* kernel_ÉRTÉK 전용 할당기와 jelszó_ÉRTÉK 난수 공급. felhasználó ELF의 libc와 별개이다. */
#include "kriptográfia_támogat.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memória_blokk { size_t hossz_ÉRTÉK; struct Memória_blokk *Tovább_cikk; int használ_ÉRTÉK; } Memória_blokk;
static unsigned char Memória_Aréna[2*1024*1024] __attribute__((aligned(16)));
static Memória_blokk *첫조각;
void *kioszt_távoli(size_t hossz_ÉRTÉK) {
    if (!hossz_ÉRTÉK || hossz_ÉRTÉK>sizeof(Memória_Aréna)-64) return 0;
    hossz_ÉRTÉK=(hossz_ÉRTÉK+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memória_Aréna;첫조각->hossz_ÉRTÉK=sizeof(Memória_Aréna)-32;}
    for(Memória_blokk *조각=첫조각;조각;조각=조각->Tovább_cikk)if(!조각->használ_ÉRTÉK&&조각->hossz_ÉRTÉK>=hossz_ÉRTÉK){
        if(조각->hossz_ÉRTÉK>=hossz_ÉRTÉK+64){Memória_blokk *새조각=(void*)((char*)조각+32+hossz_ÉRTÉK);
            새조각->hossz_ÉRTÉK=조각->hossz_ÉRTÉK-hossz_ÉRTÉK-32;새조각->Tovább_cikk=조각->Tovább_cikk;새조각->használ_ÉRTÉK=0;조각->Tovább_cikk=새조각;조각->hossz_ÉRTÉK=hossz_ÉRTÉK;}
        조각->használ_ÉRTÉK=1;return(char*)조각+32;
    }return 0;
}
void kiad_távoli(void *CÍM) {
    if(!CÍM)return;Memória_blokk *조각=(void*)((char*)CÍM-32);
    volatile unsigned char *지움=CÍM;for(size_t 순번=0;순번<조각->hossz_ÉRTÉK;순번++)지움[순번]=0;
    조각->használ_ÉRTÉK=0;
    for(조각=첫조각;조각&&조각->Tovább_cikk;){if(!조각->használ_ÉRTÉK&&!조각->Tovább_cikk->használ_ÉRTÉK){조각->hossz_ÉRTÉK+=32+조각->Tovább_cikk->hossz_ÉRTÉK;조각->Tovább_cikk=조각->Tovább_cikk->Tovább_cikk;}else 조각=조각->Tovább_cikk;}
}
void *원격재할당(void *CÍM,size_t hossz_ÉRTÉK){
    if(!CÍM)return kioszt_távoli(hossz_ÉRTÉK);if(!hossz_ÉRTÉK){kiad_távoli(CÍM);return 0;}
    Memória_blokk *조각=(void*)((char*)CÍM-32);void *새주소=kioszt_távoli(hossz_ÉRTÉK);
    if(새주소){memcpy(새주소,CÍM,hossz_ÉRTÉK<조각->hossz_ÉRTÉK?hossz_ÉRTÉK:조각->hossz_ÉRTÉK);kiad_távoli(CÍM);}return 새주소;
}
int strcmp(const char *가,const char *MPERC_operandus){while(*가&&*가==*MPERC_operandus){가++;MPERC_operandus++;}return(unsigned char)*가-(unsigned char)*MPERC_operandus;}
char *strchr(const char *szó_SMS,int karakter_ÉRTÉK){for(;;szó_SMS++){if(*szó_SMS==(char)karakter_ÉRTÉK)return(char*)szó_SMS;if(!*szó_SMS)return 0;}}
char *strstr(const char *szó_SMS,const char *찾음){size_t hossz_ÉRTÉK=strlen(찾음);for(;*szó_SMS;szó_SMS++)if(!strncmp(szó_SMS,찾음,hossz_ÉRTÉK))return(char*)szó_SMS;return hossz_ÉRTÉK?0:(char*)szó_SMS;}
char *strncpy(char *cél_ÉRTÉK,const char *원본,size_t hossz_ÉRTÉK){size_t 순번=0;for(;순번<hossz_ÉRTÉK&&원본[순번];순번++)cél_ÉRTÉK[순번]=원본[순번];for(;순번<hossz_ÉRTÉK;순번++)cél_ÉRTÉK[순번]=0;return cél_ÉRTÉK;}
char *strncat(char *cél_ÉRTÉK,const char *원본,size_t hossz_ÉRTÉK){char *끝=cél_ÉRTÉK+strlen(cél_ÉRTÉK);while(hossz_ÉRTÉK--&&*원본)*끝++=*원본++;*끝=0;return cél_ÉRTÉK;}
int strncasecmp(const char *가,const char *MPERC_operandus,size_t hossz_ÉRTÉK){while(hossz_ÉRTÉK--){unsigned 첫글자=*가++,MPERC_karakter=*MPERC_operandus++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(MPERC_karakter>='A'&&MPERC_karakter<='Z')MPERC_karakter+=32;if(첫글자!=MPERC_karakter)return(int)첫글자-(int)MPERC_karakter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *MPERC_operandus){return strncasecmp(가,MPERC_operandus,(size_t)-1);}
char *strtok_r(char *szó_SMS,const char *elválasztó_karakter_ÉRTÉK,char **Tovább_cikk){if(!szó_SMS)szó_SMS=*Tovább_cikk;while(*szó_SMS&&strchr(elválasztó_karakter_ÉRTÉK,*szó_SMS))szó_SMS++;if(!*szó_SMS){*Tovább_cikk=szó_SMS;return 0;}char *처음=szó_SMS;while(*szó_SMS&&!strchr(elválasztó_karakter_ÉRTÉK,*szó_SMS))szó_SMS++;if(*szó_SMS)*szó_SMS++=0;*Tovább_cikk=szó_SMS;return 처음;}
unsigned long strtoul(const char *szó_SMS, char **끝, int ALAP_ÉRTÉK) {
    const char *FORRÁS=szó_SMS;unsigned long ÉRTÉK=0;int 음수=0,túlfolyás_ÉRTÉK=0;
    while(*szó_SMS==' '||(*szó_SMS>=9&&*szó_SMS<=13))szó_SMS++;
    if(*szó_SMS=='-'||*szó_SMS=='+')음수=*szó_SMS++=='-';
    if((ALAP_ÉRTÉK==0||ALAP_ÉRTÉK==16)&&szó_SMS[0]=='0'&&(szó_SMS[1]=='x'||szó_SMS[1]=='X')&&
       ((szó_SMS[2]>='0'&&szó_SMS[2]<='9')||(szó_SMS[2]>='a'&&szó_SMS[2]<='f')||(szó_SMS[2]>='A'&&szó_SMS[2]<='F'))) {ALAP_ÉRTÉK=16;szó_SMS+=2;}
    if(!ALAP_ÉRTÉK)ALAP_ÉRTÉK=*szó_SMS=='0'?8:10;
    if(ALAP_ÉRTÉK<2||ALAP_ÉRTÉK>36){if(끝)*끝=(char*)FORRÁS;return 0;}
    const char *처음=szó_SMS;
    for(;;szó_SMS++) {
        unsigned karakter_ÉRTÉK=(unsigned char)*szó_SMS;
        unsigned szám=karakter_ÉRTÉK>='0'&&karakter_ÉRTÉK<='9'?karakter_ÉRTÉK-'0':karakter_ÉRTÉK>='a'&&karakter_ÉRTÉK<='z'?karakter_ÉRTÉK-'a'+10:karakter_ÉRTÉK>='A'&&karakter_ÉRTÉK<='Z'?karakter_ÉRTÉK-'A'+10:36;
        if(szám>=(unsigned)ALAP_ÉRTÉK)break;
        if(ÉRTÉK>(~0ul-szám)/(unsigned)ALAP_ÉRTÉK)túlfolyás_ÉRTÉK=1;
        if(!túlfolyás_ÉRTÉK)ÉRTÉK=ÉRTÉK*(unsigned)ALAP_ÉRTÉK+szám;
    }
    if(끝)*끝=(char*)(szó_SMS==처음?FORRÁS:szó_SMS);
    return túlfolyás_ÉRTÉK?~0ul:음수?0ul-ÉRTÉK:ÉRTÉK;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int beültet_Állapot;
void távoli_összegzés(const void *adat, size_t hossz_ÉRTÉK, unsigned char KR[32]) {
    br_sha256_context környezet_ÉRTÉK;
    br_sha256_init(&környezet_ÉRTÉK); br_sha256_update(&környezet_ÉRTÉK, adat, hossz_ÉRTÉK); br_sha256_out(&környezet_ÉRTÉK, KR);
    memset(&környezet_ÉRTÉK, 0, sizeof(környezet_ÉRTÉK));
}
#define 난수저장기(Pozíció) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Pozíció)))
int távoli_véletlenszerű(unsigned char *cél_ÉRTÉK,unsigned hossz_ÉRTÉK){
    if(!beültet_Állapot){volatile unsigned char *adat=(void*)0x01ff0000ul;const char *jelölő_ÉRTÉK="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=adat[순번]^(unsigned char)jelölő_ÉRTÉK[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=adat[8+순번];for(unsigned 순번=0;순번<40;순번++)adat[순번]=0;beültet_Állapot=2;}
        else {beültet_Állapot=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(beültet_Állapot==2){while(hossz_ÉRTÉK){unsigned char Tovább_cikk[32],bevitel_ÉRTÉK[33];memcpy(bevitel_ÉRTÉK,모의씨앗,32);bevitel_ÉRTÉK[32]=0;távoli_összegzés(bevitel_ÉRTÉK,33,Tovább_cikk);
        bevitel_ÉRTÉK[32]=1;távoli_összegzés(bevitel_ÉRTÉK,33,모의씨앗);memset(bevitel_ÉRTÉK,0,33);
        unsigned szám=hossz_ÉRTÉK<32?hossz_ÉRTÉK:32;memcpy(cél_ÉRTÉK,Tovább_cikk,szám);memset(Tovább_cikk,0,32);cél_ÉRTÉK+=szám;hossz_ÉRTÉK-=szám;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(hossz_ÉRTÉK){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t ÉRTÉK=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&hossz_ÉRTÉK;순번++,hossz_ÉRTÉK--){*cél_ÉRTÉK++=ÉRTÉK&255;ÉRTÉK>>=8;}}
    return 0;
}
