/* Kernel_VALUE 전용 할당기와 Passwuert_VALUE 난수 공급. Benotzer ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Späicher_blockéieren { size_t Längt_VALUE; struct Späicher_blockéieren *Weider_Element; int 사용; } Späicher_blockéieren;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static Späicher_blockéieren *첫조각;
void *zouweisen_extern(size_t Längt_VALUE) {
    if (!Längt_VALUE || Längt_VALUE>sizeof(기억터)-64) return 0;
    Längt_VALUE=(Längt_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->Längt_VALUE=sizeof(기억터)-32;}
    for(Späicher_blockéieren *조각=첫조각;조각;조각=조각->Weider_Element)if(!조각->사용&&조각->Längt_VALUE>=Längt_VALUE){
        if(조각->Längt_VALUE>=Längt_VALUE+64){Späicher_blockéieren *새조각=(void*)((char*)조각+32+Längt_VALUE);
            새조각->Längt_VALUE=조각->Längt_VALUE-Längt_VALUE-32;새조각->Weider_Element=조각->Weider_Element;새조각->사용=0;조각->Weider_Element=새조각;조각->Längt_VALUE=Längt_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void Versioun_extern(void *Adress) {
    if(!Adress)return;Späicher_blockéieren *조각=(void*)((char*)Adress-32);
    volatile unsigned char *지움=Adress;for(size_t 순번=0;순번<조각->Längt_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Weider_Element;){if(!조각->사용&&!조각->Weider_Element->사용){조각->Längt_VALUE+=32+조각->Weider_Element->Längt_VALUE;조각->Weider_Element=조각->Weider_Element->Weider_Element;}else 조각=조각->Weider_Element;}
}
void *원격재할당(void *Adress,size_t Längt_VALUE){
    if(!Adress)return zouweisen_extern(Längt_VALUE);if(!Längt_VALUE){Versioun_extern(Adress);return 0;}
    Späicher_blockéieren *조각=(void*)((char*)Adress-32);void *새주소=zouweisen_extern(Längt_VALUE);
    if(새주소){memcpy(새주소,Adress,Längt_VALUE<조각->Längt_VALUE?Längt_VALUE:조각->Längt_VALUE);Versioun_extern(Adress);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int Zeechen_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)Zeechen_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t Längt_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,Längt_VALUE))return(char*)Word_SMS;return Längt_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *Zil_VALUE,const char *원본,size_t Längt_VALUE){size_t 순번=0;for(;순번<Längt_VALUE&&원본[순번];순번++)Zil_VALUE[순번]=원본[순번];for(;순번<Längt_VALUE;순번++)Zil_VALUE[순번]=0;return Zil_VALUE;}
char *strncat(char *Zil_VALUE,const char *원본,size_t Längt_VALUE){char *끝=Zil_VALUE+strlen(Zil_VALUE);while(Längt_VALUE--&&*원본)*끝++=*원본++;*끝=0;return Zil_VALUE;}
int strncasecmp(const char *가,const char *나,size_t Längt_VALUE){while(Längt_VALUE--){unsigned 첫글자=*가++,SECOND_Zeechen=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_Zeechen>='A'&&SECOND_Zeechen<='Z')SECOND_Zeechen+=32;if(첫글자!=SECOND_Zeechen)return(int)첫글자-(int)SECOND_Zeechen;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *Trennzeechen_VALUE_d8ba4873,char **Weider_Element){if(!Word_SMS)Word_SMS=*Weider_Element;while(*Word_SMS&&strchr(Trennzeechen_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Weider_Element=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(Trennzeechen_VALUE_d8ba4873,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Weider_Element=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *Quell=Word_SMS;unsigned long VALUE=0;int 음수=0,Iwwerlaf_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)Quell;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned Zeechen_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=Zeechen_VALUE>='0'&&Zeechen_VALUE<='9'?Zeechen_VALUE-'0':Zeechen_VALUE>='a'&&Zeechen_VALUE<='z'?Zeechen_VALUE-'a'+10:Zeechen_VALUE>='A'&&Zeechen_VALUE<='Z'?Zeechen_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)Iwwerlaf_VALUE=1;
        if(!Iwwerlaf_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?Quell:Word_SMS);
    return Iwwerlaf_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int Startwäert_Status;
void extern_Zesummefaassung(const void *Daten, size_t Längt_VALUE, unsigned char Mooss[32]) {
    br_sha256_context Kontext_VALUE;
    br_sha256_init(&Kontext_VALUE); br_sha256_update(&Kontext_VALUE, Daten, Längt_VALUE); br_sha256_out(&Kontext_VALUE, Mooss);
    memset(&Kontext_VALUE, 0, sizeof(Kontext_VALUE));
}
#define 난수저장기(positionéieren) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(positionéieren)))
int 원격난수(unsigned char *Zil_VALUE,unsigned Längt_VALUE){
    if(!Startwäert_Status){volatile unsigned char *Daten=(void*)0x01ff0000ul;const char *Markéierung_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=Daten[순번]^(unsigned char)Markéierung_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=Daten[8+순번];for(unsigned 순번=0;순번<40;순번++)Daten[순번]=0;Startwäert_Status=2;}
        else {Startwäert_Status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(Startwäert_Status==2){while(Längt_VALUE){unsigned char Weider_Element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;extern_Zesummefaassung(입력,33,Weider_Element);
        입력[32]=1;extern_Zesummefaassung(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=Längt_VALUE<32?Längt_VALUE:32;memcpy(Zil_VALUE,Weider_Element,수);memset(Weider_Element,0,32);Zil_VALUE+=수;Längt_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(Längt_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&Längt_VALUE;순번++,Längt_VALUE--){*Zil_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
