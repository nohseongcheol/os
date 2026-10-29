/* çekirdek_değer 전용 할당기와 parola_değer 난수 공급. kullanıcı_alanı ELF의 libc와 별개이다. */
#include "şifreleme_Destek.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct Bellek_blok { size_t süre_değer; struct Bellek_blok *Sonraki_öğe; int kullanmak_değer; } Bellek_blok;
static unsigned char Bellek_Alan[2*1024*1024] __attribute__((aligned(16)));
static Bellek_blok *첫조각;
void *ayırmak_uzak(size_t süre_değer) {
    if (!süre_değer || süre_değer>sizeof(Bellek_Alan)-64) return 0;
    süre_değer=(süre_değer+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)Bellek_Alan;첫조각->süre_değer=sizeof(Bellek_Alan)-32;}
    for(Bellek_blok *parça_değer=첫조각;parça_değer;parça_değer=parça_değer->Sonraki_öğe)if(!parça_değer->kullanmak_değer&&parça_değer->süre_değer>=süre_değer){
        if(parça_değer->süre_değer>=süre_değer+64){Bellek_blok *새조각=(void*)((char*)parça_değer+32+süre_değer);
            새조각->süre_değer=parça_değer->süre_değer-süre_değer-32;새조각->Sonraki_öğe=parça_değer->Sonraki_öğe;새조각->kullanmak_değer=0;parça_değer->Sonraki_öğe=새조각;parça_değer->süre_değer=süre_değer;}
        parça_değer->kullanmak_değer=1;return(char*)parça_değer+32;
    }return 0;
}
void sürüm_uzak(void *ADRES) {
    if(!ADRES)return;Bellek_blok *parça_değer=(void*)((char*)ADRES-32);
    volatile unsigned char *지움=ADRES;for(size_t 순번=0;순번<parça_değer->süre_değer;순번++)지움[순번]=0;
    parça_değer->kullanmak_değer=0;
    for(parça_değer=첫조각;parça_değer&&parça_değer->Sonraki_öğe;){if(!parça_değer->kullanmak_değer&&!parça_değer->Sonraki_öğe->kullanmak_değer){parça_değer->süre_değer+=32+parça_değer->Sonraki_öğe->süre_değer;parça_değer->Sonraki_öğe=parça_değer->Sonraki_öğe->Sonraki_öğe;}else parça_değer=parça_değer->Sonraki_öğe;}
}
void *원격재할당(void *ADRES,size_t süre_değer){
    if(!ADRES)return ayırmak_uzak(süre_değer);if(!süre_değer){sürüm_uzak(ADRES);return 0;}
    Bellek_blok *parça_değer=(void*)((char*)ADRES-32);void *새주소=ayırmak_uzak(süre_değer);
    if(새주소){memcpy(새주소,ADRES,süre_değer<parça_değer->süre_değer?süre_değer:parça_değer->süre_değer);sürüm_uzak(ADRES);}return 새주소;
}
int strcmp(const char *가,const char *SANİYE_işlenen){while(*가&&*가==*SANİYE_işlenen){가++;SANİYE_işlenen++;}return(unsigned char)*가-(unsigned char)*SANİYE_işlenen;}
char *strchr(const char *Word_SMS,int karakter_değer){for(;;Word_SMS++){if(*Word_SMS==(char)karakter_değer)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t süre_değer=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,süre_değer))return(char*)Word_SMS;return süre_değer?0:(char*)Word_SMS;}
char *strncpy(char *hedef_değer,const char *원본,size_t süre_değer){size_t 순번=0;for(;순번<süre_değer&&원본[순번];순번++)hedef_değer[순번]=원본[순번];for(;순번<süre_değer;순번++)hedef_değer[순번]=0;return hedef_değer;}
char *strncat(char *hedef_değer,const char *원본,size_t süre_değer){char *끝=hedef_değer+strlen(hedef_değer);while(süre_değer--&&*원본)*끝++=*원본++;*끝=0;return hedef_değer;}
int strncasecmp(const char *가,const char *SANİYE_işlenen,size_t süre_değer){while(süre_değer--){unsigned 첫글자=*가++,SANİYE_karakter=*SANİYE_işlenen++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SANİYE_karakter>='A'&&SANİYE_karakter<='Z')SANİYE_karakter+=32;if(첫글자!=SANİYE_karakter)return(int)첫글자-(int)SANİYE_karakter;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SANİYE_işlenen){return strncasecmp(가,SANİYE_işlenen,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *sınırlayıcı_değer,char **Sonraki_öğe){if(!Word_SMS)Word_SMS=*Sonraki_öğe;while(*Word_SMS&&strchr(sınırlayıcı_değer,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Sonraki_öğe=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(sınırlayıcı_değer,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Sonraki_öğe=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int TABAN_değer) {
    const char *kaynakKod=Word_SMS;unsigned long değer=0;int Negatif_değer=0,Taşma_değer=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')Negatif_değer=*Word_SMS++=='-';
    if((TABAN_değer==0||TABAN_değer==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {TABAN_değer=16;Word_SMS+=2;}
    if(!TABAN_değer)TABAN_değer=*Word_SMS=='0'?8:10;
    if(TABAN_değer<2||TABAN_değer>36){if(끝)*끝=(char*)kaynakKod;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned karakter_değer=(unsigned char)*Word_SMS;
        unsigned 수=karakter_değer>='0'&&karakter_değer<='9'?karakter_değer-'0':karakter_değer>='a'&&karakter_değer<='z'?karakter_değer-'a'+10:karakter_değer>='A'&&karakter_değer<='Z'?karakter_değer-'A'+10:36;
        if(수>=(unsigned)TABAN_değer)break;
        if(değer>(~0ul-수)/(unsigned)TABAN_değer)Taşma_değer=1;
        if(!Taşma_değer)değer=değer*(unsigned)TABAN_değer+수;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?kaynakKod:Word_SMS);
    return Taşma_değer?~0ul:Negatif_değer?0ul-değer:değer;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int çekirdek_değer_Durum;
void uzak_özet(const void *veri, size_t süre_değer, unsigned char sonuç[32]) {
    br_sha256_context Bağlam_değer;
    br_sha256_init(&Bağlam_değer); br_sha256_update(&Bağlam_değer, veri, süre_değer); br_sha256_out(&Bağlam_değer, sonuç);
    memset(&Bağlam_değer, 0, sizeof(Bağlam_değer));
}
#define 난수저장기(konum) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(konum)))
int uzak_rastgele(unsigned char *hedef_değer,unsigned süre_değer){
    if(!çekirdek_değer_Durum){volatile unsigned char *veri=(void*)0x01ff0000ul;const char *işaret_değer="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=veri[순번]^(unsigned char)işaret_değer[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=veri[8+순번];for(unsigned 순번=0;순번<40;순번++)veri[순번]=0;çekirdek_değer_Durum=2;}
        else {çekirdek_değer_Durum=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(çekirdek_değer_Durum==2){while(süre_değer){unsigned char Sonraki_öğe[32],artış_değer[33];memcpy(artış_değer,모의씨앗,32);artış_değer[32]=0;uzak_özet(artış_değer,33,Sonraki_öğe);
        artış_değer[32]=1;uzak_özet(artış_değer,33,모의씨앗);memset(artış_değer,0,33);
        unsigned 수=süre_değer<32?süre_değer:32;memcpy(hedef_değer,Sonraki_öğe,수);memset(Sonraki_öğe,0,32);hedef_değer+=수;süre_değer-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(süre_değer){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t değer=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&süre_değer;순번++,süre_değer--){*hedef_değer++=değer&255;değer>>=8;}}
    return 0;
}
