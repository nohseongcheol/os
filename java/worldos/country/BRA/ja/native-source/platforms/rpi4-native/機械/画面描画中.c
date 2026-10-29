/* 実際データ 画面 메모리와 기존 C 呼出 규약만 연결한다. 합성 구현은 ソース/描画領域組立器.java. */
#include "../命名/機械連結名前一覧.h"
#include "画面情報.h"
static volatile uint32_t *画素列一覧;
static unsigned 画面行番号語個数, 画面幅, 画面高さ;
extern void Java描画用意(int,int),Java描画終端位置(void),Java描画矩形(int,int,int,int,int),Java描画ポインタ(int,int,int);
extern int Java描画幅(void),Java描画高さ(void),Java描画個数下位(void),Java描画個数上位(void);
extern int Java描画切抜き(int,int,int,int),Java描画切抜き値(int),Java描画開始点(int,int,int,int),Java描画画素(int,int,int);
uintptr_t 基板描画領域読取(uintptr_t 水平位置,uintptr_t 垂直位置){
    return 画素列一覧&&水平位置<画面幅&&垂直位置<画面高さ?画素列一覧[垂直位置*画面行番号語個数+水平位置]:0;
}
void 基板描画領域書込(uintptr_t 水平位置,uintptr_t 垂直位置,uintptr_t 色値){
    if(画素列一覧&&水平位置<画面幅&&垂直位置<画面高さ)画素列一覧[垂直位置*画面行番号語個数+水平位置]=(uint32_t)色値;
}
void 基板用意描画中(volatile uint32_t *データ,unsigned 幅跨域,unsigned 長さ,unsigned 行間隔値){
    画素列一覧=データ;画面幅=幅跨域;画面高さ=長さ;画面行番号語個数=行間隔値/4;Java描画用意((int)幅跨域,(int)長さ);
}
uintptr_t 基板画面幅(void){return (unsigned)Java描画幅();}
uintptr_t 基板画面高さ(void){return (unsigned)Java描画高さ();}
uint64_t 基板描画中個数(void){return ((uint64_t)(uint32_t)Java描画個数上位()<<32)|(uint32_t)Java描画個数下位();}
uint32_t 基板読取画面(unsigned 水平位置,unsigned 垂直位置){return (uint32_t)基板描画領域読取(水平位置,垂直位置);}
int 基板描画中境界(int *水平位置,int *垂直位置,int *幅跨域,int *長さ){
    if(!Java描画切抜き(*水平位置,*垂直位置,*幅跨域,*長さ))return 0;
    *水平位置=Java描画切抜き値(0);*垂直位置=Java描画切抜き値(1);*幅跨域=Java描画切抜き値(2);*長さ=Java描画切抜き値(3);return 1;
}
int 基板開始処理描画中(int 水平位置,int 垂直位置,int 幅跨域,int 長さ){return Java描画開始点(水平位置,垂直位置,幅跨域,長さ);}
void 基板終了処理描画中(void){Java描画終端位置();}
uintptr_t 基板画素(uintptr_t 水平位置,uintptr_t 垂直位置,uintptr_t 色値){return (unsigned)Java描画画素((int)水平位置,(int)垂直位置,(int)色値);}
void 基板矩形塗潰し(int 水平位置,int 垂直位置,int 幅跨域,int 長さ,uint32_t 色値){Java描画矩形(水平位置,垂直位置,幅跨域,長さ,(int)色値);}
void 基板ポインタ(int 水平位置,int 垂直位置,unsigned 形状値){Java描画ポインタ(水平位置,垂直位置,(int)形状値);}
