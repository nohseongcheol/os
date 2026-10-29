// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 編譯器的受限 native 邊界，只負責 x86 指令與實體位址存取。 */
public final class 設備 {
    public static native int 檔案記憶體();
    public static native int Java檔案捆綁();
    public static native int Java檔案捆綁大小();
    public static native int 讀取輸入輸出位元組(int 編號);
    public static native void 寫入輸入輸出位元組(int 編號, int 值);
    public static native int 讀取記憶體(int 地址);
    public static native void 寫入記憶體(int 地址, int 值);
    public static native int 啓動標記();
    public static native int 啓動信息();
    public static native int 陣列用量();
    public static native void 掛起短暫地();
    public static native void 停機執行狀態();
    public static native void 結束操作測試(int 值);
    public static native int 讀取輸入輸出整數(int 編號);
    public static native void 寫入輸入輸出整數(int 編號, int 值);
    public static native void 寫入輸入輸出短整數(int 編號, int 值);
    public static native int 讀取輸入輸出短整數(int 編號);
    public static native void 準備用戶程式();
    public static native void 用戶清空內容();
    public static native int 運行用戶程式(int 條目地址, int 操作數棧地址);
    public static native int 毫秒();
    public static native int 用戶剩餘毫秒();
    public static native int 可執行文件捆綁();
    public static native int 可執行文件捆綁大小();
    public static native int 網路記憶體();
}
