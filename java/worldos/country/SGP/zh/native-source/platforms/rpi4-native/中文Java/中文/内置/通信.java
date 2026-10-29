// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4 UDP 报文通信；外部对端使用数字地址。 */
public final class 通信 {
    private 通信() {}
    public static DatagramSocket 打开(int 端口值) throws 输入输出异常 {
        try { return new DatagramSocket(端口值);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static void 发送(DatagramSocket 端点, int 端口值, String 内容值) throws 输入输出异常 {
        try {
        发送(端点, "127.0.0.1", 端口值, 内容值);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static void 发送(DatagramSocket 端点, String 地址, int 端口值, String 内容值) throws 输入输出异常 {
        try {
        byte[] 字节值 = 字符.编码(内容值);
        端点.send(new DatagramPacket(字节值, 字节值.length, InetAddress.getByName(地址), 端口值));
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static String 接收(DatagramSocket 端点) throws 输入输出异常 {
        try {
        byte[] 字节值 = new byte[512]; DatagramPacket 数据报 = new DatagramPacket(字节值, 字节值.length); 端点.receive(数据报);
        byte[] 结果 = new byte[数据报.getLength()]; System.arraycopy(字节值, 0, 结果, 0, 结果.length); return 字符.解密数据(结果);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static void 超时(DatagramSocket 端点, int 毫秒) throws 输入输出异常 {
        try { 端点.setSoTimeout(毫秒);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static void 关闭(DatagramSocket 端点) { 端点.close(); }
}
