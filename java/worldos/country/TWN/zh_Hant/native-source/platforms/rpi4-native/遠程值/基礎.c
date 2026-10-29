/* 內核值 전용 할당기와 密碼值 난수 공급. 使用者 ELF의 libc와 별개이다. */
#include "密碼學支持.h"
#include "../命名/計算機連接名稱列.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 板經過毫秒(void);
typedef struct 記憶體塊 { size_t 長度; struct 記憶體塊 *下一項目; int 使用值; } 記憶體塊;
static unsigned char 記憶體連續區[2*1024*1024] __attribute__((aligned(16)));
static 記憶體塊 *首位片段值;
void *分配遠程(size_t 長度) {
    if (!長度 || 長度>sizeof(記憶體連續區)-64) return 0;
    長度=(長度+15)&~(size_t)15;
    if(!首位片段值){首位片段值=(void*)記憶體連續區;首位片段值->長度=sizeof(記憶體連續區)-32;}
    for(記憶體塊 *片段值=首位片段值;片段值;片段值=片段值->下一項目)if(!片段值->使用值&&片段值->長度>=長度){
        if(片段值->長度>=長度+64){記憶體塊 *新建片段=(void*)((char*)片段值+32+長度);
            新建片段->長度=片段值->長度-長度-32;新建片段->下一項目=片段值->下一項目;新建片段->使用值=0;片段值->下一項目=新建片段;片段值->長度=長度;}
        片段值->使用值=1;return(char*)片段值+32;
    }return 0;
}
void 釋放遠程(void *地址) {
    if(!地址)return;記憶體塊 *片段值=(void*)((char*)地址-32);
    volatile unsigned char *已擦除值=地址;for(size_t 序數索引=0;序數索引<片段值->長度;序數索引++)已擦除值[序數索引]=0;
    片段值->使用值=0;
    for(片段值=首位片段值;片段值&&片段值->下一項目;){if(!片段值->使用值&&!片段值->下一項目->使用值){片段值->長度+=32+片段值->下一項目->長度;片段值->下一項目=片段值->下一項目->下一項目;}else 片段值=片段值->下一項目;}
}
void *重新分配遠程(void *地址,size_t 長度){
    if(!地址)return 分配遠程(長度);if(!長度){釋放遠程(地址);return 0;}
    記憶體塊 *片段值=(void*)((char*)地址-32);void *新建地址=分配遠程(長度);
    if(新建地址){memcpy(新建地址,地址,長度<片段值->長度?長度:片段值->長度);釋放遠程(地址);}return 新建地址;
}
int strcmp(const char *首位操作數,const char *第二操作數){while(*首位操作數&&*首位操作數==*第二操作數){首位操作數++;第二操作數++;}return(unsigned char)*首位操作數-(unsigned char)*第二操作數;}
char *strchr(const char *機器字文本,int 字元值){for(;;機器字文本++){if(*機器字文本==(char)字元值)return(char*)機器字文本;if(!*機器字文本)return 0;}}
char *strstr(const char *機器字文本,const char *已找到值){size_t 長度=strlen(已找到值);for(;*機器字文本;機器字文本++)if(!strncmp(機器字文本,已找到值,長度))return(char*)機器字文本;return 長度?0:(char*)機器字文本;}
char *strncpy(char *目的地址值,const char *原始,size_t 長度){size_t 序數索引=0;for(;序數索引<長度&&原始[序數索引];序數索引++)目的地址值[序數索引]=原始[序數索引];for(;序數索引<長度;序數索引++)目的地址值[序數索引]=0;return 目的地址值;}
char *strncat(char *目的地址值,const char *原始,size_t 長度){char *結尾=目的地址值+strlen(目的地址值);while(長度--&&*原始)*結尾++=*原始++;*結尾=0;return 目的地址值;}
int strncasecmp(const char *首位操作數,const char *第二操作數,size_t 長度){while(長度--){unsigned 首位字元=*首位操作數++,第二字元=*第二操作數++;if(首位字元>='A'&&首位字元<='Z')首位字元+=32;if(第二字元>='A'&&第二字元<='Z')第二字元+=32;if(首位字元!=第二字元)return(int)首位字元-(int)第二字元;if(!首位字元)break;}return 0;}
int strcasecmp(const char *首位操作數,const char *第二操作數){return strncasecmp(首位操作數,第二操作數,(size_t)-1);}
char *strtok_r(char *機器字文本,const char *分隔符值,char **下一項目){if(!機器字文本)機器字文本=*下一項目;while(*機器字文本&&strchr(分隔符值,*機器字文本))機器字文本++;if(!*機器字文本){*下一項目=機器字文本;return 0;}char *初始項目=機器字文本;while(*機器字文本&&!strchr(分隔符值,*機器字文本))機器字文本++;if(*機器字文本)*機器字文本++=0;*下一項目=機器字文本;return 初始項目;}
unsigned long strtoul(const char *機器字文本, char **結尾, int 基底值) {
    const char *原始碼=機器字文本;unsigned long 值=0;int 負數值=0,溢出值=0;
    while(*機器字文本==' '||(*機器字文本>=9&&*機器字文本<=13))機器字文本++;
    if(*機器字文本=='-'||*機器字文本=='+')負數值=*機器字文本++=='-';
    if((基底值==0||基底值==16)&&機器字文本[0]=='0'&&(機器字文本[1]=='x'||機器字文本[1]=='X')&&
       ((機器字文本[2]>='0'&&機器字文本[2]<='9')||(機器字文本[2]>='a'&&機器字文本[2]<='f')||(機器字文本[2]>='A'&&機器字文本[2]<='F'))) {基底值=16;機器字文本+=2;}
    if(!基底值)基底值=*機器字文本=='0'?8:10;
    if(基底值<2||基底值>36){if(結尾)*結尾=(char*)原始碼;return 0;}
    const char *初始項目=機器字文本;
    for(;;機器字文本++) {
        unsigned 字元值=(unsigned char)*機器字文本;
        unsigned 數=字元值>='0'&&字元值<='9'?字元值-'0':字元值>='a'&&字元值<='z'?字元值-'a'+10:字元值>='A'&&字元值<='Z'?字元值-'A'+10:36;
        if(數>=(unsigned)基底值)break;
        if(值>(~0ul-數)/(unsigned)基底值)溢出值=1;
        if(!溢出值)值=值*(unsigned)基底值+數;
    }
    if(結尾)*結尾=(char*)(機器字文本==初始項目?原始碼:機器字文本);
    return 溢出值?~0ul:負數值?0ul-值:值;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 測試替身種子[32];
static int 種子狀態;
void 遠程摘要(const void *資料, size_t 長度, unsigned char 結果[32]) {
    br_sha256_context 上下文值;
    br_sha256_init(&上下文值); br_sha256_update(&上下文值, 資料, 長度); br_sha256_out(&上下文值, 結果);
    memset(&上下文值, 0, sizeof(上下文值));
}
#define 隨機寄存器集(位置) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(位置)))
int 遠程隨機(unsigned char *目的地址值,unsigned 長度){
    if(!種子狀態){volatile unsigned char *資料=(void*)0x01ff0000ul;const char *標記值="JKRENRG1";unsigned 差異值=0;
        for(unsigned 序數索引=0;序數索引<8;序數索引++)差異值|=資料[序數索引]^(unsigned char)標記值[序數索引];
        if(!差異值){for(unsigned 序數索引=0;序數索引<32;序數索引++)測試替身種子[序數索引]=資料[8+序數索引];for(unsigned 序數索引=0;序數索引<40;序數索引++)資料[序數索引]=0;種子狀態=2;}
        else {種子狀態=1;隨機寄存器集(0)=(隨機寄存器集(0)&~0x1fffu)|1;}
    }
    if(種子狀態==2){while(長度){unsigned char 下一項目[32],輸入值[33];memcpy(輸入值,測試替身種子,32);輸入值[32]=0;遠程摘要(輸入值,33,下一項目);
        輸入值[32]=1;遠程摘要(輸入值,33,測試替身種子);memset(輸入值,0,33);
        unsigned 數=長度<32?長度:32;memcpy(目的地址值,下一項目,數);memset(下一項目,0,32);目的地址值+=數;長度-=數;}return 0;}
    uintptr_t 限制值=板經過毫秒()+1000;
    while(長度){if((隨機寄存器集(0x18)&0x80000020u)||板經過毫秒()>限制值)return -1;
        if(!(隨機寄存器集(0x24)&255))continue;uint32_t 值=隨機寄存器集(0x20);
        for(unsigned 序數索引=0;序數索引<4&&長度;序數索引++,長度--){*目的地址值++=值&255;值>>=8;}}
    return 0;
}
