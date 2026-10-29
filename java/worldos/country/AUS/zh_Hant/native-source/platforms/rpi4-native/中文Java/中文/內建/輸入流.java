// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 依序讀取傳入位元組的通道。 */
public final class 輸入流 {
    private final java.io.InputStream 標準流;
    輸入流(java.io.InputStream 標準流) { this.標準流 = 標準流; }
    public int 讀取() throws 輸入輸出異常 {
        try { return 標準流.read();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public int 讀取(byte[] 資料) throws 輸入輸出異常 {
        try { return 標準流.read(資料);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public int 讀取(byte[] 資料, int 運行, int 長度) throws 輸入輸出異常 {
        try { return 標準流.read(資料, 運行, 長度);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 關閉() throws 輸入輸出異常 {
        try { 標準流.close();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
}
