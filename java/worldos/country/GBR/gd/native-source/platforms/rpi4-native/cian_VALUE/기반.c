/* eitean_VALUE 전용 할당기와 facal_faire_VALUE 난수 공급. cleachdaiche ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct cuimhne_bac { size_t faid_VALUE; struct cuimhne_bac *air_adhart_nì; int 사용; } cuimhne_bac;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static cuimhne_bac *첫조각;
void *sònraich_cian(size_t faid_VALUE) {
    if (!faid_VALUE || faid_VALUE>sizeof(기억터)-64) return 0;
    faid_VALUE=(faid_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->faid_VALUE=sizeof(기억터)-32;}
    for(cuimhne_bac *조각=첫조각;조각;조각=조각->air_adhart_nì)if(!조각->사용&&조각->faid_VALUE>=faid_VALUE){
        if(조각->faid_VALUE>=faid_VALUE+64){cuimhne_bac *새조각=(void*)((char*)조각+32+faid_VALUE);
            새조각->faid_VALUE=조각->faid_VALUE-faid_VALUE-32;새조각->air_adhart_nì=조각->air_adhart_nì;새조각->사용=0;조각->air_adhart_nì=새조각;조각->faid_VALUE=faid_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void sgaoileadh_cian(void *ADDRESS) {
    if(!ADDRESS)return;cuimhne_bac *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->faid_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->air_adhart_nì;){if(!조각->사용&&!조각->air_adhart_nì->사용){조각->faid_VALUE+=32+조각->air_adhart_nì->faid_VALUE;조각->air_adhart_nì=조각->air_adhart_nì->air_adhart_nì;}else 조각=조각->air_adhart_nì;}
}
void *원격재할당(void *ADDRESS,size_t faid_VALUE){
    if(!ADDRESS)return sònraich_cian(faid_VALUE);if(!faid_VALUE){sgaoileadh_cian(ADDRESS);return 0;}
    cuimhne_bac *조각=(void*)((char*)ADDRESS-32);void *새주소=sònraich_cian(faid_VALUE);
    if(새주소){memcpy(새주소,ADDRESS,faid_VALUE<조각->faid_VALUE?faid_VALUE:조각->faid_VALUE);sgaoileadh_cian(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int caractar_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)caractar_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t faid_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,faid_VALUE))return(char*)Word_SMS;return faid_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *ceann_uidhe_VALUE,const char *원본,size_t faid_VALUE){size_t 순번=0;for(;순번<faid_VALUE&&원본[순번];순번++)ceann_uidhe_VALUE[순번]=원본[순번];for(;순번<faid_VALUE;순번++)ceann_uidhe_VALUE[순번]=0;return ceann_uidhe_VALUE;}
char *strncat(char *ceann_uidhe_VALUE,const char *원본,size_t faid_VALUE){char *끝=ceann_uidhe_VALUE+strlen(ceann_uidhe_VALUE);while(faid_VALUE--&&*원본)*끝++=*원본++;*끝=0;return ceann_uidhe_VALUE;}
int strncasecmp(const char *가,const char *나,size_t faid_VALUE){while(faid_VALUE--){unsigned 첫글자=*가++,SECOND_caractar=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_caractar>='A'&&SECOND_caractar<='Z')SECOND_caractar+=32;if(첫글자!=SECOND_caractar)return(int)첫글자-(int)SECOND_caractar;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *comharra_crìche_VALUE,char **air_adhart_nì){if(!Word_SMS)Word_SMS=*air_adhart_nì;while(*Word_SMS&&strchr(comharra_crìche_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*air_adhart_nì=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(comharra_crìche_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*air_adhart_nì=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *tùs=Word_SMS;unsigned long VALUE=0;int 음수=0,taomadh_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)tùs;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned caractar_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=caractar_VALUE>='0'&&caractar_VALUE<='9'?caractar_VALUE-'0':caractar_VALUE>='a'&&caractar_VALUE<='z'?caractar_VALUE-'a'+10:caractar_VALUE>='A'&&caractar_VALUE<='Z'?caractar_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)taomadh_VALUE=1;
        if(!taomadh_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?tùs:Word_SMS);
    return taomadh_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int sìol_cor;
void 원격요약(const void *dàta, size_t faid_VALUE, unsigned char tomhas[32]) {
    br_sha256_context co_theacsa_VALUE;
    br_sha256_init(&co_theacsa_VALUE); br_sha256_update(&co_theacsa_VALUE, dàta, faid_VALUE); br_sha256_out(&co_theacsa_VALUE, tomhas);
    memset(&co_theacsa_VALUE, 0, sizeof(co_theacsa_VALUE));
}
#define 난수저장기(suidhich) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(suidhich)))
int 원격난수(unsigned char *ceann_uidhe_VALUE,unsigned faid_VALUE){
    if(!sìol_cor){volatile unsigned char *dàta=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=dàta[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=dàta[8+순번];for(unsigned 순번=0;순번<40;순번++)dàta[순번]=0;sìol_cor=2;}
        else {sìol_cor=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(sìol_cor==2){while(faid_VALUE){unsigned char air_adhart_nì[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,air_adhart_nì);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=faid_VALUE<32?faid_VALUE:32;memcpy(ceann_uidhe_VALUE,air_adhart_nì,수);memset(air_adhart_nì,0,32);ceann_uidhe_VALUE+=수;faid_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(faid_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&faid_VALUE;순번++,faid_VALUE--){*ceann_uidhe_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
