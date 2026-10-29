// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 由自製 JVM 直接建立與繪製的中文 API 畫面元素。 */
public final class 標籤 extends 屏幕元素 {
    public 標籤(String 文本, int 水平位置, int 垂直位置, int 寬度跨度, int 高度值) {
        throw new 狀態異常("自有 JVM 需要支援建立中文 API 介面元素。");
    }
}
