// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 保留报文边界、用于收发 UDP 数据的端点。 */
public final class 数据报信道 {
    private final java.net.DatagramSocket 标准端点;
    private 数据报信道(int 端口编号) throws 输入输出异常 {
        try { 标准端点 = 通信.打开(端口编号);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static 数据报信道 打开(int 端口编号) throws 输入输出异常 {
        try { return new 数据报信道(端口编号);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 发送(String 地址, int 端口编号, String 数据) throws 输入输出异常 {
        try { 通信.发送(标准端点, 地址, 端口编号, 数据);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public String 接收() throws 输入输出异常 {
        try { return 通信.接收(标准端点);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 超时(int 毫秒) throws 输入输出异常 {
        try { 通信.超时(标准端点, 毫秒);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public int 端口编号() { return 标准端点.getLocalPort(); }
    public boolean 是否已关闭() { return 标准端点.isClosed(); }
    public void 关闭() { 通信.关闭(标准端点); }
}
