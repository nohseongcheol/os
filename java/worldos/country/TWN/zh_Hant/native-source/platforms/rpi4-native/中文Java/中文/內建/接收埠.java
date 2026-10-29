// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 接受傳入的 TCP 連線。 */
public final class 接收埠 {
    private final java.net.ServerSocket 標準埠;
    private 接收埠(int 埠編號) throws 輸入輸出異常 {
        try { 標準埠 = new java.net.ServerSocket(埠編號);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static 接收埠 打開(int 埠編號) throws 輸入輸出異常 {
        try { return new 接收埠(埠編號);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public 連接通道 接收() throws 輸入輸出異常 {
        try { return new 連接通道(標準埠.accept());
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public int 埠編號() { return 標準埠.getLocalPort(); }
    public void 超時(int 毫秒) throws 輸入輸出異常 {
        try { 標準埠.setSoTimeout(毫秒);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public boolean 是否已關閉() { return 標準埠.isClosed(); }
    public void 關閉() throws 輸入輸出異常 {
        try { 標準埠.close();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
}
