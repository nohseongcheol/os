// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 保持顺序写出字节的通道。 */
public final class 输出流 {
    private final java.io.OutputStream 标准流;
    输出流(java.io.OutputStream 标准流) { this.标准流 = 标准流; }
    public void 写入(int 值) throws 输入输出异常 {
        try { 标准流.write(值);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 写入(byte[] 数据) throws 输入输出异常 {
        try { 标准流.write(数据);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 写入(byte[] 数据, int 运行, int 长度) throws 输入输出异常 {
        try { 标准流.write(数据, 运行, 长度);
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 发射值() throws 输入输出异常 {
        try { 标准流.flush();
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
    public void 关闭() throws 输入输出异常 {
        try { 标准流.close();
        } catch (java.io.IOException 错误) { throw 转换异常.输入输出(错误); }
        catch (RuntimeException 错误) { throw 转换异常.执行命令(错误); }
    }
}
