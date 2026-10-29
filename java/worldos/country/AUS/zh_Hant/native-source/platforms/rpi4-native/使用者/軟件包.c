#include "../命名/計算機連接名稱列.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "調用.h"
#include "軟件包.h"
#include "uzlib.h"
static unsigned char 存檔[16384], 已解包[16385];
static unsigned 大小, 中央, 條目列列表;
static char 條目類別[256];
static unsigned 讀取二位元組列(unsigned 當前位置) { return 存檔[當前位置] | 存檔[當前位置+1] << 8; }
static uint32_t 讀取四位元組列(unsigned 當前位置) { return 讀取二位元組列(當前位置) | (uint32_t)讀取二位元組列(當前位置+2) << 16; }
static int 裁剪(unsigned 當前位置, unsigned 項目個數, unsigned 容量限制) { return 當前位置 <= 容量限制 && 項目個數 <= 容量限制-當前位置; }
static size_t 長度(const char *字符串資料) { size_t 項目個數=0; while(字符串資料[項目個數]) 項目個數++; return 項目個數; }
static int 相等文本(const unsigned char *首位值, const unsigned char *第二值, unsigned 項目個數) { for(unsigned 序數索引=0;序數索引<項目個數;序數索引++)if(首位值[序數索引]!=第二值[序數索引])return 0;return 1; }
static int 檔案結束(void *未使用) { (void)未使用; return -1; }
static int 屬性資料(const char *行,unsigned 已使用容量,int *條目分存在判斷) {
    if(已使用容量>=12 && 相等文本((const unsigned char*)行,(const unsigned char*)"Class-Path: ",12))return -95;
    if(已使用容量>=12 && 相等文本((const unsigned char*)行,(const unsigned char*)"Main-Class: ",12)) {
        unsigned 值=已使用容量-12;if(*條目分存在判斷||!值||值>=sizeof(條目類別))return -8;
        for(unsigned 序數索引=0;序數索引<值;序數索引++){unsigned char 字元程式碼=行[12+序數索引];if(字元程式碼<=32||字元程式碼=='/'||字元程式碼=='\\')return -8;條目類別[序數索引]=字元程式碼;}
        條目類別[值]=0;*條目分存在判斷=1;
    }
    return 0;
}
static int 成員(unsigned 當前位置, unsigned char *結果資料, unsigned 容量最大) {
    unsigned 方法條目=讀取二位元組列(當前位置+10), 配置項位元列=讀取二位元組列(當前位置+8), 已壓縮=讀取四位元組列(當前位置+20), 釋放大小=讀取四位元組列(當前位置+24), 局部=讀取四位元組列(當前位置+42);
    unsigned 名稱=讀取二位元組列(當前位置+28);
    if(釋放大小>容量最大 || 釋放大小>16384 || (方法條目!=0 && 方法條目!=8) || (配置項位元列&~0x80e))return -8;
    if(!裁剪(局部,30,中央) || 讀取四位元組列(局部)!=0x04034b50 || 讀取二位元組列(局部+8)!=方法條目 || 讀取二位元組列(局部+6)!=配置項位元列 || 讀取二位元組列(局部+26)!=名稱)return -8;
    unsigned 開始偏移=局部+30, 附加區域=讀取二位元組列(局部+28);
    if(!裁剪(開始偏移,名稱,中央) || !相等文本(存檔+開始偏移,存檔+當前位置+46,名稱))return -8;
    開始偏移+=名稱;if(!裁剪(開始偏移,附加區域,中央))return -8;開始偏移+=附加區域;
    if(!裁剪(開始偏移,已壓縮,中央))return -8;
    if(!(配置項位元列&8) && (讀取四位元組列(局部+14)!=讀取四位元組列(當前位置+16) || 讀取四位元組列(局部+18)!=已壓縮 || 讀取四位元組列(局部+22)!=釋放大小))return -8;
    if(方法條目==0) { if(已壓縮!=釋放大小)return -8; for(unsigned 序數索引=0;序數索引<釋放大小;序數索引++)結果資料[序數索引]=存檔[開始偏移+序數索引]; }
    else {
        uzlib_uncomp_t 目的地址資料={0};uzlib_uncompress_init(&目的地址資料,0,0);
        目的地址資料.source=存檔+開始偏移;目的地址資料.source_limit=目的地址資料.source+已壓縮;目的地址資料.source_read_cb=檔案結束;
        /* One extra output byte lets inflate consume/check the end marker. */
        目的地址資料.dest_start=目的地址資料.dest=已解包;目的地址資料.dest_limit=已解包+釋放大小+1;
        int 已返回值=uzlib_uncompress(&目的地址資料);
        if(已返回值!=UZLIB_DONE || 目的地址資料.eof || 目的地址資料.dest!=已解包+釋放大小 || 目的地址資料.source!=目的地址資料.source_limit)return -8;
        for(unsigned 序數索引=0;序數索引<釋放大小;序數索引++)結果資料[序數索引]=已解包[序數索引];
    }
    if((uzlib_crc32(結果資料,釋放大小,0xffffffffu)^0xffffffffu)!=讀取四位元組列(當前位置+16))return -8;
    return 釋放大小;
}
int JAR讀取(const char *名稱, unsigned char *結果資料, unsigned 緩衝區容量) {
    if(!條目列列表)return -2;unsigned 項目個數=長度(名稱),當前位置=中央;
    for(unsigned 序數索引=0;序數索引<條目列列表;序數索引++) {
        unsigned 名稱長度=讀取二位元組列(當前位置+28);
        if(名稱長度==項目個數 && 相等文本(存檔+當前位置+46,(const unsigned char*)名稱,項目個數))return 成員(當前位置,結果資料,緩衝區容量);
        當前位置+=46+名稱長度+讀取二位元組列(當前位置+30)+讀取二位元組列(當前位置+32);
    }
    return -2;
}
const char *JAR主操作(void) { return 條目類別; }
int JAR打開(const char *檔案條目名稱) {
    條目列列表=0;條目類別[0]=0;
    intptr_t 檔案句柄=用戶調用(3,(uintptr_t)檔案條目名稱,0,0,0,0,0);if(檔案句柄<0)return 檔案句柄;
    intptr_t 項目個數=用戶調用(9,檔案句柄,0,0,0,0,0);
    if(項目個數<22 || 項目個數>(intptr_t)sizeof(存檔)) { 用戶調用(4,檔案句柄,0,0,0,0,0);return -8; }
    intptr_t 已接收個數=用戶調用(2,檔案句柄,(uintptr_t)存檔,項目個數,0,0,0);用戶調用(4,檔案句柄,0,0,0,0,0);
    if(已接收個數!=項目個數)return -5;大小=項目個數;
    unsigned 結束偏移=大小-22;
    for(;;) { if(讀取四位元組列(結束偏移)==0x06054b50 && 結束偏移+22+讀取二位元組列(結束偏移+20)==大小)break; if(!結束偏移)return -8;結束偏移--; }
    unsigned 條目個數=讀取二位元組列(結束偏移+10);中央=讀取四位元組列(結束偏移+16);
    if(讀取二位元組列(結束偏移+4)||讀取二位元組列(結束偏移+6)||讀取二位元組列(結束偏移+8)!=條目個數||!條目個數||條目個數>256||!裁剪(中央,讀取四位元組列(結束偏移+12),結束偏移)||中央+讀取四位元組列(結束偏移+12)!=結束偏移)return -8;
    unsigned 當前位置=中央;
    for(unsigned 序數索引=0;序數索引<條目個數;序數索引++) {
        if(!裁剪(當前位置,46,結束偏移)||讀取四位元組列(當前位置)!=0x02014b50||讀取二位元組列(當前位置+34))return -8;
        unsigned 名稱長度=讀取二位元組列(當前位置+28),下一項目=46+名稱長度+讀取二位元組列(當前位置+30)+讀取二位元組列(當前位置+32);
        if(!名稱長度||名稱長度>511||!裁剪(當前位置,下一項目,結束偏移)||讀取四位元組列(當前位置+24)>16384)return -8;
        for(unsigned 內部側序數=0;內部側序數<名稱長度;內部側序數++)if(!存檔[當前位置+46+內部側序數])return -8;
        unsigned 其他條目=中央;
        for(unsigned 內部側序數=0;內部側序數<序數索引;內部側序數++){unsigned 長度資料=讀取二位元組列(其他條目+28);if(長度資料==名稱長度&&相等文本(存檔+其他條目+46,存檔+當前位置+46,長度資料))return -8;其他條目+=46+長度資料+讀取二位元組列(其他條目+30)+讀取二位元組列(其他條目+32);}
        當前位置+=下一項目;
    }
    if(當前位置!=結束偏移)return -8;條目列列表=條目個數;
    unsigned char 捆綁構建清單[4096];int 組大小=JAR讀取("META-INF/MANIFEST.MF",捆綁構建清單,sizeof(捆綁構建清單)-1);if(組大小<0){條目列列表=0;return -8;}
    捆綁構建清單[組大小]=0;
    char 邏輯[512];unsigned 已使用容量=0,索引值=0;int 條目分存在判斷=0;
    while(索引值<(unsigned)組大小) {
        unsigned 運行=索引值;while(索引值<(unsigned)組大小 && 捆綁構建清單[索引值]!='\n')索引值++;
        unsigned 長度資料=索引值-運行;if(索引值<(unsigned)組大小)索引值++;if(長度資料 && 捆綁構建清單[運行+長度資料-1]=='\r')長度資料--;
        if(已使用容量 && 長度資料 && 捆綁構建清單[運行]==' ') {運行++;長度資料--;}
        else {
            int 結果=屬性資料(邏輯,已使用容量,&條目分存在判斷);if(結果)return 結果;
            已使用容量=0;if(!長度資料)break;
        }
        if(長度資料>sizeof(邏輯)-已使用容量)return -8;
        for(unsigned 序數索引=0;序數索引<長度資料;序數索引++)邏輯[已使用容量++]=捆綁構建清單[運行+序數索引];
    }
    /* The last attribute may be followed by only one newline. */
    int 結果=屬性資料(邏輯,已使用容量,&條目分存在判斷);if(結果)return 結果;
    return 條目分存在判斷?0:-8;
}
