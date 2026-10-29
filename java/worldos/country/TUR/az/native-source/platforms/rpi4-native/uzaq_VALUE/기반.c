/* nüvə_VALUE 전용 할당기와 parol_VALUE 난수 공급. istifadəçi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Yaddaş_blokla { size_t uzunluq_VALUE; struct Yaddaş_blokla *Sonrakı_element; int 사용; } Yaddaş_blokla;
static unsigned char Yaddaş_Arena[2*1024*1024] __attribute__((aligned(16)));
static Yaddaş_blokla *첫조각;
void *ayırmaq_uzaq(size_t uzunluq_VALUE) {
    if (!uzunluq_VALUE || uzunluq_VALUE>sizeof(Yaddaş_Arena)-64) return 0;
    uzunluq_VALUE=(uzunluq_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Yaddaş_Arena;첫조각->uzunluq_VALUE=sizeof(Yaddaş_Arena)-32;}
    for(Yaddaş_blokla *조각=첫조각;조각;조각=조각->Sonrakı_element)if(!조각->사용&&조각->uzunluq_VALUE>=uzunluq_VALUE){
        if(조각->uzunluq_VALUE>=uzunluq_VALUE+64){Yaddaş_blokla *새조각=(void*)((char*)조각+32+uzunluq_VALUE);
            새조각->uzunluq_VALUE=조각->uzunluq_VALUE-uzunluq_VALUE-32;새조각->Sonrakı_element=조각->Sonrakı_element;새조각->사용=0;조각->Sonrakı_element=새조각;조각->uzunluq_VALUE=uzunluq_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void burax_uzaq(void *ünvan) {
    if(!ünvan)return;Yaddaş_blokla *조각=(void*)((char*)ünvan-32);
    volatile unsigned char *지움=ünvan;for(size_t 순번=0;순번<조각->uzunluq_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Sonrakı_element;){if(!조각->사용&&!조각->Sonrakı_element->사용){조각->uzunluq_VALUE+=32+조각->Sonrakı_element->uzunluq_VALUE;조각->Sonrakı_element=조각->Sonrakı_element->Sonrakı_element;}else 조각=조각->Sonrakı_element;}
}
void *원격재할당(void *ünvan,size_t uzunluq_VALUE){
    if(!ünvan)return ayırmaq_uzaq(uzunluq_VALUE);if(!uzunluq_VALUE){burax_uzaq(ünvan);return 0;}
    Yaddaş_blokla *조각=(void*)((char*)ünvan-32);void *새주소=ayırmaq_uzaq(uzunluq_VALUE);
    if(새주소){memcpy(새주소,ünvan,uzunluq_VALUE<조각->uzunluq_VALUE?uzunluq_VALUE:조각->uzunluq_VALUE);burax_uzaq(ünvan);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Söz_SMS,int simvol_VALUE_068c2631){for(;;Söz_SMS++){if(*Söz_SMS==(char)simvol_VALUE_068c2631)return(char*)Söz_SMS;if(!*Söz_SMS)return 0;}}
char *strstr(const char *Söz_SMS,const char *찾음){size_t uzunluq_VALUE=strlen(찾음);for(;*Söz_SMS;Söz_SMS++)if(!strncmp(Söz_SMS,찾음,uzunluq_VALUE))return(char*)Söz_SMS;return uzunluq_VALUE?0:(char*)Söz_SMS;}
char *strncpy(char *təyinat_VALUE_a0fbc067,const char *원본,size_t uzunluq_VALUE){size_t 순번=0;for(;순번<uzunluq_VALUE&&원본[순번];순번++)təyinat_VALUE_a0fbc067[순번]=원본[순번];for(;순번<uzunluq_VALUE;순번++)təyinat_VALUE_a0fbc067[순번]=0;return təyinat_VALUE_a0fbc067;}
char *strncat(char *təyinat_VALUE_a0fbc067,const char *원본,size_t uzunluq_VALUE){char *끝=təyinat_VALUE_a0fbc067+strlen(təyinat_VALUE_a0fbc067);while(uzunluq_VALUE--&&*원본)*끝++=*원본++;*끝=0;return təyinat_VALUE_a0fbc067;}
int strncasecmp(const char *가,const char *나,size_t uzunluq_VALUE){while(uzunluq_VALUE--){unsigned 첫글자=*가++,SECOND_simvol=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_simvol>='A'&&SECOND_simvol<='Z')SECOND_simvol+=32;if(첫글자!=SECOND_simvol)return(int)첫글자-(int)SECOND_simvol;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Söz_SMS,const char *ayırıcı_VALUE_d8ba4873,char **Sonrakı_element){if(!Söz_SMS)Söz_SMS=*Sonrakı_element;while(*Söz_SMS&&strchr(ayırıcı_VALUE_d8ba4873,*Söz_SMS))Söz_SMS++;if(!*Söz_SMS){*Sonrakı_element=Söz_SMS;return 0;}char *처음=Söz_SMS;while(*Söz_SMS&&!strchr(ayırıcı_VALUE_d8ba4873,*Söz_SMS))Söz_SMS++;if(*Söz_SMS)*Söz_SMS++=0;*Sonrakı_element=Söz_SMS;return 처음;}
unsigned long strtoul(const char *Söz_SMS, char **끝, int BASE_VALUE) {
    const char *QAYNAQ=Söz_SMS;unsigned long VALUE=0;int 음수=0,dolub_daşma_VALUE=0;
    while(*Söz_SMS==' '||(*Söz_SMS>=9&&*Söz_SMS<=13))Söz_SMS++;
    if(*Söz_SMS=='-'||*Söz_SMS=='+')음수=*Söz_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Söz_SMS[0]=='0'&&(Söz_SMS[1]=='x'||Söz_SMS[1]=='X')&&
       ((Söz_SMS[2]>='0'&&Söz_SMS[2]<='9')||(Söz_SMS[2]>='a'&&Söz_SMS[2]<='f')||(Söz_SMS[2]>='A'&&Söz_SMS[2]<='F'))) {BASE_VALUE=16;Söz_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Söz_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)QAYNAQ;return 0;}
    const char *처음=Söz_SMS;
    for(;;Söz_SMS++) {
        unsigned simvol_VALUE_068c2631=(unsigned char)*Söz_SMS;
        unsigned 수=simvol_VALUE_068c2631>='0'&&simvol_VALUE_068c2631<='9'?simvol_VALUE_068c2631-'0':simvol_VALUE_068c2631>='a'&&simvol_VALUE_068c2631<='z'?simvol_VALUE_068c2631-'a'+10:simvol_VALUE_068c2631>='A'&&simvol_VALUE_068c2631<='Z'?simvol_VALUE_068c2631-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)dolub_daşma_VALUE=1;
        if(!dolub_daşma_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Söz_SMS==처음?QAYNAQ:Söz_SMS);
    return dolub_daşma_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int mənbə_vəziyyət;
void uzaq_xülasə(const void *verilənlər, size_t uzunluq_VALUE, unsigned char ölçü[32]) {
    br_sha256_context kontekst_VALUE;
    br_sha256_init(&kontekst_VALUE); br_sha256_update(&kontekst_VALUE, verilənlər, uzunluq_VALUE); br_sha256_out(&kontekst_VALUE, ölçü);
    memset(&kontekst_VALUE, 0, sizeof(kontekst_VALUE));
}
#define 난수저장기(yerinə_qoymaq) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(yerinə_qoymaq)))
int 원격난수(unsigned char *təyinat_VALUE_a0fbc067,unsigned uzunluq_VALUE){
    if(!mənbə_vəziyyət){volatile unsigned char *verilənlər=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=verilənlər[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=verilənlər[8+순번];for(unsigned 순번=0;순번<40;순번++)verilənlər[순번]=0;mənbə_vəziyyət=2;}
        else {mənbə_vəziyyət=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(mənbə_vəziyyət==2){while(uzunluq_VALUE){unsigned char Sonrakı_element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;uzaq_xülasə(입력,33,Sonrakı_element);
        입력[32]=1;uzaq_xülasə(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=uzunluq_VALUE<32?uzunluq_VALUE:32;memcpy(təyinat_VALUE_a0fbc067,Sonrakı_element,수);memset(Sonrakı_element,0,32);təyinat_VALUE_a0fbc067+=수;uzunluq_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(uzunluq_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&uzunluq_VALUE;순번++,uzunluq_VALUE--){*təyinat_VALUE_a0fbc067++=VALUE&255;VALUE>>=8;}}
    return 0;
}
