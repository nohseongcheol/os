// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GUF.l_zh_Hant;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class 系統呼叫 {
    private 系統呼叫() { }
    public static RandomAccessFile 開啟(String 路徑, String 方式) throws IOException {
        return new RandomAccessFile(路徑, 方式);
    }
    public static int 讀取(RandomAccessFile 檔案, byte[] 資料) throws IOException {
        return 檔案.read(資料);
    }
    public static void 寫入(RandomAccessFile 檔案, byte[] 資料) throws IOException {
        檔案.write(資料);
    }
    public static void 定位(RandomAccessFile 檔案, long 位置) throws IOException {
        檔案.seek(位置);
    }
    public static void 同步(RandomAccessFile 檔案) throws IOException {
        檔案.getFD().sync();
    }
    public static void 關閉(RandomAccessFile 檔案) throws IOException {
        檔案.close();
    }
    public static void 刪除(String 路徑) throws IOException {
        Files.delete(Paths.get(路徑));
    }
    public static long 大小(String 路徑) throws IOException {
        return Files.size(Paths.get(路徑));
    }
    public static Socket 連線(String 位址, int 通訊埠號碼) throws IOException {
        return new Socket(位址, 通訊埠號碼);
    }
    public static DatagramSocket 獨立電文(int 通訊埠號碼) throws SocketException {
        return new DatagramSocket(通訊埠號碼);
    }
    public static Thread 執行緒(Runnable 動作) {
        Thread 執行緒 = new Thread(動作);
        執行緒.start();
        return 執行緒;
    }
    public static Process 執行(List<String> 命令) throws IOException {
        return new ProcessBuilder(命令).start();
    }
}
