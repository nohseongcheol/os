// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 在自製畫面中傳送動作通知的按鈕。 */
public final class 按鈕 extends 屏幕元素 {
    public 按鈕(String 文本, int 水平位置, int 垂直位置, int 寬度跨度, int 高度值, 動作接收者 接收者值) {
        throw new 狀態異常("自有 JVM 需要支援建立中文 API 按鈕。");
    }
    public native void 設定動作接收者(動作接收者 接收者值);
}
