/* төш_VALUE 전용 할당기와 серсүз_VALUE 난수 공급. кулланучы ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Хәтер_тыю { size_t озынлык_VALUE; struct Хәтер_тыю *Киләсе_элемент; int 사용; } Хәтер_тыю;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static Хәтер_тыю *첫조각;
void *атап_бирү_читтәге(size_t озынлык_VALUE) {
    if (!озынлык_VALUE || озынлык_VALUE>sizeof(기억터)-64) return 0;
    озынлык_VALUE=(озынлык_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->озынлык_VALUE=sizeof(기억터)-32;}
    for(Хәтер_тыю *조각=첫조각;조각;조각=조각->Киләсе_элемент)if(!조각->사용&&조각->озынлык_VALUE>=озынлык_VALUE){
        if(조각->озынлык_VALUE>=озынлык_VALUE+64){Хәтер_тыю *새조각=(void*)((char*)조각+32+озынлык_VALUE);
            새조각->озынлык_VALUE=조각->озынлык_VALUE-озынлык_VALUE-32;새조각->Киләсе_элемент=조각->Киләсе_элемент;새조각->사용=0;조각->Киләсе_элемент=새조각;조각->озынлык_VALUE=озынлык_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void Чыгарылыш_читтәге(void *адрес) {
    if(!адрес)return;Хәтер_тыю *조각=(void*)((char*)адрес-32);
    volatile unsigned char *지움=адрес;for(size_t 순번=0;순번<조각->озынлык_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Киләсе_элемент;){if(!조각->사용&&!조각->Киләсе_элемент->사용){조각->озынлык_VALUE+=32+조각->Киләсе_элемент->озынлык_VALUE;조각->Киләсе_элемент=조각->Киләсе_элемент->Киләсе_элемент;}else 조각=조각->Киләсе_элемент;}
}
void *원격재할당(void *адрес,size_t озынлык_VALUE){
    if(!адрес)return атап_бирү_читтәге(озынлык_VALUE);if(!озынлык_VALUE){Чыгарылыш_читтәге(адрес);return 0;}
    Хәтер_тыю *조각=(void*)((char*)адрес-32);void *새주소=атап_бирү_читтәге(озынлык_VALUE);
    if(새주소){memcpy(새주소,адрес,озынлык_VALUE<조각->озынлык_VALUE?озынлык_VALUE:조각->озынлык_VALUE);Чыгарылыш_читтәге(адрес);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_СМС,int символ_VALUE_068c2631){for(;;Word_СМС++){if(*Word_СМС==(char)символ_VALUE_068c2631)return(char*)Word_СМС;if(!*Word_СМС)return 0;}}
char *strstr(const char *Word_СМС,const char *찾음){size_t озынлык_VALUE=strlen(찾음);for(;*Word_СМС;Word_СМС++)if(!strncmp(Word_СМС,찾음,озынлык_VALUE))return(char*)Word_СМС;return озынлык_VALUE?0:(char*)Word_СМС;}
char *strncpy(char *күчерү_урыны_VALUE,const char *원본,size_t озынлык_VALUE){size_t 순번=0;for(;순번<озынлык_VALUE&&원본[순번];순번++)күчерү_урыны_VALUE[순번]=원본[순번];for(;순번<озынлык_VALUE;순번++)күчерү_урыны_VALUE[순번]=0;return күчерү_урыны_VALUE;}
char *strncat(char *күчерү_урыны_VALUE,const char *원본,size_t озынлык_VALUE){char *끝=күчерү_урыны_VALUE+strlen(күчерү_урыны_VALUE);while(озынлык_VALUE--&&*원본)*끝++=*원본++;*끝=0;return күчерү_урыны_VALUE;}
int strncasecmp(const char *가,const char *나,size_t озынлык_VALUE){while(озынлык_VALUE--){unsigned 첫글자=*가++,SECOND_символ=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_символ>='A'&&SECOND_символ<='Z')SECOND_символ+=32;if(첫글자!=SECOND_символ)return(int)첫글자-(int)SECOND_символ;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_СМС,const char *аергыч_VALUE_d8ba4873,char **Киләсе_элемент){if(!Word_СМС)Word_СМС=*Киләсе_элемент;while(*Word_СМС&&strchr(аергыч_VALUE_d8ba4873,*Word_СМС))Word_СМС++;if(!*Word_СМС){*Киләсе_элемент=Word_СМС;return 0;}char *처음=Word_СМС;while(*Word_СМС&&!strchr(аергыч_VALUE_d8ba4873,*Word_СМС))Word_СМС++;if(*Word_СМС)*Word_СМС++=0;*Киләсе_элемент=Word_СМС;return 처음;}
unsigned long strtoul(const char *Word_СМС, char **끝, int BASE_VALUE) {
    const char *чыганак=Word_СМС;unsigned long VALUE=0;int 음수=0,сыешмау_VALUE=0;
    while(*Word_СМС==' '||(*Word_СМС>=9&&*Word_СМС<=13))Word_СМС++;
    if(*Word_СМС=='-'||*Word_СМС=='+')음수=*Word_СМС++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_СМС[0]=='0'&&(Word_СМС[1]=='x'||Word_СМС[1]=='X')&&
       ((Word_СМС[2]>='0'&&Word_СМС[2]<='9')||(Word_СМС[2]>='a'&&Word_СМС[2]<='f')||(Word_СМС[2]>='A'&&Word_СМС[2]<='F'))) {BASE_VALUE=16;Word_СМС+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_СМС=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)чыганак;return 0;}
    const char *처음=Word_СМС;
    for(;;Word_СМС++) {
        unsigned символ_VALUE_068c2631=(unsigned char)*Word_СМС;
        unsigned 수=символ_VALUE_068c2631>='0'&&символ_VALUE_068c2631<='9'?символ_VALUE_068c2631-'0':символ_VALUE_068c2631>='a'&&символ_VALUE_068c2631<='z'?символ_VALUE_068c2631-'a'+10:символ_VALUE_068c2631>='A'&&символ_VALUE_068c2631<='Z'?символ_VALUE_068c2631-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)сыешмау_VALUE=1;
        if(!сыешмау_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_СМС==처음?чыганак:Word_СМС);
    return сыешмау_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int Башланма_сан_халәт;
void читтәге_Җыелма_нәтиҗә(const void *мәгълүмат, size_t озынлык_VALUE, unsigned char үлчәм[32]) {
    br_sha256_context Контекст_VALUE;
    br_sha256_init(&Контекст_VALUE); br_sha256_update(&Контекст_VALUE, мәгълүмат, озынлык_VALUE); br_sha256_out(&Контекст_VALUE, үлчәм);
    memset(&Контекст_VALUE, 0, sizeof(Контекст_VALUE));
}
#define 난수저장기(урнаштыру) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(урнаштыру)))
int 원격난수(unsigned char *күчерү_урыны_VALUE,unsigned озынлык_VALUE){
    if(!Башланма_сан_халәт){volatile unsigned char *мәгълүмат=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=мәгълүмат[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=мәгълүмат[8+순번];for(unsigned 순번=0;순번<40;순번++)мәгълүмат[순번]=0;Башланма_сан_халәт=2;}
        else {Башланма_сан_халәт=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(Башланма_сан_халәт==2){while(озынлык_VALUE){unsigned char Киләсе_элемент[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;читтәге_Җыелма_нәтиҗә(입력,33,Киләсе_элемент);
        입력[32]=1;читтәге_Җыелма_нәтиҗә(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=озынлык_VALUE<32?озынлык_VALUE:32;memcpy(күчерү_урыны_VALUE,Киләсе_элемент,수);memset(Киләсе_элемент,0,32);күчерү_урыны_VALUE+=수;озынлык_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(озынлык_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&озынлык_VALUE;순번++,озынлык_VALUE--){*күчерү_урыны_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
