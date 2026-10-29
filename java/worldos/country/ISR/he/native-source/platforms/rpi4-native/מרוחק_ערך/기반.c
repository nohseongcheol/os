/* ליבה_ערך 전용 할당기와 סיסמה_ערך 난수 공급. משתמש ELF의 libc와 별개이다. */
#include "קריפטוגרפיה_תמך.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct זיכרון_בלוק { size_t 길이; struct זיכרון_בלוק *הבא_פריט; int שימוש_ערך; } זיכרון_בלוק;
static unsigned char זיכרון_זירה[2*1024*1024] __attribute__((aligned(16)));
static זיכרון_בלוק *첫조각;
void *הקצה_מרוחק(size_t 길이) {
    if (!길이 || 길이>sizeof(זיכרון_זירה)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)זיכרון_זירה;첫조각->길이=sizeof(זיכרון_זירה)-32;}
    for(זיכרון_בלוק *조각=첫조각;조각;조각=조각->הבא_פריט)if(!조각->שימוש_ערך&&조각->길이>=길이){
        if(조각->길이>=길이+64){זיכרון_בלוק *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->הבא_פריט=조각->הבא_פריט;새조각->שימוש_ערך=0;조각->הבא_פריט=새조각;조각->길이=길이;}
        조각->שימוש_ערך=1;return(char*)조각+32;
    }return 0;
}
void לשחרר_מרוחק(void *למען) {
    if(!למען)return;זיכרון_בלוק *조각=(void*)((char*)למען-32);
    volatile unsigned char *지움=למען;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->שימוש_ערך=0;
    for(조각=첫조각;조각&&조각->הבא_פריט;){if(!조각->שימוש_ערך&&!조각->הבא_פריט->שימוש_ערך){조각->길이+=32+조각->הבא_פריט->길이;조각->הבא_פריט=조각->הבא_פריט->הבא_פריט;}else 조각=조각->הבא_פריט;}
}
void *원격재할당(void *למען,size_t 길이){
    if(!למען)return הקצה_מרוחק(길이);if(!길이){לשחרר_מרוחק(למען);return 0;}
    זיכרון_בלוק *조각=(void*)((char*)למען-32);void *새주소=הקצה_מרוחק(길이);
    if(새주소){memcpy(새주소,למען,길이<조각->길이?길이:조각->길이);לשחרר_מרוחק(למען);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *מילים_טקסט,int תו_ערך){for(;;מילים_טקסט++){if(*מילים_טקסט==(char)תו_ערך)return(char*)מילים_טקסט;if(!*מילים_טקסט)return 0;}}
char *strstr(const char *מילים_טקסט,const char *찾음){size_t 길이=strlen(찾음);for(;*מילים_טקסט;מילים_טקסט++)if(!strncmp(מילים_טקסט,찾음,길이))return(char*)מילים_טקסט;return 길이?0:(char*)מילים_טקסט;}
char *strncpy(char *יעד_ערך,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)יעד_ערך[순번]=원본[순번];for(;순번<길이;순번++)יעד_ערך[순번]=0;return יעד_ערך;}
char *strncat(char *יעד_ערך,const char *원본,size_t 길이){char *끝=יעד_ערך+strlen(יעד_ערך);while(길이--&&*원본)*끝++=*원본++;*끝=0;return יעד_ערך;}
int strncasecmp(const char *가,const char *나,size_t 길이){while(길이--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *מילים_טקסט,const char *מפריד_ערך_d8ba4873,char **הבא_פריט){if(!מילים_טקסט)מילים_טקסט=*הבא_פריט;while(*מילים_טקסט&&strchr(מפריד_ערך_d8ba4873,*מילים_טקסט))מילים_טקסט++;if(!*מילים_טקסט){*הבא_פריט=מילים_טקסט;return 0;}char *처음=מילים_טקסט;while(*מילים_טקסט&&!strchr(מפריד_ערך_d8ba4873,*מילים_טקסט))מילים_טקסט++;if(*מילים_טקסט)*מילים_טקסט++=0;*הבא_פריט=מילים_טקסט;return 처음;}
unsigned long strtoul(const char *מילים_טקסט, char **끝, int 밑) {
    const char *קודמקור=מילים_טקסט;unsigned long ערך=0;int 음수=0,גלישה_ערך=0;
    while(*מילים_טקסט==' '||(*מילים_טקסט>=9&&*מילים_טקסט<=13))מילים_טקסט++;
    if(*מילים_טקסט=='-'||*מילים_טקסט=='+')음수=*מילים_טקסט++=='-';
    if((밑==0||밑==16)&&מילים_טקסט[0]=='0'&&(מילים_טקסט[1]=='x'||מילים_טקסט[1]=='X')&&
       ((מילים_טקסט[2]>='0'&&מילים_טקסט[2]<='9')||(מילים_טקסט[2]>='a'&&מילים_טקסט[2]<='f')||(מילים_טקסט[2]>='A'&&מילים_טקסט[2]<='F'))) {밑=16;מילים_טקסט+=2;}
    if(!밑)밑=*מילים_טקסט=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)קודמקור;return 0;}
    const char *처음=מילים_טקסט;
    for(;;מילים_טקסט++) {
        unsigned תו_ערך=(unsigned char)*מילים_טקסט;
        unsigned 수=תו_ערך>='0'&&תו_ערך<='9'?תו_ערך-'0':תו_ערך>='a'&&תו_ערך<='z'?תו_ערך-'a'+10:תו_ערך>='A'&&תו_ערך<='Z'?תו_ערך-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(ערך>(~0ul-수)/(unsigned)밑)גלישה_ערך=1;
        if(!גלישה_ערך)ערך=ערך*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(מילים_טקסט==처음?קודמקור:מילים_טקסט);
    return גלישה_ערך?~0ul:음수?0ul-ערך:ערך;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int זרע_מצב;
void מרוחק_סיכום(const void *נתונים, size_t 길이, unsigned char תוצאה[32]) {
    br_sha256_context הקשר_ערך;
    br_sha256_init(&הקשר_ערך); br_sha256_update(&הקשר_ערך, נתונים, 길이); br_sha256_out(&הקשר_ערך, תוצאה);
    memset(&הקשר_ערך, 0, sizeof(הקשר_ערך));
}
#define 난수저장기(מיקום) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(מיקום)))
int 원격난수(unsigned char *יעד_ערך,unsigned 길이){
    if(!זרע_מצב){volatile unsigned char *נתונים=(void*)0x01ff0000ul;const char *סמן_ערך="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=נתונים[순번]^(unsigned char)סמן_ערך[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=נתונים[8+순번];for(unsigned 순번=0;순번<40;순번++)נתונים[순번]=0;זרע_מצב=2;}
        else {זרע_מצב=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(זרע_מצב==2){while(길이){unsigned char הבא_פריט[32],קלט_ערך[33];memcpy(קלט_ערך,모의씨앗,32);קלט_ערך[32]=0;מרוחק_סיכום(קלט_ערך,33,הבא_פריט);
        קלט_ערך[32]=1;מרוחק_סיכום(קלט_ערך,33,모의씨앗);memset(קלט_ערך,0,33);
        unsigned 수=길이<32?길이:32;memcpy(יעד_ערך,הבא_פריט,수);memset(הבא_פריט,0,32);יעד_ערך+=수;길이-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t ערך=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*יעד_ערך++=ערך&255;ערך>>=8;}}
    return 0;
}
