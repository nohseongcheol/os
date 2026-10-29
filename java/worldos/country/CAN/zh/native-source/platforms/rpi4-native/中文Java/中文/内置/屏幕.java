// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 独立内核的 RGB32 帧缓冲，大小在启动时选定。 */
public final class 屏幕 {
    private 屏幕() {}
    public static int 宽度值() { int 值 = 内核值.屏幕宽度(); if (值 < 0) throw new 状态异常("没有帧缓冲区"); return 值; }
    public static int 高度值() { int 值 = 内核值.屏幕高度(); if (值 < 0) throw new 状态异常("没有帧缓冲区"); return 值; }
    public static void 矩形(int 水平位置, int 垂直位置, int 宽度跨度, int 高度值, int 颜色值) {
        if (水平位置 < 0 || 垂直位置 < 0 || 宽度跨度 < 0 || 高度值 < 0 || 水平位置 > 宽度值() || 垂直位置 > 高度值() || 宽度跨度 > 宽度值() - 水平位置 || 高度值 > 高度值() - 垂直位置) throw new 无效参数异常("屏幕范围");
        if (内核值.矩形(水平位置, 垂直位置, 宽度跨度, 高度值, 颜色值) < 0) throw new 状态异常("没有帧缓冲区");
    }
    public static void 擦除条目(int 颜色值) { 矩形(0, 0, 宽度值(), 高度值(), 颜色值); }
    public static void 等待() { if (内核值.等待状态用于映像() < 0) throw new 状态异常("需要交互输入"); }
}
