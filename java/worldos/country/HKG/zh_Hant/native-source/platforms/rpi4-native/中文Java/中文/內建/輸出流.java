// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 保持順序寫出位元組的通道。 */
public final class 輸出流 {
    private final java.io.OutputStream 標準流;
    輸出流(java.io.OutputStream 標準流) { this.標準流 = 標準流; }
    public void 寫入(int 值) throws 輸入輸出異常 {
        try { 標準流.write(值);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 寫入(byte[] 資料) throws 輸入輸出異常 {
        try { 標準流.write(資料);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 寫入(byte[] 資料, int 運行, int 長度) throws 輸入輸出異常 {
        try { 標準流.write(資料, 運行, 長度);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 發射值() throws 輸入輸出異常 {
        try { 標準流.flush();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public void 關閉() throws 輸入輸出異常 {
        try { 標準流.close();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
}
