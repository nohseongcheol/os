/* o_zak_VALUE 전용 할당기와 parol_VALUE 난수 공급. foydalanuvchi ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Xotira_bloklash { size_t uzunlik_VALUE; struct Xotira_bloklash *Keyingi_element; int 사용; } Xotira_bloklash;
static unsigned char Xotira_Arena[2*1024*1024] __attribute__((aligned(16)));
static Xotira_bloklash *첫조각;
void *joylashtirmoq_masofaviy(size_t uzunlik_VALUE) {
    if (!uzunlik_VALUE || uzunlik_VALUE>sizeof(Xotira_Arena)-64) return 0;
    uzunlik_VALUE=(uzunlik_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Xotira_Arena;첫조각->uzunlik_VALUE=sizeof(Xotira_Arena)-32;}
    for(Xotira_bloklash *조각=첫조각;조각;조각=조각->Keyingi_element)if(!조각->사용&&조각->uzunlik_VALUE>=uzunlik_VALUE){
        if(조각->uzunlik_VALUE>=uzunlik_VALUE+64){Xotira_bloklash *새조각=(void*)((char*)조각+32+uzunlik_VALUE);
            새조각->uzunlik_VALUE=조각->uzunlik_VALUE-uzunlik_VALUE-32;새조각->Keyingi_element=조각->Keyingi_element;새조각->사용=0;조각->Keyingi_element=새조각;조각->uzunlik_VALUE=uzunlik_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void nashr_masofaviy(void *manzil) {
    if(!manzil)return;Xotira_bloklash *조각=(void*)((char*)manzil-32);
    volatile unsigned char *지움=manzil;for(size_t 순번=0;순번<조각->uzunlik_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Keyingi_element;){if(!조각->사용&&!조각->Keyingi_element->사용){조각->uzunlik_VALUE+=32+조각->Keyingi_element->uzunlik_VALUE;조각->Keyingi_element=조각->Keyingi_element->Keyingi_element;}else 조각=조각->Keyingi_element;}
}
void *원격재할당(void *manzil,size_t uzunlik_VALUE){
    if(!manzil)return joylashtirmoq_masofaviy(uzunlik_VALUE);if(!uzunlik_VALUE){nashr_masofaviy(manzil);return 0;}
    Xotira_bloklash *조각=(void*)((char*)manzil-32);void *새주소=joylashtirmoq_masofaviy(uzunlik_VALUE);
    if(새주소){memcpy(새주소,manzil,uzunlik_VALUE<조각->uzunlik_VALUE?uzunlik_VALUE:조각->uzunlik_VALUE);nashr_masofaviy(manzil);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int belgi_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)belgi_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t uzunlik_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,uzunlik_VALUE))return(char*)Word_SMS;return uzunlik_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *ko_chirish_joyi_VALUE,const char *원본,size_t uzunlik_VALUE){size_t 순번=0;for(;순번<uzunlik_VALUE&&원본[순번];순번++)ko_chirish_joyi_VALUE[순번]=원본[순번];for(;순번<uzunlik_VALUE;순번++)ko_chirish_joyi_VALUE[순번]=0;return ko_chirish_joyi_VALUE;}
char *strncat(char *ko_chirish_joyi_VALUE,const char *원본,size_t uzunlik_VALUE){char *끝=ko_chirish_joyi_VALUE+strlen(ko_chirish_joyi_VALUE);while(uzunlik_VALUE--&&*원본)*끝++=*원본++;*끝=0;return ko_chirish_joyi_VALUE;}
int strncasecmp(const char *가,const char *나,size_t uzunlik_VALUE){while(uzunlik_VALUE--){unsigned 첫글자=*가++,SECOND_belgi=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_belgi>='A'&&SECOND_belgi<='Z')SECOND_belgi+=32;if(첫글자!=SECOND_belgi)return(int)첫글자-(int)SECOND_belgi;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *ajratuvchi_VALUE,char **Keyingi_element){if(!Word_SMS)Word_SMS=*Keyingi_element;while(*Word_SMS&&strchr(ajratuvchi_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Keyingi_element=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(ajratuvchi_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Keyingi_element=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *manba=Word_SMS;unsigned long VALUE=0;int 음수=0,to_lib_ketish_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)manba;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned belgi_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=belgi_VALUE>='0'&&belgi_VALUE<='9'?belgi_VALUE-'0':belgi_VALUE>='a'&&belgi_VALUE<='z'?belgi_VALUE-'a'+10:belgi_VALUE>='A'&&belgi_VALUE<='Z'?belgi_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)to_lib_ketish_VALUE=1;
        if(!to_lib_ketish_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?manba:Word_SMS);
    return to_lib_ketish_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int quvvatlash_holat;
void masofaviy_xulosa(const void *ma_lumotlar, size_t uzunlik_VALUE, unsigned char o_lchov[32]) {
    br_sha256_context Kontekst_VALUE;
    br_sha256_init(&Kontekst_VALUE); br_sha256_update(&Kontekst_VALUE, ma_lumotlar, uzunlik_VALUE); br_sha256_out(&Kontekst_VALUE, o_lchov);
    memset(&Kontekst_VALUE, 0, sizeof(Kontekst_VALUE));
}
#define 난수저장기(Holati) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Holati)))
int 원격난수(unsigned char *ko_chirish_joyi_VALUE,unsigned uzunlik_VALUE){
    if(!quvvatlash_holat){volatile unsigned char *ma_lumotlar=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=ma_lumotlar[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=ma_lumotlar[8+순번];for(unsigned 순번=0;순번<40;순번++)ma_lumotlar[순번]=0;quvvatlash_holat=2;}
        else {quvvatlash_holat=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(quvvatlash_holat==2){while(uzunlik_VALUE){unsigned char Keyingi_element[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;masofaviy_xulosa(입력,33,Keyingi_element);
        입력[32]=1;masofaviy_xulosa(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=uzunlik_VALUE<32?uzunlik_VALUE:32;memcpy(ko_chirish_joyi_VALUE,Keyingi_element,수);memset(Keyingi_element,0,32);ko_chirish_joyi_VALUE+=수;uzunlik_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(uzunlik_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&uzunlik_VALUE;순번++,uzunlik_VALUE--){*ko_chirish_joyi_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
