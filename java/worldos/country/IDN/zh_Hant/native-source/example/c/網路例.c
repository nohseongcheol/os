#include "範例約定.h"
#include <網路ABI.h>
int main(int 實際參數個數,char **實參) {
    if(實際參數個數!=2)return 輸出("사용법: ./네트워크 UDP창구번호\n");
    unsigned 埠值=0;for(int 數=0;實參[1][數];數++) {
        if(實參[1][數]<'0'||實參[1][數]>'9')return 2;
        埠值=埠值*10+實參[1][數]-'0';if(埠值>65535)return 2;
    }
    if(!埠值)return 2;
    int 端點=創建端點(互聯網族,數據報通訊端,數據報通訊協定);if(端點<0)return 3;
    struct 互聯網通訊端地址 地址={0};地址.地址族=互聯網族;
    if(綁定地址(端點,(struct 通訊端地址 *)&地址,sizeof(地址))<0)return 4;
    地址.埠編號=網路短整數(埠值);地址.互聯網地址.地址值=網路整數(0x0a000202);
    const char 數據報[]="C UDP zh_Hant";
    if(發送數據報資料(端點,數據報,sizeof(數據報)-1,0,(struct 通訊端地址 *)&地址,sizeof(地址))!=sizeof(數據報)-1)return 5;
    char 回覆[512];unsigned 運行=毫秒();int 已接收個數;
    do {
        已接收個數=接收數據報資料(端點,回覆,sizeof(回覆),0,0,0);
        if(已接收個數<0&&錯誤編號!=嘗試執行再次錯誤)return 6;
    } while(已接收個數<0&&(unsigned)(毫秒()-運行)<700);
    關閉檔案(端點);if(已接收個數!=sizeof(數據報)-1)return 7;
    for(int 數=0;數<已接收個數;數++)if(數據報[數]!=回覆[數])return 8;
    return 輸出("C 네트워크 驗證: UDP zh_Hant\n");
}
