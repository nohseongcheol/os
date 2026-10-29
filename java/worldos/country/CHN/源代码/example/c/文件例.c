#include "示例约定.h"
int main(void) {
    const char 数据[]="C 文件: Chinese 😀\n";
    int 文件=打开文件("c.txt",读取写入|创建条件缺失|截断内容,0600);
    if(文件<0)return 1;
    if(写入文件数据(文件,数据,sizeof(数据)-1)!=sizeof(数据)-1)return 2;
    if(寻道文件(文件,0,起点开头)!=0)return 3;
    char 读取文本值[128]={0};int 长度=读取文件数据(文件,读取文本值,sizeof(读取文本值)-1);
    关闭文件(文件);
    if(长度!=sizeof(数据)-1)return 4;
    for(int 数=0;数<长度;数++)if(数据[数]!=读取文本值[数])return 5;
    return 输出(读取文本值);
}
