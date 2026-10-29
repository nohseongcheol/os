#include "../命名/計算機連接名稱列.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "調用.h"
#include "檔案ABI.h"
typedef unsigned long 計算機機器字;
static 計算機機器字 堆存儲裝置[8192];static unsigned 已使用容量;
void Java失敗(void){const char 文本[]="AOT runtime error\n";寫入檔案資料(2,文本,sizeof(文本)-1);用戶調用(6,1,0,0,0,0,0);for(;;){}}
void Java壓棧(計算機機器字 *棧存儲裝置,int *深度值,計算機機器字 值){if(*深度值<0||*深度值>=128)Java失敗();棧存儲裝置[(*深度值)++]=值;}
計算機機器字 Java彈棧值(計算機機器字 *棧存儲裝置,int *深度值){if(*深度值<=0||*深度值>128)Java失敗();return 棧存儲裝置[--*深度值];}
計算機機器字 Java數組(int 項目個數){if(項目個數<0||(unsigned)項目個數+1>8192-已使用容量)Java失敗();計算機機器字*資料位置=堆存儲裝置+已使用容量;已使用容量+=項目個數+1;資料位置[0]=項目個數;return (計算機機器字)資料位置;}
計算機機器字 *Java索引(計算機機器字 物件引用,int 項目個數){計算機機器字*資料位置=(計算機機器字*)物件引用;if(!資料位置||項目個數<0||(計算機機器字)項目個數>=資料位置[0])Java失敗();return 資料位置+項目個數+1;}
int Java長度(計算機機器字 物件引用){if(!物件引用)Java失敗();return *(計算機機器字*)物件引用;}
int Java除法(int 橫座標座標,int Y_按鈕座標,int 餘數值){if(!Y_按鈕座標)Java失敗();if(橫座標座標==(-2147483647-1)&&Y_按鈕座標==-1)return 餘數值?0:橫座標座標;return 餘數值?橫座標座標%Y_按鈕座標:橫座標座標/Y_按鈕座標;}
static unsigned 長度(const char*字符串資料){unsigned 項目個數=0;if(!字符串資料)Java失敗();while(字符串資料[項目個數])項目個數++;return 項目個數;}
void Java輸出(計算機機器字 資料位置,int 數值值,int 換行){
    if(數值值){char 第二值[16];unsigned 項目個數=0;int 值=(int)資料位置;unsigned 無符號值=值<0?0-(unsigned)值:值;do{第二值[項目個數++]='0'+無符號值%10;無符號值/=10;}while(無符號值);if(值<0)第二值[項目個數++]='-';while(項目個數)寫入檔案資料(1,第二值+--項目個數,1);}
    else{const char*字符串資料=資料位置?(const char*)資料位置:"null";寫入檔案資料(1,字符串資料,長度(字符串資料));}if(換行)寫入檔案資料(1,"\n",1);
}
計算機機器字 Java文件寫入(計算機機器字 路徑,計算機機器字 值){const char*字符串資料=(const char*)值;unsigned 項目個數=長度(字符串資料);int 檔案句柄=打開檔案((const char*)路徑,寫入僅用值|創建條件缺失|截斷內容,0600);if(檔案句柄<0)Java失敗();int 已返回值=寫入檔案資料(檔案句柄,字符串資料,項目個數);關閉檔案(檔案句柄);if(已返回值!=(int)項目個數)Java失敗();return 0;}
計算機機器字 Java文件讀取(計算機機器字 路徑){int 檔案句柄=打開檔案((const char*)路徑,讀取僅用值,0);if(檔案句柄<0)Java失敗();int 項目個數=檔案大小(檔案句柄);if(項目個數<0||項目個數>16384||(unsigned)(項目個數+8)/8>8192-已使用容量)Java失敗();char*資料位置=(char*)(堆存儲裝置+已使用容量);已使用容量+=(項目個數+8)/8;int 已返回值=讀取檔案資料(檔案句柄,資料位置,項目個數);關閉檔案(檔案句柄);if(已返回值!=項目個數)Java失敗();資料位置[項目個數]=0;return (計算機機器字)資料位置;}
