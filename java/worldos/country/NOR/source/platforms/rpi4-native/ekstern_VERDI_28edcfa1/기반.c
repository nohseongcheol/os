/* kjerne_VERDI 전용 할당기와 passord_VERDI 난수 공급. bruker ELF의 libc와 별개이다. */
#include "kryptografi_støtte.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Minne_blokk { size_t lengde_VERDI; struct Minne_blokk *Neste_vare; int bruk_VERDI; } Minne_blokk;
static unsigned char Minne_Arena[2*1024*1024] __attribute__((aligned(16)));
static Minne_blokk *첫조각;
void *tildele_ekstern(size_t lengde_VERDI) {
    if (!lengde_VERDI || lengde_VERDI>sizeof(Minne_Arena)-64) return 0;
    lengde_VERDI=(lengde_VERDI+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Minne_Arena;첫조각->lengde_VERDI=sizeof(Minne_Arena)-32;}
    for(Minne_blokk *조각=첫조각;조각;조각=조각->Neste_vare)if(!조각->bruk_VERDI&&조각->lengde_VERDI>=lengde_VERDI){
        if(조각->lengde_VERDI>=lengde_VERDI+64){Minne_blokk *새조각=(void*)((char*)조각+32+lengde_VERDI);
            새조각->lengde_VERDI=조각->lengde_VERDI-lengde_VERDI-32;새조각->Neste_vare=조각->Neste_vare;새조각->bruk_VERDI=0;조각->Neste_vare=새조각;조각->lengde_VERDI=lengde_VERDI;}
        조각->bruk_VERDI=1;return(char*)조각+32;
    }return 0;
}
void frigi_ekstern(void *e_post) {
    if(!e_post)return;Minne_blokk *조각=(void*)((char*)e_post-32);
    volatile unsigned char *지움=e_post;for(size_t 순번=0;순번<조각->lengde_VERDI;순번++)지움[순번]=0;
    조각->bruk_VERDI=0;
    for(조각=첫조각;조각&&조각->Neste_vare;){if(!조각->bruk_VERDI&&!조각->Neste_vare->bruk_VERDI){조각->lengde_VERDI+=32+조각->Neste_vare->lengde_VERDI;조각->Neste_vare=조각->Neste_vare->Neste_vare;}else 조각=조각->Neste_vare;}
}
void *원격재할당(void *e_post,size_t lengde_VERDI){
    if(!e_post)return tildele_ekstern(lengde_VERDI);if(!lengde_VERDI){frigi_ekstern(e_post);return 0;}
    Minne_blokk *조각=(void*)((char*)e_post-32);void *새주소=tildele_ekstern(lengde_VERDI);
    if(새주소){memcpy(새주소,e_post,lengde_VERDI<조각->lengde_VERDI?lengde_VERDI:조각->lengde_VERDI);frigi_ekstern(e_post);}return 새주소;
}
int strcmp(const char *가,const char *SEKUND_operand){while(*가&&*가==*SEKUND_operand){가++;SEKUND_operand++;}return(unsigned char)*가-(unsigned char)*SEKUND_operand;}
char *strchr(const char *ord_SMS,int tegn_VERDI){for(;;ord_SMS++){if(*ord_SMS==(char)tegn_VERDI)return(char*)ord_SMS;if(!*ord_SMS)return 0;}}
char *strstr(const char *ord_SMS,const char *찾음){size_t lengde_VERDI=strlen(찾음);for(;*ord_SMS;ord_SMS++)if(!strncmp(ord_SMS,찾음,lengde_VERDI))return(char*)ord_SMS;return lengde_VERDI?0:(char*)ord_SMS;}
char *strncpy(char *mål_VERDI,const char *원본,size_t lengde_VERDI){size_t 순번=0;for(;순번<lengde_VERDI&&원본[순번];순번++)mål_VERDI[순번]=원본[순번];for(;순번<lengde_VERDI;순번++)mål_VERDI[순번]=0;return mål_VERDI;}
char *strncat(char *mål_VERDI,const char *원본,size_t lengde_VERDI){char *끝=mål_VERDI+strlen(mål_VERDI);while(lengde_VERDI--&&*원본)*끝++=*원본++;*끝=0;return mål_VERDI;}
int strncasecmp(const char *가,const char *SEKUND_operand,size_t lengde_VERDI){while(lengde_VERDI--){unsigned 첫글자=*가++,SEKUND_tegn=*SEKUND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEKUND_tegn>='A'&&SEKUND_tegn<='Z')SEKUND_tegn+=32;if(첫글자!=SEKUND_tegn)return(int)첫글자-(int)SEKUND_tegn;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SEKUND_operand){return strncasecmp(가,SEKUND_operand,(size_t)-1);}
char *strtok_r(char *ord_SMS,const char *skilletegn_VERDI,char **Neste_vare){if(!ord_SMS)ord_SMS=*Neste_vare;while(*ord_SMS&&strchr(skilletegn_VERDI,*ord_SMS))ord_SMS++;if(!*ord_SMS){*Neste_vare=ord_SMS;return 0;}char *처음=ord_SMS;while(*ord_SMS&&!strchr(skilletegn_VERDI,*ord_SMS))ord_SMS++;if(*ord_SMS)*ord_SMS++=0;*Neste_vare=ord_SMS;return 처음;}
unsigned long strtoul(const char *ord_SMS, char **끝, int grunnlag_VERDI) {
    const char *KILDE=ord_SMS;unsigned long VERDI=0;int 음수=0,overløp_VERDI=0;
    while(*ord_SMS==' '||(*ord_SMS>=9&&*ord_SMS<=13))ord_SMS++;
    if(*ord_SMS=='-'||*ord_SMS=='+')음수=*ord_SMS++=='-';
    if((grunnlag_VERDI==0||grunnlag_VERDI==16)&&ord_SMS[0]=='0'&&(ord_SMS[1]=='x'||ord_SMS[1]=='X')&&
       ((ord_SMS[2]>='0'&&ord_SMS[2]<='9')||(ord_SMS[2]>='a'&&ord_SMS[2]<='f')||(ord_SMS[2]>='A'&&ord_SMS[2]<='F'))) {grunnlag_VERDI=16;ord_SMS+=2;}
    if(!grunnlag_VERDI)grunnlag_VERDI=*ord_SMS=='0'?8:10;
    if(grunnlag_VERDI<2||grunnlag_VERDI>36){if(끝)*끝=(char*)KILDE;return 0;}
    const char *처음=ord_SMS;
    for(;;ord_SMS++) {
        unsigned tegn_VERDI=(unsigned char)*ord_SMS;
        unsigned nummer=tegn_VERDI>='0'&&tegn_VERDI<='9'?tegn_VERDI-'0':tegn_VERDI>='a'&&tegn_VERDI<='z'?tegn_VERDI-'a'+10:tegn_VERDI>='A'&&tegn_VERDI<='Z'?tegn_VERDI-'A'+10:36;
        if(nummer>=(unsigned)grunnlag_VERDI)break;
        if(VERDI>(~0ul-nummer)/(unsigned)grunnlag_VERDI)overløp_VERDI=1;
        if(!overløp_VERDI)VERDI=VERDI*(unsigned)grunnlag_VERDI+nummer;
    }
    if(끝)*끝=(char*)(ord_SMS==처음?KILDE:ord_SMS);
    return overløp_VERDI?~0ul:음수?0ul-VERDI:VERDI;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int så_status;
void ekstern_sammendrag(const void *data, size_t lengde_VERDI, unsigned char KR[32]) {
    br_sha256_context kontekst_VERDI;
    br_sha256_init(&kontekst_VERDI); br_sha256_update(&kontekst_VERDI, data, lengde_VERDI); br_sha256_out(&kontekst_VERDI, KR);
    memset(&kontekst_VERDI, 0, sizeof(kontekst_VERDI));
}
#define 난수저장기(Posisjon) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Posisjon)))
int 원격난수(unsigned char *mål_VERDI,unsigned lengde_VERDI){
    if(!så_status){volatile unsigned char *data=(void*)0x01ff0000ul;const char *tusj_VERDI="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)tusj_VERDI[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;så_status=2;}
        else {så_status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(så_status==2){while(lengde_VERDI){unsigned char Neste_vare[32],inndata_VERDI[33];memcpy(inndata_VERDI,모의씨앗,32);inndata_VERDI[32]=0;ekstern_sammendrag(inndata_VERDI,33,Neste_vare);
        inndata_VERDI[32]=1;ekstern_sammendrag(inndata_VERDI,33,모의씨앗);memset(inndata_VERDI,0,33);
        unsigned nummer=lengde_VERDI<32?lengde_VERDI:32;memcpy(mål_VERDI,Neste_vare,nummer);memset(Neste_vare,0,32);mål_VERDI+=nummer;lengde_VERDI-=nummer;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(lengde_VERDI){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VERDI=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&lengde_VERDI;순번++,lengde_VERDI--){*mål_VERDI++=VERDI&255;VERDI>>=8;}}
    return 0;
}
