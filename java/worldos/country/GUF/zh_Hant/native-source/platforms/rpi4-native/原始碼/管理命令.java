// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 管理命令 {
    static String 已完成機器字() { return "網路設定 網路位址 回聲測試 路由表 網路狀態 行程列表 執行概況 記憶體狀態 儲存容量 運作時間 關機 說明"; }
    static String 機器字文本(int 編號) {
        if (編號==0) return "網路設定";
        if (編號==1) return "網路位址";
        if (編號==2) return "回聲測試";
        if (編號==3) return "路由表";
        if (編號==4) return "網路狀態";
        if (編號==5) return "行程列表";
        if (編號==6) return "執行概況";
        if (編號==7) return "記憶體狀態";
        if (編號==8) return "儲存容量";
        if (編號==9) return "運作時間";
        if (編號==10) return "關機";
        return "說明";
    }
    static String 說明(int 編號) {
        if (編號==0) return "IPv4 地址、子網路遮罩與閘道設定";
        if (編號==1) return "IPv4 介面與路由工具";
        if (編號==2) return "ICMP 回聲與往返時間";
        if (編號==3) return "直接連線網路與預設路由";
        if (編號==4) return "TCP/UDP 連線與流量";
        if (編號==5) return "核心工作與使用者行程";
        if (編號==6) return "更新工作和記憶體; q 或 Ctrl+C 離開";
        if (編號==7) return "實際核心記憶體池與使用者映射";
        if (編號==8) return "RAM 檔案系統容量和檔案槽";
        if (編號==9) return "啟動後的運作時間";
        if (編號==10) return "關閉系統; RAM 檔案不會保留";
        return "命令與中文名稱";
    }
}
