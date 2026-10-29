/* kernel_VALUE 전용 할당기와 kata_laluan_VALUE 난수 공급. ruang_pengguna ELF의 libc와 별개이다. */
#include "kriptografi_Sokongan.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Memori_blok { size_t kepanjangan_VALUE; struct Memori_blok *Seterusnya_item; int 사용; } Memori_blok;
static unsigned char Memori_Arena[2*1024*1024] __attribute__((aligned(16)));
static Memori_blok *첫조각;
void *peruntuk_jauh(size_t kepanjangan_VALUE) {
    if (!kepanjangan_VALUE || kepanjangan_VALUE>sizeof(Memori_Arena)-64) return 0;
    kepanjangan_VALUE=(kepanjangan_VALUE+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Memori_Arena;첫조각->kepanjangan_VALUE=sizeof(Memori_Arena)-32;}
    for(Memori_blok *조각=첫조각;조각;조각=조각->Seterusnya_item)if(!조각->사용&&조각->kepanjangan_VALUE>=kepanjangan_VALUE){
        if(조각->kepanjangan_VALUE>=kepanjangan_VALUE+64){Memori_blok *새조각=(void*)((char*)조각+32+kepanjangan_VALUE);
            새조각->kepanjangan_VALUE=조각->kepanjangan_VALUE-kepanjangan_VALUE-32;새조각->Seterusnya_item=조각->Seterusnya_item;새조각->사용=0;조각->Seterusnya_item=새조각;조각->kepanjangan_VALUE=kepanjangan_VALUE;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void keluaran_jauh(void *e_mel) {
    if(!e_mel)return;Memori_blok *조각=(void*)((char*)e_mel-32);
    volatile unsigned char *지움=e_mel;for(size_t 순번=0;순번<조각->kepanjangan_VALUE;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->Seterusnya_item;){if(!조각->사용&&!조각->Seterusnya_item->사용){조각->kepanjangan_VALUE+=32+조각->Seterusnya_item->kepanjangan_VALUE;조각->Seterusnya_item=조각->Seterusnya_item->Seterusnya_item;}else 조각=조각->Seterusnya_item;}
}
void *원격재할당(void *e_mel,size_t kepanjangan_VALUE){
    if(!e_mel)return peruntuk_jauh(kepanjangan_VALUE);if(!kepanjangan_VALUE){keluaran_jauh(e_mel);return 0;}
    Memori_blok *조각=(void*)((char*)e_mel-32);void *새주소=peruntuk_jauh(kepanjangan_VALUE);
    if(새주소){memcpy(새주소,e_mel,kepanjangan_VALUE<조각->kepanjangan_VALUE?kepanjangan_VALUE:조각->kepanjangan_VALUE);keluaran_jauh(e_mel);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *Word_SMS,int aksara_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)aksara_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t kepanjangan_VALUE=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,kepanjangan_VALUE))return(char*)Word_SMS;return kepanjangan_VALUE?0:(char*)Word_SMS;}
char *strncpy(char *destinasi_VALUE,const char *원본,size_t kepanjangan_VALUE){size_t 순번=0;for(;순번<kepanjangan_VALUE&&원본[순번];순번++)destinasi_VALUE[순번]=원본[순번];for(;순번<kepanjangan_VALUE;순번++)destinasi_VALUE[순번]=0;return destinasi_VALUE;}
char *strncat(char *destinasi_VALUE,const char *원본,size_t kepanjangan_VALUE){char *끝=destinasi_VALUE+strlen(destinasi_VALUE);while(kepanjangan_VALUE--&&*원본)*끝++=*원본++;*끝=0;return destinasi_VALUE;}
int strncasecmp(const char *가,const char *나,size_t kepanjangan_VALUE){while(kepanjangan_VALUE--){unsigned 첫글자=*가++,SECOND_aksara=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_aksara>='A'&&SECOND_aksara<='Z')SECOND_aksara+=32;if(첫글자!=SECOND_aksara)return(int)첫글자-(int)SECOND_aksara;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *pembatas_VALUE,char **Seterusnya_item){if(!Word_SMS)Word_SMS=*Seterusnya_item;while(*Word_SMS&&strchr(pembatas_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Seterusnya_item=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(pembatas_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Seterusnya_item=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *SUMBER=Word_SMS;unsigned long VALUE=0;int 음수=0,limpahan_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)SUMBER;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned aksara_VALUE=(unsigned char)*Word_SMS;
        unsigned 수=aksara_VALUE>='0'&&aksara_VALUE<='9'?aksara_VALUE-'0':aksara_VALUE>='a'&&aksara_VALUE<='z'?aksara_VALUE-'a'+10:aksara_VALUE>='A'&&aksara_VALUE<='Z'?aksara_VALUE-'A'+10:36;
        if(수>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-수)/(unsigned)BASE_VALUE)limpahan_VALUE=1;
        if(!limpahan_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?SUMBER:Word_SMS);
    return limpahan_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int semai_status;
void jauh_ringkasan(const void *data, size_t kepanjangan_VALUE, unsigned char ukuran[32]) {
    br_sha256_context konteks_VALUE;
    br_sha256_init(&konteks_VALUE); br_sha256_update(&konteks_VALUE, data, kepanjangan_VALUE); br_sha256_out(&konteks_VALUE, ukuran);
    memset(&konteks_VALUE, 0, sizeof(konteks_VALUE));
}
#define 난수저장기(Kedudukan) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Kedudukan)))
int jauh_rawak(unsigned char *destinasi_VALUE,unsigned kepanjangan_VALUE){
    if(!semai_status){volatile unsigned char *data=(void*)0x01ff0000ul;const char *penanda_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=data[순번]^(unsigned char)penanda_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=data[8+순번];for(unsigned 순번=0;순번<40;순번++)data[순번]=0;semai_status=2;}
        else {semai_status=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(semai_status==2){while(kepanjangan_VALUE){unsigned char Seterusnya_item[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;jauh_ringkasan(입력,33,Seterusnya_item);
        입력[32]=1;jauh_ringkasan(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=kepanjangan_VALUE<32?kepanjangan_VALUE:32;memcpy(destinasi_VALUE,Seterusnya_item,수);memset(Seterusnya_item,0,32);destinasi_VALUE+=수;kepanjangan_VALUE-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(kepanjangan_VALUE){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&kepanjangan_VALUE;순번++,kepanjangan_VALUE--){*destinasi_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
