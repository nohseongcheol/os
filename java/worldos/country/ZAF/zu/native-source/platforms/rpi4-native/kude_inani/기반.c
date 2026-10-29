/* ikhenela_inani 전용 할당기와 iphasiwedi_inani 난수 공급. umsebenzisi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct inkumbulo_vimbela { size_t ubude_inani; struct inkumbulo_vimbela *다음; int 사용; } inkumbulo_vimbela;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static inkumbulo_vimbela *첫조각;
void *abela_kude(size_t ubude_inani) {
    if (!ubude_inani || ubude_inani>sizeof(기억터)-64) return 0;
    ubude_inani=(ubude_inani+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->ubude_inani=sizeof(기억터)-32;}
    for(inkumbulo_vimbela *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->ubude_inani>=ubude_inani){
        if(조각->ubude_inani>=ubude_inani+64){inkumbulo_vimbela *새조각=(void*)((char*)조각+32+ubude_inani);
            새조각->ubude_inani=조각->ubude_inani-ubude_inani-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->ubude_inani=ubude_inani;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void khulula_kude(void *ikheli) {
    if(!ikheli)return;inkumbulo_vimbela *조각=(void*)((char*)ikheli-32);
    volatile unsigned char *지움=ikheli;for(size_t 순번=0;순번<조각->ubude_inani;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->ubude_inani+=32+조각->다음->ubude_inani;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *ikheli,size_t ubude_inani){
    if(!ikheli)return abela_kude(ubude_inani);if(!ubude_inani){khulula_kude(ikheli);return 0;}
    inkumbulo_vimbela *조각=(void*)((char*)ikheli-32);void *새주소=abela_kude(ubude_inani);
    if(새주소){memcpy(새주소,ikheli,ubude_inani<조각->ubude_inani?ubude_inani:조각->ubude_inani);khulula_kude(ikheli);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Amagama_I_SMS,int uhlamvusimo_inani){for(;;Amagama_I_SMS++){if(*Amagama_I_SMS==(char)uhlamvusimo_inani)return(char*)Amagama_I_SMS;if(!*Amagama_I_SMS)return 0;}}
char *strstr(const char *Amagama_I_SMS,const char *찾음){size_t ubude_inani=strlen(찾음);for(;*Amagama_I_SMS;Amagama_I_SMS++)if(!strncmp(Amagama_I_SMS,찾음,ubude_inani))return(char*)Amagama_I_SMS;return ubude_inani?0:(char*)Amagama_I_SMS;}
char *strncpy(char *isikhumulo_inani,const char *원본,size_t ubude_inani){size_t 순번=0;for(;순번<ubude_inani&&원본[순번];순번++)isikhumulo_inani[순번]=원본[순번];for(;순번<ubude_inani;순번++)isikhumulo_inani[순번]=0;return isikhumulo_inani;}
char *strncat(char *isikhumulo_inani,const char *원본,size_t ubude_inani){char *끝=isikhumulo_inani+strlen(isikhumulo_inani);while(ubude_inani--&&*원본)*끝++=*원본++;*끝=0;return isikhumulo_inani;}
int strncasecmp(const char *가,const char *나,size_t ubude_inani){while(ubude_inani--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Amagama_I_SMS,const char *okunqandayo_inani,char **다음){if(!Amagama_I_SMS)Amagama_I_SMS=*다음;while(*Amagama_I_SMS&&strchr(okunqandayo_inani,*Amagama_I_SMS))Amagama_I_SMS++;if(!*Amagama_I_SMS){*다음=Amagama_I_SMS;return 0;}char *처음=Amagama_I_SMS;while(*Amagama_I_SMS&&!strchr(okunqandayo_inani,*Amagama_I_SMS))Amagama_I_SMS++;if(*Amagama_I_SMS)*Amagama_I_SMS++=0;*다음=Amagama_I_SMS;return 처음;}
unsigned long strtoul(const char *Amagama_I_SMS, char **끝, int 밑) {
    const char *umthombo=Amagama_I_SMS;unsigned long inani=0;int 음수=0,ukukapaka_inani=0;
    while(*Amagama_I_SMS==' '||(*Amagama_I_SMS>=9&&*Amagama_I_SMS<=13))Amagama_I_SMS++;
    if(*Amagama_I_SMS=='-'||*Amagama_I_SMS=='+')음수=*Amagama_I_SMS++=='-';
    if((밑==0||밑==16)&&Amagama_I_SMS[0]=='0'&&(Amagama_I_SMS[1]=='x'||Amagama_I_SMS[1]=='X')&&
       ((Amagama_I_SMS[2]>='0'&&Amagama_I_SMS[2]<='9')||(Amagama_I_SMS[2]>='a'&&Amagama_I_SMS[2]<='f')||(Amagama_I_SMS[2]>='A'&&Amagama_I_SMS[2]<='F'))) {밑=16;Amagama_I_SMS+=2;}
    if(!밑)밑=*Amagama_I_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)umthombo;return 0;}
    const char *처음=Amagama_I_SMS;
    for(;;Amagama_I_SMS++) {
        unsigned uhlamvusimo_inani=(unsigned char)*Amagama_I_SMS;
        unsigned 수=uhlamvusimo_inani>='0'&&uhlamvusimo_inani<='9'?uhlamvusimo_inani-'0':uhlamvusimo_inani>='a'&&uhlamvusimo_inani<='z'?uhlamvusimo_inani-'a'+10:uhlamvusimo_inani>='A'&&uhlamvusimo_inani<='Z'?uhlamvusimo_inani-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(inani>(~0ul-수)/(unsigned)밑)ukukapaka_inani=1;
        if(!ukukapaka_inani)inani=inani*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Amagama_I_SMS==처음?umthombo:Amagama_I_SMS);
    return ukukapaka_inani?~0ul:음수?0ul-inani:inani;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int isidi_isimo;
void kude_isifinyezo(const void *imininingwane, size_t ubude_inani, unsigned char 결과[32]) {
    br_sha256_context Umongo_inani;
    br_sha256_init(&Umongo_inani); br_sha256_update(&Umongo_inani, imininingwane, ubude_inani); br_sha256_out(&Umongo_inani, 결과);
    memset(&Umongo_inani, 0, sizeof(Umongo_inani));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *isikhumulo_inani,unsigned ubude_inani){
    if(!isidi_isimo){volatile unsigned char *imininingwane=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=imininingwane[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=imininingwane[8+순번];for(unsigned 순번=0;순번<40;순번++)imininingwane[순번]=0;isidi_isimo=2;}
        else {isidi_isimo=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(isidi_isimo==2){while(ubude_inani){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;kude_isifinyezo(입력,33,다음);
        입력[32]=1;kude_isifinyezo(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=ubude_inani<32?ubude_inani:32;memcpy(isikhumulo_inani,다음,수);memset(다음,0,32);isikhumulo_inani+=수;ubude_inani-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(ubude_inani){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t inani=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&ubude_inani;순번++,ubude_inani--){*isikhumulo_inani++=inani&255;inani>>=8;}}
    return 0;
}
