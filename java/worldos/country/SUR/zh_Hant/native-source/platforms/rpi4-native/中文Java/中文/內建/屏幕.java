// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 獨立核心的 RGB32 影格緩衝區，大小在啟動時選定。 */
public final class 屏幕 {
    private 屏幕() {}
    public static int 寬度值() { int 值 = 內核值.屏幕寬度(); if (值 < 0) throw new 狀態異常("沒有畫面緩衝區"); return 值; }
    public static int 高度值() { int 值 = 內核值.屏幕高度(); if (值 < 0) throw new 狀態異常("沒有畫面緩衝區"); return 值; }
    public static void 矩形(int 水平位置, int 垂直位置, int 寬度跨度, int 高度值, int 顏色值) {
        if (水平位置 < 0 || 垂直位置 < 0 || 寬度跨度 < 0 || 高度值 < 0 || 水平位置 > 寬度值() || 垂直位置 > 高度值() || 寬度跨度 > 寬度值() - 水平位置 || 高度值 > 高度值() - 垂直位置) throw new 無效實際參數異常("螢幕範圍");
        if (內核值.矩形(水平位置, 垂直位置, 寬度跨度, 高度值, 顏色值) < 0) throw new 狀態異常("沒有畫面緩衝區");
    }
    public static void 擦除條目(int 顏色值) { 矩形(0, 0, 寬度值(), 高度值(), 顏色值); }
    public static void 等待() { if (內核值.等待狀態用於映像() < 0) throw new 狀態異常("需要互動輸入"); }
}
