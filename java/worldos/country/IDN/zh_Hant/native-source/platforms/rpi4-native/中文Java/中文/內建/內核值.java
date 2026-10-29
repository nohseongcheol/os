// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 自製 JVM 連接的固定 ABI，不是 JNI 或任意 native 方法載入器。 */
public final class 內核值 {
    private 內核值() {}
    public static native int 毫秒();
    public static native int 等待狀態用於映像();
    public static native int 屏幕寬度();
    public static native int 屏幕高度();
    public static native int 矩形(int 水平位置, int 垂直位置, int 寬度跨度, int 高度值, int 顏色值);
}
