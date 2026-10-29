/* cnewyllyn_VALUE 전용 할당기와 cyfrinair_VALUE 난수 공급. defnyddiwr ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Cof_rhwystro { size_t hyd_VALUE; struct Cof_rhwystro *Nesaf_eitem; int 사용; } Cof_rhwystro;
static unsigned char Cof_Are[2*1024*1024] __attribute__((aligned(16)));
static Cof_rhwystro *첫조각;
void *dyrannu_pell(size_t hyd_VALUE) {
    if (!hyd_VALUE || hyd_VALUE>sizeof(Cof_Are)-64) return 0;
    hyd_VALUE=(hyd_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Cof_Are;첫조각->hyd_VALUE=sizeof(Cof_Are)-32;}
    for(Cof_rhwystro *조각=첫조각;조각;조각=조각->Nesaf_eitem)if(!조각->사용&&조각->hyd_VALUE>=hyd_VALUE){
        if(조각->hyd_VALUE>=hyd_VALUE+64){Cof_rhwystro *새조각=(void*)((char*)조각+32+hyd_VALUE);
            새조각->hyd_VALUE=조각->hyd_VALUE-hyd_VALUE-32;새조각->Nesaf_eitem=조각->Nesaf_eitem;새조각->사용=0;조각->Nesaf_eitem=새조각;조각->hyd_VALUE=hyd_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void rhyddhau_pell(void *ADDRESS) {
    if(!ADDRESS)return;Cof_rhwystro *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->hyd_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Nesaf_eitem;){if(!조각->사용&&!조각->Nesaf_eitem->사용){조각->hyd_VALUE+=32+조각->Nesaf_eitem->hyd_VALUE;조각->Nesaf_eitem=조각->Nesaf_eitem->Nesaf_eitem;}else 조각=조각->Nesaf_eitem;}
}
void *원격재할당(void *ADDRESS,size_t hyd_VALUE){
    if(!ADDRESS)return dyrannu_pell(hyd_VALUE);if(!hyd_VALUE){rhyddhau_pell(ADDRESS);return 0;}
    Cof_rhwystro *조각=(void*)((char*)ADDRESS-32);void *새주소=dyrannu_pell(hyd_VALUE);
    if(새주소){memcpy(새주소,ADDRESS,hyd_VALUE<조각->hyd_VALUE?hyd_VALUE:조각->hyd_VALUE);rhyddhau_pell(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int nod_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)nod_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t hyd_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,hyd_VALUE))return(char*)Word_SMS;return hyd_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *cyrchfan_VALUE,const char *원본,size_t hyd_VALUE){size_t 순번=0;for(;순번<hyd_VALUE&&원본[순번];순번++)cyrchfan_VALUE[순번]=원본[순번];for(;순번<hyd_VALUE;순번++)cyrchfan_VALUE[순번]=0;return cyrchfan_VALUE;}
char *strncat(char *cyrchfan_VALUE,const char *원본,size_t hyd_VALUE){char *끝=cyrchfan_VALUE+strlen(cyrchfan_VALUE);while(hyd_VALUE--&&*원본)*끝++=*원본++;*끝=0;return cyrchfan_VALUE;}
int strncasecmp(const char *가,const char *나,size_t hyd_VALUE){while(hyd_VALUE--){unsigned 첫글자=*가++,SECOND_nod=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_nod>='A'&&SECOND_nod<='Z')SECOND_nod+=32;if(첫글자!=SECOND_nod)return(int)첫글자-(int)SECOND_nod;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *amffinydd_VALUE,char **Nesaf_eitem){if(!Word_SMS)Word_SMS=*Nesaf_eitem;while(*Word_SMS&&strchr(amffinydd_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Nesaf_eitem=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(amffinydd_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Nesaf_eitem=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *FFYNHONNELL=Word_SMS;unsigned long VALUE=0;int 음수=0,gorlif_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)FFYNHONNELL;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned nod_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=nod_VALUE>='0'&&nod_VALUE<='9'?nod_VALUE-'0':nod_VALUE>='a'&&nod_VALUE<='z'?nod_VALUE-'a'+10:nod_VALUE>='A'&&nod_VALUE<='Z'?nod_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)gorlif_VALUE=1;
        if(!gorlif_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?FFYNHONNELL:Word_SMS);
    return gorlif_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int dosbarthiad_cyflwr;
void pell_crynodeb(const void *data, size_t hyd_VALUE, unsigned char mesur[32]) {
    br_sha256_context Cyd_destun_VALUE;
    br_sha256_init(&Cyd_destun_VALUE); br_sha256_update(&Cyd_destun_VALUE, data, hyd_VALUE); br_sha256_out(&Cyd_destun_VALUE, mesur);
    memset(&Cyd_destun_VALUE, 0, sizeof(Cyd_destun_VALUE));
}
#define 난수저장기(safle) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(safle)))
int 원격난수(unsigned char *cyrchfan_VALUE,unsigned hyd_VALUE){
    if(!dosbarthiad_cyflwr){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;dosbarthiad_cyflwr=2;}
        else {dosbarthiad_cyflwr=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(dosbarthiad_cyflwr==2){while(hyd_VALUE){unsigned char Nesaf_eitem[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;pell_crynodeb(입력,33,Nesaf_eitem);
        입력[32]=1;pell_crynodeb(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=hyd_VALUE<32?hyd_VALUE:32;memcpy(cyrchfan_VALUE,Nesaf_eitem,수);memset(Nesaf_eitem,0,32);cyrchfan_VALUE+=수;hyd_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(hyd_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&hyd_VALUE;순번++,hyd_VALUE--){*cyrchfan_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
