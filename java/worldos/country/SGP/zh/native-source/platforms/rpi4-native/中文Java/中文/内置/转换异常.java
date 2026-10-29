// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 在中文 API 边界转换标准 Java 错误，不改变标准 catch 子句的含义。 */
final class 转换异常 {
    private 转换异常() {}
    public static 输入输出异常 输入输出(java.io.IOException 错误) {
        if (错误 instanceof 输入输出异常) return (输入输出异常)错误;
        if (错误 instanceof java.net.SocketTimeoutException) return new 等待状态超时异常("通信等待超时。");
        if (错误 instanceof java.net.UnknownHostException) return new 地址查找异常("无法解析地址。目前请使用数字形式的 IPv4 地址。");
        if (错误 instanceof java.io.FileNotFoundException) return new 缺失文件异常("无法打开文件。");
        if (错误 instanceof java.net.SocketException) return new 通信异常("通信连接操作失败: " + 错误.getMessage());
        return new 输入输出异常("输入输出操作失败: " + 错误.getMessage());
    }
    public static RuntimeException 执行命令(RuntimeException 错误) {
        if (错误 instanceof java.lang.NumberFormatException) return new 编号格式失败("请检查数字格式和范围。");
        if (错误 instanceof java.lang.IllegalArgumentException) return new 无效参数异常("请检查参数的值和范围。");
        if (错误 instanceof java.lang.ArrayIndexOutOfBoundsException) return new 数组边界异常("超出数组范围。");
        if (错误 instanceof java.lang.StringIndexOutOfBoundsException) return new 字符串边界异常("超出字符串范围。");
        if (错误 instanceof java.lang.IndexOutOfBoundsException) return new 边界异常("超出允许范围。");
        if (错误 instanceof java.lang.NullPointerException) return new 空引用引用异常("引用为空。");
        return new 执行状态异常(错误.getMessage());
    }
}
