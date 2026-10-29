// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 直接連接自製 JVM 與核心視窗管理功能的視窗。 */
public final class 窗口 extends 屏幕元素 {
    public 窗口(String 窗口標題, int 寬度跨度, int 高度值) {
        throw new 狀態異常("自有 JVM 需要支援建立中文 API 視窗。");
    }
    public native void 添加元素(屏幕元素 元素值);
    public native void 顯示窗口();
    public native void 關閉();
    public native boolean 是否可見();
}
