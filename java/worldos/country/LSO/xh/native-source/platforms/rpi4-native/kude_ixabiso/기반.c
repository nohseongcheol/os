/* ikheneli_ixabiso 전용 할당기와 iphaswedi_ixabiso 난수 공급. umsebenzisi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct imemori_thintela { size_t ubude_ixabiso; struct imemori_thintela *다음; int 사용; } imemori_thintela;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static imemori_thintela *첫조각;
void *yabela_kude(size_t ubude_ixabiso) {
    if (!ubude_ixabiso || ubude_ixabiso>sizeof(기억터)-64) return 0;
    ubude_ixabiso=(ubude_ixabiso+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->ubude_ixabiso=sizeof(기억터)-32;}
    for(imemori_thintela *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->ubude_ixabiso>=ubude_ixabiso){
        if(조각->ubude_ixabiso>=ubude_ixabiso+64){imemori_thintela *새조각=(void*)((char*)조각+32+ubude_ixabiso);
            새조각->ubude_ixabiso=조각->ubude_ixabiso-ubude_ixabiso-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->ubude_ixabiso=ubude_ixabiso;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void vulela_kude(void *idilesi) {
    if(!idilesi)return;imemori_thintela *조각=(void*)((char*)idilesi-32);
    volatile unsigned char *지움=idilesi;for(size_t 순번=0;순번<조각->ubude_ixabiso;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->ubude_ixabiso+=32+조각->다음->ubude_ixabiso;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *idilesi,size_t ubude_ixabiso){
    if(!idilesi)return yabela_kude(ubude_ixabiso);if(!ubude_ixabiso){vulela_kude(idilesi);return 0;}
    imemori_thintela *조각=(void*)((char*)idilesi-32);void *새주소=yabela_kude(ubude_ixabiso);
    if(새주소){memcpy(새주소,idilesi,ubude_ixabiso<조각->ubude_ixabiso?ubude_ixabiso:조각->ubude_ixabiso);vulela_kude(idilesi);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Igama_I_SMS,int ikharakhtha_ixabiso){for(;;Igama_I_SMS++){if(*Igama_I_SMS==(char)ikharakhtha_ixabiso)return(char*)Igama_I_SMS;if(!*Igama_I_SMS)return 0;}}
char *strstr(const char *Igama_I_SMS,const char *찾음){size_t ubude_ixabiso=strlen(찾음);for(;*Igama_I_SMS;Igama_I_SMS++)if(!strncmp(Igama_I_SMS,찾음,ubude_ixabiso))return(char*)Igama_I_SMS;return ubude_ixabiso?0:(char*)Igama_I_SMS;}
char *strncpy(char *indawo_ekuyiwa_kuyo_ixabiso,const char *원본,size_t ubude_ixabiso){size_t 순번=0;for(;순번<ubude_ixabiso&&원본[순번];순번++)indawo_ekuyiwa_kuyo_ixabiso[순번]=원본[순번];for(;순번<ubude_ixabiso;순번++)indawo_ekuyiwa_kuyo_ixabiso[순번]=0;return indawo_ekuyiwa_kuyo_ixabiso;}
char *strncat(char *indawo_ekuyiwa_kuyo_ixabiso,const char *원본,size_t ubude_ixabiso){char *끝=indawo_ekuyiwa_kuyo_ixabiso+strlen(indawo_ekuyiwa_kuyo_ixabiso);while(ubude_ixabiso--&&*원본)*끝++=*원본++;*끝=0;return indawo_ekuyiwa_kuyo_ixabiso;}
int strncasecmp(const char *가,const char *나,size_t ubude_ixabiso){while(ubude_ixabiso--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Igama_I_SMS,const char *isinqandi_esimiselweyo_ixabiso,char **다음){if(!Igama_I_SMS)Igama_I_SMS=*다음;while(*Igama_I_SMS&&strchr(isinqandi_esimiselweyo_ixabiso,*Igama_I_SMS))Igama_I_SMS++;if(!*Igama_I_SMS){*다음=Igama_I_SMS;return 0;}char *처음=Igama_I_SMS;while(*Igama_I_SMS&&!strchr(isinqandi_esimiselweyo_ixabiso,*Igama_I_SMS))Igama_I_SMS++;if(*Igama_I_SMS)*Igama_I_SMS++=0;*다음=Igama_I_SMS;return 처음;}
unsigned long strtoul(const char *Igama_I_SMS, char **끝, int 밑) {
    const char *UMTHOMBO=Igama_I_SMS;unsigned long ixabiso=0;int 음수=0,ukuphuphuma_ixabiso=0;
    while(*Igama_I_SMS==' '||(*Igama_I_SMS>=9&&*Igama_I_SMS<=13))Igama_I_SMS++;
    if(*Igama_I_SMS=='-'||*Igama_I_SMS=='+')음수=*Igama_I_SMS++=='-';
    if((밑==0||밑==16)&&Igama_I_SMS[0]=='0'&&(Igama_I_SMS[1]=='x'||Igama_I_SMS[1]=='X')&&
       ((Igama_I_SMS[2]>='0'&&Igama_I_SMS[2]<='9')||(Igama_I_SMS[2]>='a'&&Igama_I_SMS[2]<='f')||(Igama_I_SMS[2]>='A'&&Igama_I_SMS[2]<='F'))) {밑=16;Igama_I_SMS+=2;}
    if(!밑)밑=*Igama_I_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)UMTHOMBO;return 0;}
    const char *처음=Igama_I_SMS;
    for(;;Igama_I_SMS++) {
        unsigned ikharakhtha_ixabiso=(unsigned char)*Igama_I_SMS;
        unsigned 수=ikharakhtha_ixabiso>='0'&&ikharakhtha_ixabiso<='9'?ikharakhtha_ixabiso-'0':ikharakhtha_ixabiso>='a'&&ikharakhtha_ixabiso<='z'?ikharakhtha_ixabiso-'a'+10:ikharakhtha_ixabiso>='A'&&ikharakhtha_ixabiso<='Z'?ikharakhtha_ixabiso-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(ixabiso>(~0ul-수)/(unsigned)밑)ukuphuphuma_ixabiso=1;
        if(!ukuphuphuma_ixabiso)ixabiso=ixabiso*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Igama_I_SMS==처음?UMTHOMBO:Igama_I_SMS);
    return ukuphuphuma_ixabiso?~0ul:음수?0ul-ixabiso:ixabiso;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int imbewu_imo;
void kude_ushwankathelo(const void *iingcombolo, size_t ubude_ixabiso, unsigned char 결과[32]) {
    br_sha256_context umxholo_ixabiso;
    br_sha256_init(&umxholo_ixabiso); br_sha256_update(&umxholo_ixabiso, iingcombolo, ubude_ixabiso); br_sha256_out(&umxholo_ixabiso, 결과);
    memset(&umxholo_ixabiso, 0, sizeof(umxholo_ixabiso));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *indawo_ekuyiwa_kuyo_ixabiso,unsigned ubude_ixabiso){
    if(!imbewu_imo){volatile unsigned char *iingcombolo=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=iingcombolo[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=iingcombolo[8+순번];for(unsigned 순번=0;순번<40;순번++)iingcombolo[순번]=0;imbewu_imo=2;}
        else {imbewu_imo=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(imbewu_imo==2){while(ubude_ixabiso){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;kude_ushwankathelo(입력,33,다음);
        입력[32]=1;kude_ushwankathelo(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=ubude_ixabiso<32?ubude_ixabiso:32;memcpy(indawo_ekuyiwa_kuyo_ixabiso,다음,수);memset(다음,0,32);indawo_ekuyiwa_kuyo_ixabiso+=수;ubude_ixabiso-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(ubude_ixabiso){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t ixabiso=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&ubude_ixabiso;순번++,ubude_ixabiso--){*indawo_ekuyiwa_kuyo_ixabiso++=ixabiso&255;ixabiso>>=8;}}
    return 0;
}
