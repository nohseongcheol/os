/* kjerne_VALUE 전용 할당기와 passord_VALUE 난수 공급. brukar ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Minne_Blokker { size_t lengd_VALUE; struct Minne_Blokker *Neste_vare; int 사용; } Minne_Blokker;
static unsigned char Minne_Arena[2*1024*1024] __attribute__((aligned(16)));
static Minne_Blokker *첫조각;
void *tildele_fjern(size_t lengd_VALUE) {
    if (!lengd_VALUE || lengd_VALUE>sizeof(Minne_Arena)-64) return 0;
    lengd_VALUE=(lengd_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Minne_Arena;첫조각->lengd_VALUE=sizeof(Minne_Arena)-32;}
    for(Minne_Blokker *조각=첫조각;조각;조각=조각->Neste_vare)if(!조각->사용&&조각->lengd_VALUE>=lengd_VALUE){
        if(조각->lengd_VALUE>=lengd_VALUE+64){Minne_Blokker *새조각=(void*)((char*)조각+32+lengd_VALUE);
            새조각->lengd_VALUE=조각->lengd_VALUE-lengd_VALUE-32;새조각->Neste_vare=조각->Neste_vare;새조각->사용=0;조각->Neste_vare=새조각;조각->lengd_VALUE=lengd_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void frigi_fjern(void *ADDRESS) {
    if(!ADDRESS)return;Minne_Blokker *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->lengd_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Neste_vare;){if(!조각->사용&&!조각->Neste_vare->사용){조각->lengd_VALUE+=32+조각->Neste_vare->lengd_VALUE;조각->Neste_vare=조각->Neste_vare->Neste_vare;}else 조각=조각->Neste_vare;}
}
void *원격재할당(void *ADDRESS,size_t lengd_VALUE){
    if(!ADDRESS)return tildele_fjern(lengd_VALUE);if(!lengd_VALUE){frigi_fjern(ADDRESS);return 0;}
    Minne_Blokker *조각=(void*)((char*)ADDRESS-32);void *새주소=tildele_fjern(lengd_VALUE);
    if(새주소){memcpy(새주소,ADDRESS,lengd_VALUE<조각->lengd_VALUE?lengd_VALUE:조각->lengd_VALUE);frigi_fjern(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int teikn_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)teikn_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t lengd_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,lengd_VALUE))return(char*)Word_SMS;return lengd_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *mål_VALUE,const char *원본,size_t lengd_VALUE){size_t 순번=0;for(;순번<lengd_VALUE&&원본[순번];순번++)mål_VALUE[순번]=원본[순번];for(;순번<lengd_VALUE;순번++)mål_VALUE[순번]=0;return mål_VALUE;}
char *strncat(char *mål_VALUE,const char *원본,size_t lengd_VALUE){char *끝=mål_VALUE+strlen(mål_VALUE);while(lengd_VALUE--&&*원본)*끝++=*원본++;*끝=0;return mål_VALUE;}
int strncasecmp(const char *가,const char *나,size_t lengd_VALUE){while(lengd_VALUE--){unsigned 첫글자=*가++,SECOND_teikn=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_teikn>='A'&&SECOND_teikn<='Z')SECOND_teikn+=32;if(첫글자!=SECOND_teikn)return(int)첫글자-(int)SECOND_teikn;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *skiljeteikn_VALUE,char **Neste_vare){if(!Word_SMS)Word_SMS=*Neste_vare;while(*Word_SMS&&strchr(skiljeteikn_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Neste_vare=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(skiljeteikn_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Neste_vare=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *KJELDE=Word_SMS;unsigned long VALUE=0;int 음수=0,overflyt_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)KJELDE;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned teikn_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=teikn_VALUE>='0'&&teikn_VALUE<='9'?teikn_VALUE-'0':teikn_VALUE>='a'&&teikn_VALUE<='z'?teikn_VALUE-'a'+10:teikn_VALUE>='A'&&teikn_VALUE<='Z'?teikn_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)overflyt_VALUE=1;
        if(!overflyt_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?KJELDE:Word_SMS);
    return overflyt_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int startverdi_status;
void fjern_samandrag(const void *data, size_t lengd_VALUE, unsigned char forretningsmål[32]) {
    br_sha256_context kontekst_VALUE;
    br_sha256_init(&kontekst_VALUE); br_sha256_update(&kontekst_VALUE, data, lengd_VALUE); br_sha256_out(&kontekst_VALUE, forretningsmål);
    memset(&kontekst_VALUE, 0, sizeof(kontekst_VALUE));
}
#define 난수저장기(Posisjon) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Posisjon)))
int 원격난수(unsigned char *mål_VALUE,unsigned lengd_VALUE){
    if(!startverdi_status){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;startverdi_status=2;}
        else {startverdi_status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(startverdi_status==2){while(lengd_VALUE){unsigned char Neste_vare[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;fjern_samandrag(입력,33,Neste_vare);
        입력[32]=1;fjern_samandrag(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=lengd_VALUE<32?lengd_VALUE:32;memcpy(mål_VALUE,Neste_vare,수);memset(Neste_vare,0,32);mål_VALUE+=수;lengd_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(lengd_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&lengd_VALUE;순번++,lengd_VALUE--){*mål_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
