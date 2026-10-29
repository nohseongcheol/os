/* kerne_VÆRDI 전용 할당기와 adgangskode_VÆRDI 난수 공급. bruger ELF의 libc와 별개이다. */
#include "kryptografi_støtte.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Hukommelse_blok { size_t varighed_VÆRDI; struct Hukommelse_blok *Næste_vare; int brug_VÆRDI; } Hukommelse_blok;
static unsigned char Hukommelse_Arena[2*1024*1024] __attribute__((aligned(16)));
static Hukommelse_blok *첫조각;
void *tildel_fjern(size_t varighed_VÆRDI) {
    if (!varighed_VÆRDI || varighed_VÆRDI>sizeof(Hukommelse_Arena)-64) return 0;
    varighed_VÆRDI=(varighed_VÆRDI+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Hukommelse_Arena;첫조각->varighed_VÆRDI=sizeof(Hukommelse_Arena)-32;}
    for(Hukommelse_blok *조각=첫조각;조각;조각=조각->Næste_vare)if(!조각->brug_VÆRDI&&조각->varighed_VÆRDI>=varighed_VÆRDI){
        if(조각->varighed_VÆRDI>=varighed_VÆRDI+64){Hukommelse_blok *새조각=(void*)((char*)조각+32+varighed_VÆRDI);
            새조각->varighed_VÆRDI=조각->varighed_VÆRDI-varighed_VÆRDI-32;새조각->Næste_vare=조각->Næste_vare;새조각->brug_VÆRDI=0;조각->Næste_vare=새조각;조각->varighed_VÆRDI=varighed_VÆRDI;}
        조각->brug_VÆRDI=1;return(char*)조각+32;
    }return 0;
}
void udgive_fjern(void *mail) {
    if(!mail)return;Hukommelse_blok *조각=(void*)((char*)mail-32);
    volatile unsigned char *지움=mail;for(size_t 순번=0;순번<조각->varighed_VÆRDI;순번++)지움[순번]=0;
    조각->brug_VÆRDI=0;
    for(조각=첫조각;조각&&조각->Næste_vare;){if(!조각->brug_VÆRDI&&!조각->Næste_vare->brug_VÆRDI){조각->varighed_VÆRDI+=32+조각->Næste_vare->varighed_VÆRDI;조각->Næste_vare=조각->Næste_vare->Næste_vare;}else 조각=조각->Næste_vare;}
}
void *원격재할당(void *mail,size_t varighed_VÆRDI){
    if(!mail)return tildel_fjern(varighed_VÆRDI);if(!varighed_VÆRDI){udgive_fjern(mail);return 0;}
    Hukommelse_blok *조각=(void*)((char*)mail-32);void *새주소=tildel_fjern(varighed_VÆRDI);
    if(새주소){memcpy(새주소,mail,varighed_VÆRDI<조각->varighed_VÆRDI?varighed_VÆRDI:조각->varighed_VÆRDI);udgive_fjern(mail);}return 새주소;
}
int strcmp(const char *가,const char *SEKUND_operand){while(*가&&*가==*SEKUND_operand){가++;SEKUND_operand++;}return(unsigned char)*가-(unsigned char)*SEKUND_operand;}
char *strchr(const char *Ord_sms,int tegn_VÆRDI){for(;;Ord_sms++){if(*Ord_sms==(char)tegn_VÆRDI)return(char*)Ord_sms;if(!*Ord_sms)return 0;}}
char *strstr(const char *Ord_sms,const char *찾음){size_t varighed_VÆRDI=strlen(찾음);for(;*Ord_sms;Ord_sms++)if(!strncmp(Ord_sms,찾음,varighed_VÆRDI))return(char*)Ord_sms;return varighed_VÆRDI?0:(char*)Ord_sms;}
char *strncpy(char *destination_VÆRDI,const char *원본,size_t varighed_VÆRDI){size_t 순번=0;for(;순번<varighed_VÆRDI&&원본[순번];순번++)destination_VÆRDI[순번]=원본[순번];for(;순번<varighed_VÆRDI;순번++)destination_VÆRDI[순번]=0;return destination_VÆRDI;}
char *strncat(char *destination_VÆRDI,const char *원본,size_t varighed_VÆRDI){char *끝=destination_VÆRDI+strlen(destination_VÆRDI);while(varighed_VÆRDI--&&*원본)*끝++=*원본++;*끝=0;return destination_VÆRDI;}
int strncasecmp(const char *가,const char *SEKUND_operand,size_t varighed_VÆRDI){while(varighed_VÆRDI--){unsigned 첫글자=*가++,SEKUND_tegn=*SEKUND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEKUND_tegn>='A'&&SEKUND_tegn<='Z')SEKUND_tegn+=32;if(첫글자!=SEKUND_tegn)return(int)첫글자-(int)SEKUND_tegn;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEKUND_operand){return strncasecmp(가,SEKUND_operand,(size_t)-1);}
char *strtok_r(char *Ord_sms,const char *afgrænser_VÆRDI,char **Næste_vare){if(!Ord_sms)Ord_sms=*Næste_vare;while(*Ord_sms&&strchr(afgrænser_VÆRDI,*Ord_sms))Ord_sms++;if(!*Ord_sms){*Næste_vare=Ord_sms;return 0;}char *처음=Ord_sms;while(*Ord_sms&&!strchr(afgrænser_VÆRDI,*Ord_sms))Ord_sms++;if(*Ord_sms)*Ord_sms++=0;*Næste_vare=Ord_sms;return 처음;}
unsigned long strtoul(const char *Ord_sms, char **끝, int BASIS_VÆRDI) {
    const char *KILDE=Ord_sms;unsigned long VÆRDI=0;int 음수=0,overløb_VÆRDI=0;
    while(*Ord_sms==' '||(*Ord_sms>=9&&*Ord_sms<=13))Ord_sms++;
    if(*Ord_sms=='-'||*Ord_sms=='+')음수=*Ord_sms++=='-';
    if((BASIS_VÆRDI==0||BASIS_VÆRDI==16)&&Ord_sms[0]=='0'&&(Ord_sms[1]=='x'||Ord_sms[1]=='X')&&
       ((Ord_sms[2]>='0'&&Ord_sms[2]<='9')||(Ord_sms[2]>='a'&&Ord_sms[2]<='f')||(Ord_sms[2]>='A'&&Ord_sms[2]<='F'))) {BASIS_VÆRDI=16;Ord_sms+=2;}
    if(!BASIS_VÆRDI)BASIS_VÆRDI=*Ord_sms=='0'?8:10;
    if(BASIS_VÆRDI<2||BASIS_VÆRDI>36){if(끝)*끝=(char*)KILDE;return 0;}
    const char *처음=Ord_sms;
    for(;;Ord_sms++) {
        unsigned tegn_VÆRDI=(unsigned char)*Ord_sms;
        unsigned tal=tegn_VÆRDI>='0'&&tegn_VÆRDI<='9'?tegn_VÆRDI-'0':tegn_VÆRDI>='a'&&tegn_VÆRDI<='z'?tegn_VÆRDI-'a'+10:tegn_VÆRDI>='A'&&tegn_VÆRDI<='Z'?tegn_VÆRDI-'A'+10:36;
        if(tal>=(unsigned)BASIS_VÆRDI)break;
        if(VÆRDI>(~0ul-tal)/(unsigned)BASIS_VÆRDI)overløb_VÆRDI=1;
        if(!overløb_VÆRDI)VÆRDI=VÆRDI*(unsigned)BASIS_VÆRDI+tal;
    }
    if(끝)*끝=(char*)(Ord_sms==처음?KILDE:Ord_sms);
    return overløb_VÆRDI?~0ul:음수?0ul-VÆRDI:VÆRDI;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int så_status;
void fjern_resume(const void *data, size_t varighed_VÆRDI, unsigned char KR[32]) {
    br_sha256_context kontekst_VÆRDI;
    br_sha256_init(&kontekst_VÆRDI); br_sha256_update(&kontekst_VÆRDI, data, varighed_VÆRDI); br_sha256_out(&kontekst_VÆRDI, KR);
    memset(&kontekst_VÆRDI, 0, sizeof(kontekst_VÆRDI));
}
#define 난수저장기(Placering) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Placering)))
int fjern_vilkårlig(unsigned char *destination_VÆRDI,unsigned varighed_VÆRDI){
    if(!så_status){volatile unsigned char *data=(void*)0x01ff0000ul;const char *mærke_VÆRDI="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)mærke_VÆRDI[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;så_status=2;}
        else {så_status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(så_status==2){while(varighed_VÆRDI){unsigned char Næste_vare[32],input_VÆRDI[33];memcpy(input_VÆRDI,모의씨앗,32);input_VÆRDI[32]=0;fjern_resume(input_VÆRDI,33,Næste_vare);
        input_VÆRDI[32]=1;fjern_resume(input_VÆRDI,33,모의씨앗);memset(input_VÆRDI,0,33);
        unsigned tal=varighed_VÆRDI<32?varighed_VÆRDI:32;memcpy(destination_VÆRDI,Næste_vare,tal);memset(Næste_vare,0,32);destination_VÆRDI+=tal;varighed_VÆRDI-=tal;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(varighed_VÆRDI){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VÆRDI=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&varighed_VÆRDI;순번++,varighed_VÆRDI--){*destination_VÆRDI++=VÆRDI&255;VÆRDI>>=8;}}
    return 0;
}
