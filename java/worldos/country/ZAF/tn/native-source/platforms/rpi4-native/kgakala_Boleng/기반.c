/* Khenele_Boleng 전용 할당기와 khoututseno_Boleng 난수 공급. modirisi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct memori_thibela { size_t boleele_Boleng; struct memori_thibela *다음; int 사용; } memori_thibela;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static memori_thibela *첫조각;
void *abela_kgakala(size_t boleele_Boleng) {
    if (!boleele_Boleng || boleele_Boleng>sizeof(기억터)-64) return 0;
    boleele_Boleng=(boleele_Boleng+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->boleele_Boleng=sizeof(기억터)-32;}
    for(memori_thibela *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->boleele_Boleng>=boleele_Boleng){
        if(조각->boleele_Boleng>=boleele_Boleng+64){memori_thibela *새조각=(void*)((char*)조각+32+boleele_Boleng);
            새조각->boleele_Boleng=조각->boleele_Boleng-boleele_Boleng-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->boleele_Boleng=boleele_Boleng;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void ntsha_kgakala(void *aterese) {
    if(!aterese)return;memori_thibela *조각=(void*)((char*)aterese-32);
    volatile unsigned char *지움=aterese;for(size_t 순번=0;순번<조각->boleele_Boleng;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->boleele_Boleng+=32+조각->다음->boleele_Boleng;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *aterese,size_t boleele_Boleng){
    if(!aterese)return abela_kgakala(boleele_Boleng);if(!boleele_Boleng){ntsha_kgakala(aterese);return 0;}
    memori_thibela *조각=(void*)((char*)aterese-32);void *새주소=abela_kgakala(boleele_Boleng);
    if(새주소){memcpy(새주소,aterese,boleele_Boleng<조각->boleele_Boleng?boleele_Boleng:조각->boleele_Boleng);ntsha_kgakala(aterese);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Lefoko_SMS,int Letshwao_Boleng){for(;;Lefoko_SMS++){if(*Lefoko_SMS==(char)Letshwao_Boleng)return(char*)Lefoko_SMS;if(!*Lefoko_SMS)return 0;}}
char *strstr(const char *Lefoko_SMS,const char *찾음){size_t boleele_Boleng=strlen(찾음);for(;*Lefoko_SMS;Lefoko_SMS++)if(!strncmp(Lefoko_SMS,찾음,boleele_Boleng))return(char*)Lefoko_SMS;return boleele_Boleng?0:(char*)Lefoko_SMS;}
char *strncpy(char *bogorogelo_Boleng,const char *원본,size_t boleele_Boleng){size_t 순번=0;for(;순번<boleele_Boleng&&원본[순번];순번++)bogorogelo_Boleng[순번]=원본[순번];for(;순번<boleele_Boleng;순번++)bogorogelo_Boleng[순번]=0;return bogorogelo_Boleng;}
char *strncat(char *bogorogelo_Boleng,const char *원본,size_t boleele_Boleng){char *끝=bogorogelo_Boleng+strlen(bogorogelo_Boleng);while(boleele_Boleng--&&*원본)*끝++=*원본++;*끝=0;return bogorogelo_Boleng;}
int strncasecmp(const char *가,const char *나,size_t boleele_Boleng){while(boleele_Boleng--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Lefoko_SMS,const char *sekgaoganyi_Boleng,char **다음){if(!Lefoko_SMS)Lefoko_SMS=*다음;while(*Lefoko_SMS&&strchr(sekgaoganyi_Boleng,*Lefoko_SMS))Lefoko_SMS++;if(!*Lefoko_SMS){*다음=Lefoko_SMS;return 0;}char *처음=Lefoko_SMS;while(*Lefoko_SMS&&!strchr(sekgaoganyi_Boleng,*Lefoko_SMS))Lefoko_SMS++;if(*Lefoko_SMS)*Lefoko_SMS++=0;*다음=Lefoko_SMS;return 처음;}
unsigned long strtoul(const char *Lefoko_SMS, char **끝, int 밑) {
    const char *Motswedi=Lefoko_SMS;unsigned long Boleng=0;int 음수=0,penologo_Boleng=0;
    while(*Lefoko_SMS==' '||(*Lefoko_SMS>=9&&*Lefoko_SMS<=13))Lefoko_SMS++;
    if(*Lefoko_SMS=='-'||*Lefoko_SMS=='+')음수=*Lefoko_SMS++=='-';
    if((밑==0||밑==16)&&Lefoko_SMS[0]=='0'&&(Lefoko_SMS[1]=='x'||Lefoko_SMS[1]=='X')&&
       ((Lefoko_SMS[2]>='0'&&Lefoko_SMS[2]<='9')||(Lefoko_SMS[2]>='a'&&Lefoko_SMS[2]<='f')||(Lefoko_SMS[2]>='A'&&Lefoko_SMS[2]<='F'))) {밑=16;Lefoko_SMS+=2;}
    if(!밑)밑=*Lefoko_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)Motswedi;return 0;}
    const char *처음=Lefoko_SMS;
    for(;;Lefoko_SMS++) {
        unsigned Letshwao_Boleng=(unsigned char)*Lefoko_SMS;
        unsigned 수=Letshwao_Boleng>='0'&&Letshwao_Boleng<='9'?Letshwao_Boleng-'0':Letshwao_Boleng>='a'&&Letshwao_Boleng<='z'?Letshwao_Boleng-'a'+10:Letshwao_Boleng>='A'&&Letshwao_Boleng<='Z'?Letshwao_Boleng-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(Boleng>(~0ul-수)/(unsigned)밑)penologo_Boleng=1;
        if(!penologo_Boleng)Boleng=Boleng*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Lefoko_SMS==처음?Motswedi:Lefoko_SMS);
    return penologo_Boleng?~0ul:음수?0ul-Boleng:Boleng;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int peo_kemo;
void kgakala_tshobokanyo(const void *tshedimosetso, size_t boleele_Boleng, unsigned char 결과[32]) {
    br_sha256_context bokao_Boleng;
    br_sha256_init(&bokao_Boleng); br_sha256_update(&bokao_Boleng, tshedimosetso, boleele_Boleng); br_sha256_out(&bokao_Boleng, 결과);
    memset(&bokao_Boleng, 0, sizeof(bokao_Boleng));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *bogorogelo_Boleng,unsigned boleele_Boleng){
    if(!peo_kemo){volatile unsigned char *tshedimosetso=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=tshedimosetso[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=tshedimosetso[8+순번];for(unsigned 순번=0;순번<40;순번++)tshedimosetso[순번]=0;peo_kemo=2;}
        else {peo_kemo=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(peo_kemo==2){while(boleele_Boleng){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;kgakala_tshobokanyo(입력,33,다음);
        입력[32]=1;kgakala_tshobokanyo(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=boleele_Boleng<32?boleele_Boleng:32;memcpy(bogorogelo_Boleng,다음,수);memset(다음,0,32);bogorogelo_Boleng+=수;boleele_Boleng-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(boleele_Boleng){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t Boleng=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&boleele_Boleng;순번++,boleele_Boleng--){*bogorogelo_Boleng++=Boleng&255;Boleng>>=8;}}
    return 0;
}
