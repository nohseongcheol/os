// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 自研 JVM 界面对象的公共契约，不保存标准 Swing 对象。 */
public abstract class 屏幕元素 {
    public native String 读取文本();
    public native void 写入文本(String 文本);
    public native void 设定边界(int 水平位置, int 垂直位置, int 宽度跨度, int 高度值);
}
