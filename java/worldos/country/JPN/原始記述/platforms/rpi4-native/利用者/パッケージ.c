#include "../命名/機械連結名前一覧.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "呼出.h"
#include "パッケージ.h"
#include "uzlib.h"
static unsigned char 書庫[16384], 展開済み[16385];
static unsigned 容量, 中央, 登録項目一覧一覧;
static char 入口クラス[256];
static unsigned 二バイト列読取(unsigned 現在位置) { return 書庫[現在位置] | 書庫[現在位置+1] << 8; }
static uint32_t 四バイト列読取(unsigned 現在位置) { return 二バイト列読取(現在位置) | (uint32_t)二バイト列読取(現在位置+2) << 16; }
static int 切抜き(unsigned 現在位置, unsigned 項目個数, unsigned 容積上限) { return 現在位置 <= 容積上限 && 項目個数 <= 容積上限-現在位置; }
static size_t 長さ(const char *文字列データ) { size_t 項目個数=0; while(文字列データ[項目個数]) 項目個数++; return 項目個数; }
static int 等価本文(const unsigned char *先頭位置値, const unsigned char *第二値, unsigned 項目個数) { for(unsigned 序数添字=0;序数添字<項目個数;序数添字++)if(先頭位置値[序数添字]!=第二値[序数添字])return 0;return 1; }
static int ファイル終端位置(void *未使用) { (void)未使用; return -1; }
static int 属性データ(const char *行,unsigned 使用済み容積,int *入口点存在判定) {
    if(使用済み容積>=12 && 等価本文((const unsigned char*)行,(const unsigned char*)"Class-Path: ",12))return -95;
    if(使用済み容積>=12 && 等価本文((const unsigned char*)行,(const unsigned char*)"Main-Class: ",12)) {
        unsigned 値=使用済み容積-12;if(*入口点存在判定||!値||値>=sizeof(入口クラス))return -8;
        for(unsigned 序数添字=0;序数添字<値;序数添字++){unsigned char 文字コード=行[12+序数添字];if(文字コード<=32||文字コード=='/'||文字コード=='\\')return -8;入口クラス[序数添字]=文字コード;}
        入口クラス[値]=0;*入口点存在判定=1;
    }
    return 0;
}
static int 成員(unsigned 現在位置, unsigned char *結果データ, unsigned 容積最大) {
    unsigned メソッド入口=二バイト列読取(現在位置+10), 構成設定ビット列=二バイト列読取(現在位置+8), 圧縮済み=四バイト列読取(現在位置+20), 容量解放=四バイト列読取(現在位置+24), 局所=四バイト列読取(現在位置+42);
    unsigned 名前=二バイト列読取(現在位置+28);
    if(容量解放>容積最大 || 容量解放>16384 || (メソッド入口!=0 && メソッド入口!=8) || (構成設定ビット列&~0x80e))return -8;
    if(!切抜き(局所,30,中央) || 四バイト列読取(局所)!=0x04034b50 || 二バイト列読取(局所+8)!=メソッド入口 || 二バイト列読取(局所+6)!=構成設定ビット列 || 二バイト列読取(局所+26)!=名前)return -8;
    unsigned 変位量開始処理=局所+30, 追加分領域=二バイト列読取(局所+28);
    if(!切抜き(変位量開始処理,名前,中央) || !等価本文(書庫+変位量開始処理,書庫+現在位置+46,名前))return -8;
    変位量開始処理+=名前;if(!切抜き(変位量開始処理,追加分領域,中央))return -8;変位量開始処理+=追加分領域;
    if(!切抜き(変位量開始処理,圧縮済み,中央))return -8;
    if(!(構成設定ビット列&8) && (四バイト列読取(局所+14)!=四バイト列読取(現在位置+16) || 四バイト列読取(局所+18)!=圧縮済み || 四バイト列読取(局所+22)!=容量解放))return -8;
    if(メソッド入口==0) { if(圧縮済み!=容量解放)return -8; for(unsigned 序数添字=0;序数添字<容量解放;序数添字++)結果データ[序数添字]=書庫[変位量開始処理+序数添字]; }
    else {
        uzlib_uncomp_t 宛先データ={0};uzlib_uncompress_init(&宛先データ,0,0);
        宛先データ.source=書庫+変位量開始処理;宛先データ.source_limit=宛先データ.source+圧縮済み;宛先データ.source_read_cb=ファイル終端位置;
        /* One extra output byte lets inflate consume/check the end marker. */
        宛先データ.dest_start=宛先データ.dest=展開済み;宛先データ.dest_limit=展開済み+容量解放+1;
        int 返却済み値=uzlib_uncompress(&宛先データ);
        if(返却済み値!=UZLIB_DONE || 宛先データ.eof || 宛先データ.dest!=展開済み+容量解放 || 宛先データ.source!=宛先データ.source_limit)return -8;
        for(unsigned 序数添字=0;序数添字<容量解放;序数添字++)結果データ[序数添字]=展開済み[序数添字];
    }
    if((uzlib_crc32(結果データ,容量解放,0xffffffffu)^0xffffffffu)!=四バイト列読取(現在位置+16))return -8;
    return 容量解放;
}
int JAR読取(const char *名前, unsigned char *結果データ, unsigned 緩衝域容積) {
    if(!登録項目一覧一覧)return -2;unsigned 項目個数=長さ(名前),現在位置=中央;
    for(unsigned 序数添字=0;序数添字<登録項目一覧一覧;序数添字++) {
        unsigned 名前長=二バイト列読取(現在位置+28);
        if(名前長==項目個数 && 等価本文(書庫+現在位置+46,(const unsigned char*)名前,項目個数))return 成員(現在位置,結果データ,緩衝域容積);
        現在位置+=46+名前長+二バイト列読取(現在位置+30)+二バイト列読取(現在位置+32);
    }
    return -2;
}
const char *JAR主処理(void) { return 入口クラス; }
int JAR開放(const char *ファイル入口名前) {
    登録項目一覧一覧=0;入口クラス[0]=0;
    intptr_t ファイル取扱い=利用者呼出(3,(uintptr_t)ファイル入口名前,0,0,0,0,0);if(ファイル取扱い<0)return ファイル取扱い;
    intptr_t 項目個数=利用者呼出(9,ファイル取扱い,0,0,0,0,0);
    if(項目個数<22 || 項目個数>(intptr_t)sizeof(書庫)) { 利用者呼出(4,ファイル取扱い,0,0,0,0,0);return -8; }
    intptr_t 受信済み個数=利用者呼出(2,ファイル取扱い,(uintptr_t)書庫,項目個数,0,0,0);利用者呼出(4,ファイル取扱い,0,0,0,0,0);
    if(受信済み個数!=項目個数)return -5;容量=項目個数;
    unsigned 終端位置変位量=容量-22;
    for(;;) { if(四バイト列読取(終端位置変位量)==0x06054b50 && 終端位置変位量+22+二バイト列読取(終端位置変位量+20)==容量)break; if(!終端位置変位量)return -8;終端位置変位量--; }
    unsigned 入口個数=二バイト列読取(終端位置変位量+10);中央=四バイト列読取(終端位置変位量+16);
    if(二バイト列読取(終端位置変位量+4)||二バイト列読取(終端位置変位量+6)||二バイト列読取(終端位置変位量+8)!=入口個数||!入口個数||入口個数>256||!切抜き(中央,四バイト列読取(終端位置変位量+12),終端位置変位量)||中央+四バイト列読取(終端位置変位量+12)!=終端位置変位量)return -8;
    unsigned 現在位置=中央;
    for(unsigned 序数添字=0;序数添字<入口個数;序数添字++) {
        if(!切抜き(現在位置,46,終端位置変位量)||四バイト列読取(現在位置)!=0x02014b50||二バイト列読取(現在位置+34))return -8;
        unsigned 名前長=二バイト列読取(現在位置+28),次回項目=46+名前長+二バイト列読取(現在位置+30)+二バイト列読取(現在位置+32);
        if(!名前長||名前長>511||!切抜き(現在位置,次回項目,終端位置変位量)||四バイト列読取(現在位置+24)>16384)return -8;
        for(unsigned 内側序数=0;内側序数<名前長;内側序数++)if(!書庫[現在位置+46+内側序数])return -8;
        unsigned 他方入口=中央;
        for(unsigned 内側序数=0;内側序数<序数添字;内側序数++){unsigned 長さデータ=二バイト列読取(他方入口+28);if(長さデータ==名前長&&等価本文(書庫+他方入口+46,書庫+現在位置+46,長さデータ))return -8;他方入口+=46+長さデータ+二バイト列読取(他方入口+30)+二バイト列読取(他方入口+32);}
        現在位置+=次回項目;
    }
    if(現在位置!=終端位置変位量)return -8;登録項目一覧一覧=入口個数;
    unsigned char 束管理目録[4096];int 集合容量=JAR読取("META-INF/MANIFEST.MF",束管理目録,sizeof(束管理目録)-1);if(集合容量<0){登録項目一覧一覧=0;return -8;}
    束管理目録[集合容量]=0;
    char 論理[512];unsigned 使用済み容積=0,添字値=0;int 入口点存在判定=0;
    while(添字値<(unsigned)集合容量) {
        unsigned 起動処理=添字値;while(添字値<(unsigned)集合容量 && 束管理目録[添字値]!='\n')添字値++;
        unsigned 長さデータ=添字値-起動処理;if(添字値<(unsigned)集合容量)添字値++;if(長さデータ && 束管理目録[起動処理+長さデータ-1]=='\r')長さデータ--;
        if(使用済み容積 && 長さデータ && 束管理目録[起動処理]==' ') {起動処理++;長さデータ--;}
        else {
            int 結果=属性データ(論理,使用済み容積,&入口点存在判定);if(結果)return 結果;
            使用済み容積=0;if(!長さデータ)break;
        }
        if(長さデータ>sizeof(論理)-使用済み容積)return -8;
        for(unsigned 序数添字=0;序数添字<長さデータ;序数添字++)論理[使用済み容積++]=束管理目録[起動処理+序数添字];
    }
    /* The last attribute may be followed by only one newline. */
    int 結果=属性データ(論理,使用済み容積,&入口点存在判定);if(結果)return 結果;
    return 入口点存在判定?0:-8;
}
