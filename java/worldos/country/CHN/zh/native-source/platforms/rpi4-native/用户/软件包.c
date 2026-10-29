#include "../命名/计算机连接名称列.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "调用.h"
#include "软件包.h"
#include "uzlib.h"
static unsigned char 存档[16384], 已解包[16385];
static unsigned 大小, 中央, 条目列列表;
static char 条目类[256];
static unsigned 读取二字节列(unsigned 当前位置) { return 存档[当前位置] | 存档[当前位置+1] << 8; }
static uint32_t 读取四字节列(unsigned 当前位置) { return 读取二字节列(当前位置) | (uint32_t)读取二字节列(当前位置+2) << 16; }
static int 裁剪(unsigned 当前位置, unsigned 项目个数, unsigned 容量限制) { return 当前位置 <= 容量限制 && 项目个数 <= 容量限制-当前位置; }
static size_t 长度(const char *字符串数据) { size_t 项目个数=0; while(字符串数据[项目个数]) 项目个数++; return 项目个数; }
static int 相等文本(const unsigned char *首位值, const unsigned char *第二值, unsigned 项目个数) { for(unsigned 序数索引=0;序数索引<项目个数;序数索引++)if(首位值[序数索引]!=第二值[序数索引])return 0;return 1; }
static int 文件结束(void *未使用) { (void)未使用; return -1; }
static int 属性数据(const char *行,unsigned 已使用容量,int *条目分存在判断) {
    if(已使用容量>=12 && 相等文本((const unsigned char*)行,(const unsigned char*)"Class-Path: ",12))return -95;
    if(已使用容量>=12 && 相等文本((const unsigned char*)行,(const unsigned char*)"Main-Class: ",12)) {
        unsigned 值=已使用容量-12;if(*条目分存在判断||!值||值>=sizeof(条目类))return -8;
        for(unsigned 序数索引=0;序数索引<值;序数索引++){unsigned char 字符代码=行[12+序数索引];if(字符代码<=32||字符代码=='/'||字符代码=='\\')return -8;条目类[序数索引]=字符代码;}
        条目类[值]=0;*条目分存在判断=1;
    }
    return 0;
}
static int 成员(unsigned 当前位置, unsigned char *结果数据, unsigned 容量最大) {
    unsigned 方法条目=读取二字节列(当前位置+10), 配置项位列=读取二字节列(当前位置+8), 已压缩=读取四字节列(当前位置+20), 释放大小=读取四字节列(当前位置+24), 局部=读取四字节列(当前位置+42);
    unsigned 名称=读取二字节列(当前位置+28);
    if(释放大小>容量最大 || 释放大小>16384 || (方法条目!=0 && 方法条目!=8) || (配置项位列&~0x80e))return -8;
    if(!裁剪(局部,30,中央) || 读取四字节列(局部)!=0x04034b50 || 读取二字节列(局部+8)!=方法条目 || 读取二字节列(局部+6)!=配置项位列 || 读取二字节列(局部+26)!=名称)return -8;
    unsigned 开始偏移=局部+30, 附加区域=读取二字节列(局部+28);
    if(!裁剪(开始偏移,名称,中央) || !相等文本(存档+开始偏移,存档+当前位置+46,名称))return -8;
    开始偏移+=名称;if(!裁剪(开始偏移,附加区域,中央))return -8;开始偏移+=附加区域;
    if(!裁剪(开始偏移,已压缩,中央))return -8;
    if(!(配置项位列&8) && (读取四字节列(局部+14)!=读取四字节列(当前位置+16) || 读取四字节列(局部+18)!=已压缩 || 读取四字节列(局部+22)!=释放大小))return -8;
    if(方法条目==0) { if(已压缩!=释放大小)return -8; for(unsigned 序数索引=0;序数索引<释放大小;序数索引++)结果数据[序数索引]=存档[开始偏移+序数索引]; }
    else {
        uzlib_uncomp_t 目的地址数据={0};uzlib_uncompress_init(&目的地址数据,0,0);
        目的地址数据.source=存档+开始偏移;目的地址数据.source_limit=目的地址数据.source+已压缩;目的地址数据.source_read_cb=文件结束;
        /* One extra output byte lets inflate consume/check the end marker. */
        目的地址数据.dest_start=目的地址数据.dest=已解包;目的地址数据.dest_limit=已解包+释放大小+1;
        int 已返回值=uzlib_uncompress(&目的地址数据);
        if(已返回值!=UZLIB_DONE || 目的地址数据.eof || 目的地址数据.dest!=已解包+释放大小 || 目的地址数据.source!=目的地址数据.source_limit)return -8;
        for(unsigned 序数索引=0;序数索引<释放大小;序数索引++)结果数据[序数索引]=已解包[序数索引];
    }
    if((uzlib_crc32(结果数据,释放大小,0xffffffffu)^0xffffffffu)!=读取四字节列(当前位置+16))return -8;
    return 释放大小;
}
int JAR读取(const char *名称, unsigned char *结果数据, unsigned 缓冲容量) {
    if(!条目列列表)return -2;unsigned 项目个数=长度(名称),当前位置=中央;
    for(unsigned 序数索引=0;序数索引<条目列列表;序数索引++) {
        unsigned 名称长度=读取二字节列(当前位置+28);
        if(名称长度==项目个数 && 相等文本(存档+当前位置+46,(const unsigned char*)名称,项目个数))return 成员(当前位置,结果数据,缓冲容量);
        当前位置+=46+名称长度+读取二字节列(当前位置+30)+读取二字节列(当前位置+32);
    }
    return -2;
}
const char *JAR主操作(void) { return 条目类; }
int JAR打开(const char *文件条目名称) {
    条目列列表=0;条目类[0]=0;
    intptr_t 文件句柄=用户调用(3,(uintptr_t)文件条目名称,0,0,0,0,0);if(文件句柄<0)return 文件句柄;
    intptr_t 项目个数=用户调用(9,文件句柄,0,0,0,0,0);
    if(项目个数<22 || 项目个数>(intptr_t)sizeof(存档)) { 用户调用(4,文件句柄,0,0,0,0,0);return -8; }
    intptr_t 已接收个数=用户调用(2,文件句柄,(uintptr_t)存档,项目个数,0,0,0);用户调用(4,文件句柄,0,0,0,0,0);
    if(已接收个数!=项目个数)return -5;大小=项目个数;
    unsigned 结束偏移=大小-22;
    for(;;) { if(读取四字节列(结束偏移)==0x06054b50 && 结束偏移+22+读取二字节列(结束偏移+20)==大小)break; if(!结束偏移)return -8;结束偏移--; }
    unsigned 条目个数=读取二字节列(结束偏移+10);中央=读取四字节列(结束偏移+16);
    if(读取二字节列(结束偏移+4)||读取二字节列(结束偏移+6)||读取二字节列(结束偏移+8)!=条目个数||!条目个数||条目个数>256||!裁剪(中央,读取四字节列(结束偏移+12),结束偏移)||中央+读取四字节列(结束偏移+12)!=结束偏移)return -8;
    unsigned 当前位置=中央;
    for(unsigned 序数索引=0;序数索引<条目个数;序数索引++) {
        if(!裁剪(当前位置,46,结束偏移)||读取四字节列(当前位置)!=0x02014b50||读取二字节列(当前位置+34))return -8;
        unsigned 名称长度=读取二字节列(当前位置+28),下一项目=46+名称长度+读取二字节列(当前位置+30)+读取二字节列(当前位置+32);
        if(!名称长度||名称长度>511||!裁剪(当前位置,下一项目,结束偏移)||读取四字节列(当前位置+24)>16384)return -8;
        for(unsigned 内部侧序数=0;内部侧序数<名称长度;内部侧序数++)if(!存档[当前位置+46+内部侧序数])return -8;
        unsigned 其他条目=中央;
        for(unsigned 内部侧序数=0;内部侧序数<序数索引;内部侧序数++){unsigned 长度数据=读取二字节列(其他条目+28);if(长度数据==名称长度&&相等文本(存档+其他条目+46,存档+当前位置+46,长度数据))return -8;其他条目+=46+长度数据+读取二字节列(其他条目+30)+读取二字节列(其他条目+32);}
        当前位置+=下一项目;
    }
    if(当前位置!=结束偏移)return -8;条目列列表=条目个数;
    unsigned char 捆绑构建清单[4096];int 组大小=JAR读取("META-INF/MANIFEST.MF",捆绑构建清单,sizeof(捆绑构建清单)-1);if(组大小<0){条目列列表=0;return -8;}
    捆绑构建清单[组大小]=0;
    char 逻辑[512];unsigned 已使用容量=0,索引值=0;int 条目分存在判断=0;
    while(索引值<(unsigned)组大小) {
        unsigned 运行=索引值;while(索引值<(unsigned)组大小 && 捆绑构建清单[索引值]!='\n')索引值++;
        unsigned 长度数据=索引值-运行;if(索引值<(unsigned)组大小)索引值++;if(长度数据 && 捆绑构建清单[运行+长度数据-1]=='\r')长度数据--;
        if(已使用容量 && 长度数据 && 捆绑构建清单[运行]==' ') {运行++;长度数据--;}
        else {
            int 结果=属性数据(逻辑,已使用容量,&条目分存在判断);if(结果)return 结果;
            已使用容量=0;if(!长度数据)break;
        }
        if(长度数据>sizeof(逻辑)-已使用容量)return -8;
        for(unsigned 序数索引=0;序数索引<长度数据;序数索引++)逻辑[已使用容量++]=捆绑构建清单[运行+序数索引];
    }
    /* The last attribute may be followed by only one newline. */
    int 结果=属性数据(逻辑,已使用容量,&条目分存在判断);if(结果)return 结果;
    return 条目分存在判断?0:-8;
}
