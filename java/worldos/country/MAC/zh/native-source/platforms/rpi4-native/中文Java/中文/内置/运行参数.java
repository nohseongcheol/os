// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 自研 JVM 传给入口方法的命令行参数，不包含类名。 */
public final class 运行参数 {
    private 运行参数() {}
    public static native int 项目个数();
    public static native String 文本(int 序数索引) throws 边界异常;
}
