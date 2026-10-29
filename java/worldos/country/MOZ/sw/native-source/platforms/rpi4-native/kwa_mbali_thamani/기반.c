/* kiini_thamani_0611a8a8 전용 할당기와 nywila_thamani 난수 공급. mtumiaji ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct kumbukumbu_zuia { size_t urefu_thamani; struct kumbukumbu_zuia *다음; int 사용; } kumbukumbu_zuia;
static unsigned char kumbukumbu_Uwanja_wa_mchezo[2*1024*1024] __attribute__((aligned(16)));
static kumbukumbu_zuia *첫조각;
void *tengea_kwa_mbali(size_t urefu_thamani) {
    if (!urefu_thamani || urefu_thamani>sizeof(kumbukumbu_Uwanja_wa_mchezo)-64) return 0;
    urefu_thamani=(urefu_thamani+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)kumbukumbu_Uwanja_wa_mchezo;첫조각->urefu_thamani=sizeof(kumbukumbu_Uwanja_wa_mchezo)-32;}
    for(kumbukumbu_zuia *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->urefu_thamani>=urefu_thamani){
        if(조각->urefu_thamani>=urefu_thamani+64){kumbukumbu_zuia *새조각=(void*)((char*)조각+32+urefu_thamani);
            새조각->urefu_thamani=조각->urefu_thamani-urefu_thamani-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->urefu_thamani=urefu_thamani;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void toleo_kwa_mbali(void *anwani) {
    if(!anwani)return;kumbukumbu_zuia *조각=(void*)((char*)anwani-32);
    volatile unsigned char *지움=anwani;for(size_t 순번=0;순번<조각->urefu_thamani;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->urefu_thamani+=32+조각->다음->urefu_thamani;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *anwani,size_t urefu_thamani){
    if(!anwani)return tengea_kwa_mbali(urefu_thamani);if(!urefu_thamani){toleo_kwa_mbali(anwani);return 0;}
    kumbukumbu_zuia *조각=(void*)((char*)anwani-32);void *새주소=tengea_kwa_mbali(urefu_thamani);
    if(새주소){memcpy(새주소,anwani,urefu_thamani<조각->urefu_thamani?urefu_thamani:조각->urefu_thamani);toleo_kwa_mbali(anwani);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Neno_SMS,int kibambo_thamani){for(;;Neno_SMS++){if(*Neno_SMS==(char)kibambo_thamani)return(char*)Neno_SMS;if(!*Neno_SMS)return 0;}}
char *strstr(const char *Neno_SMS,const char *찾음){size_t urefu_thamani=strlen(찾음);for(;*Neno_SMS;Neno_SMS++)if(!strncmp(Neno_SMS,찾음,urefu_thamani))return(char*)Neno_SMS;return urefu_thamani?0:(char*)Neno_SMS;}
char *strncpy(char *fikio_thamani,const char *원본,size_t urefu_thamani){size_t 순번=0;for(;순번<urefu_thamani&&원본[순번];순번++)fikio_thamani[순번]=원본[순번];for(;순번<urefu_thamani;순번++)fikio_thamani[순번]=0;return fikio_thamani;}
char *strncat(char *fikio_thamani,const char *원본,size_t urefu_thamani){char *끝=fikio_thamani+strlen(fikio_thamani);while(urefu_thamani--&&*원본)*끝++=*원본++;*끝=0;return fikio_thamani;}
int strncasecmp(const char *가,const char *나,size_t urefu_thamani){while(urefu_thamani--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Neno_SMS,const char *kitenganishi_thamani_d8ba4873,char **다음){if(!Neno_SMS)Neno_SMS=*다음;while(*Neno_SMS&&strchr(kitenganishi_thamani_d8ba4873,*Neno_SMS))Neno_SMS++;if(!*Neno_SMS){*다음=Neno_SMS;return 0;}char *처음=Neno_SMS;while(*Neno_SMS&&!strchr(kitenganishi_thamani_d8ba4873,*Neno_SMS))Neno_SMS++;if(*Neno_SMS)*Neno_SMS++=0;*다음=Neno_SMS;return 처음;}
unsigned long strtoul(const char *Neno_SMS, char **끝, int 밑) {
    const char *chanzo=Neno_SMS;unsigned long thamani=0;int 음수=0,ziada_thamani=0;
    while(*Neno_SMS==' '||(*Neno_SMS>=9&&*Neno_SMS<=13))Neno_SMS++;
    if(*Neno_SMS=='-'||*Neno_SMS=='+')음수=*Neno_SMS++=='-';
    if((밑==0||밑==16)&&Neno_SMS[0]=='0'&&(Neno_SMS[1]=='x'||Neno_SMS[1]=='X')&&
       ((Neno_SMS[2]>='0'&&Neno_SMS[2]<='9')||(Neno_SMS[2]>='a'&&Neno_SMS[2]<='f')||(Neno_SMS[2]>='A'&&Neno_SMS[2]<='F'))) {밑=16;Neno_SMS+=2;}
    if(!밑)밑=*Neno_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)chanzo;return 0;}
    const char *처음=Neno_SMS;
    for(;;Neno_SMS++) {
        unsigned kibambo_thamani=(unsigned char)*Neno_SMS;
        unsigned 수=kibambo_thamani>='0'&&kibambo_thamani<='9'?kibambo_thamani-'0':kibambo_thamani>='a'&&kibambo_thamani<='z'?kibambo_thamani-'a'+10:kibambo_thamani>='A'&&kibambo_thamani<='Z'?kibambo_thamani-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(thamani>(~0ul-수)/(unsigned)밑)ziada_thamani=1;
        if(!ziada_thamani)thamani=thamani*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Neno_SMS==처음?chanzo:Neno_SMS);
    return ziada_thamani?~0ul:음수?0ul-thamani:thamani;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int pakia_hali;
void kwa_mbali_muhtasari(const void *data, size_t urefu_thamani, unsigned char 결과[32]) {
    br_sha256_context Muktadha_thamani;
    br_sha256_init(&Muktadha_thamani); br_sha256_update(&Muktadha_thamani, data, urefu_thamani); br_sha256_out(&Muktadha_thamani, 결과);
    memset(&Muktadha_thamani, 0, sizeof(Muktadha_thamani));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *fikio_thamani,unsigned urefu_thamani){
    if(!pakia_hali){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;pakia_hali=2;}
        else {pakia_hali=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(pakia_hali==2){while(urefu_thamani){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;kwa_mbali_muhtasari(입력,33,다음);
        입력[32]=1;kwa_mbali_muhtasari(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=urefu_thamani<32?urefu_thamani:32;memcpy(fikio_thamani,다음,수);memset(다음,0,32);fikio_thamani+=수;urefu_thamani-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(urefu_thamani){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t thamani=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&urefu_thamani;순번++,urefu_thamani--){*fikio_thamani++=thamani&255;thamani>>=8;}}
    return 0;
}
