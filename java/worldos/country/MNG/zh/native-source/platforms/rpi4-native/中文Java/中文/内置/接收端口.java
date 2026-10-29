// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 接受传入的 TCP 连接。 */
public final class 接收端口 {
    private final java.net.ServerSocket 标准端口;
    private 接收端口(int 端口编号) throws 输入输出异常 {
        try { 标准端口 = new java.net.ServerSocket(端口编号);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static 接收端口 打开(int 端口编号) throws 输入输出异常 {
        try { return new 接收端口(端口编号);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public 连接通道 接收() throws 输入输出异常 {
        try { return new 连接通道(标准端口.accept());
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public int 端口编号() { return 标准端口.getLocalPort(); }
    public void 超时(int 毫秒) throws 输入输出异常 {
        try { 标准端口.setSoTimeout(毫秒);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public boolean 是否已关闭() { return 标准端口.isClosed(); }
    public void 关闭() throws 输入输出异常 {
        try { 标准端口.close();
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
}
