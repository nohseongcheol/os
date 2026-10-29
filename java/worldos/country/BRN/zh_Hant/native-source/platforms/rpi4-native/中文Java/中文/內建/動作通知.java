// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 由自製 JVM 事件處理器產生的動作通知。 */
public final class 動作通知 {
    private 動作通知() {}
    public native String 命令文本();
    public native 屏幕元素 事件原始碼();
    public native int 編號();
}
