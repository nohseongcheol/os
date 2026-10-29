#include "../命名/計算機連接名稱列.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "調用.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int 錯誤;
int *__errno_location(void){return &錯誤;}
void exit(int 狀態值){用戶調用(6,狀態值,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *檢查表達式,const char *檔案,unsigned 行,const char *方法條目名稱){fprintf(stderr,"cc assertion: %s %s:%u %s\n",檢查表達式,檔案,行,方法條目名稱);exit(1);}
size_t strlen(const char*字符串資料){const char*資料位置=字符串資料;while(*資料位置)資料位置++;return 資料位置-字符串資料;}
int strcmp(const char*首位值,const char*第二值){while(*首位值&&*首位值==*第二值){首位值++;第二值++;}return (unsigned char)*首位值-(unsigned char)*第二值;}
int strncmp(const char*首位值,const char*第二值,size_t 項目個數){while(項目個數--){unsigned char 橫座標座標=*首位值++,Y_按鈕座標=*第二值++;if(橫座標座標!=Y_按鈕座標)return 橫座標座標-Y_按鈕座標;if(!橫座標座標)return 0;}return 0;}
char *strcpy(char*目的地址資料,const char*字符串資料){char*已返回值=目的地址資料;while((*目的地址資料++=*字符串資料++)){}return 已返回值;}
char *strchr(const char*字符串資料,int 字元程式碼){do{if(*字符串資料==(char)字元程式碼)return (char*)字符串資料;}while(*字符串資料++);return 0;}
char *strrchr(const char*字符串資料,int 字元程式碼){const char*已返回值=0;do{if(*字符串資料==(char)字元程式碼)已返回值=字符串資料;}while(*字符串資料++);return (char*)已返回值;}
char *strstr(const char*字符串資料,const char*終端條目){size_t 項目個數=strlen(終端條目);for(;*字符串資料;字符串資料++)if(!strncmp(字符串資料,終端條目,項目個數))return (char*)字符串資料;return 項目個數?0:(char*)字符串資料;}
int memcmp(const void*首位值,const void*第二值,size_t 項目個數){const unsigned char*橫座標座標=首位值,*Y_按鈕座標=第二值;while(項目個數--){if(*橫座標座標!=*Y_按鈕座標)return *橫座標座標-*Y_按鈕座標;橫座標座標++;Y_按鈕座標++;}return 0;}
void *memmove(void*目的地址資料,const void*字符串資料,size_t 項目個數){unsigned char*橫座標座標=目的地址資料;const unsigned char*Y_按鈕座標=字符串資料;if(橫座標座標<Y_按鈕座標){for(size_t 序數索引=0;序數索引<項目個數;序數索引++)橫座標座標[序數索引]=Y_按鈕座標[序數索引];}else while(項目個數){項目個數--;橫座標座標[項目個數]=Y_按鈕座標[項目個數];}return 目的地址資料;}
static unsigned char 分配狀態連續區[6*1024*1024] __attribute__((aligned(16)));
typedef struct 資料塊 {size_t 大小;struct 資料塊*下一項目;int 剩餘容量;int 襯墊;uint64_t 對齊方式單位;} 資料塊;
static 資料塊 *首位條目;
void free(void*資料位置){if(!資料位置)return;資料塊*第二值=(資料塊*)資料位置-1;第二值->剩餘容量=1;for(資料塊*下一偏移=首位條目;下一偏移&&下一偏移->下一項目;){if(下一偏移->剩餘容量&&下一偏移->下一項目->剩餘容量){下一偏移->大小+=sizeof(資料塊)+下一偏移->下一項目->大小;下一偏移->下一項目=下一偏移->下一項目->下一項目;}else 下一偏移=下一偏移->下一項目;}}
void *realloc(void*資料位置,size_t 項目個數){
    if(!項目個數){free(資料位置);return 0;}if(項目個數>sizeof(分配狀態連續區)-sizeof(資料塊))return 0;項目個數=(項目個數+15)&~(size_t)15;
    if(!首位條目){首位條目=(資料塊*)分配狀態連續區;首位條目->大小=sizeof(分配狀態連續區)-sizeof(資料塊);首位條目->剩餘容量=1;首位條目->下一項目=0;}
    資料塊*上一個項目=資料位置?(資料塊*)資料位置-1:0;if(上一個項目&&上一個項目->大小>=項目個數)return 資料位置;
    for(資料塊*第二值=首位條目;第二值;第二值=第二值->下一項目)if(第二值->剩餘容量&&第二值->大小>=項目個數){
        if(第二值->大小>=項目個數+sizeof(資料塊)+16){資料塊*剩餘部分=(資料塊*)((unsigned char*)(第二值+1)+項目個數);剩餘部分->大小=第二值->大小-項目個數-sizeof(資料塊);剩餘部分->下一項目=第二值->下一項目;剩餘部分->剩餘容量=1;第二值->下一項目=剩餘部分;第二值->大小=項目個數;}
        第二值->剩餘容量=0;void*已返回值=第二值+1;if(上一個項目){memcpy(已返回值,資料位置,上一個項目->大小);free(資料位置);}return 已返回值;
    }錯誤=12;return 0;
}
void *malloc(size_t 項目個數){return realloc(0,項目個數);}
void *calloc(size_t 項目個數,size_t 字符串資料){if(字符串資料&&項目個數>SIZE_MAX/字符串資料)return 0;void*資料位置=malloc(項目個數*字符串資料);if(資料位置)memset(資料位置,0,項目個數*字符串資料);return 資料位置;}
unsigned long long strtoull(const char*字符串資料,char**結束偏移,int 背景值){
    const char*開始偏移=字符串資料;while(*字符串資料==' '||(*字符串資料>=9&&*字符串資料<=13))字符串資料++;int 是否負數=0;if(*字符串資料=='-'||*字符串資料=='+')是否負數=*字符串資料++=='-';
    if((!背景值||背景值==16)&&字符串資料[0]=='0'&&(字符串資料[1]=='x'||字符串資料[1]=='X')){背景值=16;字符串資料+=2;}if(!背景值)背景值=*字符串資料=='0'?8:10;
    unsigned long long 臨時資料=0;int 任意值=0;for(;;){unsigned 字元程式碼=*字符串資料,目的地址資料=字元程式碼>='0'&&字元程式碼<='9'?字元程式碼-'0':字元程式碼>='a'&&字元程式碼<='z'?字元程式碼-'a'+10:字元程式碼>='A'&&字元程式碼<='Z'?字元程式碼-'A'+10:99;if(目的地址資料>=(unsigned)背景值)break;任意值=1;字符串資料++;if(臨時資料>(~0ull-目的地址資料)/(unsigned)背景值){臨時資料=~0ull;錯誤=34;}else 臨時資料=臨時資料*背景值+目的地址資料;}
    if(結束偏移)*結束偏移=(char*)(任意值?字符串資料:開始偏移);return 是否負數?0-臨時資料:臨時資料;
}
unsigned long strtoul(const char*字符串資料,char**輔助條目,int 第二值){return strtoull(字符串資料,輔助條目,第二值);}
long strtol(const char*字符串資料,char**輔助條目,int 第二值){return (long)strtoull(字符串資料,輔助條目,第二值);}
int atoi(const char*字符串資料){return (int)strtol(字符串資料,0,10);}
long double ldexpl(long double 橫座標座標,int 項目個數){while(項目個數>0){橫座標座標*=2;項目個數--;}while(項目個數<0){橫座標座標/=2;項目個數++;}return 橫座標座標;}
long double strtold(const char*字符串資料,char**結束偏移){
    const char*開始偏移=字符串資料;while(*字符串資料==' '||(*字符串資料>=9&&*字符串資料<=13))字符串資料++;int 是否負數=0;if(*字符串資料=='-'||*字符串資料=='+')是否負數=*字符串資料++=='-';
    int 背景值=10;if(字符串資料[0]=='0'&&(字符串資料[1]=='x'||字符串資料[1]=='X')){背景值=16;字符串資料+=2;}long double 臨時資料=0,比例=1;int 小數部分=0,任意值=0;
    for(;;){int 字元程式碼=*字符串資料,目的地址資料=字元程式碼>='0'&&字元程式碼<='9'?字元程式碼-'0':字元程式碼>='a'&&字元程式碼<='f'?字元程式碼-'a'+10:字元程式碼>='A'&&字元程式碼<='F'?字元程式碼-'A'+10:99;
        if(字元程式碼=='.'&&!小數部分){小數部分=1;字符串資料++;continue;}if(目的地址資料>=背景值)break;任意值=1;字符串資料++;臨時資料=臨時資料*背景值+目的地址資料;if(小數部分)比例*=背景值;
    }臨時資料/=比例;
    if((背景值==10&&(*字符串資料=='e'||*字符串資料=='E'))||(背景值==16&&(*字符串資料=='p'||*字符串資料=='P'))){const char*顯示值=字符串資料++;int 減法值列=0;if(*字符串資料=='-'||*字符串資料=='+')減法值列=*字符串資料++=='-';int 項目個數=0,條目個數=0;while(*字符串資料>='0'&&*字符串資料<='9'){條目個數++;if(項目個數<20000)項目個數=項目個數*10+*字符串資料-'0';字符串資料++;}if(!條目個數)字符串資料=顯示值;else{long double 係數=背景值==16?2:10;while(項目個數-->0&&項目個數<200000)臨時資料=減法值列?臨時資料/係數:臨時資料*係數;}}
    if(結束偏移)*結束偏移=(char*)(任意值?字符串資料:開始偏移);return 是否負數?-臨時資料:臨時資料;
}
double strtod(const char*字符串資料,char**輔助條目){return (double)strtold(字符串資料,輔助條目);}float strtof(const char*字符串資料,char**輔助條目){return (float)strtold(字符串資料,輔助條目);}
void qsort(void*背景值,size_t 項目個數,size_t 大小,int(*比較)(const void*,const void*)){
    unsigned char*資料位置=背景值;for(size_t 序數索引=1;序數索引<項目個數;序數索引++)for(size_t 內部側序數=序數索引;內部側序數&&比較(資料位置+(內部側序數-1)*大小,資料位置+內部側序數*大小)>0;內部側序數--)for(size_t 第三索引=0;第三索引<大小;第三索引++){unsigned char 字元程式碼=資料位置[(內部側序數-1)*大小+第三索引];資料位置[(內部側序數-1)*大小+第三索引]=資料位置[內部側序數*大小+第三索引];資料位置[內部側序數*大小+第三索引]=字元程式碼;}
}
static struct {int 已使用容量,查找索引;size_t 位置;} 已打開[24];
static unsigned char 輸出結果[32768];static size_t 輸出大小,輸出位置;static int 輸出打開;
const unsigned char *C輸出(size_t *項目個數){*項目個數=輸出大小;return 輸出結果;}
int open(const char*名稱,int 配置項位元列,...){
    if(!strcmp(名稱,"/@cc-output")){if(輸出打開){錯誤=16;return -1;}輸出打開=1;輸出大小=輸出位置=0;return 100;}
    for(unsigned 序數索引=0;序數索引<sizeof(編譯器資源集)/sizeof(編譯器資源集[0]);序數索引++)if(!strcmp(名稱,編譯器資源集[序數索引].名稱)){
        if(配置項位元列&3){錯誤=30;return -1;}for(int 內部側序數=0;內部側序數<24;內部側序數++)if(!已打開[內部側序數].已使用容量){已打開[內部側序數].已使用容量=1;已打開[內部側序數].查找索引=序數索引;已打開[內部側序數].位置=0;return 128+內部側序數;}錯誤=24;return -1;
    }
    intptr_t 已返回值=用戶調用(3,(uintptr_t)名稱,配置項位元列,0,0,0,0);if(已返回值<0){錯誤=-已返回值;return -1;}return 已返回值;
}
int close(int 檔案句柄){if(檔案句柄==100){輸出打開=0;return 0;}if(檔案句柄>=128&&檔案句柄<152){已打開[檔案句柄-128].已使用容量=0;return 0;}intptr_t 已返回值=用戶調用(4,檔案句柄,0,0,0,0,0);if(已返回值<0){錯誤=-已返回值;return -1;}return 0;}
long read(int 檔案句柄,void*資料,size_t 項目個數){
    if(檔案句柄>=128&&檔案句柄<152&&已打開[檔案句柄-128].已使用容量){int 序數索引=檔案句柄-128;const 編譯器資源*已返回值=&編譯器資源集[已打開[序數索引].查找索引];size_t 左側=已返回值->大小-已打開[序數索引].位置;if(項目個數>左側)項目個數=左側;memcpy(資料,已返回值->資料+已打開[序數索引].位置,項目個數);已打開[序數索引].位置+=項目個數;return 項目個數;}
    intptr_t 已返回值=用戶調用(2,檔案句柄,(uintptr_t)資料,項目個數,0,0,0);if(已返回值<0){錯誤=-已返回值;return -1;}return 已返回值;
}
long write(int 檔案句柄,const void*資料,size_t 項目個數){
    if(檔案句柄==100){if(項目個數>sizeof(輸出結果)-輸出位置){錯誤=28;return -1;}memcpy(輸出結果+輸出位置,資料,項目個數);輸出位置+=項目個數;if(輸出大小<輸出位置)輸出大小=輸出位置;return 項目個數;}
    intptr_t 已返回值=用戶調用(1,檔案句柄,(uintptr_t)資料,項目個數,0,0,0);if(已返回值<0){錯誤=-已返回值;return -1;}return 已返回值;
}
long lseek(int 檔案句柄,long 偏移值,int 尋道原點){
    if(檔案句柄==100){long 資料位置=偏移值+(尋道原點==0?0:尋道原點==1?輸出位置:輸出大小);if(資料位置<0||(size_t)資料位置>sizeof(輸出結果)){錯誤=22;return -1;}輸出位置=資料位置;return 資料位置;}
    if(檔案句柄>=128&&檔案句柄<152&&已打開[檔案句柄-128].已使用容量){int 序數索引=檔案句柄-128;long 資料位置=偏移值+(尋道原點==0?0:尋道原點==1?已打開[序數索引].位置:編譯器資源集[已打開[序數索引].查找索引].大小);if(資料位置<0||(size_t)資料位置>編譯器資源集[已打開[序數索引].查找索引].大小){錯誤=22;return -1;}已打開[序數索引].位置=資料位置;return 資料位置;}
    intptr_t 已返回值=用戶調用(5,檔案句柄,偏移值,尋道原點,0,0,0);if(已返回值<0){錯誤=-已返回值;return -1;}return 已返回值;
}
int unlink(const char*名稱){intptr_t 已返回值=用戶調用(11,(uintptr_t)名稱,0,0,0,0,0);if(已返回值<0){錯誤=-已返回值;return -1;}return 已返回值;}
char *realpath(const char*名稱,char*結果資料){if(!結果資料){結果資料=malloc(strlen(名稱)+1);if(!結果資料)return 0;}return strcpy(結果資料,名稱);}
char *getcwd(char*資料位置,size_t 項目個數){if(項目個數<2){錯誤=34;return 0;}資料位置[0]='/';資料位置[1]=0;return 資料位置;}
char *strerror(int 輔助條目){(void)輔助條目;return "native compiler I/O error";}
time_t time(time_t*終端條目){time_t 臨時資料=0;if(終端條目)*終端條目=臨時資料;return 臨時資料;}
struct tm *localtime(const time_t*終端條目){(void)終端條目;static struct tm 臨時資料={.tm_year=126,.tm_mon=0,.tm_mday=1};return &臨時資料;}
static FILE 數據流集[18]={{1,0,1},{2,0,1}};FILE*stdout=&數據流集[0],*stderr=&數據流集[1];
FILE*fdopen(int 檔案句柄,const char*方法模式){(void)方法模式;for(unsigned 序數索引=2;序數索引<18;序數索引++)if(!數據流集[序數索引].已使用容量){數據流集[序數索引].已使用容量=1;數據流集[序數索引].錯誤=0;數據流集[序數索引].檔案句柄=檔案句柄;return &數據流集[序數索引];}錯誤=24;return 0;}
int fflush(FILE*檔案條目){return 檔案條目&&檔案條目->錯誤?-1:0;}
int fclose(FILE*檔案條目){int 已返回值=close(檔案條目->檔案句柄);if(檔案條目->錯誤)已返回值=-1;檔案條目->已使用容量=0;return 已返回值;}
size_t fwrite(const void*資料位置,size_t 字符串資料,size_t 項目個數,FILE*檔案條目){if(!字符串資料)return 0;if(項目個數>SIZE_MAX/字符串資料){檔案條目->錯誤=1;return 0;}long 已返回值=write(檔案條目->檔案句柄,資料位置,字符串資料*項目個數);if(已返回值<0){檔案條目->錯誤=1;return 0;}return (size_t)已返回值/字符串資料;}
int fputc(int 字元程式碼,FILE*檔案條目){unsigned char 第二值=字元程式碼;return fwrite(&第二值,1,1,檔案條目)==1?第二值:EOF;}
int fputs(const char*字符串資料,FILE*檔案條目){return fwrite(字符串資料,1,strlen(字符串資料),檔案條目)==strlen(字符串資料)?0:EOF;}
static void 放入值(char*結果資料,size_t 容量最大,size_t*當前位置,char 字元程式碼){if(*當前位置+1<容量最大)結果資料[*當前位置]=字元程式碼;(*當前位置)++;}
int vsnprintf(char*結果資料,size_t 容量最大,const char*格式,va_list 可變參數參數列){
    size_t 當前位置=0;while(*格式){if(*格式!='%'){放入值(結果資料,容量最大,&當前位置,*格式++);continue;}格式++;
        int 左側=0,零值=0,回退值=0;while(*格式=='-'||*格式=='0'||*格式=='#'||*格式=='+'||*格式==' '){if(*格式=='-')左側=1;if(*格式=='0')零值=1;if(*格式=='#')回退值=1;格式++;}
        int 寬度值=0,精度值=-1;if(*格式=='*'){寬度值=va_arg(可變參數參數列,int);格式++;}else while(*格式>='0'&&*格式<='9')寬度值=寬度值*10+*格式++-'0';
        if(*格式=='.'){格式++;精度值=0;if(*格式=='*'){精度值=va_arg(可變參數參數列,int);格式++;}else while(*格式>='0'&&*格式<='9')精度值=精度值*10+*格式++-'0';}
        int 寬幅字元=0;while(*格式=='l'||*格式=='z'||*格式=='t'||*格式=='j'||*格式=='h'){if(*格式!='h')寬幅字元=1;格式++;}
        char 類型分類=*格式?*格式++:0,緩衝區存儲裝置[80];const char*字符串資料=緩衝區存儲裝置;size_t 項目個數=0;
        if(類型分類=='s'){字符串資料=va_arg(可變參數參數列,const char*);if(!字符串資料)字符串資料="(null)";項目個數=strlen(字符串資料);if(精度值>=0&&項目個數>(size_t)精度值)項目個數=精度值;}
        else if(類型分類=='c'){緩衝區存儲裝置[0]=va_arg(可變參數參數列,int);項目個數=1;}
        else if(類型分類=='%'){緩衝區存儲裝置[0]='%';項目個數=1;}
        else if(類型分類=='d'||類型分類=='i'||類型分類=='u'||類型分類=='x'||類型分類=='X'||類型分類=='o'||類型分類=='p'){
            unsigned long long 值;int 負數=0;
            if(類型分類=='d'||類型分類=='i'){long long 臨時資料=寬幅字元?va_arg(可變參數參數列,long long):va_arg(可變參數參數列,int);負數=臨時資料<0;值=負數?0-(unsigned long long)臨時資料:臨時資料;}
            else 值=類型分類=='p'?(uintptr_t)va_arg(可變參數參數列,void*):寬幅字元?va_arg(可變參數參數列,unsigned long long):va_arg(可變參數參數列,unsigned);
            unsigned 背景值=類型分類=='x'||類型分類=='X'||類型分類=='p'?16:類型分類=='o'?8:10;char 數字個數[64];unsigned 已使用容量=0;
            do{數字個數[已使用容量++]="0123456789abcdef"[值%背景值];值/=背景值;}while(值);
            if(負數)緩衝區存儲裝置[項目個數++]='-';if(類型分類=='p'||(回退值&&背景值==16)){緩衝區存儲裝置[項目個數++]='0';緩衝區存儲裝置[項目個數++]='x';}
            for(int 填充值=(int)已使用容量;精度值>填充值&&項目個數<sizeof(緩衝區存儲裝置)-已使用容量;填充值++)緩衝區存儲裝置[項目個數++]='0';
            if(零值&&!左側&&精度值<0)while(寬度值>(int)(項目個數+已使用容量)&&項目個數<sizeof(緩衝區存儲裝置)-已使用容量)緩衝區存儲裝置[項目個數++]='0';
            while(已使用容量)緩衝區存儲裝置[項目個數++]=數字個數[--已使用容量];
        }else{緩衝區存儲裝置[0]='?';項目個數=1;}
        if(寬度值>4096)寬度值=4096;while(!左側&&寬度值>(int)項目個數){放入值(結果資料,容量最大,&當前位置,' ');寬度值--;}
        for(size_t 序數索引=0;序數索引<項目個數;序數索引++)放入值(結果資料,容量最大,&當前位置,字符串資料[序數索引]);while(左側&&寬度值>(int)項目個數){放入值(結果資料,容量最大,&當前位置,' ');寬度值--;}
    }if(容量最大)結果資料[當前位置<容量最大?當前位置:容量最大-1]=0;return 當前位置;
}
int snprintf(char*結果資料,size_t 容量最大,const char*檔案條目,...){va_list 首位值;va_start(首位值,檔案條目);int 已返回值=vsnprintf(結果資料,容量最大,檔案條目,首位值);va_end(首位值);return 已返回值;}
int sprintf(char*結果資料,const char*檔案條目,...){va_list 首位值;va_start(首位值,檔案條目);int 已返回值=vsnprintf(結果資料,SIZE_MAX,檔案條目,首位值);va_end(首位值);return 已返回值;}
int vfprintf(FILE*流值,const char*檔案條目,va_list 首位值){char 第二值[2048];int 項目個數=vsnprintf(第二值,sizeof(第二值),檔案條目,首位值);if(項目個數>2047)項目個數=2047;return fwrite(第二值,1,項目個數,流值)==(size_t)項目個數?項目個數:-1;}
int fprintf(FILE*流值,const char*檔案條目,...){va_list 首位值;va_start(首位值,檔案條目);int 已返回值=vfprintf(流值,檔案條目,首位值);va_end(首位值);return 已返回值;}
int printf(const char*檔案條目,...){va_list 首位值;va_start(首位值,檔案條目);int 已返回值=vfprintf(stdout,檔案條目,首位值);va_end(首位值);return 已返回值;}
