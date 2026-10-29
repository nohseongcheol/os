// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 机器边界，不把指针截断成 Java int。 */
public final class 板 {
    public static native int 读取显示操作像素(int 水平位置, int 垂直位置);
    public static native void 写入显示操作像素(int 水平位置, int 垂直位置, int 颜色值);
    public static native int 远程控制(int 种类值, int 动作);
    public static native void 结束远程命令(int 状态值);
    public static native void 远程等待状态(int 状态值);
    public static native void 写入串行(int 值);
    public static native int 读取串行();
    public static native int 毫秒();
    public static native int CPU特权级别();
    public static native int 准备屏幕();
    public static native int 屏幕宽度();
    public static native int 屏幕高度();
    public static native void 放入屏幕像素(int 水平位置, int 垂直位置, int 颜色值);
    public static native void 挂起处理器();
    public static native int 创建任务(int 编号);
    public static native int 任务状态(int 编号);
    public static native void 停止(int 状态值);
    public static native int 测试Cpp();
    public static native int 运行用户程序(int 编号);
    public static native int 检查用户程序();
    public static native int 准备参数列(int 项目个数);
    public static native int 执行用户文件();
    public static native int 执行Linux文件();
    public static native int 参数字节(int 编号, int 位置, int 值);
    public static native int 终端(int 动作);
    public static native int 控制用户程序(int 动作);
    public static native void 切换输入输出(int 动作);
    public static native int 文件传送服务(int 动作);
    public static native int 网络运行状态(int 条目值, int 编号);
    public static native int 网络设置(int 动作, int 地址, int 掩码值, int 网关值);
    public static native int 发送响应(int 地址, int 排序值);
    public static native int 读取响应(int 条目值);
    public static native int 查询系统(int 条目值, int 编号);
    public static native void 电源关闭侧();
}
