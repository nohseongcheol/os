// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 直接连接自研 JVM 和内核窗口管理功能的窗口。 */
public final class 窗口 extends 屏幕元素 {
    public 窗口(String 窗口标题, int 宽度跨度, int 高度值) {
        throw new 状态异常("自有 JVM 需要支持创建中文 API 窗口。");
    }
    public native void 添加元素(屏幕元素 元素值);
    public native void 显示窗口();
    public native void 关闭();
    public native boolean 是否可见();
}
