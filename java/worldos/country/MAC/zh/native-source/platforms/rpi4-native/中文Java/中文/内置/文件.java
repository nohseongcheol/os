// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 保留用户熟悉的文件概念；当前存储是重启后消失的 RAM 文件。 */
public final class 文件 {
    private 文件() {}
    public static byte[] 读取字节值(String 名称) throws 输入输出异常 {
        try {
        FileInputStream 流值 = new FileInputStream(名称);
        try {
            byte[] 临时值 = new byte[16384]; int 数 = 0, 值;
            while ((值 = 流值.read()) != -1) { if (数 == 临时值.length) throw new 输入输出异常("文件大小限制"); 临时值[数++] = (byte)值; }
            byte[] 结果 = new byte[数]; System.arraycopy(临时值, 0, 结果, 0, 数); return 结果;
        } finally { 流值.close(); }
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static void 写入字节值(String 名称, byte[] 内容值) throws 输入输出异常 {
        try {
        FileOutputStream 流值 = new FileOutputStream(名称);
        try { for (int 循环索引 = 0; 循环索引 < 内容值.length; 循环索引++) 流值.write(内容值[循环索引] & 255); } finally { 流值.close(); }
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static String 读取(String 名称) throws 输入输出异常 {
        try { return 字符.解密数据(读取字节值(名称));
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static void 写入(String 名称, String 内容值) throws 输入输出异常 {
        try { 写入字节值(名称, 字符.编码(内容值));
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
}
