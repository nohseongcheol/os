/* kern_VALUE 전용 할당기와 wagwoord_VALUE 난수 공급. gebruiker ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Geheue_blokkeer { size_t lengte_VALUE; struct Geheue_blokkeer *Volgende_item; int 사용; } Geheue_blokkeer;
static unsigned char Geheue_Arena[2*1024*1024] __attribute__((aligned(16)));
static Geheue_blokkeer *첫조각;
void *toewys_afstands(size_t lengte_VALUE) {
    if (!lengte_VALUE || lengte_VALUE>sizeof(Geheue_Arena)-64) return 0;
    lengte_VALUE=(lengte_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Geheue_Arena;첫조각->lengte_VALUE=sizeof(Geheue_Arena)-32;}
    for(Geheue_blokkeer *조각=첫조각;조각;조각=조각->Volgende_item)if(!조각->사용&&조각->lengte_VALUE>=lengte_VALUE){
        if(조각->lengte_VALUE>=lengte_VALUE+64){Geheue_blokkeer *새조각=(void*)((char*)조각+32+lengte_VALUE);
            새조각->lengte_VALUE=조각->lengte_VALUE-lengte_VALUE-32;새조각->Volgende_item=조각->Volgende_item;새조각->사용=0;조각->Volgende_item=새조각;조각->lengte_VALUE=lengte_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void stel_vry_afstands(void *adres) {
    if(!adres)return;Geheue_blokkeer *조각=(void*)((char*)adres-32);
    volatile unsigned char *지움=adres;for(size_t 순번=0;순번<조각->lengte_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Volgende_item;){if(!조각->사용&&!조각->Volgende_item->사용){조각->lengte_VALUE+=32+조각->Volgende_item->lengte_VALUE;조각->Volgende_item=조각->Volgende_item->Volgende_item;}else 조각=조각->Volgende_item;}
}
void *원격재할당(void *adres,size_t lengte_VALUE){
    if(!adres)return toewys_afstands(lengte_VALUE);if(!lengte_VALUE){stel_vry_afstands(adres);return 0;}
    Geheue_blokkeer *조각=(void*)((char*)adres-32);void *새주소=toewys_afstands(lengte_VALUE);
    if(새주소){memcpy(새주소,adres,lengte_VALUE<조각->lengte_VALUE?lengte_VALUE:조각->lengte_VALUE);stel_vry_afstands(adres);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int karakter_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)karakter_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t lengte_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,lengte_VALUE))return(char*)Word_SMS;return lengte_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *bestemming_VALUE,const char *원본,size_t lengte_VALUE){size_t 순번=0;for(;순번<lengte_VALUE&&원본[순번];순번++)bestemming_VALUE[순번]=원본[순번];for(;순번<lengte_VALUE;순번++)bestemming_VALUE[순번]=0;return bestemming_VALUE;}
char *strncat(char *bestemming_VALUE,const char *원본,size_t lengte_VALUE){char *끝=bestemming_VALUE+strlen(bestemming_VALUE);while(lengte_VALUE--&&*원본)*끝++=*원본++;*끝=0;return bestemming_VALUE;}
int strncasecmp(const char *가,const char *나,size_t lengte_VALUE){while(lengte_VALUE--){unsigned 첫글자=*가++,SECOND_karakter=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_karakter>='A'&&SECOND_karakter<='Z')SECOND_karakter+=32;if(첫글자!=SECOND_karakter)return(int)첫글자-(int)SECOND_karakter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *skeier_VALUE,char **Volgende_item){if(!Word_SMS)Word_SMS=*Volgende_item;while(*Word_SMS&&strchr(skeier_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Volgende_item=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(skeier_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Volgende_item=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *Bron=Word_SMS;unsigned long VALUE=0;int 음수=0,oorloop_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)Bron;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned karakter_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=karakter_VALUE>='0'&&karakter_VALUE<='9'?karakter_VALUE-'0':karakter_VALUE>='a'&&karakter_VALUE<='z'?karakter_VALUE-'a'+10:karakter_VALUE>='A'&&karakter_VALUE<='Z'?karakter_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)oorloop_VALUE=1;
        if(!oorloop_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?Bron:Word_SMS);
    return oorloop_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int voorsien_stand;
void 원격요약(const void *data, size_t lengte_VALUE, unsigned char maatreël[32]) {
    br_sha256_context Konteks_VALUE;
    br_sha256_init(&Konteks_VALUE); br_sha256_update(&Konteks_VALUE, data, lengte_VALUE); br_sha256_out(&Konteks_VALUE, maatreël);
    memset(&Konteks_VALUE, 0, sizeof(Konteks_VALUE));
}
#define 난수저장기(Posisie) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Posisie)))
int 원격난수(unsigned char *bestemming_VALUE,unsigned lengte_VALUE){
    if(!voorsien_stand){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;voorsien_stand=2;}
        else {voorsien_stand=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(voorsien_stand==2){while(lengte_VALUE){unsigned char Volgende_item[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;원격요약(입력,33,Volgende_item);
        입력[32]=1;원격요약(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=lengte_VALUE<32?lengte_VALUE:32;memcpy(bestemming_VALUE,Volgende_item,수);memset(Volgende_item,0,32);bestemming_VALUE+=수;lengte_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(lengte_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&lengte_VALUE;순번++,lengte_VALUE--){*bestemming_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
