/* eithne_VALUE 전용 할당기와 pasfhocal_VALUE 난수 공급. úsáideoir ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Cuimhne_bac { size_t fad_VALUE; struct Cuimhne_bac *Ar_aghaidh_mír; int 사용; } Cuimhne_bac;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static Cuimhne_bac *첫조각;
void *leithdháil_cianda(size_t fad_VALUE) {
    if (!fad_VALUE || fad_VALUE>sizeof(기억터)-64) return 0;
    fad_VALUE=(fad_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->fad_VALUE=sizeof(기억터)-32;}
    for(Cuimhne_bac *조각=첫조각;조각;조각=조각->Ar_aghaidh_mír)if(!조각->사용&&조각->fad_VALUE>=fad_VALUE){
        if(조각->fad_VALUE>=fad_VALUE+64){Cuimhne_bac *새조각=(void*)((char*)조각+32+fad_VALUE);
            새조각->fad_VALUE=조각->fad_VALUE-fad_VALUE-32;새조각->Ar_aghaidh_mír=조각->Ar_aghaidh_mír;새조각->사용=0;조각->Ar_aghaidh_mír=새조각;조각->fad_VALUE=fad_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void leagan_cianda(void *ADDRESS) {
    if(!ADDRESS)return;Cuimhne_bac *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->fad_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Ar_aghaidh_mír;){if(!조각->사용&&!조각->Ar_aghaidh_mír->사용){조각->fad_VALUE+=32+조각->Ar_aghaidh_mír->fad_VALUE;조각->Ar_aghaidh_mír=조각->Ar_aghaidh_mír->Ar_aghaidh_mír;}else 조각=조각->Ar_aghaidh_mír;}
}
void *원격재할당(void *ADDRESS,size_t fad_VALUE){
    if(!ADDRESS)return leithdháil_cianda(fad_VALUE);if(!fad_VALUE){leagan_cianda(ADDRESS);return 0;}
    Cuimhne_bac *조각=(void*)((char*)ADDRESS-32);void *새주소=leithdháil_cianda(fad_VALUE);
    if(새주소){memcpy(새주소,ADDRESS,fad_VALUE<조각->fad_VALUE?fad_VALUE:조각->fad_VALUE);leagan_cianda(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int carachtar_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)carachtar_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t fad_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,fad_VALUE))return(char*)Word_SMS;return fad_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *sprioc_VALUE,const char *원본,size_t fad_VALUE){size_t 순번=0;for(;순번<fad_VALUE&&원본[순번];순번++)sprioc_VALUE[순번]=원본[순번];for(;순번<fad_VALUE;순번++)sprioc_VALUE[순번]=0;return sprioc_VALUE;}
char *strncat(char *sprioc_VALUE,const char *원본,size_t fad_VALUE){char *끝=sprioc_VALUE+strlen(sprioc_VALUE);while(fad_VALUE--&&*원본)*끝++=*원본++;*끝=0;return sprioc_VALUE;}
int strncasecmp(const char *가,const char *나,size_t fad_VALUE){while(fad_VALUE--){unsigned 첫글자=*가++,SECOND_carachtar=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_carachtar>='A'&&SECOND_carachtar<='Z')SECOND_carachtar+=32;if(첫글자!=SECOND_carachtar)return(int)첫글자-(int)SECOND_carachtar;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *teormharcóir_VALUE,char **Ar_aghaidh_mír){if(!Word_SMS)Word_SMS=*Ar_aghaidh_mír;while(*Word_SMS&&strchr(teormharcóir_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Ar_aghaidh_mír=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(teormharcóir_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Ar_aghaidh_mír=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *FOINSE=Word_SMS;unsigned long VALUE=0;int 음수=0,róshreabhadh_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)FOINSE;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned carachtar_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=carachtar_VALUE>='0'&&carachtar_VALUE<='9'?carachtar_VALUE-'0':carachtar_VALUE>='a'&&carachtar_VALUE<='z'?carachtar_VALUE-'a'+10:carachtar_VALUE>='A'&&carachtar_VALUE<='Z'?carachtar_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)róshreabhadh_VALUE=1;
        if(!róshreabhadh_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?FOINSE:Word_SMS);
    return róshreabhadh_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int síol_staid;
void cianda_achoimre(const void *sonraí, size_t fad_VALUE, unsigned char tomhas[32]) {
    br_sha256_context Comhthéacs_VALUE;
    br_sha256_init(&Comhthéacs_VALUE); br_sha256_update(&Comhthéacs_VALUE, sonraí, fad_VALUE); br_sha256_out(&Comhthéacs_VALUE, tomhas);
    memset(&Comhthéacs_VALUE, 0, sizeof(Comhthéacs_VALUE));
}
#define 난수저장기(suíomh) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(suíomh)))
int 원격난수(unsigned char *sprioc_VALUE,unsigned fad_VALUE){
    if(!síol_staid){volatile unsigned char *sonraí=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=sonraí[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=sonraí[8+순번];for(unsigned 순번=0;순번<40;순번++)sonraí[순번]=0;síol_staid=2;}
        else {síol_staid=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(síol_staid==2){while(fad_VALUE){unsigned char Ar_aghaidh_mír[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;cianda_achoimre(입력,33,Ar_aghaidh_mír);
        입력[32]=1;cianda_achoimre(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=fad_VALUE<32?fad_VALUE:32;memcpy(sprioc_VALUE,Ar_aghaidh_mír,수);memset(Ar_aghaidh_mír,0,32);sprioc_VALUE+=수;fad_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(fad_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&fad_VALUE;순번++,fad_VALUE--){*sprioc_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
