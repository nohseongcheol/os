/* kernel_VALUE 전용 할당기와 password_VALUE 난수 공급. gumagamit ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memory_i_block { size_t haba_VALUE; struct Memory_i_block *Susunod_item; int 사용; } Memory_i_block;
static unsigned char Memory_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memory_i_block *첫조각;
void *maglaan_malayuan(size_t haba_VALUE) {
    if (!haba_VALUE || haba_VALUE>sizeof(Memory_Arena)-64) return 0;
    haba_VALUE=(haba_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memory_Arena;첫조각->haba_VALUE=sizeof(Memory_Arena)-32;}
    for(Memory_i_block *조각=첫조각;조각;조각=조각->Susunod_item)if(!조각->사용&&조각->haba_VALUE>=haba_VALUE){
        if(조각->haba_VALUE>=haba_VALUE+64){Memory_i_block *새조각=(void*)((char*)조각+32+haba_VALUE);
            새조각->haba_VALUE=조각->haba_VALUE-haba_VALUE-32;새조각->Susunod_item=조각->Susunod_item;새조각->사용=0;조각->Susunod_item=새조각;조각->haba_VALUE=haba_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void release_malayuan(void *email) {
    if(!email)return;Memory_i_block *조각=(void*)((char*)email-32);
    volatile unsigned char *지움=email;for(size_t 순번=0;순번<조각->haba_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Susunod_item;){if(!조각->사용&&!조각->Susunod_item->사용){조각->haba_VALUE+=32+조각->Susunod_item->haba_VALUE;조각->Susunod_item=조각->Susunod_item->Susunod_item;}else 조각=조각->Susunod_item;}
}
void *원격재할당(void *email,size_t haba_VALUE){
    if(!email)return maglaan_malayuan(haba_VALUE);if(!haba_VALUE){release_malayuan(email);return 0;}
    Memory_i_block *조각=(void*)((char*)email-32);void *새주소=maglaan_malayuan(haba_VALUE);
    if(새주소){memcpy(새주소,email,haba_VALUE<조각->haba_VALUE?haba_VALUE:조각->haba_VALUE);release_malayuan(email);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int karakter_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)karakter_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t haba_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,haba_VALUE))return(char*)Word_SMS;return haba_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *patutunguhan_VALUE,const char *원본,size_t haba_VALUE){size_t 순번=0;for(;순번<haba_VALUE&&원본[순번];순번++)patutunguhan_VALUE[순번]=원본[순번];for(;순번<haba_VALUE;순번++)patutunguhan_VALUE[순번]=0;return patutunguhan_VALUE;}
char *strncat(char *patutunguhan_VALUE,const char *원본,size_t haba_VALUE){char *끝=patutunguhan_VALUE+strlen(patutunguhan_VALUE);while(haba_VALUE--&&*원본)*끝++=*원본++;*끝=0;return patutunguhan_VALUE;}
int strncasecmp(const char *가,const char *나,size_t haba_VALUE){while(haba_VALUE--){unsigned 첫글자=*가++,SECOND_karakter=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_karakter>='A'&&SECOND_karakter<='Z')SECOND_karakter+=32;if(첫글자!=SECOND_karakter)return(int)첫글자-(int)SECOND_karakter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *panghiwalay_VALUE,char **Susunod_item){if(!Word_SMS)Word_SMS=*Susunod_item;while(*Word_SMS&&strchr(panghiwalay_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Susunod_item=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(panghiwalay_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Susunod_item=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *pinagmulan=Word_SMS;unsigned long VALUE=0;int 음수=0,sobrang_teksto_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)pinagmulan;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned karakter_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=karakter_VALUE>='0'&&karakter_VALUE<='9'?karakter_VALUE-'0':karakter_VALUE>='a'&&karakter_VALUE<='z'?karakter_VALUE-'a'+10:karakter_VALUE>='A'&&karakter_VALUE<='Z'?karakter_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)sobrang_teksto_VALUE=1;
        if(!sobrang_teksto_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?pinagmulan:Word_SMS);
    return sobrang_teksto_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int seed_katayuan;
void malayuan_buod(const void *data, size_t haba_VALUE, unsigned char sukat[32]) {
    br_sha256_context Konteksto_VALUE;
    br_sha256_init(&Konteksto_VALUE); br_sha256_update(&Konteksto_VALUE, data, haba_VALUE); br_sha256_out(&Konteksto_VALUE, sukat);
    memset(&Konteksto_VALUE, 0, sizeof(Konteksto_VALUE));
}
#define 난수저장기(posisyon) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(posisyon)))
int 원격난수(unsigned char *patutunguhan_VALUE,unsigned haba_VALUE){
    if(!seed_katayuan){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;seed_katayuan=2;}
        else {seed_katayuan=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(seed_katayuan==2){while(haba_VALUE){unsigned char Susunod_item[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;malayuan_buod(입력,33,Susunod_item);
        입력[32]=1;malayuan_buod(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=haba_VALUE<32?haba_VALUE:32;memcpy(patutunguhan_VALUE,Susunod_item,수);memset(Susunod_item,0,32);patutunguhan_VALUE+=수;haba_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(haba_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&haba_VALUE;순번++,haba_VALUE--){*patutunguhan_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
