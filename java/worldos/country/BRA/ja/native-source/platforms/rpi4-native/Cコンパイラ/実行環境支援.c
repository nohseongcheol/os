#include "../命名/機械連結名前一覧.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "呼出.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int エラー;
int *__errno_location(void){return &エラー;}
void exit(int 状況値){利用者呼出(6,状況値,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *式検査,const char *ファイル,unsigned 行,const char *メソッド入口名前){fprintf(stderr,"cc assertion: %s %s:%u %s\n",式検査,ファイル,行,メソッド入口名前);exit(1);}
size_t strlen(const char*文字列データ){const char*データ位置=文字列データ;while(*データ位置)データ位置++;return データ位置-文字列データ;}
int strcmp(const char*先頭位置値,const char*第二値){while(*先頭位置値&&*先頭位置値==*第二値){先頭位置値++;第二値++;}return (unsigned char)*先頭位置値-(unsigned char)*第二値;}
int strncmp(const char*先頭位置値,const char*第二値,size_t 項目個数){while(項目個数--){unsigned char 横座標=*先頭位置値++,縦座標=*第二値++;if(横座標!=縦座標)return 横座標-縦座標;if(!横座標)return 0;}return 0;}
char *strcpy(char*宛先データ,const char*文字列データ){char*返却済み値=宛先データ;while((*宛先データ++=*文字列データ++)){}return 返却済み値;}
char *strchr(const char*文字列データ,int 文字コード){do{if(*文字列データ==(char)文字コード)return (char*)文字列データ;}while(*文字列データ++);return 0;}
char *strrchr(const char*文字列データ,int 文字コード){const char*返却済み値=0;do{if(*文字列データ==(char)文字コード)返却済み値=文字列データ;}while(*文字列データ++);return (char*)返却済み値;}
char *strstr(const char*文字列データ,const char*端末入口){size_t 項目個数=strlen(端末入口);for(;*文字列データ;文字列データ++)if(!strncmp(文字列データ,端末入口,項目個数))return (char*)文字列データ;return 項目個数?0:(char*)文字列データ;}
int memcmp(const void*先頭位置値,const void*第二値,size_t 項目個数){const unsigned char*横座標=先頭位置値,*縦座標=第二値;while(項目個数--){if(*横座標!=*縦座標)return *横座標-*縦座標;横座標++;縦座標++;}return 0;}
void *memmove(void*宛先データ,const void*文字列データ,size_t 項目個数){unsigned char*横座標=宛先データ;const unsigned char*縦座標=文字列データ;if(横座標<縦座標){for(size_t 序数添字=0;序数添字<項目個数;序数添字++)横座標[序数添字]=縦座標[序数添字];}else while(項目個数){項目個数--;横座標[項目個数]=縦座標[項目個数];}return 宛先データ;}
static unsigned char 確保状態一括領域[6*1024*1024] __attribute__((aligned(16)));
typedef struct データブロック {size_t 容量;struct データブロック*次回項目;int 残り容積;int 詰め物;uint64_t 整列条件単位;} データブロック;
static データブロック *先頭位置入口;
void free(void*データ位置){if(!データ位置)return;データブロック*第二値=(データブロック*)データ位置-1;第二値->残り容積=1;for(データブロック*次回変位量=先頭位置入口;次回変位量&&次回変位量->次回項目;){if(次回変位量->残り容積&&次回変位量->次回項目->残り容積){次回変位量->容量+=sizeof(データブロック)+次回変位量->次回項目->容量;次回変位量->次回項目=次回変位量->次回項目->次回項目;}else 次回変位量=次回変位量->次回項目;}}
void *realloc(void*データ位置,size_t 項目個数){
    if(!項目個数){free(データ位置);return 0;}if(項目個数>sizeof(確保状態一括領域)-sizeof(データブロック))return 0;項目個数=(項目個数+15)&~(size_t)15;
    if(!先頭位置入口){先頭位置入口=(データブロック*)確保状態一括領域;先頭位置入口->容量=sizeof(確保状態一括領域)-sizeof(データブロック);先頭位置入口->残り容積=1;先頭位置入口->次回項目=0;}
    データブロック*前回項目=データ位置?(データブロック*)データ位置-1:0;if(前回項目&&前回項目->容量>=項目個数)return データ位置;
    for(データブロック*第二値=先頭位置入口;第二値;第二値=第二値->次回項目)if(第二値->残り容積&&第二値->容量>=項目個数){
        if(第二値->容量>=項目個数+sizeof(データブロック)+16){データブロック*残り部分=(データブロック*)((unsigned char*)(第二値+1)+項目個数);残り部分->容量=第二値->容量-項目個数-sizeof(データブロック);残り部分->次回項目=第二値->次回項目;残り部分->残り容積=1;第二値->次回項目=残り部分;第二値->容量=項目個数;}
        第二値->残り容積=0;void*返却済み値=第二値+1;if(前回項目){memcpy(返却済み値,データ位置,前回項目->容量);free(データ位置);}return 返却済み値;
    }エラー=12;return 0;
}
void *malloc(size_t 項目個数){return realloc(0,項目個数);}
void *calloc(size_t 項目個数,size_t 文字列データ){if(文字列データ&&項目個数>SIZE_MAX/文字列データ)return 0;void*データ位置=malloc(項目個数*文字列データ);if(データ位置)memset(データ位置,0,項目個数*文字列データ);return データ位置;}
unsigned long long strtoull(const char*文字列データ,char**終端位置変位量,int 背景値){
    const char*変位量開始処理=文字列データ;while(*文字列データ==' '||(*文字列データ>=9&&*文字列データ<=13))文字列データ++;int 判定負数=0;if(*文字列データ=='-'||*文字列データ=='+')判定負数=*文字列データ++=='-';
    if((!背景値||背景値==16)&&文字列データ[0]=='0'&&(文字列データ[1]=='x'||文字列データ[1]=='X')){背景値=16;文字列データ+=2;}if(!背景値)背景値=*文字列データ=='0'?8:10;
    unsigned long long 一時データ=0;int 任意値=0;for(;;){unsigned 文字コード=*文字列データ,宛先データ=文字コード>='0'&&文字コード<='9'?文字コード-'0':文字コード>='a'&&文字コード<='z'?文字コード-'a'+10:文字コード>='A'&&文字コード<='Z'?文字コード-'A'+10:99;if(宛先データ>=(unsigned)背景値)break;任意値=1;文字列データ++;if(一時データ>(~0ull-宛先データ)/(unsigned)背景値){一時データ=~0ull;エラー=34;}else 一時データ=一時データ*背景値+宛先データ;}
    if(終端位置変位量)*終端位置変位量=(char*)(任意値?文字列データ:変位量開始処理);return 判定負数?0-一時データ:一時データ;
}
unsigned long strtoul(const char*文字列データ,char**補助入口,int 第二値){return strtoull(文字列データ,補助入口,第二値);}
long strtol(const char*文字列データ,char**補助入口,int 第二値){return (long)strtoull(文字列データ,補助入口,第二値);}
int atoi(const char*文字列データ){return (int)strtol(文字列データ,0,10);}
long double ldexpl(long double 横座標,int 項目個数){while(項目個数>0){横座標*=2;項目個数--;}while(項目個数<0){横座標/=2;項目個数++;}return 横座標;}
long double strtold(const char*文字列データ,char**終端位置変位量){
    const char*変位量開始処理=文字列データ;while(*文字列データ==' '||(*文字列データ>=9&&*文字列データ<=13))文字列データ++;int 判定負数=0;if(*文字列データ=='-'||*文字列データ=='+')判定負数=*文字列データ++=='-';
    int 背景値=10;if(文字列データ[0]=='0'&&(文字列データ[1]=='x'||文字列データ[1]=='X')){背景値=16;文字列データ+=2;}long double 一時データ=0,倍率=1;int 小数部=0,任意値=0;
    for(;;){int 文字コード=*文字列データ,宛先データ=文字コード>='0'&&文字コード<='9'?文字コード-'0':文字コード>='a'&&文字コード<='f'?文字コード-'a'+10:文字コード>='A'&&文字コード<='F'?文字コード-'A'+10:99;
        if(文字コード=='.'&&!小数部){小数部=1;文字列データ++;continue;}if(宛先データ>=背景値)break;任意値=1;文字列データ++;一時データ=一時データ*背景値+宛先データ;if(小数部)倍率*=背景値;
    }一時データ/=倍率;
    if((背景値==10&&(*文字列データ=='e'||*文字列データ=='E'))||(背景値==16&&(*文字列データ=='p'||*文字列データ=='P'))){const char*値表示=文字列データ++;int 値一覧減算=0;if(*文字列データ=='-'||*文字列データ=='+')値一覧減算=*文字列データ++=='-';int 項目個数=0,入口個数=0;while(*文字列データ>='0'&&*文字列データ<='9'){入口個数++;if(項目個数<20000)項目個数=項目個数*10+*文字列データ-'0';文字列データ++;}if(!入口個数)文字列データ=値表示;else{long double 係数=背景値==16?2:10;while(項目個数-->0&&項目個数<200000)一時データ=値一覧減算?一時データ/係数:一時データ*係数;}}
    if(終端位置変位量)*終端位置変位量=(char*)(任意値?文字列データ:変位量開始処理);return 判定負数?-一時データ:一時データ;
}
double strtod(const char*文字列データ,char**補助入口){return (double)strtold(文字列データ,補助入口);}float strtof(const char*文字列データ,char**補助入口){return (float)strtold(文字列データ,補助入口);}
void qsort(void*背景値,size_t 項目個数,size_t 容量,int(*比較)(const void*,const void*)){
    unsigned char*データ位置=背景値;for(size_t 序数添字=1;序数添字<項目個数;序数添字++)for(size_t 内側序数=序数添字;内側序数&&比較(データ位置+(内側序数-1)*容量,データ位置+内側序数*容量)>0;内側序数--)for(size_t 第三添字=0;第三添字<容量;第三添字++){unsigned char 文字コード=データ位置[(内側序数-1)*容量+第三添字];データ位置[(内側序数-1)*容量+第三添字]=データ位置[内側序数*容量+第三添字];データ位置[内側序数*容量+第三添字]=文字コード;}
}
static struct {int 使用済み容積,検索添字;size_t 位置;} 開放済み[24];
static unsigned char 出力結果[32768];static size_t 出力容量,出力位置;static int 出力開放;
const unsigned char *C出力(size_t *項目個数){*項目個数=出力容量;return 出力結果;}
int open(const char*名前,int 構成設定ビット列,...){
    if(!strcmp(名前,"/@cc-output")){if(出力開放){エラー=16;return -1;}出力開放=1;出力容量=出力位置=0;return 100;}
    for(unsigned 序数添字=0;序数添字<sizeof(コンパイラ資源一覧)/sizeof(コンパイラ資源一覧[0]);序数添字++)if(!strcmp(名前,コンパイラ資源一覧[序数添字].名前)){
        if(構成設定ビット列&3){エラー=30;return -1;}for(int 内側序数=0;内側序数<24;内側序数++)if(!開放済み[内側序数].使用済み容積){開放済み[内側序数].使用済み容積=1;開放済み[内側序数].検索添字=序数添字;開放済み[内側序数].位置=0;return 128+内側序数;}エラー=24;return -1;
    }
    intptr_t 返却済み値=利用者呼出(3,(uintptr_t)名前,構成設定ビット列,0,0,0,0);if(返却済み値<0){エラー=-返却済み値;return -1;}return 返却済み値;
}
int close(int ファイル取扱い){if(ファイル取扱い==100){出力開放=0;return 0;}if(ファイル取扱い>=128&&ファイル取扱い<152){開放済み[ファイル取扱い-128].使用済み容積=0;return 0;}intptr_t 返却済み値=利用者呼出(4,ファイル取扱い,0,0,0,0,0);if(返却済み値<0){エラー=-返却済み値;return -1;}return 0;}
long read(int ファイル取扱い,void*データ,size_t 項目個数){
    if(ファイル取扱い>=128&&ファイル取扱い<152&&開放済み[ファイル取扱い-128].使用済み容積){int 序数添字=ファイル取扱い-128;const コンパイラ資源*返却済み値=&コンパイラ資源一覧[開放済み[序数添字].検索添字];size_t 左側面=返却済み値->容量-開放済み[序数添字].位置;if(項目個数>左側面)項目個数=左側面;memcpy(データ,返却済み値->データ+開放済み[序数添字].位置,項目個数);開放済み[序数添字].位置+=項目個数;return 項目個数;}
    intptr_t 返却済み値=利用者呼出(2,ファイル取扱い,(uintptr_t)データ,項目個数,0,0,0);if(返却済み値<0){エラー=-返却済み値;return -1;}return 返却済み値;
}
long write(int ファイル取扱い,const void*データ,size_t 項目個数){
    if(ファイル取扱い==100){if(項目個数>sizeof(出力結果)-出力位置){エラー=28;return -1;}memcpy(出力結果+出力位置,データ,項目個数);出力位置+=項目個数;if(出力容量<出力位置)出力容量=出力位置;return 項目個数;}
    intptr_t 返却済み値=利用者呼出(1,ファイル取扱い,(uintptr_t)データ,項目個数,0,0,0);if(返却済み値<0){エラー=-返却済み値;return -1;}return 返却済み値;
}
long lseek(int ファイル取扱い,long 変位量値,int 原点位置移動){
    if(ファイル取扱い==100){long データ位置=変位量値+(原点位置移動==0?0:原点位置移動==1?出力位置:出力容量);if(データ位置<0||(size_t)データ位置>sizeof(出力結果)){エラー=22;return -1;}出力位置=データ位置;return データ位置;}
    if(ファイル取扱い>=128&&ファイル取扱い<152&&開放済み[ファイル取扱い-128].使用済み容積){int 序数添字=ファイル取扱い-128;long データ位置=変位量値+(原点位置移動==0?0:原点位置移動==1?開放済み[序数添字].位置:コンパイラ資源一覧[開放済み[序数添字].検索添字].容量);if(データ位置<0||(size_t)データ位置>コンパイラ資源一覧[開放済み[序数添字].検索添字].容量){エラー=22;return -1;}開放済み[序数添字].位置=データ位置;return データ位置;}
    intptr_t 返却済み値=利用者呼出(5,ファイル取扱い,変位量値,原点位置移動,0,0,0);if(返却済み値<0){エラー=-返却済み値;return -1;}return 返却済み値;
}
int unlink(const char*名前){intptr_t 返却済み値=利用者呼出(11,(uintptr_t)名前,0,0,0,0,0);if(返却済み値<0){エラー=-返却済み値;return -1;}return 返却済み値;}
char *realpath(const char*名前,char*結果データ){if(!結果データ){結果データ=malloc(strlen(名前)+1);if(!結果データ)return 0;}return strcpy(結果データ,名前);}
char *getcwd(char*データ位置,size_t 項目個数){if(項目個数<2){エラー=34;return 0;}データ位置[0]='/';データ位置[1]=0;return データ位置;}
char *strerror(int 補助入口){(void)補助入口;return "native compiler I/O error";}
time_t time(time_t*端末入口){time_t 一時データ=0;if(端末入口)*端末入口=一時データ;return 一時データ;}
struct tm *localtime(const time_t*端末入口){(void)端末入口;static struct tm 一時データ={.tm_year=126,.tm_mon=0,.tm_mday=1};return &一時データ;}
static FILE ストリーム群[18]={{1,0,1},{2,0,1}};FILE*stdout=&ストリーム群[0],*stderr=&ストリーム群[1];
FILE*fdopen(int ファイル取扱い,const char*メソッド方式){(void)メソッド方式;for(unsigned 序数添字=2;序数添字<18;序数添字++)if(!ストリーム群[序数添字].使用済み容積){ストリーム群[序数添字].使用済み容積=1;ストリーム群[序数添字].エラー=0;ストリーム群[序数添字].ファイル取扱い=ファイル取扱い;return &ストリーム群[序数添字];}エラー=24;return 0;}
int fflush(FILE*ファイル入口){return ファイル入口&&ファイル入口->エラー?-1:0;}
int fclose(FILE*ファイル入口){int 返却済み値=close(ファイル入口->ファイル取扱い);if(ファイル入口->エラー)返却済み値=-1;ファイル入口->使用済み容積=0;return 返却済み値;}
size_t fwrite(const void*データ位置,size_t 文字列データ,size_t 項目個数,FILE*ファイル入口){if(!文字列データ)return 0;if(項目個数>SIZE_MAX/文字列データ){ファイル入口->エラー=1;return 0;}long 返却済み値=write(ファイル入口->ファイル取扱い,データ位置,文字列データ*項目個数);if(返却済み値<0){ファイル入口->エラー=1;return 0;}return (size_t)返却済み値/文字列データ;}
int fputc(int 文字コード,FILE*ファイル入口){unsigned char 第二値=文字コード;return fwrite(&第二値,1,1,ファイル入口)==1?第二値:EOF;}
int fputs(const char*文字列データ,FILE*ファイル入口){return fwrite(文字列データ,1,strlen(文字列データ),ファイル入口)==strlen(文字列データ)?0:EOF;}
static void 値格納(char*結果データ,size_t 容積最大,size_t*現在位置,char 文字コード){if(*現在位置+1<容積最大)結果データ[*現在位置]=文字コード;(*現在位置)++;}
int vsnprintf(char*結果データ,size_t 容積最大,const char*書式,va_list 可変引数引数列){
    size_t 現在位置=0;while(*書式){if(*書式!='%'){値格納(結果データ,容積最大,&現在位置,*書式++);continue;}書式++;
        int 左側面=0,零値=0,代替値=0;while(*書式=='-'||*書式=='0'||*書式=='#'||*書式=='+'||*書式==' '){if(*書式=='-')左側面=1;if(*書式=='0')零値=1;if(*書式=='#')代替値=1;書式++;}
        int 幅値=0,精度値=-1;if(*書式=='*'){幅値=va_arg(可変引数引数列,int);書式++;}else while(*書式>='0'&&*書式<='9')幅値=幅値*10+*書式++-'0';
        if(*書式=='.'){書式++;精度値=0;if(*書式=='*'){精度値=va_arg(可変引数引数列,int);書式++;}else while(*書式>='0'&&*書式<='9')精度値=精度値*10+*書式++-'0';}
        int 広幅文字=0;while(*書式=='l'||*書式=='z'||*書式=='t'||*書式=='j'||*書式=='h'){if(*書式!='h')広幅文字=1;書式++;}
        char 型分類=*書式?*書式++:0,緩衝域記憶装置[80];const char*文字列データ=緩衝域記憶装置;size_t 項目個数=0;
        if(型分類=='s'){文字列データ=va_arg(可変引数引数列,const char*);if(!文字列データ)文字列データ="(null)";項目個数=strlen(文字列データ);if(精度値>=0&&項目個数>(size_t)精度値)項目個数=精度値;}
        else if(型分類=='c'){緩衝域記憶装置[0]=va_arg(可変引数引数列,int);項目個数=1;}
        else if(型分類=='%'){緩衝域記憶装置[0]='%';項目個数=1;}
        else if(型分類=='d'||型分類=='i'||型分類=='u'||型分類=='x'||型分類=='X'||型分類=='o'||型分類=='p'){
            unsigned long long 値;int 負数=0;
            if(型分類=='d'||型分類=='i'){long long 一時データ=広幅文字?va_arg(可変引数引数列,long long):va_arg(可変引数引数列,int);負数=一時データ<0;値=負数?0-(unsigned long long)一時データ:一時データ;}
            else 値=型分類=='p'?(uintptr_t)va_arg(可変引数引数列,void*):広幅文字?va_arg(可変引数引数列,unsigned long long):va_arg(可変引数引数列,unsigned);
            unsigned 背景値=型分類=='x'||型分類=='X'||型分類=='p'?16:型分類=='o'?8:10;char 桁個数[64];unsigned 使用済み容積=0;
            do{桁個数[使用済み容積++]="0123456789abcdef"[値%背景値];値/=背景値;}while(値);
            if(負数)緩衝域記憶装置[項目個数++]='-';if(型分類=='p'||(代替値&&背景値==16)){緩衝域記憶装置[項目個数++]='0';緩衝域記憶装置[項目個数++]='x';}
            for(int 値塗潰し=(int)使用済み容積;精度値>値塗潰し&&項目個数<sizeof(緩衝域記憶装置)-使用済み容積;値塗潰し++)緩衝域記憶装置[項目個数++]='0';
            if(零値&&!左側面&&精度値<0)while(幅値>(int)(項目個数+使用済み容積)&&項目個数<sizeof(緩衝域記憶装置)-使用済み容積)緩衝域記憶装置[項目個数++]='0';
            while(使用済み容積)緩衝域記憶装置[項目個数++]=桁個数[--使用済み容積];
        }else{緩衝域記憶装置[0]='?';項目個数=1;}
        if(幅値>4096)幅値=4096;while(!左側面&&幅値>(int)項目個数){値格納(結果データ,容積最大,&現在位置,' ');幅値--;}
        for(size_t 序数添字=0;序数添字<項目個数;序数添字++)値格納(結果データ,容積最大,&現在位置,文字列データ[序数添字]);while(左側面&&幅値>(int)項目個数){値格納(結果データ,容積最大,&現在位置,' ');幅値--;}
    }if(容積最大)結果データ[現在位置<容積最大?現在位置:容積最大-1]=0;return 現在位置;
}
int snprintf(char*結果データ,size_t 容積最大,const char*ファイル入口,...){va_list 先頭位置値;va_start(先頭位置値,ファイル入口);int 返却済み値=vsnprintf(結果データ,容積最大,ファイル入口,先頭位置値);va_end(先頭位置値);return 返却済み値;}
int sprintf(char*結果データ,const char*ファイル入口,...){va_list 先頭位置値;va_start(先頭位置値,ファイル入口);int 返却済み値=vsnprintf(結果データ,SIZE_MAX,ファイル入口,先頭位置値);va_end(先頭位置値);return 返却済み値;}
int vfprintf(FILE*ストリーム値,const char*ファイル入口,va_list 先頭位置値){char 第二値[2048];int 項目個数=vsnprintf(第二値,sizeof(第二値),ファイル入口,先頭位置値);if(項目個数>2047)項目個数=2047;return fwrite(第二値,1,項目個数,ストリーム値)==(size_t)項目個数?項目個数:-1;}
int fprintf(FILE*ストリーム値,const char*ファイル入口,...){va_list 先頭位置値;va_start(先頭位置値,ファイル入口);int 返却済み値=vfprintf(ストリーム値,ファイル入口,先頭位置値);va_end(先頭位置値);return 返却済み値;}
int printf(const char*ファイル入口,...){va_list 先頭位置値;va_start(先頭位置値,ファイル入口);int 返却済み値=vfprintf(stdout,ファイル入口,先頭位置値);va_end(先頭位置値);return 返却済み値;}
