// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 由自研 JVM 直接创建和绘制的中文 API 界面元素。 */
public final class 标签 extends 屏幕元素 {
    public 标签(String 文本, int 水平位置, int 垂直位置, int 宽度跨度, int 高度值) {
        throw new 状态异常("自有 JVM 需要支持创建中文 API 界面元素。");
    }
}
