/* කර්නලය_අගය 전용 할당기와 මුර_පදය_අගය 난수 공급. පරිශීලක ELF의 libc와 별개이다. */
#include "암호기반.h"
#include "../명명/기계연결이름.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 보드밀리초(void);
typedef struct මතකය_අවහිර_කරන්න { size_t දිග_අගය; struct මතකය_අවහිර_කරන්න *다음; int 사용; } මතකය_අවහිර_කරන්න;
static unsigned char 기억터[2*1024*1024] __attribute__((aligned(16)));
static මතකය_අවහිර_කරන්න *첫조각;
void *විබෙදන්න_දුරස්ථ(size_t දිග_අගය) {
    if (!දිග_අගය || දිග_අගය>sizeof(기억터)-64) return 0;
    දිග_අගය=(දිග_අගය+15)&~(size_t)15;
    if(!첫조각){첫조각=(void*)기억터;첫조각->දිග_අගය=sizeof(기억터)-32;}
    for(මතකය_අවහිර_කරන්න *조각=첫조각;조각;조각=조각->다음)if(!조각->사용&&조각->දිග_අගය>=දිග_අගය){
        if(조각->දිග_අගය>=දිග_අගය+64){මතකය_අවහිර_කරන්න *새조각=(void*)((char*)조각+32+දිග_අගය);
            새조각->දිග_අගය=조각->දිග_අගය-දිග_අගය-32;새조각->다음=조각->다음;새조각->사용=0;조각->다음=새조각;조각->දිග_අගය=දිග_අගය;}
        조각->사용=1;return(char*)조각+32;
    }return 0;
}
void මුදාහැරීම_දුරස්ථ(void *යොමුව) {
    if(!යොමුව)return;මතකය_අවහිර_කරන්න *조각=(void*)((char*)යොමුව-32);
    volatile unsigned char *지움=යොමුව;for(size_t 순번=0;순번<조각->දිග_අගය;순번++)지움[순번]=0;
    조각->사용=0;
    for(조각=첫조각;조각&&조각->다음;){if(!조각->사용&&!조각->다음->사용){조각->දිග_අගය+=32+조각->다음->දිග_අගය;조각->다음=조각->다음->다음;}else 조각=조각->다음;}
}
void *원격재할당(void *යොමුව,size_t දිග_අගය){
    if(!යොමුව)return විබෙදන්න_දුරස්ථ(දිග_අගය);if(!දිග_අගය){මුදාහැරීම_දුරස්ථ(යොමුව);return 0;}
    මතකය_අවහිර_කරන්න *조각=(void*)((char*)යොමුව-32);void *새주소=විබෙදන්න_දුරස්ථ(දිග_අගය);
    if(새주소){memcpy(새주소,යොමුව,දිග_අගය<조각->දිග_අගය?දිග_අගය:조각->දිග_අගය);මුදාහැරීම_දුරස්ථ(යොමුව);}return 새주소;
}
int strcmp(const char *가,const char *나){while(*가&&*가==*나){가++;나++;}return(unsigned char)*가-(unsigned char)*나;}
char *strchr(const char *말,int අනුලකුණ_අගය){for(;;말++){if(*말==(char)අනුලකුණ_අගය)return(char*)말;if(!*말)return 0;}}
char *strstr(const char *말,const char *찾음){size_t දිග_අගය=strlen(찾음);for(;*말;말++)if(!strncmp(말,찾음,දිග_අගය))return(char*)말;return දිග_අගය?0:(char*)말;}
char *strncpy(char *ගමනාන්තය_අගය,const char *원본,size_t දිග_අගය){size_t 순번=0;for(;순번<දිග_අගය&&원본[순번];순번++)ගමනාන්තය_අගය[순번]=원본[순번];for(;순번<දිග_අගය;순번++)ගමනාන්තය_අගය[순번]=0;return ගමනාන්තය_අගය;}
char *strncat(char *ගමනාන්තය_අගය,const char *원본,size_t දිග_අගය){char *끝=ගමනාන්තය_අගය+strlen(ගමනාන්තය_අගය);while(දිග_අගය--&&*원본)*끝++=*원본++;*끝=0;return ගමනාන්තය_අගය;}
int strncasecmp(const char *가,const char *나,size_t දිග_අගය){while(දිග_අගය--){unsigned 첫글자=*가++,둘째글자=*나++;if(첫글자>='A'&&첫글자<='Z')첫글자+=32;if(둘째글자>='A'&&둘째글자<='Z')둘째글자+=32;if(첫글자!=둘째글자)return(int)첫글자-(int)둘째글자;if(!첫글자)break;}return 0;}
int strcasecmp(const char *가,const char *나){return strncasecmp(가,나,(size_t)-1);}
char *strtok_r(char *말,const char *පරිසීමකය_අගය,char **다음){if(!말)말=*다음;while(*말&&strchr(පරිසීමකය_අගය,*말))말++;if(!*말){*다음=말;return 0;}char *처음=말;while(*말&&!strchr(පරිසීමකය_අගය,*말))말++;if(*말)*말++=0;*다음=말;return 처음;}
unsigned long strtoul(const char *말, char **끝, int 밑) {
    const char *මූලය=말;unsigned long අගය=0;int 음수=0,පිටාරය_අගය=0;
    while(*말==' '||(*말>=9&&*말<=13))말++;
    if(*말=='-'||*말=='+')음수=*말++=='-';
    if((밑==0||밑==16)&&말[0]=='0'&&(말[1]=='x'||말[1]=='X')&&
       ((말[2]>='0'&&말[2]<='9')||(말[2]>='a'&&말[2]<='f')||(말[2]>='A'&&말[2]<='F'))) {밑=16;말+=2;}
    if(!밑)밑=*말=='0'?8:10;
    if(밑<2||밑>36){if(끝)*끝=(char*)මූලය;return 0;}
    const char *처음=말;
    for(;;말++) {
        unsigned අනුලකුණ_අගය=(unsigned char)*말;
        unsigned 수=අනුලකුණ_අගය>='0'&&අනුලකුණ_අගය<='9'?අනුලකුණ_අගය-'0':අනුලකුණ_අගය>='a'&&අනුලකුණ_අගය<='z'?අනුලකුණ_අගය-'a'+10:අනුලකුණ_අගය>='A'&&අනුලකුණ_අගය<='Z'?අනුලකුණ_අගය-'A'+10:36;
        if(수>=(unsigned)밑)break;
        if(අගය>(~0ul-수)/(unsigned)밑)පිටාරය_අගය=1;
        if(!පිටාරය_අගය)අගය=අගය*(unsigned)밑+수;
    }
    if(끝)*끝=(char*)(말==처음?මූලය:말);
    return පිටාරය_අගය?~0ul:음수?0ul-අගය:අගය;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 모의씨앗[32];
static int බීජනය_තත්වය;
void දුරස්ථ_සාරාංශය(const void *දත්ත, size_t දිග_අගය, unsigned char 결과[32]) {
    br_sha256_context සන්දර්භය_අගය;
    br_sha256_init(&සන්දර්භය_අගය); br_sha256_update(&සන්දර්භය_අගය, දත්ත, දිග_අගය); br_sha256_out(&සන්දර්භය_අගය, 결과);
    memset(&සන්දර්භය_අගය, 0, sizeof(සන්දර්භය_අගය));
}
#define 난수저장기(පිහිටීම) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(පිහිටීම)))
int 원격난수(unsigned char *ගමනාන්තය_අගය,unsigned දිග_අගය){
    if(!බීජනය_තත්වය){volatile unsigned char *දත්ත=(void*)0x01ff0000ul;const char *표식="JKRENRG1";unsigned 차이=0;
        for(unsigned 순번=0;순번<8;순번++)차이|=දත්ත[순번]^(unsigned char)표식[순번];
        if(!차이){for(unsigned 순번=0;순번<32;순번++)모의씨앗[순번]=දත්ත[8+순번];for(unsigned 순번=0;순번<40;순번++)දත්ත[순번]=0;බීජනය_තත්වය=2;}
        else {බීජනය_තත්වය=1;난수저장기(0)=(난수저장기(0)&~0x1fffu)|1;}
    }
    if(බීජනය_තත්වය==2){while(දිග_අගය){unsigned char 다음[32],입력[33];memcpy(입력,모의씨앗,32);입력[32]=0;දුරස්ථ_සාරාංශය(입력,33,다음);
        입력[32]=1;දුරස්ථ_සාරාංශය(입력,33,모의씨앗);memset(입력,0,33);
        unsigned 수=දිග_අගය<32?දිග_අගය:32;memcpy(ගමනාන්තය_අගය,다음,수);memset(다음,0,32);ගමනාන්තය_අගය+=수;දිග_අගය-=수;}return 0;}
    uintptr_t 제한=보드밀리초()+1000;
    while(දිග_අගය){if((난수저장기(0x18)&0x80000020u)||보드밀리초()>제한)return -1;
        if(!(난수저장기(0x24)&255))continue;uint32_t අගය=난수저장기(0x20);
        for(unsigned 순번=0;순번<4&&දිග_අගය;순번++,දිග_අගය--){*ගමනාන්තය_අගය++=අගය&255;අගය>>=8;}}
    return 0;
}
