// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 编译器的受限 native 边界，只负责 x86 指令和物理地址访问。 */
public final class 设备 {
    public static native int 文件内存();
    public static native int Java文件捆绑();
    public static native int Java文件捆绑大小();
    public static native int 读取输入输出字节(int 编号);
    public static native void 写入输入输出字节(int 编号, int 值);
    public static native int 读取内存(int 地址);
    public static native void 写入内存(int 地址, int 值);
    public static native int 启动标记();
    public static native int 启动信息();
    public static native int 数组用量();
    public static native void 挂起短暂地();
    public static native void 停机执行状态();
    public static native void 结束操作测试(int 值);
    public static native int 读取输入输出整数(int 编号);
    public static native void 写入输入输出整数(int 编号, int 值);
    public static native void 写入输入输出短整数(int 编号, int 值);
    public static native int 读取输入输出短整数(int 编号);
    public static native void 准备用户程序();
    public static native void 用户清空内容();
    public static native int 运行用户程序(int 条目地址, int 操作数栈地址);
    public static native int 毫秒();
    public static native int 用户剩余毫秒();
    public static native int 可执行文件捆绑();
    public static native int 可执行文件捆绑大小();
    public static native int 网络内存();
}
