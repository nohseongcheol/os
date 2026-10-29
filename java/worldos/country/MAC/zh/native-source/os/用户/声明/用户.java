// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros 用户 ELF 专用 API，不是 Linux/JVM 的 JNI 或 java.net API。 */
public final class 用户 {
    public static native int 打开文件描述符(int[] 文件条目名称, int 打开设置);
    public static native int 读取一文件字节(int 文件描述符);
    public static native int 写入一文件字节(int 文件描述符, int 字节值);
    public static native int 关闭文件描述符(int 文件描述符);
    public static native int 提交文件存储装置(int 文件描述符);
    public static native int 读取文件(int[] 名称, int[] 数据);
    public static native int 写入字符值(int 字符);
    public static native int 写入文件(int[] 名称, int[] 数据, int 长度);
    public static native int 写入(String 内容值);
    public static native int 参数列个数();
    public static native String 实参(int 编号);
    public static native int 执行状态权限();
    public static native int 打开网络(int 局部端口);
    public static native int 发送数据(int 句柄值, int 地址, int 目的地址端口, int[] 数据, int 长度);
    public static native int 接收数据(int 句柄值, int[] 数据, int 限制毫秒);
    public static native int 关闭网络(int 句柄值);
    public static native int 自有对象地址();
    public static native int 已发送地址(int 句柄值);
    public static native int 已发送端口(int 句柄值);
}
