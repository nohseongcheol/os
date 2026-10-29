/* 内核值 전용 할당기와 密码值 난수 공급. 用户 ELF의 libc와 별개이다. */
#include "密码学支持.h"
#include "../命名/计算机连接名称列.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t 板经过毫秒(void);
typedef struct 内存块 { size_t 长度; struct 内存块 *下一项目; int 使用值; } 内存块;
static unsigned char 内存连续区[2*1024*1024] __attribute__((aligned(16)));
static 内存块 *首位片段值;
void *分配远程(size_t 长度) {
    if (!长度 || 长度>sizeof(内存连续区)-64) return 0;
    长度=(长度+15)&~(size_t)15;
    if(!首位片段值){首位片段值=(void*)内存连续区;首位片段值->长度=sizeof(内存连续区)-32;}
    for(内存块 *片段值=首位片段值;片段值;片段值=片段值->下一项目)if(!片段值->使用值&&片段值->长度>=长度){
        if(片段值->长度>=长度+64){内存块 *新建片段=(void*)((char*)片段值+32+长度);
            新建片段->长度=片段值->长度-长度-32;新建片段->下一项目=片段值->下一项目;新建片段->使用值=0;片段值->下一项目=新建片段;片段值->长度=长度;}
        片段值->使用值=1;return(char*)片段值+32;
    }return 0;
}
void 释放远程(void *地址) {
    if(!地址)return;内存块 *片段值=(void*)((char*)地址-32);
    volatile unsigned char *已擦除值=地址;for(size_t 序数索引=0;序数索引<片段值->长度;序数索引++)已擦除值[序数索引]=0;
    片段值->使用值=0;
    for(片段值=首位片段值;片段值&&片段值->下一项目;){if(!片段值->使用值&&!片段值->下一项目->使用值){片段值->长度+=32+片段值->下一项目->长度;片段值->下一项目=片段值->下一项目->下一项目;}else 片段值=片段值->下一项目;}
}
void *重新分配远程(void *地址,size_t 长度){
    if(!地址)return 分配远程(长度);if(!长度){释放远程(地址);return 0;}
    内存块 *片段值=(void*)((char*)地址-32);void *新建地址=分配远程(长度);
    if(新建地址){memcpy(新建地址,地址,长度<片段值->长度?长度:片段值->长度);释放远程(地址);}return 新建地址;
}
int strcmp(const char *首位操作数,const char *第二操作数){while(*首位操作数&&*首位操作数==*第二操作数){首位操作数++;第二操作数++;}return(unsigned char)*首位操作数-(unsigned char)*第二操作数;}
char *strchr(const char *机器字文本,int 字符值){for(;;机器字文本++){if(*机器字文本==(char)字符值)return(char*)机器字文本;if(!*机器字文本)return 0;}}
char *strstr(const char *机器字文本,const char *已找到值){size_t 长度=strlen(已找到值);for(;*机器字文本;机器字文本++)if(!strncmp(机器字文本,已找到值,长度))return(char*)机器字文本;return 长度?0:(char*)机器字文本;}
char *strncpy(char *目的地址值,const char *原始,size_t 长度){size_t 序数索引=0;for(;序数索引<长度&&原始[序数索引];序数索引++)目的地址值[序数索引]=原始[序数索引];for(;序数索引<长度;序数索引++)目的地址值[序数索引]=0;return 目的地址值;}
char *strncat(char *目的地址值,const char *原始,size_t 长度){char *结尾=目的地址值+strlen(目的地址值);while(长度--&&*原始)*结尾++=*原始++;*结尾=0;return 目的地址值;}
int strncasecmp(const char *首位操作数,const char *第二操作数,size_t 长度){while(长度--){unsigned 首位字符=*首位操作数++,第二字符=*第二操作数++;if(首位字符>='A'&&首位字符<='Z')首位字符+=32;if(第二字符>='A'&&第二字符<='Z')第二字符+=32;if(首位字符!=第二字符)return(int)首位字符-(int)第二字符;if(!首位字符)break;}return 0;}
int strcasecmp(const char *首位操作数,const char *第二操作数){return strncasecmp(首位操作数,第二操作数,(size_t)-1);}
char *strtok_r(char *机器字文本,const char *分隔符值,char **下一项目){if(!机器字文本)机器字文本=*下一项目;while(*机器字文本&&strchr(分隔符值,*机器字文本))机器字文本++;if(!*机器字文本){*下一项目=机器字文本;return 0;}char *初始项目=机器字文本;while(*机器字文本&&!strchr(分隔符值,*机器字文本))机器字文本++;if(*机器字文本)*机器字文本++=0;*下一项目=机器字文本;return 初始项目;}
unsigned long strtoul(const char *机器字文本, char **结尾, int 基底值) {
    const char *源代码=机器字文本;unsigned long 值=0;int 负数值=0,溢出值=0;
    while(*机器字文本==' '||(*机器字文本>=9&&*机器字文本<=13))机器字文本++;
    if(*机器字文本=='-'||*机器字文本=='+')负数值=*机器字文本++=='-';
    if((基底值==0||基底值==16)&&机器字文本[0]=='0'&&(机器字文本[1]=='x'||机器字文本[1]=='X')&&
       ((机器字文本[2]>='0'&&机器字文本[2]<='9')||(机器字文本[2]>='a'&&机器字文本[2]<='f')||(机器字文本[2]>='A'&&机器字文本[2]<='F'))) {基底值=16;机器字文本+=2;}
    if(!基底值)基底值=*机器字文本=='0'?8:10;
    if(基底值<2||基底值>36){if(结尾)*结尾=(char*)源代码;return 0;}
    const char *初始项目=机器字文本;
    for(;;机器字文本++) {
        unsigned 字符值=(unsigned char)*机器字文本;
        unsigned 数=字符值>='0'&&字符值<='9'?字符值-'0':字符值>='a'&&字符值<='z'?字符值-'a'+10:字符值>='A'&&字符值<='Z'?字符值-'A'+10:36;
        if(数>=(unsigned)基底值)break;
        if(值>(~0ul-数)/(unsigned)基底值)溢出值=1;
        if(!溢出值)值=值*(unsigned)基底值+数;
    }
    if(结尾)*结尾=(char*)(机器字文本==初始项目?源代码:机器字文本);
    return 溢出值?~0ul:负数值?0ul-值:值;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char 测试替身种子[32];
static int 种子状态;
void 远程摘要(const void *数据, size_t 长度, unsigned char 结果[32]) {
    br_sha256_context 上下文值;
    br_sha256_init(&上下文值); br_sha256_update(&上下文值, 数据, 长度); br_sha256_out(&上下文值, 结果);
    memset(&上下文值, 0, sizeof(上下文值));
}
#define 随机寄存器集(位置) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(位置)))
int 远程随机(unsigned char *目的地址值,unsigned 长度){
    if(!种子状态){volatile unsigned char *数据=(void*)0x01ff0000ul;const char *标记值="JKRENRG1";unsigned 差异值=0;
        for(unsigned 序数索引=0;序数索引<8;序数索引++)差异值|=数据[序数索引]^(unsigned char)标记值[序数索引];
        if(!差异值){for(unsigned 序数索引=0;序数索引<32;序数索引++)测试替身种子[序数索引]=数据[8+序数索引];for(unsigned 序数索引=0;序数索引<40;序数索引++)数据[序数索引]=0;种子状态=2;}
        else {种子状态=1;随机寄存器集(0)=(随机寄存器集(0)&~0x1fffu)|1;}
    }
    if(种子状态==2){while(长度){unsigned char 下一项目[32],输入值[33];memcpy(输入值,测试替身种子,32);输入值[32]=0;远程摘要(输入值,33,下一项目);
        输入值[32]=1;远程摘要(输入值,33,测试替身种子);memset(输入值,0,33);
        unsigned 数=长度<32?长度:32;memcpy(目的地址值,下一项目,数);memset(下一项目,0,32);目的地址值+=数;长度-=数;}return 0;}
    uintptr_t 限制值=板经过毫秒()+1000;
    while(长度){if((随机寄存器集(0x18)&0x80000020u)||板经过毫秒()>限制值)return -1;
        if(!(随机寄存器集(0x24)&255))continue;uint32_t 值=随机寄存器集(0x20);
        for(unsigned 序数索引=0;序数索引<4&&长度;序数索引++,长度--){*目的地址值++=值&255;值>>=8;}}
    return 0;
}
