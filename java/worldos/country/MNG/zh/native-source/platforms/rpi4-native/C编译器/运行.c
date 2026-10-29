#include "../命名/计算机连接名称列.h"
#include "调用.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C输出(size_t *);
extern const char *Java提前编译源代码(const char *);
typedef struct { unsigned char 标识符值[16];uint16_t 类型分类,计算机类型;uint32_t 版本编号;uint64_t 条目分,程序头部偏移,区段头部偏移;uint32_t 配置项位列;uint16_t 大小,程序头部大小,程序头部个数,区段头部大小,区段头部个数,区段名称表; } 头部值;
typedef struct {uint32_t 类型分类,配置项位列;uint64_t 偏移值,地址,物理地址,文件区域大小,内存区大小,对齐边界位置;} 段值;
static unsigned char 映像[16384];
static int 发布条目(const char *名称){
    size_t 项目个数;const unsigned char*原始数据=C输出(&项目个数);if(项目个数<sizeof(头部值))return -1;
    头部值 可执行文件头部;memcpy(&可执行文件头部,原始数据,sizeof(可执行文件头部));
    if(可执行文件头部.类型分类!=2||可执行文件头部.计算机类型!=183||可执行文件头部.程序头部大小!=sizeof(段值)||!可执行文件头部.程序头部个数||可执行文件头部.程序头部个数>16||可执行文件头部.程序头部偏移>项目个数||可执行文件头部.程序头部个数*sizeof(段值)>项目个数-可执行文件头部.程序头部偏移)return -1;
    可执行文件头部.程序头部偏移=sizeof(可执行文件头部);可执行文件头部.区段头部偏移=可执行文件头部.区段头部个数=可执行文件头部.区段头部大小=可执行文件头部.区段名称表=0;memcpy(映像,&可执行文件头部,sizeof(可执行文件头部));
    size_t 辅助信息=sizeof(可执行文件头部)+可执行文件头部.程序头部个数*sizeof(段值),下一项目=4096;unsigned char 页列表[3072]={0};int 有效条目分=0;
    for(unsigned 序数索引=0;序数索引<可执行文件头部.程序头部个数;序数索引++){
        段值 数据位置;头部值 原始;memcpy(&原始,原始数据,sizeof(原始));memcpy(&数据位置,原始数据+原始.程序头部偏移+序数索引*sizeof(数据位置),sizeof(数据位置));
        if(数据位置.偏移值>项目个数||数据位置.文件区域大小>项目个数-数据位置.偏移值||数据位置.文件区域大小>数据位置.内存区大小)return -1;
        if(数据位置.类型分类==1){
            if((数据位置.配置项位列&~7u)||!(数据位置.配置项位列&4)||(数据位置.配置项位列&3)==3||数据位置.地址<0x02000000||数据位置.地址>0x02c00000||数据位置.内存区大小>0x02c00000-数据位置.地址)return -1;
            if((数据位置.配置项位列&1)&&可执行文件头部.条目分>=数据位置.地址&&可执行文件头部.条目分-数据位置.地址<数据位置.文件区域大小&&!(可执行文件头部.条目分&3))有效条目分=1;
            size_t 前置值=数据位置.地址&4095,字节值列=数据位置.文件区域大小?前置值+数据位置.文件区域大小:0;
            if(下一项目>sizeof(映像)||字节值列>sizeof(映像)-下一项目){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(下一项目+字节值列),(unsigned)sizeof(映像));return -1;}
            if(字节值列)memcpy(映像+下一项目+前置值,原始数据+数据位置.偏移值,数据位置.文件区域大小);
            数据位置.地址-=前置值;数据位置.物理地址=数据位置.地址;数据位置.内存区大小+=前置值;数据位置.文件区域大小=字节值列;数据位置.偏移值=下一项目;数据位置.对齐边界位置=4096;
            for(uint64_t 页值=数据位置.地址;页值<数据位置.地址+数据位置.内存区大小;页值+=4096){unsigned 查找索引=(页值-0x02000000)/4096;if(查找索引>=sizeof(页列表)||页列表[查找索引]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}页列表[查找索引]=1;}
            下一项目+=(字节值列+4095)&~(size_t)4095;
        }else if(数据位置.类型分类==4){if(数据位置.文件区域大小>4096-辅助信息)return -1;memcpy(映像+辅助信息,原始数据+数据位置.偏移值,数据位置.文件区域大小);数据位置.偏移值=辅助信息;辅助信息+=数据位置.文件区域大小;}
        else if(数据位置.类型分类!=0&&数据位置.类型分类!=6&&数据位置.类型分类!=0x6474e551)return -1;
        memcpy(映像+可执行文件头部.程序头部偏移+序数索引*sizeof(数据位置),&数据位置,sizeof(数据位置));
    }
    if(!有效条目分)return -1;
    intptr_t 文件句柄=用户调用(3,(uintptr_t)名称,577,0600,0,0,0);if(文件句柄<0){printf("cc: cannot create output file, error %d\n",(int)文件句柄);return -1;}
    intptr_t 已写入=用户调用(1,文件句柄,(uintptr_t)映像,下一项目,0,0,0);用户调用(4,文件句柄,0,0,0,0,0);return 已写入==(intptr_t)下一项目?0:-1;
}
int 开始用户程序(int 方法模式){
    char 输入结果[256],已选择条目[256],输出结果[256]="a.elf";
    int 参数列个数=用户调用(15,UINTPTR_MAX,0,0,0,0,0);
    if(参数列个数!=1&&参数列个数!=3){printf(方法模式?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(用户调用(15,0,(uintptr_t)输入结果,sizeof(输入结果),0,0,0)<0)return 2;
    if(参数列个数==1&&(!strcmp(输入结果,"--version")||!strcmp(输入结果,"-version"))){printf(方法模式?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(参数列个数==3){用户调用(15,1,(uintptr_t)已选择条目,sizeof(已选择条目),0,0,0);if(strcmp(已选择条目,"-o")||用户调用(15,2,(uintptr_t)输出结果,sizeof(输出结果),0,0,0)<0)return 2;}
    if(!strcmp(输入结果,输出结果)){printf("cc: input and output must differ\n");return 2;}
    TCCState*字符串数据=tcc_new();if(!字符串数据)return 1;
    tcc_undefine_symbol(字符串数据,"__linux__");tcc_undefine_symbol(字符串数据,"__linux");tcc_undefine_symbol(字符串数据,"linux");
    tcc_undefine_symbol(字符串数据,"__unix__");tcc_undefine_symbol(字符串数据,"__unix");tcc_undefine_symbol(字符串数据,"unix");
    tcc_undefine_symbol(字符串数据,"__STDC_HOSTED__");tcc_define_symbol(字符串数据,"__STDC_HOSTED__","0");tcc_define_symbol(字符串数据,"__JKOROS__","1");
    tcc_set_options(字符串数据,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(字符串数据,"/sdk/include");
    int 已返回值=tcc_set_output_type(字符串数据,TCC_OUTPUT_EXE);
    if(!已返回值){if(方法模式){const char*原始数据=Java提前编译源代码(输入结果);已返回值=原始数据?tcc_compile_string(字符串数据,原始数据):-1;}else 已返回值=tcc_add_file(字符串数据,输入结果);}
    if(!已返回值)已返回值=tcc_add_file(字符串数据,"/sdk/lib/start.o");
    if(!已返回值)已返回值=tcc_add_file(字符串数据,"/sdk/lib/crt.o");
    if(!已返回值&&方法模式)已返回值=tcc_add_file(字符串数据,"/sdk/lib/aot-runtime.o");
    if(!已返回值)已返回值=tcc_add_file(字符串数据,"/sdk/lib/libposix-kor-user.a");
    if(!已返回值)已返回值=tcc_output_file(字符串数据,"/@cc-output");
    if(!已返回值)已返回值=发布条目(输出结果);
    tcc_delete(字符串数据);
    if(已返回值){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(方法模式?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",输出结果);return 0;
}
