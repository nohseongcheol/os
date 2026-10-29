/* kärna_värde 전용 할당기와 lösenord_värde 난수 공급. användarutrymme ELF의 libc와 별개이다. */
#include "kryptografi_stöd.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Minne_block { size_t längd_värde; struct Minne_block *Nästa_objekt; int använda_värde; } Minne_block;
static unsigned char Minne_Arena[2*1024*1024] __attribute__((aligned(16)));
static Minne_block *첫조각;
void *allokera_fjärr(size_t längd_värde) {
    if (!längd_värde || längd_värde>sizeof(Minne_Arena)-64) return 0;
    längd_värde=(längd_värde+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Minne_Arena;첫조각->längd_värde=sizeof(Minne_Arena)-32;}
    for(Minne_block *조각=첫조각;조각;조각=조각->Nästa_objekt)if(!조각->använda_värde&&조각->längd_värde>=längd_värde){
        if(조각->längd_värde>=längd_värde+64){Minne_block *새조각=(void*)((char*)조각+32+längd_värde);
            새조각->längd_värde=조각->längd_värde-längd_värde-32;새조각->Nästa_objekt=조각->Nästa_objekt;새조각->använda_värde=0;조각->Nästa_objekt=새조각;조각->längd_värde=längd_värde;}
        조각->använda_värde=1;return(char*)조각+32;
    }return 0;
}
void släppa_fjärr(void *Adress) {
    if(!Adress)return;Minne_block *조각=(void*)((char*)Adress-32);
    volatile unsigned char *지움=Adress;for(size_t 순번=0;순번<조각->längd_värde;순번++)지움[순번]=0;
    조각->använda_värde=0;
    for(조각=첫조각;조각&&조각->Nästa_objekt;){if(!조각->använda_värde&&!조각->Nästa_objekt->använda_värde){조각->längd_värde+=32+조각->Nästa_objekt->längd_värde;조각->Nästa_objekt=조각->Nästa_objekt->Nästa_objekt;}else 조각=조각->Nästa_objekt;}
}
void *원격재할당(void *Adress,size_t längd_värde){
    if(!Adress)return allokera_fjärr(längd_värde);if(!längd_värde){släppa_fjärr(Adress);return 0;}
    Minne_block *조각=(void*)((char*)Adress-32);void *새주소=allokera_fjärr(längd_värde);
    if(새주소){memcpy(새주소,Adress,längd_värde<조각->längd_värde?längd_värde:조각->längd_värde);släppa_fjärr(Adress);}return 새주소;
}
int strcmp(const char *가,const char *SEKUND_operand){while(*가&&*가==*SEKUND_operand){가++;SEKUND_operand++;}return(unsigned char)*가-(unsigned char)*SEKUND_operand;}
char *strchr(const char *Ord_SMS,int tecken_värde){for(;;Ord_SMS++){if(*Ord_SMS==(char)tecken_värde)return(char*)Ord_SMS;if(!*Ord_SMS)return 0;}}
char *strstr(const char *Ord_SMS,const char *찾음){size_t längd_värde=strlen(찾음);for(;*Ord_SMS;Ord_SMS++)if(!strncmp(Ord_SMS,찾음,längd_värde))return(char*)Ord_SMS;return längd_värde?0:(char*)Ord_SMS;}
char *strncpy(char *mål_värde,const char *원본,size_t längd_värde){size_t 순번=0;for(;순번<längd_värde&&원본[순번];순번++)mål_värde[순번]=원본[순번];for(;순번<längd_värde;순번++)mål_värde[순번]=0;return mål_värde;}
char *strncat(char *mål_värde,const char *원본,size_t längd_värde){char *끝=mål_värde+strlen(mål_värde);while(längd_värde--&&*원본)*끝++=*원본++;*끝=0;return mål_värde;}
int strncasecmp(const char *가,const char *SEKUND_operand,size_t längd_värde){while(längd_värde--){unsigned 첫글자=*가++,SEKUND_tecken=*SEKUND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEKUND_tecken>='A'&&SEKUND_tecken<='Z')SEKUND_tecken+=32;if(첫글자!=SEKUND_tecken)return(int)첫글자-(int)SEKUND_tecken;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEKUND_operand){return strncasecmp(가,SEKUND_operand,(size_t)-1);}
char *strtok_r(char *Ord_SMS,const char *avgränsare_värde_d8ba4873,char **Nästa_objekt){if(!Ord_SMS)Ord_SMS=*Nästa_objekt;while(*Ord_SMS&&strchr(avgränsare_värde_d8ba4873,*Ord_SMS))Ord_SMS++;if(!*Ord_SMS){*Nästa_objekt=Ord_SMS;return 0;}char *처음=Ord_SMS;while(*Ord_SMS&&!strchr(avgränsare_värde_d8ba4873,*Ord_SMS))Ord_SMS++;if(*Ord_SMS)*Ord_SMS++=0;*Nästa_objekt=Ord_SMS;return 처음;}
unsigned long strtoul(const char *Ord_SMS, char **끝, int BAS_värde) {
    const char *källfil=Ord_SMS;unsigned long värde=0;int 음수=0,spill_värde=0;
    while(*Ord_SMS==' '||(*Ord_SMS>=9&&*Ord_SMS<=13))Ord_SMS++;
    if(*Ord_SMS=='-'||*Ord_SMS=='+')음수=*Ord_SMS++=='-';
    if((BAS_värde==0||BAS_värde==16)&&Ord_SMS[0]=='0'&&(Ord_SMS[1]=='x'||Ord_SMS[1]=='X')&&
       ((Ord_SMS[2]>='0'&&Ord_SMS[2]<='9')||(Ord_SMS[2]>='a'&&Ord_SMS[2]<='f')||(Ord_SMS[2]>='A'&&Ord_SMS[2]<='F'))) {BAS_värde=16;Ord_SMS+=2;}
    if(!BAS_värde)BAS_värde=*Ord_SMS=='0'?8:10;
    if(BAS_värde<2||BAS_värde>36){if(끝)*끝=(char*)källfil;return 0;}
    const char *처음=Ord_SMS;
    for(;;Ord_SMS++) {
        unsigned tecken_värde=(unsigned char)*Ord_SMS;
        unsigned nummer=tecken_värde>='0'&&tecken_värde<='9'?tecken_värde-'0':tecken_värde>='a'&&tecken_värde<='z'?tecken_värde-'a'+10:tecken_värde>='A'&&tecken_värde<='Z'?tecken_värde-'A'+10:36;
        if(nummer>=(unsigned)BAS_värde)break;
        if(värde>(~0ul-nummer)/(unsigned)BAS_värde)spill_värde=1;
        if(!spill_värde)värde=värde*(unsigned)BAS_värde+nummer;
    }
    if(끝)*끝=(char*)(Ord_SMS==처음?källfil:Ord_SMS);
    return spill_värde?~0ul:음수?0ul-värde:värde;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int så_status;
void fjärr_sammanfattning(const void *data, size_t längd_värde, unsigned char RESULTAT[32]) {
    br_sha256_context sammanhang_värde;
    br_sha256_init(&sammanhang_värde); br_sha256_update(&sammanhang_värde, data, längd_värde); br_sha256_out(&sammanhang_värde, RESULTAT);
    memset(&sammanhang_värde, 0, sizeof(sammanhang_värde));
}
#define 난수저장기(position) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(position)))
int fjärr_slumpmässig(unsigned char *mål_värde,unsigned längd_värde){
    if(!så_status){volatile unsigned char *data=(void*)0x01ff0000ul;const char *markör_värde="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)markör_värde[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;så_status=2;}
        else {så_status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(så_status==2){while(längd_värde){unsigned char Nästa_objekt[32],indata_värde[33];memcpy(indata_värde,모의씨앗,32);indata_värde[32]=0;fjärr_sammanfattning(indata_värde,33,Nästa_objekt);
        indata_värde[32]=1;fjärr_sammanfattning(indata_värde,33,모의씨앗);memset(indata_värde,0,33);
        unsigned nummer=längd_värde<32?längd_värde:32;memcpy(mål_värde,Nästa_objekt,nummer);memset(Nästa_objekt,0,32);mål_värde+=nummer;längd_värde-=nummer;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(längd_värde){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t värde=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&längd_värde;순번++,längd_värde--){*mål_värde++=värde&255;värde>>=8;}}
    return 0;
}
