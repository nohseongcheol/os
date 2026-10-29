// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
import java.net.*;
public final class 连接状态传输 {
    private 连接状态传输() {}
    public static 连接通道 打开(String 地址, int 端口编号) throws 输入输出异常 {
        try { return 连接通道.打开(地址, 端口编号);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static 接收端口 打开接收者(int 端口编号) throws 输入输出异常 {
        try { return 接收端口.打开(端口编号);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static Socket 连接(String 地址, int 端口值) throws 输入输出异常 {
        try { return new Socket(地址, 端口值);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static ServerSocket 侦听端点(int 端口值) throws 输入输出异常 {
        try { return new ServerSocket(端口值);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public static Socket 接收(ServerSocket 服务器值) throws 输入输出异常 {
        try { return 服务器值.accept();
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
}
