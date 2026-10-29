// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 連線至對端的 TCP 位元組串流端點。 */
public final class 連接通道 {
    private final java.net.Socket 標準庫橋接;
    連接通道(java.net.Socket 標準庫橋接) { this.標準庫橋接 = 標準庫橋接; }
    public static 連接通道 打開(String 地址, int 埠編號) throws 輸入輸出異常 {
        try {
            return new 連接通道(new java.net.Socket(地址, 埠編號));
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public 輸入流 輸入值() throws 輸入輸出異常 {
        try { return new 輸入流(標準庫橋接.getInputStream());
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public 輸出流 輸出() throws 輸入輸出異常 {
        try { return new 輸出流(標準庫橋接.getOutputStream());
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 超時(int 毫秒) throws 輸入輸出異常 {
        try { 標準庫橋接.setSoTimeout(毫秒);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public int 埠編號() { return 標準庫橋接.getPort(); }
    public int 局部埠編號() { return 標準庫橋接.getLocalPort(); }
    public boolean 是否已關閉() { return 標準庫橋接.isClosed(); }
    public boolean 已連接() { return 標準庫橋接.isConnected(); }
    public void 關閉() throws 輸入輸出異常 {
        try { 標準庫橋接.close();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
}
