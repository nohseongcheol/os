/* giáTrịNhân 전용 할당기와 giáTrịMậtKhẩu 난수 공급. NgườiDùng ELF의 libc와 별개이다. */
#include "hỗTrợMậtMãHọc.h"
#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t miliGiâyGọnBoMạch(void);
typedef struct khốiBộNhớ { size_t độDài; struct khốiBộNhớ *phầnMụcKếTiếp; int giáTrịDùng; } khốiBộNhớ;
static unsigned char vùngCấpPhátBộNhớ[2*1024*1024] __attribute__((aligned(16)));
static khốiBộNhớ *giáTrịĐoạnĐầuTiên;
void *cấpPhátTừXa(size_t độDài) {
    if (!độDài || độDài>sizeof(vùngCấpPhátBộNhớ)-64) return 0;
    độDài=(độDài+15)&~(size_t)15;
    if(!giáTrịĐoạnĐầuTiên){giáTrịĐoạnĐầuTiên=(void*)vùngCấpPhátBộNhớ;giáTrịĐoạnĐầuTiên->độDài=sizeof(vùngCấpPhátBộNhớ)-32;}
    for(khốiBộNhớ *giáTrịĐoạn=giáTrịĐoạnĐầuTiên;giáTrịĐoạn;giáTrịĐoạn=giáTrịĐoạn->phầnMụcKếTiếp)if(!giáTrịĐoạn->giáTrịDùng&&giáTrịĐoạn->độDài>=độDài){
        if(giáTrịĐoạn->độDài>=độDài+64){khốiBộNhớ *đoạnMới=(void*)((char*)giáTrịĐoạn+32+độDài);
            đoạnMới->độDài=giáTrịĐoạn->độDài-độDài-32;đoạnMới->phầnMụcKếTiếp=giáTrịĐoạn->phầnMụcKếTiếp;đoạnMới->giáTrịDùng=0;giáTrịĐoạn->phầnMụcKếTiếp=đoạnMới;giáTrịĐoạn->độDài=độDài;}
        giáTrịĐoạn->giáTrịDùng=1;return(char*)giáTrịĐoạn+32;
    }return 0;
}
void giảiPhóngTừXa(void *địaChỉ) {
    if(!địaChỉ)return;khốiBộNhớ *giáTrịĐoạn=(void*)((char*)địaChỉ-32);
    volatile unsigned char *giáTrịĐãXóa=địaChỉ;for(size_t chỉSốThứBậc=0;chỉSốThứBậc<giáTrịĐoạn->độDài;chỉSốThứBậc++)giáTrịĐãXóa[chỉSốThứBậc]=0;
    giáTrịĐoạn->giáTrịDùng=0;
    for(giáTrịĐoạn=giáTrịĐoạnĐầuTiên;giáTrịĐoạn&&giáTrịĐoạn->phầnMụcKếTiếp;){if(!giáTrịĐoạn->giáTrịDùng&&!giáTrịĐoạn->phầnMụcKếTiếp->giáTrịDùng){giáTrịĐoạn->độDài+=32+giáTrịĐoạn->phầnMụcKếTiếp->độDài;giáTrịĐoạn->phầnMụcKếTiếp=giáTrịĐoạn->phầnMụcKếTiếp->phầnMụcKếTiếp;}else giáTrịĐoạn=giáTrịĐoạn->phầnMụcKếTiếp;}
}
void *cấpPhátLạiTừXa(void *địaChỉ,size_t độDài){
    if(!địaChỉ)return cấpPhátTừXa(độDài);if(!độDài){giảiPhóngTừXa(địaChỉ);return 0;}
    khốiBộNhớ *giáTrịĐoạn=(void*)((char*)địaChỉ-32);void *địaChỉMới=cấpPhátTừXa(độDài);
    if(địaChỉMới){memcpy(địaChỉMới,địaChỉ,độDài<giáTrịĐoạn->độDài?độDài:giáTrịĐoạn->độDài);giảiPhóngTừXa(địaChỉ);}return địaChỉMới;
}
int strcmp(const char *toánHạngĐầuTiên,const char *toánHạngThứHai){while(*toánHạngĐầuTiên&&*toánHạngĐầuTiên==*toánHạngThứHai){toánHạngĐầuTiên++;toánHạngThứHai++;}return(unsigned char)*toánHạngĐầuTiên-(unsigned char)*toánHạngThứHai;}
char *strchr(const char *vănBảnTừ,int giáTrịKýTự){for(;;vănBảnTừ++){if(*vănBảnTừ==(char)giáTrịKýTự)return(char*)vănBảnTừ;if(!*vănBảnTừ)return 0;}}
char *strstr(const char *vănBảnTừ,const char *giáTrịĐãTìmThấy){size_t độDài=strlen(giáTrịĐãTìmThấy);for(;*vănBảnTừ;vănBảnTừ++)if(!strncmp(vănBảnTừ,giáTrịĐãTìmThấy,độDài))return(char*)vănBảnTừ;return độDài?0:(char*)vănBảnTừ;}
char *strncpy(char *giáTrịĐích,const char *nguyênBản,size_t độDài){size_t chỉSốThứBậc=0;for(;chỉSốThứBậc<độDài&&nguyênBản[chỉSốThứBậc];chỉSốThứBậc++)giáTrịĐích[chỉSốThứBậc]=nguyênBản[chỉSốThứBậc];for(;chỉSốThứBậc<độDài;chỉSốThứBậc++)giáTrịĐích[chỉSốThứBậc]=0;return giáTrịĐích;}
char *strncat(char *giáTrịĐích,const char *nguyênBản,size_t độDài){char *phầnKết=giáTrịĐích+strlen(giáTrịĐích);while(độDài--&&*nguyênBản)*phầnKết++=*nguyênBản++;*phầnKết=0;return giáTrịĐích;}
int strncasecmp(const char *toánHạngĐầuTiên,const char *toánHạngThứHai,size_t độDài){while(độDài--){unsigned kýTựĐầuTiên=*toánHạngĐầuTiên++,kýTựThứHai=*toánHạngThứHai++;if(kýTựĐầuTiên>='A'&&kýTựĐầuTiên<='Z')kýTựĐầuTiên+=32;if(kýTựThứHai>='A'&&kýTựThứHai<='Z')kýTựThứHai+=32;if(kýTựĐầuTiên!=kýTựThứHai)return(int)kýTựĐầuTiên-(int)kýTựThứHai;if(!kýTựĐầuTiên)break;}return 0;}
int strcasecmp(const char *toánHạngĐầuTiên,const char *toánHạngThứHai){return strncasecmp(toánHạngĐầuTiên,toánHạngThứHai,(size_t)-1);}
char *strtok_r(char *vănBảnTừ,const char *giáTrịDấuPhânCách,char **phầnMụcKếTiếp){if(!vănBảnTừ)vănBảnTừ=*phầnMụcKếTiếp;while(*vănBảnTừ&&strchr(giáTrịDấuPhânCách,*vănBảnTừ))vănBảnTừ++;if(!*vănBảnTừ){*phầnMụcKếTiếp=vănBảnTừ;return 0;}char *phầnMụcBanĐầu=vănBảnTừ;while(*vănBảnTừ&&!strchr(giáTrịDấuPhânCách,*vănBảnTừ))vănBảnTừ++;if(*vănBảnTừ)*vănBảnTừ++=0;*phầnMụcKếTiếp=vănBảnTừ;return phầnMụcBanĐầu;}
unsigned long strtoul(const char *vănBảnTừ, char **phầnKết, int giáTrịCơSở) {
    const char *mãNguồn=vănBảnTừ;unsigned long giáTrị=0;int giáTrịÂm=0,giáTrịTràn=0;
    while(*vănBảnTừ==' '||(*vănBảnTừ>=9&&*vănBảnTừ<=13))vănBảnTừ++;
    if(*vănBảnTừ=='-'||*vănBảnTừ=='+')giáTrịÂm=*vănBảnTừ++=='-';
    if((giáTrịCơSở==0||giáTrịCơSở==16)&&vănBảnTừ[0]=='0'&&(vănBảnTừ[1]=='x'||vănBảnTừ[1]=='X')&&
       ((vănBảnTừ[2]>='0'&&vănBảnTừ[2]<='9')||(vănBảnTừ[2]>='a'&&vănBảnTừ[2]<='f')||(vănBảnTừ[2]>='A'&&vănBảnTừ[2]<='F'))) {giáTrịCơSở=16;vănBảnTừ+=2;}
    if(!giáTrịCơSở)giáTrịCơSở=*vănBảnTừ=='0'?8:10;
    if(giáTrịCơSở<2||giáTrịCơSở>36){if(phầnKết)*phầnKết=(char*)mãNguồn;return 0;}
    const char *phầnMụcBanĐầu=vănBảnTừ;
    for(;;vănBảnTừ++) {
        unsigned giáTrịKýTự=(unsigned char)*vănBảnTừ;
        unsigned trịSố=giáTrịKýTự>='0'&&giáTrịKýTự<='9'?giáTrịKýTự-'0':giáTrịKýTự>='a'&&giáTrịKýTự<='z'?giáTrịKýTự-'a'+10:giáTrịKýTự>='A'&&giáTrịKýTự<='Z'?giáTrịKýTự-'A'+10:36;
        if(trịSố>=(unsigned)giáTrịCơSở)break;
        if(giáTrị>(~0ul-trịSố)/(unsigned)giáTrịCơSở)giáTrịTràn=1;
        if(!giáTrịTràn)giáTrị=giáTrị*(unsigned)giáTrịCơSở+trịSố;
    }
    if(phầnKết)*phầnKết=(char*)(vănBảnTừ==phầnMụcBanĐầu?mãNguồn:vănBảnTừ);
    return giáTrịTràn?~0ul:giáTrịÂm?0ul-giáTrị:giáTrị;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char hạtGiốngGiảLập[32];
static int trạngTháiHạtGiống;
void tómLượcTừXa(const void *DữLiệu, size_t độDài, unsigned char kếtQuả[32]) {
    br_sha256_context giáTrịNgữCảnh;
    br_sha256_init(&giáTrịNgữCảnh); br_sha256_update(&giáTrịNgữCảnh, DữLiệu, độDài); br_sha256_out(&giáTrịNgữCảnh, kếtQuả);
    memset(&giáTrịNgữCảnh, 0, sizeof(giáTrịNgữCảnh));
}
#define cácThanhGhiNgẫuNhiên(vịTrí) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(vịTrí)))
int ngẫuNhiênTừXa(unsigned char *giáTrịĐích,unsigned độDài){
    if(!trạngTháiHạtGiống){volatile unsigned char *DữLiệu=(void*)0x01ff0000ul;const char *giáTrịDấuMốc="JKRENRG1";unsigned giáTrịKhácBiệt=0;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<8;chỉSốThứBậc++)giáTrịKhácBiệt|=DữLiệu[chỉSốThứBậc]^(unsigned char)giáTrịDấuMốc[chỉSốThứBậc];
        if(!giáTrịKhácBiệt){for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++)hạtGiốngGiảLập[chỉSốThứBậc]=DữLiệu[8+chỉSốThứBậc];for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<40;chỉSốThứBậc++)DữLiệu[chỉSốThứBậc]=0;trạngTháiHạtGiống=2;}
        else {trạngTháiHạtGiống=1;cácThanhGhiNgẫuNhiên(0)=(cácThanhGhiNgẫuNhiên(0)&~0x1fffu)|1;}
    }
    if(trạngTháiHạtGiống==2){while(độDài){unsigned char phầnMụcKếTiếp[32],giáTrịVào[33];memcpy(giáTrịVào,hạtGiốngGiảLập,32);giáTrịVào[32]=0;tómLượcTừXa(giáTrịVào,33,phầnMụcKếTiếp);
        giáTrịVào[32]=1;tómLượcTừXa(giáTrịVào,33,hạtGiốngGiảLập);memset(giáTrịVào,0,33);
        unsigned trịSố=độDài<32?độDài:32;memcpy(giáTrịĐích,phầnMụcKếTiếp,trịSố);memset(phầnMụcKếTiếp,0,32);giáTrịĐích+=trịSố;độDài-=trịSố;}return 0;}
    uintptr_t giáTrịGiớiHạn=miliGiâyGọnBoMạch()+1000;
    while(độDài){if((cácThanhGhiNgẫuNhiên(0x18)&0x80000020u)||miliGiâyGọnBoMạch()>giáTrịGiớiHạn)return -1;
        if(!(cácThanhGhiNgẫuNhiên(0x24)&255))continue;uint32_t giáTrị=cácThanhGhiNgẫuNhiên(0x20);
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<4&&độDài;chỉSốThứBậc++,độDài--){*giáTrịĐích++=giáTrị&255;giáTrị>>=8;}}
    return 0;
}
