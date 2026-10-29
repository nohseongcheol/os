/* nukleo_balio 전용 할당기와 pasahitz_balio 난수 공급. erabiltzaile ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memoria_blokeatu { size_t luzera_balio; struct Memoria_blokeatu *Hurrengoa_elementu; int 사용; } Memoria_blokeatu;
static unsigned char Memoria_Borroka_lekua[2*1024*1024] __attribute__((aligned(16)));
static Memoria_blokeatu *첫조각;
void *esleitu_urruneko(size_t luzera_balio) {
    if (!luzera_balio || luzera_balio>sizeof(Memoria_Borroka_lekua)-64) return 0;
    luzera_balio=(luzera_balio+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memoria_Borroka_lekua;첫조각->luzera_balio=sizeof(Memoria_Borroka_lekua)-32;}
    for(Memoria_blokeatu *조각=첫조각;조각;조각=조각->Hurrengoa_elementu)if(!조각->사용&&조각->luzera_balio>=luzera_balio){
        if(조각->luzera_balio>=luzera_balio+64){Memoria_blokeatu *새조각=(void*)((char*)조각+32+luzera_balio);
            새조각->luzera_balio=조각->luzera_balio-luzera_balio-32;새조각->Hurrengoa_elementu=조각->Hurrengoa_elementu;새조각->사용=0;조각->Hurrengoa_elementu=새조각;조각->luzera_balio=luzera_balio;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void askatu_urruneko(void *helbide) {
    if(!helbide)return;Memoria_blokeatu *조각=(void*)((char*)helbide-32);
    volatile unsigned char *지움=helbide;for(size_t 순번=0;순번<조각->luzera_balio;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Hurrengoa_elementu;){if(!조각->사용&&!조각->Hurrengoa_elementu->사용){조각->luzera_balio+=32+조각->Hurrengoa_elementu->luzera_balio;조각->Hurrengoa_elementu=조각->Hurrengoa_elementu->Hurrengoa_elementu;}else 조각=조각->Hurrengoa_elementu;}
}
void *원격재할당(void *helbide,size_t luzera_balio){
    if(!helbide)return esleitu_urruneko(luzera_balio);if(!luzera_balio){askatu_urruneko(helbide);return 0;}
    Memoria_blokeatu *조각=(void*)((char*)helbide-32);void *새주소=esleitu_urruneko(luzera_balio);
    if(새주소){memcpy(새주소,helbide,luzera_balio<조각->luzera_balio?luzera_balio:조각->luzera_balio);askatu_urruneko(helbide);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int karaktere_balio){for(;;Word_SMS++){if(*Word_SMS==(char)karaktere_balio)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t luzera_balio=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,luzera_balio))return(char*)Word_SMS;return luzera_balio?0:(char*)Word_SMS;}
char *strncpy(char *helburu_balio_a0fbc067,const char *원본,size_t luzera_balio){size_t 순번=0;for(;순번<luzera_balio&&원본[순번];순번++)helburu_balio_a0fbc067[순번]=원본[순번];for(;순번<luzera_balio;순번++)helburu_balio_a0fbc067[순번]=0;return helburu_balio_a0fbc067;}
char *strncat(char *helburu_balio_a0fbc067,const char *원본,size_t luzera_balio){char *끝=helburu_balio_a0fbc067+strlen(helburu_balio_a0fbc067);while(luzera_balio--&&*원본)*끝++=*원본++;*끝=0;return helburu_balio_a0fbc067;}
int strncasecmp(const char *가,const char *나,size_t luzera_balio){while(luzera_balio--){unsigned 첫글자=*가++,SEGUNDOA_karaktere=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEGUNDOA_karaktere>='A'&&SEGUNDOA_karaktere<='Z')SEGUNDOA_karaktere+=32;if(첫글자!=SEGUNDOA_karaktere)return(int)첫글자-(int)SEGUNDOA_karaktere;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *mugatzaile_balio,char **Hurrengoa_elementu){if(!Word_SMS)Word_SMS=*Hurrengoa_elementu;while(*Word_SMS&&strchr(mugatzaile_balio,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Hurrengoa_elementu=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(mugatzaile_balio,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Hurrengoa_elementu=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_balio) {
    const char *ITURBURUA=Word_SMS;unsigned long balio=0;int 음수=0,넘침=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_balio==0||BASE_balio==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_balio=16;Word_SMS+=2;}
    if(!BASE_balio)BASE_balio=*Word_SMS=='0'?8:10;
    if(BASE_balio<2||BASE_balio>36){if(끝)*끝=(char*)ITURBURUA;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned karaktere_balio=(unsigned char)*Word_SMS;
        unsigned 수=karaktere_balio>='0'&&karaktere_balio<='9'?karaktere_balio-'0':karaktere_balio>='a'&&karaktere_balio<='z'?karaktere_balio-'a'+10:karaktere_balio>='A'&&karaktere_balio<='Z'?karaktere_balio-'A'+10:36;
        if(수>=(unsigned)BASE_balio)break;
        if(balio>(~0ul-수)/(unsigned)BASE_balio)넘침=1;
        if(!넘침)balio=balio*(unsigned)BASE_balio+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?ITURBURUA:Word_SMS);
    return 넘침?~0ul:음수?0ul-balio:balio;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int erein_Egoera;
void 원격요약(const void *datuak, size_t luzera_balio, unsigned char EMAITZA[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, datuak, luzera_balio); br_sha256_out(&문맥, EMAITZA);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(Posizioa) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Posizioa)))
int 원격난수(unsigned char *helburu_balio_a0fbc067,unsigned luzera_balio){
    if(!erein_Egoera){volatile unsigned char *datuak=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=datuak[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=datuak[8+순번];for(unsigned 순번=0;순번<40;순번++)datuak[순번]=0;erein_Egoera=2;}
        else {erein_Egoera=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(erein_Egoera==2){while(luzera_balio){unsigned char Hurrengoa_elementu[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,Hurrengoa_elementu);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=luzera_balio<32?luzera_balio:32;memcpy(helburu_balio_a0fbc067,Hurrengoa_elementu,수);memset(Hurrengoa_elementu,0,32);helburu_balio_a0fbc067+=수;luzera_balio-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(luzera_balio){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t balio=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&luzera_balio;순번++,luzera_balio--){*helburu_balio_a0fbc067++=balio&255;balio>>=8;}}
    return 0;
}
