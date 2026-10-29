/* nucli_VALOR 전용 할당기와 contrasenya_VALOR 난수 공급. usuari ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memòria_bloquejar { size_t durada_VALOR; struct Memòria_bloquejar *Següent_element; int ús_VALOR; } Memòria_bloquejar;
static unsigned char Memòria_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memòria_bloquejar *첫조각;
void *assignar_remot(size_t durada_VALOR) {
    if (!durada_VALOR || durada_VALOR>sizeof(Memòria_Arena)-64) return 0;
    durada_VALOR=(durada_VALOR+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memòria_Arena;첫조각->durada_VALOR=sizeof(Memòria_Arena)-32;}
    for(Memòria_bloquejar *조각=첫조각;조각;조각=조각->Següent_element)if(!조각->ús_VALOR&&조각->durada_VALOR>=durada_VALOR){
        if(조각->durada_VALOR>=durada_VALOR+64){Memòria_bloquejar *새조각=(void*)((char*)조각+32+durada_VALOR);
            새조각->durada_VALOR=조각->durada_VALOR-durada_VALOR-32;새조각->Següent_element=조각->Següent_element;새조각->ús_VALOR=0;조각->Següent_element=새조각;조각->durada_VALOR=durada_VALOR;}
        조각->ús_VALOR=1;return(char*)조각+32;
    }return 0;
}
void versió_remot(void *Adreça) {
    if(!Adreça)return;Memòria_bloquejar *조각=(void*)((char*)Adreça-32);
    volatile unsigned char *지움=Adreça;for(size_t 순번=0;순번<조각->durada_VALOR;순번++)지움[순번]=0;
    조각->ús_VALOR=0;
    for(조각=첫조각;조각&&조각->Següent_element;){if(!조각->ús_VALOR&&!조각->Següent_element->ús_VALOR){조각->durada_VALOR+=32+조각->Següent_element->durada_VALOR;조각->Següent_element=조각->Següent_element->Següent_element;}else 조각=조각->Següent_element;}
}
void *원격재할당(void *Adreça,size_t durada_VALOR){
    if(!Adreça)return assignar_remot(durada_VALOR);if(!durada_VALOR){versió_remot(Adreça);return 0;}
    Memòria_bloquejar *조각=(void*)((char*)Adreça-32);void *새주소=assignar_remot(durada_VALOR);
    if(새주소){memcpy(새주소,Adreça,durada_VALOR<조각->durada_VALOR?durada_VALOR:조각->durada_VALOR);versió_remot(Adreça);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int caràcter_VALOR){for(;;Word_SMS++){if(*Word_SMS==(char)caràcter_VALOR)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t durada_VALOR=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,durada_VALOR))return(char*)Word_SMS;return durada_VALOR?0:(char*)Word_SMS;}
char *strncpy(char *destinació_VALOR,const char *원본,size_t durada_VALOR){size_t 순번=0;for(;순번<durada_VALOR&&원본[순번];순번++)destinació_VALOR[순번]=원본[순번];for(;순번<durada_VALOR;순번++)destinació_VALOR[순번]=0;return destinació_VALOR;}
char *strncat(char *destinació_VALOR,const char *원본,size_t durada_VALOR){char *끝=destinació_VALOR+strlen(destinació_VALOR);while(durada_VALOR--&&*원본)*끝++=*원본++;*끝=0;return destinació_VALOR;}
int strncasecmp(const char *가,const char *나,size_t durada_VALOR){while(durada_VALOR--){unsigned 첫글자=*가++,SEGON_caràcter=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SEGON_caràcter>='A'&&SEGON_caràcter<='Z')SEGON_caràcter+=32;if(첫글자!=SEGON_caràcter)return(int)첫글자-(int)SEGON_caràcter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *구분,char **Següent_element){if(!Word_SMS)Word_SMS=*Següent_element;while(*Word_SMS&&strchr(구분,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Següent_element=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(구분,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Següent_element=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALOR) {
    const char *FONT=Word_SMS;unsigned long VALOR=0;int 음수=0,sobreeiximent_VALOR=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALOR==0||BASE_VALOR==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALOR=16;Word_SMS+=2;}
    if(!BASE_VALOR)BASE_VALOR=*Word_SMS=='0'?8:10;
    if(BASE_VALOR<2||BASE_VALOR>36){if(끝)*끝=(char*)FONT;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned caràcter_VALOR=(unsigned char)*Word_SMS;
        unsigned 수=caràcter_VALOR>='0'&&caràcter_VALOR<='9'?caràcter_VALOR-'0':caràcter_VALOR>='a'&&caràcter_VALOR<='z'?caràcter_VALOR-'a'+10:caràcter_VALOR>='A'&&caràcter_VALOR<='Z'?caràcter_VALOR-'A'+10:36;
        if(수>=(unsigned)BASE_VALOR)break;
        if(VALOR>(~0ul-수)/(unsigned)BASE_VALOR)sobreeiximent_VALOR=1;
        if(!sobreeiximent_VALOR)VALOR=VALOR*(unsigned)BASE_VALOR+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?FONT:Word_SMS);
    return sobreeiximent_VALOR?~0ul:음수?0ul-VALOR:VALOR;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int proveir_Estat;
void remot_resum(const void *dades, size_t durada_VALOR, unsigned char RESULTAT[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, dades, durada_VALOR); br_sha256_out(&문맥, RESULTAT);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(Posició) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Posició)))
int 원격난수(unsigned char *destinació_VALOR,unsigned durada_VALOR){
    if(!proveir_Estat){volatile unsigned char *dades=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=dades[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=dades[8+순번];for(unsigned 순번=0;순번<40;순번++)dades[순번]=0;proveir_Estat=2;}
        else {proveir_Estat=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(proveir_Estat==2){while(durada_VALOR){unsigned char Següent_element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;remot_resum(입력,33,Següent_element);
        입력[32]=1;remot_resum(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=durada_VALOR<32?durada_VALOR:32;memcpy(destinació_VALOR,Següent_element,수);memset(Següent_element,0,32);destinació_VALOR+=수;durada_VALOR-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(durada_VALOR){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALOR=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&durada_VALOR;순번++,durada_VALOR--){*destinació_VALOR++=VALOR&255;VALOR>>=8;}}
    return 0;
}
