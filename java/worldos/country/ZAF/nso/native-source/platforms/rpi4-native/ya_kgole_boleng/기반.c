/* khenele_boleng 전용 할당기와 phasewete_boleng 난수 공급. mošomiši ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct memori_thibela { size_t botelele_boleng; struct memori_thibela *다음; int 사용; } memori_thibela;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static memori_thibela *첫조각;
void *aba_ya_kgole(size_t botelele_boleng) {
    if (!botelele_boleng || botelele_boleng>sizeof(기억터)-64) return 0;
    botelele_boleng=(botelele_boleng+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->botelele_boleng=sizeof(기억터)-32;}
    for(memori_thibela *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->botelele_boleng>=botelele_boleng){
        if(조각->botelele_boleng>=botelele_boleng+64){memori_thibela *새조각=(void*)((char*)조각+32+botelele_boleng);
            새조각->botelele_boleng=조각->botelele_boleng-botelele_boleng-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->botelele_boleng=botelele_boleng;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void lokolla_ya_kgole(void *atrese) {
    if(!atrese)return;memori_thibela *조각=(void*)((char*)atrese-32);
    volatile unsigned char *지움=atrese;for(size_t 순번=0;순번<조각->botelele_boleng;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->botelele_boleng+=32+조각->다음->botelele_boleng;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *atrese,size_t botelele_boleng){
    if(!atrese)return aba_ya_kgole(botelele_boleng);if(!botelele_boleng){lokolla_ya_kgole(atrese);return 0;}
    memori_thibela *조각=(void*)((char*)atrese-32);void *새주소=aba_ya_kgole(botelele_boleng);
    if(새주소){memcpy(새주소,atrese,botelele_boleng<조각->botelele_boleng?botelele_boleng:조각->botelele_boleng);lokolla_ya_kgole(atrese);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Thalokontšu_SMS,int tlhaka_boleng){for(;;Thalokontšu_SMS++){if(*Thalokontšu_SMS==(char)tlhaka_boleng)return(char*)Thalokontšu_SMS;if(!*Thalokontšu_SMS)return 0;}}
char *strstr(const char *Thalokontšu_SMS,const char *찾음){size_t botelele_boleng=strlen(찾음);for(;*Thalokontšu_SMS;Thalokontšu_SMS++)if(!strncmp(Thalokontšu_SMS,찾음,botelele_boleng))return(char*)Thalokontšu_SMS;return botelele_boleng?0:(char*)Thalokontšu_SMS;}
char *strncpy(char *boyo_boleng,const char *원본,size_t botelele_boleng){size_t 순번=0;for(;순번<botelele_boleng&&원본[순번];순번++)boyo_boleng[순번]=원본[순번];for(;순번<botelele_boleng;순번++)boyo_boleng[순번]=0;return boyo_boleng;}
char *strncat(char *boyo_boleng,const char *원본,size_t botelele_boleng){char *끝=boyo_boleng+strlen(boyo_boleng);while(botelele_boleng--&&*원본)*끝++=*원본++;*끝=0;return boyo_boleng;}
int strncasecmp(const char *가,const char *나,size_t botelele_boleng){while(botelele_boleng--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Thalokontšu_SMS,const char *searoganyi_boleng_d8ba4873,char **다음){if(!Thalokontšu_SMS)Thalokontšu_SMS=*다음;while(*Thalokontšu_SMS&&strchr(searoganyi_boleng_d8ba4873,*Thalokontšu_SMS))Thalokontšu_SMS++;if(!*Thalokontšu_SMS){*다음=Thalokontšu_SMS;return 0;}char *처음=Thalokontšu_SMS;while(*Thalokontšu_SMS&&!strchr(searoganyi_boleng_d8ba4873,*Thalokontšu_SMS))Thalokontšu_SMS++;if(*Thalokontšu_SMS)*Thalokontšu_SMS++=0;*다음=Thalokontšu_SMS;return 처음;}
unsigned long strtoul(const char *Thalokontšu_SMS, char **끝, int 밑) {
    const char *mohlodi=Thalokontšu_SMS;unsigned long boleng=0;int 음수=0,mongwaloutama_boleng=0;
    while(*Thalokontšu_SMS==' '||(*Thalokontšu_SMS>=9&&*Thalokontšu_SMS<=13))Thalokontšu_SMS++;
    if(*Thalokontšu_SMS=='-'||*Thalokontšu_SMS=='+')음수=*Thalokontšu_SMS++=='-';
    if((밑==0||밑==16)&&Thalokontšu_SMS[0]=='0'&&(Thalokontšu_SMS[1]=='x'||Thalokontšu_SMS[1]=='X')&&
       ((Thalokontšu_SMS[2]>='0'&&Thalokontšu_SMS[2]<='9')||(Thalokontšu_SMS[2]>='a'&&Thalokontšu_SMS[2]<='f')||(Thalokontšu_SMS[2]>='A'&&Thalokontšu_SMS[2]<='F'))) {밑=16;Thalokontšu_SMS+=2;}
    if(!밑)밑=*Thalokontšu_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)mohlodi;return 0;}
    const char *처음=Thalokontšu_SMS;
    for(;;Thalokontšu_SMS++) {
        unsigned tlhaka_boleng=(unsigned char)*Thalokontšu_SMS;
        unsigned 수=tlhaka_boleng>='0'&&tlhaka_boleng<='9'?tlhaka_boleng-'0':tlhaka_boleng>='a'&&tlhaka_boleng<='z'?tlhaka_boleng-'a'+10:tlhaka_boleng>='A'&&tlhaka_boleng<='Z'?tlhaka_boleng-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(boleng>(~0ul-수)/(unsigned)밑)mongwaloutama_boleng=1;
        if(!mongwaloutama_boleng)boleng=boleng*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Thalokontšu_SMS==처음?mohlodi:Thalokontšu_SMS);
    return mongwaloutama_boleng?~0ul:음수?0ul-boleng:boleng;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int kalo_boemo;
void ya_kgole_khutsofatšo(const void *data, size_t botelele_boleng, unsigned char 결과[32]) {
    br_sha256_context Kamano_boleng;
    br_sha256_init(&Kamano_boleng); br_sha256_update(&Kamano_boleng, data, botelele_boleng); br_sha256_out(&Kamano_boleng, 결과);
    memset(&Kamano_boleng, 0, sizeof(Kamano_boleng));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *boyo_boleng,unsigned botelele_boleng){
    if(!kalo_boemo){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;kalo_boemo=2;}
        else {kalo_boemo=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(kalo_boemo==2){while(botelele_boleng){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;ya_kgole_khutsofatšo(입력,33,다음);
        입력[32]=1;ya_kgole_khutsofatšo(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=botelele_boleng<32?botelele_boleng:32;memcpy(boyo_boleng,다음,수);memset(다음,0,32);boyo_boleng+=수;botelele_boleng-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(botelele_boleng){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t boleng=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&botelele_boleng;순번++,botelele_boleng--){*boyo_boleng++=boleng&255;boleng>>=8;}}
    return 0;
}
