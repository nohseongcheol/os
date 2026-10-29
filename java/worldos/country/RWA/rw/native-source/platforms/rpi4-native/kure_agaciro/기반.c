/* intima_agaciro 전용 할당기와 ijambobanga_agaciro 난수 공급. ukoresha ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct ububiko_guheza { size_t uburebure_agaciro; struct ububiko_guheza *다음; int 사용; } ububiko_guheza;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static ububiko_guheza *첫조각;
void *kugenera_kure(size_t uburebure_agaciro) {
    if (!uburebure_agaciro || uburebure_agaciro>sizeof(기억터)-64) return 0;
    uburebure_agaciro=(uburebure_agaciro+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->uburebure_agaciro=sizeof(기억터)-32;}
    for(ububiko_guheza *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->uburebure_agaciro>=uburebure_agaciro){
        if(조각->uburebure_agaciro>=uburebure_agaciro+64){ububiko_guheza *새조각=(void*)((char*)조각+32+uburebure_agaciro);
            새조각->uburebure_agaciro=조각->uburebure_agaciro-uburebure_agaciro-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->uburebure_agaciro=uburebure_agaciro;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void kurekura_kure(void *aderesi) {
    if(!aderesi)return;ububiko_guheza *조각=(void*)((char*)aderesi-32);
    volatile unsigned char *지움=aderesi;for(size_t 순번=0;순번<조각->uburebure_agaciro;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->uburebure_agaciro+=32+조각->다음->uburebure_agaciro;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *aderesi,size_t uburebure_agaciro){
    if(!aderesi)return kugenera_kure(uburebure_agaciro);if(!uburebure_agaciro){kurekura_kure(aderesi);return 0;}
    ububiko_guheza *조각=(void*)((char*)aderesi-32);void *새주소=kugenera_kure(uburebure_agaciro);
    if(새주소){memcpy(새주소,aderesi,uburebure_agaciro<조각->uburebure_agaciro?uburebure_agaciro:조각->uburebure_agaciro);kurekura_kure(aderesi);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Ijambo_SMS,int inyuguti_agaciro){for(;;Ijambo_SMS++){if(*Ijambo_SMS==(char)inyuguti_agaciro)return(char*)Ijambo_SMS;if(!*Ijambo_SMS)return 0;}}
char *strstr(const char *Ijambo_SMS,const char *찾음){size_t uburebure_agaciro=strlen(찾음);for(;*Ijambo_SMS;Ijambo_SMS++)if(!strncmp(Ijambo_SMS,찾음,uburebure_agaciro))return(char*)Ijambo_SMS;return uburebure_agaciro?0:(char*)Ijambo_SMS;}
char *strncpy(char *aho_ijya_agaciro,const char *원본,size_t uburebure_agaciro){size_t 순번=0;for(;순번<uburebure_agaciro&&원본[순번];순번++)aho_ijya_agaciro[순번]=원본[순번];for(;순번<uburebure_agaciro;순번++)aho_ijya_agaciro[순번]=0;return aho_ijya_agaciro;}
char *strncat(char *aho_ijya_agaciro,const char *원본,size_t uburebure_agaciro){char *끝=aho_ijya_agaciro+strlen(aho_ijya_agaciro);while(uburebure_agaciro--&&*원본)*끝++=*원본++;*끝=0;return aho_ijya_agaciro;}
int strncasecmp(const char *가,const char *나,size_t uburebure_agaciro){while(uburebure_agaciro--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Ijambo_SMS,const char *mutandukanya_agaciro_d8ba4873,char **다음){if(!Ijambo_SMS)Ijambo_SMS=*다음;while(*Ijambo_SMS&&strchr(mutandukanya_agaciro_d8ba4873,*Ijambo_SMS))Ijambo_SMS++;if(!*Ijambo_SMS){*다음=Ijambo_SMS;return 0;}char *처음=Ijambo_SMS;while(*Ijambo_SMS&&!strchr(mutandukanya_agaciro_d8ba4873,*Ijambo_SMS))Ijambo_SMS++;if(*Ijambo_SMS)*Ijambo_SMS++=0;*다음=Ijambo_SMS;return 처음;}
unsigned long strtoul(const char *Ijambo_SMS, char **끝, int 밑) {
    const char *Inkomoko=Ijambo_SMS;unsigned long agaciro=0;int 음수=0,umusago_agaciro=0;
    while(*Ijambo_SMS==' '||(*Ijambo_SMS>=9&&*Ijambo_SMS<=13))Ijambo_SMS++;
    if(*Ijambo_SMS=='-'||*Ijambo_SMS=='+')음수=*Ijambo_SMS++=='-';
    if((밑==0||밑==16)&&Ijambo_SMS[0]=='0'&&(Ijambo_SMS[1]=='x'||Ijambo_SMS[1]=='X')&&
       ((Ijambo_SMS[2]>='0'&&Ijambo_SMS[2]<='9')||(Ijambo_SMS[2]>='a'&&Ijambo_SMS[2]<='f')||(Ijambo_SMS[2]>='A'&&Ijambo_SMS[2]<='F'))) {밑=16;Ijambo_SMS+=2;}
    if(!밑)밑=*Ijambo_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)Inkomoko;return 0;}
    const char *처음=Ijambo_SMS;
    for(;;Ijambo_SMS++) {
        unsigned inyuguti_agaciro=(unsigned char)*Ijambo_SMS;
        unsigned 수=inyuguti_agaciro>='0'&&inyuguti_agaciro<='9'?inyuguti_agaciro-'0':inyuguti_agaciro>='a'&&inyuguti_agaciro<='z'?inyuguti_agaciro-'a'+10:inyuguti_agaciro>='A'&&inyuguti_agaciro<='Z'?inyuguti_agaciro-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(agaciro>(~0ul-수)/(unsigned)밑)umusago_agaciro=1;
        if(!umusago_agaciro)agaciro=agaciro*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Ijambo_SMS==처음?Inkomoko:Ijambo_SMS);
    return umusago_agaciro?~0ul:음수?0ul-agaciro:agaciro;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int amakuru_imimerere;
void 원격요약(const void *amakurushingiro, size_t uburebure_agaciro, unsigned char 결과[32]) {
    br_sha256_context Imikoreshereze_agaciro;
    br_sha256_init(&Imikoreshereze_agaciro); br_sha256_update(&Imikoreshereze_agaciro, amakurushingiro, uburebure_agaciro); br_sha256_out(&Imikoreshereze_agaciro, 결과);
    memset(&Imikoreshereze_agaciro, 0, sizeof(Imikoreshereze_agaciro));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *aho_ijya_agaciro,unsigned uburebure_agaciro){
    if(!amakuru_imimerere){volatile unsigned char *amakurushingiro=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=amakurushingiro[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=amakurushingiro[8+순번];for(unsigned 순번=0;순번<40;순번++)amakurushingiro[순번]=0;amakuru_imimerere=2;}
        else {amakuru_imimerere=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(amakuru_imimerere==2){while(uburebure_agaciro){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,다음);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=uburebure_agaciro<32?uburebure_agaciro:32;memcpy(aho_ijya_agaciro,다음,수);memset(다음,0,32);aho_ijya_agaciro+=수;uburebure_agaciro-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(uburebure_agaciro){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t agaciro=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&uburebure_agaciro;순번++,uburebure_agaciro--){*aho_ijya_agaciro++=agaciro&255;agaciro>>=8;}}
    return 0;
}
