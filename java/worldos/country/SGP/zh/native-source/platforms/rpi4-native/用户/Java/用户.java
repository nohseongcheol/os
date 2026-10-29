// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 Java 工具专用的 SVC 桥接，与现有 x86 工具源码一同构建。 */
public final class 用户 {
    public static native int 打开文件描述符(int[] 名称, int 设置);
    public static native int 读取一文件字节(int 描述符条目);
    public static native int 写入一文件字节(int 描述符条目, int 值);
    public static native int 关闭文件描述符(int 描述符条目);
    public static native int 读取文件(int[] 名称, int[] 数据);
    public static native int 写入文件(int[] 名称, int[] 数据, int 长度);
    public static native int 写入(String 文本);
    public static native int 写入字符值(int 值);
    public static native int 参数列个数();
    public static native String 实参(int 编号);
    public static native int 工具编号();
    public static native int 屏幕连接状态(int 动作, int 编号, int 首位操作数, int 第二操作数, int 第三操作数, int 第四操作数);
    public static native int 屏幕文本(int 编号, int[] 文本, int 长度);
    public static native int 屏幕宽度();
    public static native int 屏幕高度();
    public static native int 流控制(int 动作, int 描述符条目, int 值);
    public static native int 连接流(int 描述符条目, int 地址, int 端口值);
    public static native int 打开网络(int 端口值);
    public static native int 发送网络(int 描述符条目, int 地址, int 端口值, int[] 数据, int 长度);
    public static native int 接收网络(int 描述符条目, int[] 数据, int 长度);
    public static native int 网络端口(int 描述符条目);
    public static native int 毫秒();
    public static native int 等待状态用于映像();
    public static native int 矩形(int 水平位置, int 垂直位置, int 宽度跨度, int 高度值, int 颜色值);
}
