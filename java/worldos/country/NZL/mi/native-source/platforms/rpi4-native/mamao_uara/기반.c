/* kākano_uara_0611a8a8 전용 할당기와 kupuhipa_uara 난수 공급. kaiwhakamahi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Pūmahara_aukati { size_t roa_uara; struct Pūmahara_aukati *Panuku_tuemi; int 사용; } Pūmahara_aukati;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static Pūmahara_aukati *첫조각;
void *tiritiri_mamao(size_t roa_uara) {
    if (!roa_uara || roa_uara>sizeof(기억터)-64) return 0;
    roa_uara=(roa_uara+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->roa_uara=sizeof(기억터)-32;}
    for(Pūmahara_aukati *조각=첫조각;조각;조각=조각->Panuku_tuemi)if(!조각->사용&&조각->roa_uara>=roa_uara){
        if(조각->roa_uara>=roa_uara+64){Pūmahara_aukati *새조각=(void*)((char*)조각+32+roa_uara);
            새조각->roa_uara=조각->roa_uara-roa_uara-32;새조각->Panuku_tuemi=조각->Panuku_tuemi;새조각->사용=0;조각->Panuku_tuemi=새조각;조각->roa_uara=roa_uara;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void tuku_mamao(void *ADDRESS) {
    if(!ADDRESS)return;Pūmahara_aukati *조각=(void*)((char*)ADDRESS-32);
    volatile unsigned char *지움=ADDRESS;for(size_t 순번=0;순번<조각->roa_uara;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Panuku_tuemi;){if(!조각->사용&&!조각->Panuku_tuemi->사용){조각->roa_uara+=32+조각->Panuku_tuemi->roa_uara;조각->Panuku_tuemi=조각->Panuku_tuemi->Panuku_tuemi;}else 조각=조각->Panuku_tuemi;}
}
void *원격재할당(void *ADDRESS,size_t roa_uara){
    if(!ADDRESS)return tiritiri_mamao(roa_uara);if(!roa_uara){tuku_mamao(ADDRESS);return 0;}
    Pūmahara_aukati *조각=(void*)((char*)ADDRESS-32);void *새주소=tiritiri_mamao(roa_uara);
    if(새주소){memcpy(새주소,ADDRESS,roa_uara<조각->roa_uara?roa_uara:조각->roa_uara);tuku_mamao(ADDRESS);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_TEXT,int pūāhua_uara){for(;;Word_TEXT++){if(*Word_TEXT==(char)pūāhua_uara)return(char*)Word_TEXT;if(!*Word_TEXT)return 0;}}
char *strstr(const char *Word_TEXT,const char *찾음){size_t roa_uara=strlen(찾음);for(;*Word_TEXT;Word_TEXT++)if(!strncmp(Word_TEXT,찾음,roa_uara))return(char*)Word_TEXT;return roa_uara?0:(char*)Word_TEXT;}
char *strncpy(char *ūnga_uara,const char *원본,size_t roa_uara){size_t 순번=0;for(;순번<roa_uara&&원본[순번];순번++)ūnga_uara[순번]=원본[순번];for(;순번<roa_uara;순번++)ūnga_uara[순번]=0;return ūnga_uara;}
char *strncat(char *ūnga_uara,const char *원본,size_t roa_uara){char *끝=ūnga_uara+strlen(ūnga_uara);while(roa_uara--&&*원본)*끝++=*원본++;*끝=0;return ūnga_uara;}
int strncasecmp(const char *가,const char *나,size_t roa_uara){while(roa_uara--){unsigned 첫글자=*가++,SECOND_pūāhua=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_pūāhua>='A'&&SECOND_pūāhua<='Z')SECOND_pūāhua+=32;if(첫글자!=SECOND_pūāhua)return(int)첫글자-(int)SECOND_pūāhua;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_TEXT,const char *pūwehe_uara,char **Panuku_tuemi){if(!Word_TEXT)Word_TEXT=*Panuku_tuemi;while(*Word_TEXT&&strchr(pūwehe_uara,*Word_TEXT))Word_TEXT++;if(!*Word_TEXT){*Panuku_tuemi=Word_TEXT;return 0;}char *처음=Word_TEXT;while(*Word_TEXT&&!strchr(pūwehe_uara,*Word_TEXT))Word_TEXT++;if(*Word_TEXT)*Word_TEXT++=0;*Panuku_tuemi=Word_TEXT;return 처음;}
unsigned long strtoul(const char *Word_TEXT, char **끝, int BASE_uara) {
    const char *pūtake=Word_TEXT;unsigned long uara=0;int 음수=0,waipuke_uara=0;
    while(*Word_TEXT==' '||(*Word_TEXT>=9&&*Word_TEXT<=13))Word_TEXT++;
    if(*Word_TEXT=='-'||*Word_TEXT=='+')음수=*Word_TEXT++=='-';
    if((BASE_uara==0||BASE_uara==16)&&Word_TEXT[0]=='0'&&(Word_TEXT[1]=='x'||Word_TEXT[1]=='X')&&
       ((Word_TEXT[2]>='0'&&Word_TEXT[2]<='9')||(Word_TEXT[2]>='a'&&Word_TEXT[2]<='f')||(Word_TEXT[2]>='A'&&Word_TEXT[2]<='F'))) {BASE_uara=16;Word_TEXT+=2;}
    if(!BASE_uara)BASE_uara=*Word_TEXT=='0'?8:10;
    if(BASE_uara<2||BASE_uara>36){if(끝)*끝=(char*)pūtake;return 0;}
    const char *처음=Word_TEXT;
    for(;;Word_TEXT++) {
        unsigned pūāhua_uara=(unsigned char)*Word_TEXT;
        unsigned 수=pūāhua_uara>='0'&&pūāhua_uara<='9'?pūāhua_uara-'0':pūāhua_uara>='a'&&pūāhua_uara<='z'?pūāhua_uara-'a'+10:pūāhua_uara>='A'&&pūāhua_uara<='Z'?pūāhua_uara-'A'+10:36;
        if(수>=(unsigned)BASE_uara)break;
        if(uara>(~0ul-수)/(unsigned)BASE_uara)waipuke_uara=1;
        if(!waipuke_uara)uara=uara*(unsigned)BASE_uara+수;
    }
    if(끝)*끝=(char*)(Word_TEXT==처음?pūtake:Word_TEXT);
    return waipuke_uara?~0ul:음수?0ul-uara:uara;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int kākano_tūnga;
void mamao_whakarāpoto(const void *raraunga, size_t roa_uara, unsigned char mēhua[32]) {
    br_sha256_context Horopaki_uara;
    br_sha256_init(&Horopaki_uara); br_sha256_update(&Horopaki_uara, raraunga, roa_uara); br_sha256_out(&Horopaki_uara, mēhua);
    memset(&Horopaki_uara, 0, sizeof(Horopaki_uara));
}
#define 난수저장기(tūranga) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(tūranga)))
int 원격난수(unsigned char *ūnga_uara,unsigned roa_uara){
    if(!kākano_tūnga){volatile unsigned char *raraunga=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=raraunga[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=raraunga[8+순번];for(unsigned 순번=0;순번<40;순번++)raraunga[순번]=0;kākano_tūnga=2;}
        else {kākano_tūnga=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(kākano_tūnga==2){while(roa_uara){unsigned char Panuku_tuemi[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;mamao_whakarāpoto(입력,33,Panuku_tuemi);
        입력[32]=1;mamao_whakarāpoto(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=roa_uara<32?roa_uara:32;memcpy(ūnga_uara,Panuku_tuemi,수);memset(Panuku_tuemi,0,32);ūnga_uara+=수;roa_uara-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(roa_uara){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t uara=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&roa_uara;순번++,roa_uara--){*ūnga_uara++=uara&255;uara>>=8;}}
    return 0;
}
