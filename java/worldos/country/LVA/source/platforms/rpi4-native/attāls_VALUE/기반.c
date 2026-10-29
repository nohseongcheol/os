/* kodols_VALUE 전용 할당기와 parole_VALUE 난수 공급. lietotājs ELF의 libc와 별개이다. */
#include "kriptogrāfija_Atbalsts.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct atmiņa_bloks { size_t 길이; struct atmiņa_bloks *Tālāk_krājums; int lietot_VALUE; } atmiņa_bloks;
static unsigned char atmiņa_Arēna[2*1024*1024] __attribute__((aligned(16)));
static atmiņa_bloks *첫조각;
void *piešķirt_attāls(size_t 길이) {
    if (!길이 || 길이>sizeof(atmiņa_Arēna)-64) return 0;
    길이=(길이+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)atmiņa_Arēna;첫조각->길이=sizeof(atmiņa_Arēna)-32;}
    for(atmiņa_bloks *조각=첫조각;조각;조각=조각->Tālāk_krājums)if(!조각->lietot_VALUE&&조각->길이>=길이){
        if(조각->길이>=길이+64){atmiņa_bloks *새조각=(void*)((char*)조각+32+길이);
            새조각->길이=조각->길이-길이-32;새조각->Tālāk_krājums=조각->Tālāk_krājums;새조각->lietot_VALUE=0;조각->Tālāk_krājums=새조각;조각->길이=길이;}
        조각->lietot_VALUE=1;return(char*)조각+32;
    }return 0;
}
void izlaist_attāls(void *adrese) {
    if(!adrese)return;atmiņa_bloks *조각=(void*)((char*)adrese-32);
    volatile unsigned char *지움=adrese;for(size_t 순번=0;순번<조각->길이;순번++)지움[순번]=0;
    조각->lietot_VALUE=0;
    for(조각=첫조각;조각&&조각->Tālāk_krājums;){if(!조각->lietot_VALUE&&!조각->Tālāk_krājums->lietot_VALUE){조각->길이+=32+조각->Tālāk_krājums->길이;조각->Tālāk_krājums=조각->Tālāk_krājums->Tālāk_krājums;}else 조각=조각->Tālāk_krājums;}
}
void *원격재할당(void *adrese,size_t 길이){
    if(!adrese)return piešķirt_attāls(길이);if(!길이){izlaist_attāls(adrese);return 0;}
    atmiņa_bloks *조각=(void*)((char*)adrese-32);void *새주소=piešķirt_attāls(길이);
    if(새주소){memcpy(새주소,adrese,길이<조각->길이?길이:조각->길이);izlaist_attāls(adrese);}return 새주소;
}
int strcmp(const char *가,const char *SECOND_operands){while(*가&&*가==*SECOND_operands){가++;SECOND_operands++;}return(unsigned char)*가-(unsigned char)*SECOND_operands;}
char *strchr(const char *Word_SMS,int rakstzīme_VALUE){for(;;Word_SMS++){if(*Word_SMS==(char)rakstzīme_VALUE)return(char*)Word_SMS;if(!*Word_SMS)return 0;}}
char *strstr(const char *Word_SMS,const char *찾음){size_t 길이=strlen(찾음);for(;*Word_SMS;Word_SMS++)if(!strncmp(Word_SMS,찾음,길이))return(char*)Word_SMS;return 길이?0:(char*)Word_SMS;}
char *strncpy(char *mērķis_VALUE,const char *원본,size_t 길이){size_t 순번=0;for(;순번<길이&&원본[순번];순번++)mērķis_VALUE[순번]=원본[순번];for(;순번<길이;순번++)mērķis_VALUE[순번]=0;return mērķis_VALUE;}
char *strncat(char *mērķis_VALUE,const char *원본,size_t 길이){char *끝=mērķis_VALUE+strlen(mērķis_VALUE);while(길이--&&*원본)*끝++=*원본++;*끝=0;return mērķis_VALUE;}
int strncasecmp(const char *가,const char *SECOND_operands,size_t 길이){while(길이--){unsigned 첫글자=*가++,SECOND_rakstzīme=*SECOND_operands++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(SECOND_rakstzīme>='A'&&SECOND_rakstzīme<='Z')SECOND_rakstzīme+=32;if(첫글자!=SECOND_rakstzīme)return(int)첫글자-(int)SECOND_rakstzīme;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *SECOND_operands){return strncasecmp(가,SECOND_operands,(size_t)-1);}
char *strtok_r(char *Word_SMS,const char *norobežotājs_VALUE,char **Tālāk_krājums){if(!Word_SMS)Word_SMS=*Tālāk_krājums;while(*Word_SMS&&strchr(norobežotājs_VALUE,*Word_SMS))Word_SMS++;if(!*Word_SMS){*Tālāk_krājums=Word_SMS;return 0;}char *처음=Word_SMS;while(*Word_SMS&&!strchr(norobežotājs_VALUE,*Word_SMS))Word_SMS++;if(*Word_SMS)*Word_SMS++=0;*Tālāk_krājums=Word_SMS;return 처음;}
unsigned long strtoul(const char *Word_SMS, char **끝, int BASE_VALUE) {
    const char *AVOTS=Word_SMS;unsigned long VALUE=0;int 음수=0,pārpilde_VALUE=0;
    while(*Word_SMS==' '||(*Word_SMS>=9&&*Word_SMS<=13))Word_SMS++;
    if(*Word_SMS=='-'||*Word_SMS=='+')음수=*Word_SMS++=='-';
    if((BASE_VALUE==0||BASE_VALUE==16)&&Word_SMS[0]=='0'&&(Word_SMS[1]=='x'||Word_SMS[1]=='X')&&
       ((Word_SMS[2]>='0'&&Word_SMS[2]<='9')||(Word_SMS[2]>='a'&&Word_SMS[2]<='f')||(Word_SMS[2]>='A'&&Word_SMS[2]<='F'))) {BASE_VALUE=16;Word_SMS+=2;}
    if(!BASE_VALUE)BASE_VALUE=*Word_SMS=='0'?8:10;
    if(BASE_VALUE<2||BASE_VALUE>36){if(끝)*끝=(char*)AVOTS;return 0;}
    const char *처음=Word_SMS;
    for(;;Word_SMS++) {
        unsigned rakstzīme_VALUE=(unsigned char)*Word_SMS;
        unsigned numurs=rakstzīme_VALUE>='0'&&rakstzīme_VALUE<='9'?rakstzīme_VALUE-'0':rakstzīme_VALUE>='a'&&rakstzīme_VALUE<='z'?rakstzīme_VALUE-'a'+10:rakstzīme_VALUE>='A'&&rakstzīme_VALUE<='Z'?rakstzīme_VALUE-'A'+10:36;
        if(numurs>=(unsigned)BASE_VALUE)break;
        if(VALUE>(~0ul-numurs)/(unsigned)BASE_VALUE)pārpilde_VALUE=1;
        if(!pārpilde_VALUE)VALUE=VALUE*(unsigned)BASE_VALUE+numurs;
    }
    if(끝)*끝=(char*)(Word_SMS==처음?AVOTS:Word_SMS);
    return pārpilde_VALUE?~0ul:음수?0ul-VALUE:VALUE;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int dēstīt_Statuss;
void attāls_kopsavilkums(const void *dati, size_t 길이, unsigned char mērs[32]) {
    br_sha256_context konteksts_VALUE;
    br_sha256_init(&konteksts_VALUE); br_sha256_update(&konteksts_VALUE, dati, 길이); br_sha256_out(&konteksts_VALUE, mērs);
    memset(&konteksts_VALUE, 0, sizeof(konteksts_VALUE));
}
#define 난수저장기(Novietojums) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(Novietojums)))
int attāls_nejaušs(unsigned char *mērķis_VALUE,unsigned 길이){
    if(!dēstīt_Statuss){volatile unsigned char *dati=(void*)0x01ff0000ul;const char *marķieris_VALUE="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=dati[순번]^(unsigned char)marķieris_VALUE[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=dati[8+순번];for(unsigned 순번=0;순번<40;순번++)dati[순번]=0;dēstīt_Statuss=2;}
        else {dēstīt_Statuss=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(dēstīt_Statuss==2){while(길이){unsigned char Tālāk_krājums[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;attāls_kopsavilkums(입력,33,Tālāk_krājums);
        입력[32]=1;attāls_kopsavilkums(입력,33,모의씨앗);memset(입력,0,33);
        unsigned numurs=길이<32?길이:32;memcpy(mērķis_VALUE,Tālāk_krājums,numurs);memset(Tālāk_krājums,0,32);mērķis_VALUE+=numurs;길이-=numurs;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(길이){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t VALUE=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&길이;순번++,길이--){*mērķis_VALUE++=VALUE&255;VALUE>>=8;}}
    return 0;
}
