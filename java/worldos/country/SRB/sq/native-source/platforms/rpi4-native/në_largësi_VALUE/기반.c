/* bërthamë_VALUE 전용 할당기와 fjalëkalim_VALUE 난수 공급. përdorues ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memorie_bllokoj { size_t gjatësi_VALUE; struct Memorie_bllokoj *Tjetër_njësi; int 사용; } Memorie_bllokoj;
static unsigned char Memorie_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memorie_bllokoj *첫조각;
void *caktoj_në_largësi(size_t gjatësi_VALUE) {
    if (!gjatësi_VALUE || gjatësi_VALUE>sizeof(Memorie_Arena)-64) return 0;
    gjatësi_VALUE=(gjatësi_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memorie_Arena;첫조각->gjatësi_VALUE=sizeof(Memorie_Arena)-32;}
    for(Memorie_bllokoj *조각=첫조각;조각;조각=조각->Tjetër_njësi)if(!조각->사용&&조각->gjatësi_VALUE>=gjatësi_VALUE){
        if(조각->gjatësi_VALUE>=gjatësi_VALUE+64){Memorie_bllokoj *새조각=(void*)((char*)조각+32+gjatësi_VALUE);
            새조각->gjatësi_VALUE=조각->gjatësi_VALUE-gjatësi_VALUE-32;새조각->Tjetër_njësi=조각->Tjetër_njësi;새조각->사용=0;조각->Tjetër_njësi=새조각;조각->gjatësi_VALUE=gjatësi_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void liroj_në_largësi(void *email) {
    if(!email)return;Memorie_bllokoj *조각=(void*)((char*)email-32);
    volatile unsigned char *지움=email;for(size_t 순번=0;순번<조각->gjatësi_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Tjetër_njësi;){if(!조각->사용&&!조각->Tjetër_njësi->사용){조각->gjatësi_VALUE+=32+조각->Tjetër_njësi->gjatësi_VALUE;조각->Tjetër_njësi=조각->Tjetër_njësi->Tjetër_njësi;}else 조각=조각->Tjetër_njësi;}
}
void *원격재할당(void *email,size_t gjatësi_VALUE){
    if(!email)return caktoj_në_largësi(gjatësi_VALUE);if(!gjatësi_VALUE){liroj_në_largësi(email);return 0;}
    Memorie_bllokoj *조각=(void*)((char*)email-32);void *새주소=caktoj_në_largësi(gjatësi_VALUE);
    if(새주소){memcpy(새주소,email,gjatësi_VALUE<조각->gjatësi_VALUE?gjatësi_VALUE:조각->gjatësi_VALUE);liroj_në_largësi(email);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int karakter_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)karakter_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t gjatësi_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,gjatësi_VALUE))return(char*)Word_SMS;return gjatësi_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *vendmbërritje_VALUE,const char *원본,size_t gjatësi_VALUE){size_t 순번=0;for(;순번<gjatësi_VALUE&&원본[순번];순번++)vendmbërritje_VALUE[순번]=원본[순번];for(;순번<gjatësi_VALUE;순번++)vendmbërritje_VALUE[순번]=0;return vendmbërritje_VALUE;}
char *strncat(char *vendmbërritje_VALUE,const char *원본,size_t gjatësi_VALUE){char *끝=vendmbërritje_VALUE+strlen(vendmbërritje_VALUE);while(gjatësi_VALUE--&&*원본)*끝++=*원본++;*끝=0;return vendmbërritje_VALUE;}
int strncasecmp(const char *가,const char *나,size_t gjatësi_VALUE){while(gjatësi_VALUE--){unsigned 첫글자=*가++,SECOND_karakter=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_karakter>='A'&&SECOND_karakter<='Z')SECOND_karakter+=32;if(첫글자!=SECOND_karakter)return(int)첫글자-(int)SECOND_karakter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *kufizues_VALUE,char **Tjetër_njësi){if(!Word_SMS)Word_SMS=*Tjetër_njësi;while(*Word_SMS&&strchr(kufizues_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Tjetër_njësi=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(kufizues_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Tjetër_njësi=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *BURIMI=Word_SMS;unsigned long VALUE=0;int 음수=0,tejkalim_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)BURIMI;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned karakter_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=karakter_VALUE>='0'&&karakter_VALUE<='9'?karakter_VALUE-'0':karakter_VALUE>='a'&&karakter_VALUE<='z'?karakter_VALUE-'a'+10:karakter_VALUE>='A'&&karakter_VALUE<='Z'?karakter_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)tejkalim_VALUE=1;
        if(!tejkalim_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?BURIMI:Word_SMS);
    return tejkalim_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int jap_status;
void në_largësi_përmbledhje(const void *të_dhëna, size_t gjatësi_VALUE, unsigned char llogaritje[32]) {
    br_sha256_context Konteksti_VALUE;
    br_sha256_init(&Konteksti_VALUE); br_sha256_update(&Konteksti_VALUE, të_dhëna, gjatësi_VALUE); br_sha256_out(&Konteksti_VALUE, llogaritje);
    memset(&Konteksti_VALUE, 0, sizeof(Konteksti_VALUE));
}
#define 난수저장기(Pozicioni) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Pozicioni)))
int 원격난수(unsigned char *vendmbërritje_VALUE,unsigned gjatësi_VALUE){
    if(!jap_status){volatile unsigned char *të_dhëna=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=të_dhëna[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=të_dhëna[8+순번];for(unsigned 순번=0;순번<40;순번++)të_dhëna[순번]=0;jap_status=2;}
        else {jap_status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(jap_status==2){while(gjatësi_VALUE){unsigned char Tjetër_njësi[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;në_largësi_përmbledhje(입력,33,Tjetër_njësi);
        입력[32]=1;në_largësi_përmbledhje(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=gjatësi_VALUE<32?gjatësi_VALUE:32;memcpy(vendmbërritje_VALUE,Tjetër_njësi,수);memset(Tjetër_njësi,0,32);vendmbërritje_VALUE+=수;gjatësi_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(gjatësi_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&gjatësi_VALUE;순번++,gjatësi_VALUE--){*vendmbërritje_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
