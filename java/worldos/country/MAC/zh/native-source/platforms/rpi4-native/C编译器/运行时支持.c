#include "../命名/计算机连接名称列.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "调用.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int 错误;
int *__errno_location(void){return &错误;}
void exit(int 状态值){用户调用(6,状态值,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *检查表达式,const char *文件,unsigned 行,const char *方法条目名称){fprintf(stderr,"cc assertion: %s %s:%u %s\n",检查表达式,文件,行,方法条目名称);exit(1);}
size_t strlen(const char*字符串数据){const char*数据位置=字符串数据;while(*数据位置)数据位置++;return 数据位置-字符串数据;}
int strcmp(const char*首位值,const char*第二值){while(*首位值&&*首位值==*第二值){首位值++;第二值++;}return (unsigned char)*首位值-(unsigned char)*第二值;}
int strncmp(const char*首位值,const char*第二值,size_t 项目个数){while(项目个数--){unsigned char 横坐标坐标=*首位值++,Y_按钮坐标=*第二值++;if(横坐标坐标!=Y_按钮坐标)return 横坐标坐标-Y_按钮坐标;if(!横坐标坐标)return 0;}return 0;}
char *strcpy(char*目的地址数据,const char*字符串数据){char*已返回值=目的地址数据;while((*目的地址数据++=*字符串数据++)){}return 已返回值;}
char *strchr(const char*字符串数据,int 字符代码){do{if(*字符串数据==(char)字符代码)return (char*)字符串数据;}while(*字符串数据++);return 0;}
char *strrchr(const char*字符串数据,int 字符代码){const char*已返回值=0;do{if(*字符串数据==(char)字符代码)已返回值=字符串数据;}while(*字符串数据++);return (char*)已返回值;}
char *strstr(const char*字符串数据,const char*终端条目){size_t 项目个数=strlen(终端条目);for(;*字符串数据;字符串数据++)if(!strncmp(字符串数据,终端条目,项目个数))return (char*)字符串数据;return 项目个数?0:(char*)字符串数据;}
int memcmp(const void*首位值,const void*第二值,size_t 项目个数){const unsigned char*横坐标坐标=首位值,*Y_按钮坐标=第二值;while(项目个数--){if(*横坐标坐标!=*Y_按钮坐标)return *横坐标坐标-*Y_按钮坐标;横坐标坐标++;Y_按钮坐标++;}return 0;}
void *memmove(void*目的地址数据,const void*字符串数据,size_t 项目个数){unsigned char*横坐标坐标=目的地址数据;const unsigned char*Y_按钮坐标=字符串数据;if(横坐标坐标<Y_按钮坐标){for(size_t 序数索引=0;序数索引<项目个数;序数索引++)横坐标坐标[序数索引]=Y_按钮坐标[序数索引];}else while(项目个数){项目个数--;横坐标坐标[项目个数]=Y_按钮坐标[项目个数];}return 目的地址数据;}
static unsigned char 分配状态连续区[6*1024*1024] __attribute__((aligned(16)));
typedef struct 数据块 {size_t 大小;struct 数据块*下一项目;int 剩余容量;int 衬垫;uint64_t 对齐方式单位;} 数据块;
static 数据块 *首位条目;
void free(void*数据位置){if(!数据位置)return;数据块*第二值=(数据块*)数据位置-1;第二值->剩余容量=1;for(数据块*下一偏移=首位条目;下一偏移&&下一偏移->下一项目;){if(下一偏移->剩余容量&&下一偏移->下一项目->剩余容量){下一偏移->大小+=sizeof(数据块)+下一偏移->下一项目->大小;下一偏移->下一项目=下一偏移->下一项目->下一项目;}else 下一偏移=下一偏移->下一项目;}}
void *realloc(void*数据位置,size_t 项目个数){
    if(!项目个数){free(数据位置);return 0;}if(项目个数>sizeof(分配状态连续区)-sizeof(数据块))return 0;项目个数=(项目个数+15)&~(size_t)15;
    if(!首位条目){首位条目=(数据块*)分配状态连续区;首位条目->大小=sizeof(分配状态连续区)-sizeof(数据块);首位条目->剩余容量=1;首位条目->下一项目=0;}
    数据块*上一个项目=数据位置?(数据块*)数据位置-1:0;if(上一个项目&&上一个项目->大小>=项目个数)return 数据位置;
    for(数据块*第二值=首位条目;第二值;第二值=第二值->下一项目)if(第二值->剩余容量&&第二值->大小>=项目个数){
        if(第二值->大小>=项目个数+sizeof(数据块)+16){数据块*剩余部分=(数据块*)((unsigned char*)(第二值+1)+项目个数);剩余部分->大小=第二值->大小-项目个数-sizeof(数据块);剩余部分->下一项目=第二值->下一项目;剩余部分->剩余容量=1;第二值->下一项目=剩余部分;第二值->大小=项目个数;}
        第二值->剩余容量=0;void*已返回值=第二值+1;if(上一个项目){memcpy(已返回值,数据位置,上一个项目->大小);free(数据位置);}return 已返回值;
    }错误=12;return 0;
}
void *malloc(size_t 项目个数){return realloc(0,项目个数);}
void *calloc(size_t 项目个数,size_t 字符串数据){if(字符串数据&&项目个数>SIZE_MAX/字符串数据)return 0;void*数据位置=malloc(项目个数*字符串数据);if(数据位置)memset(数据位置,0,项目个数*字符串数据);return 数据位置;}
unsigned long long strtoull(const char*字符串数据,char**结束偏移,int 背景值){
    const char*开始偏移=字符串数据;while(*字符串数据==' '||(*字符串数据>=9&&*字符串数据<=13))字符串数据++;int 是否负数=0;if(*字符串数据=='-'||*字符串数据=='+')是否负数=*字符串数据++=='-';
    if((!背景值||背景值==16)&&字符串数据[0]=='0'&&(字符串数据[1]=='x'||字符串数据[1]=='X')){背景值=16;字符串数据+=2;}if(!背景值)背景值=*字符串数据=='0'?8:10;
    unsigned long long 临时数据=0;int 任意值=0;for(;;){unsigned 字符代码=*字符串数据,目的地址数据=字符代码>='0'&&字符代码<='9'?字符代码-'0':字符代码>='a'&&字符代码<='z'?字符代码-'a'+10:字符代码>='A'&&字符代码<='Z'?字符代码-'A'+10:99;if(目的地址数据>=(unsigned)背景值)break;任意值=1;字符串数据++;if(临时数据>(~0ull-目的地址数据)/(unsigned)背景值){临时数据=~0ull;错误=34;}else 临时数据=临时数据*背景值+目的地址数据;}
    if(结束偏移)*结束偏移=(char*)(任意值?字符串数据:开始偏移);return 是否负数?0-临时数据:临时数据;
}
unsigned long strtoul(const char*字符串数据,char**辅助条目,int 第二值){return strtoull(字符串数据,辅助条目,第二值);}
long strtol(const char*字符串数据,char**辅助条目,int 第二值){return (long)strtoull(字符串数据,辅助条目,第二值);}
int atoi(const char*字符串数据){return (int)strtol(字符串数据,0,10);}
long double ldexpl(long double 横坐标坐标,int 项目个数){while(项目个数>0){横坐标坐标*=2;项目个数--;}while(项目个数<0){横坐标坐标/=2;项目个数++;}return 横坐标坐标;}
long double strtold(const char*字符串数据,char**结束偏移){
    const char*开始偏移=字符串数据;while(*字符串数据==' '||(*字符串数据>=9&&*字符串数据<=13))字符串数据++;int 是否负数=0;if(*字符串数据=='-'||*字符串数据=='+')是否负数=*字符串数据++=='-';
    int 背景值=10;if(字符串数据[0]=='0'&&(字符串数据[1]=='x'||字符串数据[1]=='X')){背景值=16;字符串数据+=2;}long double 临时数据=0,比例=1;int 小数部分=0,任意值=0;
    for(;;){int 字符代码=*字符串数据,目的地址数据=字符代码>='0'&&字符代码<='9'?字符代码-'0':字符代码>='a'&&字符代码<='f'?字符代码-'a'+10:字符代码>='A'&&字符代码<='F'?字符代码-'A'+10:99;
        if(字符代码=='.'&&!小数部分){小数部分=1;字符串数据++;continue;}if(目的地址数据>=背景值)break;任意值=1;字符串数据++;临时数据=临时数据*背景值+目的地址数据;if(小数部分)比例*=背景值;
    }临时数据/=比例;
    if((背景值==10&&(*字符串数据=='e'||*字符串数据=='E'))||(背景值==16&&(*字符串数据=='p'||*字符串数据=='P'))){const char*显示值=字符串数据++;int 减法值列=0;if(*字符串数据=='-'||*字符串数据=='+')减法值列=*字符串数据++=='-';int 项目个数=0,条目个数=0;while(*字符串数据>='0'&&*字符串数据<='9'){条目个数++;if(项目个数<20000)项目个数=项目个数*10+*字符串数据-'0';字符串数据++;}if(!条目个数)字符串数据=显示值;else{long double 系数=背景值==16?2:10;while(项目个数-->0&&项目个数<200000)临时数据=减法值列?临时数据/系数:临时数据*系数;}}
    if(结束偏移)*结束偏移=(char*)(任意值?字符串数据:开始偏移);return 是否负数?-临时数据:临时数据;
}
double strtod(const char*字符串数据,char**辅助条目){return (double)strtold(字符串数据,辅助条目);}float strtof(const char*字符串数据,char**辅助条目){return (float)strtold(字符串数据,辅助条目);}
void qsort(void*背景值,size_t 项目个数,size_t 大小,int(*比较)(const void*,const void*)){
    unsigned char*数据位置=背景值;for(size_t 序数索引=1;序数索引<项目个数;序数索引++)for(size_t 内部侧序数=序数索引;内部侧序数&&比较(数据位置+(内部侧序数-1)*大小,数据位置+内部侧序数*大小)>0;内部侧序数--)for(size_t 第三索引=0;第三索引<大小;第三索引++){unsigned char 字符代码=数据位置[(内部侧序数-1)*大小+第三索引];数据位置[(内部侧序数-1)*大小+第三索引]=数据位置[内部侧序数*大小+第三索引];数据位置[内部侧序数*大小+第三索引]=字符代码;}
}
static struct {int 已使用容量,查找索引;size_t 位置;} 已打开[24];
static unsigned char 输出结果[32768];static size_t 输出大小,输出位置;static int 输出打开;
const unsigned char *C输出(size_t *项目个数){*项目个数=输出大小;return 输出结果;}
int open(const char*名称,int 配置项位列,...){
    if(!strcmp(名称,"/@cc-output")){if(输出打开){错误=16;return -1;}输出打开=1;输出大小=输出位置=0;return 100;}
    for(unsigned 序数索引=0;序数索引<sizeof(编译器资源集)/sizeof(编译器资源集[0]);序数索引++)if(!strcmp(名称,编译器资源集[序数索引].名称)){
        if(配置项位列&3){错误=30;return -1;}for(int 内部侧序数=0;内部侧序数<24;内部侧序数++)if(!已打开[内部侧序数].已使用容量){已打开[内部侧序数].已使用容量=1;已打开[内部侧序数].查找索引=序数索引;已打开[内部侧序数].位置=0;return 128+内部侧序数;}错误=24;return -1;
    }
    intptr_t 已返回值=用户调用(3,(uintptr_t)名称,配置项位列,0,0,0,0);if(已返回值<0){错误=-已返回值;return -1;}return 已返回值;
}
int close(int 文件句柄){if(文件句柄==100){输出打开=0;return 0;}if(文件句柄>=128&&文件句柄<152){已打开[文件句柄-128].已使用容量=0;return 0;}intptr_t 已返回值=用户调用(4,文件句柄,0,0,0,0,0);if(已返回值<0){错误=-已返回值;return -1;}return 0;}
long read(int 文件句柄,void*数据,size_t 项目个数){
    if(文件句柄>=128&&文件句柄<152&&已打开[文件句柄-128].已使用容量){int 序数索引=文件句柄-128;const 编译器资源*已返回值=&编译器资源集[已打开[序数索引].查找索引];size_t 左侧=已返回值->大小-已打开[序数索引].位置;if(项目个数>左侧)项目个数=左侧;memcpy(数据,已返回值->数据+已打开[序数索引].位置,项目个数);已打开[序数索引].位置+=项目个数;return 项目个数;}
    intptr_t 已返回值=用户调用(2,文件句柄,(uintptr_t)数据,项目个数,0,0,0);if(已返回值<0){错误=-已返回值;return -1;}return 已返回值;
}
long write(int 文件句柄,const void*数据,size_t 项目个数){
    if(文件句柄==100){if(项目个数>sizeof(输出结果)-输出位置){错误=28;return -1;}memcpy(输出结果+输出位置,数据,项目个数);输出位置+=项目个数;if(输出大小<输出位置)输出大小=输出位置;return 项目个数;}
    intptr_t 已返回值=用户调用(1,文件句柄,(uintptr_t)数据,项目个数,0,0,0);if(已返回值<0){错误=-已返回值;return -1;}return 已返回值;
}
long lseek(int 文件句柄,long 偏移值,int 寻道原点){
    if(文件句柄==100){long 数据位置=偏移值+(寻道原点==0?0:寻道原点==1?输出位置:输出大小);if(数据位置<0||(size_t)数据位置>sizeof(输出结果)){错误=22;return -1;}输出位置=数据位置;return 数据位置;}
    if(文件句柄>=128&&文件句柄<152&&已打开[文件句柄-128].已使用容量){int 序数索引=文件句柄-128;long 数据位置=偏移值+(寻道原点==0?0:寻道原点==1?已打开[序数索引].位置:编译器资源集[已打开[序数索引].查找索引].大小);if(数据位置<0||(size_t)数据位置>编译器资源集[已打开[序数索引].查找索引].大小){错误=22;return -1;}已打开[序数索引].位置=数据位置;return 数据位置;}
    intptr_t 已返回值=用户调用(5,文件句柄,偏移值,寻道原点,0,0,0);if(已返回值<0){错误=-已返回值;return -1;}return 已返回值;
}
int unlink(const char*名称){intptr_t 已返回值=用户调用(11,(uintptr_t)名称,0,0,0,0,0);if(已返回值<0){错误=-已返回值;return -1;}return 已返回值;}
char *realpath(const char*名称,char*结果数据){if(!结果数据){结果数据=malloc(strlen(名称)+1);if(!结果数据)return 0;}return strcpy(结果数据,名称);}
char *getcwd(char*数据位置,size_t 项目个数){if(项目个数<2){错误=34;return 0;}数据位置[0]='/';数据位置[1]=0;return 数据位置;}
char *strerror(int 辅助条目){(void)辅助条目;return "native compiler I/O error";}
time_t time(time_t*终端条目){time_t 临时数据=0;if(终端条目)*终端条目=临时数据;return 临时数据;}
struct tm *localtime(const time_t*终端条目){(void)终端条目;static struct tm 临时数据={.tm_year=126,.tm_mon=0,.tm_mday=1};return &临时数据;}
static FILE 数据流集[18]={{1,0,1},{2,0,1}};FILE*stdout=&数据流集[0],*stderr=&数据流集[1];
FILE*fdopen(int 文件句柄,const char*方法模式){(void)方法模式;for(unsigned 序数索引=2;序数索引<18;序数索引++)if(!数据流集[序数索引].已使用容量){数据流集[序数索引].已使用容量=1;数据流集[序数索引].错误=0;数据流集[序数索引].文件句柄=文件句柄;return &数据流集[序数索引];}错误=24;return 0;}
int fflush(FILE*文件条目){return 文件条目&&文件条目->错误?-1:0;}
int fclose(FILE*文件条目){int 已返回值=close(文件条目->文件句柄);if(文件条目->错误)已返回值=-1;文件条目->已使用容量=0;return 已返回值;}
size_t fwrite(const void*数据位置,size_t 字符串数据,size_t 项目个数,FILE*文件条目){if(!字符串数据)return 0;if(项目个数>SIZE_MAX/字符串数据){文件条目->错误=1;return 0;}long 已返回值=write(文件条目->文件句柄,数据位置,字符串数据*项目个数);if(已返回值<0){文件条目->错误=1;return 0;}return (size_t)已返回值/字符串数据;}
int fputc(int 字符代码,FILE*文件条目){unsigned char 第二值=字符代码;return fwrite(&第二值,1,1,文件条目)==1?第二值:EOF;}
int fputs(const char*字符串数据,FILE*文件条目){return fwrite(字符串数据,1,strlen(字符串数据),文件条目)==strlen(字符串数据)?0:EOF;}
static void 放入值(char*结果数据,size_t 容量最大,size_t*当前位置,char 字符代码){if(*当前位置+1<容量最大)结果数据[*当前位置]=字符代码;(*当前位置)++;}
int vsnprintf(char*结果数据,size_t 容量最大,const char*格式,va_list 可变参数参数列){
    size_t 当前位置=0;while(*格式){if(*格式!='%'){放入值(结果数据,容量最大,&当前位置,*格式++);continue;}格式++;
        int 左侧=0,零值=0,回退值=0;while(*格式=='-'||*格式=='0'||*格式=='#'||*格式=='+'||*格式==' '){if(*格式=='-')左侧=1;if(*格式=='0')零值=1;if(*格式=='#')回退值=1;格式++;}
        int 宽度值=0,精度值=-1;if(*格式=='*'){宽度值=va_arg(可变参数参数列,int);格式++;}else while(*格式>='0'&&*格式<='9')宽度值=宽度值*10+*格式++-'0';
        if(*格式=='.'){格式++;精度值=0;if(*格式=='*'){精度值=va_arg(可变参数参数列,int);格式++;}else while(*格式>='0'&&*格式<='9')精度值=精度值*10+*格式++-'0';}
        int 宽幅字符=0;while(*格式=='l'||*格式=='z'||*格式=='t'||*格式=='j'||*格式=='h'){if(*格式!='h')宽幅字符=1;格式++;}
        char 类型分类=*格式?*格式++:0,缓冲存储装置[80];const char*字符串数据=缓冲存储装置;size_t 项目个数=0;
        if(类型分类=='s'){字符串数据=va_arg(可变参数参数列,const char*);if(!字符串数据)字符串数据="(null)";项目个数=strlen(字符串数据);if(精度值>=0&&项目个数>(size_t)精度值)项目个数=精度值;}
        else if(类型分类=='c'){缓冲存储装置[0]=va_arg(可变参数参数列,int);项目个数=1;}
        else if(类型分类=='%'){缓冲存储装置[0]='%';项目个数=1;}
        else if(类型分类=='d'||类型分类=='i'||类型分类=='u'||类型分类=='x'||类型分类=='X'||类型分类=='o'||类型分类=='p'){
            unsigned long long 值;int 负数=0;
            if(类型分类=='d'||类型分类=='i'){long long 临时数据=宽幅字符?va_arg(可变参数参数列,long long):va_arg(可变参数参数列,int);负数=临时数据<0;值=负数?0-(unsigned long long)临时数据:临时数据;}
            else 值=类型分类=='p'?(uintptr_t)va_arg(可变参数参数列,void*):宽幅字符?va_arg(可变参数参数列,unsigned long long):va_arg(可变参数参数列,unsigned);
            unsigned 背景值=类型分类=='x'||类型分类=='X'||类型分类=='p'?16:类型分类=='o'?8:10;char 数字个数[64];unsigned 已使用容量=0;
            do{数字个数[已使用容量++]="0123456789abcdef"[值%背景值];值/=背景值;}while(值);
            if(负数)缓冲存储装置[项目个数++]='-';if(类型分类=='p'||(回退值&&背景值==16)){缓冲存储装置[项目个数++]='0';缓冲存储装置[项目个数++]='x';}
            for(int 填充值=(int)已使用容量;精度值>填充值&&项目个数<sizeof(缓冲存储装置)-已使用容量;填充值++)缓冲存储装置[项目个数++]='0';
            if(零值&&!左侧&&精度值<0)while(宽度值>(int)(项目个数+已使用容量)&&项目个数<sizeof(缓冲存储装置)-已使用容量)缓冲存储装置[项目个数++]='0';
            while(已使用容量)缓冲存储装置[项目个数++]=数字个数[--已使用容量];
        }else{缓冲存储装置[0]='?';项目个数=1;}
        if(宽度值>4096)宽度值=4096;while(!左侧&&宽度值>(int)项目个数){放入值(结果数据,容量最大,&当前位置,' ');宽度值--;}
        for(size_t 序数索引=0;序数索引<项目个数;序数索引++)放入值(结果数据,容量最大,&当前位置,字符串数据[序数索引]);while(左侧&&宽度值>(int)项目个数){放入值(结果数据,容量最大,&当前位置,' ');宽度值--;}
    }if(容量最大)结果数据[当前位置<容量最大?当前位置:容量最大-1]=0;return 当前位置;
}
int snprintf(char*结果数据,size_t 容量最大,const char*文件条目,...){va_list 首位值;va_start(首位值,文件条目);int 已返回值=vsnprintf(结果数据,容量最大,文件条目,首位值);va_end(首位值);return 已返回值;}
int sprintf(char*结果数据,const char*文件条目,...){va_list 首位值;va_start(首位值,文件条目);int 已返回值=vsnprintf(结果数据,SIZE_MAX,文件条目,首位值);va_end(首位值);return 已返回值;}
int vfprintf(FILE*流值,const char*文件条目,va_list 首位值){char 第二值[2048];int 项目个数=vsnprintf(第二值,sizeof(第二值),文件条目,首位值);if(项目个数>2047)项目个数=2047;return fwrite(第二值,1,项目个数,流值)==(size_t)项目个数?项目个数:-1;}
int fprintf(FILE*流值,const char*文件条目,...){va_list 首位值;va_start(首位值,文件条目);int 已返回值=vfprintf(流值,文件条目,首位值);va_end(首位值);return 已返回值;}
int printf(const char*文件条目,...){va_list 首位值;va_start(首位值,文件条目);int 已返回值=vfprintf(stdout,文件条目,首位值);va_end(首位值);return 已返回值;}
