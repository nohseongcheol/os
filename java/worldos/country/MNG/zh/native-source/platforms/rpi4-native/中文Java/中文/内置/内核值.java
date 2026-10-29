// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 自研 JVM 连接的固定 ABI，不是 JNI 或任意 native 方法加载器。 */
public final class 内核值 {
    private 内核值() {}
    public static native int 毫秒();
    public static native int 等待状态用于映像();
    public static native int 屏幕宽度();
    public static native int 屏幕高度();
    public static native int 矩形(int 水平位置, int 垂直位置, int 宽度跨度, int 高度值, int 颜色值);
}
