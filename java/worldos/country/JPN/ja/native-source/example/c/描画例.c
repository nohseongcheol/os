#include "用例規約.h"
int main(void) {
    if(矩形描画処理(600,400,28,20,0x0000ff)<0)return 1;
    if(矩形描画処理(600,425,28,20,0x00ff00)<0)return 2;
    if(矩形描画処理(600,450,28,20,0xff0000)<0)return 3;
    出力("C 그래픽: RGB\nEnter\n");
    return 対象描画中待合()<0?4:0;
}
