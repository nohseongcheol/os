// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 由自製 JVM 排程器管理的執行流程，不包裝標準 Thread。 */
public final class 後臺任務 {
    public 後臺任務(可運行任務任務 任務動作) {
        throw new 狀態異常("自有 JVM 需要支援建立中文 API 執行緒。");
    }
    public native void 開始任務() throws 執行緒狀態異常;
    public native void 等待() throws 等待狀態已中斷異常;
    public native boolean 是否存活();
    public static native void 掛起任務();
}
