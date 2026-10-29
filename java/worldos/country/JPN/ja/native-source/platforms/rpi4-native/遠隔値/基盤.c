/* 中核値 전용 할당기와 合言葉値 난수 공급. 利用者 ELF의 libc와 별개이다. */
#include "暗号学支援.h"
#include "../命名/機械連結名前一覧.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 基板経過ミリ秒(void);
typedef struct 記憶ブロック { size_t 長さ; struct 記憶ブロック *次回項目; int 使用値; } 記憶ブロック;
static unsigned char 記憶一括領域[2*1024*1024] __attribute__((aligned(16)));
static 記憶ブロック *先頭位置断片値;
void *遠隔確保(size_t 長さ) {
    if (!長さ || 長さ>sizeof(記憶一括領域)-64) return 0;
    長さ=(長さ+15)&~(size_t)15;
    if(!先頭位置断片値){先頭位置断片値=(void*)記憶一括領域;先頭位置断片値->長さ=sizeof(記憶一括領域)-32;}
    for(記憶ブロック *断片値=先頭位置断片値;断片値;断片値=断片値->次回項目)if(!断片値->使用値&&断片値->長さ>=長さ){
        if(断片値->長さ>=長さ+64){記憶ブロック *新規断片=(void*)((char*)断片値+32+長さ);
            新規断片->長さ=断片値->長さ-長さ-32;新規断片->次回項目=断片値->次回項目;新規断片->使用値=0;断片値->次回項目=新規断片;断片値->長さ=長さ;}
        断片値->使用値=1;return(char*)断片値+32;
    }return 0;
}
void 遠隔解放(void *番地) {
    if(!番地)return;記憶ブロック *断片値=(void*)((char*)番地-32);
    volatile unsigned char *消去済み値=番地;for(size_t 序数添字=0;序数添字<断片値->長さ;序数添字++)消去済み値[序数添字]=0;
    断片値->使用値=0;
    for(断片値=先頭位置断片値;断片値&&断片値->次回項目;){if(!断片値->使用値&&!断片値->次回項目->使用値){断片値->長さ+=32+断片値->次回項目->長さ;断片値->次回項目=断片値->次回項目->次回項目;}else 断片値=断片値->次回項目;}
}
void *遠隔再確保(void *番地,size_t 長さ){
    if(!番地)return 遠隔確保(長さ);if(!長さ){遠隔解放(番地);return 0;}
    記憶ブロック *断片値=(void*)((char*)番地-32);void *新規番地=遠隔確保(長さ);
    if(新規番地){memcpy(新規番地,番地,長さ<断片値->長さ?長さ:断片値->長さ);遠隔解放(番地);}return 新規番地;
}
int strcmp(const char *先頭位置被演算子,const char *第二被演算子){while(*先頭位置被演算子&&*先頭位置被演算子==*第二被演算子){先頭位置被演算子++;第二被演算子++;}return(unsigned char)*先頭位置被演算子-(unsigned char)*第二被演算子;}
char *strchr(const char *語本文,int 文字値){for(;;語本文++){if(*語本文==(char)文字値)return(char*)語本文;if(!*語本文)return 0;}}
char *strstr(const char *語本文,const char *発見結果値){size_t 長さ=strlen(発見結果値);for(;*語本文;語本文++)if(!strncmp(語本文,発見結果値,長さ))return(char*)語本文;return 長さ?0:(char*)語本文;}
char *strncpy(char *宛先値,const char *原本,size_t 長さ){size_t 序数添字=0;for(;序数添字<長さ&&原本[序数添字];序数添字++)宛先値[序数添字]=原本[序数添字];for(;序数添字<長さ;序数添字++)宛先値[序数添字]=0;return 宛先値;}
char *strncat(char *宛先値,const char *原本,size_t 長さ){char *終端=宛先値+strlen(宛先値);while(長さ--&&*原本)*終端++=*原本++;*終端=0;return 宛先値;}
int strncasecmp(const char *先頭位置被演算子,const char *第二被演算子,size_t 長さ){while(長さ--){unsigned 先頭位置文字=*先頭位置被演算子++,第二文字=*第二被演算子++;if(先頭位置文字>='A'&&先頭位置文字<='Z')先頭位置文字+=32;if(第二文字>='A'&&第二文字<='Z')第二文字+=32;if(先頭位置文字!=第二文字)return(int)先頭位置文字-(int)第二文字;if(!先頭位置文字)break;}return 0;}
int strcasecmp(const char *先頭位置被演算子,const char *第二被演算子){return strncasecmp(先頭位置被演算子,第二被演算子,(size_t)-1);}
char *strtok_r(char *語本文,const char *区切り記号値,char **次回項目){if(!語本文)語本文=*次回項目;while(*語本文&&strchr(区切り記号値,*語本文))語本文++;if(!*語本文){*次回項目=語本文;return 0;}char *初期項目=語本文;while(*語本文&&!strchr(区切り記号値,*語本文))語本文++;if(*語本文)*語本文++=0;*次回項目=語本文;return 初期項目;}
unsigned long strtoul(const char *語本文, char **終端, int 基底値) {
    const char *ソース=語本文;unsigned long 値=0;int 負数値=0,桁あふれ値=0;
    while(*語本文==' '||(*語本文>=9&&*語本文<=13))語本文++;
    if(*語本文=='-'||*語本文=='+')負数値=*語本文++=='-';
    if((基底値==0||基底値==16)&&語本文[0]=='0'&&(語本文[1]=='x'||語本文[1]=='X')&&
       ((語本文[2]>='0'&&語本文[2]<='9')||(語本文[2]>='a'&&語本文[2]<='f')||(語本文[2]>='A'&&語本文[2]<='F'))) {基底値=16;語本文+=2;}
    if(!基底値)基底値=*語本文=='0'?8:10;
    if(基底値<2||基底値>36){if(終端)*終端=(char*)ソース;return 0;}
    const char *初期項目=語本文;
    for(;;語本文++) {
        unsigned 文字値=(unsigned char)*語本文;
        unsigned 数=文字値>='0'&&文字値<='9'?文字値-'0':文字値>='a'&&文字値<='z'?文字値-'a'+10:文字値>='A'&&文字値<='Z'?文字値-'A'+10:36;
        if(数>=(unsigned)基底値)break;
        if(値>(~0ul-数)/(unsigned)基底値)桁あふれ値=1;
        if(!桁あふれ値)値=値*(unsigned)基底値+数;
    }
    if(終端)*終端=(char*)(語本文==初期項目?ソース:語本文);
    return 桁あふれ値?~0ul:負数値?0ul-値:値;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 試験用模擬種[32];
static int 種状況;
void 遠隔要約(const void *データ, size_t 長さ, unsigned char 結果[32]) {
    br_sha256_context 文脈値;
    br_sha256_init(&文脈値); br_sha256_update(&文脈値, データ, 長さ); br_sha256_out(&文脈値, 結果);
    memset(&文脈値, 0, sizeof(文脈値));
}
#define 乱数レジスタ群(位置) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(位置)))
int 遠隔乱数(unsigned char *宛先値,unsigned 長さ){
    if(!種状況){volatile unsigned char *データ=(void*)0x01ff0000ul;const char *標識値="JKRENRG1";unsigned 差分値=0;
        for(unsigned 序数添字=0;序数添字<8;序数添字++)差分値|=データ[序数添字]^(unsigned char)標識値[序数添字];
        if(!差分値){for(unsigned 序数添字=0;序数添字<32;序数添字++)試験用模擬種[序数添字]=データ[8+序数添字];for(unsigned 序数添字=0;序数添字<40;序数添字++)データ[序数添字]=0;種状況=2;}
        else {種状況=1;乱数レジスタ群(0)=(乱数レジスタ群(0)&~0x1fffu)|1;}
    }
    if(種状況==2){while(長さ){unsigned char 次回項目[32],入力値[33];memcpy(入力値,試験用模擬種,32);入力値[32]=0;遠隔要約(入力値,33,次回項目);
        入力値[32]=1;遠隔要約(入力値,33,試験用模擬種);memset(入力値,0,33);
        unsigned 数=長さ<32?長さ:32;memcpy(宛先値,次回項目,数);memset(次回項目,0,32);宛先値+=数;長さ-=数;}return 0;}
    uintptr_t 上限値=基板経過ミリ秒()+1000;
    while(長さ){if((乱数レジスタ群(0x18)&0x80000020u)||基板経過ミリ秒()>上限値)return -1;
        if(!(乱数レジスタ群(0x24)&255))continue;uint32_t 値=乱数レジスタ群(0x20);
        for(unsigned 序数添字=0;序数添字<4&&長さ;序数添字++,長さ--){*宛先値++=値&255;値>>=8;}}
    return 0;
}
