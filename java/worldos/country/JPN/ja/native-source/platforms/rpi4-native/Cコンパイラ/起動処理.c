#include "../命名/機械連結名前一覧.h"
#include "呼出.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C出力(size_t *);
extern const char *Java事前翻訳ソース(const char *);
typedef struct { unsigned char 識別子値[16];uint16_t 型分類,機械型;uint32_t 版番号;uint64_t 入口点,プログラムヘッダー変位量,区画ヘッダー変位量;uint32_t 構成設定ビット列;uint16_t 容量,プログラムヘッダー容量,プログラムヘッダー個数,区画ヘッダー容量,区画ヘッダー個数,区画名前表; } ヘッダー値;
typedef struct {uint32_t 型分類,構成設定ビット列;uint64_t 変位量値,番地,物理番地,ファイル領域容量,メモリ容量,整列境界位置;} 区間値;
static unsigned char イメージ[16384];
static int 公表入口(const char *名前){
    size_t 項目個数;const unsigned char*原本データ=C出力(&項目個数);if(項目個数<sizeof(ヘッダー値))return -1;
    ヘッダー値 実行形式ヘッダー;memcpy(&実行形式ヘッダー,原本データ,sizeof(実行形式ヘッダー));
    if(実行形式ヘッダー.型分類!=2||実行形式ヘッダー.機械型!=183||実行形式ヘッダー.プログラムヘッダー容量!=sizeof(区間値)||!実行形式ヘッダー.プログラムヘッダー個数||実行形式ヘッダー.プログラムヘッダー個数>16||実行形式ヘッダー.プログラムヘッダー変位量>項目個数||実行形式ヘッダー.プログラムヘッダー個数*sizeof(区間値)>項目個数-実行形式ヘッダー.プログラムヘッダー変位量)return -1;
    実行形式ヘッダー.プログラムヘッダー変位量=sizeof(実行形式ヘッダー);実行形式ヘッダー.区画ヘッダー変位量=実行形式ヘッダー.区画ヘッダー個数=実行形式ヘッダー.区画ヘッダー容量=実行形式ヘッダー.区画名前表=0;memcpy(イメージ,&実行形式ヘッダー,sizeof(実行形式ヘッダー));
    size_t 補助情報=sizeof(実行形式ヘッダー)+実行形式ヘッダー.プログラムヘッダー個数*sizeof(区間値),次回項目=4096;unsigned char ページ一覧[3072]={0};int 妥当入口点=0;
    for(unsigned 序数添字=0;序数添字<実行形式ヘッダー.プログラムヘッダー個数;序数添字++){
        区間値 データ位置;ヘッダー値 原本;memcpy(&原本,原本データ,sizeof(原本));memcpy(&データ位置,原本データ+原本.プログラムヘッダー変位量+序数添字*sizeof(データ位置),sizeof(データ位置));
        if(データ位置.変位量値>項目個数||データ位置.ファイル領域容量>項目個数-データ位置.変位量値||データ位置.ファイル領域容量>データ位置.メモリ容量)return -1;
        if(データ位置.型分類==1){
            if((データ位置.構成設定ビット列&~7u)||!(データ位置.構成設定ビット列&4)||(データ位置.構成設定ビット列&3)==3||データ位置.番地<0x02000000||データ位置.番地>0x02c00000||データ位置.メモリ容量>0x02c00000-データ位置.番地)return -1;
            if((データ位置.構成設定ビット列&1)&&実行形式ヘッダー.入口点>=データ位置.番地&&実行形式ヘッダー.入口点-データ位置.番地<データ位置.ファイル領域容量&&!(実行形式ヘッダー.入口点&3))妥当入口点=1;
            size_t 直前値=データ位置.番地&4095,バイト値一覧=データ位置.ファイル領域容量?直前値+データ位置.ファイル領域容量:0;
            if(次回項目>sizeof(イメージ)||バイト値一覧>sizeof(イメージ)-次回項目){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(次回項目+バイト値一覧),(unsigned)sizeof(イメージ));return -1;}
            if(バイト値一覧)memcpy(イメージ+次回項目+直前値,原本データ+データ位置.変位量値,データ位置.ファイル領域容量);
            データ位置.番地-=直前値;データ位置.物理番地=データ位置.番地;データ位置.メモリ容量+=直前値;データ位置.ファイル領域容量=バイト値一覧;データ位置.変位量値=次回項目;データ位置.整列境界位置=4096;
            for(uint64_t ページ値=データ位置.番地;ページ値<データ位置.番地+データ位置.メモリ容量;ページ値+=4096){unsigned 検索添字=(ページ値-0x02000000)/4096;if(検索添字>=sizeof(ページ一覧)||ページ一覧[検索添字]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ページ一覧[検索添字]=1;}
            次回項目+=(バイト値一覧+4095)&~(size_t)4095;
        }else if(データ位置.型分類==4){if(データ位置.ファイル領域容量>4096-補助情報)return -1;memcpy(イメージ+補助情報,原本データ+データ位置.変位量値,データ位置.ファイル領域容量);データ位置.変位量値=補助情報;補助情報+=データ位置.ファイル領域容量;}
        else if(データ位置.型分類!=0&&データ位置.型分類!=6&&データ位置.型分類!=0x6474e551)return -1;
        memcpy(イメージ+実行形式ヘッダー.プログラムヘッダー変位量+序数添字*sizeof(データ位置),&データ位置,sizeof(データ位置));
    }
    if(!妥当入口点)return -1;
    intptr_t ファイル取扱い=利用者呼出(3,(uintptr_t)名前,577,0600,0,0,0);if(ファイル取扱い<0){printf("cc: cannot create output file, error %d\n",(int)ファイル取扱い);return -1;}
    intptr_t 書込済み=利用者呼出(1,ファイル取扱い,(uintptr_t)イメージ,次回項目,0,0,0);利用者呼出(4,ファイル取扱い,0,0,0,0,0);return 書込済み==(intptr_t)次回項目?0:-1;
}
int 利用者プログラム開始処理(int メソッド方式){
    char 入力結果[256],選択済み入口[256],出力結果[256]="a.elf";
    int 引数列個数=利用者呼出(15,UINTPTR_MAX,0,0,0,0,0);
    if(引数列個数!=1&&引数列個数!=3){printf(メソッド方式?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(利用者呼出(15,0,(uintptr_t)入力結果,sizeof(入力結果),0,0,0)<0)return 2;
    if(引数列個数==1&&(!strcmp(入力結果,"--version")||!strcmp(入力結果,"-version"))){printf(メソッド方式?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(引数列個数==3){利用者呼出(15,1,(uintptr_t)選択済み入口,sizeof(選択済み入口),0,0,0);if(strcmp(選択済み入口,"-o")||利用者呼出(15,2,(uintptr_t)出力結果,sizeof(出力結果),0,0,0)<0)return 2;}
    if(!strcmp(入力結果,出力結果)){printf("cc: input and output must differ\n");return 2;}
    TCCState*文字列データ=tcc_new();if(!文字列データ)return 1;
    tcc_undefine_symbol(文字列データ,"__linux__");tcc_undefine_symbol(文字列データ,"__linux");tcc_undefine_symbol(文字列データ,"linux");
    tcc_undefine_symbol(文字列データ,"__unix__");tcc_undefine_symbol(文字列データ,"__unix");tcc_undefine_symbol(文字列データ,"unix");
    tcc_undefine_symbol(文字列データ,"__STDC_HOSTED__");tcc_define_symbol(文字列データ,"__STDC_HOSTED__","0");tcc_define_symbol(文字列データ,"__JKOROS__","1");
    tcc_set_options(文字列データ,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(文字列データ,"/sdk/include");
    int 返却済み値=tcc_set_output_type(文字列データ,TCC_OUTPUT_EXE);
    if(!返却済み値){if(メソッド方式){const char*原本データ=Java事前翻訳ソース(入力結果);返却済み値=原本データ?tcc_compile_string(文字列データ,原本データ):-1;}else 返却済み値=tcc_add_file(文字列データ,入力結果);}
    if(!返却済み値)返却済み値=tcc_add_file(文字列データ,"/sdk/lib/start.o");
    if(!返却済み値)返却済み値=tcc_add_file(文字列データ,"/sdk/lib/crt.o");
    if(!返却済み値&&メソッド方式)返却済み値=tcc_add_file(文字列データ,"/sdk/lib/aot-runtime.o");
    if(!返却済み値)返却済み値=tcc_add_file(文字列データ,"/sdk/lib/libposix-kor-user.a");
    if(!返却済み値)返却済み値=tcc_output_file(文字列データ,"/@cc-output");
    if(!返却済み値)返却済み値=公表入口(出力結果);
    tcc_delete(文字列データ);
    if(返却済み値){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(メソッド方式?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",出力結果);return 0;
}
