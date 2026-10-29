/* Kwara_Daraja 전용 할당기와 kalmar_sirri_Daraja 난수 공급. Mai_anfani_da_kwamfuta ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Mahardatar_kwamfuta_bulo { size_t Tsawo_Daraja; struct Mahardatar_kwamfuta_bulo *다음; int 사용; } Mahardatar_kwamfuta_bulo;
static unsigned char Mahardatar_kwamfuta_Fage[2*1024*1024] __attribute__((aligned(16)));
static Mahardatar_kwamfuta_bulo *첫조각;
void *kasafta_na_nesa(size_t Tsawo_Daraja) {
    if (!Tsawo_Daraja || Tsawo_Daraja>sizeof(Mahardatar_kwamfuta_Fage)-64) return 0;
    Tsawo_Daraja=(Tsawo_Daraja+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Mahardatar_kwamfuta_Fage;첫조각->Tsawo_Daraja=sizeof(Mahardatar_kwamfuta_Fage)-32;}
    for(Mahardatar_kwamfuta_bulo *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->Tsawo_Daraja>=Tsawo_Daraja){
        if(조각->Tsawo_Daraja>=Tsawo_Daraja+64){Mahardatar_kwamfuta_bulo *새조각=(void*)((char*)조각+32+Tsawo_Daraja);
            새조각->Tsawo_Daraja=조각->Tsawo_Daraja-Tsawo_Daraja-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->Tsawo_Daraja=Tsawo_Daraja;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void saka_na_nesa(void *imel) {
    if(!imel)return;Mahardatar_kwamfuta_bulo *조각=(void*)((char*)imel-32);
    volatile unsigned char *지움=imel;for(size_t 순번=0;순번<조각->Tsawo_Daraja;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->Tsawo_Daraja+=32+조각->다음->Tsawo_Daraja;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *imel,size_t Tsawo_Daraja){
    if(!imel)return kasafta_na_nesa(Tsawo_Daraja);if(!Tsawo_Daraja){saka_na_nesa(imel);return 0;}
    Mahardatar_kwamfuta_bulo *조각=(void*)((char*)imel-32);void *새주소=kasafta_na_nesa(Tsawo_Daraja);
    if(새주소){memcpy(새주소,imel,Tsawo_Daraja<조각->Tsawo_Daraja?Tsawo_Daraja:조각->Tsawo_Daraja);saka_na_nesa(imel);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Microsoft_Word_SMS,int Harafi_Daraja){for(;;Microsoft_Word_SMS++){if(*Microsoft_Word_SMS==(char)Harafi_Daraja)return(char*)Microsoft_Word_SMS;if(!*Microsoft_Word_SMS)return 0;}}
char *strstr(const char *Microsoft_Word_SMS,const char *찾음){size_t Tsawo_Daraja=strlen(찾음);for(;*Microsoft_Word_SMS;Microsoft_Word_SMS++)if(!strncmp(Microsoft_Word_SMS,찾음,Tsawo_Daraja))return(char*)Microsoft_Word_SMS;return Tsawo_Daraja?0:(char*)Microsoft_Word_SMS;}
char *strncpy(char *Zangon_ƙarshe_Daraja,const char *원본,size_t Tsawo_Daraja){size_t 순번=0;for(;순번<Tsawo_Daraja&&원본[순번];순번++)Zangon_ƙarshe_Daraja[순번]=원본[순번];for(;순번<Tsawo_Daraja;순번++)Zangon_ƙarshe_Daraja[순번]=0;return Zangon_ƙarshe_Daraja;}
char *strncat(char *Zangon_ƙarshe_Daraja,const char *원본,size_t Tsawo_Daraja){char *끝=Zangon_ƙarshe_Daraja+strlen(Zangon_ƙarshe_Daraja);while(Tsawo_Daraja--&&*원본)*끝++=*원본++;*끝=0;return Zangon_ƙarshe_Daraja;}
int strncasecmp(const char *가,const char *나,size_t Tsawo_Daraja){while(Tsawo_Daraja--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Microsoft_Word_SMS,const char *Haruffan_rabawa_Daraja,char **다음){if(!Microsoft_Word_SMS)Microsoft_Word_SMS=*다음;while(*Microsoft_Word_SMS&&strchr(Haruffan_rabawa_Daraja,*Microsoft_Word_SMS))Microsoft_Word_SMS++;if(!*Microsoft_Word_SMS){*다음=Microsoft_Word_SMS;return 0;}char *처음=Microsoft_Word_SMS;while(*Microsoft_Word_SMS&&!strchr(Haruffan_rabawa_Daraja,*Microsoft_Word_SMS))Microsoft_Word_SMS++;if(*Microsoft_Word_SMS)*Microsoft_Word_SMS++=0;*다음=Microsoft_Word_SMS;return 처음;}
unsigned long strtoul(const char *Microsoft_Word_SMS, char **끝, int 밑) {
    const char *tushe=Microsoft_Word_SMS;unsigned long Daraja=0;int 음수=0,Mamayar_bayanai_Daraja=0;
    while(*Microsoft_Word_SMS==' '||(*Microsoft_Word_SMS>=9&&*Microsoft_Word_SMS<=13))Microsoft_Word_SMS++;
    if(*Microsoft_Word_SMS=='-'||*Microsoft_Word_SMS=='+')음수=*Microsoft_Word_SMS++=='-';
    if((밑==0||밑==16)&&Microsoft_Word_SMS[0]=='0'&&(Microsoft_Word_SMS[1]=='x'||Microsoft_Word_SMS[1]=='X')&&
       ((Microsoft_Word_SMS[2]>='0'&&Microsoft_Word_SMS[2]<='9')||(Microsoft_Word_SMS[2]>='a'&&Microsoft_Word_SMS[2]<='f')||(Microsoft_Word_SMS[2]>='A'&&Microsoft_Word_SMS[2]<='F'))) {밑=16;Microsoft_Word_SMS+=2;}
    if(!밑)밑=*Microsoft_Word_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)tushe;return 0;}
    const char *처음=Microsoft_Word_SMS;
    for(;;Microsoft_Word_SMS++) {
        unsigned Harafi_Daraja=(unsigned char)*Microsoft_Word_SMS;
        unsigned 수=Harafi_Daraja>='0'&&Harafi_Daraja<='9'?Harafi_Daraja-'0':Harafi_Daraja>='a'&&Harafi_Daraja<='z'?Harafi_Daraja-'a'+10:Harafi_Daraja>='A'&&Harafi_Daraja<='Z'?Harafi_Daraja-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(Daraja>(~0ul-수)/(unsigned)밑)Mamayar_bayanai_Daraja=1;
        if(!Mamayar_bayanai_Daraja)Daraja=Daraja*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Microsoft_Word_SMS==처음?tushe:Microsoft_Word_SMS);
    return Mamayar_bayanai_Daraja?~0ul:음수?0ul-Daraja:Daraja;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int iri_Matsayi;
void na_nesa_taƙaitawa(const void *Tarin_bayani, size_t Tsawo_Daraja, unsigned char 결과[32]) {
    br_sha256_context Kwaryar_rubutu_Daraja;
    br_sha256_init(&Kwaryar_rubutu_Daraja); br_sha256_update(&Kwaryar_rubutu_Daraja, Tarin_bayani, Tsawo_Daraja); br_sha256_out(&Kwaryar_rubutu_Daraja, 결과);
    memset(&Kwaryar_rubutu_Daraja, 0, sizeof(Kwaryar_rubutu_Daraja));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *Zangon_ƙarshe_Daraja,unsigned Tsawo_Daraja){
    if(!iri_Matsayi){volatile unsigned char *Tarin_bayani=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=Tarin_bayani[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=Tarin_bayani[8+순번];for(unsigned 순번=0;순번<40;순번++)Tarin_bayani[순번]=0;iri_Matsayi=2;}
        else {iri_Matsayi=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(iri_Matsayi==2){while(Tsawo_Daraja){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;na_nesa_taƙaitawa(입력,33,다음);
        입력[32]=1;na_nesa_taƙaitawa(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=Tsawo_Daraja<32?Tsawo_Daraja:32;memcpy(Zangon_ƙarshe_Daraja,다음,수);memset(다음,0,32);Zangon_ƙarshe_Daraja+=수;Tsawo_Daraja-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(Tsawo_Daraja){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t Daraja=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&Tsawo_Daraja;순번++,Tsawo_Daraja--){*Zangon_ƙarshe_Daraja++=Daraja&255;Daraja>>=8;}}
    return 0;
}
