/* mkpụrụobī_kọmpùta_valuu 전용 할당기와 okwuntughe_valuu 난수 공급. òjìàrụ ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct memọrị_gbochie { size_t ogologo_valuu; struct memọrị_gbochie *다음; int 사용; } memọrị_gbochie;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static memọrị_gbochie *첫조각;
void *kepụta_ebe_dị̀anyā(size_t ogologo_valuu) {
    if (!ogologo_valuu || ogologo_valuu>sizeof(기억터)-64) return 0;
    ogologo_valuu=(ogologo_valuu+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->ogologo_valuu=sizeof(기억터)-32;}
    for(memọrị_gbochie *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->ogologo_valuu>=ogologo_valuu){
        if(조각->ogologo_valuu>=ogologo_valuu+64){memọrị_gbochie *새조각=(void*)((char*)조각+32+ogologo_valuu);
            새조각->ogologo_valuu=조각->ogologo_valuu-ogologo_valuu-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->ogologo_valuu=ogologo_valuu;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void bupute_ebe_dị̀anyā(void *àdreèsì) {
    if(!àdreèsì)return;memọrị_gbochie *조각=(void*)((char*)àdreèsì-32);
    volatile unsigned char *지움=àdreèsì;for(size_t 순번=0;순번<조각->ogologo_valuu;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->ogologo_valuu+=32+조각->다음->ogologo_valuu;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *àdreèsì,size_t ogologo_valuu){
    if(!àdreèsì)return kepụta_ebe_dị̀anyā(ogologo_valuu);if(!ogologo_valuu){bupute_ebe_dị̀anyā(àdreèsì);return 0;}
    memọrị_gbochie *조각=(void*)((char*)àdreèsì-32);void *새주소=kepụta_ebe_dị̀anyā(ogologo_valuu);
    if(새주소){memcpy(새주소,àdreèsì,ogologo_valuu<조각->ogologo_valuu?ogologo_valuu:조각->ogologo_valuu);bupute_ebe_dị̀anyā(àdreèsì);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Mkpụrụokwu_SMS,int mkpụrụedemede_valuu){for(;;Mkpụrụokwu_SMS++){if(*Mkpụrụokwu_SMS==(char)mkpụrụedemede_valuu)return(char*)Mkpụrụokwu_SMS;if(!*Mkpụrụokwu_SMS)return 0;}}
char *strstr(const char *Mkpụrụokwu_SMS,const char *찾음){size_t ogologo_valuu=strlen(찾음);for(;*Mkpụrụokwu_SMS;Mkpụrụokwu_SMS++)if(!strncmp(Mkpụrụokwu_SMS,찾음,ogologo_valuu))return(char*)Mkpụrụokwu_SMS;return ogologo_valuu?0:(char*)Mkpụrụokwu_SMS;}
char *strncpy(char *ebemwèga_valuu,const char *원본,size_t ogologo_valuu){size_t 순번=0;for(;순번<ogologo_valuu&&원본[순번];순번++)ebemwèga_valuu[순번]=원본[순번];for(;순번<ogologo_valuu;순번++)ebemwèga_valuu[순번]=0;return ebemwèga_valuu;}
char *strncat(char *ebemwèga_valuu,const char *원본,size_t ogologo_valuu){char *끝=ebemwèga_valuu+strlen(ebemwèga_valuu);while(ogologo_valuu--&&*원본)*끝++=*원본++;*끝=0;return ebemwèga_valuu;}
int strncasecmp(const char *가,const char *나,size_t ogologo_valuu){while(ogologo_valuu--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Mkpụrụokwu_SMS,const char *nzinjedebe_valuu,char **다음){if(!Mkpụrụokwu_SMS)Mkpụrụokwu_SMS=*다음;while(*Mkpụrụokwu_SMS&&strchr(nzinjedebe_valuu,*Mkpụrụokwu_SMS))Mkpụrụokwu_SMS++;if(!*Mkpụrụokwu_SMS){*다음=Mkpụrụokwu_SMS;return 0;}char *처음=Mkpụrụokwu_SMS;while(*Mkpụrụokwu_SMS&&!strchr(nzinjedebe_valuu,*Mkpụrụokwu_SMS))Mkpụrụokwu_SMS++;if(*Mkpụrụokwu_SMS)*Mkpụrụokwu_SMS++=0;*다음=Mkpụrụokwu_SMS;return 처음;}
unsigned long strtoul(const char *Mkpụrụokwu_SMS, char **끝, int 밑) {
    const char *ebensìbịa=Mkpụrụokwu_SMS;unsigned long valuu=0;int 음수=0,njubigaoke_valuu=0;
    while(*Mkpụrụokwu_SMS==' '||(*Mkpụrụokwu_SMS>=9&&*Mkpụrụokwu_SMS<=13))Mkpụrụokwu_SMS++;
    if(*Mkpụrụokwu_SMS=='-'||*Mkpụrụokwu_SMS=='+')음수=*Mkpụrụokwu_SMS++=='-';
    if((밑==0||밑==16)&&Mkpụrụokwu_SMS[0]=='0'&&(Mkpụrụokwu_SMS[1]=='x'||Mkpụrụokwu_SMS[1]=='X')&&
       ((Mkpụrụokwu_SMS[2]>='0'&&Mkpụrụokwu_SMS[2]<='9')||(Mkpụrụokwu_SMS[2]>='a'&&Mkpụrụokwu_SMS[2]<='f')||(Mkpụrụokwu_SMS[2]>='A'&&Mkpụrụokwu_SMS[2]<='F'))) {밑=16;Mkpụrụokwu_SMS+=2;}
    if(!밑)밑=*Mkpụrụokwu_SMS=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)ebensìbịa;return 0;}
    const char *처음=Mkpụrụokwu_SMS;
    for(;;Mkpụrụokwu_SMS++) {
        unsigned mkpụrụedemede_valuu=(unsigned char)*Mkpụrụokwu_SMS;
        unsigned 수=mkpụrụedemede_valuu>='0'&&mkpụrụedemede_valuu<='9'?mkpụrụedemede_valuu-'0':mkpụrụedemede_valuu>='a'&&mkpụrụedemede_valuu<='z'?mkpụrụedemede_valuu-'a'+10:mkpụrụedemede_valuu>='A'&&mkpụrụedemede_valuu<='Z'?mkpụrụedemede_valuu-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(valuu>(~0ul-수)/(unsigned)밑)njubigaoke_valuu=1;
        if(!njubigaoke_valuu)valuu=valuu*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(Mkpụrụokwu_SMS==처음?ebensìbịa:Mkpụrụokwu_SMS);
    return njubigaoke_valuu?~0ul:음수?0ul-valuu:valuu;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int mkpụrụ_ọnọdụ;
void ebe_dị̀anyā_nchịkọta(const void *datà, size_t ogologo_valuu, unsigned char 결과[32]) {
    br_sha256_context Ọnọdụ_valuu;
    br_sha256_init(&Ọnọdụ_valuu); br_sha256_update(&Ọnọdụ_valuu, datà, ogologo_valuu); br_sha256_out(&Ọnọdụ_valuu, 결과);
    memset(&Ọnọdụ_valuu, 0, sizeof(Ọnọdụ_valuu));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *ebemwèga_valuu,unsigned ogologo_valuu){
    if(!mkpụrụ_ọnọdụ){volatile unsigned char *datà=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=datà[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=datà[8+순번];for(unsigned 순번=0;순번<40;순번++)datà[순번]=0;mkpụrụ_ọnọdụ=2;}
        else {mkpụrụ_ọnọdụ=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(mkpụrụ_ọnọdụ==2){while(ogologo_valuu){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;ebe_dị̀anyā_nchịkọta(입력,33,다음);
        입력[32]=1;ebe_dị̀anyā_nchịkọta(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=ogologo_valuu<32?ogologo_valuu:32;memcpy(ebemwèga_valuu,다음,수);memset(다음,0,32);ebemwèga_valuu+=수;ogologo_valuu-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(ogologo_valuu){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t valuu=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&ogologo_valuu;순번++,ogologo_valuu--){*ebemwèga_valuu++=valuu&255;valuu>>=8;}}
    return 0;
}
