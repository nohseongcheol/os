// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 保留使用者熟悉的檔案概念；目前儲存是重新啟動後消失的 RAM 檔案。 */
public final class 檔案 {
    private 檔案() {}
    public static byte[] 讀取位元組值(String 名稱) throws 輸入輸出異常 {
        try {
        FileInputStream 流值 = new FileInputStream(名稱);
        try {
            byte[] 臨時值 = new byte[16384]; int 數 = 0, 值;
            while ((值 = 流值.read()) != -1) { if (數 == 臨時值.length) throw new 輸入輸出異常("檔案大小限制"); 臨時值[數++] = (byte)值; }
            byte[] 結果 = new byte[數]; System.arraycopy(臨時值, 0, 結果, 0, 數); return 結果;
        } finally { 流值.close(); }
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static void 寫入位元組值(String 名稱, byte[] 內容值) throws 輸入輸出異常 {
        try {
        FileOutputStream 流值 = new FileOutputStream(名稱);
        try { for (int 循環索引 = 0; 循環索引 < 內容值.length; 循環索引++) 流值.write(內容值[循環索引] & 255); } finally { 流值.close(); }
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static String 讀取(String 名稱) throws 輸入輸出異常 {
        try { return 字元.解密資料(讀取位元組值(名稱));
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static void 寫入(String 名稱, String 內容值) throws 輸入輸出異常 {
        try { 寫入位元組值(名稱, 字元.編碼(內容值));
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
}
