// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 機器邊界，不把指標截斷成 Java int。 */
public final class 板 {
    public static native int 讀取顯示操作像素(int 水平位置, int 垂直位置);
    public static native void 寫入顯示操作像素(int 水平位置, int 垂直位置, int 顏色值);
    public static native int 遠程控制(int 種類值, int 動作);
    public static native void 結束遠程命令(int 狀態值);
    public static native void 遠程等待狀態(int 狀態值);
    public static native void 寫入串行(int 值);
    public static native int 讀取串行();
    public static native int 毫秒();
    public static native int CPU特權級別();
    public static native int 準備屏幕();
    public static native int 屏幕寬度();
    public static native int 屏幕高度();
    public static native void 放入屏幕像素(int 水平位置, int 垂直位置, int 顏色值);
    public static native void 掛起處理器();
    public static native int 創建任務(int 編號);
    public static native int 任務狀態(int 編號);
    public static native void 停止(int 狀態值);
    public static native int 測試Cpp();
    public static native int 運行用戶程式(int 編號);
    public static native int 檢查用戶程式();
    public static native int 準備參數列(int 項目個數);
    public static native int 執行用戶檔案();
    public static native int 執行Linux檔案();
    public static native int 實際參數位元組(int 編號, int 位置, int 值);
    public static native int 終端(int 動作);
    public static native int 控制用戶程式(int 動作);
    public static native void 切換輸入輸出(int 動作);
    public static native int 檔案傳送服務(int 動作);
    public static native int 網路運行狀態(int 條目值, int 編號);
    public static native int 網路設置(int 動作, int 地址, int 掩碼值, int 網關值);
    public static native int 發送響應(int 地址, int 排序值);
    public static native int 讀取響應(int 條目值);
    public static native int 查詢系統(int 條目值, int 編號);
    public static native void 電源關閉側();
}
