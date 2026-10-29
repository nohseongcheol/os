// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 保留資料報邊界、用於收發 UDP 資料的端點。 */
public final class 數據報信道 {
    private final java.net.DatagramSocket 標準端點;
    private 數據報信道(int 埠編號) throws 輸入輸出異常 {
        try { 標準端點 = 通信.打開(埠編號);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static 數據報信道 打開(int 埠編號) throws 輸入輸出異常 {
        try { return new 數據報信道(埠編號);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 發送(String 地址, int 埠編號, String 資料) throws 輸入輸出異常 {
        try { 通信.發送(標準端點, 地址, 埠編號, 資料);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public String 接收() throws 輸入輸出異常 {
        try { return 通信.接收(標準端點);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 超時(int 毫秒) throws 輸入輸出異常 {
        try { 通信.超時(標準端點, 毫秒);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public int 埠編號() { return 標準端點.getLocalPort(); }
    public boolean 是否已關閉() { return 標準端點.isClosed(); }
    public void 關閉() { 通信.關閉(標準端點); }
}
