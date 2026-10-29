// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 執行緒是一條執行流程；自製 JVM 依已執行指令數輪流執行各執行緒。 */
public final class 任務 {
    private 任務() {}
    public static 後臺任務 運行(可運行任務任務 任務動作) { 後臺任務 執行緒值 = new 後臺任務(任務動作); 執行緒值.開始任務(); return 執行緒值; }
    public static void 等待(後臺任務 執行緒值) throws 等待狀態已中斷異常 { 執行緒值.等待(); }
    public static boolean 是否存活(後臺任務 執行緒值) { return 執行緒值.是否存活(); }
    public static void 掛起任務() { 後臺任務.掛起任務(); }
}
