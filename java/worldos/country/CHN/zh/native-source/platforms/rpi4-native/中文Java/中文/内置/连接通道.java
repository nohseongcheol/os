// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 连接到对端的 TCP 字节流端点。 */
public final class 连接通道 {
    private final java.net.Socket 标准库桥接;
    连接通道(java.net.Socket 标准库桥接) { this.标准库桥接 = 标准库桥接; }
    public static 连接通道 打开(String 地址, int 端口编号) throws 输入输出异常 {
        try {
            return new 连接通道(new java.net.Socket(地址, 端口编号));
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public 输入流 输入值() throws 输入输出异常 {
        try { return new 输入流(标准库桥接.getInputStream());
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public 输出流 输出() throws 输入输出异常 {
        try { return new 输出流(标准库桥接.getOutputStream());
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 超时(int 毫秒) throws 输入输出异常 {
        try { 标准库桥接.setSoTimeout(毫秒);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public int 端口编号() { return 标准库桥接.getPort(); }
    public int 局部端口编号() { return 标准库桥接.getLocalPort(); }
    public boolean 是否已关闭() { return 标准库桥接.isClosed(); }
    public boolean 已连接() { return 标准库桥接.isConnected(); }
    public void 关闭() throws 输入输出异常 {
        try { 标准库桥接.close();
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
}
