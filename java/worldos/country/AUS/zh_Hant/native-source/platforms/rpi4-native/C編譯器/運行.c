#include "../命名/計算機連接名稱列.h"
#include "調用.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C輸出(size_t *);
extern const char *Java提前編譯原始碼(const char *);
typedef struct { unsigned char 標識符值[16];uint16_t 類型分類,計算機類型;uint32_t 版本編號;uint64_t 條目分,程式標頭偏移,區段標頭偏移;uint32_t 配置項位元列;uint16_t 大小,程式標頭大小,程式標頭個數,區段標頭大小,區段標頭個數,區段名稱表; } 標頭值;
typedef struct {uint32_t 類型分類,配置項位元列;uint64_t 偏移值,地址,物理地址,文件區域大小,內存區大小,對齊邊界位置;} 段值;
static unsigned char 映像[16384];
static int 發佈條目(const char *名稱){
    size_t 項目個數;const unsigned char*原始資料=C輸出(&項目個數);if(項目個數<sizeof(標頭值))return -1;
    標頭值 可執行文件標頭;memcpy(&可執行文件標頭,原始資料,sizeof(可執行文件標頭));
    if(可執行文件標頭.類型分類!=2||可執行文件標頭.計算機類型!=183||可執行文件標頭.程式標頭大小!=sizeof(段值)||!可執行文件標頭.程式標頭個數||可執行文件標頭.程式標頭個數>16||可執行文件標頭.程式標頭偏移>項目個數||可執行文件標頭.程式標頭個數*sizeof(段值)>項目個數-可執行文件標頭.程式標頭偏移)return -1;
    可執行文件標頭.程式標頭偏移=sizeof(可執行文件標頭);可執行文件標頭.區段標頭偏移=可執行文件標頭.區段標頭個數=可執行文件標頭.區段標頭大小=可執行文件標頭.區段名稱表=0;memcpy(映像,&可執行文件標頭,sizeof(可執行文件標頭));
    size_t 輔助信息=sizeof(可執行文件標頭)+可執行文件標頭.程式標頭個數*sizeof(段值),下一項目=4096;unsigned char 頁列表[3072]={0};int 有效條目分=0;
    for(unsigned 序數索引=0;序數索引<可執行文件標頭.程式標頭個數;序數索引++){
        段值 資料位置;標頭值 原始;memcpy(&原始,原始資料,sizeof(原始));memcpy(&資料位置,原始資料+原始.程式標頭偏移+序數索引*sizeof(資料位置),sizeof(資料位置));
        if(資料位置.偏移值>項目個數||資料位置.文件區域大小>項目個數-資料位置.偏移值||資料位置.文件區域大小>資料位置.內存區大小)return -1;
        if(資料位置.類型分類==1){
            if((資料位置.配置項位元列&~7u)||!(資料位置.配置項位元列&4)||(資料位置.配置項位元列&3)==3||資料位置.地址<0x02000000||資料位置.地址>0x02c00000||資料位置.內存區大小>0x02c00000-資料位置.地址)return -1;
            if((資料位置.配置項位元列&1)&&可執行文件標頭.條目分>=資料位置.地址&&可執行文件標頭.條目分-資料位置.地址<資料位置.文件區域大小&&!(可執行文件標頭.條目分&3))有效條目分=1;
            size_t 前置值=資料位置.地址&4095,位元組值列=資料位置.文件區域大小?前置值+資料位置.文件區域大小:0;
            if(下一項目>sizeof(映像)||位元組值列>sizeof(映像)-下一項目){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(下一項目+位元組值列),(unsigned)sizeof(映像));return -1;}
            if(位元組值列)memcpy(映像+下一項目+前置值,原始資料+資料位置.偏移值,資料位置.文件區域大小);
            資料位置.地址-=前置值;資料位置.物理地址=資料位置.地址;資料位置.內存區大小+=前置值;資料位置.文件區域大小=位元組值列;資料位置.偏移值=下一項目;資料位置.對齊邊界位置=4096;
            for(uint64_t 頁值=資料位置.地址;頁值<資料位置.地址+資料位置.內存區大小;頁值+=4096){unsigned 查找索引=(頁值-0x02000000)/4096;if(查找索引>=sizeof(頁列表)||頁列表[查找索引]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}頁列表[查找索引]=1;}
            下一項目+=(位元組值列+4095)&~(size_t)4095;
        }else if(資料位置.類型分類==4){if(資料位置.文件區域大小>4096-輔助信息)return -1;memcpy(映像+輔助信息,原始資料+資料位置.偏移值,資料位置.文件區域大小);資料位置.偏移值=輔助信息;輔助信息+=資料位置.文件區域大小;}
        else if(資料位置.類型分類!=0&&資料位置.類型分類!=6&&資料位置.類型分類!=0x6474e551)return -1;
        memcpy(映像+可執行文件標頭.程式標頭偏移+序數索引*sizeof(資料位置),&資料位置,sizeof(資料位置));
    }
    if(!有效條目分)return -1;
    intptr_t 檔案句柄=用戶調用(3,(uintptr_t)名稱,577,0600,0,0,0);if(檔案句柄<0){printf("cc: cannot create output file, error %d\n",(int)檔案句柄);return -1;}
    intptr_t 已寫入=用戶調用(1,檔案句柄,(uintptr_t)映像,下一項目,0,0,0);用戶調用(4,檔案句柄,0,0,0,0,0);return 已寫入==(intptr_t)下一項目?0:-1;
}
int 開始用戶程式(int 方法模式){
    char 輸入結果[256],已選擇條目[256],輸出結果[256]="a.elf";
    int 參數列個數=用戶調用(15,UINTPTR_MAX,0,0,0,0,0);
    if(參數列個數!=1&&參數列個數!=3){printf(方法模式?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(用戶調用(15,0,(uintptr_t)輸入結果,sizeof(輸入結果),0,0,0)<0)return 2;
    if(參數列個數==1&&(!strcmp(輸入結果,"--version")||!strcmp(輸入結果,"-version"))){printf(方法模式?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(參數列個數==3){用戶調用(15,1,(uintptr_t)已選擇條目,sizeof(已選擇條目),0,0,0);if(strcmp(已選擇條目,"-o")||用戶調用(15,2,(uintptr_t)輸出結果,sizeof(輸出結果),0,0,0)<0)return 2;}
    if(!strcmp(輸入結果,輸出結果)){printf("cc: input and output must differ\n");return 2;}
    TCCState*字符串資料=tcc_new();if(!字符串資料)return 1;
    tcc_undefine_symbol(字符串資料,"__linux__");tcc_undefine_symbol(字符串資料,"__linux");tcc_undefine_symbol(字符串資料,"linux");
    tcc_undefine_symbol(字符串資料,"__unix__");tcc_undefine_symbol(字符串資料,"__unix");tcc_undefine_symbol(字符串資料,"unix");
    tcc_undefine_symbol(字符串資料,"__STDC_HOSTED__");tcc_define_symbol(字符串資料,"__STDC_HOSTED__","0");tcc_define_symbol(字符串資料,"__JKOROS__","1");
    tcc_set_options(字符串資料,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(字符串資料,"/sdk/include");
    int 已返回值=tcc_set_output_type(字符串資料,TCC_OUTPUT_EXE);
    if(!已返回值){if(方法模式){const char*原始資料=Java提前編譯原始碼(輸入結果);已返回值=原始資料?tcc_compile_string(字符串資料,原始資料):-1;}else 已返回值=tcc_add_file(字符串資料,輸入結果);}
    if(!已返回值)已返回值=tcc_add_file(字符串資料,"/sdk/lib/start.o");
    if(!已返回值)已返回值=tcc_add_file(字符串資料,"/sdk/lib/crt.o");
    if(!已返回值&&方法模式)已返回值=tcc_add_file(字符串資料,"/sdk/lib/aot-runtime.o");
    if(!已返回值)已返回值=tcc_add_file(字符串資料,"/sdk/lib/libposix-kor-user.a");
    if(!已返回值)已返回值=tcc_output_file(字符串資料,"/@cc-output");
    if(!已返回值)已返回值=發佈條目(輸出結果);
    tcc_delete(字符串資料);
    if(已返回值){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(方法模式?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",輸出結果);return 0;
}
