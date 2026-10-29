#include "範例約定.h"
int main(void) {
    const char 資料[]="C 檔案: zh_Hant 😀\n";
    int 檔案=打開檔案("c.txt",讀取寫入|創建條件缺失|截斷內容,0600);
    if(檔案<0)return 1;
    if(寫入檔案資料(檔案,資料,sizeof(資料)-1)!=sizeof(資料)-1)return 2;
    if(尋道檔案(檔案,0,起點開頭)!=0)return 3;
    char 讀取文本值[128]={0};int 長度=讀取檔案資料(檔案,讀取文本值,sizeof(讀取文本值)-1);
    關閉檔案(檔案);
    if(長度!=sizeof(資料)-1)return 4;
    for(int 數=0;數<長度;數++)if(資料[數]!=讀取文本值[數])return 5;
    return 輸出(讀取文本值);
}
