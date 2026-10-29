#include "示例约定.h"
int main(void) {
    if(绘制矩形(600,400,28,20,0x0000ff)<0)return 1;
    if(绘制矩形(600,425,28,20,0x00ff00)<0)return 2;
    if(绘制矩形(600,450,28,20,0xff0000)<0)return 3;
    输出("C 그래픽: RGB\nEnter\n");
    return 等待状态用于绘图()<0?4:0;
}
