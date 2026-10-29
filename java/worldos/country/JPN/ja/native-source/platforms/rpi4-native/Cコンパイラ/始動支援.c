#include "../命名/機械連結名前一覧.h"
#include "呼出.h"
extern int main(int,char **);
static char 引数配列[8][256];
int 利用者開始処理(int 未使用){
    (void)未使用;char *引数一覧[9];int 引数列個数=利用者呼出(15,UINTPTR_MAX,0,0,0,0,0);
    if(引数列個数<0||引数列個数>8)return 126;
    for(int 序数添字=0;序数添字<引数列個数;序数添字++){if(利用者呼出(15,序数添字,(uintptr_t)引数配列[序数添字],256,0,0,0)<0)return 126;引数一覧[序数添字]=引数配列[序数添字];}引数一覧[引数列個数]=0;
    return main(引数列個数,引数一覧);
}
void *memset(void*データ位置,int 文字コード,size_t 項目個数){unsigned char*宛先データ=データ位置;while(項目個数--)*宛先データ++=文字コード;return データ位置;}
void *memcpy(void*宛先データ,const void*文字列データ,size_t 項目個数){unsigned char*先頭位置値=宛先データ;const unsigned char*第二値=文字列データ;while(項目個数--)*先頭位置値++=*第二値++;return 宛先データ;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned 横座標,unsigned 縦座標,unsigned 幅値,unsigned 高さ値,unsigned 画素色){return 画面矩形(横座標,縦座標,幅値,高さ値,画素色);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 利用者呼出(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 対象画面キー待合();}
int 矩形描画処理(unsigned 水平位置,unsigned 垂直位置,unsigned 幅値,unsigned 高さ値,unsigned 画素色){return pk_rectangle(水平位置,垂直位置,幅値,高さ値,画素色);}
unsigned ミリ秒(void){return pk_ticks_ms();}
int 対象描画中待合(void){return pk_graphics_wait();}
int 画面幅(void){return 画面幅読取();}
int 画面高さ(void){return 画面高さ読取();}
