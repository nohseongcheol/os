// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 自製 JVM 畫面物件的共同契約，不保存標準 Swing 物件。 */
public abstract class 屏幕元素 {
    public native String 讀取文本();
    public native void 寫入文本(String 文本);
    public native void 設定邊界(int 水平位置, int 垂直位置, int 寬度跨度, int 高度值);
}
