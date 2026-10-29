// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
import java.net.*;
public final class 連接狀態傳輸 {
    private 連接狀態傳輸() {}
    public static 連接通道 打開(String 地址, int 埠編號) throws 輸入輸出異常 {
        try { return 連接通道.打開(地址, 埠編號);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static 接收埠 打開接收者(int 埠編號) throws 輸入輸出異常 {
        try { return 接收埠.打開(埠編號);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static Socket 連接(String 地址, int 埠值) throws 輸入輸出異常 {
        try { return new Socket(地址, 埠值);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static ServerSocket 偵聽端點(int 埠值) throws 輸入輸出異常 {
        try { return new ServerSocket(埠值);
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
    public static Socket 接收(ServerSocket 服務器值) throws 輸入輸出異常 {
        try { return 服務器值.accept();
        } catch (java.io.IOException 錯誤) { throw 轉換異常.輸入輸出(錯誤); }
        catch (RuntimeException 錯誤) { throw 轉換異常.執行命令(錯誤); }
    }
}
