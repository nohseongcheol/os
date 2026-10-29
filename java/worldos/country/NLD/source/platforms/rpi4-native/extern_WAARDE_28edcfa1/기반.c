/* kernel_WAARDE 전용 할당기와 wachtwoord_WAARDE 난수 공급. gebruikersruimte ELF의 libc와 별개이다. */
#include "cryptografie_steun.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Geheugen_blok { size_t tijdsduur_WAARDE; struct Geheugen_blok *Volgende_item; int gebruik_WAARDE; } Geheugen_blok;
static unsigned char Geheugen_Arena[2*1024*1024] __attribute__((aligned(16)));
static Geheugen_blok *첫조각;
void *toewijzen_extern(size_t tijdsduur_WAARDE) {
    if (!tijdsduur_WAARDE || tijdsduur_WAARDE>sizeof(Geheugen_Arena)-64) return 0;
    tijdsduur_WAARDE=(tijdsduur_WAARDE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Geheugen_Arena;첫조각->tijdsduur_WAARDE=sizeof(Geheugen_Arena)-32;}
    for(Geheugen_blok *조각=첫조각;조각;조각=조각->Volgende_item)if(!조각->gebruik_WAARDE&&조각->tijdsduur_WAARDE>=tijdsduur_WAARDE){
        if(조각->tijdsduur_WAARDE>=tijdsduur_WAARDE+64){Geheugen_blok *새조각=(void*)((char*)조각+32+tijdsduur_WAARDE);
            새조각->tijdsduur_WAARDE=조각->tijdsduur_WAARDE-tijdsduur_WAARDE-32;새조각->Volgende_item=조각->Volgende_item;새조각->gebruik_WAARDE=0;조각->Volgende_item=새조각;조각->tijdsduur_WAARDE=tijdsduur_WAARDE;}
        조각->gebruik_WAARDE=1;return(char*)조각+32;
    }return 0;
}
void versie_extern(void *ADRES) {
    if(!ADRES)return;Geheugen_blok *조각=(void*)((char*)ADRES-32);
    volatile unsigned char *지움=ADRES;for(size_t 순번=0;순번<조각->tijdsduur_WAARDE;순번++)지움[순번]=0;
    조각->gebruik_WAARDE=0;
    for(조각=첫조각;조각&&조각->Volgende_item;){if(!조각->gebruik_WAARDE&&!조각->Volgende_item->gebruik_WAARDE){조각->tijdsduur_WAARDE+=32+조각->Volgende_item->tijdsduur_WAARDE;조각->Volgende_item=조각->Volgende_item->Volgende_item;}else 조각=조각->Volgende_item;}
}
void *원격재할당(void *ADRES,size_t tijdsduur_WAARDE){
    if(!ADRES)return toewijzen_extern(tijdsduur_WAARDE);if(!tijdsduur_WAARDE){versie_extern(ADRES);return 0;}
    Geheugen_blok *조각=(void*)((char*)ADRES-32);void *새주소=toewijzen_extern(tijdsduur_WAARDE);
    if(새주소){memcpy(새주소,ADRES,tijdsduur_WAARDE<조각->tijdsduur_WAARDE?tijdsduur_WAARDE:조각->tijdsduur_WAARDE);versie_extern(ADRES);}return 새주소;
}
int strcmp(const char *가,const char *SECONDE_operand){while(*가&&*가==*SECONDE_operand){가++;SECONDE_operand++;}return(unsigned char)*가-(unsigned char)*SECONDE_operand;}
char *strchr(const char *Word_sms,int teken_WAARDE){for(;;Word_sms++){if(*Word_sms==(char)teken_WAARDE)return(char*)Word_sms;if(!*Word_sms)return 0;}}
char *strstr(const char *Word_sms,const char *찾음){size_t tijdsduur_WAARDE=strlen(찾음);for(;*Word_sms;Word_sms++)if(!strncmp(Word_sms,찾음,tijdsduur_WAARDE))return(char*)Word_sms;return tijdsduur_WAARDE?0:(char*)Word_sms;}
char *strncpy(char *doel_WAARDE,const char *원본,size_t tijdsduur_WAARDE){size_t 순번=0;for(;순번<tijdsduur_WAARDE&&원본[순번];순번++)doel_WAARDE[순번]=원본[순번];for(;순번<tijdsduur_WAARDE;순번++)doel_WAARDE[순번]=0;return doel_WAARDE;}
char *strncat(char *doel_WAARDE,const char *원본,size_t tijdsduur_WAARDE){char *끝=doel_WAARDE+strlen(doel_WAARDE);while(tijdsduur_WAARDE--&&*원본)*끝++=*원본++;*끝=0;return doel_WAARDE;}
int strncasecmp(const char *가,const char *SECONDE_operand,size_t tijdsduur_WAARDE){while(tijdsduur_WAARDE--){unsigned 첫글자=*가++,SECONDE_teken=*SECONDE_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECONDE_teken>='A'&&SECONDE_teken<='Z')SECONDE_teken+=32;if(첫글자!=SECONDE_teken)return(int)첫글자-(int)SECONDE_teken;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECONDE_operand){return strncasecmp(가,SECONDE_operand,(size_t)-1);}
char *strtok_r(char *Word_sms,const char *scheidingsteken_WAARDE,char **Volgende_item){if(!Word_sms)Word_sms=*Volgende_item;while(*Word_sms&&strchr(scheidingsteken_WAARDE,*Word_sms))Word_sms++;if(!*Word_sms){*Volgende_item=Word_sms;return 0;}char *처음=Word_sms;while(*Word_sms&&!strchr(scheidingsteken_WAARDE,*Word_sms))Word_sms++;if(*Word_sms)*Word_sms++=0;*Volgende_item=Word_sms;return 처음;}
unsigned long strtoul(const char *Word_sms, char **끝, int BASIS_WAARDE) {
    const char *broncode=Word_sms;unsigned long WAARDE=0;int 음수=0,overloop_WAARDE=0;
    while(*Word_sms==' '||(*Word_sms>=9&&*Word_sms<=13))Word_sms++;
    if(*Word_sms=='-'||*Word_sms=='+')음수=*Word_sms++=='-';
    if((BASIS_WAARDE==0||BASIS_WAARDE==16)&&Word_sms[0]=='0'&&(Word_sms[1]=='x'||Word_sms[1]=='X')&&
       ((Word_sms[2]>='0'&&Word_sms[2]<='9')||(Word_sms[2]>='a'&&Word_sms[2]<='f')||(Word_sms[2]>='A'&&Word_sms[2]<='F'))) {BASIS_WAARDE=16;Word_sms+=2;}
    if(!BASIS_WAARDE)BASIS_WAARDE=*Word_sms=='0'?8:10;
    if(BASIS_WAARDE<2||BASIS_WAARDE>36){if(끝)*끝=(char*)broncode;return 0;}
    const char *처음=Word_sms;
    for(;;Word_sms++) {
        unsigned teken_WAARDE=(unsigned char)*Word_sms;
        unsigned nummer=teken_WAARDE>='0'&&teken_WAARDE<='9'?teken_WAARDE-'0':teken_WAARDE>='a'&&teken_WAARDE<='z'?teken_WAARDE-'a'+10:teken_WAARDE>='A'&&teken_WAARDE<='Z'?teken_WAARDE-'A'+10:36;
        if(nummer>=(unsigned)BASIS_WAARDE)break;
        if(WAARDE>(~0ul-nummer)/(unsigned)BASIS_WAARDE)overloop_WAARDE=1;
        if(!overloop_WAARDE)WAARDE=WAARDE*(unsigned)BASIS_WAARDE+nummer;
    }
    if(끝)*끝=(char*)(Word_sms==처음?broncode:Word_sms);
    return overloop_WAARDE?~0ul:음수?0ul-WAARDE:WAARDE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int seed_Status;
void extern_samenvatting(const void *gegevens, size_t tijdsduur_WAARDE, unsigned char resultaat[32]) {
    br_sha256_context context_WAARDE;
    br_sha256_init(&context_WAARDE); br_sha256_update(&context_WAARDE, gegevens, tijdsduur_WAARDE); br_sha256_out(&context_WAARDE, resultaat);
    memset(&context_WAARDE, 0, sizeof(context_WAARDE));
}
#define 난수저장기(positie) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(positie)))
int extern_willekeurig(unsigned char *doel_WAARDE,unsigned tijdsduur_WAARDE){
    if(!seed_Status){volatile unsigned char *gegevens=(void*)0x01ff0000ul;const char *markering_WAARDE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=gegevens[순번]^(unsigned char)markering_WAARDE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=gegevens[8+순번];for(unsigned 순번=0;순번<40;순번++)gegevens[순번]=0;seed_Status=2;}
        else {seed_Status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(seed_Status==2){while(tijdsduur_WAARDE){unsigned char Volgende_item[32],invoer_WAARDE[33];memcpy(invoer_WAARDE,모의씨앗,32);invoer_WAARDE[32]=0;extern_samenvatting(invoer_WAARDE,33,Volgende_item);
        invoer_WAARDE[32]=1;extern_samenvatting(invoer_WAARDE,33,모의씨앗);memset(invoer_WAARDE,0,33);
        unsigned nummer=tijdsduur_WAARDE<32?tijdsduur_WAARDE:32;memcpy(doel_WAARDE,Volgende_item,nummer);memset(Volgende_item,0,32);doel_WAARDE+=nummer;tijdsduur_WAARDE-=nummer;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(tijdsduur_WAARDE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t WAARDE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&tijdsduur_WAARDE;순번++,tijdsduur_WAARDE--){*doel_WAARDE++=WAARDE&255;WAARDE>>=8;}}
    return 0;
}
