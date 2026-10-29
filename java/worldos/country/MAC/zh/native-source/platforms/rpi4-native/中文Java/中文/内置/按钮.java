// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 在自研界面中发送动作通知的按钮。 */
public final class 按钮 extends 屏幕元素 {
    public 按钮(String 文本, int 水平位置, int 垂直位置, int 宽度跨度, int 高度值, 动作接收者 接收者值) {
        throw new 状态异常("自有 JVM 需要支持创建中文 API 按钮。");
    }
    public native void 设定动作接收者(动作接收者 接收者值);
}
