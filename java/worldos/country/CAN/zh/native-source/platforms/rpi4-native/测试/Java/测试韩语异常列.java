// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.内置.*;

public class 测试韩语异常列 {
    static void 默认超时() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 异常");
    }
    public static void main(String[] 实参) throws 输入输出异常 {
        try { throw new 等待状态超时异常("等待状态状态 结尾"); }
        catch (等待状态超时异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 地址查找异常("地址 失败值"); }
        catch (输入输出异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 缺失文件异常("文件 失败值"); }
        catch (java.io.IOException 错误) { 输出.写入行("표준 상위 异常 호환"); }
        try { 默认超时(); }
        catch (等待状态超时异常 曾经已捕获错误地) { 输出.写入行("잘못된 备用名称"); }
        catch (java.io.IOException 原始错误) { 输出.写入行("中文 예외의 독립된 类型分类"); }
        try { 文件.读取("없는한글파일"); }
        catch (缺失文件异常 错误) { 输出.写入行("文件 错误 中文 转换值"); }
        try { 字符.解析整数("숫자가아님"); }
        catch (编号格式失败 错误) { 输出.写入行("数字值 错误 中文 转换值"); }
        try { 检查项.确认真值(false, "检查项 失败值"); }
        catch (无效参数异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 数组边界异常("裁剪 失败值"); }
        catch (边界异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 空引用引用异常("빈 引用"); }
        catch (java.lang.RuntimeException 错误) { 输出.写入行("执行命令 异常 호환"); }
        try { throw new 异常("직접 정의한 说明"); }
        catch (异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 线程状态异常("线程状态异常"); }
        catch (线程状态异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 等待状态超时异常("等待状态超时异常"); }
        catch (等待状态超时异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 等待状态已中断异常("等待状态已中断异常"); }
        catch (等待状态已中断异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 字符串边界异常("字符串边界异常"); }
        catch (字符串边界异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 数组边界异常("数组边界异常"); }
        catch (数组边界异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 数组存储失败("数组存储失败"); }
        catch (数组存储失败 错误) { 输出.写入行(错误.说明()); }
        try { throw new 边界异常("边界异常"); }
        catch (边界异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 空引用引用异常("空引用引用异常"); }
        catch (空引用引用异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 算术失败("算术失败"); }
        catch (算术失败 错误) { 输出.写入行(错误.说明()); }
        try { throw new 状态异常("状态异常"); }
        catch (状态异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 编号格式失败("编号格式失败"); }
        catch (编号格式失败 错误) { 输出.写入行(错误.说明()); }
        try { throw new 执行状态异常("执行状态异常"); }
        catch (执行状态异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 异常("异常"); }
        catch (异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 负数数组大小失败("负数数组大小失败"); }
        catch (负数数组大小失败 错误) { 输出.写入行(错误.说明()); }
        try { throw new 输入输出异常("输入输出异常"); }
        catch (输入输出异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 无效参数异常("无效参数异常"); }
        catch (无效参数异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 地址查找异常("地址查找异常"); }
        catch (地址查找异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 通信异常("通信异常"); }
        catch (通信异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 缺失文件异常("缺失文件异常"); }
        catch (缺失文件异常 错误) { 输出.写入行(错误.说明()); }
        try { throw new 类型类型转换异常("类型类型转换异常"); }
        catch (类型类型转换异常 错误) { 输出.写入行(错误.说明()); }
        输出.写入行("中文 异常 进程值条目 是否完成");
    }
}
