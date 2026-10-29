#include "用例規約.h"
int main(void) {
    const char データ[]="C ファイル: ja 😀\n";
    int ファイル=ファイル開放("c.txt",読取書込|作成条件未存在|切詰め内容,0600);
    if(ファイル<0)return 1;
    if(ファイルデータ書込(ファイル,データ,sizeof(データ)-1)!=sizeof(データ)-1)return 2;
    if(ファイル位置移動(ファイル,0,起点先頭)!=0)return 3;
    char 本文値読取[128]={0};int 長さ=ファイルデータ読取(ファイル,本文値読取,sizeof(本文値読取)-1);
    ファイル閉鎖(ファイル);
    if(長さ!=sizeof(データ)-1)return 4;
    for(int 数=0;数<長さ;数++)if(データ[数]!=本文値読取[数])return 5;
    return 出力(本文値読取);
}
