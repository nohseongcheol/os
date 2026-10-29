/* ýadro_baha 전용 할당기와 parol_baha 난수 공급. ulanyjy ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ýat_bökde { size_t dowamlylyk_baha; struct ýat_bökde *다음; int 사용; } ýat_bökde;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ýat_bökde *첫조각;
void *bölüp_aýyr_uzakdan(size_t dowamlylyk_baha) {
    if (!dowamlylyk_baha || dowamlylyk_baha>sizeof(기억터)-64) return 0;
    dowamlylyk_baha=(dowamlylyk_baha+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->dowamlylyk_baha=sizeof(기억터)-32;}
    for(ýat_bökde *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->dowamlylyk_baha>=dowamlylyk_baha){
        if(조각->dowamlylyk_baha>=dowamlylyk_baha+64){ýat_bökde *새조각=(void*)((char*)조각+32+dowamlylyk_baha);
            새조각->dowamlylyk_baha=조각->dowamlylyk_baha-dowamlylyk_baha-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->dowamlylyk_baha=dowamlylyk_baha;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void goýbermek_uzakdan(void *salgy) {
    if(!salgy)return;ýat_bökde *조각=(void*)((char*)salgy-32);
    volatile unsigned char *지움=salgy;for(size_t 순번=0;순번<조각->dowamlylyk_baha;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->dowamlylyk_baha+=32+조각->다음->dowamlylyk_baha;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *salgy,size_t dowamlylyk_baha){
    if(!salgy)return bölüp_aýyr_uzakdan(dowamlylyk_baha);if(!dowamlylyk_baha){goýbermek_uzakdan(salgy);return 0;}
    ýat_bökde *조각=(void*)((char*)salgy-32);void *새주소=bölüp_aýyr_uzakdan(dowamlylyk_baha);
    if(새주소){memcpy(새주소,salgy,dowamlylyk_baha<조각->dowamlylyk_baha?dowamlylyk_baha:조각->dowamlylyk_baha);goýbermek_uzakdan(salgy);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Söz_SMS,int nyşan_baha_068c2631){for(;;Söz_SMS++){if(*Söz_SMS==(char)nyşan_baha_068c2631)return(char*)Söz_SMS;if(!*Söz_SMS)return 0;}}
char *strstr(const char *Söz_SMS,const char *찾음){size_t dowamlylyk_baha=strlen(찾음);for(;*Söz_SMS;Söz_SMS++)if(!strncmp(Söz_SMS,찾음,dowamlylyk_baha))return(char*)Söz_SMS;return dowamlylyk_baha?0:(char*)Söz_SMS;}
char *strncpy(char *barylmaly_ýer_baha,const char *원본,size_t dowamlylyk_baha){size_t 순번=0;for(;순번<dowamlylyk_baha&&원본[순번];순번++)barylmaly_ýer_baha[순번]=원본[순번];for(;순번<dowamlylyk_baha;순번++)barylmaly_ýer_baha[순번]=0;return barylmaly_ýer_baha;}
char *strncat(char *barylmaly_ýer_baha,const char *원본,size_t dowamlylyk_baha){char *끝=barylmaly_ýer_baha+strlen(barylmaly_ýer_baha);while(dowamlylyk_baha--&&*원본)*끝++=*원본++;*끝=0;return barylmaly_ýer_baha;}
int strncasecmp(const char *가,const char *나,size_t dowamlylyk_baha){while(dowamlylyk_baha--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Söz_SMS,const char *bölüji_baha_d8ba4873,char **다음){if(!Söz_SMS)Söz_SMS=*다음;while(*Söz_SMS&&strchr(bölüji_baha_d8ba4873,*Söz_SMS))Söz_SMS++;if(!*Söz_SMS){*다음=Söz_SMS;return 0;}char *처음=Söz_SMS;while(*Söz_SMS&&!strchr(bölüji_baha_d8ba4873,*Söz_SMS))Söz_SMS++;if(*Söz_SMS)*Söz_SMS++=0;*다음=Söz_SMS;return 처음;}
unsigned long strtoul(const char *Söz_SMS, char **끝, int 밑) {
    const char *Çeşme=Söz_SMS;unsigned long baha=0;int 음수=0,gyrmalanma_baha=0;
    while(*Söz_SMS==' '||(*Söz_SMS>=9&&*Söz_SMS<=13))Söz_SMS++;
    if(*Söz_SMS=='-'||*Söz_SMS=='+')음수=*Söz_SMS++=='-';
    if((밑==0||밑==16)&&Söz_SMS[0]=='0'&&(Söz_SMS[1]=='x'||Söz_SMS[1]=='X')&&
       ((Söz_SMS[2]>='0'&&Söz_SMS[2]<='9')||(Söz_SMS[2]>='a'&&Söz_SMS[2]<='f')||(Söz_SMS[2]>='A'&&Söz_SMS[2]<='F'))) {밑=16;Söz_SMS+=2;}
    if(!밑)밑=*Söz_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)Çeşme;return 0;}
    const char *처음=Söz_SMS;
    for(;;Söz_SMS++) {
        unsigned nyşan_baha_068c2631=(unsigned char)*Söz_SMS;
        unsigned 수=nyşan_baha_068c2631>='0'&&nyşan_baha_068c2631<='9'?nyşan_baha_068c2631-'0':nyşan_baha_068c2631>='a'&&nyşan_baha_068c2631<='z'?nyşan_baha_068c2631-'a'+10:nyşan_baha_068c2631>='A'&&nyşan_baha_068c2631<='Z'?nyşan_baha_068c2631-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(baha>(~0ul-수)/(unsigned)밑)gyrmalanma_baha=1;
        if(!gyrmalanma_baha)baha=baha*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Söz_SMS==처음?Çeşme:Söz_SMS);
    return gyrmalanma_baha?~0ul:음수?0ul-baha:baha;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int deslapky_baha_ýagdaý;
void uzakdan_gysgaça_mazmun(const void *maglumat, size_t dowamlylyk_baha, unsigned char 결과[32]) {
    br_sha256_context Kontekst_baha;
    br_sha256_init(&Kontekst_baha); br_sha256_update(&Kontekst_baha, maglumat, dowamlylyk_baha); br_sha256_out(&Kontekst_baha, 결과);
    memset(&Kontekst_baha, 0, sizeof(Kontekst_baha));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *barylmaly_ýer_baha,unsigned dowamlylyk_baha){
    if(!deslapky_baha_ýagdaý){volatile unsigned char *maglumat=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=maglumat[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=maglumat[8+순번];for(unsigned 순번=0;순번<40;순번++)maglumat[순번]=0;deslapky_baha_ýagdaý=2;}
        else {deslapky_baha_ýagdaý=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(deslapky_baha_ýagdaý==2){while(dowamlylyk_baha){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;uzakdan_gysgaça_mazmun(입력,33,다음);
        입력[32]=1;uzakdan_gysgaça_mazmun(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=dowamlylyk_baha<32?dowamlylyk_baha:32;memcpy(barylmaly_ýer_baha,다음,수);memset(다음,0,32);barylmaly_ýer_baha+=수;dowamlylyk_baha-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(dowamlylyk_baha){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t baha=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&dowamlylyk_baha;순번++,dowamlylyk_baha--){*barylmaly_ýer_baha++=baha&255;baha>>=8;}}
    return 0;
}
