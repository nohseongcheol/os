// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4 UDP 資料報通訊；外部對端使用數字位址。 */
public final class 通信 {
    private 通信() {}
    public static DatagramSocket 打開(int 埠值) throws 輸入輸出異常 {
        try { return new DatagramSocket(埠值);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static void 發送(DatagramSocket 端點, int 埠值, String 內容值) throws 輸入輸出異常 {
        try {
        發送(端點, "127.0.0.1", 埠值, 內容值);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static void 發送(DatagramSocket 端點, String 地址, int 埠值, String 內容值) throws 輸入輸出異常 {
        try {
        byte[] 位元組值 = 字元.編碼(內容值);
        端點.send(new DatagramPacket(位元組值, 位元組值.length, InetAddress.getByName(地址), 埠值));
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static String 接收(DatagramSocket 端點) throws 輸入輸出異常 {
        try {
        byte[] 位元組值 = new byte[512]; DatagramPacket 數據報 = new DatagramPacket(位元組值, 位元組值.length); 端點.receive(數據報);
        byte[] 結果 = new byte[數據報.getLength()]; System.arraycopy(位元組值, 0, 結果, 0, 結果.length); return 字元.解密資料(結果);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static void 超時(DatagramSocket 端點, int 毫秒) throws 輸入輸出異常 {
        try { 端點.setSoTimeout(毫秒);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static void 關閉(DatagramSocket 端點) { 端點.close(); }
}
