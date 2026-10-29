// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.JPN.l_ja;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class 体系呼出し {
    private 体系呼出し() { }
    public static RandomAccessFile 開く(String 経路, String 方式) throws IOException {
        return new RandomAccessFile(経路, 方式);
    }
    public static int 読む(RandomAccessFile 文書, byte[] 資料) throws IOException {
        return 文書.read(資料);
    }
    public static void 書く(RandomAccessFile 文書, byte[] 資料) throws IOException {
        文書.write(資料);
    }
    public static void 位置を移す(RandomAccessFile 文書, long 位置) throws IOException {
        文書.seek(位置);
    }
    public static void 記録を同期する(RandomAccessFile 文書) throws IOException {
        文書.getFD().sync();
    }
    public static void 閉じる(RandomAccessFile 文書) throws IOException {
        文書.close();
    }
    public static void 削除する(String 経路) throws IOException {
        Files.delete(Paths.get(経路));
    }
    public static long 大きさ(String 経路) throws IOException {
        return Files.size(Paths.get(経路));
    }
    public static Socket 接続する(String 住所, int 通信口番号) throws IOException {
        return new Socket(住所, 通信口番号);
    }
    public static DatagramSocket 独立電文(int 通信口番号) throws SocketException {
        return new DatagramSocket(通信口番号);
    }
    public static Thread 実行の糸(Runnable 動作) {
        Thread 実行の糸 = new Thread(動作);
        実行の糸.start();
        return 実行の糸;
    }
    public static Process 実行する(List<String> 命令) throws IOException {
        return new ProcessBuilder(命令).start();
    }
}
