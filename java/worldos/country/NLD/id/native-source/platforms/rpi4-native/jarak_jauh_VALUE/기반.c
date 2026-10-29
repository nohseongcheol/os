/* kernel_VALUE 전용 할당기와 sandi_VALUE 난수 공급. ruang_pengguna ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memori_blok { size_t panjang_VALUE; struct Memori_blok *Berikutnya_item; int gunakan_VALUE; } Memori_blok;
static unsigned char Memori_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memori_blok *첫조각;
void *alokasi_jarak_jauh(size_t panjang_VALUE) {
    if (!panjang_VALUE || panjang_VALUE>sizeof(Memori_Arena)-64) return 0;
    panjang_VALUE=(panjang_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memori_Arena;첫조각->panjang_VALUE=sizeof(Memori_Arena)-32;}
    for(Memori_blok *조각=첫조각;조각;조각=조각->Berikutnya_item)if(!조각->gunakan_VALUE&&조각->panjang_VALUE>=panjang_VALUE){
        if(조각->panjang_VALUE>=panjang_VALUE+64){Memori_blok *새조각=(void*)((char*)조각+32+panjang_VALUE);
            새조각->panjang_VALUE=조각->panjang_VALUE-panjang_VALUE-32;새조각->Berikutnya_item=조각->Berikutnya_item;새조각->gunakan_VALUE=0;조각->Berikutnya_item=새조각;조각->panjang_VALUE=panjang_VALUE;}
        조각->gunakan_VALUE=1;return(char*)조각+32;
    }return 0;
}
void lepas_jarak_jauh(void *surel) {
    if(!surel)return;Memori_blok *조각=(void*)((char*)surel-32);
    volatile unsigned char *지움=surel;for(size_t 순번=0;순번<조각->panjang_VALUE;순번++)지움[순번]=0;
    조각->gunakan_VALUE=0;
    for(조각=첫조각;조각&&조각->Berikutnya_item;){if(!조각->gunakan_VALUE&&!조각->Berikutnya_item->gunakan_VALUE){조각->panjang_VALUE+=32+조각->Berikutnya_item->panjang_VALUE;조각->Berikutnya_item=조각->Berikutnya_item->Berikutnya_item;}else 조각=조각->Berikutnya_item;}
}
void *원격재할당(void *surel,size_t panjang_VALUE){
    if(!surel)return alokasi_jarak_jauh(panjang_VALUE);if(!panjang_VALUE){lepas_jarak_jauh(surel);return 0;}
    Memori_blok *조각=(void*)((char*)surel-32);void *새주소=alokasi_jarak_jauh(panjang_VALUE);
    if(새주소){memcpy(새주소,surel,panjang_VALUE<조각->panjang_VALUE?panjang_VALUE:조각->panjang_VALUE);lepas_jarak_jauh(surel);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operand){while(*가&&*가==*SECOND_operand){가++;SECOND_operand++;}return(unsigned char)*가-(unsigned char)*SECOND_operand;}
char *strchr(const char *Kata_SMS,int karakter_VALUE){for(;;Kata_SMS++){if(*Kata_SMS==(char)karakter_VALUE)return(char*)Kata_SMS;if(!*Kata_SMS)return 0;}}
char *strstr(const char *Kata_SMS,const char *찾음){size_t panjang_VALUE=strlen(찾음);for(;*Kata_SMS;Kata_SMS++)if(!strncmp(Kata_SMS,찾음,panjang_VALUE))return(char*)Kata_SMS;return panjang_VALUE?0:(char*)Kata_SMS;}
char *strncpy(char *tujuan_VALUE,const char *원본,size_t panjang_VALUE){size_t 순번=0;for(;순번<panjang_VALUE&&원본[순번];순번++)tujuan_VALUE[순번]=원본[순번];for(;순번<panjang_VALUE;순번++)tujuan_VALUE[순번]=0;return tujuan_VALUE;}
char *strncat(char *tujuan_VALUE,const char *원본,size_t panjang_VALUE){char *끝=tujuan_VALUE+strlen(tujuan_VALUE);while(panjang_VALUE--&&*원본)*끝++=*원본++;*끝=0;return tujuan_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operand,size_t panjang_VALUE){while(panjang_VALUE--){unsigned 첫글자=*가++,SECOND_karakter=*SECOND_operand++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_karakter>='A'&&SECOND_karakter<='Z')SECOND_karakter+=32;if(첫글자!=SECOND_karakter)return(int)첫글자-(int)SECOND_karakter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operand){return strncasecmp(가,SECOND_operand,(size_t)-1);}
char *strtok_r(char *Kata_SMS,const char *pemisah_VALUE_d8ba4873,char **Berikutnya_item){if(!Kata_SMS)Kata_SMS=*Berikutnya_item;while(*Kata_SMS&&strchr(pemisah_VALUE_d8ba4873,*Kata_SMS))Kata_SMS++;if(!*Kata_SMS){*Berikutnya_item=Kata_SMS;return 0;}char *처음=Kata_SMS;while(*Kata_SMS&&!strchr(pemisah_VALUE_d8ba4873,*Kata_SMS))Kata_SMS++;if(*Kata_SMS)*Kata_SMS++=0;*Berikutnya_item=Kata_SMS;return 처음;}
unsigned long strtoul(const char *Kata_SMS, char **끝, int BASE_VALUE) {
    const char *kodeSumber=Kata_SMS;unsigned long VALUE=0;int 음수=0,luapan_VALUE=0;
    while(*Kata_SMS==' '||(*Kata_SMS>=9&&*Kata_SMS<=13))Kata_SMS++;
    if(*Kata_SMS=='-'||*Kata_SMS=='+')음수=*Kata_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Kata_SMS[0]=='0'&&(Kata_SMS[1]=='x'||Kata_SMS[1]=='X')&&
       ((Kata_SMS[2]>='0'&&Kata_SMS[2]<='9')||(Kata_SMS[2]>='a'&&Kata_SMS[2]<='f')||(Kata_SMS[2]>='A'&&Kata_SMS[2]<='F'))) {BASE_VALUE=16;Kata_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Kata_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)kodeSumber;return 0;}
    const char *처음=Kata_SMS;
    for(;;Kata_SMS++) {
        unsigned karakter_VALUE=(unsigned char)*Kata_SMS;
        unsigned 수=karakter_VALUE>='0'&&karakter_VALUE<='9'?karakter_VALUE-'0':karakter_VALUE>='a'&&karakter_VALUE<='z'?karakter_VALUE-'a'+10:karakter_VALUE>='A'&&karakter_VALUE<='Z'?karakter_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)luapan_VALUE=1;
        if(!luapan_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Kata_SMS==처음?kodeSumber:Kata_SMS);
    return luapan_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int seed_Status;
void jarak_jauh_ringkasan(const void *data, size_t panjang_VALUE, unsigned char hasil[32]) {
    br_sha256_context 문맥;
    br_sha256_init(&문맥); br_sha256_update(&문맥, data, panjang_VALUE); br_sha256_out(&문맥, hasil);
    memset(&문맥, 0, sizeof(문맥));
}
#define 난수저장기(posisi) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(posisi)))
int jarak_jauh_acak(unsigned char *tujuan_VALUE,unsigned panjang_VALUE){
    if(!seed_Status){volatile unsigned char *data=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;seed_Status=2;}
        else {seed_Status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(seed_Status==2){while(panjang_VALUE){unsigned char Berikutnya_item[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;jarak_jauh_ringkasan(입력,33,Berikutnya_item);
        입력[32]=1;jarak_jauh_ringkasan(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=panjang_VALUE<32?panjang_VALUE:32;memcpy(tujuan_VALUE,Berikutnya_item,수);memset(Berikutnya_item,0,32);tujuan_VALUE+=수;panjang_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(panjang_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&panjang_VALUE;순번++,panjang_VALUE--){*tujuan_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
