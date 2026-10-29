/* kánẹ́ẹ̀lì_iye 전용 할당기와 ọ̀rọ̀_aṣínà_iye 난수 공급. aṣàmúlò ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ibi_ìpamọ́_sèdíwọ { size_t gígùn_iye; struct ibi_ìpamọ́_sèdíwọ *다음; int 사용; } ibi_ìpamọ́_sèdíwọ;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ibi_ìpamọ́_sèdíwọ *첫조각;
void *pín_Ìjìnnà(size_t gígùn_iye) {
    if (!gígùn_iye || gígùn_iye>sizeof(기억터)-64) return 0;
    gígùn_iye=(gígùn_iye+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->gígùn_iye=sizeof(기억터)-32;}
    for(ibi_ìpamọ́_sèdíwọ *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->gígùn_iye>=gígùn_iye){
        if(조각->gígùn_iye>=gígùn_iye+64){ibi_ìpamọ́_sèdíwọ *새조각=(void*)((char*)조각+32+gígùn_iye);
            새조각->gígùn_iye=조각->gígùn_iye-gígùn_iye-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->gígùn_iye=gígùn_iye;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void dápadà_Ìjìnnà(void *àdírẹ́ẹ̀sì) {
    if(!àdírẹ́ẹ̀sì)return;ibi_ìpamọ́_sèdíwọ *조각=(void*)((char*)àdírẹ́ẹ̀sì-32);
    volatile unsigned char *지움=àdírẹ́ẹ̀sì;for(size_t 순번=0;순번<조각->gígùn_iye;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->gígùn_iye+=32+조각->다음->gígùn_iye;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *àdírẹ́ẹ̀sì,size_t gígùn_iye){
    if(!àdírẹ́ẹ̀sì)return pín_Ìjìnnà(gígùn_iye);if(!gígùn_iye){dápadà_Ìjìnnà(àdírẹ́ẹ̀sì);return 0;}
    ibi_ìpamọ́_sèdíwọ *조각=(void*)((char*)àdírẹ́ẹ̀sì-32);void *새주소=pín_Ìjìnnà(gígùn_iye);
    if(새주소){memcpy(새주소,àdírẹ́ẹ̀sì,gígùn_iye<조각->gígùn_iye?gígùn_iye:조각->gígùn_iye);dápadà_Ìjìnnà(àdírẹ́ẹ̀sì);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Ọ̀rọ̀_SMS,int ẹyọ_ọ̀rọ̀_iye){for(;;Ọ̀rọ̀_SMS++){if(*Ọ̀rọ̀_SMS==(char)ẹyọ_ọ̀rọ̀_iye)return(char*)Ọ̀rọ̀_SMS;if(!*Ọ̀rọ̀_SMS)return 0;}}
char *strstr(const char *Ọ̀rọ̀_SMS,const char *찾음){size_t gígùn_iye=strlen(찾음);for(;*Ọ̀rọ̀_SMS;Ọ̀rọ̀_SMS++)if(!strncmp(Ọ̀rọ̀_SMS,찾음,gígùn_iye))return(char*)Ọ̀rọ̀_SMS;return gígùn_iye?0:(char*)Ọ̀rọ̀_SMS;}
char *strncpy(char *èbúté_iye,const char *원본,size_t gígùn_iye){size_t 순번=0;for(;순번<gígùn_iye&&원본[순번];순번++)èbúté_iye[순번]=원본[순번];for(;순번<gígùn_iye;순번++)èbúté_iye[순번]=0;return èbúté_iye;}
char *strncat(char *èbúté_iye,const char *원본,size_t gígùn_iye){char *끝=èbúté_iye+strlen(èbúté_iye);while(gígùn_iye--&&*원본)*끝++=*원본++;*끝=0;return èbúté_iye;}
int strncasecmp(const char *가,const char *나,size_t gígùn_iye){while(gígùn_iye--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Ọ̀rọ̀_SMS,const char *àmí_ìdá_iye,char **다음){if(!Ọ̀rọ̀_SMS)Ọ̀rọ̀_SMS=*다음;while(*Ọ̀rọ̀_SMS&&strchr(àmí_ìdá_iye,*Ọ̀rọ̀_SMS))Ọ̀rọ̀_SMS++;if(!*Ọ̀rọ̀_SMS){*다음=Ọ̀rọ̀_SMS;return 0;}char *처음=Ọ̀rọ̀_SMS;while(*Ọ̀rọ̀_SMS&&!strchr(àmí_ìdá_iye,*Ọ̀rọ̀_SMS))Ọ̀rọ̀_SMS++;if(*Ọ̀rọ̀_SMS)*Ọ̀rọ̀_SMS++=0;*다음=Ọ̀rọ̀_SMS;return 처음;}
unsigned long strtoul(const char *Ọ̀rọ̀_SMS, char **끝, int 밑) {
    const char *orísun=Ọ̀rọ̀_SMS;unsigned long iye=0;int 음수=0,rékọjá_iye=0;
    while(*Ọ̀rọ̀_SMS==' '||(*Ọ̀rọ̀_SMS>=9&&*Ọ̀rọ̀_SMS<=13))Ọ̀rọ̀_SMS++;
    if(*Ọ̀rọ̀_SMS=='-'||*Ọ̀rọ̀_SMS=='+')음수=*Ọ̀rọ̀_SMS++=='-';
    if((밑==0||밑==16)&&Ọ̀rọ̀_SMS[0]=='0'&&(Ọ̀rọ̀_SMS[1]=='x'||Ọ̀rọ̀_SMS[1]=='X')&&
       ((Ọ̀rọ̀_SMS[2]>='0'&&Ọ̀rọ̀_SMS[2]<='9')||(Ọ̀rọ̀_SMS[2]>='a'&&Ọ̀rọ̀_SMS[2]<='f')||(Ọ̀rọ̀_SMS[2]>='A'&&Ọ̀rọ̀_SMS[2]<='F'))) {밑=16;Ọ̀rọ̀_SMS+=2;}
    if(!밑)밑=*Ọ̀rọ̀_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)orísun;return 0;}
    const char *처음=Ọ̀rọ̀_SMS;
    for(;;Ọ̀rọ̀_SMS++) {
        unsigned ẹyọ_ọ̀rọ̀_iye=(unsigned char)*Ọ̀rọ̀_SMS;
        unsigned 수=ẹyọ_ọ̀rọ̀_iye>='0'&&ẹyọ_ọ̀rọ̀_iye<='9'?ẹyọ_ọ̀rọ̀_iye-'0':ẹyọ_ọ̀rọ̀_iye>='a'&&ẹyọ_ọ̀rọ̀_iye<='z'?ẹyọ_ọ̀rọ̀_iye-'a'+10:ẹyọ_ọ̀rọ̀_iye>='A'&&ẹyọ_ọ̀rọ̀_iye<='Z'?ẹyọ_ọ̀rọ̀_iye-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(iye>(~0ul-수)/(unsigned)밑)rékọjá_iye=1;
        if(!rékọjá_iye)iye=iye*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Ọ̀rọ̀_SMS==처음?orísun:Ọ̀rọ̀_SMS);
    return rékọjá_iye?~0ul:음수?0ul-iye:iye;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int iye_ìbẹ̀rẹ̀_ipò;
void Ìjìnnà_ìṣoníṣókí(const void *détà, size_t gígùn_iye, unsigned char 결과[32]) {
    br_sha256_context Ìṣètò_kíkà_iye;
    br_sha256_init(&Ìṣètò_kíkà_iye); br_sha256_update(&Ìṣètò_kíkà_iye, détà, gígùn_iye); br_sha256_out(&Ìṣètò_kíkà_iye, 결과);
    memset(&Ìṣètò_kíkà_iye, 0, sizeof(Ìṣètò_kíkà_iye));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *èbúté_iye,unsigned gígùn_iye){
    if(!iye_ìbẹ̀rẹ̀_ipò){volatile unsigned char *détà=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=détà[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=détà[8+순번];for(unsigned 순번=0;순번<40;순번++)détà[순번]=0;iye_ìbẹ̀rẹ̀_ipò=2;}
        else {iye_ìbẹ̀rẹ̀_ipò=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(iye_ìbẹ̀rẹ̀_ipò==2){while(gígùn_iye){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;Ìjìnnà_ìṣoníṣókí(입력,33,다음);
        입력[32]=1;Ìjìnnà_ìṣoníṣókí(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=gígùn_iye<32?gígùn_iye:32;memcpy(èbúté_iye,다음,수);memset(다음,0,32);èbúté_iye+=수;gígùn_iye-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(gígùn_iye){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t iye=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&gígùn_iye;순번++,gígùn_iye--){*èbúté_iye++=iye&255;iye>>=8;}}
    return 0;
}
