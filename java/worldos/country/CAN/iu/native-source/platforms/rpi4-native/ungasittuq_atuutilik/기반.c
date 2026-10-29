/* kernel_atuutilik 전용 할당기와 isirut_atuutilik 난수 공급. atuqtuq ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct puigujjaikkut_sapummili { size_t takininga_atuutilik; struct puigujjaikkut_sapummili *다음; int 사용; } puigujjaikkut_sapummili;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static puigujjaikkut_sapummili *첫조각;
void *qumirrutigili_ungasittuq(size_t takininga_atuutilik) {
    if (!takininga_atuutilik || takininga_atuutilik>sizeof(기억터)-64) return 0;
    takininga_atuutilik=(takininga_atuutilik+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->takininga_atuutilik=sizeof(기억터)-32;}
    for(puigujjaikkut_sapummili *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->takininga_atuutilik>=takininga_atuutilik){
        if(조각->takininga_atuutilik>=takininga_atuutilik+64){puigujjaikkut_sapummili *새조각=(void*)((char*)조각+32+takininga_atuutilik);
            새조각->takininga_atuutilik=조각->takininga_atuutilik-takininga_atuutilik-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->takininga_atuutilik=takininga_atuutilik;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void anititaujuq_ungasittuq(void *turaarut) {
    if(!turaarut)return;puigujjaikkut_sapummili *조각=(void*)((char*)turaarut-32);
    volatile unsigned char *지움=turaarut;for(size_t 순번=0;순번<조각->takininga_atuutilik;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->takininga_atuutilik+=32+조각->다음->takininga_atuutilik;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *turaarut,size_t takininga_atuutilik){
    if(!turaarut)return qumirrutigili_ungasittuq(takininga_atuutilik);if(!takininga_atuutilik){anititaujuq_ungasittuq(turaarut);return 0;}
    puigujjaikkut_sapummili *조각=(void*)((char*)turaarut-32);void *새주소=qumirrutigili_ungasittuq(takininga_atuutilik);
    if(새주소){memcpy(새주소,turaarut,takininga_atuutilik<조각->takininga_atuutilik?takininga_atuutilik:조각->takininga_atuutilik);anititaujuq_ungasittuq(turaarut);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *말,int immikkuuqtuq_atuutilik){for(;;말++){if(*말==(char)immikkuuqtuq_atuutilik)return(char*)말;if(!*말)return 0;}}
char *strstr(const char *말,const char *찾음){size_t takininga_atuutilik=strlen(찾음);for(;*말;말++)if(!strncmp(말,찾음,takininga_atuutilik))return(char*)말;return takininga_atuutilik?0:(char*)말;}
char *strncpy(char *namunngarvik_atuutilik,const char *원본,size_t takininga_atuutilik){size_t 순번=0;for(;순번<takininga_atuutilik&&원본[순번];순번++)namunngarvik_atuutilik[순번]=원본[순번];for(;순번<takininga_atuutilik;순번++)namunngarvik_atuutilik[순번]=0;return namunngarvik_atuutilik;}
char *strncat(char *namunngarvik_atuutilik,const char *원본,size_t takininga_atuutilik){char *끝=namunngarvik_atuutilik+strlen(namunngarvik_atuutilik);while(takininga_atuutilik--&&*원본)*끝++=*원본++;*끝=0;return namunngarvik_atuutilik;}
int strncasecmp(const char *가,const char *나,size_t takininga_atuutilik){while(takininga_atuutilik--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *말,const char *isuaguurut_atuutilik,char **다음){if(!말)말=*다음;while(*말&&strchr(isuaguurut_atuutilik,*말))말++;if(!*말){*다음=말;return 0;}char *처음=말;while(*말&&!strchr(isuaguurut_atuutilik,*말))말++;if(*말)*말++=0;*다음=말;return 처음;}
unsigned long strtoul(const char *말, char **끝, int 밑) {
    const char *pivviujuq=말;unsigned long atuutilik=0;int 음수=0,tatattuq_atuutilik=0;
    while(*말==' '||(*말>=9&&*말<=13))말++;
    if(*말=='-'||*말=='+')음수=*말++=='-';
    if((밑==0||밑==16)&&말[0]=='0'&&(말[1]=='x'||말[1]=='X')&&
       ((말[2]>='0'&&말[2]<='9')||(말[2]>='a'&&말[2]<='f')||(말[2]>='A'&&말[2]<='F'))) {밑=16;말+=2;}
    if(!밑)밑=*말=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)pivviujuq;return 0;}
    const char *처음=말;
    for(;;말++) {
        unsigned immikkuuqtuq_atuutilik=(unsigned char)*말;
        unsigned 수=immikkuuqtuq_atuutilik>='0'&&immikkuuqtuq_atuutilik<='9'?immikkuuqtuq_atuutilik-'0':immikkuuqtuq_atuutilik>='a'&&immikkuuqtuq_atuutilik<='z'?immikkuuqtuq_atuutilik-'a'+10:immikkuuqtuq_atuutilik>='A'&&immikkuuqtuq_atuutilik<='Z'?immikkuuqtuq_atuutilik-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(atuutilik>(~0ul-수)/(unsigned)밑)tatattuq_atuutilik=1;
        if(!tatattuq_atuutilik)atuutilik=atuutilik*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(말==처음?pivviujuq:말);
    return tatattuq_atuutilik?~0ul:음수?0ul-atuutilik:atuutilik;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int 씨앗상태;
void ungasittuq_naiglitiqsimajuq(const void *titiqqat, size_t takininga_atuutilik, unsigned char 결과[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, titiqqat, takininga_atuutilik); br_sha256_out(&문맥, 결과);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(위치) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(위치)))
int 원격난수(unsigned char *namunngarvik_atuutilik,unsigned takininga_atuutilik){
    if(!씨앗상태){volatile unsigned char *titiqqat=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=titiqqat[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=titiqqat[8+순번];for(unsigned 순번=0;순번<40;순번++)titiqqat[순번]=0;씨앗상태=2;}
        else {씨앗상태=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(씨앗상태==2){while(takininga_atuutilik){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;ungasittuq_naiglitiqsimajuq(입력,33,다음);
        입력[32]=1;ungasittuq_naiglitiqsimajuq(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=takininga_atuutilik<32?takininga_atuutilik:32;memcpy(namunngarvik_atuutilik,다음,수);memset(다음,0,32);namunngarvik_atuutilik+=수;takininga_atuutilik-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(takininga_atuutilik){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t atuutilik=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&takininga_atuutilik;순번++,takininga_atuutilik--){*namunngarvik_atuutilik++=atuutilik&255;atuutilik>>=8;}}
    return 0;
}
