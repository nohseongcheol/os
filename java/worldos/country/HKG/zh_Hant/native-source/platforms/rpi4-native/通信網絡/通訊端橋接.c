#include "../命名/計算機連接名稱列.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "通信網絡.h"
extern int32_t Java迴環網絡通訊端(int32_t,int32_t,int32_t), Java迴環網絡綁定(int32_t,int32_t,int32_t);
extern int32_t Java迴環網絡發送(int32_t,int32_t,int32_t,int32_t), Java迴環網絡接收操作(int32_t,int32_t);
extern int32_t Java迴環網絡埠(int32_t), Java迴環網絡地址(int32_t), Java迴環網絡對端(int32_t), Java迴環網絡關閉(int32_t);
extern int32_t Java網絡放入(int32_t,int32_t),Java網絡獲取(int32_t);
extern int32_t Java迴環流創建(void),Java迴環流綁定(int32_t,int32_t,int32_t),Java迴環流偵聽(int32_t,int32_t);
extern int32_t Java迴環流連接(int32_t,int32_t,int32_t),Java迴環流接受(int32_t),Java迴環流讀取(int32_t,int32_t),Java迴環流寫入(int32_t,int32_t);
extern int32_t Java迴環流埠(int32_t),Java迴環流對端(int32_t),Java迴環流關閉(int32_t);
static int 外部[24];
static int 任意地址[24], 雙重偵聽器[24], UDP外部對端[8], 已綁定地址[8];
static int 外部編號(int 檔案句柄) { return 檔案句柄>=32 && 檔案句柄<56 ? 外部[檔案句柄-32]-1 : -1; }
static int 粘貼文本(int 檔案句柄,int 類型分類) {
    if(檔案句柄<32||檔案句柄>=56)return -9;int 上一個項目=外部編號(檔案句柄);if(上一個項目>=0)return 上一個項目;
    int 項目個數=創建通訊端端點(類型分類);if(項目個數>=0)外部[檔案句柄-32]=項目個數+1;return 項目個數;
}
int32_t Java網絡通訊端(int32_t 首位值,int32_t 第二值,int32_t 字元程式碼){return Java迴環網絡通訊端(首位值,第二值,字元程式碼);}
int32_t Java網絡綁定(int32_t 檔案句柄,int32_t 互聯網地址,int32_t 埠編號){
    if(互聯網地址==0x7f000001)return Java迴環網絡綁定(檔案句柄,互聯網地址,埠編號);
    if(互聯網地址!=0&&互聯網地址!=讀取網路運行狀態(0,0))return -99;
    int 已返回值=Java迴環網絡綁定(檔案句柄,0,埠編號);if(已返回值<0)return 已返回值;
    int 項目個數=粘貼文本(檔案句柄,2);if(項目個數<0)return 項目個數;已返回值=網路層綁定(項目個數,讀取網路運行狀態(0,0),Java迴環網絡埠(檔案句柄));if(!已返回值)已綁定地址[檔案句柄-32]=互聯網地址;return 已返回值;
}
int32_t Java網絡發送(int32_t 檔案句柄,int32_t 互聯網地址,int32_t 埠編號,int32_t 大小){
    if(互聯網地址==0x7f000001)return Java迴環網絡發送(檔案句柄,互聯網地址,埠編號,大小);
    if(大小<0||大小>512)return -90;if(埠編號<1||埠編號>65535)return -22;
    if(Java迴環網絡埠(檔案句柄)<0)return -9;
    if(Java迴環網絡地址(檔案句柄)==0x7f000001)return -101;
    int 項目個數=外部編號(檔案句柄);if(項目個數<0){int 已返回值=0;if(Java迴環網絡埠(檔案句柄)==0)已返回值=Java迴環網絡綁定(檔案句柄,0,0);if(已返回值<0)return 已返回值;項目個數=粘貼文本(檔案句柄,2);if(項目個數<0)return 項目個數;已返回值=網路層綁定(項目個數,讀取網路運行狀態(0,0),Java迴環網絡埠(檔案句柄));if(已返回值<0)return 已返回值;}
    unsigned char 資料[512];for(int 序數索引=0;序數索引<大小;序數索引++)資料[序數索引]=Java網絡獲取(序數索引);return 發送數據報(項目個數,資料,大小,互聯網地址,埠編號);
}
int32_t Java網絡接收操作(int32_t 檔案句柄,int32_t 大小){
    int 項目個數=外部編號(檔案句柄);if(項目個數<0)return Java迴環網絡接收操作(檔案句柄,大小);if(大小<0||大小>512)return -22;
    int 局部=Java迴環網絡接收操作(檔案句柄,大小);if(局部!=-11){UDP外部對端[檔案句柄-32]=0;return 局部;}
    unsigned char 資料[512];int 已返回值=接收數據報(項目個數,資料,大小);if(已返回值>=0)UDP外部對端[檔案句柄-32]=1;for(int 序數索引=0;序數索引<已返回值;序數索引++)Java網絡放入(序數索引,資料[序數索引]);return 已返回值;
}
int32_t Java網絡埠(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);return 項目個數<0?Java迴環網絡埠(檔案句柄):(int32_t)網路埠編號(項目個數);}
int32_t Java網絡地址(int32_t 檔案句柄){return 外部編號(檔案句柄)<0?Java迴環網絡地址(檔案句柄):已綁定地址[檔案句柄-32];}
int32_t Java網絡對端(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);return 項目個數<0||!UDP外部對端[檔案句柄-32]?Java迴環網絡對端(檔案句柄):(int32_t)對端埠編號(項目個數);}
int32_t Java網絡遠程(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);return 項目個數<0||!UDP外部對端[檔案句柄-32]?0x7f000001:(int32_t)網路層對端地址(項目個數);}
int32_t Java網絡關閉(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);if(項目個數>=0){關閉網路(項目個數);外部[檔案句柄-32]=0;}if(檔案句柄>=32&&檔案句柄<40)UDP外部對端[檔案句柄-32]=已綁定地址[檔案句柄-32]=0;return Java迴環網絡關閉(檔案句柄);}
int32_t Java流創建(void){return Java迴環流創建();}
int32_t Java流綁定(int32_t 檔案句柄,int32_t 互聯網地址,int32_t 埠編號){
    if(互聯網地址==0||互聯網地址==0x7f000001){int 已返回值=Java迴環流綁定(檔案句柄,互聯網地址,埠編號);if(!已返回值)任意地址[檔案句柄-32]=互聯網地址==0;return 已返回值;}
    if(互聯網地址!=讀取網路運行狀態(0,0))return -99;int 已返回值=Java迴環流綁定(檔案句柄,0,埠編號);if(已返回值<0)return 已返回值;
    int 項目個數=粘貼文本(檔案句柄,1);return 項目個數<0?項目個數:網路層綁定(項目個數,互聯網地址,Java迴環流埠(檔案句柄));
}
int32_t Java流偵聽(int32_t 檔案句柄,int32_t 待接隊列長度){
    int 項目個數=外部編號(檔案句柄);if(項目個數<0){int 已返回值=Java迴環流偵聽(檔案句柄,待接隊列長度);if(已返回值<0||!任意地址[檔案句柄-32])return 已返回值;
        項目個數=粘貼文本(檔案句柄,1);if(項目個數<0)return 項目個數;已返回值=網路層綁定(項目個數,讀取網路運行狀態(0,0),Java迴環流埠(檔案句柄));if(已返回值<0)return 已返回值;雙重偵聽器[檔案句柄-32]=1;
    }return 待接隊列長度<1?-22:網路層偵聽(項目個數);
}
int32_t Java流連接(int32_t 檔案句柄,int32_t 互聯網地址,int32_t 埠編號){
    if(互聯網地址==0x7f000001 && 外部編號(檔案句柄)<0)return Java迴環流連接(檔案句柄,互聯網地址,埠編號);
    if(Java迴環流埠(檔案句柄)<0)return -9;int 項目個數=粘貼文本(檔案句柄,1);return 項目個數<0?項目個數:網路層連接(項目個數,互聯網地址,埠編號);
}
int32_t Java流接受(int32_t 檔案句柄){
    int 項目個數=外部編號(檔案句柄);if(項目個數<0)return Java迴環流接受(檔案句柄);
    if(雙重偵聽器[檔案句柄-32]){int 局部=Java迴環流接受(檔案句柄);if(局部!=-11)return 局部;}
    int 對端值=網路層接受(項目個數);if(對端值<0)return 對端值;
    int 目標值=Java迴環流創建();if(目標值<0){關閉網路(對端值);return 目標值;}外部[目標值-32]=對端值+1;return 目標值;
}
int32_t Java流讀取(int32_t 檔案句柄,int32_t 大小){
    int 項目個數=外部編號(檔案句柄);if(項目個數<0)return Java迴環流讀取(檔案句柄,大小);if(大小<0||大小>512)return -22;
    unsigned char 資料[512];int 已返回值=網路層讀取(項目個數,資料,大小);for(int 序數索引=0;序數索引<已返回值;序數索引++)Java網絡放入(序數索引,資料[序數索引]);return 已返回值;
}
int32_t Java流寫入(int32_t 檔案句柄,int32_t 大小){
    int 項目個數=外部編號(檔案句柄);if(項目個數<0)return Java迴環流寫入(檔案句柄,大小);if(大小<0||大小>512)return -22;
    unsigned char 資料[512];for(int 序數索引=0;序數索引<大小;序數索引++)資料[序數索引]=Java網絡獲取(序數索引);return 網路層寫入(項目個數,資料,大小);
}
int32_t Java流埠(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);return 項目個數<0?Java迴環流埠(檔案句柄):(int32_t)網路埠編號(項目個數);}
int32_t Java流對端(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);return 項目個數<0?Java迴環流對端(檔案句柄):(int32_t)對端埠編號(項目個數);}
int32_t Java流地址(int32_t 檔案句柄){return 外部編號(檔案句柄)<0?0x7f000001:雙重偵聽器[檔案句柄-32]?0:讀取網路運行狀態(0,0);}
int32_t Java流關閉(int32_t 檔案句柄){int 項目個數=外部編號(檔案句柄);if(項目個數>=0){關閉網路(項目個數);外部[檔案句柄-32]=0;}if(檔案句柄>=40&&檔案句柄<56)任意地址[檔案句柄-32]=雙重偵聽器[檔案句柄-32]=0;return Java迴環流關閉(檔案句柄);}
