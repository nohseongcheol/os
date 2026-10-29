/* kjarni_VALUE 전용 할당기와 aðgangsorð_VALUE 난수 공급. notandi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Minni_útiloka { size_t lengd_VALUE; struct Minni_útiloka *Áfram_vara; int 사용; } Minni_útiloka;
static unsigned char Minni_Arena[2*1024*1024] __attribute__((aligned(16)));
static Minni_útiloka *첫조각;
void *úthluta_fjartengdur(size_t lengd_VALUE) {
    if (!lengd_VALUE || lengd_VALUE>sizeof(Minni_Arena)-64) return 0;
    lengd_VALUE=(lengd_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Minni_Arena;첫조각->lengd_VALUE=sizeof(Minni_Arena)-32;}
    for(Minni_útiloka *조각=첫조각;조각;조각=조각->Áfram_vara)if(!조각->사용&&조각->lengd_VALUE>=lengd_VALUE){
        if(조각->lengd_VALUE>=lengd_VALUE+64){Minni_útiloka *새조각=(void*)((char*)조각+32+lengd_VALUE);
            새조각->lengd_VALUE=조각->lengd_VALUE-lengd_VALUE-32;새조각->Áfram_vara=조각->Áfram_vara;새조각->사용=0;조각->Áfram_vara=새조각;조각->lengd_VALUE=lengd_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void losa_fjartengdur(void *slóð) {
    if(!slóð)return;Minni_útiloka *조각=(void*)((char*)slóð-32);
    volatile unsigned char *지움=slóð;for(size_t 순번=0;순번<조각->lengd_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Áfram_vara;){if(!조각->사용&&!조각->Áfram_vara->사용){조각->lengd_VALUE+=32+조각->Áfram_vara->lengd_VALUE;조각->Áfram_vara=조각->Áfram_vara->Áfram_vara;}else 조각=조각->Áfram_vara;}
}
void *원격재할당(void *slóð,size_t lengd_VALUE){
    if(!slóð)return úthluta_fjartengdur(lengd_VALUE);if(!lengd_VALUE){losa_fjartengdur(slóð);return 0;}
    Minni_útiloka *조각=(void*)((char*)slóð-32);void *새주소=úthluta_fjartengdur(lengd_VALUE);
    if(새주소){memcpy(새주소,slóð,lengd_VALUE<조각->lengd_VALUE?lengd_VALUE:조각->lengd_VALUE);losa_fjartengdur(slóð);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int stafur_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)stafur_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t lengd_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,lengd_VALUE))return(char*)Word_SMS;return lengd_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *endastaður_VALUE,const char *원본,size_t lengd_VALUE){size_t 순번=0;for(;순번<lengd_VALUE&&원본[순번];순번++)endastaður_VALUE[순번]=원본[순번];for(;순번<lengd_VALUE;순번++)endastaður_VALUE[순번]=0;return endastaður_VALUE;}
char *strncat(char *endastaður_VALUE,const char *원본,size_t lengd_VALUE){char *끝=endastaður_VALUE+strlen(endastaður_VALUE);while(lengd_VALUE--&&*원본)*끝++=*원본++;*끝=0;return endastaður_VALUE;}
int strncasecmp(const char *가,const char *나,size_t lengd_VALUE){while(lengd_VALUE--){unsigned 첫글자=*가++,SECOND_stafur=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_stafur>='A'&&SECOND_stafur<='Z')SECOND_stafur+=32;if(첫글자!=SECOND_stafur)return(int)첫글자-(int)SECOND_stafur;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *skiltákn_VALUE_d8ba4873,char **Áfram_vara){if(!Word_SMS)Word_SMS=*Áfram_vara;while(*Word_SMS&&strchr(skiltákn_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Áfram_vara=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(skiltákn_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Áfram_vara=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *Uppruni=Word_SMS;unsigned long VALUE=0;int 음수=0,yfirflæði_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)Uppruni;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned stafur_VALUE=(unsigned char)*Word_SMS;
        unsigned númer=stafur_VALUE>='0'&&stafur_VALUE<='9'?stafur_VALUE-'0':stafur_VALUE>='a'&&stafur_VALUE<='z'?stafur_VALUE-'a'+10:stafur_VALUE>='A'&&stafur_VALUE<='Z'?stafur_VALUE-'A'+10:36;
        if(númer>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-númer)/(unsigned)BASE_VALUE)yfirflæði_VALUE=1;
        if(!yfirflæði_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+númer;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?Uppruni:Word_SMS);
    return yfirflæði_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int fræ_staða;
void fjartengdur_samantekt(const void *gögn, size_t lengd_VALUE, unsigned char NIÐURSTAÐA[32]) {
    br_sha256_context Samhengi_VALUE;
    br_sha256_init(&Samhengi_VALUE); br_sha256_update(&Samhengi_VALUE, gögn, lengd_VALUE); br_sha256_out(&Samhengi_VALUE, NIÐURSTAÐA);
    memset(&Samhengi_VALUE, 0, sizeof(Samhengi_VALUE));
}
#define 난수저장기(Staðsetning) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Staðsetning)))
int 원격난수(unsigned char *endastaður_VALUE,unsigned lengd_VALUE){
    if(!fræ_staða){volatile unsigned char *gögn=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=gögn[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=gögn[8+순번];for(unsigned 순번=0;순번<40;순번++)gögn[순번]=0;fræ_staða=2;}
        else {fræ_staða=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(fræ_staða==2){while(lengd_VALUE){unsigned char Áfram_vara[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;fjartengdur_samantekt(입력,33,Áfram_vara);
        입력[32]=1;fjartengdur_samantekt(입력,33,모의씨앗);memset(입력,0,33);
        unsigned númer=lengd_VALUE<32?lengd_VALUE:32;memcpy(endastaður_VALUE,Áfram_vara,númer);memset(Áfram_vara,0,32);endastaður_VALUE+=númer;lengd_VALUE-=númer;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(lengd_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&lengd_VALUE;순번++,lengd_VALUE--){*endastaður_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
